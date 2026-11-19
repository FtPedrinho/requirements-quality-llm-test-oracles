import importlib.util
import json
from pathlib import Path

from z3 import Solver, sat, unsat, unknown

ROOT = Path(__file__).resolve().parents[3]
EXP = ROOT / "experimentacao" / "experimentacao-1"
DIAG = EXP / "diagnostics"
PARSER = ROOT / "experimentacao" / "experimentacao-0" / "z3-analysis" / "scripts" / "analyze_requirements.py"

spec = importlib.util.spec_from_file_location("exp0_parser", PARSER)
parser_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser_module)


def load_decisions(filename):
    path = EXP / "requirements" / "experimental" / filename
    data = json.loads(path.read_text(encoding="utf-8"))
    enum_values = {}
    variables = {}
    constraints = []
    kinds = {}
    for item in data["inputs"]:
        name = item["name"]
        kinds[name] = item["type"]
        if item["type"] == "enum":
            enum_values[name] = item["values"]
            variables[name] = __import__("z3").Int(name)
            constraints += [variables[name] >= 0, variables[name] < len(item["values"])]
        elif item["type"] == "bool":
            variables[name] = __import__("z3").Bool(name)
        elif item["type"] == "int":
            variables[name] = __import__("z3").Int(name)
        elif item["type"] == "real":
            variables[name] = __import__("z3").Real(name)
    decisions = {item["requirement"]: item for item in data["decisions"]}
    return data, enum_values, variables, kinds, constraints, decisions


def compile_decision(decision, variables, enum_values):
    node = parser_module.ExprParser(
        decision["guard"], set(variables), enum_values
    ).parse()
    return parser_module.compile_node(node, variables, enum_values)


def model_text(model, variables, enum_values):
    result = {}
    for name in sorted(variables):
        value = model.eval(variables[name], model_completion=True)
        text = str(value)
        if name in enum_values:
            try:
                index = int(text)
                if 0 <= index < len(enum_values[name]):
                    text = enum_values[name][index]
            except ValueError:
                pass
        result[name] = text
    return json.dumps(result, ensure_ascii=False, sort_keys=True)


def action_map(decision):
    result = {}
    for action in decision["actions"]:
        if ":=" in action:
            variable, value = action.split(":=", 1)
            result[variable.strip()] = value.strip()
    return result


def analyze_pair(left, right, variables, enum_values, constraints):
    left_expr = compile_decision(left, variables, enum_values)
    right_expr = compile_decision(right, variables, enum_values)
    solver = Solver()
    solver.add(*constraints)
    solver.add(left_expr)
    solver.add(right_expr)
    result = solver.check()
    status = "SAT" if result == sat else "UNSAT" if result == unsat else "UNKNOWN"
    model = solver.model() if result == sat else None
    left_actions = action_map(left)
    right_actions = action_map(right)
    conflicts = sorted(
        set(left_actions) & set(right_actions)
        for _ in [0]
    )[0]
    action_conflicts = [
        {
            "variable": variable,
            "left": left_actions[variable],
            "right": right_actions[variable],
        }
        for variable in conflicts
        if left_actions[variable] != right_actions[variable]
    ]
    return {
        "status": status,
        "model": model_text(model, variables, enum_values) if model is not None else "",
        "action_conflicts": action_conflicts,
    }


def write_csv(path, fieldnames, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        import csv
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    DIAG.mkdir(parents=True, exist_ok=True)

    tis_data, tis_enum, tis_vars, tis_kinds, tis_constraints, tis_decisions = load_decisions(
        "tis-decisoes.json"
    )
    tis_rows = []
    for left_id in ("REQ002", "REQ003", "REQ004"):
        pair = analyze_pair(
            tis_decisions[left_id],
            tis_decisions["REQ006"],
            tis_vars,
            tis_enum,
            tis_constraints,
        )
        left = tis_decisions[left_id]
        right = tis_decisions["REQ006"]
        tis_rows.append({
            "pair": f"{left_id} x REQ006",
            "left_requirement": left_id,
            "right_requirement": "REQ006",
            "left_guard": left["guard"],
            "right_guard": right["guard"],
            "left_actions": "; ".join(left["actions"]),
            "right_actions": "; ".join(right["actions"]),
            "z3_status": pair["status"],
            "counterexample": pair["model"],
            "variable_conflicts": json.dumps(pair["action_conflicts"], ensure_ascii=False),
            "documentary_priority": "Nenhuma prioridade encontrada nos JSON TIS experimentais/originais",
            "classification": (
                "Conflito potencial dependente de informação ausente"
                if pair["status"] == "SAT"
                else "Não avaliável"
            ),
            "needed_information": "Confirmação de processamento simultâneo e de prioridade temporal entre os modos de pisca e REQ006",
        })

    write_csv(
        DIAG / "tis-conflicts.csv",
        [
            "pair", "left_requirement", "right_requirement", "left_guard",
            "right_guard", "left_actions", "right_actions", "z3_status",
            "counterexample", "variable_conflicts", "documentary_priority",
            "classification", "needed_information",
        ],
        tis_rows,
    )

    npp_data, npp_enum, npp_vars, npp_kinds, npp_constraints, npp_decisions = load_decisions(
        "npp-decisoes.json"
    )
    npp_pair = analyze_pair(
        npp_decisions["REQ005"],
        npp_decisions["REQ008"],
        npp_vars,
        npp_enum,
        npp_constraints,
    )
    npp_rows = [{
        "pair": "REQ005 x REQ008",
        "left_requirement": "REQ005",
        "right_requirement": "REQ008",
        "left_guard": npp_decisions["REQ005"]["guard"],
        "right_guard": npp_decisions["REQ008"]["guard"],
        "left_actions": "; ".join(npp_decisions["REQ005"]["actions"]),
        "right_actions": "; ".join(npp_decisions["REQ008"]["actions"]),
        "z3_status": npp_pair["status"],
        "counterexample": npp_pair["model"],
        "variable_conflicts": json.dumps(npp_pair["action_conflicts"], ensure_ascii=False),
        "documentary_priority": "Nenhuma prioridade ou precedência encontrada nos JSON NPP experimentais/originais",
        "classification": (
            "Conflito potencial dependente de informação ausente"
            if npp_pair["status"] == "SAT"
            else "Não avaliável"
        ),
        "needed_information": "Confirmação de simultaneidade das transições de blockage e pressure mode e da precedência das ações",
    }]
    write_csv(
        DIAG / "npp-conflicts.csv",
        [
            "pair", "left_requirement", "right_requirement", "left_guard",
            "right_guard", "left_actions", "right_actions", "z3_status",
            "counterexample", "variable_conflicts", "documentary_priority",
            "classification", "needed_information",
        ],
        npp_rows,
    )

    print(json.dumps({
        "tis": tis_rows,
        "npp": npp_rows,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
