"""Formalização independente da fonte C1; não importa módulos do SUT."""
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parent
A, B, C = z3.Bools("A B C")
speed = z3.Int("speed")
rows = []
formulas = []


def solve(name, constraint, variables):
    solver = z3.Solver()
    solver.add(constraint)
    result = solver.check()
    item = {"objetivo": name, "resultado": str(result)}
    if result == z3.sat:
        model = solver.model()
        item["testemunha"] = {
            str(v): str(model.eval(v, model_completion=True)) for v in variables
        }
    elif result == z3.unknown:
        item["motivo"] = solver.reason_unknown()
    rows.append(item)
    formulas.append(f"; {name}\n{solver.to_smt2()}\n")
    return result


for expr_name, expr, variables in [
    ("A", A, [A]),
    ("not_A", z3.Not(A), [A]),
    ("A_and_B", z3.And(A, B), [A, B]),
    ("A_or_B", z3.Or(A, B), [A, B]),
    ("A_and_B_or_C", z3.Or(z3.And(A, B), C), [A, B, C]),
]:
    for mask in range(2 ** len(variables)):
        conditions = [v == bool(mask & (1 << i)) for i, v in enumerate(variables)]
        for outcome in (False, True):
            solve(
                f"{expr_name} vetor={mask} saida={outcome}",
                z3.And(*conditions, expr == outcome),
                variables,
            )

solve("B22 restricao exclui A=T B=F", z3.And(z3.Or(z3.Not(A), B), A, z3.Not(B)), [A, B])
solve("B22 restricao admite A=F B=F", z3.And(z3.Or(z3.Not(A), B), z3.Not(A), z3.Not(B)), [A, B])
solve("B23 impossibilidade speed>100 e nao speed>50", z3.And(speed > 100, speed <= 50), [speed])
solve("B23 fronteira falsa", speed == 100, [speed])
solve("B23 fronteira verdadeira", speed == 101, [speed])
solve("B26 conflito", z3.And(A, 0 != 1), [A])
solve("B27 lacuna", z3.And(z3.Not(A), z3.Not(A)), [A])
solve("B29 B muda decisao", z3.Xor(z3.Or(A, z3.And(A, B)), z3.Or(A, z3.And(A, z3.Not(B)))), [A, B])
solve("B30 A muda entre vetores validos", z3.And(A, z3.Not(A)), [A])

vectors = [(bool(i & 1), bool(i & 2), bool(i & 4)) for i in range(8)]
outcomes = [(a and b) or c for a, b, c in vectors]
selected = z3.Bools("v0 v1 v2 v3 v4 v5 v6 v7")
pairs = []
for condition in range(3):
    choices = []
    for i, left in enumerate(vectors):
        for j in range(i + 1, len(vectors)):
            right = vectors[j]
            if left[condition] != right[condition] and outcomes[i] != outcomes[j] and all(
                left[k] == right[k] for k in range(3) if k != condition
            ):
                choices.append(z3.And(selected[i], selected[j]))
    pairs.append(z3.Or(*choices))

for size in (3, 4):
    result = solve(
        f"B24 cobertura causa unica com no maximo {size} vetores",
        z3.And(*pairs, z3.Sum([z3.If(v, 1, 0) for v in selected]) <= size),
        selected,
    )
    if size == 3 and result != z3.unsat or size == 4 and result != z3.sat:
        raise RuntimeError(f"B24 inesperado: {size}: {result}")

(ROOT / "z3-resultados.json").write_text(
    json.dumps({"versao": z3.get_version_string(), "resultados": rows}, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)
(ROOT / "formulas.smt2").write_text(
    "; Blocos independentes, cada bloco reinicia o contexto.\n"
    + "\n(reset)\n".join(formulas),
    encoding="utf-8",
)
if any(row["resultado"] == "unknown" for row in rows):
    raise RuntimeError("Z3 retornou unknown; consultar z3-resultados.json")
print(f"Z3 {z3.get_version_string()}: {len(rows)} consultas; evidências gravadas.")
