import json
import re
import sys
from pathlib import Path

from z3 import Bool, BoolVal, Int, Real, Solver, unsat, sat, unknown

ROOT = Path(__file__).resolve().parents[4]
EXPERIMENT = ROOT / "experimentacao" / "experimentacao-0"
RESULTS = EXPERIMENT / "z3-analysis" / "results"
OUT_JSON = RESULTS / "formal-results.json"


class ExprParser:
    def __init__(self, text, variables, enum_values):
        text = text.replace("/\\", " and ").replace("\\/", " or ")
        self.tokens = re.findall(r"/\\|\\/|!=|==|<=|>=|[()=<>!]|-?\d+(?:\.\d+)?|[A-Za-z_][A-Za-z0-9_]*", text)
        self.pos = 0
        self.variables = variables
        self.enum_values = enum_values

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def take(self):
        value = self.peek()
        self.pos += 1
        return value

    def parse(self):
        result = self.parse_or()
        if self.peek() is not None:
            raise ValueError(f"Token inesperado em posicao {self.pos}: {self.peek()} em {self.tokens}")
        return result

    def parse_or(self):
        left = self.parse_and()
        while self.peek() == "or":
            self.take()
            right = self.parse_and()
            left = ("or", left, right)
        return left

    def parse_and(self):
        left = self.parse_not()
        while self.peek() == "and":
            self.take()
            right = self.parse_not()
            left = ("and", left, right)
        return left

    def parse_not(self):
        if self.peek() in ("!", "not"):
            self.take()
            return ("not", self.parse_not())
        return self.parse_atom()

    def parse_atom(self):
        token = self.peek()
        if token == "(":
            self.take()
            result = self.parse_or()
            if self.take() != ")":
                raise ValueError("Parenteses nao fechados")
            return result

        left = self.take()
        if left in ("true", "false"):
            return ("boollit", left == "true")
        if left not in self.variables:
            raise ValueError(f"Variavel nao declarada: {left}")

        op = self.peek()
        if op in ("=", "==", "!=", "<", "<=", ">", ">=", " "):
            if op == " ":
                self.take()
            op = self.take()
            right = self.take()
            if right is None:
                raise ValueError(f"Operando ausente apos {left} {op}")
            if right in ("true", "false"):
                right_value = right == "true"
            elif re.fullmatch(r"-?\d+", right):
                right_value = int(right)
            elif re.fullmatch(r"-?\d+\.\d+", right):
                right_value = float(right)
            elif right in self.variables:
                right_value = right
            else:
                right_value = right
            return ("compare", left, op, right_value)
        return ("variable", left)


def variable_expr(name, kind):
    if kind == "bool":
        return Bool(name)
    if kind == "int":
        return Int(name)
    if kind == "real":
        return Real(name)
    return Int(name)


def compile_node(node, variable_map, enum_values):
    kind = node[0]
    if kind == "boollit":
        return BoolVal(node[1])
    if kind == "variable":
        value = variable_map[node[1]]
        if enum_values.get(node[1]):
            return value >= 0
        return value
    if kind == "compare":
        left_name, op, right = node[1], node[2], node[3]
        left = variable_map[left_name]
        if isinstance(right, str) and right in variable_map:
            right_expr = variable_map[right]
        elif isinstance(right, str) and right in enum_values.get(left_name, []):
            right_expr = enum_values[left_name].index(right)
        elif isinstance(right, str):
            right_expr = right
        elif isinstance(right, bool):
            right_expr = BoolVal(right)
        else:
            right_expr = right
        if op in ("=", "=="):
            return left == right_expr
        if op == "!=":
            return left != right_expr
        if op == "<":
            return left < right_expr
        if op == "<=":
            return left <= right_expr
        if op == ">":
            return left > right_expr
        if op == ">=":
            return left >= right_expr
        raise ValueError(f"Operador nao suportado: {op}")
    if kind == "not":
        return __import__("z3").Not(compile_node(node[1], variable_map, enum_values))
    if kind == "and":
        return __import__("z3").And(
            compile_node(node[1], variable_map, enum_values),
            compile_node(node[2], variable_map, enum_values),
        )
    if kind == "or":
        return __import__("z3").Or(
            compile_node(node[1], variable_map, enum_values),
            compile_node(node[2], variable_map, enum_values),
        )
    raise ValueError(f"No desconehcido: {kind}")


def leaf_occurrences(node, out=None):
    if out is None:
        out = []
    if node[0] in ("and", "or"):
        leaf_occurrences(node[1], out)
        leaf_occurrences(node[2], out)
    else:
        out.append(node)
    return out


def replace_occurrence(node, index, replacement, current=None):
    if current is None:
        current = [0]
    if node[0] in ("and", "or"):
        left = replace_occurrence(node[1], index, replacement, current)
        right = replace_occurrence(node[2], index, replacement, current)
        return (node[0], left, right)
    if current[0] == index:
        current[0] += 1
        return replacement
    current[0] += 1
    return node


def solve_status(expression, constraints=None):
    solver = Solver()
    if constraints:
        solver.add(*constraints)
    solver.add(expression)
    result = solver.check()
    if result == sat:
        return "SAT", solver.model()
    if result == unsat:
        return "UNSAT", None
    return "UNKNOWN", None


def z3_model_text(model):
    if model is None:
        return ""
    items = []
    for declaration in sorted(model.decls(), key=lambda item: item.name()):
        items.append(f"{declaration.name()}={model[declaration]}")
    return ", ".join(items)


def z3_status(expression):
    solver = Solver()
    solver.add(expression)
    result = solver.check()
    if result == sat:
        return "SAT", z3_model_text(solver.model())
    if result == unsat:
        return "UNSAT", ""
    return "UNKNOWN", ""


def analyze_decision(record, system_inputs):
    guard = record["guard"]
    enum_values = {}
    kinds = {}
    variable_map = {}
    for item in system_inputs:
        name = item["name"]
        kinds[name] = item["type"]
        if item["type"] == "enum":
            enum_values[name] = item["values"]
            values = item["values"]
            variable_map[name] = Int(name)
        elif item["type"] == "bool":
            variable_map[name] = Bool(name)
        elif item["type"] == "int":
            variable_map[name] = Int(name)
        elif item["type"] == "real":
            variable_map[name] = Real(name)

    for name, kind in kinds.items():
        if kind == "bool":
            continue
        if kind == "enum":
            continue

    parser = ExprParser(guard, set(variable_map), enum_values)
    node = parser.parse()
    expression = compile_node(node, variable_map, enum_values)

    constraints = []
    for name, values in enum_values.items():
        constraints.append(variable_map[name] >= 0)
        constraints.append(variable_map[name] < len(values))

    status, model = solve_status(expression, constraints)

    leaves = leaf_occurrences(node)
    redundancy = []
    for index, leaf in enumerate(leaves):
        true_node = replace_occurrence(node, index, ("boollit", True))
        false_node = replace_occurrence(node, index, ("boollit", False))
        true_expr = compile_node(true_node, variable_map, enum_values)
        false_expr = compile_node(false_node, variable_map, enum_values)
        status_equiv, _ = z3_status(__import__("z3").And(*constraints, true_expr != false_expr) if False else (true_expr != false_expr))
        redundant = status_equiv == "UNSAT"
        redundancy.append({"condition": "leaf-" + str(index + 1), "expression": repr_leaf(leaf), "redundant": redundant})

    mcdc_pairs = []
    abstract_vars = [Bool(f"c{index}") for index in range(len(leaves))]
    abstract_map = abstract_vars
    from z3 import And, Or, Not

    def compile_abstract(node, leaves, abstract_vars, index=None):
        if node[0] in ("and", "or"):
            left = compile_abstract(node[1], leaves, abstract_vars)
            right = compile_abstract(node[2], leaves, abstract_vars)
            return And(left, right) if node[0] == "and" else Or(left, right)
        if node[0] in ("not",):
            return Not(compile_abstract(node[1], leaves, abstract_vars))
        raise ValueError("Internal")

    def compile_abstract_node(node, abstract_map, current=None):
        if current is None:
            current = [0]
        kind = node[0]
        if kind in ("and", "or"):
            left = compile_abstract_node(node[1], abstract_map, current)
            right = compile_abstract_node(node[2], abstract_map, current)
            return And(left, right) if kind == "and" else Or(left, right)
        if kind == "not":
            return Not(compile_abstract_node(node[1], abstract_map, current))
        idx = current[0]
        current[0] += 1
        return abstract_map[idx]

    abstract_expression = compile_abstract_node(node, abstract_map)

    for index, leaf in enumerate(leaves):
        s = Solver()
        left_vars = [Bool(f"left_c{i}") for i in range(len(leaves))]
        right_vars = [Bool(f"right_c{i}") for i in range(len(leaves))]
        left_expr = compile_abstract_node(node, left_vars)
        right_expr = compile_abstract_node(node, right_vars)
        s.add(left_vars[index] == True)
        s.add(right_vars[index] == False)
        s.add(left_expr != right_expr)
        for other in range(len(leaves)):
            if other != index:
                s.add(left_vars[other] == right_vars[other])
        positive_result = s.check()
        if positive_result == sat:
            model = s.model()
            pair = {
                "condition": "leaf-" + str(index + 1),
                "expression": repr_leaf(leaf),
                "left_vector": abstract_model_text(model, len(leaves), "left"),
                "right_vector": abstract_model_text(model, len(leaves), "right"),
                "pair_status": "FOUND",
            }
        else:
            pair = {
                "condition": "leaf-" + str(index + 1),
                "expression": repr_leaf(leaf),
                "pair_status": "NOT_FOUND",
            }
        mcdc_pairs.append(pair)

    return {
        "id": record["id"],
        "requirement": record["requirement"],
        "system": record["_system"],
        "text": record["text"],
        "guard": guard,
        "actions": record["actions"],
        "satisfiability": status,
        "model": z3_model_text(model) if status == "SAT" else "",
        "redundancy": redundancy,
        "mcdc_symbolic_pairs": mcdc_pairs,
    }


def abstract_model_text(model, length=None, prefix=None):
    if model is None:
        return ""
    items = []
    for decl in sorted(model.decls(), key=lambda item: item.name()):
        name = decl.name()
        if prefix is not None and not name.startswith(prefix + "_"):
            continue
        items.append(f"{name}={model[decl]}")
    return ", ".join(items)


def repr_leaf(node):
    kind = node[0]
    if kind == "variable":
        return node[1]
    if kind == "boollit":
        return "true" if node[1] else "false"
    if kind == "compare":
        right = str(node[3]).lower() if isinstance(node[3], bool) else str(node[3])
        return f"{node[1]} {node[2]} {right}"
    if kind == "not":
        return f"not ({repr_leaf(node[1])})"
    return str(node)


def add_generic_inventory(results):
    generic_path = ROOT / "exemplos" / "requisitos.mcdc"
    kinds = {"alarme_ativo": "bool", "porta_aberta": "bool", "botao_emergencia": "bool",
             "porta_fechada": "bool", "obstaculo": "bool", "freio_acionado": "bool",
             "pedal_pressionado": "bool"}
    for line in generic_path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        req, guard = (part.strip() for part in line.split(":", 1))
        variable_map = {name: Bool(name) for name in kinds}
        parser = ExprParser(guard, set(variable_map), {})
        node = parser.parse()
        expression = compile_node(node, variable_map, {})
        status, model = z3_status(expression)
        leaves = leaf_occurrences(node)
        record = {
            "id": req,
            "requirement": req,
            "system": "generic",
            "text": guard,
            "guard": guard,
            "actions": [],
            "satisfiability": status,
            "model": model,
            "redundancy": [],
            "mcdc_symbolic_pairs": [],
        }
        for index, leaf in enumerate(leaves):
            record["redundancy"].append({
                "condition": f"leaf-{index + 1}",
                "expression": repr_leaf(leaf),
                "redundant": False,
            })
        results.append(record)


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    results = []
    for filename in ("vm-decisoes.json", "tis-decisoes.json", "npp-decisoes.json"):
        path = ROOT / "exemplos" / filename
        data = json.loads(path.read_text(encoding="utf-8"))
        inputs = data["inputs"]
        for decision in data["decisions"]:
            record = dict(decision)
            record["_system"] = data["system"]
            results.append(analyze_decision(record, inputs))
    add_generic_inventory(results)
    OUT_JSON.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"count": len(results), "output": str(OUT_JSON)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
