import json
from pathlib import Path

root = Path(__file__).parent.parent
frozen = json.loads((root / "oraculos" / "casos.json").read_text(encoding="utf-8"))
solver = json.loads((root / "oraculos" / "resultado-z3.json").read_text(encoding="utf-8"))
groups = {}
for case in frozen:
    if case["tipo"] == "truth":
        groups.setdefault(case["expressao"], []).append({
            "id_oraculo": case["id"], "entradas": case["entradas"], "esperado": case["esperado"],
        })

cases = []


def add(**entry):
    entry["id"] = f"X{len(cases) + 1:03}"
    entry["classificacao"] = "CONFORME À DOCUMENTAÇÃO"
    cases.append(entry)


for expression, rows in groups.items():
    for variant in ("masking", "unique"):
        add(
            tipo="avaliacao", expressao=expression, variante=variant, linhas=rows,
            regra="cada resultado de decisão deve corresponder ao oráculo booleano congelado",
            vinculo="Conjunção dos casos de verdade citados; R01, R02 e R12",
        )
    add(
        tipo="truth_csv", expressao=expression, linhas=rows,
        regra="cada combinação deve aparecer com o resultado de decisão congelado",
        vinculo="Conjunção dos casos de verdade citados; R01, R02 e R16",
    )

by_id = {q["id"]: q for q in solver["consultas"]}
for number, expected in ((100, False), (101, True)):
    proof = by_id[f"fronteira-{number}"]
    if proof["status"] != "sat" or proof["testemunha"].get("speed") != str(number):
        raise RuntimeError(f"Testemunha congelada inesperada: {number}")
    add(
        tipo="numeric", expressao="speed > 100", entradas={"speed": str(number)},
        esperado=expected, referencia_smt=f"fronteira-{number}",
        regra="avaliar a comparação para a testemunha de fronteira congelada",
        vinculo="R08 e consulta SMT congelada",
    )

with (Path(__file__).parent / "casos.json").open("x", encoding="utf-8") as file:
    file.write(json.dumps(cases, ensure_ascii=False, indent=2) + "\n")
print("Expressões de verdade reutilizadas:", len(groups))
print("Casos gerados:", len(cases))
