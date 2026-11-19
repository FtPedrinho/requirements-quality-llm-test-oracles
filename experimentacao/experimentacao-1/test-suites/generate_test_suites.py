import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXP = ROOT / "experimentacao" / "experimentacao-1"
FORMAL = EXP / "formalization" / "results" / "formal-results.json"
OUT = EXP / "test-suites"

POTENTIAL = {"tis#2", "tis#3", "tis#4", "tis#6", "npp#5", "npp#8"}
NPP_OUTPUT = {"npp#9", "npp#10", "npp#11"}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    records = json.loads(FORMAL.read_text(encoding="utf-8"))
    cases = []
    for record in records:
        if record["system"] == "generic":
            continue
        reserve = []
        if record["id"] in POTENTIAL:
            reserve.append("RESSALVA-CONFLITO-POTENCIAL")
        if record["id"] in NPP_OUTPUT:
            reserve.append("RESSALVA-NPP-SAFETY-INJECTION-UNDECLARED")
        cases.append({
            "Test Case ID": f"E1-TC-{record['id']}-PASS",
            "Oracle ID": f"E1-ORC-{next(i for i, r in enumerate(json.loads((EXP / 'oracles' / 'oracle-catalog.json').read_text(encoding='utf-8')), 1) if r['Decision ID']==record['id'])}",
            "Requirement ID": record["requirement"],
            "Decision ID": record["id"],
            "Kind": "PASS",
            "Preconditions": record["guard"],
            "Inputs": "Modelo concreto que satisfaz a guarda",
            "Expected": "A decisao e verdadeira e as acoes explicitadas sao aplicadas",
            "Evaluability": "concretizavel",
            "Reserve": "; ".join(reserve) if reserve else "Nenhuma",
        })
    # Pair cases are counted from the formal record only; concrete values remain in formal/Z3 artifacts.
    formal_by_id = {record["id"]: record for record in records}
    # The exp0-style pair count is 119 leaves among 33 NAT2TEST decisions.
    # Pair rows do not require new domain information and remain traceable to the formal guard.
    pair_count = 0
    for record in records:
        if record["system"] == "generic":
            continue
        # No pair inventory is present in the simplified C1 formal JSON yet; use guard leaf count.
        guard = record["guard"]
        # Count AND/OR leaves approximately as comparison/variables, preserving only documented inventory.
        import re
        leaves = re.findall(r"[A-Za-z_][A-Za-z0-9_]*\s*(?:=|!=|<=|>=|<|>)\s*(?:-?\d+(?:\.\d+)?|true|false|[A-Za-z_][A-Za-z0-9_]*)", guard)
        if guard.count(" and ") == 0 and " /\\ " not in guard and " /\\ " not in guard:
            pass
        reserve = []
        if record["id"] in POTENTIAL:
            reserve.append("RESSALVA-CONFLITO-POTENCIAL")
        if record["id"] in NPP_OUTPUT:
            reserve.append("RESSALVA-NPP-SAFETY-INJECTION-UNDECLARED")
        for index in range(len(leaves)):
            pair_count += 1
            cases.append({
                "Test Case ID": f"E1-TC-{record['id']}-C{index + 1}",
                "Oracle ID": f"E1-ORC-{next(i for i, r in enumerate(json.loads((EXP / 'oracles' / 'oracle-catalog.json').read_text(encoding='utf-8')), 1) if r['Decision ID']==record['id'])}",
                "Requirement ID": record["requirement"],
                "Decision ID": record["id"],
                "Kind": "MC/DC",
                "Preconditions": "Demais condicoes fixadas conforme a formalizacao",
                "Inputs": "Par abstrato do modelo de independência",
                "Expected": "A condicao muda a decisao enquanto as demais condicoes permanecem fixas",
                "Evaluability": "simbólico",
                "Reserve": "; ".join(reserve) if reserve else "Nenhuma",
            })

    (OUT).mkdir(parents=True, exist_ok=True)
    import csv
    with (OUT / "generated-test-cases.csv").open("w", newline="", encoding="utf-8") as handle:
        fieldnames = list(cases[0].keys())
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cases)

    lines = [
        "# Casos de teste - Experimento 1",
        "",
        "Casos derivados dos oráculos C1 e das expressões experimentais. Casos não concretizados não são aprovados ou reprovados.",
        "",
        "| Test Case ID | Requirement ID | Decision ID | Tipo | Resultado esperado | Verificabilidade | Ressalva |",
        "|---|---|---|---|---|---|---|",
    ]
    for case in cases:
        lines.append(
            f"| {case['Test Case ID']} | {case['Requirement ID']} | {case['Decision ID']} | "
            f"{case['Kind']} | {case['Expected']} | {case['Evaluability']} | {case['Reserve']} |"
        )
    (OUT / "generated-test-cases.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"cases": len(cases), "pairs": pair_count}, ensure_ascii=False))


if __name__ == "__main__":
    main()
