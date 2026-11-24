"""Extensao 2 da suite C2 (congelada antes da execucao): corrige apenas a verificacao de C2-020 e C2-E07 da extensao 1.
Expectativas (oraculo-extensao1.json) inalteradas."""
import csv, io, re
from test_c2 import run, mkfile, cid  # noqa: F401  (fixtures)
from test_c2 import SISTEMAS, _conj


def test_C2_020(run, tmp_path):
    out = tmp_path / "t20.txt"
    r = run("analyze", _conj(20), "-o", out)
    assert r.code == 0
    txt = out.read_text(encoding="utf-8")
    assert re.search(r"Tabela verdade: 1048576 linhas", txt)
    assert "Cobertura MC/DC: completa" in txt
    pares = txt.split("Pares de independência:")[1].split("Suíte mínima")[0]
    assert len(re.findall(r"^\s+X\d+: \(V", pares, re.M)) == 20


def test_C2_E07(run):
    r = run("analyze", "--json", SISTEMAS["VM"][0], "--z3", "--format", "truth-csv", z3=True, timeout=600)
    rd = csv.reader(io.StringIO(r.out))
    head = next(rd)
    i0, i1 = head.index("row") + 1, head.index("outcome")
    by = {}
    for w in rd:
        by.setdefault(w[0], []).append(w[i0:i1])
    assert by
    for d, rows in by.items():
        assert len(rows) == 2 ** (i1 - i0), d
        assert all(v == "T" for v in rows[0]), d
