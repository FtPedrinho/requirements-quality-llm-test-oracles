import itertools
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parent
A, B, C = z3.Bools("A B C")
EXPRESSIONS = [
    ("and-word", "A and B", [A, B], z3.And(A, B), []),
    ("and-symbol", "A && B", [A, B], z3.And(A, B), []),
    ("and-dfrs", r"A /\ B", [A, B], z3.And(A, B), []),
    ("or-word", "A or B", [A, B], z3.Or(A, B), []),
    ("or-symbol", "A || B", [A, B], z3.Or(A, B), []),
    ("or-dfrs", r"A \/ B", [A, B], z3.Or(A, B), []),
    ("not-word", "not A", [A], z3.Not(A), []),
    ("not-symbol", "!A", [A], z3.Not(A), []),
    ("nested", "(A and B) or C", [A, B, C], z3.Or(z3.And(A, B), C), []),
    ("unique", "(A and B) or C", [A, B, C], z3.Or(z3.And(A, B), C), ["--unique-cause"]),
    ("repeated", "(A and B) or (not A and C)", [A, B, C],
     z3.Or(z3.And(A, B), z3.And(z3.Not(A), C)), []),
    ("grouping", "A and (B or C)", [A, B, C], z3.And(A, z3.Or(B, C)), []),
    ("tautology", "A or not A", [A], z3.Or(A, z3.Not(A)), []),
]


def main():
    cases = []
    evidence = []
    for label, expr, variables, formula, options in EXPRESSIONS:
        for values in itertools.product((False, True), repeat=len(variables)):
            bindings = [var == value for var, value in zip(variables, values)]
            answers = []
            queries = []
            for predicate in (formula, z3.Not(formula)):
                solver = z3.Solver()
                solver.add(*bindings, predicate)
                result = solver.check()
                answers.append(str(result))
                queries.append({
                    "smtlib": solver.to_smt2(),
                    "resultado": str(result),
                    "testemunha": str(solver.model()) if result == z3.sat else None,
                })
            if answers not in (["sat", "unsat"], ["unsat", "sat"]):
                raise RuntimeError(f"Z3 inconclusivo para {label}: {answers}")
            case_id = f"{label}-" + "".join("1" if v else "0" for v in values)
            cases.append({
                "id": case_id, "tipo": "linha_tabela",
                "expressao": expr, "opcoes": options,
                "entradas": {str(v): value for v, value in zip(variables, values)},
                "esperado": answers[0] == "sat",
                "oraculo": "CONFORME À DOCUMENTAÇÃO",
                "referencias": ["R2", "R3", "R4", "R5", "R7"],
                "evidencia_z3": case_id,
            })
            evidence.append({"id": case_id, "formula": str(formula), "consultas": queries})
    cases.extend([
        {"id": "invalid-expression", "tipo": "codigo_saida", "expressao": "A and",
         "opcoes": [], "entradas": {}, "esperado": 1,
         "oraculo": "CONFORME À DOCUMENTAÇÃO", "referencias": ["R6"],
         "evidencia_z3": "não aplicável: sintaxe"},
        {"id": "tautology-no-pair", "tipo": "codigo_saida", "expressao": "A or not A",
         "opcoes": [], "entradas": {}, "esperado": 2,
         "oraculo": "CONFORME À DOCUMENTAÇÃO", "referencias": ["R2", "R6"],
         "evidencia_z3": "tautology-0 e tautology-1"},
    ])
    (ROOT / "oraculos.json").write_text(json.dumps(cases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "z3-evidencias.json").write_text(
        json.dumps({"versao": z3.get_version_string(), "objetivo": "enumeração exaustiva por expressão",
                    "evidencias": evidence}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(cases)} casos; {len(evidence)} valorações; Z3 {z3.get_version_string()}")


if __name__ == "__main__":
    main()
