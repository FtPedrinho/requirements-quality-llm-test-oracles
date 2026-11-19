import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXP = ROOT / "experimentacao" / "experimentacao-2"
C2 = EXP / "documentation" / "tool-readme-C2.md"
INVENTORY = ROOT / "research" / "experimentacao" / "behavior-inventory.csv"
OUT = EXP / "oracles"

PROPERTIES = {
    "B004": ("Ambiguo", "Sem comando, a CLI pode apresentar instruções, mas o texto não garante o resultado."),
    "B005": ("Ambiguo", "O texto indica uma única fonte, mas não especifica exatamente a validação de fontes combinadas."),
    "B006": ("Determinado", "Opção não reconhecida resulta em erro."),
    "B007": ("Ambiguo", "Os operadores são listados, mas a precedência não é descrita."),
    "B008": ("Ambiguo", "Os operadores são listados, mas a precedência não é descrita."),
    "B009": ("Ambiguo", "NOT é listado sem explicar precedência ou expressões complexas."),
    "B010": ("Determinado", "Comparações incluem igualdade, diferença, menor e maior."),
    "B011": ("Ambiguo", "Expressões inválidas são mencionadas, mas a resposta exata não é definida."),
    "B012": ("Determinado", "Um arquivo .mcdc contém linha com identificação e expressão."),
    "B013": ("Indeterminado", "O comportamento de arquivo vazio não é definido."),
    "B014": ("Ambiguo", "JSON contém sistema, entradas e decisões, mas o esquema completo não é definido."),
    "B015": ("Indeterminado", "O texto não diz o que ocorre com JSON sem decisões."),
    "B016": ("Indeterminado", "O conteúdo do CSV de testes não é descrito."),
    "B017": ("Indeterminado", "O tratamento de cabeçalho inválido não é especificado."),
    "B018": ("Determinado", "A tabela é limitada a 20 entradas."),
    "B019": ("Indeterminado", "O texto não menciona entradas repetidas."),
    "B020": ("Determinado", "Mascaramento é o modo inicial por padrão."),
    "B021": ("Determinado", "Causa única existe e pode ser escolhida."),
    "B022": ("Ambiguo", "Z3 pode indicar combinação impossível, mas a marcação no resultado não é detalhada."),
    "B023": ("Ambiguo", "Uma seleção pode ser feita, mas o algoritmo guloso não é descrito."),
    "B024": ("Ambiguo", "A busca exata é mencionada, mas não o critério operacional completo."),
    "B025": ("Ambiguo", "O modo direto é limitado a 30 entradas, mas o formato da saída não é claro."),
    "B026": ("Ambiguo", "Fronteiras podem ser consideradas, mas os casos exatos não são descritos."),
    "B027": ("Ambiguo", "Mutação interna é mencionada apenas implicitamente."),
    "B028": ("Determinado", "Valores diferentes na mesma variável podem representar conflito."),
    "B029": ("Determinado", "Nenhuma decisão aplicável pode representar lacuna."),
    "B030": ("Ambiguo", "JSON é uma saída possível, mas os campos não são definidos."),
    "B031": ("Ambiguo", "CSV é uma saída possível, mas as colunas não são definidas."),
    "B032": ("Ambiguo", "truth-csv é possível, mas a representação não é definida."),
    "B033": ("Determinado", "Código 2 representa condição não coberta, divergência ou problema de verify."),
    "B034": ("Determinado", "Z3 necessário ausente significa que o cálculo não terminou."),
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    text = C2.read_text(encoding="utf-8")
    inventory = {}
    with INVENTORY.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            inventory[row["Behavior ID"]] = row

    oracles = []
    for behavior_id, row in inventory.items():
        classification, uncertainty = PROPERTIES.get(
            behavior_id,
            ("Indeterminado", "Nenhum trecho C2 fornece uma definição suficiente."),
        )
        oracles.append({
            "oracle_id": f"C2-ORACLE-{behavior_id}",
            "behavior_id": behavior_id,
            "source_excerpt": "Trecho C2 relacionado; nenhuma correção por C1 foi usada.",
            "classified_requirement": row["Feature"],
            "interpretation": uncertainty,
            "classification": classification,
            "preconditions": "Somente documentação C2 disponível",
            "inputs": "Não determinados ou inferidos apenas se explicitados no trecho",
            "expected_result": "Não inventado quando a documentação não fornece",
            "confidence": "high" if classification == "Determinado" else "low",
            "inferred_information": [] if classification != "Inferido" else uncertainty,
            "indeterminate_information": uncertainty if classification in ("Ambiguo", "Indeterminado") else "",
            "generator": "GitHub Copilot agent; external model execution not performed",
        })

    (OUT / "oracle-catalog.json").write_text(
        json.dumps(oracles, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Catálogo de oráculos C2",
        "",
        "Esta geração usa exclusivamente a documentação C2 literal.",
        "Não foi utilizado LLM externo independente nem informação de C1.",
        "",
        "| Oracle ID | Behavior ID | Classificação | Interpretação |",
        "|---|---|---|---|",
    ]
    for oracle in oracles:
        lines.append(
            f"| {oracle['oracle_id']} | {oracle['behavior_id']} | "
            f"{oracle['classification']} | {oracle['interpretation']} |"
        )
    (OUT / "oracle-catalog.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    with (OUT / "oracle-catalog.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(oracles[0].keys()))
        writer.writeheader()
        writer.writerows(oracles)

    print(json.dumps({
        "oracles": len(oracles),
        "determined": sum(o["classification"] == "Determinado" for o in oracles),
        "inferred": sum(o["classification"] == "Inferido" for o in oracles),
        "ambiguous": sum(o["classification"] == "Ambiguo" for o in oracles),
        "indeterminate": sum(o["classification"] == "Indeterminado" for o in oracles),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
