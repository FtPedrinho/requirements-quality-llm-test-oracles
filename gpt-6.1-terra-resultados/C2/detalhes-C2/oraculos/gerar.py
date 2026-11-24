import itertools
import json
from pathlib import Path

import z3

ROOT = Path(__file__).parent
TIMEOUT = 60000
cases = []
queries = []
case_number = 0


def solver_result(label, assertions, variables):
    solver = z3.Solver()
    solver.set(timeout=TIMEOUT)
    solver.add(*assertions)
    result = solver.check()
    if result == z3.unknown:
        raise RuntimeError(f"{label}: unknown: {solver.reason_unknown()}")
    model = solver.model() if result == z3.sat else None
    witness = {}
    if model is not None:
        for variable in variables:
            witness[str(variable)] = str(model.eval(variable, model_completion=True))
    smt = solver.sexpr()
    queries.append({"id": label, "status": str(result), "testemunha": witness, "smtlib": smt})
    return result, model


def add_case(**fields):
    global case_number
    case_number += 1
    fields["id"] = f"C{case_number:03}"
    cases.append(fields)


A, B, C, D = z3.Bools("A B C D")
templates = [
    ("A", (A,), A),
    ("A and B", (A, B), z3.And(A, B)),
    ("A && B", (A, B), z3.And(A, B)),
    ("A /\\ B", (A, B), z3.And(A, B)),
    ("A or B", (A, B), z3.Or(A, B)),
    ("A || B", (A, B), z3.Or(A, B)),
    ("A \\/ B", (A, B), z3.Or(A, B)),
    ("not A", (A,), z3.Not(A)),
    ("! A", (A,), z3.Not(A)),
    ("A and (not B)", (A, B), z3.And(A, z3.Not(B))),
    ("(not A) or B", (A, B), z3.Or(z3.Not(A), B)),
    ("(A and B) or C", (A, B, C), z3.Or(z3.And(A, B), C)),
    ("(A or B) and C", (A, B, C), z3.And(z3.Or(A, B), C)),
    ("(A and B) or (not A and C)", (A, B, C), z3.Or(z3.And(A, B), z3.And(z3.Not(A), C))),
    ("not (A and (B or C))", (A, B, C), z3.Not(z3.And(A, z3.Or(B, C)))),
]
quote_truth = "para  entradas distintas  expressão, são consideradas  2ⁿ combinações  calculado  resultado da guada em cada"

for expression, variables, formula in templates:
    for values in itertools.product((False, True), repeat=len(variables)):
        assertions = [variable == value for variable, value in zip(variables, values)] + [D == formula]
        result, model = solver_result(f"truth-{case_number + 1:03}", assertions, [*variables, D])
        if result != z3.sat:
            raise RuntimeError(f"Vetor booleano inviável: {expression} {values}")
        expected = z3.is_true(model.eval(D, model_completion=True))
        proof, _ = solver_result(f"unico-{case_number + 1:03}", assertions + [D != expected], [])
        if proof != z3.unsat:
            raise RuntimeError(f"Resultado não único: {expression} {values}")
        add_case(
            tipo="truth", expressao=expression,
            entradas={str(variable): value for variable, value in zip(variables, values)},
            esperado=expected, precondicao="entradas booleanas sem restrição",
            regra=formula.sexpr(), vinculo="Conectivos de R02 e tabela de R01",
            referencia="R01, R02", citacao=quote_truth, classificacao="CONFORME À DOCUMENTAÇÃO",
            evidencia_z3=f"truth-{case_number + 1:03}; unico-{case_number + 1:03}",
        )


def cli(label, args, expected, rule, reference, quote, evidence, validation="exit"):
    add_case(
        tipo="cli", objetivo=label, argumentos=args, esperado=expected,
        validacao=validation, precondicao="fontes e dependências da rodada disponíveis",
        regra=rule, vinculo="Regra deduzida da definição citada e, quando aplicável, da fórmula SMT",
        referencia=reference, citacao=quote, classificacao="CONFORME À DOCUMENTAÇÃO",
        evidencia_z3=evidence,
    )


quote_code = "`0`: comndo concluido  apontr os prblemas dscrtos pra  cdgo `2`; `1`: entraa invalida; `2`: resutado vido  processamto"
quote_pair = "essa conição muda,  resultado  decisão  muda"
simple_guards = ["A", "not A", "A and B", "A or B", "A and (not B)", "(not A) or B", "(A and B) or C", "(A or B) and C"]
for expression in simple_guards:
    for option in ([], ["--unique-cause"]):
        cli("Análise de guarda com par para cada ocorrência", ["analyze", expression, *option], 0,
            "cada condição tem par independente; logo não há condição sem par",
            "R04, R13", quote_pair, "pares-simples")
for expression in ("A and not A", "A or not A"):
    for option in ([], ["--unique-cause"]):
        cli("Decisão constante sem par", ["analyze", expression, *option], 2,
            "a decisão constante não pode mudar entre duas linhas", "R04, R13", quote_code, "constantes")
for expression, constraint in [("A and B", "A"), ("A or B", "A"), ("A and B", "not A or B")]:
    cli("Restrição impede ao menos um par de causa única", ["analyze", expression, "--constraint", constraint, "--unique-cause"], 2,
        "não existe par viável de causa única para ao menos uma ocorrência", "R10, R13", quote_code, "restricao-and-a; restricao-or-a; restricao-implica")
for expression, size in [("A", 2), ("A and B", 3), ("A or B", 3), ("(A and B) or C", 4)]:
    cli("Suíte exata mínima em causa única", ["analyze", expression, "--exact", "--unique-cause", "--format", "json"], size,
        f"mínimo de {size} vetores para os pares independentes", "R05, R09",
        "`--exact`,  Z   3 pocura  suíte de tamanho mnimo", f"minimo-{expression}-{size - 1}; minimo-{expression}-{size}", "exact_size")
for expression in ("A", "A and B", "A or B", "(A and B) or C"):
    cli("Pares em modo direto", ["analyze", expression, "--direct", "--format", "json"], 0,
        "há par para cada condição; modo direto não constrói tabela completa",
        "R04, R09, R13", "Paes pedds dreto  Z   3,  mnar a tabela ( 30 entradas)",
        "pares-simples")
for form in ("text", "json", "csv", "truth-csv"):
    cli("Formato documentado", ["analyze", "A and B", "--format", form], 0,
        "guarda completa e relatório no formato pedido", "R13, R16",
        "`text` (pdrão), `json`, `csv` (suíte)  `truth-csv` (tabela-verdade intea)",
        "pares-simples", "json" if form == "json" else "nonempty")
cli("Restrição numérica implica impossibilidade",
    ["analyze", "speed > 100 or speed > 50", "--z3", "--format", "json"], 2,
    "speed > 100 implica speed > 50; primeira ocorrência fica sem par viável",
    "R07, R13", "Combinaçoes impossiveis descrtadas  valoes concretos", "implicacao")
cli("Fronteira documentada", ["analyze", "speed > 100", "--z3", "--boundary", "--format", "json"], [100, 101],
    "fronteiras do exemplo são 100 e 101", "R08", "`speed > 100` → 100  101", "fronteira", "boundary")
for args, expected, rule, proof in [
    (["verify", "-f", "@simples"], 2, "A falsa produz lacuna", "gap-a"),
    (["verify", "-f", "@complementar"], 0, "A ou não A é sempre verdadeira; sem ações conflitantes", "gap-complementar"),
    (["verify", "-f", "@simples", "--context", "A"], 0, "no contexto A, A é verdadeira", "gap-contexto"),
    (["verify", "-f", "@complementar", "--format", "json"], 0, "guardas complementares, sem lacuna", "gap-complementar"),
]:
    cli("Verificação de lacunas", args, expected, rule, "R11, R13", "lacunas (nnum requisito vale)", proof)
cli("Fonte mcdc com comentário", ["analyze", "-f", "@complementar"], 0,
    "duas guardas simples possuem pares", "R04, R14", "um requisito  linha, `ID: expressão`. Lnhas com `#`  comentrios", "pares-simples")
for expression in ("A and", "(A or B", "A @ B", ""):
    if expression == "A @ B":
        add_case(
            tipo="diagnostico", objetivo="Operador não descrito na tabela",
            argumentos=["analyze", expression], esperado=None,
            precondicao="entrada textual de expressão",
            regra="Não há afirmação de que os operadores listados são os únicos aceitos",
            vinculo="Omissão documental", referencia="R02, R13",
            citacao="`1`: entraa invalida",
            classificacao="INDETERMINADO — OMISSÃO", evidencia_z3="não aplicável",
        )
        continue
    cli("Expressão sintaticamente incompleta ou inválida", ["analyze", expression], 1,
        "entrada não constitui expressão lógica válida", "R01, R13", "`1`: entraa invalida", "não aplicável")

for variant in ("vlue", "value"):
    add_case(
        tipo="diagnostico", objetivo=f"Grafia da coluna CSV {variant}",
        argumentos=["check", "A", "--tests", "@csv-" + variant],
        esperado=None, precondicao="CSV com valores booleanos",
        regra="O exemplo contém vlue; não especifica inequivocamente a grafia aceita em geral",
        vinculo="Omissão/ambiguidade documental", referencia="R12",
        citacao="As colunas `decision`  `expected_outcome` são opcionis",
        classificacao="INDETERMINADO — AMBIGUIDADE", evidencia_z3="não aplicável",
    )
add_case(
    tipo="diagnostico", objetivo="Campo de guarda JSON literal do exemplo",
    argumentos=["analyze", "--json", "@json-literal"],
    esperado=None, precondicao="JSON baseado no formato apresentado",
    regra="O exemplo usa gard; o texto não resolve se essa grafia representa o campo obrigatório",
    vinculo="Ambiguidade documental", referencia="R15", citacao='"gard": "the_system_mode = idle /\\\\ the_coin_sensor = true"',
    classificacao="INDETERMINADO — AMBIGUIDADE", evidencia_z3="não aplicável",
)

# Independently check the satisfiability of the boolean, numeric and pair constraints.
x = z3.Real("speed")
for label, constraints, variables, expected in [
    ("implicacao", [x > 100, z3.Not(x > 50)], [], z3.unsat),
    ("fronteira-100", [x == 100, z3.Not(x > 100)], [x], z3.sat),
    ("fronteira-101", [x == 101, x > 100], [x], z3.sat),
    ("gap-a", [z3.Not(A)], [A], z3.sat),
    ("gap-complementar", [z3.Not(z3.Or(A, z3.Not(A)))], [], z3.unsat),
    ("gap-contexto", [A, z3.Not(A)], [], z3.unsat),
    ("constantes-false", [z3.Xor(z3.And(A, z3.Not(A)), z3.And(B, z3.Not(B)))], [], z3.unsat),
    ("constantes-true", [z3.Xor(z3.Or(A, z3.Not(A)), z3.Or(B, z3.Not(B)))], [], z3.unsat),
]:
    result, _ = solver_result(label, constraints, variables)
    if result != expected:
        raise RuntimeError(f"Resultado SMT inesperado em {label}: {result}")

# For each documented manual restriction, show that one input has no pair.
for label, decision, constraint, target in [
    ("restricao-and-a", z3.And(A, B), A, A),
    ("restricao-or-a", z3.Or(A, B), A, A),
    ("restricao-implica", z3.And(A, B), z3.Or(z3.Not(A), B), B),
]:
    a0, b0, a1, b1 = z3.Bools("a0 b0 a1 b1")
    f0 = z3.substitute(decision, (A, a0), (B, b0))
    f1 = z3.substitute(decision, (A, a1), (B, b1))
    c0 = z3.substitute(constraint, (A, a0), (B, b0))
    c1 = z3.substitute(constraint, (A, a1), (B, b1))
    changed = a0 != a1 if target.eq(A) else b0 != b1
    unchanged = b0 == b1 if target.eq(A) else a0 == a1
    status, _ = solver_result(label, [c0, c1, changed, unchanged, f0 != f1], [])
    if status != z3.unsat:
        raise RuntimeError(f"Restrição não bloqueou todos os pares: {label}")

# A unique-cause pair differs only in the selected input and changes the decision.
for expression, variables, formula in [(x[0], x[1], x[2]) for x in templates if x[0] in simple_guards]:
    for target in variables:
        before = {v: z3.Bool(f"{v}_before") for v in variables}
        after = {v: z3.Bool(f"{v}_after") for v in variables}
        first = z3.substitute(formula, *[(v, before[v]) for v in variables])
        second = z3.substitute(formula, *[(v, after[v]) for v in variables])
        constraints = [before[target] != after[target], first != second]
        constraints.extend(before[v] == after[v] for v in variables if v is not target)
        status, _ = solver_result(f"par-{expression}-{target}", constraints, list(before.values()) + list(after.values()))
        if status != z3.sat:
            raise RuntimeError(f"Par não encontrado: {expression} {target}")

# For the four named simple expressions, prove the exact minimum by exhaustive
# selection of complete Boolean rows and unique-cause pairs.
for expression, variables, formula in [(x[0], x[1], x[2]) for x in templates if x[0] in ("A", "A and B", "A or B", "(A and B) or C")]:
    rows = list(itertools.product((False, True), repeat=len(variables)))
    chosen = [z3.Bool(f"selected_{i}") for i in range(len(rows))]
    result_by_row = []
    for values in rows:
        simplified = z3.simplify(z3.substitute(formula, *[(var, z3.BoolVal(val)) for var, val in zip(variables, values)]))
        result_by_row.append(z3.is_true(simplified))
    requirements = []
    for i, _ in enumerate(variables):
        pairs = [
            z3.And(chosen[a], chosen[b])
            for a in range(len(rows)) for b in range(a + 1, len(rows))
            if rows[a][i] != rows[b][i]
            and all(rows[a][j] == rows[b][j] for j in range(len(variables)) if j != i)
            and result_by_row[a] != result_by_row[b]
        ]
        requirements.append(z3.Or(pairs))
    minimum = len(variables) + 1
    for limit, wanted in ((minimum - 1, z3.unsat), (minimum, z3.sat)):
        assertions = requirements + [z3.PbLe([(v, 1) for v in chosen], limit)]
        status, _ = solver_result(f"minimo-{expression}-{limit}", assertions, chosen)
        if status != wanted:
            raise RuntimeError(f"Mínimo inesperado: {expression} {limit} {status}")

with (ROOT / "casos.json").open("x", encoding="utf-8") as file:
    file.write(json.dumps(cases, ensure_ascii=False, indent=2) + "\n")
with (ROOT / "resultado-z3.json").open("x", encoding="utf-8") as file:
    file.write(json.dumps({
    "versao": z3.get_full_version(), "timeout_ms": TIMEOUT, "consultas": queries,
    "limite": "Z3 verifica as fórmulas, não a fidelidade de tradução documental.",
    }, ensure_ascii=False, indent=2) + "\n")
with (ROOT / "formulas.smt2").open("x", encoding="utf-8") as file:
    for query in queries:
        file.write(f'; {query["id"]}\n(reset)\n(set-option :timeout {TIMEOUT})\n')
        file.write(query["smtlib"])
        file.write("\n(check-sat)\n")
        if query["status"] == "sat":
            file.write("(get-model)\n")
print("Casos gerados:", len(cases))
print("Consultas SMT:", len(queries))
print("Conformes:", sum(c["classificacao"] == "CONFORME À DOCUMENTAÇÃO" for c in cases))
print("Indeterminados:", sum(c["classificacao"].startswith("INDETERMINADO") for c in cases))
