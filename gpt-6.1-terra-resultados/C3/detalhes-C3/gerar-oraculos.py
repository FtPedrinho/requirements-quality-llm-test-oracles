import itertools
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parent
SPECS = [
    ("T01", "A and B", ["A", "B"], "(and A B)", "D02,D03"),
    ("T02", "A && B", ["A", "B"], "(and A B)", "D02,D03"),
    ("T03", r"A /\ B", ["A", "B"], "(and A B)", "D02,D03"),
    ("T04", "A or B", ["A", "B"], "(or A B)", "D02,D03"),
    ("T05", "A || B", ["A", "B"], "(or A B)", "D02,D03"),
    ("T06", r"A \/ B", ["A", "B"], "(or A B)", "D02,D03"),
    ("T07", "not A", ["A"], "(not A)", "D02,D03"),
    ("T08", "!A", ["A"], "(not A)", "D02,D03"),
    ("T09", "(A and B) or C", ["A", "B", "C"], "(or (and A B) C)", "D02,D03"),
    ("T10", "porta_fechada and not obstaculo", ["porta_fechada", "obstaculo"],
     "(and porta_fechada (not obstaculo))", "D02,D03,D05"),
    ("T11", "(A and B) or (not A and C)", ["A", "B", "C"],
     "(or (and A B) (and (not A) C))", "D02,D03"),
]


def main():
    cases = []
    smt = ["; Restricoes documentais de tabelas-verdade. Uma consulta por vetor.",
           "(set-option :produce-models true)"]
    for case_id, expression, inputs, formula, references in SPECS:
        smt.append(f"; {case_id}: {expression}")
        smt.append("(reset)")
        smt.append("(set-option :produce-models true)")
        for name in inputs:
            smt.append(f"(declare-const {name} Bool)")
        smt.append("(declare-const decisao Bool)")
        smt.append(f"(assert (= decisao {formula}))")
        rows = []
        for values in itertools.product((False, True), repeat=len(inputs)):
            smt.append("(push)")
            assignments = dict(zip(inputs, values))
            for name, value in assignments.items():
                smt.append(f"(assert (= {name} {'true' if value else 'false'}))")
            smt.append("(check-sat)")
            smt.append(f"(get-value ({' '.join(inputs)} decisao))")
            smt.append("(pop)")

            variables = {name: z3.Bool(name) for name in inputs}
            constraints = z3.parse_smt2_string(f"(assert {formula})", decls=variables)
            decision = constraints[0]
            solver = z3.Solver()
            solver.add(*(variables[name] == value for name, value in assignments.items()))
            status = solver.check()
            if status != z3.sat:
                raise RuntimeError(f"{case_id}: erro tecnico Z3 {status}: {assignments}")
            result = solver.model().eval(decision, model_completion=True)
            if not (z3.is_true(result) or z3.is_false(result)):
                raise RuntimeError(f"{case_id}: resultado nao booleano: {result}")
            rows.append({"entradas": assignments, "resultado": z3.is_true(result),
                         "z3": str(status)})
        cases.append({
            "id": case_id, "objetivo": "Tabela-verdade completa da guarda",
            "fonte": "tool-readme-C3.md", "referencias": references,
            "citacoes": [
                "para as entradas distintas da expressão, são consideradas as 2ⁿ combinações e calculado o resultado da guarda em cada uma",
                "| e | `and`, `&&`, `/\\` |",
                "| ou | `or`, `\\|\\|`, `\\/` |",
                "| não | `not`, `!` |",
            ],
            "entrada": {"fonte": "expressao direta", "expressao": expression},
            "precondicoes": "entradas logicas distintas e sem restricoes",
            "formula_smt": formula, "esperado": rows,
            "classificacao": "CONFORME À DOCUMENTAÇÃO",
            "instrucao": "Invocar analyze sem mutacao; examinar tabela da guarda, sem julgar pares ou codigo de saida.",
            "limite": "Sem julgamento de ordem, formatos CSV, pares ou classes de condicao.",
        })
    smt_text = "\n".join(smt) + "\n"
    context = z3.Context()
    result = z3.z3core.Z3_eval_smtlib2_string(context.ref(), smt_text)
    if "error" in result.lower() or "unsat" in result or "unknown" in result:
        raise RuntimeError("Erro tecnico no SMT-LIB: " + result)
    (ROOT / "formulas.smt2").write_text(smt_text, encoding="utf-8")
    (ROOT / "z3-resultados.txt").write_text(
        "Z3 " + z3.get_full_version() + "\n" + result, encoding="utf-8"
    )
    (ROOT / "oraculos.json").write_text(
        json.dumps(cases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"{len(cases)} tabelas; {sum(len(c['esperado']) for c in cases)} vetores; Z3 {z3.get_full_version()}")


if __name__ == "__main__":
    main()
