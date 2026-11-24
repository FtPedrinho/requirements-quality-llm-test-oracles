import csv
import html
import json
import xml.etree.ElementTree as ET
from pathlib import Path

root = Path(__file__).parent.parent
out = Path(__file__).parent
sources = [
    ("baseline", "baseline/total-resultados.json"),
    ("extensao-1", "extensao-1/total-extensao.json"),
    ("extensao-2", "extensao-2/total-extensao-2.json"),
]
cases = []
for phase, relative in sources:
    for row in json.loads((root / relative).read_text(encoding="utf-8")):
        cases.append({"rodada": phase, **row})
with (out / "casos.json").open("x", encoding="utf-8") as file:
    file.write(json.dumps(cases, ensure_ascii=False, indent=2) + "\n")

columns = ["rodada", "id", "tipo", "classificacao", "entrada", "esperado", "observado",
           "status", "erro", "evidencia_z3", "stdout", "stderr", "duracao_ms"]
with (out / "casos.csv").open("x", encoding="utf-8-sig", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=columns, extrasaction="ignore")
    writer.writeheader()
    for case in cases:
        row = dict(case)
        for field in ("entrada", "esperado", "observado"):
            if isinstance(row.get(field), (dict, list)):
                row[field] = json.dumps(row[field], ensure_ascii=False, separators=(",", ":"))
        writer.writerow(row)

coverage = []
for phase in ("baseline", "extensao-1", "extensao-2"):
    for subset in ("total", "conformes"):
        tree = ET.parse(root / phase / f"{subset}-jacoco.xml").getroot()
        counter = next(c for c in tree.findall("counter") if c.get("type") == "BRANCH")
        covered = int(counter.get("covered"))
        missed = int(counter.get("missed"))
        coverage.append({
            "rodada": phase, "subconjunto": subset, "branches_cobertos": covered,
            "branches_totais": covered + missed, "percentual": round(100 * covered / (covered + missed), 4),
        })
with (out / "cobertura.csv").open("x", encoding="utf-8-sig", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=list(coverage[0]))
    writer.writeheader()
    writer.writerows(coverage)

tree = ET.parse(root / "extensao-2" / "total-jacoco.xml").getroot()
classes = []
for package in tree.findall("package"):
    for node in package.findall("class"):
        counter = next((c for c in node.findall("counter") if c.get("type") == "BRANCH"), None)
        covered = int(counter.get("covered")) if counter is not None else 0
        missed = int(counter.get("missed")) if counter is not None else 0
        name = node.get("name")
        module = next((m for m in ("core", "requirements", "z3", "cli") if f"/mcdc/{m}/" in name), "desconhecido")
        classes.append({"modulo": "mcdc-" + module, "classe": name,
                        "branches_cobertos": covered, "branches_totais": covered + missed})
with (out / "escopo-classes.csv").open("x", encoding="utf-8-sig", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["modulo", "classe", "branches_cobertos", "branches_totais"])
    writer.writeheader()
    writer.writerows(sorted(classes, key=lambda row: row["classe"]))

rows = "\n".join(
    f"<tr><td>{html.escape(c['rodada'])}</td><td>{html.escape(c['subconjunto'])}</td>"
    f"<td>{c['branches_cobertos']}/{c['branches_totais']}</td><td>{c['percentual']:.2f}%</td>"
    f"<td><progress value=\"{c['branches_cobertos']}\" max=\"{c['branches_totais']}\"></progress></td></tr>"
    for c in coverage
)
page = f"""<!doctype html>
<html lang="pt-br"><head><meta charset="utf-8"><title>Experimento C2</title>
<style>body{{font:16px sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem}}
table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #aaa;padding:.5rem;text-align:left}}
progress{{width:100%}}.warning{{border-left:4px solid #a50;padding:.5rem 1rem;background:#fff3dd}}</style></head>
<body><h1>Experimento C2</h1>
<p class="warning">Sem cegamento garantido. C108 falhou sob o oráculo congelado, mas sua fundamentação é ambígua em revisão posterior. Os casos concretos da extensão 2 foram formalizados após inspeção do SUT.</p>
<h2>Branch Coverage</h2><table><thead><tr><th>Rodada acumulada</th><th>Subconjunto</th><th>Branches</th><th>Percentual</th><th>Visualização</th></tr></thead>
<tbody>{rows}</tbody></table>
<p><a href="../relatorio.md">Relatório</a> · <a href="casos-detalhados.csv">Casos CSV</a> · <a href="casos-detalhados.json">Casos JSON</a> · <a href="escopo-classes.csv">Classes</a></p>
</body></html>"""
with (out / "painel.html").open("x", encoding="utf-8") as file:
    file.write(page)
print("Casos consolidados:", len(cases))
print("Classes no escopo:", len(classes))
print("Séries de cobertura:", len(coverage))
