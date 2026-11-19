import csv
import importlib.util
import json
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

from z3 import And, Bool, Int, Not, Or, Real, Solver, Xor, sat, unsat, unknown

ROOT = Path(__file__).resolve().parents[4]
if len(sys.argv) > 1:
    EXPERIMENT_NUMBER = sys.argv[1]
else:
    EXPERIMENT_NUMBER = "0"

EXP = ROOT / "experimentacao" / f"experimentacao-{EXPERIMENT_NUMBER}"
OUT = EXP / "test-suites" / "executable-suite"
PARSER = ROOT / "experimentacao" / "experimentacao-0" / "z3-analysis" / "scripts" / "analyze_requirements.py"

spec = importlib.util.spec_from_file_location("exp_parser", PARSER)
parser_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser_module)

if EXPERIMENT_NUMBER == "0":
    SOURCE_ROOT = ROOT / "exemplos"
else:
    SOURCE_ROOT = EXP / "requirements" / "experimental"

SYSTEM_FILES = ("vm-decisoes.json", "tis-decisoes.json", "npp-decisoes.json")


def load_system(filename):
    data = json.loads((SOURCE_ROOT / filename).read_text(encoding="utf-8"))
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
            variables[name] = Int(name)
            constraints += [variables[name] >= 0, variables[name] < len(item["values"])]
        elif kind == "bool":
            variables[name] = Bool(name)
        elif kind == "int":
            variables[name] = Int(name)
        elif kind == "real":
            variables[name] = Real(name)
    decisions = []
    for decision in data["decisions"]:
        node = parser_module.ExprParser(
            decision["guard"], set(variables), enum_values
        ).parse()
        expression = parser_module.compile_node(node, variables, enum_values)
        decisions.append({
            "id": decision["id"],
            "requirement": decision["requirement"],
            "text": decision.get("text", ""),
            "guard": decision["guard"],
            "actions": decision["actions"],
            "node": node,
            "expression": expression,
        })
    return data, variables, enum_values, kinds, constraints, decisions


def check_status(expression, constraints):
    solver = Solver()
    solver.add(*constraints)
    solver.add(expression)
    result = solver.check()
    if result == sat:
        return "SAT", solver.model()
    if result == unsat:
        return "UNSAT", None
    return "UNKNOWN", None


def model_text(model, variables, enum_values):
    output = {}
    if model is None:
        return json.dumps(output, sort_keys=True)
    for name in sorted(variables):
        value = model.eval(variables[name], model_completion=True)
        text = str(value)
        original_name = name
        if name.endswith("_left"):
            original_name = name[:-5]
        elif name.endswith("_right"):
            original_name = name[:-6]
        if original_name in enum_values:
            try:
                index = int(text)
                if 0 <= index < len(enum_values[original_name]):
                    text = enum_values[original_name][index]
            except ValueError:
                pass
        elif text in ("True", "False"):
            text = text.lower()
        output[original_name] = text
    return json.dumps(output, ensure_ascii=False, sort_keys=True)


def copy_variables(kinds, enum_values, suffix):
    variables = {}
    for name, kind in kinds.items():
        if kind == "enum" or kind == "int":
            variables[name] = Int(name + suffix)
        elif kind == "real":
            variables[name] = Real(name + suffix)
        else:
            variables[name] = Bool(name + suffix)
    return variables


def copy_constraints(variables, kinds, enum_values):
    constraints = []
    for name, kind in kinds.items():
        if kind == "enum":
            constraints += [
                variables[name] >= 0,
                variables[name] < len(enum_values[name]),
            ]
    return constraints


def leaf_nodes(node):
    if node[0] in ("and", "or"):
        return leaf_nodes(node[1]) + leaf_nodes(node[2])
    return [node]


def node_text(node):
    kind = node[0]
    if kind == "boollit":
        return "false" if not node[1] else "true"
    if kind == "variable":
        return node[1]
    if kind == "compare":
        right = node[3]
        if isinstance(right, bool):
            right_text = "true" if right else "false"
        else:
            right_text = str(right)
        return f"{node[1]} {node[2]} {right_text}"
    if kind == "not":
        return f"(not {node_text(node[1])})"
    if kind == "and":
        return f"({node_text(node[1])} /\\ {node_text(node[2])})"
    if kind == "or":
        return f"({node_text(node[1])} \\/ {node_text(node[2])})"
    return str(node)


def get_preorder(node):
    result = []

    def visit(current):
        index = len(result)
        result.append((index, current))
        kind = current[0]
        if kind in ("and", "or"):
            visit(current[1])
            visit(current[2])
        elif kind == "not":
            visit(current[1])

    visit(node)
    return result


def replace_at(node, target, replacement):
    counter = [0]

    def visit(current):
        kind = current[0]
        if counter[0] == target:
            counter[0] += 1
            return replacement
        counter[0] += 1
        if kind in ("and", "or"):
            return (kind, visit(current[1]), visit(current[2]))
        if kind == "not":
            return ("not", visit(current[1]))
        return current

    return visit(node)


def generate_mutants(node):
    original_text = node_text(node)
    mutants = []

    def add(replacement, operator, description):
        text = node_text(replacement)
        if text != original_text:
            mutants.append({
                "operator": operator,
                "description": description,
                "expression": text,
                "node": replacement,
            })

    for index, current in get_preorder(node):
        kind = current[0]
        if kind in ("and", "or"):
            left, right = current[1], current[2]
            if kind == "and":
                add(replace_at(node, index, ("or", left, right)), "AOD", "AND alterado para OR")
                add(replace_at(node, index, ("boollit", False)), "REM", "Subexpressao AND removida")
                add(replace_at(node, index, ("not", current)), "NEG-SUB", "Subexpressao AND negada")
            else:
                add(replace_at(node, index, ("and", left, right)), "AOD", "OR alterado para AND")
                add(replace_at(node, index, ("boollit", True)), "REM", "Subexpressao OR removida")
                add(replace_at(node, index, ("not", current)), "NEG-SUB", "Subexpressao OR negada")
            add(replace_at(node, index, left), "REM-CONDITION", "Condicao esquerda removida")
            add(replace_at(node, index, right), "REM-CONDITION", "Condicao direita removida")
        if kind == "not":
            add(replace_at(node, index, current[1]), "REM-NOT", "Negacao removida")
        if kind == "compare":
            left_name, op, right = current[1], current[2], current[3]
            alternatives = {
                "=": ["!="],
                "!=": ["="],
                "<": ["<=", "=", ">="],
                "<=": ["<", "=", "!="],
                ">": [">=", "=", "<="],
                ">=": [">", "=", "!="],
            }
            for new_op in alternatives.get(op, []):
                add(
                    replace_at(node, index, ("compare", left_name, new_op, right)),
                    "ROP",
                    f"{op} alterado para {new_op}",
                )
            add(
                replace_at(node, index, ("not", current)),
                "NEG-CONDITION",
                "Folha negada",
            )
            if isinstance(right, int) or isinstance(right, float):
                for new_constant in (right - 1, right + 1):
                    add(
                        replace_at(node, index, ("compare", left_name, op, new_constant)),
                        "CONST",
                        f"{right} alterado para {new_constant}",
                    )
                add(
                    replace_at(node, index, ("compare", left_name, op, -right)),
                    "CONST",
                    f"Sinal de {right} alterado",
                )

    add(("not", node), "NEG-GUARD", "Guarda integral negada")
    unique = {}
    for mutant in mutants:
        unique.setdefault(mutant["expression"], mutant)
    return list(unique.values())


def evaluate_model(node, assignment_json, variables, enum_values, kinds):
    assignment = json.loads(assignment_json)
    def get_value(name):
        value = assignment.get(name)
        kind = kinds.get(name)
        if kind == "bool":
            return str(value).lower() == "true"
        if kind == "int":
            return int(value)
        if kind == "real":
            return float(value)
        return value

    def evaluate(current):
        kind = current[0]
        if kind == "boollit":
            return current[1]
        if kind == "variable":
            return get_value(current[1])
        if kind == "compare":
            left_name, op, right = current[1], current[2], current[3]
            left = get_value(left_name)
            if isinstance(right, str) and right in assignment:
                right_value = get_value(right)
            elif isinstance(right, str) and right in enum_values.get(left_name, []):
                right_value = right
            elif isinstance(right, bool):
                right_value = right
            elif isinstance(right, (float, int)):
                right_value = right
            else:
                right_value = right
            if op in ("=", "=="):
                return left == right_value
            if op == "!=":
                return left != right_value
            if op == "<":
                return left < right_value
            if op == "<=":
                return left <= right_value
            if op == ">":
                return left > right_value
            if op == ">=":
                return left >= right_value
            raise ValueError(f"Unsupported operator: {op}")
        if kind == "not":
            return not evaluate(current[1])
        if kind == "and":
            return evaluate(current[1]) and evaluate(current[2])
        if kind == "or":
            return evaluate(current[1]) or evaluate(current[2])
        raise ValueError(f"Unknown AST kind: {kind}")

    return evaluate(node)


def generate_concrete_cases(data, variables, enum_values, kinds, constraints, decisions):
    cases = []
    for decision in decisions:
        id_value = decision["id"]
        status, model = check_status(decision["expression"], constraints)
        if status == "SAT":
            pass_assignment = model_text(model, variables, enum_values)
            cases.append({
                "case_id": f"E{EXPERIMENT_NUMBER}-TC-{id_value}-PASS",
                "experiment": f"EXP{EXPERIMENT_NUMBER}",
                "system": data["system"],
                "oracle_id": id_value,
                "requirement_id": decision["requirement"],
                "decision_id": id_value,
                "kind": "PASS",
                "left": pass_assignment,
                "right": "",
                "evaluability": "VALID",
            })
        else:
            cases.append({
                "case_id": f"E{EXPERIMENT_NUMBER}-TC-{id_value}-PASS",
                "experiment": f"EXP{EXPERIMENT_NUMBER}",
                "system": data["system"],
                "oracle_id": id_value,
                "requirement_id": decision["requirement"],
                "decision_id": id_value,
                "kind": "PASS",
                "left": "",
                "right": "",
                "evaluability": "NON-EVALUABLE",
            })

        negative_status, negative_model = check_status(
            Not(decision["expression"]), constraints
        )
        if negative_status == "SAT":
            negative_assignment = model_text(negative_model, variables, enum_values)
            cases.append({
                "case_id": f"E{EXPERIMENT_NUMBER}-TC-{id_value}-NEG",
                "experiment": f"EXP{EXPERIMENT_NUMBER}",
                "system": data["system"],
                "oracle_id": id_value,
                "requirement_id": decision["requirement"],
                "decision_id": id_value,
                "kind": "NEGATIVE",
                "left": negative_assignment,
                "right": "",
                "evaluability": "VALID",
            })
        else:
            cases.append({
                "case_id": f"E{EXPERIMENT_NUMBER}-TC-{id_value}-NEG",
                "experiment": f"EXP{EXPERIMENT_NUMBER}",
                "system": data["system"],
                "oracle_id": id_value,
                "requirement_id": decision["requirement"],
                "decision_id": id_value,
                "kind": "NEGATIVE",
                "left": "",
                "right": "",
                "evaluability": "NON-EVALUABLE",
            })

        leaves = leaf_nodes(decision["node"])
        for leaf_index, leaf in enumerate(leaves, 1):
            left_vars = copy_variables(kinds, enum_values, "_left")
            right_vars = copy_variables(kinds, enum_values, "_right")
            pair_constraints = copy_constraints(left_vars, kinds, enum_values)
            pair_constraints += copy_constraints(right_vars, kinds, enum_values)
            left_expression = parser_module.compile_node(
                decision["node"], left_vars, enum_values
            )
            right_expression = parser_module.compile_node(
                decision["node"], right_vars, enum_values
            )
            pair_constraints += [left_expression != right_expression]
            for index, current_leaf in enumerate(leaves):
                left_leaf = parser_module.compile_node(
                    current_leaf, left_vars, enum_values
                )
                right_leaf = parser_module.compile_node(
                    current_leaf, right_vars, enum_values
                )
                if index == leaf_index - 1:
                    pair_constraints += [left_leaf != right_leaf]
                else:
                    pair_constraints += [left_leaf == right_leaf]
            solver = Solver()
            solver.add(*pair_constraints)
            result = solver.check()
            if result == sat:
                model = solver.model()
                left_assignment = model_text(model, left_vars, enum_values)
                right_assignment = model_text(model, right_vars, enum_values)
                cases.append({
                    "case_id": f"E{EXPERIMENT_NUMBER}-TC-{id_value}-C{leaf_index}",
                    "experiment": f"EXP{EXPERIMENT_NUMBER}",
                    "system": data["system"],
                    "oracle_id": id_value,
                    "requirement_id": decision["requirement"],
                    "decision_id": id_value,
                    "kind": "MC/DC",
                    "left": left_assignment,
                    "right": right_assignment,
                    "evaluability": "VALID",
                })
            else:
                cases.append({
                    "case_id": f"E{EXPERIMENT_NUMBER}-TC-{id_value}-C{leaf_index}",
                    "experiment": f"EXP{EXPERIMENT_NUMBER}",
                    "system": data["system"],
                    "oracle_id": id_value,
                    "requirement_id": decision["requirement"],
                    "decision_id": id_value,
                    "kind": "MC/DC",
                    "left": "",
                    "right": "",
                    "evaluability": "NON-EVALUABLE",
                })
    return cases


def write_csv(path, fieldnames, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def normalize_mutant_expression(expression):
    text = expression
    text = text.replace("= True", "= true").replace("= False", "= false")
    text = text.replace("and ", "/\\ ").replace(" or ", " \\/ ")
    text = text.replace("(not ", "(not ")
    return text


def load_existing_mutants():
    inventory_path = EXP / "mutation-testing" / "mutants" / "mutants.json"
    if not inventory_path.exists():
        return []
    try:
        return json.loads(inventory_path.read_text(encoding="utf-8"))
    except Exception:
        return []


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    mutation_copies = OUT / "mutation-copies"
    mutation_copies.mkdir(parents=True, exist_ok=True)
    suite_results = OUT / "suite-results"
    suite_results.mkdir(parents=True, exist_ok=True)

    all_cases = []
    systems = {}
    mutants = []
    existing_mutants = load_existing_mutants()
    mutants_by_decision = defaultdict(list)
    for mutant in existing_mutants:
        mutants_by_decision[mutant["oracle_id"]].append(mutant)

    for filename in SYSTEM_FILES:
        data, variables, enum_values, kinds, constraints, decisions = load_system(filename)
        systems[data["system"]] = {
            "data": data,
            "variables": variables,
            "enum_values": enum_values,
            "kinds": kinds,
            "constraints": constraints,
            "decisions": decisions,
        }
        all_cases += generate_concrete_cases(
            data, variables, enum_values, kinds, constraints, decisions
        )

        for decision in decisions:
            original_expression = decision["expression"]
            generated = mutants_by_decision.get(decision["id"])
            if not generated:
                generated = []
                for index, fallback_mutant in enumerate(generate_mutants(decision["node"]), 1):
                    generated.append({
                        "mutant_id": f"{decision['id']}-M{index:04d}",
                        "operator": fallback_mutant["operator"],
                        "description": fallback_mutant["description"],
                        "mutant_expression": fallback_mutant["expression"],
                        "node": fallback_mutant["node"],
                    })
            for mutant in generated:
                mutant_id = mutant.get("mutant_id", f"{decision['id']}-M0001")
                if "mutant_expression" in mutant:
                    mutant_guard = mutant["mutant_expression"]
                else:
                    mutant_guard = mutant.get("expression", mutant.get("mutant_expression", ""))
                if "node" in mutant:
                    mutated_node = mutant["node"]
                else:
                    normalized_guard = normalize_mutant_expression(mutant_guard)
                    try:
                        mutated_node = parser_module.ExprParser(
                            normalized_guard, set(variables), enum_values
                        ).parse()
                    except Exception:
                        classification = "UNKNOWN"
                        mutants.append({
                            "mutant_id": mutant_id,
                            "decision_id": decision["id"],
                            "requirement_id": decision["requirement"],
                            "system": data["system"],
                            "operator": mutant.get("operator", "UNKNOWN"),
                            "description": mutant.get("description", "Mutante nao reprocessado"),
                            "original_guard": decision["guard"],
                            "mutant_guard": mutant_guard,
                            "classification": classification,
                            "equivalence": "UNKNOWN",
                        })
                        continue
                mutant_data = json.loads(json.dumps(data))
                for candidate in mutant_data["decisions"]:
                    if candidate["id"] == decision["id"]:
                        candidate["guard"] = normalized_guard if "node" not in mutant else node_text(mutated_node)
                        candidate["mutation"] = {
                            "mutant_id": mutant_id,
                            "operator": mutant.get("operator", "UNKNOWN"),
                            "description": mutant.get("description", "Mutante existente"),
                        }
                        break
                copy_path = mutation_copies / f"{mutant_id}.json"
                copy_path.write_text(
                    json.dumps(mutant_data, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )

                mutated_variables = dict(variables)
                try:
                    mutated_expression = parser_module.compile_node(
                        mutated_node, variables, enum_values
                    )
                except Exception:
                    classification = "UNKNOWN"
                    equivalence = "UNKNOWN"
                else:
                    xor_solver = Solver()
                    xor_solver.add(*constraints)
                    xor_solver.add(Xor(original_expression, mutated_expression))
                    xor_result = xor_solver.check()
                    if xor_result == unsat:
                        classification = "EQUIVALENT"
                        equivalence = "YES"
                    elif xor_result == sat:
                        classification = "NON-EQUIVALENT"
                        equivalence = "NO"
                    else:
                        classification = "UNKNOWN"
                        equivalence = "UNKNOWN"
                mutants.append({
                    "mutant_id": mutant_id,
                    "decision_id": decision["id"],
                    "requirement_id": decision["requirement"],
                    "system": data["system"],
                    "operator": mutant["operator"],
                    "description": mutant["description"],
                    "original_guard": decision["guard"],
                    "mutant_guard": mutant_guard,
                    "classification": classification,
                    "equivalence": equivalence,
                })

    write_csv(
        OUT / "executable-cases.csv",
        [
            "case_id", "experiment", "system", "oracle_id", "requirement_id",
            "decision_id", "kind", "left", "right", "evaluability",
        ],
        all_cases,
    )
    (OUT / "mutant-inventory.json").write_text(
        json.dumps(mutants, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    original_failures = []
    original_passes = 0
    original_non_evaluable = 0
    execution_rows = []

    for system_name, system in systems.items():
        data = system["data"]
        variables = system["variables"]
        enum_values = system["enum_values"]
        kinds = system["kinds"]
        constraints = system["constraints"]
        decision_map = {item["id"]: item for item in system["decisions"]}
        system_cases = [case for case in all_cases if case["system"] == system_name]
        for case in system_cases:
            if case["evaluability"] != "VALID":
                original_non_evaluable += 1
                original_failures.append({
                    "case_id": case["case_id"],
                    "status": "NON-EVALUABLE",
                    "reason": "No concrete Z3 model for the case",
                })
                continue
            decision = decision_map[case["decision_id"]]
            if case["kind"] == "NEGATIVE":
                passed = not evaluate_model(
                    decision["node"], case["left"], variables, enum_values, kinds
                )
            elif case["kind"] == "PASS":
                passed = evaluate_model(
                    decision["node"], case["left"], variables, enum_values, kinds
                )
            else:
                left = evaluate_model(
                    decision["node"], case["left"], variables, enum_values, kinds
                )
                right = evaluate_model(
                    decision["node"], case["right"], variables, enum_values, kinds
                )
                passed = left != right
            if passed:
                original_passes += 1
            else:
                original_failures.append({
                    "case_id": case["case_id"],
                    "status": "FAILED",
                    "reason": "Original specification did not satisfy the oracle",
                })
            execution_rows.append({
                "case_id": case["case_id"],
                "decision_id": case["decision_id"],
                "system": case["system"],
                "mutant_id": "ORIGINAL",
                "kind": case["kind"],
                "passed": str(passed).upper(),
                "status": "PASSED" if passed else "FAILED",
                "left": case["left"],
                "right": case["right"],
            })

    mutant_execution = []
    killed_mutants = set()
    survived_mutants = set()

    for mutant in mutants:
        if mutant["classification"] in ("EQUIVALENT", "UNKNOWN"):
            continue
        copy_path = mutation_copies / f"{mutant['mutant_id']}.json"
        mutant_data = json.loads(copy_path.read_text(encoding="utf-8"))
        enum_values = {}
        variables = {}
        kinds = {}
        constraints = []
        for item in mutant_data["inputs"]:
            name = item["name"]
            kind = item["type"]
            kinds[name] = kind
            if kind == "enum":
                enum_values[name] = item["values"]
                variables[name] = Int(name)
                constraints += [variables[name] >= 0, variables[name] < len(item["values"])]
            elif kind == "bool":
                variables[name] = Bool(name)
            elif kind == "int":
                variables[name] = Int(name)
            elif kind == "real":
                variables[name] = Real(name)

        mutant_decision = next(
            item for item in mutant_data["decisions"]
            if item["id"] == mutant["decision_id"]
        )
        try:
            mutant_node = parser_module.ExprParser(
                mutant_decision["guard"], set(variables), enum_values
            ).parse()
        except Exception:
            continue

        original_node = next(
            decision["node"]
            for system in systems.values()
            for decision in system["decisions"]
            if decision["id"] == mutant["decision_id"]
        )
        original_variables = next(
            system["variables"]
            for system in systems.values()
            if any(decision["id"] == mutant["decision_id"] for decision in system["decisions"])
        )
        original_kinds = next(
            system["kinds"]
            for system in systems.values()
            if any(decision["id"] == mutant["decision_id"] for decision in system["decisions"])
        )
        original_enum = next(
            system["enum_values"]
            for system in systems.values()
            if any(decision["id"] == mutant["decision_id"] for decision in system["decisions"])
        )

        killed = False
        evaluated = False
        for case in all_cases:
            if case["decision_id"] != mutant["decision_id"] or case["evaluability"] != "VALID":
                continue
            evaluated = True
            if case["kind"] == "PASS":
                original_outcome = evaluate_model(
                    original_node, case["left"], original_variables,
                    original_enum, original_kinds
                )
                mutant_outcome = evaluate_model(
                    mutant_node, case["left"], variables, enum_values, kinds
                )
                difference = original_outcome != mutant_outcome
            elif case["kind"] == "NEGATIVE":
                original_outcome = evaluate_model(
                    original_node, case["left"], original_variables,
                    original_enum, original_kinds
                )
                mutant_outcome = evaluate_model(
                    mutant_node, case["left"], variables, enum_values, kinds
                )
                difference = original_outcome != mutant_outcome
            else:
                original_left = evaluate_model(
                    original_node, case["left"], original_variables,
                    original_enum, original_kinds
                )
                original_right = evaluate_model(
                    original_node, case["right"], original_variables,
                    original_enum, original_kinds
                )
                mutant_left = evaluate_model(
                    mutant_node, case["left"], variables, enum_values, kinds
                )
                mutant_right = evaluate_model(
                    mutant_node, case["right"], variables, enum_values, kinds
                )
                difference = (
                    (original_left != original_right) !=
                    (mutant_left != mutant_right)
                )
            if difference:
                killed = True
            mutant_execution.append({
                "mutant_id": mutant["mutant_id"],
                "case_id": case["case_id"],
                "decision_id": mutant["decision_id"],
                "system": mutant["system"],
                "classification": mutant["classification"],
                "difference": str(difference).upper(),
                "status": "KILL" if difference else "SURVIVE",
            })
        if evaluated:
            if killed:
                killed_mutants.add(mutant["mutant_id"])
            else:
                survived_mutants.add(mutant["mutant_id"])

    for mutant in mutants:
        if mutant["mutant_id"] in killed_mutants:
            mutant["killed"] = "YES"
            mutant["survival"] = "KILLED"
        elif mutant["mutant_id"] in survived_mutants:
            mutant["killed"] = "NO"
            mutant["survival"] = "SURVIVED"
        elif mutant["classification"] == "EQUIVALENT":
            mutant["killed"] = "NO"
            mutant["survival"] = "EQUIVALENT"
        elif mutant["classification"] == "UNKNOWN":
            mutant["killed"] = "NO"
            mutant["survival"] = "NOT-EVALUABLE"
        else:
            mutant["killed"] = "NO"
            mutant["survival"] = "NOT-EVALUABLE"

    write_csv(
        suite_results / "original-execution.csv",
        [
            "case_id", "decision_id", "system", "mutant_id", "kind",
            "passed", "status", "left", "right",
        ],
        execution_rows,
    )
    write_csv(
        suite_results / "mutant-execution.csv",
        [
            "mutant_id", "case_id", "decision_id", "system",
            "classification", "difference", "status",
        ],
        mutant_execution,
    )
    write_csv(
        OUT / "executable-cases.csv",
        [
            "case_id", "experiment", "system", "oracle_id", "requirement_id",
            "decision_id", "kind", "left", "right", "evaluability",
        ],
        all_cases,
    )
    (OUT / "mutant-inventory.json").write_text(
        json.dumps(mutants, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    equivalent = sum(item["classification"] == "EQUIVALENT" for item in mutants)
    unknown = sum(item["classification"] == "UNKNOWN" for item in mutants)
    killed = len(killed_mutants)
    survived = len(survived_mutants)
    not_evaluable = len(mutants) - equivalent - unknown - killed - survived
    ms_reported = 100 * killed / (len(mutants) - equivalent) if len(mutants) - equivalent else None
    ms_corrected = 100 * killed / (len(mutants) - equivalent - unknown) if len(mutants) - equivalent - unknown else None
    precision = killed / killed if killed else None
    recall = killed / (killed + survived) if (killed + survived) else None
    f1 = (2 * precision * recall / (precision + recall)
          if precision is not None and recall is not None and (precision + recall)
          else None)

    summary = {
        "experiment": f"EXP{EXPERIMENT_NUMBER}",
        "condition": "original" if EXPERIMENT_NUMBER == "0" else "C1",
        "total_mutants": len(mutants),
        "equivalent": equivalent,
        "unknown": unknown,
        "killed": killed,
        "survived": survived,
        "not_evaluable": not_evaluable,
        "mutation_score_reported": ms_reported,
        "mutation_score_corrected": ms_corrected,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "cases": len(all_cases),
        "valid_cases": sum(case["evaluability"] == "VALID" for case in all_cases),
        "non_evaluable_cases": sum(case["evaluability"] == "NON-EVALUABLE" for case in all_cases),
        "original_passes": original_passes,
        "original_failures": sum(row["status"] == "FAILED" for row in execution_rows),
        "original_non_evaluable": sum(case["evaluability"] == "NON-EVALUABLE" for case in all_cases),
    }
    (suite_results / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
