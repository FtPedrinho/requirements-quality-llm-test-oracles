import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT = ROOT / "experimentacao" / "experimentacao-0"
FORMAL = EXPERIMENT / "z3-analysis" / "results" / "formal-results.json"
OUT_MD = EXPERIMENT / "test-suites" / "generated-test-cases.md"
OUT_MCDC = EXPERIMENT / "test-suites" / "mcdc-analysis.md"


def main():
    records = json.loads(FORMAL.read_text(encoding="utf-8"))
    cases = []
    for record in records:
        if record["system"] == "generic":
            continue
        cases.append({
            "id": f"TC-{record['id']}-PASS",
            "requirement": record["requirement"],
            "oracle": record["id"],
            "condition": record["guard"],
            "preconditions": "Conforme a guarda original",
            "inputs": "Valores que satisfazem a guarda",
            "event": "Avaliar a decisão do requisito",
            "expected": "A decisão é verdadeira e as ações explícitas são aplicadas",
            "verifiability": "Teste lógico/simbólico; concretização depende do domínio",
        })
        for pair in record["mcdc_symbolic_pairs"]:
            if pair["pair_status"] != "FOUND":
                continue
            cases.append({
                "id": f"TC-{record['id']}-{pair['condition'].replace('leaf-', 'C')}",
                "requirement": record["requirement"],
                "oracle": record["id"],
                "condition": pair["expression"],
                "preconditions": "Demais condições simbólicas fixadas conforme o par",
                "inputs": f"{pair['left_vector']} | {pair['right_vector']}",
                "event": "Avaliar a decisão com a condição alterada",
                "expected": "O par mantém o vetor independente da condição; o resultado da decisão deve mudar",
                "verifiability": "Par simbólico abstrato; não declarado como vetor concreto executável",
            })

    lines = [
        "# Casos de teste derivados",
        "",
        "Esta suíte contém casos simbólicos derivados dos oráculos e das análises Z3. Não equivale a uma suíte executável sem implementação de domínio.",
        "",
        "| Test Case ID | Requirement ID | Oracle ID | Valores ou condições | Resultado esperado | Verificabilidade |",
        "|---|---|---|---|---|---|",
    ]
    for case in cases:
        inputs = str(case["inputs"]).replace("|", "\\|")
        lines.append(
            f"| {case['id']} | {case['requirement']} | {case['oracle']} | {inputs} | "
            f"{case['expected']} | {case['verifiability']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    mcdc_lines = [
        "# Análise preliminar MC/DC",
        "",
        "A análise abaixo é simbólica sobre folhas/condições das expressões estruturadas. Não demonstra cobertura executável em implementação de domínio.",
        "",
        "| Decisão | Condições | Pares encontrados | Limitação |",
        "|---|---:|---:|---|",
    ]
    for record in records:
        if record["system"] == "generic":
            continue
        found = sum(pair["pair_status"] == "FOUND" for pair in record["mcdc_symbolic_pairs"])
        mcdc_lines.append(
            f"| {record['id']} | {len(record['redundancy'])} | {found} | "
            "Vetores não concretizados; dependências entre variáveis e estado não resolvidas |"
        )
    mcdc_lines.extend([
        "",
        "## Classificação",
        "",
        "- Casos simbólicos: condições e pares abstraídos das expressões.",
        "- Casos concretos documentados: nenhum foi declarado nesta etapa.",
        "- Casos potencialmente executáveis: dependem de implementação ou modelo do domínio.",
        "- Casos não determináveis: requisitos sem formalização segura ou sem domínio.",
        "",
        "Não foi declarada cobertura MC/DC de 100%.",
    ])
    OUT_MCDC.write_text("\n".join(mcdc_lines) + "\n", encoding="utf-8")
    print(json.dumps({"cases": len(cases), "mcdc_decisions": sum(r["system"] != "generic" for r in records)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
