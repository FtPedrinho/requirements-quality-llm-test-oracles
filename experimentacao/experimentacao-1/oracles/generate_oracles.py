import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXP = ROOT / "experimentacao" / "experimentacao-1"
REQ = EXP / "requirements" / "experimental"
OUT = EXP / "oracles"

POTENTIAL_CONFLICTS = {
    "tis#2", "tis#3", "tis#4", "tis#6",
    "npp#5", "npp#8",
}
NPP_OUTPUT_UNDECLARED = {"npp#9", "npp#10", "npp#11"}


def parse_records():
    records = []
    for filename in ("vm-decisoes.json", "tis-decisoes.json", "npp-decisoes.json"):
        data = json.loads((REQ / filename).read_text(encoding="utf-8"))
        input_names = [item["name"] for item in data["inputs"]]
        for decision in data["decisions"]:
            records.append({
                "id": decision["id"],
                "requirement": decision["requirement"],
                "system": data["system"],
                "text": decision["text"],
                "guard": decision["guard"],
                "actions": decision["actions"],
                "source": f"experimentacao/experimentacao-1/requirements/experimental/{filename}",
                "inputs": [name for name in input_names if name in decision["guard"]],
            })

    for line in (REQ / "requisitos.mcdc").read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        req, guard = (part.strip() for part in line.split(":", 1))
        records.append({
            "id": req,
            "requirement": req,
            "system": "generic",
            "text": guard,
            "guard": guard,
            "actions": [],
            "source": "experimentacao/experimentacao-1/requirements/experimental/requisitos.mcdc",
            "inputs": sorted(set(
                part for part in guard.replace("(", " ").replace(")", " ")
                .replace("and", " ").replace("or", " ").replace("not", " ")
                .split()
                if part
            )),
        })
    return records


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    records = parse_records()
    catalog = []
    for index, record in enumerate(records, 1):
        uncertainties = [
            "Estado inicial nao especificado independentemente da guarda.",
            "Comportamentos fora das acoes explicitas nao foram inferidos.",
        ]
        reserved = ""
        confidence = "documentado"
        if record["id"] in POTENTIAL_CONFLICTS:
            uncertainties.append(
                "O requisito participa de uma sobreposicao formal com acoes potencialmente conflitantes; alcançabilidade e prioridade nao foram confirmadas."
            )
            reserved = "RESSALVA-TIS-NPP"
            confidence = "documentado-com-ressalva"
        if record["id"] in NPP_OUTPUT_UNDECLARED:
            uncertainties.append(
                "the_safety_injection_mode aparece em acoes, mas nao esta declarado em inputs com tipo ou dominio; nenhuma hipotese foi usada como fato."
            )
            reserved = "RESSALVA-NPP-OUTPUT"
            confidence = "parcialmente-especificado"

        catalog.append({
            "Oracle ID": f"E1-ORC-{index:03d}",
            "System": record["system"],
            "Requirement ID": record["requirement"],
            "Decision ID": record["id"],
            "Source": record["source"],
            "Execution Condition": record["guard"],
            "Initial State": "Nao especificado",
            "Inputs": record["inputs"],
            "Expected Decision": "verdadeiro quando a guarda e satisfeita",
            "Expected Action": record["actions"] if record["actions"] else "Nenhuma acao explicitamente documentada",
            "Expected Output": "Nao especificado além das acoes explicitas",
            "Rationale": record["text"],
            "Uncertainties": uncertainties,
            "Confidence": confidence,
            "Reserve": reserved,
        })

    (OUT / "oracle-catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    lines = [
        "# Catalogo de oráculos - Experimento 1",
        "",
        "Os oraculos foram gerados exclusivamente a partir de `requirements/experimental/`. Nenhum resultado Z3 foi usado para induzir expectativas.",
        "",
        "| Oracle ID | Sistema | Requirement ID | Decision ID | Condição de execução | Confiança | Ressalva |",
        "|---|---|---|---|---|---|---|",
    ]
    for oracle in catalog:
        lines.append(
            f"| {oracle['Oracle ID']} | {oracle['System']} | {oracle['Requirement ID']} | "
            f"{oracle['Decision ID']} | {oracle['Execution Condition']} | "
            f"{oracle['Confidence']} | {oracle['Reserve'] or 'Nenhuma'} |"
        )
    lines += ["", "## Detalhes", ""]
    for oracle in catalog:
        lines.append(f"### {oracle['Oracle ID']} - {oracle['Decision ID']}")
        for field in ("System", "Requirement ID", "Source", "Execution Condition", "Initial State",
                      "Inputs", "Expected Decision", "Expected Action", "Expected Output",
                      "Rationale", "Uncertainties", "Confidence", "Reserve"):
            value = oracle[field]
            if isinstance(value, list):
                value = ", ".join(str(item) for item in value) if value else "Nenhum"
            lines.append(f"- **{field}:** {value}")
        lines.append("")
    (OUT / "oracle-catalog.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"oracles": len(catalog)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
