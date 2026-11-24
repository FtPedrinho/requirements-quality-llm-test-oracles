import json
import re
from pathlib import Path

import z3

root = Path(__file__).parent
script = (root / "formulas.smt2").read_text(encoding="utf-8")
reference = json.loads((root / "resultado-z3.json").read_text(encoding="utf-8"))
output = z3.Z3_eval_smtlib2_string(z3.main_ctx().ref(), script)
if isinstance(output, bytes):
    output = output.decode("utf-8")
statuses = re.findall(r"^(sat|unsat|unknown)$", output, re.MULTILINE)
expected = [query["status"] for query in reference["consultas"]]
if statuses != expected or "(error" in output:
    raise RuntimeError(f"Resultados divergentes: {len(statuses)} consultas, esperadas {len(expected)}")
with (root / "reexecucao-z3.txt").open("x", encoding="utf-8") as file:
    file.write("Z3 independente: " + z3.get_full_version() + "\n")
    file.write(output)
print(f"Reexecução SMT: {len(statuses)} resultados confirmados")
