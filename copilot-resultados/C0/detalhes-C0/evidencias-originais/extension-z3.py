import json
from pathlib import Path
import z3

a, b = z3.Bools("A B")
x = z3.Int("x")
queries = [
    ("restricao-A-falso", [a, z3.Not(a)]),
    ("restricao-B-falso", [a, z3.Not(b)]),
    ("restricao-B-verdadeiro", [a, b]),
    ("conflito-duas-guardas", [a, b, z3.And(a, b), z3.Or(a, b)]),
    ("guardas-complementares-nao-se-sobrepoem", [a, z3.Not(a)]),
    ("complementares-sem-lacuna", [z3.Or(a, z3.Not(a)), z3.Not(z3.Or(a, z3.Not(a)))]),
    ("lacuna", [z3.Or(a, z3.Not(a)), z3.Not(a)]),
    ("fronteira-nao-satisfaz", [x == 3, z3.Not(x > 3)]),
    ("fronteira-satisfaz", [x == 4, x > 3]),
]
evidence = []
for name, formulas in queries:
    solver = z3.Solver()
    solver.add(*formulas)
    result = solver.check()
    if result == z3.unknown:
        raise RuntimeError(f"Z3 unknown: {name}")
    evidence.append({"id": name, "smtlib": solver.to_smt2(), "resultado": str(result),
                     "testemunha": str(solver.model()) if result == z3.sat else None})
Path(__file__).with_name("extension-z3.json").write_text(
    json.dumps({"versao": z3.get_version_string(), "consultas": evidence}, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8")
