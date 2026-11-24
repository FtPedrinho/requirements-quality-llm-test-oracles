import json
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent
COVERAGE = ROOT / "cobertura"
REPORTS = [
    "baseline-total", "baseline-conformes-conclusivos", "repeticao-f03",
    "acumulado-total", "acumulado-conformes-conclusivos", "extensao",
    "final-total", "final-conformes-conclusivos",
]


def branch(node):
    counter = next((c for c in node.findall("counter") if c.get("type") == "BRANCH"), None)
    if counter is None:
        return {"cobertos": 0, "total": 0, "percentual": None}
    covered = int(counter.get("covered"))
    total = covered + int(counter.get("missed"))
    return {"cobertos": covered, "total": total,
            "percentual": round(100 * covered / total, 4) if total else None}


def summary(results):
    counts = {}
    for row in results:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    evaluated = sum(value for key, value in counts.items() if key == "PASSOU" or key.startswith("FALHOU"))
    passed = counts.get("PASSOU", 0)
    return {"casos": len(results), "status": counts, "assercoes_compostas_avaliadas": evaluated,
            "assercoes_satisfeitas": passed,
            "aprovacao_percentual": round(100 * passed / evaluated, 4) if evaluated else None,
            "duracao_segundos_soma": round(sum(r["duracao_segundos"] for r in results), 6)}


def main():
    baseline = json.loads((ROOT / "resultados.json").read_text(encoding="utf-8"))
    retry = json.loads((ROOT / "evidencias" / "F03-R2" / "resultado.json").read_text(encoding="utf-8"))
    extension = json.loads((ROOT / "resultados-extensao.json").read_text(encoding="utf-8"))
    coverage = {}
    classfiles = {p.relative_to(ROOT / "build" / "classes").with_suffix("").as_posix()
                  for p in (ROOT / "build" / "classes").rglob("*.class")}
    for name in REPORTS:
        report = ET.parse(COVERAGE / (name + ".xml")).getroot()
        report_classes = {c.get("name") for c in report.iter("class")}
        if report_classes != classfiles:
            raise RuntimeError(f"Escopo de classes diverge em {name}: {classfiles ^ report_classes}")
        totals = branch(report)
        modules = {}
        for pkg in report.findall("package"):
            module = pkg.get("name").split("/")[4]
            row = branch(pkg)
            target = modules.setdefault(module, {"cobertos": 0, "total": 0})
            target["cobertos"] += row["cobertos"]
            target["total"] += row["total"]
        for row in modules.values():
            row["percentual"] = round(100 * row["cobertos"] / row["total"], 4) if row["total"] else None
        coverage[name] = {"total": totals, "modulos": modules, "classfiles": len(classfiles)}
    mutation = sorted(c for c in classfiles if "/mutation/" in c)
    if not mutation:
        raise RuntimeError("Classes de mutacao ausentes do denominador")
    data = {
        "baseline": summary(baseline),
        "repeticao_tecnica": summary([retry]),
        "extensao": summary(extension),
        "execucoes_incluindo_repeticao": summary([*baseline, retry, *extension]),
        "oraculos_determinados_distintos": 14,
        "registros_indeterminados_de_conflito": 15,
        "taxa_indeterminacao_registros_percentual": round(100 * 15 / 29, 4),
        "nota_contagem_indeterminacao": "Contagem conservadora de registros de conflito; nao sao casos com entradas completas.",
        "revisao": "autoavaliacao; nao houve revisor independente",
        "classfiles_producao": len(classfiles),
        "classfiles_mutacao_incluidas": mutation,
        "branch_coverage": coverage,
    }
    data["branch_coverage_baseline_conformes_validos_executaveis"] = coverage["baseline-total"]
    data["branch_coverage_final_conformes_validos_executaveis"] = coverage["final-total"]
    data["nota_escopo_conforme"] = (
        "Todos os casos foram invocados, estruturalmente validos e autoavaliados conformes; "
        "F03 baseline teve erro tecnico posterior a invocacao. Os subconjuntos conclusivos sao adicionais."
    )
    (ROOT / "metricas.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    bars = [
        ("Baseline total", coverage["baseline-total"]["total"]),
        ("Baseline conformes conclusivos", coverage["baseline-conformes-conclusivos"]["total"]),
        ("Extensao isolada", coverage["extensao"]["total"]),
        ("Final total", coverage["final-total"]["total"]),
        ("Final conformes conclusivos", coverage["final-conformes-conclusivos"]["total"]),
    ]
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="820" height="250" viewBox="0 0 820 250">',
           '<rect width="820" height="250" fill="white"/>',
           '<text x="20" y="24" font-family="sans-serif" font-size="16">Branch Coverage - escopo completo</text>']
    for index, (label, values) in enumerate(bars):
        y = 52 + index * 36
        width = 400 * values["cobertos"] / values["total"]
        svg.extend([
            f'<text x="20" y="{y + 14}" font-family="sans-serif" font-size="12">{label}</text>',
            f'<rect x="260" y="{y}" width="400" height="18" fill="#eeeeee"/>',
            f'<rect x="260" y="{y}" width="{width:.2f}" height="18" fill="#276e9b"/>',
            f'<text x="670" y="{y + 14}" font-family="sans-serif" font-size="12">'
            f'{values["cobertos"]}/{values["total"]} ({values["percentual"]:.2f}%)</text>',
        ])
    svg.append("</svg>")
    (ROOT / "branch-coverage.svg").write_text("\n".join(svg) + "\n", encoding="utf-8")
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
