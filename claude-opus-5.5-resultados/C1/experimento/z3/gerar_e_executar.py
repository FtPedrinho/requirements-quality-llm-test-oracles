"""Gera as consultas SMT-LIB do oráculo C1 e as executa no Z3 independente.

Fonte das regras: somente experimentacao-pesquisa/experimentacao-1/documentation/tool-readme-C1.md
(SHA-256 91981FA0...D33B). Nenhum código ou saída do SUT foi consultado.
Uso: python -I gerar_e_executar.py <caminho-do-z3.exe>
"""
import itertools, os, subprocess, sys

Z3 = sys.argv[1]
BASE = os.path.dirname(os.path.abspath(__file__))
QDIR = os.path.join(BASE, "consultas")
ODIR = os.path.join(BASE, "saidas")
queries = {}


def q(name, text):
    queries[name] = text.strip() + "\n"


def bools(names, suffix=""):
    return "\n".join(f"(declare-const {n}{suffix} Bool)" for n in names)


def subst(expr, names, suffix):
    out = expr
    for n in sorted(names, key=len, reverse=True):
        out = out.replace(f"<{n}>", f"{n}{suffix}")
    return out


def uc_pair(tag, names, expr, constraint=None, note=""):
    """Para cada entrada x: existe par de linhas que difere só em x, ambas satisfazendo a
    restrição, com resultado diferente? (definição de par de causa única por entrada)."""
    for x in names:
        body = [f"; {note}", f"; condição alvo: {x}", bools(names, "_1"), bools(names, "_2")]
        for n in names:
            if n != x:
                body.append(f"(assert (= {n}_1 {n}_2))")
        body.append(f"(assert (not (= {x}_1 {x}_2)))")
        if constraint:
            body.append(f"(assert {subst(constraint, names, '_1')})")
            body.append(f"(assert {subst(constraint, names, '_2')})")
        body.append(f"(assert (not (= {subst(expr, names, '_1')} {subst(expr, names, '_2')})))")
        body.append("(check-sat)\n(get-model)")
        q(f"{tag}_par_{x}", "\n".join(body))


# ---- Q01: pares de causa única (que valem também em mascaramento, segundo o C1) ----
uc_pair("Q01_AN01_ABorC", ["A", "B", "C"], "(or (and <A> <B>) <C>)",
        note="(A and B) or C; C1: 'todo par de causa única vale em mascaramento'")
uc_pair("Q01_AN04_AandnotB", ["A", "B"], "(and <A> (not <B>))", note="A and not B")
uc_pair("Q01_AN05_speed_mode", ["S", "M"], "(and <S> <M>)",
        note="speed > 100 /\\ mode = idle, sem Z3: S=speed>100, M=mode=idle tratadas como condições")
uc_pair("Q01_AN13_constraint", ["A", "B", "C"], "(or <A> (and <B> <C>))", "(or (not <A>) <B>)",
        note="A or (B and C) --constraint 'not A or B'")
uc_pair("Q01_AN14_bloq_com_restricao", ["A", "B"], "(and <A> <B>)", "<A>",
        note="A and B --constraint 'A': A deve ficar sem par (unsat)")
uc_pair("Q01_AN14_bloq_sem_restricao", ["A", "B"], "(and <A> <B>)",
        note="A and B sem restrição: A tem par (sat) => falta de par vem da restrição => bloqueada")
uc_pair("Q01_REQ003", ["F", "P"], "(or <F> (and <F> <P>))",
        note="REQ-003 freio or (freio and pedal): pedal sem efeito (unsat) => redundante")

# ---- Q02: tamanho mínimo de suíte com pares de causa única (evidência auxiliar) ----
def min_suite(tag, names, expr, k, note):
    lines = [f"; {note}", f"; k = {k} linhas"]
    for i in range(k):
        lines.append(bools(names, f"_{i}"))
    for x in names:
        alts = []
        for i, j in itertools.combinations(range(k), 2):
            same = [f"(= {n}_{i} {n}_{j})" for n in names if n != x]
            alts.append("(and " + " ".join(same + [f"(not (= {x}_{i} {x}_{j}))",
                        f"(not (= {subst(expr, names, f'_{i}')} {subst(expr, names, f'_{j}')}))"]) + ")")
        lines.append(f"(assert (or {' '.join(alts)}))  ; par para {x}")
    lines.append("(check-sat)\n(get-model)")
    q(f"{tag}_k{k}", "\n".join(lines))

for k in (3, 4):
    min_suite("Q02_AN02_ABorC", ["A", "B", "C"], "(or (and <A> <B>) <C>)", k,
              "(A and B) or C: C1 declara 4 testes; espera-se k=3 unsat e k=4 sat")
for k in (2, 3):
    min_suite("Q02_AN04_AandnotB", ["A", "B"], "(and <A> (not <B>))", k,
              "A and not B: C1 declara 3 testes; espera-se k=2 unsat e k=3 sat")
for k in (4, 5):
    min_suite("Q02_AN27_exata_entradas", ["E", "D", "A", "B"],
              "(or (and (or <E> <D>) (or (not <A>) <D>)) <B>)", k,
              "((E or D) and (not A or D)) or B, causa única POR ENTRADA (aproximação; D se repete). "
              "Só evidência auxiliar: o C1 declara 5 testes para --exact (mascaramento por ocorrência).")

# paridade: a expressão usada no caso AN-12 é equivalente a XOR de 3 entradas
q("Q02_AN12_paridade_equivalencia", """
; a expressão do AN-12 é a paridade (ímpar) de 3 entradas? unsat => equivalente
(declare-const A Bool) (declare-const B Bool) (declare-const C Bool)
(define-fun e () Bool (or (and A (not B) (not C)) (and (not A) B (not C)) (and (not A) (not B) C) (and A B C)))
(assert (not (= e (xor A (xor B C)))))
(check-sat)
""")

# ---- Q03: velocidade: combinações impossíveis e fronteiras ----
for a, b, r in itertools.product([True, False], repeat=3):
    tv = lambda v: "true" if v else "false"
    q(f"Q03_AN29_linha_A{int(a)}_B{int(b)}_R{int(r)}", f"""
; speed > 100 or (speed > 50 and rain): A=speed>100, B=speed>50, R=rain; speed inteiro
(declare-const speed Int) (declare-const rain Bool)
(assert (= (> speed 100) {tv(a)}))
(assert (= (> speed 50) {tv(b)}))
(assert (= rain {tv(r)}))
(check-sat)
(get-model)
""")
for c in (100, 50):
    q(f"Q03_AN31_fronteira_{c}", f"""
; fronteira de speed > {c}: {c+1} satisfaz, {c} não, e não há inteiro entre eles
(declare-const s Int)
(assert (not (and (> {c+1} {c}) (not (> {c} {c})) (forall ((x Int)) (=> (> x {c}) (>= x {c+1}))))))
(check-sat)
""")
uc_pair("Q03_AN42_bloq_z3", ["A", "B"], "(and <A> <B>)", "(=> <A> <B>)",
        note="speed > 100 and speed > 50 com Z3: A=>B; B deve ficar sem par (unsat)")
uc_pair("Q03_AN43_sem_z3", ["A", "B"], "(and <A> <B>)",
        note="speed > 100 and speed > 50 sem Z3: tabela completa, B tem par (sat)")

# ---- Q04: VM, combinações impossíveis por decisão ----
VM_DECL = """
(declare-datatypes () ((Mode idle choice preparing_weak preparing_strong)))
(declare-datatypes () ((Btn released pressed)))
(declare-const the_system_mode Mode)
(declare-const the_coin_sensor Bool)
(declare-const the_coin_sensor_antes Bool)
(declare-const the_coffee_request_button Btn)
(declare-const the_coffee_request_button_antes Btn)
(declare-const the_request_timer Real)
"""
VM = {
    "vm1": ["(= the_system_mode idle)", "(= the_coin_sensor_antes false)", "(= the_coin_sensor true)"],
    "vm2": ["(= the_system_mode choice)", "(= the_coin_sensor false)", "(= the_coin_sensor_antes false)",
            "(not (= the_coffee_request_button_antes pressed))", "(= the_coffee_request_button pressed)",
            "(<= the_request_timer 30.0)"],
    "vm3": ["(= the_system_mode choice)", "(= the_coin_sensor false)", "(= the_coin_sensor_antes false)",
            "(not (= the_coffee_request_button_antes pressed))", "(= the_coffee_request_button pressed)",
            "(> the_request_timer 30.0)"],
    "vm4": ["(= the_system_mode preparing_weak)", "(>= the_request_timer 10.0)", "(<= the_request_timer 30.0)"],
    "vm5": ["(= the_system_mode preparing_strong)", "(>= the_request_timer 30.0)", "(<= the_request_timer 50.0)"],
}
for d, conds in VM.items():
    lines = [f"; VM {d}: viabilidade de cada uma das 2^{len(conds)} combinações (uma check-sat por linha)", VM_DECL]
    for bits in itertools.product([True, False], repeat=len(conds)):
        lines.append("(push)")
        lines.append(f"(echo \"linha {''.join('T' if b else 'F' for b in bits)}\")")
        for c, b in zip(conds, bits):
            lines.append(f"(assert {c})" if b else f"(assert (not {c}))")
        lines.append("(check-sat)\n(pop)")
    q(f"Q04_VM_viabilidade_{d}", "\n".join(lines))

# ---- Q05: VM, conflitos e lacuna no contexto ----
g = {d: "(and " + " ".join(c) + ")" for d, c in VM.items()}
# escritas: mode: vm1 choice, vm2 weak, vm3 strong, vm4 idle, vm5 idle; timer: vm1,vm2,vm3 := 0;
# output: vm4 weak, vm5 strong. Conflito = guardas simultâneas e valores diferentes na mesma variável.
pairs_diff = [("vm1", "vm2"), ("vm1", "vm3"), ("vm1", "vm4"), ("vm1", "vm5"), ("vm2", "vm3"), ("vm2", "vm4"),
              ("vm2", "vm5"), ("vm3", "vm4"), ("vm3", "vm5"), ("vm4", "vm5")]
for a, b in pairs_diff:
    q(f"Q05_VM_conflito_{a}_{b}", f"""
; {a} e {b} escrevem valores diferentes em the_system_mode (e/ou the_coffee_machine_output);
; conflito só se as guardas puderem valer juntas. Esperado pelo C1 (0 conflitos na VM): unsat
{VM_DECL}
(assert {g[a]})
(assert {g[b]})
(check-sat)
""")
q("Q05_VM_lacuna_contexto_preparing_weak", f"""
; verify --context 'the_system_mode = preparing_weak': existe situação em que nenhuma guarda vale? sat => lacuna
{VM_DECL}
(assert (= the_system_mode preparing_weak))
(assert (not (or {' '.join(g.values())})))
(check-sat)
(get-model)
""")

# ---- Q06: verify com JSON montado para o experimento ----
VF_DECL = """
(declare-datatypes () ((Mode a b c)))
(declare-const mode Mode) (declare-const flag Bool) (declare-const sw Bool)
"""
q("Q06_VF01_sobreposicao", VF_DECL + """
; VF-01: d1 'flag = true' escreve mode := a; d2 'sw = true' escreve mode := b. Podem valer juntas? sat => conflito
(assert (= flag true)) (assert (= sw true))
(check-sat) (get-model)
""")
q("Q06_VF03_disjuntas", VF_DECL + """
; VF-03: d1 'flag = true', d2 'flag = false'. Podem valer juntas? unsat => sem conflito
(assert (= flag true)) (assert (= flag false))
(check-sat)
""")
q("Q06_VF04_lacuna", VF_DECL + """
; VF-04: arquivo do VF-01 com --context 'flag = false': nenhuma guarda vale? sat => lacuna
(assert (= flag false)) (assert (not (or (= flag true) (= sw true))))
(check-sat) (get-model)
""")
q("Q06_VF05_sem_lacuna", VF_DECL + """
; VF-05: arquivo do VF-03 com --context 'mode = a': nenhuma guarda vale? unsat => sem lacuna
(assert (= mode a)) (assert (not (or (= flag true) (= flag false))))
(check-sat)
""")

# ---- Q07: consistência aritmética dos números documentados ----
q("Q07_regressao_consistencia", """
; Tabela 'Números travados pela regressão' do C1. Consistência interna: totais, N+1, mutantes.
(declare-const vR Int) (declare-const tR Int) (declare-const nR Int)
(assert (and (= vR 5) (= tR 17) (= nR 11)))
(define-fun ok () Bool (and
  (= (+ 5 17 11) 33) (= (+ 5 14 11) 30) (= (+ 21 69 29) 119) (= (+ 152 268 76) 496)
  (= (+ 4 4 1) 9) (= (+ 26 80 40) 146) (= (+ 152 450 146) 748) (= (+ 0 21 0) 21)
  (= (+ 152 428 146) 726) (= (+ 0 3 1) 4)
  ; VM e NPP: todos completos => testes = condições + requisitos
  (= (+ 21 5) 26) (= (+ 29 11) 40)
  ; detectáveis = mutantes - equivalentes; 727 detectáveis e 1 escapou (Limites conhecidos)
  (= (- 748 21) 727) (= (- 727 726) 1)
  ; VM: combinações = soma de 2^condições (3,6,6,3,3) do arquivo de entrada
  (= (+ 8 64 64 8 8) 152)
  ; VM: testes = soma (condições+1) = 4+7+7+4+4
  (= (+ 4 7 7 4 4) 26)))
(assert (not ok))
(check-sat)
""")
q("Q07_TIS_nao_completos", """
; TIS: 69 condições, 17 requisitos, 14 completos, 80 testes. Se todos fossem N+1 dariam 86.
; Existe distribuição em que os 14 completos têm N+1 e os 3 restantes totalizam 80-? Apenas mostra que
; N+1 não vale para os 17 (86 != 80); o texto não define 'completo'.
(assert (not (= (+ 69 17) 80)))
(check-sat)
""")

# ---- Q08: check: avaliação das guardas para os testes ----
q("Q08_CK05_decisoes_T4", """
; exemplos/decisoes.json #3: (mode = choice /\\ button = true) \\/ coin = true
; T4: mode=idle, button=true, coin=false, esperado T. Guarda = T? unsat => guarda é F => esperado divergente
(declare-datatypes () ((Mode idle choice preparing_strong preparing_weak)))
(declare-const mode Mode) (declare-const button Bool) (declare-const coin Bool)
(assert (= mode idle)) (assert (= button true)) (assert (= coin false))
(assert (or (and (= mode choice) (= button true)) (= coin true)))
(check-sat)
""")
q("Q08_CK05_decisoes_T3", """
; T3: mode=choice, button=true, coin=false, esperado T. Guarda = F? unsat => guarda é T (coerente)
(declare-datatypes () ((Mode idle choice preparing_strong preparing_weak)))
(declare-const mode Mode) (declare-const button Bool) (declare-const coin Bool)
(assert (= mode choice)) (assert (= button true)) (assert (= coin false))
(assert (not (or (and (= mode choice) (= button true)) (= coin true))))
(check-sat)
""")
q("Q08_CK01_AandB", """
; CK-01: A and B com T1=(T,T)->T, T2=(F,T)->F, T3=(T,F)->F. Algum esperado diverge da guarda? unsat => não
(define-fun g ((a Bool) (b Bool)) Bool (and a b))
(assert (or (not (= (g true true) true)) (not (= (g false true) false)) (not (= (g true false) false))))
(check-sat)
""")

# ---- Q09: precedência ----
q("Q09_AN07_precedencia_discrimina", """
; A or (B and C) difere de (A or B) and C? sat => o teste de precedência discrimina
(declare-const A Bool) (declare-const B Bool) (declare-const C Bool)
(assert (not (= (or A (and B C)) (and (or A B) C))))
(check-sat) (get-model)
""")

os.makedirs(QDIR, exist_ok=True)
os.makedirs(ODIR, exist_ok=True)
summary = []
for name, text in sorted(queries.items()):
    qp = os.path.join(QDIR, name + ".smt2")
    with open(qp, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    r = subprocess.run([Z3, "-T:60", qp], capture_output=True, text=True)
    out = r.stdout + (("\n[stderr]\n" + r.stderr) if r.stderr else "")
    with open(os.path.join(ODIR, name + ".out"), "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    answers = [l.strip() for l in r.stdout.splitlines() if l.strip() in ("sat", "unsat", "unknown")]
    summary.append(f"{name}\t{' '.join(answers) if len(answers) < 10 else str(answers.count('sat')) + ' sat / ' + str(answers.count('unsat')) + ' unsat'}")
with open(os.path.join(ODIR, "_resumo.tsv"), "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(summary) + "\n")
print("\n".join(summary))
