from pathlib import Path

import z3


root = Path(__file__).resolve().parent
source = root / "integracao.smt2"
context = z3.Context()
result = z3.z3core.Z3_eval_smtlib2_string(context.ref(), source.read_text(encoding="utf-8"))
if "error" in result.lower() or "unsat" in result or "unknown" in result:
    raise RuntimeError(result)
if sum(line.strip() == "sat" for line in result.splitlines()) != 3:
    raise RuntimeError("Numero inesperado de resultados: " + result)
(root / "integracao-z3.txt").write_text(
    "Z3 " + z3.get_full_version() + "\n" + result, encoding="utf-8"
)
print(result)
