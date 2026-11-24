import csv
import json
from pathlib import Path

root = Path(__file__).parent
records = json.loads((root / "casos.json").read_text(encoding="utf-8"))
for row in records:
    if "esperado" not in row:
        entry = row["entrada"]
        if entry["tipo"] in ("avaliacao", "truth_csv"):
            row["esperado"] = {item["id_oraculo"]: item["esperado"] for item in entry["linhas"]}
        else:
            row["esperado"] = entry.get("esperado")

with (root / "casos-detalhados.json").open("x", encoding="utf-8") as file:
    file.write(json.dumps(records, ensure_ascii=False, indent=2) + "\n")
columns = ["rodada", "id", "tipo", "classificacao", "entrada", "esperado", "observado",
           "status", "erro", "evidencia_z3", "stdout", "stderr", "duracao_ms"]
with (root / "casos-detalhados.csv").open("x", encoding="utf-8-sig", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=columns, extrasaction="ignore")
    writer.writeheader()
    for row in records:
        formatted = dict(row)
        for field in ("entrada", "esperado", "observado"):
            if isinstance(formatted.get(field), (dict, list)):
                formatted[field] = json.dumps(formatted[field], ensure_ascii=False, separators=(",", ":"))
        writer.writerow(formatted)
print("Casos detalhados:", len(records))
