import csv
import importlib.util
import json
import sys
from collections import defaultdict
from pathlib import Path

from z3 import (
    And, Bool, BoolVal, Int, Not, Or, Real, Solver, sat, unsat, unknown,
)

ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT = ROOT / "experimentacao" / "experimentacao-1"
BASE = EXPERIMENT / "mutation-testing"
PARSER = ROOT / "experimentacao" / "experimentacao-0" / "z3-analysis" / "scripts" / "analyze_requirements.py"

spec = importlib.util.spec_from_file_location("exp_parser", PARSER)
parser_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser_module)

Mut = parser_module.compile_node
Parse = parser_module.ExprParser


def make_domain(data):
    enum_values = {}
    variables = {}
    constraints = []
    kinds = {}
    for item in data["inputs"]:
        name = item["name"]
        kinds[name] = item["type"]
        if item["type"] == "enum":
            enum_values[name] = item["values"]
            variables[name] = Int(name)
            constraints += [variables[name] >= 0, variables[name] < len(item["values"])]
        elif item["type"] == "bool":
            variables[name] = Bool(name)
        elif item["type"] == "int":
            variables[name] = Int(name)
        elif item["type"] == "real":
            variables[name] = Real(name)
    return enum_values, variables, kinds, constraints


def clone_variable_map(variables, suffix):
    return {
        name: (Int(name + suffix) if isinstance(value, Int(0).__class__) else
               Bool(name + suffix) if isinstance(value, BoolVal(True).__class__) else Real(name + suffix))
        for name, value in variables.items()
    }


def copy_map(variables, kinds, suffix):
    copied = {}
    for name, kind in kinds.items():
        if kind == "enum" or kind == "int":
            copied[name] = Int(name + suffix)
        elif kind == "real":
            copied[name] = Real(name + suffix)
        else:
            copied[name] = Bool(name + suffix)
    return copied


def copy_constraints(copied, enum_values, kinds):
    constraints = []
    for name, kind in kinds.items():
        if kind == "enum":
            constraints += [copied[name] >= 0, copied[name] < len(enum_values[name])]
    return constraints


def z3_status(expression, constraints):
    solver = Solver()
    solver.add(*constraints)
    solver.add(expression)
    result = solver.check()
    if result == sat:
        return "SAT", solver.model()
    if result == unsat:
        return "UNSAT", None
    return "UNKNOWN", None


def model_text(model, enum_values, variables):
    if model is None:
        return ""
    output = {}
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
        output[name] = text
    return json.dumps(output, ensure_ascii=False, sort_keys=True)


def node_text(node):
    kind = node[0]
    if kind == "compare":
        return f"{node[1]} {node[2]} {node[3]}"
    if kind == "boollit":
        return "true" if node[1] else "false"
    if kind == "variable":
        return node[1]
    if kind == "not":
        return f"(not {node_text(node[1])})"
    if kind == "and":
        return f"({node_text(node[1])} and {node_text(node[2])})"
    if kind == "or":
        return f"({node_text(node[1])} or {node_text(node[2])})"
    return str(node)


def leaves(node):
    if node[0] in ("and", "or", "not"):
        if node[0] == "not":
            return [node] + leaves(node[1])
        return leaves(node[1]) + leaves(node[2])
    return [node]


def replace_node(node, target, replacement, counter=None):
    if counter is None:
        counter = [0]
    if counter[0] == target:
        counter[0] += 1
        return replacement
    counter[0] += 1
    kind = node[0]
    if kind in ("and", "or"):
        left = replace_node(node[1], target, replacement, counter)
        right = replace_node(node[2], target, replacement, counter)
        return (kind, left, right)
    if kind == "not":
        return ("not", replace_node(node[1], target, replacement, counter))
    return node


def replace_node_inplace(node, target, replacement, counter=None):
    if counter is None:
        counter = [0]
    if counter[0] == target:
        counter[0] += 1
        return replacement
    counter[0] += 1
    kind = node[0]
    if kind in ("and", "or"):
        left = replace_node_inplace(node[1], target, replacement, counter)
        right = replace_node_inplace(node[2], target, replacement, counter)
        return (kind, left, right)
    if kind == "not":
        return ("not", replace_node_inplace(node[1], target, replacement, counter))
    return node


def walk_nodes(node, start=0):
    nodes = [(start, node)]
    kind = node[0]
    if kind in ("and", "or"):
        left = walk_nodes(node[1], start + 1)
        right_offset = start + 1 + len(left)
        right = walk_nodes(node[2], right_offset)
        nodes += left + right
    elif kind == "not":
        nodes += walk_nodes(node[1], start + 1)
    return nodes


def replace_preorder(node, target, replacement, counter=None):
    if counter is None:
        counter = [0]
    if counter[0] == target:
        counter[0] += 1
        return replacement
    counter[0] += 1
    kind = node[0]
    if kind in ("and", "or"):
        left = replace_preorder(node[1], target, replacement, counter)
        right = replace_preorder(node[2], target, replacement, counter)
        return (kind, left, right)
    if kind == "not":
        return ("not", replace_preorder(node[1], target, replacement, counter))
    return node


def flatten_preorder(node):
    result = [(0, node)]
    if node[0] in ("and", "or"):
        left = flatten_preorder(node[1])
        right = flatten_preorder(node[2])
        offset = len(left)
        result += [(index + 1, item) for index, item in left]
        result += [(index + offset + 1, item) for index, item in right]
    elif node[0] == "not":
        result += [(1, item) for item in flatten_preorder(node[1])]
    return result


def get_preorder(node):
    result = []

    def visit(current):
        index = len(result)
        result.append((index, current))
        if current[0] in ("and", "or"):
            visit(current[1])
            visit(current[2])
        elif current[0] == "not":
            visit(current[1])

    visit(node)
    return result


def replace_at(node, index, replacement):
    counter = [0]

    def visit(current):
        kind = current[0]
        if counter[0] == index:
            counter[0] += 1
            return replacement
        counter[0] += 1
        if kind in ("and", "or"):
            return (kind, visit(current[1]), visit(current[2]))
        if kind == "not":
            return ("not", visit(current[1]))
        return current

    return visit(node)


def generate_mutants(node, operator_id, original_text):
    mutants = []

    def add(replacement, operator, description):
        text = node_text(replacement)
        if text != original_text:
            mutants.append({"operator": operator, "description": description,
                            "expression": text, "node": replacement})

    for index, current in get_preorder(node):
        kind = current[0]
        if kind in ("and", "or"):
            left, right = current[1], current[2]
            if kind == "and":
                add(replace_at(node, index, ("or", left, right)),
                    "AOD", "Substitui AND por OR")
                add(replace_at(node, index, ("boollit", False)),
                    "REM", "Remove a subexpressao AND")
                add(replace_at(node, index, ("not", current)),
                    "NEG-SUB", "Nega a subexpressao AND")
            else:
                add(replace_at(node, index, ("and", left, right)),
                    "AOD", "Substitui OR por AND")
                add(replace_at(node, index, ("boollit", True)),
                    "REM", "Remove a subexpressao OR")
                add(replace_at(node, index, ("not", current)),
                    "NEG-SUB", "Nega a subexpressao OR")

            for side_name, side in (("left", left), ("right", right)):
                add(replace_at(node, index, side),
                    "REM-CONDITION", f"Remove a condicao {side_name} da expressao")

        if kind == "not":
            add(replace_at(node, index, current[1]),
                "REM-NOT", "Remove uma negacao")

        if kind == "compare":
            left, op, right = current[1], current[2], current[3]
            alternatives = {
                "=": ["!="],
                "!=": ["="],
                "<": ["<=", "=", ">="],
                "<=": ["<", "=", "!="],
                ">": [">=", "=", "<="],
                ">=": [">", "=", "!="],
            }
            for new_op in alternatives.get(op, []):
                add(replace_at(node, index, ("compare", left, new_op, right)),
                    "ROP", f"Substitui {op} por {new_op}")
            add(replace_at(node, index, ("boollit", True)),
                "NEG-CONDITION", f"Nega a condicao {node_text(current)}")
            add(replace_at(node, index, ("not", current)),
                "NEG-CONDITION", f"Negacao exclusiva da folha {node_text(current)}")

            if isinstance(right, int) or isinstance(right, float):
                for new_constant in (right - 1, right + 1):
                    add(replace_at(node, index, ("compare", left, op, new_constant)),
                        "CONST", f"Altera o limite {right} para {new_constant}")
                add(replace_at(node, index, ("compare", left, op, -right)),
                    "CONST", f"Inverte o sinal do limite {right}")

    add(("not", node), "NEG-GUARD", "Nega integralmente a guarda")

    unique = {}
    for mutant in mutants:
        unique.setdefault(mutant["expression"], mutant)
    return list(unique.values())


def compile_case(node, variables, enum_values):
    return Mut(node, variables, enum_values)


def model_for_expression(expression, constraints, variables, enum_values):
    status, model = z3_status(expression, constraints)
    if status != "SAT":
        return None
    return model_text(model, enum_values, variables)


def build_concrete_cases(records, constraints, enum_values, variables, kinds):
    cases = []
    for record in records:
        node = record["node"]
        expression = Mut(node, variables, enum_values)
        model = model_for_expression(expression, constraints, variables, enum_values)
        cases.append({
            "case_id": f"TC-{record['id']}-PASS",
            "oracle_id": record["id"],
            "requirement_id": record["requirement"],
            "kind": "PASS",
            "left": model,
            "right": "",
            "expected_left": True,
            "expected_right": "",
            "evaluability": "VALID" if model is not None else "NON-EVALUABLE",
        })

        for pair in record["pairs"]:
            if pair["pair_status"] != "FOUND":
                continue
            target = int(pair["condition"].split("-")[1]) - 1
            leaf_nodes = leaves(node)
            if target >= len(leaf_nodes):
                continue
            left_map = copy_map(variables, kinds, "_left")
            right_map = copy_map(variables, kinds, "_right")
            left_expr = Mut(node, left_map, enum_values)
            right_expr = Mut(node, right_map, enum_values)
            pair_constraints = list(constraints)
            pair_constraints += copy_constraints(left_map, enum_values, kinds)
            pair_constraints += copy_constraints(right_map, enum_values, kinds)
            pair_constraints += [left_expr != right_expr]
            for index, leaf in enumerate(leaf_nodes):
                left_leaf = Mut(leaf, left_map, enum_values)
                right_leaf = Mut(leaf, right_map, enum_values)
                if index == target:
                    pair_constraints += [left_leaf != right_leaf]
                else:
                    pair_constraints += [left_leaf == right_leaf]
            solver = Solver()
            solver.add(*pair_constraints)
            result = solver.check()
            if result == sat:
                model = solver.model()
                left_text = model_text(model, enum_values, left_map)
                right_text = model_text(model, enum_values, right_map)
                cases.append({
                    "case_id": f"TC-{record['id']}-{pair['condition'].replace('leaf-', 'C')}",
                    "oracle_id": record["id"],
                    "requirement_id": record["requirement"],
                    "kind": "MC/DC",
                    "left": left_text,
                    "right": right_text,
                    "expected_left": True,
                    "expected_right": False,
                    "evaluability": "VALID",
                })
            else:
                cases.append({
                    "case_id": f"TC-{record['id']}-{pair['condition'].replace('leaf-', 'C')}",
                    "oracle_id": record["id"],
                    "requirement_id": record["requirement"],
                    "kind": "MC/DC",
                    "left": "",
                    "right": "",
                    "expected_left": True,
                    "expected_right": False,
                    "evaluability": "NON-EVALUABLE",
                })
    return cases


def effective_boolean(node, model_dict, variables, enum_values):
    return None


def eval_json_model(node, model_json, variables, enum_values, kinds):
    assignment = json.loads(model_json)
    local_map = {}
    for name, kind in kinds.items():
        if kind == "enum" or kind == "int":
            local_map[name] = Int(name)
        elif kind == "real":
            local_map[name] = Real(name)
        else:
            local_map[name] = Bool(name)
    solver = Solver()
    for name, kind in kinds.items():
        if name not in assignment:
            continue
        value = assignment[name]
        if kind == "enum":
            solver.add(local_map[name] == enum_values[name].index(value))
        elif kind == "bool":
            solver.add(local_map[name] == (value.lower() == "true"))
        elif kind == "int":
            solver.add(local_map[name] == int(value))
        else:
            solver.add(local_map[name] == RealVal(value))
    expression = Mut(node, local_map, enum_values)
    solver.add(expression)
    return solver.check() == sat


def eval_model(node, model_json, variables, enum_values, kinds):
    assignment = json.loads(model_json)
    local_map = {}
    constraints = []
    for name, kind in kinds.items():
        if kind == "enum" or kind == "int":
            local_map[name] = Int(name)
        elif kind == "real":
            local_map[name] = Real(name)
        else:
            local_map[name] = Bool(name)
        if name not in assignment:
            continue
        value = assignment[name]
        if kind == "enum":
            constraints.append(local_map[name] == enum_values[name].index(value))
        elif kind == "bool":
            constraints.append(local_map[name] == (value.lower() == "true"))
        elif kind == "int":
            constraints.append(local_map[name] == int(value))
        else:
            from z3 import RealVal
            constraints.append(local_map[name] == RealVal(value))
    solver = Solver()
    solver.add(*constraints)
    solver.add(Mut(node, local_map, enum_values))
    return solver.check() == sat


def write_csv(path, fieldnames, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def metrics(tp, tn, fp, fn):
    precision = tp / (tp + fp) if (tp + fp) else None
    recall = tp / (tp + fn) if (tp + fn) else None
    f1 = (2 * precision * recall / (precision + recall)
          if precision is not None and recall is not None and (precision + recall) else None)
    return precision, recall, f1


def main():
    (BASE / "mutants").mkdir(parents=True, exist_ok=True)
    (BASE / "execution").mkdir(parents=True, exist_ok=True)
    (BASE / "metrics").mkdir(parents=True, exist_ok=True)
    (BASE / "analysis").mkdir(parents=True, exist_ok=True)

    records = []
    for filename in ("vm-decisoes.json", "tis-decisoes.json", "npp-decisoes.json"):
        data = json.loads((ROOT / "experimentacao" / "experimentacao-1" / "requirements" / "experimental" / filename).read_text(encoding="utf-8"))
        enum_values, variables, kinds, constraints = make_domain(data)
        for decision in data["decisions"]:
            node = Parse(decision["guard"], set(variables), enum_values).parse()
            formal = next((item for item in json.loads(
                (EXPERIMENT / "formalization" / "results" / "formal-results.json").read_text(
                    encoding="utf-8")).items()),
                          None) if False else None
            pair_data = []
            formal_records = json.loads(
                (EXPERIMENT / "formalization" / "results" / "formal-results.json").read_text(
                    encoding="utf-8"))
            found = next(item for item in formal_records if item["id"] == decision["id"])
            record = {
                "id": decision["id"],
                "requirement": decision["requirement"],
                "system": data["system"],
                "guard": decision["guard"],
                "node": node,
                "pairs": found["mcdc_symbolic_pairs"],
                "variables": variables,
                "enum_values": enum_values,
                "kinds": kinds,
                "constraints": constraints,
            }
            records.append(record)

    cases_by_record = {}
    all_cases = []
    for record in records:
        enum_values = record["enum_values"]
        variables = record["variables"]
        kinds = record["kinds"]
        constraints = record["constraints"]
        cases = build_concrete_cases([record], constraints, enum_values, variables, kinds)
        cases_by_record[record["id"]] = cases
        all_cases += cases

    original_rows = []
    original_tp = original_tn = original_fp = original_fn = 0
    for record in records:
        cases = cases_by_record[record["id"]]
        for case in cases:
            if case["evaluability"] != "VALID":
                status = "NON-EVALUABLE"
                passed = None
                original_rows.append({
                    "case_id": case["case_id"], "oracle_id": case["oracle_id"],
                    "requirement_id": case["requirement_id"], "mutant_id": "ORIGINAL",
                    "case_kind": case["kind"], "passed": "NON-EVALUABLE",
                    "result": "NOT_EVALUABLE", "evidence": "Nenhum modelo concreto encontrado",
                })
                continue
            if case["kind"] == "PASS":
                passed = eval_model(record["node"], case["left"], record["variables"],
                                    record["enum_values"], record["kinds"])
                status = "PASSED" if passed else "FAILED"
                original_tn += int(passed)
                original_fn += int(not passed)
                original_rows.append({
                    "case_id": case["case_id"], "oracle_id": case["oracle_id"],
                    "requirement_id": case["requirement_id"], "mutant_id": "ORIGINAL",
                    "case_kind": "PASS", "passed": str(passed).upper(),
                    "result": "PASSED" if passed else "FALSE_POSITIVE",
                    "evidence": f"modelo={case['left']}; outcome={passed}",
                })
            else:
                left = eval_model(record["node"], case["left"], record["variables"],
                                  record["enum_values"], record["kinds"])
                right = eval_model(record["node"], case["right"], record["variables"],
                                   record["enum_values"], record["kinds"])
                passed = left != right
                status = "PASSED" if passed else "FAILED"
                if passed:
                    original_tn += 1
                else:
                    original_fn += 1
                original_rows.append({
                    "case_id": case["case_id"], "oracle_id": case["oracle_id"],
                    "requirement_id": case["requirement_id"], "mutant_id": "ORIGINAL",
                    "case_kind": "MC/DC", "passed": str(passed).upper(),
                    "result": "PASSED" if passed else "FALSE_POSITIVE",
                    "evidence": f"left={left}; right={right}; pair_difference={left != right}",
                })

    mutants = []
    mutant_rows = []
    for record in records:
        original_text = node_text(record["node"])
        generated = generate_mutants(record["node"], record["id"], original_text)
        original_expr = Mut(record["node"], record["variables"], record["enum_values"])
        for index, generated_mutant in enumerate(generated, 1):
            mutant_node = generated_mutant["node"]
            try:
                mutant_expr = Mut(mutant_node, record["variables"], record["enum_values"])
            except Exception as error:
                mutant_id = f"{record['id']}-M{index:04d}"
                mutants.append({
                    "mutant_id": mutant_id,
                    "requirement_id": record["requirement"],
                    "oracle_id": record["id"],
                    "system": record["system"],
                    "original_expression": record["guard"],
                    "mutant_expression": generated_mutant["expression"],
                    "operator": generated_mutant["operator"],
                    "description": generated_mutant["description"],
                    "relevance": "Mutacao controlada da estrutura ou de um limite da guarda",
                    "satisfiability": "UNKNOWN",
                    "equivalence": "UNKNOWN",
                    "classification": "UNKNOWN",
                    "killed": "NO",
                    "survival": "NOT-EVALUABLE",
                })
                continue
            equivalence_expression = __import__("z3").Xor(original_expr, mutant_expr)
            eq_status, eq_model = z3_status(
                equivalence_expression,
                record["constraints"],
            )
            equivalence = eq_status == "UNSAT"
            classification = ("EQUIVALENT" if equivalence else
                              "UNKNOWN" if eq_status == "UNKNOWN" else "NON-EQUIVALENT")
            mutant_id = f"{record['id']}-M{index:04d}"
            mutants.append({
                "mutant_id": mutant_id,
                "requirement_id": record["requirement"],
                "oracle_id": record["id"],
                "system": record["system"],
                "original_expression": record["guard"],
                "mutant_expression": generated_mutant["expression"],
                "operator": generated_mutant["operator"],
                "description": generated_mutant["description"],
                "relevance": "Mutacao controlada da estrutura ou de um limite da guarda",
                "satisfiability": eq_status,
                "equivalence": "YES" if equivalence else "NO" if eq_status == "SAT" else "UNKNOWN",
                "classification": classification,
            })

            killed = False
            evaluated = False
            for case in cases_by_record[record["id"]]:
                if case["evaluability"] != "VALID":
                    evidence = "Case non-evaluable"
                    passed = None
                    result = "NON-EVALUABLE"
                else:
                    evaluated = True
                    if case["kind"] == "PASS":
                        original_outcome = eval_model(record["node"], case["left"], record["variables"],
                                                      record["enum_values"], record["kinds"])
                        mutant_outcome = eval_model(mutant_node, case["left"], record["variables"],
                                                    record["enum_values"], record["kinds"])
                        passed = original_outcome != mutant_outcome
                        evidence = f"original={original_outcome}; mutant={mutant_outcome}"
                    else:
                        original_left = eval_model(record["node"], case["left"], record["variables"],
                                                   record["enum_values"], record["kinds"])
                        original_right = eval_model(record["node"], case["right"], record["variables"],
                                                    record["enum_values"], record["kinds"])
                        mutant_left = eval_model(mutant_node, case["left"], record["variables"],
                                                 record["enum_values"], record["kinds"])
                        mutant_right = eval_model(mutant_node, case["right"], record["variables"],
                                                  record["enum_values"], record["kinds"])
                        original_pair = original_left != original_right
                        mutant_pair = mutant_left != mutant_right
                        passed = original_pair and (mutant_pair != original_pair)
                        evidence = (f"original=({original_left},{original_right}); "
                                    f"mutant=({mutant_left},{mutant_right}); "
                                    f"pair_original={original_pair}; pair_mutant={mutant_pair}")
                    result = "KILL" if passed else "SURVIVE"
                mutant_rows.append({
                    "mutant_id": mutant_id,
                    "case_id": case["case_id"],
                    "oracle_id": case["oracle_id"],
                    "requirement_id": case["requirement_id"],
                    "expected_result": "original behavior",
                    "observed_result": "difference observed" if passed else "no difference",
                    "passed": str(passed).upper() if passed is not None else "NON-EVALUABLE",
                    "mutant_status": result,
                    "evidence": evidence,
                })
                killed = killed or bool(passed)

            if evaluated:
                mutants[-1]["killed"] = "YES" if killed else "NO"
                mutants[-1]["survival"] = (
                    "KILLED" if killed else
                    "EQUIVALENT" if equivalence else
                    "SURVIVED" if mutant_node is not None and not equivalence else
                    "NOT-EVALUABLE"
                )
            else:
                mutants[-1]["killed"] = "NO"
                mutants[-1]["survival"] = "NOT-EVALUABLE"

    # Preserve result classifications consistently.
    for mutant in mutants:
        if mutant["classification"] == "EQUIVALENT":
            mutant["killed"] = "NO"
        elif mutant["killed"] == "NO" and mutant["classification"] != "UNKNOWN":
            mutant["survival"] = "SURVIVED"

    write_csv(
        BASE / "mutants" / "mutants.json",
        [],
        [],
    ) if False else (BASE / "mutants" / "mutants.json").write_text(
        json.dumps(mutants, ensure_ascii=False, indent=2), encoding="utf-8")

    write_csv(
        BASE / "execution" / "original-execution.csv",
        ["case_id", "oracle_id", "requirement_id", "mutant_id", "case_kind", "passed", "result", "evidence"],
        original_rows,
    )
    write_csv(
        BASE / "execution" / "mutant-execution.csv",
        ["mutant_id", "case_id", "oracle_id", "requirement_id", "expected_result",
         "observed_result", "passed", "mutant_status", "evidence"],
        mutant_rows,
    )

    from collections import Counter
    summary = Counter(mutant["classification"] for mutant in mutants)
    killed = sum(mutant["killed"] == "YES" for mutant in mutants)
    equivalent = sum(mutant["classification"] == "EQUIVALENT" for mutant in mutants)
    survived = sum(mutant["survival"] == "SURVIVED" for mutant in mutants)
    unknown = sum(mutant["classification"] == "UNKNOWN" for mutant in mutants)
    not_eval = sum(mutant["survival"] == "NOT-EVALUABLE" for mutant in mutants)
    non_equivalent = len(mutants) - equivalent
    mutation_score = 100 * killed / (len(mutants) - equivalent) if (len(mutants) - equivalent) else None

    tp = killed
    fn = survived
    fp = sum(mutant["classification"] == "EQUIVALENT" and mutant["killed"] == "YES"
             for mutant in mutants)
    tn = sum(mutant["classification"] == "EQUIVALENT" and mutant["killed"] == "NO"
             for mutant in mutants)
    precision, recall, f1 = metrics(tp, tn, fp, fn)

    summary_rows = [{
        "total": len(mutants), "equivalent": equivalent, "killed": killed,
        "survived": survived, "unknown": unknown, "not_evaluable": not_eval,
        "mutation_score": mutation_score, "precision": precision, "recall": recall,
        "f1": f1, "tp": tp, "tn": tn, "fp": fp, "fn": fn,
    }]
    write_csv(
        BASE / "mutants" / "mutation-summary.csv",
        ["total", "equivalent", "killed", "survived", "unknown", "not_evaluable",
         "mutation_score", "precision", "recall", "f1", "tp", "tn", "fp", "fn"],
        summary_rows,
    )

    # Confusion matrix.
    write_csv(
        BASE / "metrics" / "confusion-matrix.csv",
        ["unit", "predicted_positive", "predicted_negative", "true_positive", "true_negative",
         "false_positive", "false_negative"],
        [{
            "unit": "mutante agregado", "predicted_positive": tp + fp,
            "predicted_negative": tn + fn, "true_positive": tp, "true_negative": tn,
            "false_positive": fp, "false_negative": fn,
        }],
    )

    # Per-oracle and per-requirement metrics.
    def aggregate_group(field):
        grouped = defaultdict(list)
        for mutant in mutants:
            grouped[mutant[field]].append(mutant)
        rows = []
        for key, items in sorted(grouped.items()):
            eq = sum(item["classification"] == "EQUIVALENT" for item in items)
            killed_items = sum(item["killed"] == "YES" for item in items)
            survived_items = sum(item["survival"] == "SURVIVED" for item in items)
            unknown_items = sum(item["classification"] == "UNKNOWN" for item in items)
            not_eval_items = sum(item["survival"] == "NOT-EVALUABLE" for item in items)
            tpp = killed_items
            fnn = survived_items
            fpp = sum(item["classification"] == "EQUIVALENT" and item["killed"] == "YES" for item in items)
            tnn = sum(item["classification"] == "EQUIVALENT" and item["killed"] == "NO" for item in items)
            pp, rr, ff = metrics(tpp, tnn, fpp, fnn)
            ms = (100 * tpp / (len(items) - eq) if len(items) - eq else None)
            rows.append({
                "group": key, "mutants": len(items), "equivalent": eq,
                "killed": killed_items, "survived": survived_items,
                "unknown": unknown_items, "not_evaluable": not_eval_items,
                "mutation_score": ms, "precision": pp, "recall": rr, "f1": ff,
                "tp": tpp, "tn": tnn, "fp": fpp, "fn": fnn,
            })
        return rows

    write_csv(
        BASE / "metrics" / "metrics-by-oracle.csv",
        ["group", "mutants", "equivalent", "killed", "survived", "unknown", "not_evaluable",
         "mutation_score", "precision", "recall", "f1", "tp", "tn", "fp", "fn"],
        aggregate_group("oracle_id"),
    )
    write_csv(
        BASE / "metrics" / "metrics-by-requirement.csv",
        ["group", "mutants", "equivalent", "killed", "survived", "unknown", "not_evaluable",
         "mutation_score", "precision", "recall", "f1", "tp", "tn", "fp", "fn"],
        aggregate_group("requirement_id"),
    )

    (BASE / "execution" / "execution-summary.md").write_text(
        f"""# Resumo da execuÃ§Ã£o

## Modelo original

- Casos PASS/MC/DC: {len(original_rows)}
- ExecuÃ§Ãµes nÃ£o avaliÃ¡veis: {sum(row["passed"] == "NON-EVALUABLE" for row in original_rows)}
- ExecuÃ§Ãµes que passaram: {sum(row["passed"] == "TRUE" for row in original_rows)}
- Falhas ou falsos positivos contra o original: {sum(row["result"] == "FALSE_POSITIVE" for row in original_rows)}

## Mutantes

- Total: {len(mutants)}
- Equivalentes: {equivalent}
- Mortos: {killed}
- Sobreviventes: {survived}
- UNKNOWN: {unknown}
- NÃ£o avaliÃ¡veis: {not_eval}
- Mutation Score: {mutation_score if mutation_score is not None else 'indefinido'}
""", encoding="utf-8")

    print(json.dumps({
        "mutants": len(mutants),
        "equivalent": equivalent,
        "killed": killed,
        "survived": survived,
        "unknown": unknown,
        "not_evaluable": not_eval,
        "mutation_score": mutation_score,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()

