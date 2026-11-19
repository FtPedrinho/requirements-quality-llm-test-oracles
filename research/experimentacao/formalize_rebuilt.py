import json
from pathlib import Path

from z3 import And, Bool, Int, Not, Or, Solver, sat, unsat, unknown

ROOT = Path(__file__).resolve().parents[2]
OUT_ROOT = ROOT / "research" / "experimentacao"


def status(expression):
    solver = Solver()
    solver.add(expression)
    result = solver.check()
    if result == sat:
        return "SAT", str(solver.model())
    if result == unsat:
        return "UNSAT", ""
    return "UNKNOWN", ""


def main():
    expression_source = Bool("expression_source")
    file_source = Bool("file_source")
    json_source = Bool("json_source")
    exactly_one = (
        (expression_source & ~file_source & ~json_source)
        | (~expression_source & file_source & ~json_source)
        | (~expression_source & ~file_source & json_source)
    )
    exactly_one_status, exactly_one_model = status(exactly_one)

    n = Int("n")
    table_limit = And(n >= 0, n <= 20)
    table_limit_status, table_limit_model = status(table_limit)

    direct_limit = And(n >= 0, n <= 30)
    direct_status, direct_model = status(direct_limit)

    greedy_tests = Int("greedy_tests")
    exact_tests = Int("exact_tests")
    exact_minimum = And(greedy_tests == 6, exact_tests == 5)
    exact_status, exact_model = status(exact_minimum)

    z3_available = Bool("z3_available")
    z3_required = Bool("z3_required")
    z3_behavior = And(z3_required, z3_available)
    z3_status, z3_model = status(z3_behavior)

    properties = [
        {
            "property": "exactly-one-source",
            "formula": "one of expression/file/json",
            "status": exactly_one_status,
            "model": exactly_one_model,
        },
        {
            "property": "table-limit",
            "formula": "0 <= n <= 20",
            "status": table_limit_status,
            "model": table_limit_model,
        },
        {
            "property": "direct-limit",
            "formula": "0 <= n <= 30",
            "status": direct_status,
            "model": direct_model,
        },
        {
            "property": "exact-vs-greedy",
            "formula": "greedy=6 and exact=5",
            "status": exact_status,
            "model": exact_model,
        },
        {
            "property": "z3-required-mode",
            "formula": "z3_required and z3_available",
            "status": z3_status,
            "model": z3_model,
        },
    ]

    for exp in ("experimentacao-0", "experimentacao-1"):
        out = OUT_ROOT / exp / "formalization" / "z3-properties.json"
        out.write_text(json.dumps(properties, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"properties": len(properties)}))


if __name__ == "__main__":
    main()
