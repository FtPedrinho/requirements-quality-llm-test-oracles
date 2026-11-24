"""Testemunhas SMT independentes para a extensão, sem importar o SUT."""
import json
from pathlib import Path

import z3

root = Path(__file__).resolve().parent
x = z3.Int("x")
operators = [
    ("=", x == 0, 0, 1), ("==", x == 0, 0, 1), ("!=", x != 0, 1, 0),
    ("<", x < 0, -1, 0), ("<=", x <= 0, 0, 1), (">", x > 0, 1, 0), (">=", x >= 0, 0, -1),
]
entries, blocks = [], []
for name, expr, yes, no in operators:
    for val, expected in ((yes, True), (no, False)):
        solver = z3.Solver()
        solver.add(x == val, expr == expected)
        result = solver.check()
        if result != z3.sat:
            raise RuntimeError(f"Z3 {result} para {name} {val} {expected}")
        entries.append({"operador": name, "esperado": expected, "resultado": str(result),
                        "testemunha": str(solver.model()[x])})
        blocks.append(f"; x {name} 0, x={val}, resultado={expected}\n" + solver.to_smt2())
(root / "extensao-formulas.smt2").write_text("\n(reset)\n".join(blocks), encoding="utf-8")
(root / "extensao-z3.json").write_text(json.dumps(
    {"versao": z3.get_version_string(), "consultas": entries}, ensure_ascii=False, indent=2
), encoding="utf-8")
print("14 consultas sat com testemunhas")
