import importlib.util
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("baseline_harness", root / "suite-baseline.py")
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
b.EVIDENCE = root / "extensao2"
b.EVIDENCE.mkdir(exist_ok=True)
b.RESULTS = []


def verify(result):
    b.code(0)(result)
    text = result["stdout"]
    table = re.findall(r"(?m)^\s*(\S+)\s+([TF])\s+([TF])\s*\|\s*([TF])\s*$", text)
    if len(table) != 4:
        raise ValueError("Não foi possível interpretar quatro linhas da tabela textual")
    vectors = {name: (a == "T", c == "T", out == "T") for name, a, c, out in table}
    expected = {(a, c): a and c for a in (False, True) for c in (False, True)}
    b.require({(a, c): out for a, c, out in vectors.values()} == expected,
              "tabela textual não corresponde a A e B")
    found = {name: (left, right) for name, left, right in
             re.findall(r"(?m)^\s*([AB]):\s*\((\S+),\s*(\S+)\)", text)}
    if set(found) != {"A", "B"}:
        raise ValueError("Não foi possível interpretar os pares do relatório textual")
    suite = set(re.findall(r"(?m)^\s*(\S+)\s+[TF]{2}\s+->\s+[TF]", text))
    for i, name in enumerate(("A", "B")):
        left, right = found[name]
        a, c = vectors[left], vectors[right]
        b.require(left in suite and right in suite and a[i] != c[i] and a[2] != c[2],
                  f"par ou suíte inválidos para {name}")


b.run_case("E20", ["analyze", "A and B"], verify)
(b.EVIDENCE / "resultados.json").write_text(json.dumps(b.RESULTS, ensure_ascii=False, indent=2), encoding="utf-8")
if b.RESULTS[0]["resultado"] != "PASSOU":
    raise SystemExit(1)
