"""Correção + extensão r2 do oráculo C3 (gerado depois da rodada r1, antes da r2).

Correção: em r1, os CSVs de check usaram decision = "D", mas a fonte não define o
identificador de uma decisão escrita como expressão direta; nenhum teste foi associado
(casos inválidos por entrada do harness). Aqui a mesma decisão vem de um arquivo .mcdc
"D: (A and B) or C", cujo ID é definido pelo formato documentado (L151).
Extensão: situações documentadas ainda não exercitadas (valores concretos tipados,
comparações com ==, !=, <, negativos, verify em JSON) e diagnósticos indeterminados.
As expectativas vêm só do texto C3; a cobertura de r1 apenas apontou onde procurar.
Uso: python -I gerar_r2.py <z3.exe>
"""
import itertools
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(HERE)
sys.path.insert(0, EXP)
import exprlib as X  # noqa: E402

Z3 = sys.argv[1]
ENT = os.path.join(HERE, "entradas")
ZD = os.path.join(HERE, "z3")
os.makedirs(ENT, exist_ok=True)
os.makedirs(ZD, exist_ok=True)
base = json.load(open(os.path.join(EXP, "oraculo.json"), encoding="utf-8"))
Q = {c["id"]: c for c in base["casos"]}
ev = json.load(open(os.path.join(EXP, "z3-evidencias.json"), encoding="utf-8"))
log = []


def z3(qid, text, expect=None):
    p = os.path.join(ZD, qid + ".smt2")
    open(p, "w", encoding="utf-8", newline="\n").write(text)
    out = subprocess.run([Z3, "-T:60", p], capture_output=True, text=True).stdout
    open(os.path.join(ZD, qid + ".out"), "w", encoding="utf-8", newline="\n").write(out)
    ans = [ln.strip() for ln in out.splitlines() if ln.strip() in ("sat", "unsat", "unknown")]
    if "unknown" in ans or "error" in out:
        raise SystemExit(f"erro técnico Z3 {qid}: {out}")
    if expect is not None and ans != expect:
        raise SystemExit(f"{qid}: {ans} != {expect}")
    log.append({"id": qid, "respostas": ans})
    return ans, out


def w(name, text):
    open(os.path.join(ENT, name), "w", encoding="utf-8", newline="\n").write(text)


# ------------------------------------------------------------------ entradas
w("abc.mcdc", "# decisão D usada pelos casos de check corrigidos\nD: (A and B) or C\n")
for n in ["check-completa", "check-um-teste", "check-esperado-errado", "check-sem-mudanca-de-resultado"]:
    w(n + ".csv", open(os.path.join(EXP, "entradas", n + ".csv"), encoding="utf-8").read())

GUARD = "x < 3 /\\ x >= -2 \\/ r <= 1.5 /\\ m != b \\/ k = true"
tip = {"system": "extensao", "inputs": [{"name": "x", "type": "int"}, {"name": "r", "type": "real"},
                                        {"name": "m", "type": "enum", "values": ["a", "b", "c"]},
                                        {"name": "k", "type": "bool"}],
       "decisions": [{"id": "e#1", "requirement": "R1", "guard": GUARD, "actions": ["y := 1"]}]}
json.dump(tip, open(os.path.join(ENT, "tipada.json"), "w", encoding="utf-8"), indent=2)
types = {i["name"]: i["type"] for i in tip["inputs"]}
TESTS = [("U1", {"x": "0", "r": "9", "m": "b", "k": "false"}, "T"),
         ("U2", {"x": "5", "r": "9", "m": "b", "k": "false"}, "F"),
         ("U3", {"x": "-3", "r": "1.5", "m": "a", "k": "false"}, "T"),
         ("U4", {"x": "-3", "r": "1.5", "m": "b", "k": "false"}, "T"),   # guarda F: esperado errado
         ("U5", {"x": "7", "r": "2", "m": "c", "k": "true"}, "F")]       # guarda T: esperado errado
w("tipada.csv", "decision,test,input,value,expected_outcome\n" + "".join(
    f"e#1,{t},{k},{v},{o}\n" for t, vals, o in TESTS for k, v in vals.items()))

# Z3: guarda nos valores concretos (Int, Real, enum como datatype, Bool)
hdr = ["(declare-datatypes () ((M a b c)))", "(declare-const x Int)(declare-const r Real)(declare-const m M)(declare-const k Bool)"]
gs = "(or (or (and (< x 3) (>= x (- 2))) (and (<= r 1.5) (not (= m b)))) (= k true))"
t = ["; guarda de tipada.json nos testes de tipada.csv"] + hdr
for name, vals, _ in TESTS:
    x = vals["x"]
    xs = f"(- {x[1:]})" if x.startswith("-") else x
    t.append(f"(push)(assert (and (= x {xs}) (= r {vals['r']}) (= m {vals['m']}) (= k {vals['k']}) {gs}))(check-sat)(pop) ; {name}")
ans, _ = z3("R2_tipada_testes", "\n".join(t) + "\n")
e = X.parse(GUARD)
DIV = []
for (name, vals, o), a in zip(TESTS, ans):
    py = X.ev(e, {at: X.eval_atom_concrete(at, vals, types) for at in X.atoms(e)})
    assert py == (a == "sat")
    if (o == "T") != py:
        DIV.append(name)
assert DIV == ["U4", "U5"], DIV


def bnd(qid, op, k, real=False):
    t = [f"; fronteira inteira de x {op} {k}", "(declare-const v Int)",
         f"(assert (not (= ({op} v {k}) ({op} (+ v 1) {k}))))", "(check-sat)", "(get-value (v))"]
    a, out = z3(qid, "\n".join(t) + "\n", ["sat"])
    s = out.split("(v ")[1].split(")")[0].strip()
    v = -int(s.split()[-1]) if s.startswith("(-") else int(s)
    z3(qid + "_unico", "\n".join(t[:3] + [f"(assert (not (= v {v})))", "(check-sat)"]) + "\n", ["unsat"])
    return [v, v + 1]


B1 = bnd("R2_fronteira_x_lt3", "<", 3)
B2 = bnd("R2_fronteira_x_ge_m2", ">=", "(- 2)")
assert B1 == [2, 3] and B2 == [-3, -2]


def tt(qid, expr):
    ex = X.parse(expr)
    ats = X.atoms(ex)
    names = {a: f"p{i}" for i, a in enumerate(ats)}
    lines = [f"; tabela-verdade de {expr}"] + [f"(declare-const {names[a]} Bool)" for a in ats]
    combos = list(itertools.product([True, False], repeat=len(ats)))
    for c in combos:
        asg = " ".join(f"(= {names[a]} {'true' if v else 'false'})" for a, v in zip(ats, c))
        lines.append(f"(push)(assert (and {asg} {X.smt(ex, names)}))(check-sat)(pop)")
    ans, _ = z3(qid, "\n".join(lines) + "\n")
    rows = [{"entradas": dict(zip(ats, c)), "saida": a == "sat"} for c, a in zip(combos, ans)]
    assert all(r["saida"] == X.ev(ex, r["entradas"]) for r in rows)
    return rows


TT_CMP = tt("R2_tt_cmp", "x == 5 or y != 2 and z < -1")

# ------------------------------------------------------------------ casos
C = []


def copy(old, new, args, extra_just):
    c = json.loads(json.dumps(Q[old]))
    c["id"], c["args"] = new, args
    c["justificativa"] = c["justificativa"] + " " + extra_just
    c["corrige"] = old
    C.append(c)


J = "Correção de r1: decisão vinda de abc.mcdc (ID 'D' definido pelo formato .mcdc, L151); CSV idêntico."
copy("C3-T20", "C3-T20c", ["check", "-f", "{ENT2}/abc.mcdc", "--tests", "{ENT2}/check-completa.csv"], J)
copy("C3-T21", "C3-T21c", ["check", "-f", "{ENT2}/abc.mcdc", "--tests", "{ENT2}/check-um-teste.csv"], J)
copy("C3-T22", "C3-T22c", ["check", "-f", "{ENT2}/abc.mcdc", "--tests", "{ENT2}/check-esperado-errado.csv"], J)
copy("C3-T25", "C3-T25c", ["check", "-f", "{ENT2}/abc.mcdc", "--tests", "{ENT2}/check-completa.csv", "--format", "json"], J)
copy("C3-I03", "C3-I03c", ["check", "-f", "{ENT2}/abc.mcdc", "--tests", "{ENT2}/check-esperado-errado.csv"], J)
copy("C3-I38", "C3-I38c", ["check", "-f", "{ENT2}/abc.mcdc", "--tests", "{ENT2}/check-sem-mudanca-de-resultado.csv"], J)

Qcheck = Q["C3-T22"]["trechos"] + [Q["C3-T24"]["trechos"][2]]


def D(id_, titulo, args, trechos, regra, expectativa, verif, just, z3ids):
    C.append(dict(id=id_, titulo=titulo, status="DETERMINADO", args=args, precondicao="z3 no PATH do processo",
                  trechos=trechos, regra=regra, expectativa=expectativa, verificacoes=verif, justificativa=just,
                  z3=z3ids, conflitos_avaliados=["K3"]))


def I(id_, titulo, args, trechos, motivo):
    C.append(dict(id=id_, titulo=titulo, status="INDETERMINADO", args=args, precondicao="z3 no PATH do processo",
                  trechos=trechos, regra=None, expectativa=None, verificacoes=[], justificativa=motivo, z3=[],
                  conflitos_avaliados=["omissão", "K3"]))


TJ = "Componentes não julgados: código de saída (K3)."
D("C3-E01", "check com valores concretos tipados (int, real, enum, bool)",
  ["check", "--json", "{ENT2}/tipada.json", "--tests", "{ENT2}/tipada.csv"], Qcheck,
  "Valores concretos conforme o tipo; testes cujo esperado difere da guarda são apontados.",
  "Exatamente U4 e U5 apontados com resultado esperado errado. " + TJ,
  [{"tipo": "check_divergentes", "testes": DIV}],
  "Guarda avaliada pelo Z3 com Int/Real/enum/Bool (inclui negativo -3 e real 1.5).", ["R2_tipada_testes"])
D("C3-E02", "Valores concretos e fronteiras com <, >=, <=, != e negativos",
  ["analyze", "--json", "{ENT2}/tipada.json", "--z3", "--boundary", "--format", "json"],
  Q["C3-T30"]["trechos"] + Q["C3-T27"]["trechos"],
  "Valores concretos realizam a combinação; fronteiras de cada comparação inteira.",
  "Todo teste com valores concretos os tem coerentes com a combinação e com a guarda; fronteiras de x incluem 2 e 3 (x < 3) e -3 e -2 (x >= -2). " + TJ,
  [{"tipo": "valores_realizam", "tipos": types}, {"tipo": "fronteira", "variavel": "x", "valores": [2, 3, -3, -2]}],
  "Mesmas regras de C3-T28/C3-T30; r é real, por isso só x é julgado nas fronteiras (decisão A4).",
  ["R2_fronteira_x_lt3", "R2_fronteira_x_ge_m2"])
D("C3-E03", "Comparações ==, != e < com negativo",
  ["analyze", "x == 5 or y != 2 and z < -1"], Q["C3-T04"]["trechos"] + Q["C3-T01"]["trechos"][3:],
  "`==` é comparação; e antes de ou; cada comparação é uma entrada.",
  "Tabela-verdade com 3 entradas e 8 combinações de (x == 5) ∨ ((y != 2) ∧ (z < -1)). " + TJ,
  [{"tipo": "tabela_verdade", "combinacoes": 8, "linhas": TT_CMP}], "Operadores listados em L143.", ["R2_tt_cmp"])
D("C3-E04", "verify em JSON sem --context",
  ["verify", "--json", "{EX}/npp-decisoes.json", "--format", "json"], Q["C3-T26"]["trechos"] + [Q["C3-T25"]["trechos"][0]],
  "verify aceita json; lacunas só com contexto.",
  "Saída é JSON válido e não aponta lacuna encontrada. " + TJ,
  [{"tipo": "json_valido"}, {"tipo": "sem_lacunas_json"}], "L127 + L567.", [])
OMI = [Q["C3-I29"]["trechos"][0]]
I("C3-I40", "--boundary sem --z3", ["analyze", "speed > 100", "--boundary"], [Q["C3-T27"]["trechos"][0]],
  "Omissão: 'Com --z3' não diz a reação ao uso isolado.")
I("C3-I41", "Duas fontes ao mesmo tempo", ["analyze", "A and B", "-f", "{EX}/requisitos.mcdc"], [Q["C3-I29"]["trechos"][0]],
  "Omissão: 'Fonte (uma só)' não diz a reação.")
I("C3-I42", "check sem --tests", ["check", "A and B"], [Q["C3-I37"]["trechos"][0]], "Omissão da reação.")
I("C3-I43", "--exact com --direct", ["analyze", "A and B", "--exact", "--direct"], [Q["C3-I12"]["trechos"][0]],
  "Omissão; também K8/K10.")
I("C3-I44", "Opção sem valor", ["analyze", "A and B", "--format"], [Q["C3-I32"]["trechos"][0]], "Omissão da reação.")
I("C3-I45", "--context em analyze", ["analyze", "A and B", "--context", "A"], [Q["C3-I16"]["trechos"][0]],
  "Omissão: --context é descrito só para verify.")
I("C3-I46", "verify com --z3", ["verify", "--json", "{EX}/npp-decisoes.json", "--z3"], [Q["C3-I15"]["trechos"][0]],
  "Omissão da reação; verify já usa o Z3.")
I("C3-I47", "--direct com --mutation", ["analyze", "(A and B) or C", "--direct", "--mutation"], [Q["C3-I24"]["trechos"][0]],
  "Omissão e K10 (o direto monta ou não a tabela).")

json.dump({"condicao": "C3", "rodada": "r2", "base": "oraculo.json (congelado)", "casos": C},
          open(os.path.join(HERE, "oraculo-r2.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(log, open(os.path.join(HERE, "z3-evidencias-r2.json"), "w", encoding="utf-8"), indent=1)
print(len(C), sum(c["status"] == "DETERMINADO" for c in C))
