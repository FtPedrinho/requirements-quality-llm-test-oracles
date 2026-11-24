"""Gera consultas SMT-LIB (formalizacao do oraculo C2) e executa o Z3 independente.

Nao usa o SUT. Cada consulta grava <nome>.smt2 e <nome>.out em ./smt/.
Definicoes (fidelidade ao texto NAO provada pelo Z3; ver analise-documental.md):
  mascaramento: c difere entre r1 e r2, f difere, e c e sensivel em r1 e em r2
                (f(r) != f(r com c invertida)).
  causa unica : so c difere entre r1 e r2 e f difere.
  suite minima: k testes simbolicos; unsat com k-1 e sat com k => minimo = k.
"""
import itertools, subprocess, pathlib, sys

Z3 = r"C:\Users\User\AppData\Roaming\Python\bin\z3.exe"
OUT = pathlib.Path(__file__).parent / "smt"
OUT.mkdir(exist_ok=True)
log = []


def run(name, text):
    p = OUT / f"{name}.smt2"
    p.write_text(text, encoding="utf-8")
    r = subprocess.run([Z3, "-T:60", str(p)], capture_output=True, text=True)
    (OUT / f"{name}.out").write_text(r.stdout + r.stderr, encoding="utf-8")
    log.append((name, r.stdout.strip().replace("\n", " | ")[:160]))
    return r.stdout


def fdef(vars_, body):
    args = " ".join(f"({v} Bool)" for v in vars_)
    return f"(define-fun f ({args}) Bool {body})\n"


def minsuite(name, vars_, body, k, variant):
    n = len(vars_)
    s = "(set-logic QF_UF)\n" + fdef(vars_, body)
    for i in range(k):
        for v in vars_:
            s += f"(declare-const {v}_{i} Bool)\n"
    def row(i): return " ".join(f"{v}_{i}" for v in vars_)
    def flip(i, c): return " ".join((f"(not {v}_{i})" if v == c else f"{v}_{i}") for v in vars_)
    for c in vars_:
        alts = []
        for i in range(k):
            for j in range(k):
                if i == j: continue
                if variant == "unique":
                    same = " ".join(f"(= {v}_{i} {v}_{j})" for v in vars_ if v != c)
                    alts.append(f"(and (not (= {c}_{i} {c}_{j})) {same} (not (= (f {row(i)}) (f {row(j)}))))")
                else:
                    alts.append(f"(and (not (= {c}_{i} {c}_{j})) (not (= (f {row(i)}) (f {row(j)})))"
                                f" (not (= (f {row(i)}) (f {flip(i,c)}))) (not (= (f {row(j)}) (f {flip(j,c)}))))")
        s += f"(assert (or {' '.join(alts)}))\n"
    out = run(name, s + "(check-sat)\n")
    if out.split()[0] == "sat":
        out = run(name, s + "(check-sat)\n(get-model)\n")
    return out


def minimum(tag, vars_, body, variant, kmax=10):
    res = {}
    for k in range(2, kmax):
        out = minsuite(f"{tag}_{variant}_k{k}", vars_, body, k, variant)
        res[k] = out.split()[0]
        if res[k] == "sat":
            return k, res
    return None, res


summary = {}
FORM = {
    "z01_abc": (["A", "B", "C"], "(or (and A B) C)"),
    "z02_anotb": (["A", "B"], "(and A (not B))"),
    "z03_aorb_and_cord": (["A", "B", "C", "D"], "(and (or A B) (or C D))"),
    "z04_and3": (["A", "B", "C"], "(and A B C)"),
    "z05_1cond": (["A"], "A"),
    "z06b_ab_or_notc": (["A", "B", "C"], "(or (and A B) (not C))"),
}
for tag, (v, b) in FORM.items():
    for variant in ("masking", "unique"):
        k, res = minimum(tag, v, b, variant)
        summary[(tag, variant)] = (k, res)

# z06: redundancia: B em A or (A and B) nunca altera f (unsat = sem par/sensibilidade)
run("z06_redundante_B", "(set-logic QF_UF)\n(declare-const A Bool)(declare-const B Bool)\n"
    "(define-fun f ((A Bool)(B Bool)) Bool (or A (and A B)))\n"
    "(assert (not (= (f A B) (f A (not B)))))\n(check-sat)\n")

# z07: A and B com restricao not(A and B): nenhuma linha possivel altera f -> A e B bloqueadas
run("z07_bloqueada", "(set-logic QF_UF)\n(declare-const A Bool)(declare-const B Bool)\n"
    "(define-fun f ((A Bool)(B Bool)) Bool (and A B))\n"
    "(define-fun ok ((A Bool)(B Bool)) Bool (not (and A B)))\n"
    "(assert (ok A B))(assert (ok (not A) B))(assert (not (= (f A B) (f (not A) B))))\n(check-sat)\n"
    "(reset)\n(declare-const A Bool)(declare-const B Bool)\n"
    "(define-fun f ((A Bool)(B Bool)) Bool (and A B))\n"
    "(assert (f A B))\n(check-sat)\n")  # sem restricao A=B=T existe; com restricao unsat
# sem a restricao, existe par (T,T)/(F,T)
run("z07b_sem_restricao", "(set-logic QF_UF)\n(declare-const A Bool)(declare-const B Bool)\n"
    "(define-fun f ((A Bool)(B Bool)) Bool (and A B))\n"
    "(assert (not (= (f A B) (f (not A) B))))\n(check-sat)\n(get-model)\n")

# z08: restricao do enunciado: A=(speed>100) implica B=(speed>50); expressao A or (B and C)
rows = list(itertools.product([True, False], repeat=3))
def b(x): return "true" if x else "false"
s = "(set-logic QF_UF)\n(declare-const A Bool)(declare-const B Bool)(declare-const C Bool)\n"
for i, (a_, b_, c_) in enumerate(rows):
    s += f"(push 1)(assert (= A {b(a_)}))(assert (= B {b(b_)}))(assert (= C {b(c_)}))(assert (or (not A) B))(echo \"linha {i}: A={b(a_)} B={b(b_)} C={b(c_)}\")(check-sat)(pop 1)\n"
run("z08_constraint_A_implica_B", s)

# z09: LIA: speed>100 or (speed>50 and rain): quais (c1,c2,rain) sao realizaveis
s = "(set-logic QF_LIA)\n(declare-const speed Int)(declare-const rain Bool)\n"
for c1, c2, r in rows:
    s += (f"(push 1)(assert (= (> speed 100) {b(c1)}))(assert (= (> speed 50) {b(c2)}))(assert (= rain {b(r)}))"
          f"(echo \"c1={b(c1)} c2={b(c2)} rain={b(r)}\")(check-sat)(get-value (speed))(pop 1)\n")
run("z09_combinacoes_velocidade", s)

# z10: fronteira: speed>100 em 100 (falso) e 101 (verdadeiro); speed>50 em 50 e 51
run("z10_fronteira", "(set-logic QF_LIA)\n(declare-const speed Int)\n"
    "(push 1)(assert (= speed 100))(assert (> speed 100))(check-sat)(pop 1)\n"
    "(push 1)(assert (= speed 101))(assert (> speed 100))(check-sat)(pop 1)\n"
    "(push 1)(assert (= speed 50))(assert (> speed 50))(check-sat)(pop 1)\n"
    "(push 1)(assert (= speed 51))(assert (> speed 50))(check-sat)(pop 1)\n")

# z11: tabela de regressao (consistencia aritmetica)
run("z11_tabela_regressao", """(set-logic QF_LIA)
(echo "VM: testes = condicoes + requisitos (todos completos)")
(push 1)(assert (= (+ 21 5) 26))(check-sat)(pop 1)
(echo "NPP: 29+11 = 40")
(push 1)(assert (= (+ 29 11) 40))(check-sat)(pop 1)
(echo "TIS: incompletos = 17-14 = 3; nao-equivalentes = 450-21 = 429 >= 428 pegos")
(push 1)(assert (= (- 17 14) 3))(assert (= (- 450 21) 429))(assert (<= 428 429))(check-sat)(pop 1)
(echo "VM: 152 mutantes, 0 equivalentes, 152 pegos")
(push 1)(assert (= (- 152 0) 152))(check-sat)(pop 1)
(echo "NPP: 146 mutantes, 0 equivalentes, 146 pegos")
(push 1)(assert (= (- 146 0) 146))(check-sat)(pop 1)
(echo "total combinacoes 152+268+76 = 496; impossiveis 4+4+1 = 9; testes 26+80+40=146; req 5+17+11=33; cond 21+69+29=119")
(push 1)(assert (= (+ 152 268 76) 496))(assert (= (+ 4 4 1) 9))(assert (= (+ 26 80 40) 146))(assert (= (+ 5 17 11) 33))(assert (= (+ 21 69 29) 119))(check-sat)(pop 1)
(echo "2^20 aproximadamente 1 milhao")
(push 1)(assert (= (* 1024 1024) 1048576))(check-sat)(pop 1)
""")

# z12: check -- conjunto de testes (A and B) or C
def chk(name, tests, wanted):
    s = ("(set-logic QF_LIA)\n(define-fun f ((A Bool)(B Bool)(C Bool)) Bool (or (and A B) C))\n"
         "(define-fun sens ((A Bool)(B Bool)(C Bool) (c Int)) Bool (ite (= c 0) (not (= (f A B C) (f (not A) B C))) (ite (= c 1) (not (= (f A B C) (f A (not B) C))) (not (= (f A B C) (f A B (not C)))))))\n")
    # pares possiveis dentro do conjunto de testes, por condicao
    for ci, cn in enumerate("ABC"):
        alts = []
        for i, t1 in enumerate(tests):
            for j, t2 in enumerate(tests):
                if t1[ci] == t2[ci]: continue
                if (f"(f {' '.join(map(b,t1))})" ):
                    alts.append(f"(and (not (= (f {' '.join(map(b,t1))}) (f {' '.join(map(b,t2))}))) (sens {' '.join(map(b,t1))} {ci}) (sens {' '.join(map(b,t2))} {ci}))")
        expr = f"(or {' '.join(alts)})" if alts else "false"
        s += f"(echo \"condicao {cn} demonstrada no conjunto?\")(push 1)(assert {expr})(check-sat)(pop 1)\n"
    run(name, s)
full = [(True, True, False), (False, True, False), (True, False, False), (True, False, True)]
chk("z12_check_completo", full, "ABC sat")
chk("z12b_check_parcial_T1T2", full[:2], "A sat; B,C unsat")
chk("z12c_check_parcial_T1T3", [full[0], full[2]], "B sat; A,C unsat")

# resultado esperado dos testes completos
s = "(set-logic QF_UF)\n(define-fun f ((A Bool)(B Bool)(C Bool)) Bool (or (and A B) C))\n"
for i, t in enumerate(full, 1):
    s += f"(echo \"T{i} {t}\")(simplify (f {' '.join(map(b,t))}))\n"
run("z12d_check_esperado", s)

# z13: verify -- conflito = guardas simultaneamente satisfativeis e valores diferentes
run("z13_verify_conflito", """(set-logic ALL)
(declare-datatypes ((Sw 0)) (((on) (off))))
(declare-const sw Sw)
(echo "G1: sw=on, G2: sw=on  (sobrepoe)")
(push 1)(assert (= sw on))(assert (= sw on))(check-sat)(pop 1)
(echo "G1: sw=on, G3: sw=off (nao sobrepoe)")
(push 1)(assert (= sw on))(assert (= sw off))(check-sat)(pop 1)
""")
# z14: lacuna -- contexto (mode=a ou mode=b), guardas {mode=a}: existe situacao sem guarda?
run("z14_verify_lacuna", """(set-logic ALL)
(declare-datatypes ((M 0)) (((a) (b))))
(declare-const mode M)
(echo "contexto mode=a|b, guardas {mode=a}: lacuna?")
(push 1)(assert (or (= mode a) (= mode b)))(assert (not (= mode a)))(check-sat)(get-model)(pop 1)
(echo "contexto mode=a|b, guardas {mode=a, mode=b}: lacuna?")
(push 1)(assert (or (= mode a) (= mode b)))(assert (not (= mode a)))(assert (not (= mode b)))(check-sat)(pop 1)
""")

# z15: formas A#1/A#2 -- 3 entradas, 2^3 = 8 linhas distintas (informativo)
s = "(set-logic QF_UF)\n(declare-const A Bool)(declare-const B Bool)(declare-const C Bool)\n"
s += "(define-fun f ((A Bool)(B Bool)(C Bool)) Bool (or (and A B) (and (not A) C)))\n"
s += "(echo \"INFORMATIVO: par mascaramento para A#1 (A#1 muda; A#2 mantido por ocorrencia): B=T,C=F\")\n"
s += "(push 1)(assert B)(assert (not C))(assert (not (= (f true B C) (f false B C))))(check-sat)(pop 1)\n"
run("z15_ocorrencias_repetidas_info", s)

# z16: restricoes do operador de comparacao: igualdade/diferenca
run("z16_comparacoes", """(set-logic QF_LIA)
(declare-const x Int)
(echo "x != 5 e x = 5 incompativeis")
(push 1)(assert (distinct x 5))(assert (= x 5))(check-sat)(pop 1)
(echo "x >= 5 e x < 5 incompativeis")
(push 1)(assert (>= x 5))(assert (< x 5))(check-sat)(pop 1)
(echo "x <= 5 e x > 5 incompativeis")
(push 1)(assert (<= x 5))(assert (> x 5))(check-sat)(pop 1)
""")

# --- resumo
lines = ["# Resumo das respostas Z3 (gerado)", ""]
for (tag, variant), (k, res) in summary.items():
    lines.append(f"- {tag} [{variant}]: respostas por k = {res}; minimo = {k}")
lines.append("")
for n, o in log:
    lines.append(f"- {n}: {o}")
(OUT / "RESUMO.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
