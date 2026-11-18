import importlib.util
import itertools
import json
from pathlib import Path

from z3 import Solver, sat, unsat, unknown, And

ROOT = Path(__file__).resolve().parents[4]
ANALYSIS = ROOT / "experimentacao" / "experimentacao-0" / "z3-analysis"
SCRIPT = ANALYSIS / "scripts" / "analyze_requirements.py"
OUT = ANALYSIS / "results" / "cross-analysis.json"

spec = importlib.util.spec_from_file_location("analyze_requirements", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def load_system(filename):
    path = ROOT / "exemplos" / filename
    data = json.loads(path.read_text(encoding="utf-8"))
    inputs = data["inputs"]
    enum_values = {item["name"]: item["values"] for item in inputs if item["type"] == "enum"}
    variables = {}
    for item in inputs:
        name = item["name"]
        if item["type"] == "enum":
            variables[name] = __import__("z3").Int(name)
        elif item["type"] == "bool":
            variables[name] = __import__("z3").Bool(name)
        elif item["type"] == "int":
            variables[name] = __import__("z3").Int(name)
        else:
            variables[name] = __import__("z3").Real(name)
    constraints = []
    for name, values in enum_values.items():
        constraints.extend([variables[name] >= 0, variables[name] < len(values)])
    records = []
    for decision in data["decisions"]:
        node = module.ExprParser(decision["guard"], set(variables), enum_values).parse()
        expr = module.compile_node(node, variables, enum_values)
        records.append({"decision": decision, "expr": expr})
    return records, constraints


def status(expr, constraints):
    solver = Solver()
    solver.add(*constraints)
    solver.add(expr)
    result = solver.check()
    if result == sat:
        return "SAT", module.z3_model_text(solver.model())
    if result == unsat:
        return "UNSAT", ""
    return "UNKNOWN", ""


def implication(left, right, constraints):
    solver = Solver()
    solver.add(*constraints)
    solver.add(And(left, __import__("z3").Not(right)))
    result = solver.check()
    if result == unsat:
        return "TRUE"
    if result == sat:
        return "FALSE"
    return "UNKNOWN"


def action_conflicts(records, constraints):
    conflicts = []
    for left, right in itertools.combinations(records, 2):
        left_actions = {action.split(":=", 1)[0].strip(): action.split(":=", 1)[1].strip()
                        for action in left["decision"].get("actions", []) if ":=" in action}
        right_actions = {action.split(":=", 1)[0].strip(): action.split(":=", 1)[1].strip()
                         for action in right["decision"].get("actions", []) if ":=" in action}
        for variable in sorted(set(left_actions) & set(right_actions)):
            if left_actions[variable] == right_actions[variable]:
                continue
            result, model = status(And(left["expr"], right["expr"]), constraints)
            if result == "SAT":
                conflicts.append({
                    "left_id": left["decision"]["id"],
                    "right_id": right["decision"]["id"],
                    "variable": variable,
                    "left_action": left_actions[variable],
                    "right_action": right_actions[variable],
                    "satisfying_model": model,
                })
    return conflicts


def main():
    result = {"equivalences": [], "implications": [], "conflicts": []}
    for filename in ("vm-decisoes.json", "tis-decisoes.json", "npp-decisoes.json"):
        records, constraints = load_system(filename)
        system = json.loads((ROOT / "exemplos" / filename).read_text(encoding="utf-8"))["system"]
        for left, right in itertools.combinations(records, 2):
            solver = Solver()
            solver.add(*constraints)
            solver.add(left["expr"] != right["expr"])
            value = solver.check()
            if value == unsat:
                result["equivalences"].append({
                    "system": system,
                    "left_id": left["decision"]["id"],
                    "right_id": right["decision"]["id"],
                })
            left_implies_right = implication(left["expr"], right["expr"], constraints)
            right_implies_left = implication(right["expr"], left["expr"], constraints)
            if left_implies_right != "FALSE" or right_implies_left != "FALSE":
                result["implications"].append({
                    "system": system,
                    "left_id": left["decision"]["id"],
                    "right_id": right["decision"]["id"],
                    "left_implies_right": left_implies_right,
                    "right_implies_left": right_implies_left,
                })
        result["conflicts"].extend(action_conflicts(records, constraints))
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "equivalences": len(result["equivalences"]),
        "implications": len(result["implications"]),
        "conflicts": len(result["conflicts"]),
        "output": str(OUT),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
