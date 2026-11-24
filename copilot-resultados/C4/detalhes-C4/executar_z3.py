import json
from pathlib import Path

import z3

root = Path(__file__).resolve().parent
cases = json.loads((root / "casos.json").read_text(encoding="utf-8"))
constraints = z3.parse_smt2_file(str(root / "regras.smt2"))
p, q, rain = z3.Bools("p q rain")
speed = z3.Int("speed")
results = []
for case in cases:
    solver = z3.Solver()
    solver.add(constraints)
    solver.add(p == case["p"], q == case["q"], rain == case["rain"])
    result = solver.check()
    item = {"id": case["id"], "resultado": str(result)}
    if result == z3.sat:
        model = solver.model()
        item["testemunha"] = {
            "speed": str(model.eval(speed, model_completion=True)),
            "rain": str(model.eval(rain, model_completion=True)),
        }
    elif result == z3.unknown:
        item["motivo"] = solver.reason_unknown()
    results.append(item)
print(json.dumps({"z3": z3.get_version_string(), "resultados": results}, indent=2))
