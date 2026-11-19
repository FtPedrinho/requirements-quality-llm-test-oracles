import importlib.util
import itertools
import json
from pathlib import Path

from z3 import Solver, sat, unsat, unknown, And, Not, Xor

ROOT = Path(__file__).resolve().parents[3]
EXP = ROOT / "experimentacao" / "experimentacao-1"
REQ = EXP / "requirements" / "experimental"
OUT = EXP / "formalization"
PARSER = ROOT / "experimentacao" / "experimentacao-0" / "z3-analysis" / "scripts" / "analyze_requirements.py"

spec = importlib.util.spec_from_file_location("exp0_parser", PARSER)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def load_system(filename):
    data = json.loads((REQ / filename).read_text(encoding="utf-8"))
    variables = {}
    enum_values = {}
    kinds = {}
    constraints = []
    for item in data["inputs"]:
        name = item["name"]
        kind = item["type"]
        kinds[name] = kind
        if kind == "enum":
            enum_values[name] = item["values"]
            variables[name] = __import__("z3").Int(name)
            constraints += [variables[name] >= 0, variables[name] < len(item["values"])]
        elif kind == "bool":
            variables[name] = __import__("z3").Bool(name)
        elif kind == "int":
            variables[name] = __import__("z3").Int(name)
        elif kind == "real":
            variables[name] = __import__("z3").Real(name)
    records = []
    for decision in data["decisions"]:
        node = module.ExprParser(decision["guard"], set(variables), enum_values).parse()
        expression = module.compile_node(node, variables, enum_values)
        records.append({
            "id": decision["id"],
            "requirement": decision["requirement"],
            "text": decision["text"],
            "guard": decision["guard"],
            "actions": decision["actions"],
            "node": node,
            "expression": expression,
        })
    return data["system"], records, variables, enum_values, kinds, constraints


def status(expression, constraints):
    solver = Solver()
    solver.add(*constraints)
    solver.add(expression)
    result = solver.check()
    if result == sat:
        model = solver.model()
        items = []
        for declaration in sorted(model.decls(), key=lambda item: item.name()):
            items.append(f"{declaration.name()}={model[declaration]}")
        return "SAT", ", ".join(items)
    if result == unsat:
        return "UNSAT", ""
    return "UNKNOWN", ""


def main():
    (OUT / "results").mkdir(parents=True, exist_ok=True)
    all_results = []
    cross = []
    for filename in ("vm-decisoes.json", "tis-decisoes.json", "npp-decisoes.json"):
        system, records, variables, enum_values, kinds, constraints = load_system(filename)
        for record in records:
            sat_status, model = status(record["expression"], constraints)
            all_results.append({
                "id": record["id"],
                "requirement": record["requirement"],
                "system": system,
                "source": f"experimentacao/experimentacao-1/requirements/experimental/{filename}",
                "text": record["text"],
                "guard": record["guard"],
                "actions": record["actions"],
                "satisfiability": sat_status,
                "model": model,
                "formalization_class": "documented",
            })

        for left, right in itertools.combinations(records, 2):
            solver = Solver()
            solver.add(*constraints)
            solver.add(left["expression"] != right["expression"])
            equivalence_result = solver.check()
            left_implies_right = None
            right_implies_left = None
            for label, first, second in (
                ("left_implies_right", left["expression"], right["expression"]),
                ("right_implies_left", right["expression"], left["expression"]),
            ):
                implication_solver = Solver()
                implication_solver.add(*constraints)
                implication_solver.add(And(first, Not(second)))
                result = implication_solver.check()
                value = "TRUE" if result == unsat else "FALSE" if result == sat else "UNKNOWN"
                if label == "left_implies_right":
                    left_implies_right = value
                else:
                    right_implies_left = value
            if equivalence_result == unsat:
                cross.append({
                    "system": system,
                    "left_id": left["id"],
                    "right_id": right["id"],
                    "property": "equivalence",
                    "result": "TRUE",
                })
            if left_implies_right == "TRUE" or right_implies_left == "TRUE":
                cross.append({
                    "system": system,
                    "left_id": left["id"],
                    "right_id": right["id"],
                    "property": "implication",
                    "left_implies_right": left_implies_right,
                    "right_implies_left": right_implies_left,
                })

            left_actions = {
                action.split(":=", 1)[0].strip(): action.split(":=", 1)[1].strip()
                for action in left["actions"] if ":=" in action
            }
            right_actions = {
                action.split(":=", 1)[0].strip(): action.split(":=", 1)[1].strip()
                for action in right["actions"] if ":=" in action
            }
            for variable in sorted(set(left_actions) & set(right_actions)):
                if left_actions[variable] == right_actions[variable]:
                    continue
                solver = Solver()
                solver.add(*constraints)
                solver.add(And(left["expression"], right["expression"]))
                result = solver.check()
                if result == sat:
                    model = solver.model()
                    items = []
                    for declaration in sorted(model.decls(), key=lambda item: item.name()):
                        items.append(f"{declaration.name()}={model[declaration]}")
                    cross.append({
                        "system": system,
                        "left_id": left["id"],
                        "right_id": right["id"],
                        "property": "action_conflict",
                        "variable": variable,
                        "left_action": left_actions[variable],
                        "right_action": right_actions[variable],
                        "result": "SAT",
                        "model": ", ".join(items),
                    })

    (OUT / "results" / "formal-results.json").write_text(
        json.dumps(all_results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT / "results" / "cross-analysis.json").write_text(
        json.dumps(cross, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    generic_path = REQ / "requisitos.mcdc"
    generic = []
    domains = {
        "alarme_ativo": "bool",
        "porta_aberta": "bool",
        "botao_emergencia": "bool",
        "porta_fechada": "bool",
        "obstaculo": "bool",
        "freio_acionado": "bool",
        "pedal_pressionado": "bool",
    }
    for line in generic_path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        req, guard = (part.strip() for part in line.split(":", 1))
        variables = {name: __import__("z3").Bool(name) for name in domains}
        node = module.ExprParser(guard, set(variables), {}).parse()
        expression = module.compile_node(node, variables, {})
        sat_status, model = status(expression, [])
        generic.append({
            "id": req,
            "requirement": req,
            "system": "generic",
            "source": "experimentacao/experimentacao-1/requirements/experimental/requisitos.mcdc",
            "text": guard,
            "guard": guard,
            "actions": [],
            "satisfiability": sat_status,
            "model": model,
            "formalization_class": "documented",
        })
    all_results.extend(generic)
    (OUT / "results" / "formal-results.json").write_text(
        json.dumps(all_results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps({"formalized": len(all_results), "cross_results": len(cross)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
