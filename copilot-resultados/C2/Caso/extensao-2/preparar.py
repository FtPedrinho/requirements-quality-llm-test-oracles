import json
from pathlib import Path

import z3

root = Path(__file__).parent
cases = []
proofs = []
A = z3.Bool("A")
X = z3.Real("speed")


def add(kind, title, payload, expected, assertions, wanted, cite, rule):
    case_id = f"Y{len(cases) + 1:03}"
    solver = z3.Solver()
    solver.set(timeout=60000)
    solver.add(*assertions)
    result = solver.check()
    if result == z3.unknown:
        raise RuntimeError(f"{case_id}: unknown {solver.reason_unknown()}")
    if result != wanted:
        raise RuntimeError(f"{case_id}: esperava {wanted}, Z3 respondeu {result}")
    model = solver.model() if result == z3.sat else None
    witness = str(model) if model is not None else None
    proofs.append({"id": case_id, "status": str(result), "testemunha": witness, "smtlib": solver.sexpr()})
    cases.append({
        "id": case_id, "tipo": kind, "objetivo": title, "entrada": payload,
        "esperado": expected, "classificacao": "CONFORME À DOCUMENTAÇÃO",
        "regra": rule, "referencia": cite, "vinculo": "Instância da regra geral congelada no inventário",
        "evidencia_z3": case_id, "precondicao": "variáveis booleanas ou numéricas conforme descrito",
    })


conflict_quote = "Confltos (dois requistos valem jtos  escrvem valoes diferetes)"
add("conflict", "mesma guarda e valores diferentes",
    {"guards": ["A", "A"], "actions": ["x := one", "x := two"]}, True,
    [A, z3.StringVal("one") != z3.StringVal("two")], z3.sat,
    "R11", conflict_quote)
add("conflict", "guardas mutuamente exclusivas",
    {"guards": ["A", "not A"], "actions": ["x := one", "x := two"]}, False,
    [A, z3.Not(A)], z3.unsat,
    "R11", conflict_quote)
add("conflict", "mesma variável e mesmo valor",
    {"guards": ["A", "A"], "actions": ["x := one", "x := one"]}, False,
    [A, z3.StringVal("one") != z3.StringVal("one")], z3.unsat,
    "R11", conflict_quote)
add("conflict", "variáveis escritas distintas",
    {"guards": ["A", "A"], "actions": ["x := one", "y := two"]}, False,
    [A, z3.StringVal("x") == z3.StringVal("y")], z3.unsat,
    "R11", conflict_quote)
gap_quote = "lacunas (nnum requisito vale)"
add("gap", "lacuna em contexto universal explícito",
    {"guards": ["A"], "context": "A or not A"}, True,
    [z3.Or(A, z3.Not(A)), z3.Not(A)], z3.sat,
    "R11", gap_quote)
add("gap", "guardas complementares sem lacuna",
    {"guards": ["A", "not A"], "context": "A or not A"}, False,
    [z3.Or(A, z3.Not(A)), z3.Not(z3.Or(A, z3.Not(A)))], z3.unsat,
    "R11", gap_quote)
add("gap", "contexto coberto pela guarda",
    {"guards": ["A"], "context": "A"}, False,
    [A, z3.Not(A)], z3.unsat,
    "R11", gap_quote)
for first, second, expected in ((True, True, True), (True, False, False), (False, True, True), (False, False, True)):
    constraints = [X > 100 if first else z3.Not(X > 100), X > 50 if second else z3.Not(X > 50)]
    add("feasibility", "combinação de comparações numéricas",
        {"expression": "speed > 100 or speed > 50", "first": first, "second": second}, expected,
        constraints, z3.sat if expected else z3.unsat,
        "R07", "Combinaçoes impossiveis descrtadas  valoes concretos")

for filename, value in (("casos.json", cases), ("resultado-z3.json", {
    "versao": z3.get_full_version(), "timeout_ms": 60000, "consultas": proofs,
    "limite": "Z3 verifica as fórmulas, não a fidelidade da tradução.",
})):
    with (root / filename).open("x", encoding="utf-8") as file:
        file.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
with (root / "formulas.smt2").open("x", encoding="utf-8") as file:
    for proof in proofs:
        file.write(f'; {proof["id"]}\n(reset)\n(set-option :timeout 60000)\n')
        file.write(proof["smtlib"] + "\n(check-sat)\n")
        if proof["status"] == "sat":
            file.write("(get-model)\n")
print("Casos gerados:", len(cases))
print("Consultas SMT:", len(proofs))
