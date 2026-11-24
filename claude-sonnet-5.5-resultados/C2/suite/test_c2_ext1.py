"""Extensao 1 da suite C2 (congelada antes da execucao). Reaproveita fixtures de test_c2.py."""
import csv, io, re
from test_c2 import run, mkfile, cid  # noqa: F401  (fixtures)
from test_c2 import dec0, SISTEMAS, FULL, _vj, _d, _conj


def test_C2_020(run, tmp_path):
    out = tmp_path / "t20.txt"
    r = run("analyze", _conj(20), "-o", out)
    assert r.code == 0
    txt = out.read_text(encoding="utf-8")
    assert re.search(r"Tabela verdade: 1048576 linhas", txt)
    assert "Cobertura MC/DC: completa" in txt
    assert len(re.findall(r"^\s+X\d+: V", txt.split("Pares de independência:")[1].split("Suíte mínima")[0], re.M)) == 20


def test_C2_E01(run, mkfile):
    r = run("check", "(A and B) or C", "--tests", mkfile("t.csv", FULL), "--format", "text")
    assert r.code == 0


def test_C2_E02(run, mkfile):
    r = run("check", "(A and B) or C", "--tests", mkfile("t.csv", "test,input,value\nT1,A,T\nT1,B,T\nT1,C,F\nT2,A,F\nT2,B,T\nT2,C,F\n"), "--format", "text")
    assert r.code == 2


def test_C2_E03(run, mkfile):
    r = run("verify", "--json", mkfile("c.json", _vj(_d(1, "sw = on", "lo") + "," + _d(2, "sw = on", "hi"))), "--format", "text", z3=True)
    assert r.code == 2


def test_C2_E04(run, mkfile):
    r = run("verify", "--json", mkfile("c.json", _vj(_d(1, "sw = on", "lo") + "," + _d(2, "sw = off", "hi"))), "--format", "text", z3=True)
    assert r.code == 0


def test_C2_E05(run):
    r = run("analyze", "--json", SISTEMAS["VM"][0], "--z3", "--format", "text", z3=True, timeout=600)
    assert r.code == 0 and r.out.strip()


def test_C2_E06(run):
    r = run("analyze", "(A and B) or C", "--z3", "--boundary", "--format", "text", z3=True)
    assert r.code == 0


def test_C2_E07(run):
    r = run("analyze", "--json", SISTEMAS["VM"][0], "--z3", "--format", "truth-csv", z3=True, timeout=600)
    by = {}
    for w in csv.DictReader(io.StringIO(r.out)):
        by.setdefault(w["decision"], []).append(w)
    assert by
    for d, rows in by.items():
        ins = [k for k in rows[0] if k not in ("decision", "requirement", "row", "outcome", "feasible", "in_suite", "demonstrates", "concrete_values")]
        assert len(rows) == 2 ** len(ins), d
        assert all(rows[0][k] == "T" for k in ins), d


def test_C2_E08(run, mkfile, tmp_path):
    out = tmp_path / "v.txt"
    r = run("verify", "--json", mkfile("c.json", _vj(_d(1, "sw = on", "lo") + "," + _d(2, "sw = on", "hi"))), "-o", out, z3=True)
    assert out.exists() and out.stat().st_size > 0 and r.code == 2
