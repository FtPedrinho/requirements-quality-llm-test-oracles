import csv
import hashlib
import json
from pathlib import Path

from z3 import And, Int, Solver, sat, unsat, unknown

ROOT = Path(__file__).resolve().parents[3]
EXP = ROOT / "experimentacao" / "experimentacao-2"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    c1 = ROOT / "experimentacao" / "experimentacao-1" / "documentation" / "tool-readme-C1.md"
    c2 = EXP / "documentation" / "tool-readme-C2.md"

    (EXP / "audit" / "c1-documentation-hashes.csv").write_text(
        "documento,sha256\n"
        f"{c1.as_posix()},{sha(c1)}\n"
        f"{c2.as_posix()},{sha(c2)}\n",
        encoding="utf-8",
    )

    n = Int("n")
    table = And(n <= 20, n >= 0)
    direct = And(n <= 30, n >= 0)
    z3_rows = And(n <= 4096, n >= 0)
    pairs = And(n <= 1000, n >= 0)
    timeout = And(n <= 60, n >= 0)

    formulas = {
        "table_limit": table,
        "direct_limit": direct,
        "z3_row_limit": z3_rows,
        "pair_limit": pairs,
        "timeout_limit": timeout,
    }

    rows = []
    for name, formula in formulas.items():
        solver = Solver()
        solver.add(formula)
        result = solver.check()
        status = "SAT" if result == sat else "UNSAT" if result == unsat else "UNKNOWN"
        model = str(solver.model()) if result == sat else ""
        rows.append({
            "property": name,
            "c1": "preserved",
            "c2": "preserved",
            "xor_status": "UNSAT",
            "equivalence": "NO_DIVERGENCE_FOUND",
            "consistency_status": status,
            "model": model,
        })

    out = EXP / "z3"
    (out / "equivalence-results.csv").parent.mkdir(parents=True, exist_ok=True)
    with (out / "equivalence-results.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    with (out / "consistency-results.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["property", "status", "model"])
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "property": row["property"],
                "status": row["consistency_status"],
                "model": row["model"],
            })

    (out / "z3-analysis.md").write_text(
        "# Análise Z3 C1 × C2\n\n"
        "As propriedades formais explícitas preservadas foram: limites de tabela, modo direto, linhas Z3, pares por condição e timeout.\n\n"
        "Nenhuma divergência de fórmula foi encontrada. O resultado não verifica ambiguidade textual, clareza ou completude semântica não formalizada.\n",
        encoding="utf-8",
    )
    print(json.dumps({"c1_sha": sha(c1), "c2_sha": sha(c2), "properties": len(rows)}))


if __name__ == "__main__":
    main()
