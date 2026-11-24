"""Gera as consultas SMT-LIB 2 do oraculo C1 e as executa com o Z3 independente.

Uso: python -I gerar_smt.py <caminho-do-z3.exe>
Escreve smt/<ID>.smt2 e smt/<ID>.out. Nao importa nem executa nenhum codigo do SUT.
Definicao usada para "par de causa unica": duas linhas que diferem apenas na
condicao i e cujo resultado da decisao difere (leitura do termo "causa unica").
"""
import itertools
import os
import subprocess
import sys

Z3 = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "smt")
os.makedirs(OUT, exist_ok=True)


def b(v):
    return "true" if v else "false"


def rows(n):
    # linha 0 = tudo verdadeiro (doc: "a linha 0 e tudo verdadeiro")
    return list(itertools.product([True, False], repeat=n))


def defun(vars_, body):
    args = " ".join(f"({v} Bool)" for v in vars_)
    return f"(define-fun f ({args}) Bool {body})\n"


def rowcall(r):
    return "(f " + " ".join(b(x) for x in r) + ")"


def truth_query(vars_, body):
    s = "(set-logic ALL)\n" + defun(vars_, body) + "(check-sat)\n"
    s += "(get-value (" + " ".join(rowcall(r) for r in rows(len(vars_))) + "))\n"
    return s


def pair_query(vars_, body, i):
    n = len(vars_)
    s = "(set-logic ALL)\n" + defun(vars_, body)
    for j in range(n):
        s += f"(declare-const x{j} Bool)\n(declare-const y{j} Bool)\n"
    for j in range(n):
        s += f"(assert (= x{j} y{j}))\n" if j != i else f"(assert (not (= x{j} y{j})))\n"
    s += "(assert (not (= (f " + " ".join(f"x{j}" for j in range(n)) + ") (f " + " ".join(f"y{j}" for j in range(n)) + "))))\n"
    s += "(check-sat)\n(get-model)\n"
    return s


def minsuite_query(vars_, body):
    """Suite minima (causa unica): menor conjunto de linhas contendo um par por entrada."""
    n = len(vars_)
    rs = rows(n)
    s = "(set-logic ALL)\n" + defun(vars_, body)
    for k in range(len(rs)):
        s += f"(declare-const s{k} Bool)\n"
    idx = {r: k for k, r in enumerate(rs)}

    def val(r):  # avalia ground por Z3 via define-fun inline
        return rowcall(r)

    for i in range(n):
        alts = []
        for r in rs:
            r2 = list(r)
            r2[i] = not r2[i]
            r2 = tuple(r2)
            if idx[r] < idx[r2]:
                alts.append(f"(and s{idx[r]} s{idx[r2]} (not (= {val(r)} {val(r2)})))")
        s += "(assert (or false " + " ".join(alts) + "))\n"
    s += "(minimize (+ " + " ".join(f"(ite s{k} 1 0)" for k in range(len(rs))) + "))\n"
    s += "(check-sat)\n(get-objectives)\n"
    return s


def run(name, text):
    p = os.path.join(OUT, name + ".smt2")
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    r = subprocess.run([Z3, "-smt2", p], capture_output=True, text=True, timeout=120)
    with open(os.path.join(OUT, name + ".out"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(r.stdout + (("\n[stderr]\n" + r.stderr) if r.stderr.strip() else ""))
    first = r.stdout.strip().splitlines()[0] if r.stdout.strip() else "VAZIO"
    print(f"{name}: {first}")


def cond_all(vars_, body, name):
    run(f"{name}_tabela", truth_query(vars_, body))
    for i, v in enumerate(vars_):
        run(f"{name}_par_{v}", pair_query(vars_, body, i))


# ---------------------------------------------------------------- expressoes
AND_B = ("A", "B"), "(and A B)"
# S01  A and not B
run("S01_tabela", truth_query(("A", "B"), "(and A (not B))"))
run("S01_minsuite_causa_unica", minsuite_query(("A", "B"), "(and A (not B))"))
# S02/S03  (A and B) or C
cond_all(("A", "B", "C"), "(or (and A B) C)", "S02")
run("S02_minsuite_causa_unica", minsuite_query(("A", "B", "C"), "(or (and A B) C)"))
# S04  and de 4
run("S04_minsuite_causa_unica", minsuite_query(("A", "B", "C", "D"), "(and A B C D)"))
# S06  ((E or D) and (not A or D)) or B
run("S06_tabela", truth_query(("E", "D", "A", "B"), "(or (and (or E D) (or (not A) D)) B)"))
run("S06_minsuite_causa_unica_informativo", minsuite_query(("E", "D", "A", "B"), "(or (and (or E D) (or (not A) D)) B)"))
# S07  paridade de 3 entradas escrita com and/or/not
x = "(or (and A (not B)) (and (not A) B))"
par = f"(or (and {x} (not C)) (and (not {x}) C))"
s = "(set-logic ALL)\n" + defun(("A", "B", "C"), par)
s += "(define-fun g ((A Bool) (B Bool) (C Bool)) Bool (xor (xor A B) C))\n"
s += "(declare-const A Bool)(declare-const B Bool)(declare-const C Bool)\n(assert (not (= (f A B C) (g A B C))))\n(check-sat)\n"
run("S07_equivalencia_com_paridade", s)
run("S07_minsuite_causa_unica", minsuite_query(("A", "B", "C"), par))
# A03  A or (A and B): B redundante (f == A)
s = "(set-logic ALL)\n(declare-const A Bool)(declare-const B Bool)\n(assert (not (= (or A (and A B)) A)))\n(check-sat)\n"
run("A03_equivalencia_com_A", s)
run("A03_par_B", pair_query(("A", "B"), "(or A (and A B))", 1))
run("A03_par_A", pair_query(("A", "B"), "(or A (and A B))", 0))
# A04  A or not A: tautologia
s = "(set-logic ALL)\n(declare-const A Bool)\n(assert (not (or A (not A))))\n(check-sat)\n"
run("A04_tautologia", s)
# A05  A and B com restricao  not A or not B  (bloqueada)
s = "(set-logic ALL)\n(declare-const x0 Bool)(declare-const x1 Bool)(declare-const y0 Bool)(declare-const y1 Bool)\n"
s += "(assert (or (not x0) (not x1)))(assert (or (not y0) (not y1)))\n"
s += "(assert (= x1 y1))(assert (not (= x0 y0)))(assert (not (= (and x0 x1) (and y0 y1))))\n(check-sat)\n"
run("A05_par_A_com_restricao", s)
s2 = s.replace("(assert (or (not x0) (not x1)))(assert (or (not y0) (not y1)))\n", "")
run("A05_par_A_sem_restricao", s2)
s = s.replace("(assert (= x1 y1))(assert (not (= x0 y0)))", "(assert (= x0 y0))(assert (not (= x1 y1)))")
run("A05_par_B_com_restricao", s)
# T01 / T02 / T03
run("T01_tabela", truth_query(("A", "B"), "(and A B)"))
run("T02_tabela", truth_query(("A", "B", "C"), "(or A (and B C))"))
run("T03_tabela_leitura_e_antes_de_ou", truth_query(("A", "B", "C"), "(or A (and B C))"))
run("T03_tabela_leitura_alternativa_refutada", truth_query(("A", "B", "C"), "(and (or A B) C)"))
# C01
run("C01_tabela_entradas_distintas", truth_query(("A", "B", "C"), "(or (and A B) (and (not A) C))"))
# K  check (termos fechados)
def pairs_closed(tests, i, nv, f):
    alts = []
    for (n1, r1, _) in tests:
        for (n2, r2, _) in tests:
            if n1 < n2 and all((r1[j] == r2[j]) == (j != i) for j in range(nv)) is False:
                pass
    return alts


def check_query(name, vars_, body, tests):
    """tests: lista (id, linha, esperado). Para cada entrada i: existe par entre os testes dados?"""
    n = len(vars_)
    s = "(set-logic ALL)\n" + defun(vars_, body)
    for i, v in enumerate(vars_):
        alts = []
        for (n1, r1, e1) in tests:
            for (n2, r2, e2) in tests:
                if n1 < n2 and all((r1[j] != r2[j]) == (j == i) for j in range(n)):
                    alts.append(f"(not (= {rowcall(r1)} {rowcall(r2)}))")
        s += f"(push)\n(assert (or false {' '.join(alts)}))\n(echo \"entrada {v}: par existe?\")\n(check-sat)\n(pop)\n"
    s += "(check-sat)\n"
    for (tid, r, e) in tests:
        s += f"(echo \"{tid}: valor calculado de f abaixo; esperado={b(e)}\")\n(get-value ({rowcall(r)}))\n"
    run(name, s)


T = True
F = False
AB = ("A", "B")
check_query("K01_check", AB, "(and A B)", [("T1", (T, T), T), ("T2", (F, T), F), ("T3", (T, F), F)])
check_query("K02_check_sem_T3", AB, "(and A B)", [("T1", (T, T), T), ("T2", (F, T), F)])
check_query("K03_check_esperado_errado", AB, "(and A B)", [("T1", (T, T), T), ("T2", (F, T), T), ("T3", (T, F), F)])
ABC = ("A", "B", "C")
body = "(or (and A B) C)"
check_query("K05_check_completa", ABC, body, [("R1", (T, T, F), T), ("R2", (F, T, F), F), ("R3", (T, F, F), F), ("R4", (T, F, T), T)])
check_query("K06_check_sem_R4", ABC, body, [("R1", (T, T, F), T), ("R2", (F, T, F), F), ("R3", (T, F, F), F)])

# Z01  speed > 100 or (speed > 50 and rain)  : fronteira, relacao entre predicados, pares
s = "(set-logic ALL)\n(declare-const x Int)\n(assert (and (> x 100) (not (> x 50))))\n(check-sat)\n"
run("Z01_P_implica_Q", s)
s = "(set-logic ALL)\n(declare-const x Int)\n(assert (not (> x 100)))\n(maximize x)\n(check-sat)\n(get-objectives)\n"
run("Z01_fronteira_P_falso_max", s)
s = "(set-logic ALL)\n(declare-const x Int)\n(assert (> x 100))\n(minimize x)\n(check-sat)\n(get-objectives)\n"
run("Z01_fronteira_P_verdadeiro_min", s)
s = "(set-logic ALL)\n(declare-const x Int)\n(assert (not (> x 50)))\n(maximize x)\n(check-sat)\n(get-objectives)\n"
run("Z01_fronteira_Q_falso_max", s)
s = "(set-logic ALL)\n(declare-const x Int)\n(assert (> x 50))\n(minimize x)\n(check-sat)\n(get-objectives)\n"
run("Z01_fronteira_Q_verdadeiro_min", s)
for i, v in enumerate(("P", "Q", "R")):
    q = "(set-logic ALL)\n(define-fun f ((P Bool) (Q Bool) (R Bool)) Bool (or P (and Q R)))\n"
    for j in range(3):
        q += f"(declare-const x{j} Bool)\n(declare-const y{j} Bool)\n"
    q += "(assert (=> x0 x1))(assert (=> y0 y1))\n"  # P implica Q
    for j in range(3):
        q += f"(assert (= x{j} y{j}))\n" if j != i else f"(assert (not (= x{j} y{j})))\n"
    q += "(assert (not (= (f x0 x1 x2) (f y0 y1 y2))))\n(check-sat)\n(get-model)\n"
    run(f"Z01_par_{v}_com_P_implica_Q", q)
# Z03 enum
s = "(set-logic ALL)\n(declare-datatypes ((Mode 0)) (((idle) (choice))))\n(declare-const m Mode)\n(assert (not (= m idle)))\n(check-sat)\n(get-value (m))\n"
run("Z03_enum_falso_idle", s)
s = "(set-logic ALL)\n(declare-datatypes ((Mode 0)) (((idle) (choice))))\n(declare-const m Mode)\n(assert (not (= m choice)))\n(assert (not (= m idle)))\n(check-sat)\n"
run("Z03_enum_so_dois_valores", s)

# V  verify
enum3 = "(declare-datatypes ((Mode 0)) (((idle) (choice) (preparing))))\n(declare-const m Mode)\n"
s = "(set-logic ALL)\n(declare-datatypes ((Coin 0)) (((t) (f))))\n" + "(declare-const coin Bool)(declare-const mode Bool)\n"
s = "(set-logic ALL)\n(declare-const coin Bool)(declare-const mode_idle Bool)\n(assert coin)\n(assert mode_idle)\n(check-sat)\n"
run("V01_guardas_coexistem", s)
s = "(set-logic ALL)\n(declare-const coin Bool)\n(assert coin)\n(assert (not coin))\n(check-sat)\n"
run("V03_guardas_disjuntas", s)
s = "(set-logic ALL)\n" + enum3 + "(assert (= m preparing))\n(assert (not (= m idle)))\n(assert (not (= m choice)))\n(check-sat)\n(get-value (m))\n"
run("V04_lacuna_em_preparing", s)
s = "(set-logic ALL)\n" + enum3 + "(assert (= m idle))\n(assert (not (= m idle)))\n(assert (not (= m choice)))\n(check-sat)\n"
run("V05_sem_lacuna_em_idle", s)
s = "(set-logic ALL)\n(declare-const coin Bool)\n(assert (not coin))\n(assert (not (not coin)))\n(check-sat)\n"
run("V02_cobertura_total", s)

# E  limites e contagens por 2^n
for n in (3, 12, 13, 20, 26):
    s = f"; 2^{n} = {2**n} combinacoes de {n} entradas distintas\n(set-logic ALL)\n(check-sat)\n(simplify (^ 2 {n}))\n"
    run(f"L_potencia_{n}", s)
# L: and-chain de n entradas tem exatamente um par por entrada (todas as demais verdadeiras)
for n in (13, 20, 26):
    vs = tuple(f"X{k}" for k in range(1, n + 1))
    q = pair_query(vs, "(and " + " ".join(vs) + ")", 0)
    run(f"L_par_cadeia_and_{n}_entrada_1", q)
print("fim")
