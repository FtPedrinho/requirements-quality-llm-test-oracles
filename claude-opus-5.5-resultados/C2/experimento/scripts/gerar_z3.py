# -*- coding: utf-8 -*-
"""Formalização SMT-LIB das restrições do oráculo C2 e execução do Z3 independente.

Não usa nenhum código do SUT (mcdc-*). O parser abaixo é próprio, escrito a partir
dos operadores listados na fonte C2 (and/&&//\\, or/||/\\/, not/!, =,==,!=,<,<=,>,>=).
Ele RECUSA cadeias que misturam and/or sem parênteses, porque a precedência não é
legível na fonte C2 (trecho "Precedênca ( ates de )"); todas as fórmulas usadas aqui
são totalmente parentizadas nesse aspecto.

Para cada consulta grava <id>.smt2 e <id>.out em experimento/z3/ e um resumo
em experimento/z3/resumo-z3.json.
"""
import itertools
import json
import os
import re
import subprocess
import sys

Z3 = "C:/Users/User/AppData/Roaming/Python/bin/z3.exe"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
ZDIR = os.path.join(BASE, "z3")
ENT = os.path.join(BASE, "entradas")
os.makedirs(ZDIR, exist_ok=True)

# ------------------------------------------------------------------ parser
TOK = re.compile(r"\s*(/\\|\\/|&&|\|\||==|!=|<=|>=|:=|[()<>=!]|-?\d+(?:\.\d+)?|[A-Za-z_][A-Za-z0-9_]*)")
AND = {"and", "&&", "/\\"}
OR = {"or", "||", "\\/"}
NOT = {"not", "!"}
CMP = {"=", "==", "!=", "<", "<=", ">", ">="}


def tokenize(s):
    pos, out = 0, []
    s = s.strip()
    while pos < len(s):
        m = TOK.match(s, pos)
        if not m:
            raise ValueError("token inválido em %r pos %d" % (s, pos))
        out.append(m.group(1))
        pos = m.end()
        while pos < len(s) and s[pos].isspace():
            pos += 1
    return out


class P:
    def __init__(self, s):
        self.t = tokenize(s)
        self.i = 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else None

    def nxt(self):
        x = self.peek()
        self.i += 1
        return x

    def parse(self):
        e = self.expr()
        if self.peek() is not None:
            raise ValueError("sobra: %r" % self.t[self.i:])
        return e

    def expr(self):
        items = [self.unary()]
        op = None
        while self.peek() in AND or self.peek() in OR:
            o = "and" if self.peek() in AND else "or"
            if op is not None and o != op:
                raise ValueError("mistura and/or sem parênteses (precedência não determinada pela fonte C2)")
            op = o
            self.nxt()
            items.append(self.unary())
        return items[0] if op is None else (op, items)

    def unary(self):
        t = self.peek()
        if t in NOT:
            self.nxt()
            return ("not", self.unary())
        if t == "(":
            self.nxt()
            e = self.expr()
            if self.nxt() != ")":
                raise ValueError("falta )")
            return e
        lhs = self.nxt()
        if self.peek() in CMP:
            op = self.nxt()
            rhs = self.nxt()
            op = "=" if op == "==" else op
            return ("atom", "%s %s %s" % (lhs, op, rhs), (lhs, op, rhs))
        return ("atom", lhs, (lhs, None, None))


def atoms_of(e, acc):
    if e[0] == "atom":
        acc.append(e)
    elif e[0] == "not":
        atoms_of(e[1], acc)
    else:
        for x in e[1]:
            atoms_of(x, acc)
    return acc


def eval_bool(e, val):  # val: key -> bool
    if e[0] == "atom":
        return val[e[1]]
    if e[0] == "not":
        return not eval_bool(e[1], val)
    if e[0] == "and":
        return all(eval_bool(x, val) for x in e[1])
    return any(eval_bool(x, val) for x in e[1])


def smt_bool(e, name):  # fórmula sobre booleanos de entrada b_<idx>
    if e[0] == "atom":
        return name(e[1])
    if e[0] == "not":
        return "(not %s)" % smt_bool(e[1], name)
    return "(%s %s)" % (e[0], " ".join(smt_bool(x, name) for x in e[1]))


# ------------------------------------------------------------- tipos/domínio
def is_num(s):
    return re.fullmatch(r"-?\d+(\.\d+)?", s or "") is not None


def num(s, sort):
    neg = s.startswith("-")
    a = s[1:] if neg else s
    if sort == "Real" and "." not in a:
        a = a + ".0"
    return "(- %s)" % a if neg else a


class Dom:
    """Declarações SMT de variáveis concretas a partir dos tipos (JSON) ou inferidos."""

    def __init__(self, inputs=None, atoms=()):
        self.sorts = {}
        self.enums = {}
        if inputs:
            for i in inputs:
                t = i["type"]
                if t == "bool":
                    self.sorts[i["name"]] = "Bool"
                elif t == "int":
                    self.sorts[i["name"]] = "Int"
                elif t == "real":
                    self.sorts[i["name"]] = "Real"
                elif t == "enum":
                    self.sorts[i["name"]] = "E_" + i["name"]
                    self.enums[i["name"]] = list(i["values"])
        else:
            # expressão direta: tipos não declarados na fonte; inferência da formalização
            # (comparação com número -> Int; identificador isolado -> Bool;
            # comparação com identificador -> domínio textual aberto).
            for a in atoms:
                l, op, r = a[2]
                if op is None:
                    self.sorts.setdefault(l, "Bool")
                elif is_num(r):
                    self.sorts.setdefault(l, "Int")
                else:
                    self.enums.setdefault(l, [])
                    if r not in self.enums[l]:
                        self.enums[l].append(r)
            for v in self.enums:
                self.enums[v].append("outro_valor")
                self.sorts[v] = "E_" + v

    def decls(self, suf=""):
        out = []
        for v, s in self.sorts.items():
            out.append("(declare-const %s%s %s)" % (v, suf, s))
        return out

    def datatypes(self):
        out = []
        for v, vals in self.enums.items():
            out.append("(declare-datatypes () ((E_%s %s)))" % (v, " ".join("%s__%s" % (v, x) for x in vals)))
        return out

    def atom(self, a, suf=""):
        l, op, r = a[2]
        lv = l + suf
        if op is None:
            return lv
        s = self.sorts.get(l)
        if s is None:
            raise ValueError("variável sem tipo: %s" % l)
        if s == "Bool":
            rv = "true" if r == "true" else "false" if r == "false" else r + suf
        elif s in ("Int", "Real"):
            rv = num(r, s) if is_num(r) else r + suf
        else:
            rv = "%s__%s" % (l, r) if r in self.enums[l] else r + suf
        if op == "=":
            return "(= %s %s)" % (lv, rv)
        if op == "!=":
            return "(not (= %s %s))" % (lv, rv)
        return "(%s %s %s)" % (op, lv, rv)


# ------------------------------------------------------------------ runner Z3
RESUMO = {"z3": None, "consultas": {}}


def run_z3(qid, lines, nota=""):
    txt = "; consulta %s -- %s\n" % (qid, nota) + "\n".join(lines) + "\n"
    p = os.path.join(ZDIR, qid + ".smt2")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    r = subprocess.run([Z3, "-smt2", p], capture_output=True, text=True, timeout=120)
    out = r.stdout
    with open(os.path.join(ZDIR, qid + ".out"), "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
        if r.stderr:
            f.write("\n;; stderr\n" + r.stderr)
    res = [l.strip() for l in out.splitlines() if l.strip() in ("sat", "unsat", "unknown")]
    if "unknown" in res or r.returncode not in (0, 1):
        print("ERRO TÉCNICO Z3", qid, r.returncode, out[:300])
    return out, res


# ------------------------------------------------------------------ análises
def entries(e):
    occ = atoms_of(e, [])
    keys = []
    for a in occ:
        if a[1] not in keys:
            keys.append(a[1])
    return occ, keys


def feasibility(qid, guard, inputs=None, extra=None, nota=""):
    """Para cada combinação das entradas distintas, sat/unsat das restrições de domínio."""
    e = P(guard).parse()
    occ, keys = entries(e)
    rep = {a[1]: a for a in occ}
    d = Dom(inputs, occ)
    lines = ["(set-logic ALL)"] + d.datatypes() + d.decls()
    rows = list(itertools.product([True, False], repeat=len(keys)))  # linha 0 = tudo verdadeiro
    for r in rows:
        lines.append("(push)")
        for k, v in zip(keys, r):
            a = d.atom(rep[k])
            lines.append("(assert %s)" % (a if v else "(not %s)" % a))
        if extra:
            lines.append("(assert %s)" % extra(d, rep, keys, r))
        lines.append("(check-sat)")
        lines.append("(pop)")
    out, res = run_z3(qid, lines, nota)
    imp = [i for i, x in enumerate(res) if x == "unsat"]
    info = {"guarda": guard, "entradas": keys, "condicoes": len(occ), "combinacoes": len(rows),
            "impossiveis": len(imp), "linhas_impossiveis": [dict(zip(keys, rows[i])) for i in imp],
            "respostas": {"sat": res.count("sat"), "unsat": res.count("unsat"), "unknown": res.count("unknown")}}
    RESUMO["consultas"][qid] = info
    return info


def pairs_unique(qid, guard, inputs=None, constraint=None, free=False, nota=""):
    """Existência de par de causa única para cada entrada não repetida:
    duas atribuições concretas (sufixos _1/_2) em que só o átomo da entrada muda e o
    resultado da guarda muda. free=True ignora o domínio (átomos como booleanos livres)."""
    e = P(guard).parse()
    occ, keys = entries(e)
    rep = {a[1]: a for a in occ}
    cnt = {k: sum(1 for a in occ if a[1] == k) for k in keys}
    d = Dom(inputs, occ)
    res_by = {}
    lines_all = ["(set-logic ALL)"] + d.datatypes()
    if free:
        bdecl = []
        for s in ("_1", "_2"):
            for i, k in enumerate(keys):
                bdecl.append("(declare-const b%d%s Bool)" % (i, s))
        lines_all += bdecl
    else:
        lines_all += d.decls("_1") + d.decls("_2")
    cons = None
    if constraint:
        ce = P(constraint).parse()
        cons = ce
    order = []
    for idx, k in enumerate(keys):
        if cnt[k] != 1:
            continue
        order.append(k)

        def nm(s):
            if free:
                return lambda key: "b%d%s" % (keys.index(key), s)
            return lambda key: d.atom(rep[key], s) if key in rep else d.atom(P(key).parse(), s)
        n1, n2 = nm("_1"), nm("_2")
        lines_all.append("(push)")
        lines_all.append("(assert %s)" % n1(k))
        lines_all.append("(assert (not %s))" % n2(k))
        for k2 in keys:
            if k2 != k:
                lines_all.append("(assert (= %s %s))" % (n1(k2), n2(k2)))
        lines_all.append("(assert (distinct %s %s))" % (smt_bool(e, n1), smt_bool(e, n2)))
        if cons is not None:
            lines_all.append("(assert %s)" % smt_bool(cons, n1))
            lines_all.append("(assert %s)" % smt_bool(cons, n2))
        lines_all.append("(check-sat)")
        lines_all.append("(pop)")
    out, res = run_z3(qid, lines_all, nota)
    for k, r in zip(order, res):
        res_by[k] = r
    info = {"guarda": guard, "restricao": constraint, "livre": free, "par_causa_unica": res_by,
            "entradas_repetidas_nao_avaliadas": [k for k in keys if cnt[k] != 1]}
    RESUMO["consultas"][qid] = info
    return info


def min_suite_unique(qid, guard, nota=""):
    """Tamanho mínimo de suíte em que cada condição tem par de causa única (Z3 decide)."""
    e = P(guard).parse()
    occ, keys = entries(e)
    n = len(keys)
    rows = list(itertools.product([True, False], repeat=n))
    args = " ".join("(b%d Bool)" % i for i in range(n))
    nm = lambda key: "b%d" % keys.index(key)
    lines = ["(set-logic ALL)", "(define-fun f (%s) Bool %s)" % (args, smt_bool(e, nm))]
    for i in range(len(rows)):
        lines.append("(declare-const s%d Bool)" % i)

    def call(r):
        return "(f %s)" % " ".join("true" if v else "false" for v in r)
    for ci in range(n):
        alts = []
        for i, r in enumerate(rows):
            if not r[ci]:
                continue
            r2 = list(r)
            r2[ci] = False
            j = rows.index(tuple(r2))
            alts.append("(and s%d s%d (distinct %s %s))" % (i, j, call(r), call(tuple(r2))))
        lines.append("(assert (or %s))" % " ".join(alts) if alts else "(assert false)")
    total = "(+ %s)" % " ".join("(ite s%d 1 0)" % i for i in range(len(rows)))
    found = None
    ks = list(range(1, len(rows) + 1))
    for k in ks:
        lines.append("(push)")
        lines.append("(assert (<= %s %d))" % (total, k))
        lines.append("(check-sat)")
        lines.append("(pop)")
    out, res = run_z3(qid, lines, nota)
    for k, r in zip(ks, res):
        if r == "sat":
            found = k
            break
    info = {"guarda": guard, "minimo_causa_unica": found,
            "respostas_por_k": dict(zip([str(k) for k in ks], res))}
    RESUMO["consultas"][qid] = info
    return info


def single(qid, lines, nota, parse=None):
    out, res = run_z3(qid, ["(set-logic ALL)"] + lines, nota)
    info = {"respostas": res, "saida": out.strip()}
    if parse:
        info.update(parse(out, res))
    RESUMO["consultas"][qid] = info
    return info


# ---------------------------------------------------------- sistemas (JSON)
def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def actions(dec):
    out = {}
    for a in dec.get("actions", []):
        l, r = [x.strip() for x in a.split(":=")]
        out[l] = r
    return out


def system_analysis(sid, path):
    data = load(path)
    tot = {"requisitos": len(data["decisions"]), "condicoes": 0, "combinacoes": 0, "impossiveis": 0}
    pares = {}
    for dec in data["decisions"]:
        q = "%s-%s-viab" % (sid, dec["id"].replace("#", "_"))
        inf = feasibility(q, dec["guard"], data["inputs"], nota="viabilidade das combinações de %s" % dec["id"])
        tot["condicoes"] += inf["condicoes"]
        tot["combinacoes"] += inf["combinacoes"]
        tot["impossiveis"] += inf["impossiveis"]
        q2 = "%s-%s-pares" % (sid, dec["id"].replace("#", "_"))
        pi = pairs_unique(q2, dec["guard"], data["inputs"], nota="par de causa única viável por entrada de %s" % dec["id"])
        pares[dec["id"]] = pi
    RESUMO["consultas"]["%s-totais" % sid] = tot
    # conflitos: pares de decisões cujas guardas podem valer juntas e que escrevem
    # valores diferentes na mesma variável.
    decs = data["decisions"]
    occ_all = []
    for dd in decs:
        occ_all += atoms_of(P(dd["guard"]).parse(), [])
    d = Dom(data["inputs"], occ_all)
    lines = d.datatypes() + d.decls()
    cand = []
    for i in range(len(decs)):
        for j in range(i + 1, len(decs)):
            ai, aj = actions(decs[i]), actions(decs[j])
            diff = [v for v in ai if v in aj and ai[v] != aj[v]]
            if not diff:
                continue
            gi = smt_bool(P(decs[i]["guard"]).parse(), lambda k: d.atom(P(k).parse()))
            gj = smt_bool(P(decs[j]["guard"]).parse(), lambda k: d.atom(P(k).parse()))
            cand.append((decs[i]["id"], decs[j]["id"], diff))
            lines += ["(push)", "(assert %s)" % gi, "(assert %s)" % gj, "(check-sat)", "(pop)"]
    out, res = run_z3("%s-conflitos" % sid, ["(set-logic ALL)"] + lines,
                      "sobreposição de guardas com ações de valores diferentes")
    conf = [c for c, r in zip(cand, res) if r == "sat"]
    RESUMO["consultas"]["%s-conflitos" % sid] = {"candidatos": len(cand), "conflitos": len(conf),
                                                 "pares": [[a, b, v] for a, b, v in conf]}
    return data, tot, pares


def guards_or(data, d):
    gs = [smt_bool(P(x["guard"]).parse(), lambda k: d.atom(P(k).parse())) for x in data["decisions"]]
    return "(or %s)" % " ".join(gs)


def lacuna(qid, path, context, nota):
    data = load(path)
    occ = []
    for dd in data["decisions"]:
        occ += atoms_of(P(dd["guard"]).parse(), [])
    occ += atoms_of(P(context).parse(), [])
    d = Dom(data["inputs"], occ)
    ctx = smt_bool(P(context).parse(), lambda k: d.atom(P(k).parse()))
    lines = d.datatypes() + d.decls() + ["(assert %s)" % ctx, "(assert (not %s))" % guards_or(data, d),
                                         "(check-sat)", "(get-model)"]
    return single(qid, lines, nota, lambda o, r: {"lacuna_existe": bool(r) and r[0] == "sat"})


def main():
    v = subprocess.run([Z3, "--version"], capture_output=True, text=True).stdout.strip()
    RESUMO["z3"] = v
    G = load(os.path.join(ENT, "expressoes-geradas.json"))
    EX = os.path.join(REPO, "exemplos")

    # Q01-Q03: pares de causa única (pure Boolean) para expressões do texto
    pairs_unique("Q01-AB-or-C-pares", "(A and B) or C", nota="A01/A02/F*: par de causa única por condição")
    pairs_unique("Q02-A-and-notB-pares", "A and not B", nota="A03/A05")
    pairs_unique("Q03-speed-mode-pares", "speed > 100 and mode = idle", nota="A06 (forma 'and' equivalente a /\\)")
    pairs_unique("Q04-eq-ne-pares", "(x = 5) and (y != 3)", nota="A07")
    pairs_unique("Q05-lt-le-ge-pares", "(a < 1) or ((b <= 2) and (c >= 3))", nota="A08")
    feasibility("Q06-repetida-tabela", "(A and B) or ((not A) and C)", nota="A09: 2^3 combinações sobre entradas distintas")
    feasibility("Q07-paridade-tabela", G["paridade3"], nota="A15: tabela de 8 combinações da paridade")
    for nm in ("e20", "e13", "e26"):
        pairs_unique("Q08-%s-pares" % nm, G[nm], free=True, nota="A16/A18/A19: par de causa única por entrada")
    # bloqueio e redundância
    pairs_unique("Q09-bloqueio-viavel", "x > 5 and x > 3", nota="A21/A22: com domínio inteiro")
    pairs_unique("Q09-bloqueio-livre", "x > 5 and x > 3", free=True, nota="A21/A22: sem restrição de domínio")
    feasibility("Q09-bloqueio-tabela", "x > 5 and x > 3", nota="A22: combinações impossíveis")
    pairs_unique("Q10-redundante-livre", "A or (A and B)", free=True, nota="A23: B sem par mesmo com todas as combinações")
    # restrição escrita à mão
    pairs_unique("Q11-restricao-pares", "A or (B and C)", constraint="(not A) or B", free=True,
                 nota="A24: pares respeitando a restrição not A or B")
    pairs_unique("Q12-restricao-bloqueio", "A and B", constraint="(not A) or B", free=True,
                 nota="A25: com restrição")
    pairs_unique("Q12-restricao-bloqueio-livre", "A and B", free=True, nota="A25: sem restrição")
    # Z3 + fronteira
    feasibility("Q13-speed-rain-tabela", "speed > 100 or (speed > 50 and rain)", nota="A27/F04")
    pairs_unique("Q13-speed-rain-pares", "speed > 100 or (speed > 50 and rain)", nota="A27")
    for c, k in (("100", "101"), ("50", "51")):
        single("Q14-fronteira-gt%s" % c,
               ["(declare-const x Int)", "(declare-const y Int)",
                "(push)", "(assert (> x %s))" % c, "(assert (not (> (- x 1) %s)))" % c,
                "(check-sat)", "(get-value (x))", "(assert (distinct x %s))" % k, "(check-sat)", "(pop)",
                "(push)", "(assert (not (> y %s)))" % c, "(assert (> (+ y 1) %s))" % c,
                "(check-sat)", "(get-value (y))", "(assert (distinct y %s))" % c, "(check-sat)", "(pop)"],
               "A28: menor valor que satisfaz e maior que não satisfaz speed > %s (inteiros)" % c)
    # suítes exatas (causa única)
    min_suite_unique("Q15-exata-AB-or-C", "(A and B) or C", nota="A31")
    min_suite_unique("Q16-exata-AorB-and-CorD", "(A or B) and (C or D)", nota="A32")
    min_suite_unique("Q17-exata-A-and-BorC", "A and (B or C)", nota="A33")
    min_suite_unique("Q18-exata-A-and-notB", "A and not B", nota="A03 (referência)")
    pairs_unique("Q19-mutacao-pares", "A and (B or C)", nota="A36")
    # sistemas de exemplo
    system_analysis("VM", os.path.join(EX, "vm-decisoes.json"))
    system_analysis("NPP", os.path.join(EX, "npp-decisoes.json"))
    system_analysis("TIS", os.path.join(EX, "tis-decisoes.json"))
    lacuna("Q20-VM-lacuna-preparing_weak", os.path.join(EX, "vm-decisoes.json"),
           "the_system_mode = preparing_weak", "V04: existe situação no contexto em que nenhuma guarda vale")
    # enum
    feasibility("Q21-enum-tabela", "m = a \\/ m = b", load(os.path.join(ENT, "j15-enum.json"))["inputs"], nota="J15")
    pairs_unique("Q21-enum-pares", "m = a \\/ m = b", load(os.path.join(ENT, "j15-enum.json"))["inputs"], nota="J15")
    # verify próprios
    for sid, f, ctx in (("V05", "v05-conflito.json", None), ("V06", "v06-mesmo-valor.json", "mode = idle"),
                        ("V07", "v07-disjuntos.json", "mode = idle")):
        system_analysis(sid, os.path.join(ENT, f))
        if ctx:
            lacuna("Q22-%s-lacuna" % sid, os.path.join(ENT, f), ctx, "%s: lacuna no contexto" % sid)
    # check: avaliação das guardas nos testes do CSV
    dj = load(os.path.join(EX, "decisoes.json"))
    occ = []
    for dd in dj["decisions"]:
        occ += atoms_of(P(dd["guard"]).parse(), [])
    d = Dom(dj["inputs"], occ)
    g3 = smt_bool(P(dj["decisions"][2]["guard"]).parse(), lambda k: d.atom(P(k).parse()))
    g1 = smt_bool(P(dj["decisions"][0]["guard"]).parse(), lambda k: d.atom(P(k).parse()))
    tests = {
        "T1": (g1, {"the_system_mode": "the_system_mode__idle", "the_coin_sensor": "true"}),
        "T2": (g1, {"the_system_mode": "the_system_mode__idle", "the_coin_sensor": "false"}),
        "T3": (g3, {"the_system_mode": "the_system_mode__choice", "the_coffee_request_button": "true", "the_coin_sensor": "false"}),
        "T4": (g3, {"the_system_mode": "the_system_mode__idle", "the_coffee_request_button": "true", "the_coin_sensor": "false"}),
    }
    lines = d.datatypes() + d.decls()
    for t, (g, vals) in tests.items():
        lines += ["(push)"] + ["(assert (= %s %s))" % (k, v) for k, v in vals.items()] + \
                 ["(check-sat)", "(get-value (%s))" % g, "(pop)"]
    single("Q23-check-exemplo", lines, "C01: valor da guarda em T1..T4 de exemplos/testes.csv")
    dc = load(os.path.join(ENT, "c06-concretos.json"))
    d2 = Dom(dc["inputs"], atoms_of(P(dc["decisions"][0]["guard"]).parse(), []))
    g = smt_bool(P(dc["decisions"][0]["guard"]).parse(), lambda k: d2.atom(P(k).parse()))
    lines = d2.datatypes() + d2.decls()
    for x, y in ((7, "true"), (3, "true"), (7, "false")):
        lines += ["(push)", "(assert (= x %d))" % x, "(assert (= y %s))" % y, "(check-sat)", "(get-value (%s))" % g, "(pop)"]
    single("Q24-check-concretos", lines, "C06: valor da guarda em T1..T3")
    pairs_unique("Q25-check-AandB-pares", "A and B", nota="C02-C04: pares de causa única de A and B")

    with open(os.path.join(ZDIR, "resumo-z3.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(RESUMO, f, ensure_ascii=False, indent=2)
    print(json.dumps({k: v for k, v in RESUMO["consultas"].items() if k.endswith("totais") or "conflitos" in k or "Q15" in k or "Q16" in k or "Q17" in k or "Q18" in k}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
