import json
from pathlib import Path
import z3

root = Path(__file__).resolve().parent
x = z3.Int("x")
ops = {
    "eq": ("=", x == 3), "ne": ("!=", x != 3),
    "lt": ("<", x < 3), "le": ("<=", x <= 3),
    "gt": (">", x > 3), "ge": (">=", x >= 3),
}
cases, evidence = [], []
for label, (operator, formula) in ops.items():
    expected = {}
    for value in (2, 3, 4):
        queries = []
        statuses = []
        for predicate in (formula, z3.Not(formula)):
            solver = z3.Solver()
            solver.add(x == value, predicate)
            result = solver.check()
            statuses.append(str(result))
            queries.append({"smtlib": solver.to_smt2(), "resultado": str(result),
                            "testemunha": str(solver.model()) if result == z3.sat else None})
        if statuses not in (["sat", "unsat"], ["unsat", "sat"]):
            raise RuntimeError(f"Z3 inconclusivo para {label}/{value}: {statuses}")
        expected[f"T{value}"] = statuses[0] == "sat"
        evidence.append({"id": f"{label}-{value}", "consultas": queries})
    for wrong in (False, True):
        name = f"extension2-{label}-{'divergente' if wrong else 'correto'}.csv"
        lines = ["test,input,value,expected_outcome"]
        for value in (2, 3, 4):
            result = expected[f"T{value}"]
            if wrong and value == 3:
                result = not result
            lines.append(f"T{value},x,{value},{'T' if result else 'F'}")
        (root / name).write_text("\n".join(lines) + "\n", encoding="utf-8")
        cases.append({
            "id": f"E2-{label}-{'divergente' if wrong else 'correto'}",
            "expressao": f"x {operator} 3", "arquivo": name, "codigo_esperado": 2 if wrong else 0,
            "resultados": expected, "regra": "R3,R6,R13: comparação numérica e check de valores concretos",
            "z3": [f"{label}-{value}" for value in (2, 3, 4)],
            "oraculo": "CONFORME À DOCUMENTAÇÃO",
        })
cases.append({
    "id": "E2-fronteira-gt", "tipo": "fronteira", "expressao": "x > 3",
    "esperado": [3, 4], "regra": "R9: comparação > acrescenta valores no limite e imediatamente acima",
    "z3": ["gt-3", "gt-4"], "oraculo": "CONFORME À DOCUMENTAÇÃO",
})
(root / "extension2-oraculos.json").write_text(json.dumps(cases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(root / "extension2-z3.json").write_text(json.dumps({"versao": z3.get_version_string(), "evidencias": evidence},
                                                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
