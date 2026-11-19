import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research" / "experimentacao" / "experimentacao-0"
GABARITO = ROOT / "research" / "experimentacao" / "oracle-reference-catalog.csv"
OUT = EXP / "oracle"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    oracles = []
    with GABARITO.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            oracles.append({
                "oracle_id": f"E0-ORACLE-{row['Behavior ID']}",
                "behavior_id": row["Behavior ID"],
                "system": "Ferramenta MC/DC",
                "condition": "documentation-original",
                "behavior": row["Behavior"],
                "preconditions": row["Conditions"],
                "inputs": row["Inputs"],
                "expected_result": row["Expected Result"],
                "postconditions": "Resultado observavel pela CLI, API ou relatorio",
                "source": row["Documentation Origin"],
                "implementation_evidence": row["Implementation Evidence"],
                "rationale": "Oráculo criado pelo Copilot a partir da especificação e do inventário do SUT.",
                "uncertainties": [],
                "confidence": "documentado" if row["Status"] == "Pending review" else "pendente",
                "generated_by": "GitHub Copilot",
            })
    (OUT / "oracle-catalog.json").write_text(
        json.dumps(oracles, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# Catálogo de oráculos - Experimento 0 reconstruído",
        "",
        "| Oracle ID | Behavior ID | Comportamento | Resultado esperado | Fonte |",
        "|---|---|---|---|---|",
    ]
    for oracle in oracles:
        lines.append(
            f"| {oracle['oracle_id']} | {oracle['behavior_id']} | {oracle['behavior']} | "
            f"{oracle['expected_result']} | {oracle['source']} |"
        )
    (OUT / "oracle-catalog.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"oracles": len(oracles)}))


if __name__ == "__main__":
    main()
