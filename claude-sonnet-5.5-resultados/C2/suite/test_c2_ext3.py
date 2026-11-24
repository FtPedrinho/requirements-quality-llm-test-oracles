"""Extensao 3 (congelada antes da execucao): corrige so a leitura do truth-csv multi-bloco em C2-E07 (um cabecalho por decisao,
separado por linha em branco). Expectativas inalteradas."""
import csv, io
from test_c2 import run, mkfile, cid  # noqa: F401  (fixtures)
from test_c2 import SISTEMAS


def test_C2_E07(run):
    r = run("analyze", "--json", SISTEMAS["VM"][0], "--z3", "--format", "truth-csv", z3=True, timeout=600)
    blocos = [b for b in r.out.replace("\r\n", "\n").split("\n\n") if b.strip()]
    assert len(blocos) == 5
    for b in blocos:
        rd = list(csv.reader(io.StringIO(b)))
        head, rows = rd[0], rd[1:]
        i0, i1 = head.index("row") + 1, head.index("outcome")
        assert len(rows) == 2 ** (i1 - i0)
        assert all(v == "T" for v in rows[0][i0:i1])
