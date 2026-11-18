import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT = ROOT / "experimentacao" / "experimentacao-0"
OUT_JSON = EXPERIMENT / "oracles" / "oracle-catalog.json"
OUT_MD = EXPERIMENT / "oracles" / "oracle-catalog.md"


def state_from_actions(actions):
    states = []
    for action in actions:
        if ":=" in action:
            states.append(action.replace(":=", "recebe"))
    return "; ".join(states) if states else "Não especificado"


def parse_generic():
    records = []
    path = ROOT / "exemplos" / "requisitos.mcdc"
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        req, guard = (part.strip() for part in line.split(":", 1))
        records.append({
            "id": f"generic-{req}",
            "requirement": req,
            "text": guard,
            "guard": guard,
            "actions": [],
            "system": "generic",
            "source": "exemplos/requisitos.mcdc",
            "inputs": sorted({token for token in guard.replace("(", " ").replace(")", " ").replace("and", " ").replace("or", " ").replace("not", " ").split() if token}),
        })
    return records


def parse_json():
    records = []
    for filename in ("vm-decisoes.json", "tis-decisoes.json", "npp-decisoes.json"):
        path = ROOT / "exemplos" / filename
        data = json.loads(path.read_text(encoding="utf-8"))
        input_names = [item["name"] for item in data["inputs"]]
        for decision in data["decisions"]:
            records.append({
                "id": decision["id"],
                "requirement": decision["requirement"],
                "text": decision["text"],
                "guard": decision["guard"],
                "actions": decision["actions"],
                "system": data["system"],
                "source": f"exemplos/{filename}",
                "inputs": [name for name in input_names if name in decision["guard"]],
            })
    return records


def build_oracle(record, index):
    uncertainty = [
        "Estado inicial não especificado independentemente da guarda.",
        "Saída não especificada fora das ações explícitas.",
        "Implementação e comportamento executável não consultados nesta etapa.",
    ]
    if "_antes" in record["guard"]:
        uncertainty.append("A semântica do estado anterior depende da transição documentada no texto original.")
    if record["system"] == "generic":
        uncertainty.append("Domínio das variáveis não informado no arquivo .mcdc.")
    return {
        "Oracle ID": f"ORC-{index:03d}",
        "Requirement ID": record["requirement"],
        "Decision ID": record["id"],
        "Preconditions": record["guard"],
        "Initial State": "Não especificado",
        "Inputs": record["inputs"],
        "Conditions": record["guard"],
        "Trigger/Event": record["text"].split(" the ", 1)[0] if record["text"] else "Não especificado",
        "Expected Decision": "verdadeiro quando a guarda é satisfeita",
        "Expected Action": record["actions"] if record["actions"] else "Nenhuma ação explicitamente documentada",
        "Expected Output": "Não especificado além das ações explícitas",
        "Expected State": state_from_actions(record["actions"]),
        "Rationale": record["text"] if record["text"] else record["guard"],
        "Source Reference": record["source"],
        "Uncertainties": uncertainty,
        "Z3 Interpretation Used": False,
    }


def main():
    records = parse_json() + parse_generic()
    catalog = [build_oracle(record, index) for index, record in enumerate(records, 1)]
    OUT_JSON.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Catálogo de oráculos",
        "",
        "Os oráculos desta etapa foram preparados a partir exclusivamente dos textos e guardas originais. Nenhum resultado interpretativo do Z3 foi usado como resposta esperada.",
        "",
        "| Oracle ID | Requirement ID | Decision ID | Resultado esperado | Fonte |",
        "|---|---|---|---|---|",
    ]
    for oracle in catalog:
        lines.append(
            f"| {oracle['Oracle ID']} | {oracle['Requirement ID']} | {oracle['Decision ID']} | "
            f"{oracle['Expected Decision']} | {oracle['Source Reference']} |"
        )
    lines.extend([
        "",
        "## Campos estruturados",
        "",
    ])
    for oracle in catalog:
        lines.append(f"### {oracle['Oracle ID']} - {oracle['Decision ID']}")
        for field in ("Preconditions", "Initial State", "Inputs", "Conditions", "Trigger/Event",
                      "Expected Decision", "Expected Action", "Expected Output", "Expected State",
                      "Rationale", "Source Reference", "Uncertainties"):
            value = oracle[field]
            if isinstance(value, list):
                value = ", ".join(str(item) for item in value) if value else "Nenhum"
            lines.append(f"- **{field}:** {value}")
        lines.append("")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"oracles": len(catalog), "output": str(OUT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
