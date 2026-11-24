# -*- coding: utf-8 -*-
"""Gera as consultas SMT-LIB do oráculo C4 e executa o Z3 independente (z3.exe 5.4.1).

Independente do SUT: o parser de expressões abaixo é próprio desta execução e não
usa nenhum código dos módulos mcdc-*. As entradas lidas são apenas os arquivos de
exemplos/ citados pela fonte C4 (vm/tis/npp-decisoes.json, decisoes.json,
testes.csv, requisitos.mcdc).

Uso: python gerar_e_executar.py <raiz-do-repositorio> <z3.exe>
Gera em ./consultas/*.smt2 e ./saidas/*.out e grava ./resumo.json.
"""
import itertools
import json
import os
import re
import subprocess
import sys

RAIZ = sys.argv[1]
Z3 = sys.argv[2]
AQUI = os.path.dirname(os.path.abspath(__file__))
CONS = os.path.join(AQUI, "consultas")
SAI = os.path.join(AQUI, "saidas")
os.makedirs(CONS, exist_ok=True)
os.makedirs(SAI, exist_ok=True)

# ---------------------------------------------------------------- parser próprio
TOK = re.compile(r"\s*(/\\|\\/|\(|\)|<=|>=|!=|<|>|=|[A-Za-z_][A-Za-z0-9_]*|-?[0-9]+(?:\.[0-9]+)?)")


def tokenize(s):
    pos, out = 0, []
    s = s.strip()
    while pos < len(s):
        m = TOK.match(s, pos)
        if not m:
            raise ValueError("token inválido em %r pos %d" % (s, pos))
        out.append(m.group(1))
        pos = m.end()
    return out


class P:
    """Gramática: or := and (('or'|'\\/') and)* ; and := un (('and'|'/\\') un)* ;
    un := 'not' un | '(' or ')' | atom ; atom := ID [op valor]"""

    def __init__(self, s):
        self.t = tokenize(s)
        self.i = 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else None

    def eat(self, x=None):
        v = self.peek()
        if x is not None and v != x:
            raise ValueError("esperado %r, obtido %r" % (x, v))
        self.i += 1
        return v

    def parse(self):
        e = self.p_or()
        if self.peek() is not None:
            raise ValueError("sobra: %r" % self.peek())
        return e

    def p_or(self):
        e = self.p_and()
        while self.peek() in ("or", "\\/"):
            self.eat()
            e = ("or", e, self.p_and())
        return e

    def p_and(self):
        e = self.p_un()
        while self.peek() in ("and", "/\\"):
            self.eat()
            e = ("and", e, self.p_un())
        return e

    def p_un(self):
        v = self.peek()
        if v == "not":
            self.eat()
            return ("not", self.p_un())
        if v == "(":
            self.eat("(")
            e = self.p_or()
            self.eat(")")
            return e
        name = self.eat()
        if self.peek() in ("=", "!=", "<", "<=", ">", ">="):
            op = self.eat()
            val = self.eat()
            return ("atom", "%s %s %s" % (name, op, val), (name, op, val))
        return ("atom", name, None)


def occurrences(e, acc=None):
    if acc is None:
        acc = []
    if e[0] == "atom":
        acc.append(e[1])
    elif e[0] == "not":
        occurrences(e[1], acc)
    else:
        occurrences(e[1], acc)
        occurrences(e[2], acc)
    return acc


def distinct(e):
    out = []
    for a in occurrences(e):
        if a not in out:
            out.append(a)
    return out


def smt_bool(e, name_of):
    """Expressão booleana em SMT-LIB sobre variáveis booleanas (uma por entrada distinta)."""
    if e[0] == "atom":
        return name_of(e[1])
    if e[0] == "not":
        return "(not %s)" % smt_bool(e[1], name_of)
    return "(%s %s %s)" % (e[0], smt_bool(e[1], name_of), smt_bool(e[2], name_of))


def pyeval(e, env):
    if e[0] == "atom":
        return env[e[1]]
    if e[0] == "not":
        return not pyeval(e[1], env)
    a, b = pyeval(e[1], env), pyeval(e[2], env)
    return (a and b) if e[0] == "and" else (a or b)


def run_z3(nome, texto):
    p = os.path.join(CONS, nome + ".smt2")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)
    r = subprocess.run([Z3, "-smt2", p], capture_output=True, text=True, timeout=600)
    out = r.stdout
    with open(os.path.join(SAI, nome + ".out"), "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
        if r.stderr:
            f.write("\n;; stderr\n" + r.stderr)
    return [l.strip() for l in out.splitlines() if l.strip()]


def bvar(i):
    return "b%d" % i


resumo = {}

# ------------------------------------------------- Q01: tabela-verdade de expressões próprias
# Regra do texto: n entradas distintas -> 2^n combinações; resultado da decisão em cada uma.
# Linha 0 = tudo verdadeiro (TruthTableTest). Ordem das linhas seguinte não é usada.
proprias = {
    "E1": "x and y and z",
    "E2": "x or y",
    "E3": "(p and q) or (not p and r)",
    "E4": "p or (q and r)",
}
for k, s in proprias.items():
    e = P(s).parse()
    ins = distinct(e)
    occ = occurrences(e)
    linhas = []
    txt = ["; Q01-%s: avaliacao de cada combinacao de %r" % (k, s), "(set-option :produce-models true)"]
    for i, n in enumerate(ins):
        txt.append("(declare-const %s Bool) ; %s" % (bvar(i), n))
    txt.append("(declare-const d Bool)")
    txt.append("(assert (= d %s))" % smt_bool(e, lambda a: bvar(ins.index(a))))
    combos = list(itertools.product([True, False], repeat=len(ins)))  # linha 0 = tudo verdadeiro
    for c in combos:
        txt.append("(push)")
        for i, v in enumerate(c):
            txt.append("(assert (= %s %s))" % (bvar(i), "true" if v else "false"))
        txt.append("(check-sat)")
        txt.append("(get-value (d))")
        txt.append("(pop)")
    out = run_z3("Q01-" + k, "\n".join(txt) + "\n")
    vals = [l for l in out if l.startswith("((d")]
    sats = [l for l in out if l in ("sat", "unsat", "unknown")]
    res = []
    for c, v in zip(combos, vals):
        res.append({"linha": dict(zip(ins, c)), "decisao": "true" in v})
    resumo["Q01-" + k] = {
        "expressao": s,
        "entradas_distintas": ins,
        "condicoes(aparicoes)": occ,
        "combinacoes": len(combos),
        "respostas": sorted(set(sats)),
        "linhas": res,
        "quantidade_decisao_falsa": sum(1 for r in res if not r["decisao"]),
        "quantidade_decisao_verdadeira": sum(1 for r in res if r["decisao"]),
    }

# ------------------------------------------------- Q02: restrição escrita à mão (E4 + "not p or q")
e4 = P(proprias["E4"]).parse()
ins4 = distinct(e4)
ce = P("not p or q").parse()
txt = ["; Q02: linhas de E4 = p or (q and r) que violam a restricao 'not p or q' (p implica q)"]
for i, n in enumerate(ins4):
    txt.append("(declare-const %s Bool) ; %s" % (bvar(i), n))
txt.append("(define-fun restricao () Bool %s)" % smt_bool(ce, lambda a: bvar(ins4.index(a))))
combos = list(itertools.product([True, False], repeat=len(ins4)))
for c in combos:
    txt.append("(push)")
    for i, v in enumerate(c):
        txt.append("(assert (= %s %s))" % (bvar(i), "true" if v else "false"))
    txt.append("(assert (not restricao))")
    txt.append("(check-sat)")
    txt.append("(pop)")
out = run_z3("Q02-restricao", "\n".join(txt) + "\n")
viol = [dict(zip(ins4, c)) for c, r in zip(combos, out) if r == "sat"]
resumo["Q02-restricao"] = {"respostas": out, "linhas_que_violam": viol, "quantidade_violam": len(viol),
                          "quantidade_aceitas": len(combos) - len(viol)}

# ------------------------------------------------- Q03: existência de par por condição (requisitos.mcdc)
# Leitura A (critério do passo 3): par = duas combinações em que a condição muda E a decisão muda.
#   Usa-se o par de causa única (só a condição muda) como testemunha; pelo texto, todo par de
#   causa única também vale no mascaramento (IndependencePairsTest).
# Leitura B ("Critério simplificado"): basta a condição mudar isoladamente; a decisão pode ficar igual.
req = {}
with open(os.path.join(RAIZ, "exemplos", "requisitos.mcdc"), encoding="utf-8") as f:
    for linha in f:
        linha = linha.strip()
        if not linha or linha.startswith("#"):
            continue
        rid, expr = linha.split(":", 1)
        req[rid.strip()] = expr.strip()
resumo["requisitos.mcdc"] = req
for rid, s in req.items():
    e = P(s).parse()
    ins = distinct(e)
    reg = {"expressao": s, "entradas_distintas": ins, "condicoes(aparicoes)": occurrences(e),
           "combinacoes": 2 ** len(ins), "por_entrada": {}}
    for j, alvo in enumerate(ins):
        txt = ["; Q03-%s-%s: existe par para a entrada %s ?" % (rid, j, alvo)]
        for i, n in enumerate(ins):
            txt.append("(declare-const a%d Bool) ; %s (linha 1)" % (i, n))
            txt.append("(declare-const c%d Bool) ; %s (linha 2)" % (i, n))
        for i in range(len(ins)):
            if i != j:
                txt.append("(assert (= a%d c%d))" % (i, i))
        txt.append("(assert (not (= a%d c%d)))" % (j, j))
        fa = smt_bool(e, lambda a: "a%d" % ins.index(a))
        fc = smt_bool(e, lambda a: "c%d" % ins.index(a))
        txt.append("(push) ; leitura A: decisao tambem muda")
        txt.append("(assert (not (= %s %s)))" % (fa, fc))
        txt.append("(check-sat)")
        txt.append("(pop)")
        txt.append("(push) ; leitura B: so a mudanca isolada da condicao")
        txt.append("(check-sat)")
        txt.append("(pop)")
        out = run_z3("Q03-%s-%d" % (rid, j), "\n".join(txt) + "\n")
        reg["por_entrada"][alvo] = {"leitura_A_par_que_muda_decisao": out[0], "leitura_B_mudanca_isolada": out[1],
                                    "ocorrencias": occurrences(e).count(alvo)}
    resumo["Q03-" + rid] = reg

# ------------------------------------------------- Q04: check (decisoes.json + testes.csv)
dec = json.load(open(os.path.join(RAIZ, "exemplos", "decisoes.json"), encoding="utf-8"))
tipos = {i["name"]: i for i in dec["inputs"]}
guards = {d["id"]: d["guard"] for d in dec["decisions"]}
testes = {}
with open(os.path.join(RAIZ, "exemplos", "testes.csv"), encoding="utf-8") as f:
    linhas = [l.strip() for l in f if l.strip() and not l.startswith("#")]
cab = linhas[0].split(",")
for l in linhas[1:]:
    r = dict(zip(cab, l.split(",")))
    t = testes.setdefault((r["decision"], r["test"]), {"valores": {}, "esperado": None})
    t["valores"][r["input"]] = r["value"]
    t["esperado"] = r["expected_outcome"]


def smt_val(var, val):
    tp = tipos[var]
    if tp["type"] == "enum":
        return str(tp["values"].index(val))
    if tp["type"] == "bool":
        return val
    return val


def smt_atom(atom):
    name, op, val = atom
    tp = tipos[name]
    v = smt_val(name, val)
    if op == "!=":
        return "(not (= %s %s))" % (name, v)
    return "(%s %s %s)" % (op, name, v)


def smt_dfrs(e):
    if e[0] == "atom":
        return smt_atom(e[2])
    if e[0] == "not":
        return "(not %s)" % smt_dfrs(e[1])
    return "(%s %s %s)" % (e[0], smt_dfrs(e[1]), smt_dfrs(e[2]))


q4 = {}
for (did, tid), t in sorted(testes.items(), key=lambda x: x[0][1]):
    e = P(guards[did]).parse()
    txt = ["; Q04-%s: valor da guarda %s com os valores concretos de %s" % (tid, did, tid)]
    for n, tp in tipos.items():
        if tp["type"] == "bool":
            txt.append("(declare-const %s Bool)" % n)
        else:
            txt.append("(declare-const %s Int)" % n)
            if tp["type"] == "enum":
                txt.append("(assert (and (<= 0 %s) (< %s %d))) ; enum %s" % (n, n, len(tp["values"]), tp["values"]))
    for n, v in t["valores"].items():
        txt.append("(assert (= %s %s))" % (n, smt_val(n, v)))
    txt.append("(define-fun guarda () Bool %s)" % smt_dfrs(e))
    txt.append("(push)\n(assert guarda)\n(check-sat)\n(pop)")
    txt.append("(push)\n(assert (not guarda))\n(check-sat)\n(pop)")
    out = run_z3("Q04-" + tid, "\n".join(txt) + "\n")
    valor = "T" if out == ["sat", "unsat"] else ("F" if out == ["unsat", "sat"] else "?")
    atoms = {}
    for a in distinct(e):
        name, op, val = P(a).parse()[2]
        # valor da condição no teste (avaliação concreta, conferida pelo Z3 na guarda)
        x = t["valores"].get(name)
        atoms[a] = None if x is None else ((x == val) if op == "=" else (x != val))
    q4[tid] = {"decisao": did, "valores": t["valores"], "esperado": t["esperado"], "guarda_avaliada_z3": valor,
               "respostas": out, "esperado_confere": valor == t["esperado"], "condicoes": atoms}
resumo["Q04-check"] = q4
# cobertura das decisões pelos testes existentes: há par de testes em que cada condição muda?
cob = {}
for did in guards:
    ts = [v for v in q4.values() if v["decisao"] == did]
    e = P(guards[did]).parse()
    conds = distinct(e)
    cob[did] = {"testes": len(ts),
                "condicao_muda_entre_testes": {c: len(set(t["condicoes"][c] for t in ts)) > 1 for c in conds}}
resumo["Q04-cobertura"] = cob

# ------------------------------------------------- Q05: sistemas exemplo (contagens e conflito sat/unsat)
def dfrs_types(sistema):
    d = json.load(open(os.path.join(RAIZ, "exemplos", sistema + "-decisoes.json"), encoding="utf-8"))
    return d, {i["name"]: i for i in d["inputs"]}


tabela = {"vm": (5, 21, 152, 4), "tis": (17, 69, 268, 4), "npp": (11, 29, 76, 1)}
for sist, (nreq, ncond, ncomb, nimp) in tabela.items():
    d, tps = dfrs_types(sist)
    total_cond, total_comb, unsat_total, sat_total = 0, 0, 0, 0
    por_dec = []
    txt = ["; Q05-%s: viabilidade de cada combinacao (leitura original: unsat = impossivel)" % sist]
    for n, tp in tps.items():
        if tp["type"] == "bool":
            txt.append("(declare-const %s Bool)" % n)
        elif tp["type"] == "real":
            txt.append("(declare-const %s Real)" % n)
        else:
            txt.append("(declare-const %s Int)" % n)
            if tp["type"] == "enum":
                txt.append("(assert (and (<= 0 %s) (< %s %d))) ; enum %s" % (n, n, len(tp["values"]), tp["values"]))
    meta = []
    for dd in d["decisions"]:
        e = P(dd["guard"]).parse()
        ins = distinct(e)
        total_cond += len(occurrences(e))
        total_comb += 2 ** len(ins)

        def at(a, tps=tps):
            name, op, val = P(a).parse()[2]
            tp = tps[name]
            v = str(tp["values"].index(val)) if tp["type"] == "enum" else val
            return "(not (= %s %s))" % (name, v) if op == "!=" else "(%s %s %s)" % (op, name, v)
        for c in itertools.product([True, False], repeat=len(ins)):
            txt.append("(push)")
            for a, v in zip(ins, c):
                txt.append("(assert %s)" % (at(a) if v else "(not %s)" % at(a)))
            txt.append("(check-sat)\n(pop)")
            meta.append((dd["id"], c))
        por_dec.append({"id": dd["id"], "condicoes": len(occurrences(e)), "entradas_distintas": len(ins),
                        "combinacoes": 2 ** len(ins)})
    out = run_z3("Q05-%s" % sist, "\n".join(txt) + "\n")
    unsat_total = sum(1 for r in out if r == "unsat")
    sat_total = sum(1 for r in out if r == "sat")
    resumo["Q05-" + sist] = {
        "decisoes": len(d["decisions"]), "condicoes": total_cond, "combinacoes": total_comb,
        "respostas_sat": sat_total, "respostas_unsat": unsat_total,
        "outras_respostas": len(out) - sat_total - unsat_total,
        "impossiveis_leitura_original(unsat)": unsat_total,
        "impossiveis_leitura_substituta(sat)": sat_total,
        "tabela_do_texto": {"requisitos": nreq, "condicoes": ncond, "combinacoes": ncomb, "impossiveis": nimp},
        "unsat_por_combinacao": [{"decisao": m[0], "linha": list(m[1])} for m, r in zip(meta, out) if r == "unsat"],
        "por_decisao": por_dec,
    }
    # consulta aritmética: tabela do texto x contagem derivada da regra 2^n
    arit = ["; Q05-%s-aritmetica: numeros da tabela de regressao x regra 2^n" % sist,
            "(declare-const combinacoes Int)", "(declare-const condicoes Int)", "(declare-const requisitos Int)",
            "(assert (= combinacoes (+ %s)))" % " ".join(str(p["combinacoes"]) for p in por_dec),
            "(assert (= condicoes (+ %s)))" % " ".join(str(p["condicoes"]) for p in por_dec),
            "(assert (= requisitos %d))" % len(por_dec),
            "(push)", "(assert (and (= combinacoes %d) (= condicoes %d) (= requisitos %d)))" % (ncomb, ncond, nreq),
            "(check-sat)", "(pop)",
            "(push) ; leitura substituta: impossiveis = combinacoes sat; tabela diz %d" % nimp,
            "(assert (= %d %d))" % (sat_total, nimp), "(check-sat)", "(pop)",
            "(push) ; leitura original: impossiveis = combinacoes unsat; tabela diz %d" % nimp,
            "(assert (= %d %d))" % (unsat_total, nimp), "(check-sat)", "(pop)"]
    resumo["Q05-%s-aritmetica" % sist] = run_z3("Q05-%s-aritmetica" % sist, "\n".join(arit) + "\n")

# ------------------------------------------------- Q06: limite de 1000 pares por condição
# E5 = x01 and (x02 or ... or x20): 20 entradas distintas; pares de causa única de x01 = linhas em
# que (x02 or ... or x20) é verdadeiro = 2^19 - 1.
q6 = ["; Q06: 20 entradas -> 2^20 combinacoes; pares de causa unica de x01 em E5 > 1000",
      "(declare-const combinacoes Int)", "(declare-const pares_x01 Int)",
      "(assert (= combinacoes (^ 2 20)))", "(assert (= pares_x01 (- (^ 2 19) 1)))",
      "(push)", "(assert (= combinacoes 1048576))", "(assert (> pares_x01 1000))", "(check-sat)", "(pop)",
      "(push)", "(assert (<= pares_x01 1000))", "(check-sat)", "(pop)"]
resumo["Q06-limites"] = run_z3("Q06-limites", "\n".join(q6) + "\n")

# ------------------------------------------------- Q07: subconjunto causa única ⊆ mascaramento
# Não há fórmula do mascaramento no texto C4 (critério em conflito); registra-se apenas a
# existência de pares de causa única em E6 = (p and q) or r para cada entrada.
e6 = P("(p and q) or r").parse()
ins6 = distinct(e6)
r7 = {}
for j, alvo in enumerate(ins6):
    txt = ["; Q07-%s: existe par de causa unica para %s em (p and q) or r ?" % (alvo, alvo)]
    for i in range(len(ins6)):
        txt.append("(declare-const a%d Bool)\n(declare-const c%d Bool)" % (i, i))
        if i != j:
            txt.append("(assert (= a%d c%d))" % (i, i))
    txt.append("(assert (not (= a%d c%d)))" % (j, j))
    txt.append("(assert (not (= %s %s)))" % (smt_bool(e6, lambda a: "a%d" % ins6.index(a)),
                                             smt_bool(e6, lambda a: "c%d" % ins6.index(a))))
    txt.append("(check-sat)")
    r7[alvo] = run_z3("Q07-" + alvo, "\n".join(txt) + "\n")
resumo["Q07-causa-unica-E6"] = r7

with open(os.path.join(AQUI, "resumo.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(resumo, f, ensure_ascii=False, indent=1)
print(json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk not in ("linhas", "unsat_por_combinacao", "por_decisao")}) for k, v in resumo.items()}, ensure_ascii=False, indent=1))
