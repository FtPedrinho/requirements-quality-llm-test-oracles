import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

out = Path(sys.argv[1])
indeterminate = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
cases = [json.loads(line) for line in (out / "casos.jsonl").read_text(encoding="utf-8").splitlines()]
root = ET.parse(out / "jacoco.xml").getroot()
counter = next(c for c in root.findall("counter") if c.attrib["type"] == "BRANCH")
missed = int(counter.attrib["missed"])
covered = int(counter.attrib["covered"])
total = missed + covered
statuses = {}
for case in cases:
    statuses[case["execucao"]] = statuses.get(case["execucao"], 0) + 1
summary = {
    "casos_conformes_gerados": 8,
    "casos_indeterminados_gerados": len(indeterminate),
    "casos_executados": len(cases),
    "resultados": statuses,
    "branch_covered": covered,
    "branch_total": total,
    "branch_percent": 100 * covered / total if total else None,
    "escopo": "todas as classes compiladas dos quatro módulos, inclusive mutação; harness excluído",
    "subconjunto_conforme": "igual à execução total: apenas os oito casos conformes foram executados"
}
(out / "resumo.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
width = 500 * covered / total if total else 0
svg = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="600" height="100">'
    '<text x="10" y="20">Branch Coverage: '
    f'{covered}/{total} ({summary["branch_percent"]:.2f}%)</text>'
    '<rect x="10" y="35" width="500" height="25" fill="#ddd"/>'
    f'<rect x="10" y="35" width="{width:.2f}" height="25" fill="#357abd"/>'
    '</svg>'
) if total else '<svg xmlns="http://www.w3.org/2000/svg"><text x="10" y="20">Não calculável</text></svg>'
(out / "branch.svg").write_text(svg, encoding="utf-8")
