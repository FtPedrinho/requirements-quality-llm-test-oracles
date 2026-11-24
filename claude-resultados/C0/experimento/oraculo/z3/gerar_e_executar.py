"""Gera consultas SMT-LIB do oraculo C0 e as executa no Z3 independente (z3.exe).

As formulas traduzem regras do README C0 (tool-readme-original.md):
- par de mascaramento: dois testes possiveis em que a condicao muda, a saida muda
  e ela decide nos dois (trocar so aquela aparicao muda a saida);
- causa unica: alem disso, todas as demais entradas iguais;
- combinacoes impossiveis: linhas insatisfativeis sob a restricao;
- conflito: duas guardas valem juntas e escrevem valores diferentes;
- lacuna: no contexto, nenhuma guarda vale.
Nenhuma formula usa codigo ou saida do SUT.
"""
import json, os, subprocess, sys

Z3 = os.environ.get("Z3_EXE", os.path.expanduser(r"~\AppData\Roaming\Python\bin\z3.exe"))
HERE = os.path.dirname(os.path.abspath(__file__))
QDIR = os.path.join(HERE, "consultas")
os.makedirs(QDIR, exist_ok=True)

# --- AST: ('v', nome, aparicao) | ('not', e) | ('and', [..]) | ('or', [..])
def V(n, k=None): return ('v', n, k)
def Not(e): return ('not', e)
def And(*es): return ('and', list(es))
def Or(*es): return ('or', list(es))

def leaves(e, acc=None):
    acc = [] if acc is None else acc
    if e[0] == 'v': acc.append(e)
    elif e[0] == 'not': leaves(e[1], acc)
    else:
        for x in e[1]: leaves(x, acc)
    return acc

def cond_name(leaf): return leaf[1] if leaf[2] is None else f"{leaf[1]}#{leaf[2]}"

def smt(e, t, flip=None):
    """t: prefixo do teste; flip: nome da condicao cuja aparicao e trocada."""
    if e[0] == 'v':
        s = f"{t}_{e[1]}"
        return f"(not {s})" if flip == cond_name(e) else s
    if e[0] == 'not': return f"(not {smt(e[1], t, flip)})"
    op = e[0]
    return f"({op} {' '.join(smt(x, t, flip) for x in e[1])})"

def inputs(e): return sorted({l[1] for l in leaves(e)}, key=lambda s: (len(s), s))

def decl(e, t): return "".join(f"(declare-const {t}_{v} Bool)\n" for v in inputs(e))

def pair_formula(e, c, ta, tb, unique=False, constraint=None):
    vname = c.split('#')[0]
    parts = [f"(distinct {ta}_{vname} {tb}_{vname})",
             f"(distinct {smt(e, ta)} {smt(e, tb)})",
             f"(distinct {smt(e, ta)} {smt(e, ta, c)})",
             f"(distinct {smt(e, tb)} {smt(e, tb, c)})"]
    if unique:
        parts += [f"(= {ta}_{v} {tb}_{v})" for v in inputs(e) if v != vname]
    if constraint is not None:
        parts += [smt(constraint, ta), smt(constraint, tb)]
    return "(and " + " ".join(parts) + ")"

RESULTS = []

def run(qid, text, expect, note):
    path = os.path.join(QDIR, qid + ".smt2")
    with open(path, "w", encoding="utf-8") as f: f.write(text)
    try:
        p = subprocess.run([Z3, "-smt2", "-T:60", path], capture_output=True, text=True, timeout=90)
        out = p.stdout.strip()
    except Exception as ex:  # erro tecnico, nao indeterminacao
        out = f"ERRO_TECNICO: {ex}"
    with open(os.path.join(QDIR, qid + ".out"), "w", encoding="utf-8") as f: f.write(out + "\n")
    first = out.splitlines()[0] if out else ""
    RESULTS.append({"id": qid, "esperado": expect, "obtido": first, "ok": first == expect, "nota": note,
                    "testemunha": "\n".join(out.splitlines()[1:])[:2000]})

def q_pair(qid, e, c, unique=False, constraint=None, expect="sat", note=""):
    txt = f"; {qid}: par {'causa unica' if unique else 'mascaramento'} de {c}\n"
    txt += decl(e, "t1") + decl(e, "t2")
    txt += f"(assert {pair_formula(e, c, 't1', 't2', unique, constraint)})\n(check-sat)\n"
    if expect == "sat": txt += "(get-model)\n"
    run(qid, txt, expect, note)

def q_min_suite(qid, e, k, unique=False, constraint=None, expect="sat", note=""):
    """Existe suite de k testes contendo par valido para cada condicao?"""
    conds = [cond_name(l) for l in leaves(e)]
    txt = f"; {qid}: existe suite de {k} testes com par {'causa unica' if unique else 'mascaramento'} de cada condicao\n"
    for i in range(k): txt += decl(e, f"s{i}")
    if constraint is not None:
        for i in range(k): txt += f"(assert {smt(constraint, f's{i}')})\n"
    for c in conds:
        opts = [pair_formula(e, c, f"s{i}", f"s{j}", unique) for i in range(k) for j in range(i + 1, k)]
        txt += f"(assert (or {' '.join(opts)}))\n" if opts else "(assert false)\n"
    txt += "(check-sat)\n" + ("(get-model)\n" if expect == "sat" else "")
    run(qid, txt, expect, note)

def q_rows(prefix, e_vars, constraint_fn, note):
    """Viabilidade de cada linha (combinacao das condicoes)."""
    import itertools
    for bits in itertools.product([True, False], repeat=len(e_vars)):
        tag = "".join("T" if b else "F" for b in bits)
        yield tag, bits

A, B, C, D, E = (V(x) for x in "ABCDE")

# Q-E1: (A and B) or C
e1 = Or(And(A, B), C)
for c in ["A", "B", "C"]:
    q_pair(f"Q-E1-par-{c}", e1, c, note="C0-A01/A02")
    q_pair(f"Q-E1-parUC-{c}", e1, c, unique=True, note="C0-A03")
q_min_suite("Q-E1-min-3", e1, 3, expect="unsat", note="C0-A02: 3 testes nao bastam")
q_min_suite("Q-E1-min-4", e1, 4, expect="sat", note="C0-A02: 4 testes bastam")
q_min_suite("Q-E1-minUC-3", e1, 3, unique=True, expect="unsat", note="C0-A03 (informativo)")
q_min_suite("Q-E1-minUC-4", e1, 4, unique=True, expect="sat", note="C0-A03 (informativo)")

# Q-E2: A and not B
e2 = And(A, Not(B))
q_min_suite("Q-E2-min-2", e2, 2, expect="unsat", note="C0-A04")
q_min_suite("Q-E2-min-3", e2, 3, expect="sat", note="C0-A04")

# Q-E3: ((E or D) and (not A or D)) or B  -- entrada D repetida
e3 = Or(And(Or(E, V("D", 1)), Or(Not(A), V("D", 2))), B)
q_min_suite("Q-E3-min-4", e3, 4, expect="unsat", note="C0-A12: --exact nao acha 4")
q_min_suite("Q-E3-min-5", e3, 5, expect="sat", note="C0-A12: --exact acha 5")

# Q-E4: paridade de 3 entradas
P = Or(And(V("A", 1), V("B", 1), V("C", 1)), And(V("A", 2), Not(V("B", 2)), Not(V("C", 2))),
       And(Not(V("A", 3)), V("B", 3), Not(V("C", 3))), And(Not(V("A", 4)), Not(V("B", 4)), V("C", 4)))
q_min_suite("Q-E4-min-7", P, 7, expect="unsat", note="C0-A13")
q_min_suite("Q-E4-min-8", P, 8, expect="sat", note="C0-A13")

# Q-E5: (A and B) or (not A and C)
e5 = Or(And(V("A", 1), B), And(Not(V("A", 2)), C))
for c in ["A#1", "B", "A#2", "C"]:
    q_pair(f"Q-E5-par-{c.replace('#','_')}", e5, c, note="C0-A05")

# Q-E6: A or (A and B)
e6 = Or(V("A", 1), And(V("A", 2), B))
q_pair("Q-E6-par-A_1", e6, "A#1", expect="sat", note="C0-A06")
q_pair("Q-E6-par-A_2", e6, "A#2", expect="unsat", note="C0-A06: A#2 sem par")
q_pair("Q-E6-par-B", e6, "B", expect="unsat", note="C0-A06: B sem par")

# Q-E7: A and B, restricao not A or not B
e7 = And(A, B); k7 = Or(Not(A), Not(B))
for c in ["A", "B"]:
    q_pair(f"Q-E7-par-{c}-restrito", e7, c, constraint=k7, expect="unsat", note="C0-A08: sem par com restricao")
    q_pair(f"Q-E7-par-{c}-livre", e7, c, expect="sat", note="C0-A08: com par sem restricao => bloqueada")
run("Q-E7-linha-TT", "(declare-const A Bool)(declare-const B Bool)(assert (and A B (or (not A) (not B))))(check-sat)\n", "unsat", "C0-A08: 1 impossivel")

# Q-E8: A or (B and C), restricao not A or B
e8 = Or(A, And(B, C)); k8 = Or(Not(A), B)
import itertools
for bits in itertools.product([True, False], repeat=3):
    tag = "".join("T" if b else "F" for b in bits)
    lits = " ".join(n if b else f"(not {n})" for n, b in zip("ABC", bits))
    exp = "unsat" if (bits[0] and not bits[1]) else "sat"
    run(f"Q-E8-linha-{tag}", f"(declare-const A Bool)(declare-const B Bool)(declare-const C Bool)\n(assert (and {lits} (or (not A) B)))\n(check-sat)\n", exp, "C0-A10/B08")
for c in ["A", "B", "C"]:
    q_pair(f"Q-E8-par-{c}", e8, c, constraint=k8, note="C0-A10")

# Q-E9: speed > 100 or (speed > 50 and rain), speed inteiro
for bits in itertools.product([True, False], repeat=3):
    tag = "".join("T" if b else "F" for b in bits)
    a = "(> speed 100)" if bits[0] else "(not (> speed 100))"
    b = "(> speed 50)" if bits[1] else "(not (> speed 50))"
    r = "rain" if bits[2] else "(not rain)"
    exp = "unsat" if (bits[0] and not bits[1]) else "sat"
    run(f"Q-E9-linha-{tag}", f"(declare-const speed Int)(declare-const rain Bool)\n(assert (and {a} {b} {r}))\n(check-sat)\n" + ("(get-model)\n" if exp == "sat" else ""), exp, "C0-D01: impossiveis = 2")
for lim in (100, 50):
    run(f"Q-E9-fronteira-{lim}", f"; nao ha inteiro entre {lim} e {lim+1}; {lim} falso e {lim+1} verdadeiro para speed > {lim}\n(declare-const speed Int)\n(assert (or (and (> speed {lim}) (< speed {lim+1})) (> {lim} {lim}) (not (> {lim+1} {lim}))))\n(check-sat)\n", "unsat", "C0-D01: fronteira")
# pares sob viabilidade numerica (A=speed>100, B=speed>50, C=rain)
for c in ["A", "B", "C"]:
    t = ""
    for p in ("t1", "t2"):
        t += f"(declare-const {p}_speed Int)(declare-const {p}_rain Bool)\n"
    def f(p, flip=None):
        a = f"(> {p}_speed 100)"; b = f"(> {p}_speed 50)"; r = f"{p}_rain"
        if flip == "A": a = f"(not {a})"
        if flip == "B": b = f"(not {b})"
        if flip == "C": r = f"(not {r})"
        return f"(or {a} (and {b} {r}))"
    atom = {"A": "(> {}_speed 100)", "B": "(> {}_speed 50)", "C": "{}_rain"}[c]
    t += f"(assert (and (distinct {atom.format('t1')} {atom.format('t2')}) (distinct {f('t1')} {f('t2')}) (distinct {f('t1')} {f('t1', c)}) (distinct {f('t2')} {f('t2', c)})))\n(check-sat)\n(get-model)\n"
    run(f"Q-E9-par-{c}", t, "sat", "C0-D01: todas com par")

# Q-E10: cafe (enum idle/choice)
for bits in itertools.product([True, False], repeat=2):
    tag = "".join("T" if b else "F" for b in bits)
    m = "(= mode idle)" if bits[0] else "(not (= mode idle))"
    s = "coin" if bits[1] else "(not coin)"
    run(f"Q-E10-linha-{tag}", f"(declare-datatypes () ((Mode idle choice)))\n(declare-const mode Mode)(declare-const coin Bool)\n(assert (and {m} {s}))\n(check-sat)\n(get-model)\n", "sat", "C0-C08: 0 impossiveis")
q_min_suite("Q-E10-min-2", And(V("M"), V("S")), 2, expect="unsat", note="C0-C07: 3 testes")
q_min_suite("Q-E10-min-3", And(V("M"), V("S")), 3, expect="sat", note="C0-C07: 3 testes")

# Q-E11: verify
run("Q-E11a-conflito", "(declare-const c Bool)(declare-const d Bool)\n; R1: c -> m:=choice ; R2: d -> m:=weak ; valores diferentes\n(assert (and c d (distinct 1 2)))\n(check-sat)\n(get-model)\n", "sat", "C0-G01")
run("Q-E11b-disjuntas", "(declare-const c Bool)\n(assert (and c (not c)))\n(check-sat)\n", "unsat", "C0-G03")
run("Q-E11c-lacuna", "(declare-const c Bool)(declare-const d Bool)\n; contexto c=false; guardas c, d; lacuna = contexto e nenhuma guarda\n(assert (and (not c) (not c) (not d)))\n(check-sat)\n(get-model)\n", "sat", "C0-G04")
run("Q-E11d-sem-lacuna", "(declare-const c Bool)(declare-const d Bool)\n; contexto d=true; guardas c, not c\n(assert (and d (not c) (not (not c))))\n(check-sat)\n", "unsat", "C0-G05")

# Q-E12: suites fixas do check sobre (A and B) or C
rows = {"T1": (1, 1, 0), "T2": (0, 1, 0), "T3": (1, 0, 0), "T4": (0, 1, 1)}
def fixed(names):
    txt = ""
    for n in names:
        a, b, c = rows[n]
        txt += decl(e1, n)
        txt += f"(assert (and {'' if a else '(not '}{n}_A{'' if a else ')'} {'' if b else '(not '}{n}_B{'' if b else ')'} {'' if c else '(not '}{n}_C{'' if c else ')'}))\n"
    return txt
for c in ["A", "B", "C"]:
    names = list(rows)
    opts = [pair_formula(e1, c, x, y) for i, x in enumerate(names) for y in names[i + 1:]]
    run(f"Q-E12-completa-{c}", fixed(names) + f"(assert (or {' '.join(opts)}))\n(check-sat)\n", "sat", "C0-F01")
for c, exp in [("A", "sat"), ("B", "unsat"), ("C", "unsat")]:
    names = ["T1", "T2"]
    opts = [pair_formula(e1, c, "T1", "T2")]
    run(f"Q-E12-incompleta-{c}", fixed(names) + f"(assert (or {' '.join(opts)}))\n(check-sat)\n", exp, "C0-F02")
run("Q-E12-esperado-T2", fixed(["T2"]) + f"(assert (= {smt(e1, 'T2')} true))\n(check-sat)\n", "unsat", "C0-F03: guarda em T2 e F, CSV declara T")

# Q-E13: check concreto speed > 100 and rain
conc = {"T1": (150, True), "T2": (50, True), "T3": (150, False)}
txt = ""
for n, (s, r) in conc.items():
    txt += f"(define-fun {n}_A () Bool (> {s} 100))(define-fun {n}_B () Bool {'true' if r else 'false'})\n"
ee = And(A, B)
for c in ["A", "B"]:
    opts = [pair_formula(ee, c, x, y) for i, x in enumerate(conc) for y in list(conc)[i + 1:]]
    run(f"Q-E13-par-{c}", txt + f"(assert (or {' '.join(opts)}))\n(check-sat)\n", "sat", "C0-F04")
run("Q-E13-esperados", txt + "(assert (not (and (= (and T1_A T1_B) true) (= (and T2_A T2_B) false) (= (and T3_A T3_B) false))))\n(check-sat)\n", "unsat", "C0-F04: esperados coerentes")

# Q-E14: conjuncao de 13 entradas: minimo 14
a13 = And(*[V(f"A{i}") for i in range(1, 14)])
# A busca direta com 13 slots excedeu 60 s na 1a rodada (erro tecnico registrado em
# rodada-1-timeout.txt). Substituida por lemas: todo par de Ai contem a linha toda-T
# e a linha que so difere em Ai; logo n condicoes exigem n linhas distintas + toda-T = n+1.
q_min_suite("Q-E14-min-14", a13, 14, expect="sat", note="C0-A16: 14 testes bastam")
for n in (13, 20):
    an = And(*[V(f"A{i}") for i in range(1, n + 1)])
    ins = inputs(an)
    for c in ("A1", f"A{n}"):
        base = decl(an, "t1") + decl(an, "t2")
        pf = pair_formula(an, c, "t1", "t2")
        allT = lambda p: "(and " + " ".join(f"{p}_{v}" for v in ins) + ")"
        onlyc = lambda p: "(and (not " + f"{p}_{c}" + ") " + " ".join(f"{p}_{v}" for v in ins if v != c) + ")"
        run(f"Q-E14-n{n}-{c}-par-sem-todaT", base + f"(assert (and {pf} (not {allT('t1')}) (not {allT('t2')})))\n(check-sat)\n", "unsat", f"C0-A14/A16: lema 1 (n={n})")
        run(f"Q-E14-n{n}-{c}-par-outra-linha", base + f"(assert (and {pf} (not (or {allT('t1')} {onlyc('t1')})) ))\n(check-sat)\n", "unsat", f"C0-A14/A16: lema 2 (n={n})")
        run(f"Q-E14-n{n}-{c}-par-existe", base + f"(assert {pf})\n(check-sat)\n", "sat", f"C0-A14/A16 (n={n})")

# Q-E16: exemplo .mcdc da documentacao
r1 = Or(And(V("alarme_ativo"), V("porta_aberta")), V("botao_emergencia"))
r2 = And(V("porta_fechada"), Not(V("obstaculo")))
for c in ["alarme_ativo", "porta_aberta", "botao_emergencia"]:
    q_pair(f"Q-E16-REQ001-{c}", r1, c, note="C0-C03")
for c in ["porta_fechada", "obstaculo"]:
    q_pair(f"Q-E16-REQ002-{c}", r2, c, note="C0-C03")

# Q-E18: guarda temporal
for bits in itertools.product([True, False], repeat=2):
    tag = "".join("T" if b else "F" for b in bits)
    a = "(= antes false)" if bits[0] else "(not (= antes false))"
    b = "(= agora true)" if bits[1] else "(not (= agora true))"
    run(f"Q-E18-linha-{tag}", f"(declare-const antes Bool)(declare-const agora Bool)\n(assert (and {a} {b}))\n(check-sat)\n", "sat", "C0-C09")

ver = subprocess.run([Z3, "--version"], capture_output=True, text=True).stdout.strip()
summary = {"z3": ver, "z3_exe": Z3, "total": len(RESULTS), "conforme": sum(r["ok"] for r in RESULTS),
           "divergentes": [r["id"] for r in RESULTS if not r["ok"]], "consultas": RESULTS}
with open(os.path.join(HERE, "resultados-z3.json"), "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=1)
print(ver); print(f"{summary['conforme']}/{summary['total']} conforme"); print("divergentes:", summary["divergentes"])
