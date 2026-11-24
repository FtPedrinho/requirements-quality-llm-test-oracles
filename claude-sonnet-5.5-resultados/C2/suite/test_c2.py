"""Suite pytest C2 -- um teste por caso DETERMINADO do oraculo congelado (C2-nnn).
Casos INDETERMINADOS nao sao executados (decisao do pesquisador); ver conftest.py.
As expectativas vem do oraculo (texto de tool-readme-C2.md), nunca do comportamento observado."""
import csv, io, json, os, re, subprocess
from pathlib import Path
import pytest

REPO = Path(os.environ.get("MCDC_REPO", Path(__file__).resolve().parents[3]))
RAW = Path(os.environ.get("C2_RAW", Path(__file__).resolve().parents[1] / "resultados" / "rodada-01-baseline" / "bruto"))
Z3_DIR = os.environ.get("Z3_DIR", r"C:\Users\User\AppData\Roaming\Python\bin")
CLASSPATH = str(REPO / "mcdc-cli" / "target" / "classes") + os.pathsep + \
    (REPO / "mcdc-cli" / "target" / "classpath.txt").read_text().strip()
MAIN = "io.github.rvdomingos.mcdc.cli.Main"


def _env(z3):
    env = dict(os.environ)
    parts = [p for p in env.get("PATH", "").split(os.pathsep) if p and Path(p).resolve() != Path(Z3_DIR).resolve()
             and not (Path(p) / "z3.exe").exists()]
    if z3:
        parts.append(Z3_DIR)
    env["PATH"] = os.pathsep.join(parts)
    return env


class Res:
    def __init__(self, code, out, err):
        self.code, self.out, self.err = code, out, err

    @property
    def js(self):
        try:
            return json.loads(self.out)
        except Exception as e:  # saida nao-JSON => falha semantica da expectativa
            raise AssertionError(f"saida nao e JSON valido: {e}; inicio={self.out[:200]!r}")


@pytest.fixture
def cid(request):
    return request.node.name.replace("test_", "").replace("_", "-")


@pytest.fixture
def run(cid, tmp_path):
    counter = [0]

    def _run(*args, z3=False, timeout=240, keep=True):
        counter[0] += 1
        cmd = ["java", "-Dstdout.encoding=UTF-8", "-Dstderr.encoding=UTF-8", "-cp", CLASSPATH, MAIN, *map(str, args)]
        p = subprocess.run(cmd, cwd=REPO, env=_env(z3), capture_output=True, timeout=timeout)
        out, err = p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")
        d = RAW / cid
        d.mkdir(parents=True, exist_ok=True)
        n = counter[0]
        (d / f"{n}_comando.txt").write_text("mcdc " + " ".join(map(str, args)) + f"\nz3_no_PATH={z3}\nexit={p.returncode}\n", encoding="utf-8")
        (d / f"{n}_stdout.txt").write_text(out[:200000], encoding="utf-8")
        (d / f"{n}_stderr.txt").write_text(err[:20000], encoding="utf-8")
        return Res(p.returncode, out, err)

    return _run


@pytest.fixture
def mkfile(cid, tmp_path):
    def _mk(name, content):
        p = tmp_path / name
        p.write_text(content, encoding="utf-8", newline="\n")
        d = RAW / cid / "entradas"
        d.mkdir(parents=True, exist_ok=True)
        (d / name).write_text(content, encoding="utf-8", newline="\n")
        return p
    return _mk


# ---------------------------------------------------------------- utilitarios de leitura dos relatorios
def dec0(js):
    return js["decisions"][0]


def labels(x):
    return [c["label"] for c in x["conditions"]]


def all_demonstrated(x):
    return bool(x["complete"]) and not x["uncovered"]


def pairs_only_target_differs(x):
    """causa unica: em cada par listado, so a entrada da condicao difere."""
    rows = {r["vector"]: r["values"] for r in x["truthTable"]}
    inp = {c["label"]: c["input"] for c in x["conditions"]}
    for lab, prs in x["independencePairs"].items():
        assert prs, f"condicao {lab} sem par"
        for a, b in prs:
            diff = [k for k in rows[a] if rows[a][k] != rows[b][k]]
            assert diff == [inp[lab]], (lab, a, b, diff)


def ev(expr, env):
    return bool(eval(expr, {}, env))


def eval_guard(expr_py, row):
    return ev(expr_py, row)


# ================================================================ A: analyze basico
def test_C2_001(run):
    r = run("analyze", "(A and B) or C", "--format", "json")
    x = dec0(r.js)
    assert r.code == 0
    assert [i["name"] for i in x["inputs"]] == ["A", "B", "C"] and labels(x) == ["A", "B", "C"]
    assert x["truthTableRows"] == 8 and not [t for t in x["truthTable"] if not t["feasible"]]
    assert all_demonstrated(x) and all(x["independencePairs"][l] for l in "ABC")
    assert len(x["minimalSuite"]) == 4


def test_C2_002(run):
    r = run("analyze", "(A and B) or C", "--unique-cause", "--format", "json")
    x = dec0(r.js)
    assert r.code == 0 and all_demonstrated(x)
    assert labels(x) == ["A", "B", "C"]
    pairs_only_target_differs(x)
    assert len(x["minimalSuite"]) == 4


def test_C2_003(run):
    r = run("analyze", "A and not B", "--format", "json")
    x = dec0(r.js)
    assert r.code == 0 and all_demonstrated(x)
    assert len(x["conditions"]) == 2 and x["truthTableRows"] == 4
    assert len(x["minimalSuite"]) == 3


def test_C2_004(run):
    r = run("analyze", "(A and B) or (not A and C)", "--format", "json")
    x = dec0(r.js)
    assert len(x["inputs"]) == 3
    assert labels(x) == ["A#1", "B", "A#2", "C"]
    assert x["truthTableRows"] == 8


def test_C2_006(run):
    r = run("analyze", "(A && B) || !C", "--format", "json")
    x = dec0(r.js)
    assert r.code == 0 and all_demonstrated(x)
    assert len(x["conditions"]) == 3 and x["truthTableRows"] == 8 and len(x["minimalSuite"]) == 4


def test_C2_007(run):
    r = run("analyze", r"(A /\ B) \/ not C", "--format", "json")
    x = dec0(r.js)
    assert r.code == 0 and all_demonstrated(x)
    assert len(x["conditions"]) == 3 and x["truthTableRows"] == 8 and len(x["minimalSuite"]) == 4


def test_C2_008(run):
    r = run("analyze", r"speed > 100 /\ mode = idle", "--format", "json")
    x = dec0(r.js)
    assert r.code == 0 and all_demonstrated(x)
    assert len(x["conditions"]) == 2 and x["truthTableRows"] == 4 and len(x["minimalSuite"]) == 3


def test_C2_009(run):
    for op in ["=", "==", "!=", "<", "<=", ">", ">="]:
        r = run("analyze", f"x {op} 5", "--format", "json")
        assert r.code == 0, op
        x = dec0(r.js)
        assert all_demonstrated(x) and len(x["conditions"]) == 1, op
        assert x["truthTableRows"] == 2 and len(x["minimalSuite"]) == 2, op


# ================================================================ B: diagnostico
def test_C2_010(run):
    r = run("analyze", "A or (B and C)", "--constraint", "not A or B", "--format", "json")
    x = dec0(r.js)
    assert r.code == 0 and all_demonstrated(x) and len(x["conditions"]) == 3
    assert x["truthTableRows"] == 8
    imp = [t for t in x["truthTable"] if not t["feasible"]]
    assert len(imp) == 2 and all(t["values"]["A"] and not t["values"]["B"] for t in imp)
    r2 = run("analyze", "A or (B and C)", "--constraint", "not A or B", "--format", "truth-csv")
    rows = list(csv.DictReader(io.StringIO(r2.out)))
    assert len(rows) == 8 and sum(1 for w in rows if w["feasible"] == "F") == 2


def test_C2_011(run):
    r = run("analyze", "A and B", "--constraint", "not A or not B")
    assert r.code == 2
    assert re.search(r"A: bloqueada", r.out) and re.search(r"B: bloqueada", r.out)
    assert "redundante" not in r.out.split("Cobertura MC/DC")[-1]


def test_C2_012(run):
    r = run("analyze", "A or (A and B)")
    assert r.code == 2
    assert re.search(r"B: redundante", r.out) and not re.search(r"B: bloqueada", r.out)


def test_C2_013(run):
    r = run("analyze", "speed > 100 or (speed > 50 and rain)", "--z3", "--format", "json", z3=True)
    x = dec0(r.js)
    assert r.code == 0
    assert x["truthTableRows"] == 8
    imp = [t for t in x["truthTable"] if not t["feasible"]]
    assert len(imp) == 2
    assert all(t["values"]["speed > 100"] and not t["values"]["speed > 50"] for t in imp)
    assert x["minimalSuite"]
    for t in x["minimalSuite"]:
        a = t["assignment"]
        speed, rain = int(a["speed"]), a["rain"] in ("true", "T", True)
        c1, c2 = speed > 100, speed > 50
        assert t["values"]["speed > 100"] == c1 and t["values"]["speed > 50"] == c2 and t["values"]["rain"] == rain
        assert t["outcome"] == (c1 or (c2 and rain))


def test_C2_014(run):
    r = run("analyze", "speed > 100 or (speed > 50 and rain)", "--z3", "--boundary", "--format", "csv", z3=True)
    assert r.code == 0
    speeds = set()
    for row in csv.DictReader(io.StringIO(r.out)):
        m = re.search(r"speed = (-?\d+)", row["concrete_values"])
        if m:
            speeds.add(int(m.group(1)))
    assert {100, 101, 50, 51} <= speeds, speeds


def test_C2_015(run):
    r = run("analyze", "(A and B) or C", "--z3", z3=False)
    assert re.search(r"z3", r.out + r.err, re.I)


# ================================================================ C: exact / direct / limites
def test_C2_016(run):
    r = run("analyze", "(A and B) or C", "--exact", "--format", "json", z3=True)
    assert r.code == 0 and len(dec0(r.js)["minimalSuite"]) == 4
    r = run("analyze", "A and not B", "--exact", "--format", "json", z3=True)
    assert r.code == 0 and len(dec0(r.js)["minimalSuite"]) == 3


def test_C2_017(run):
    r = run("analyze", "(A or B) and (C or D)", "--exact", "--unique-cause", "--format", "json", z3=True)
    x = dec0(r.js)
    assert r.code == 0 and all_demonstrated(x) and len(x["conditions"]) == 4
    assert len(x["minimalSuite"]) == 5


def _conj(n):
    return " and ".join(f"X{i}" for i in range(1, n + 1))


def test_C2_020(run, tmp_path):
    out = tmp_path / "t20.txt"
    r = run("analyze", _conj(20), "-o", out)
    assert r.code == 0
    txt = out.read_text(encoding="utf-8")
    assert "Cobertura MC/DC: completa" in txt
    assert len(re.findall(r"^V\d+ ", txt, re.M)) == 2 ** 20
    demo = txt.split("Demonstração por condição:")[1]
    assert len(re.findall(r"^\s+X\d+: ", demo, re.M)) == 20


def test_C2_021(run):
    r = run("analyze", _conj(13), "--z3", "--format", "json", z3=True)
    x = dec0(r.js)
    assert r.code == 0 and all_demonstrated(x) and len(x["conditions"]) == 13


def test_C2_022(run):
    r = run("analyze", _conj(30), "--direct", "--format", "json", z3=True)
    x = dec0(r.js)
    assert r.code == 0 and all_demonstrated(x) and len(x["conditions"]) == 30


def test_C2_023(run):
    r = run("analyze", "(A and B) or C", "--direct", "--format", "json", z3=True)
    x = dec0(r.js)
    assert r.code == 0 and all_demonstrated(x) and len(x["conditions"]) == 3
    r = run("analyze", "A or (A and B)", "--direct", "--format", "json", z3=True)
    x = dec0(r.js)
    assert r.code == 2
    assert any(u["condition"] == "B" and u["reason"] == "REDUNDANT" for u in x["uncovered"])


# ================================================================ D: sistemas de exemplo
SISTEMAS = {
    "VM": ("exemplos/vm-decisoes.json", 5, 5, 21, 152, 4, 26, 152, 0, 152, 0),
    "TIS": ("exemplos/tis-decisoes.json", 17, 14, 69, 268, 4, 80, 450, 21, 428, 3),
    "NPP": ("exemplos/npp-decisoes.json", 11, 11, 29, 76, 1, 40, 146, 0, 146, 1),
}


def _analyze_sys(run, key, *extra):
    arq = SISTEMAS[key][0]
    return run("analyze", "--json", arq, "--z3", *extra, "--format", "json", z3=True, timeout=600)


def _sys_numbers(js):
    ds = js["decisions"]
    return dict(req=len(ds), completos=sum(1 for d in ds if d["complete"]),
                cond=sum(len(d["conditions"]) for d in ds),
                comb=sum(d["truthTableRows"] for d in ds),
                imp=sum(1 for d in ds for t in d["truthTable"] if not t["feasible"]),
                testes=sum(len(d["minimalSuite"]) for d in ds))


def _sys_case(run, key):
    _, req, comp, cond, comb, imp, tst, *_ = SISTEMAS[key]
    r = _analyze_sys(run, key)
    n = _sys_numbers(r.js)
    assert n == dict(req=req, completos=comp, cond=cond, comb=comb, imp=imp, testes=tst), n
    assert r.code == (0 if comp == req else 2)


def test_C2_026(run): _sys_case(run, "VM")
def test_C2_027(run): _sys_case(run, "TIS")
def test_C2_028(run): _sys_case(run, "NPP")


def _mut_case(run, key):
    _, *_, mut, eq, peg, _c = SISTEMAS[key]
    r = _analyze_sys(run, key, "--mutation")
    faults = [f for d in r.js["decisions"] for f in d["mutation"]["faults"].values()]
    got = (sum(f["total"] for f in faults), sum(f["equivalent"] for f in faults), sum(f["killed"] for f in faults))
    assert got == (mut, eq, peg), got


def test_C2_029(run): _mut_case(run, "VM")
def test_C2_030(run): _mut_case(run, "TIS")
def test_C2_031(run): _mut_case(run, "NPP")


def _verify_case(run, key):
    arq, *_, conf = SISTEMAS[key]
    r = run("verify", "--json", arq, "--format", "json", z3=True, timeout=300)
    assert len(r.js["conflicts"]) == conf
    assert r.code == (0 if conf == 0 else 2)


def test_C2_032(run): _verify_case(run, "VM")
def test_C2_033(run): _verify_case(run, "TIS")
def test_C2_034(run): _verify_case(run, "NPP")


def test_C2_036(run):
    r = run("analyze", "-f", "exemplos/requisitos.mcdc", "--format", "json")
    ds = {d["id"]: d for d in r.js["decisions"]}
    assert "REQ-003" in ds
    assert any(u["reason"] == "REDUNDANT" for u in ds["REQ-003"]["uncovered"])
    assert r.code == 2


# ================================================================ E: formatos
def test_C2_037(run, mkfile):
    f = mkfile("req.mcdc", "# comentario\nREQ-001: (alarme_ativo and porta_aberta) or botao_emergencia\nREQ-002: porta_fechada and not obstaculo\n")
    r = run("analyze", "-f", f, "--format", "json")
    ds = {d["id"]: d for d in r.js["decisions"]}
    assert set(ds) == {"REQ-001", "REQ-002"} and len(r.js["decisions"]) == 2
    assert len(ds["REQ-001"]["conditions"]) == 3 and len(ds["REQ-001"]["minimalSuite"]) == 4
    assert len(ds["REQ-002"]["conditions"]) == 2 and len(ds["REQ-002"]["minimalSuite"]) == 3
    assert r.code == 0


VM1 = ('{"system":"the_coffee_machine_system","inputs":[{"name":"the_system_mode","type":"enum","values":["idle","choice"]},'
       '{"name":"the_coin_sensor","type":"bool"}],"decisions":[{"id":"vm#1","requirement":"REQ-001",'
       '"guard":"the_system_mode = idle /\\\\ the_coin_sensor = true","actions":["the_system_mode := choice"]}]}')


def test_C2_038(run, mkfile):
    f = mkfile("vm1.json", VM1)
    r = run("analyze", "--json", f, "--format", "json")
    x = dec0(r.js)
    assert x["id"] == "vm#1" and x["requirement"] == "REQ-001"
    assert len(x["conditions"]) == 2 and all_demonstrated(x) and len(x["minimalSuite"]) == 3
    assert r.code == 0


def test_C2_039(run):
    r = run("analyze", "(A and B) or C", "--format", "csv")
    rows = list(csv.DictReader(io.StringIO(r.out)))
    tests = {}
    for w in rows:
        tests.setdefault(w["test"], {})[w["input"]] = (w["value"] == "T")
        tests[w["test"]]["_exp"] = (w["expected_outcome"] == "T")
    assert len(tests) == 4
    for t in tests.values():
        assert t["_exp"] == ((t["A"] and t["B"]) or t["C"])


def test_C2_040(run):
    r = run("analyze", "(A and B) or C", "--format", "truth-csv")
    rows = list(csv.DictReader(io.StringIO(r.out)))
    assert len(rows) == 8
    assert (rows[0]["A"], rows[0]["B"], rows[0]["C"]) == ("T", "T", "T")
    for w in rows:
        a, b, c = (w[k] == "T" for k in "ABC")
        assert (w["outcome"] == "T") == ((a and b) or c)


def test_C2_041(run):
    r = run("analyze", "(A and B) or C", "--format", "json")
    assert isinstance(r.js, dict)


def test_C2_042(run, tmp_path):
    out = tmp_path / "relatorio.txt"
    r = run("analyze", "(A and B) or C", "-o", out)
    assert out.exists() and out.stat().st_size > 0
    assert "Suíte mínima" in out.read_text(encoding="utf-8")
    assert "Suíte mínima" not in r.out and "Pares de independência" not in r.out


# ================================================================ F: check
FULL = "test,input,value\nT1,A,T\nT1,B,T\nT1,C,F\nT2,A,F\nT2,B,T\nT2,C,F\nT3,A,T\nT3,B,F\nT3,C,F\nT4,A,T\nT4,B,F\nT4,C,T\n"


def test_C2_043(run, mkfile):
    f = mkfile("t.csv", FULL)
    r = run("check", "(A and B) or C", "--tests", f, "--format", "json")
    x = dec0(r.js)
    assert r.code == 0 and x["complete"] and x["conditionsDemonstrated"] == 3 == x["conditionsTotal"]


def test_C2_044(run, mkfile):
    f = mkfile("t.csv", "test,input,value\nT1,A,T\nT1,B,T\nT1,C,F\nT2,A,F\nT2,B,T\nT2,C,F\n")
    r = run("check", "(A and B) or C", "--tests", f, "--format", "json")
    x = dec0(r.js)
    dem = {c["condition"]: c["demonstrated"] for c in x["conditions"]}
    assert r.code == 2 and dem == {"A": True, "B": False, "C": False}


def test_C2_045(run, mkfile):
    f = mkfile("t.csv", "test,input,value,expected_outcome\nT1,A,T,F\nT1,B,T,F\nT1,C,F,F\nT2,A,F,F\nT2,B,T,F\nT2,C,F,F\n"
               "T3,A,T,F\nT3,B,F,F\nT3,C,F,F\nT4,A,T,T\nT4,B,F,T\nT4,C,T,T\n")
    r = run("check", "(A and B) or C", "--tests", f, "--format", "json")
    x = dec0(r.js)
    assert r.code == 2
    assert any("T1" in p for p in x["problems"])


GUARD_JSON = ('{"system":"s","inputs":[{"name":"the_system_mode","type":"enum","values":["idle","choice"]},'
              '{"name":"the_coin_sensor","type":"bool"}],"decisions":[{"id":"vm#1","requirement":"REQ-001",'
              '"guard":"the_system_mode = idle /\\\\ the_coin_sensor = true","actions":[]}]}')


def test_C2_046(run, mkfile):
    j = mkfile("d.json", GUARD_JSON)
    f = mkfile("t.csv", "decision,test,input,value,expected_outcome\nvm#1,T1,the_system_mode,idle,T\nvm#1,T1,the_coin_sensor,true,T\n"
               "vm#1,T2,the_system_mode,choice,F\nvm#1,T2,the_coin_sensor,true,F\nvm#1,T3,the_system_mode,idle,F\nvm#1,T3,the_coin_sensor,false,F\n")
    r = run("check", "--json", j, "--tests", f, "--format", "json")
    x = dec0(r.js)
    assert r.code == 0 and x["complete"] and x["conditionsDemonstrated"] == 2 and not x["problems"]


def test_C2_047(run, mkfile):
    f = mkfile("t.csv", "test,input\nT1,A\nT1,B\n")
    r = run("check", "(A and B) or C", "--tests", f)
    assert r.code == 1


# ================================================================ G: verify
def _vj(decs):
    return ('{"system":"s","inputs":[{"name":"sw","type":"enum","values":["on","off"]},'
            '{"name":"out","type":"enum","values":["lo","hi"]}],"decisions":[' + decs + ']}')


def _d(i, guard, val):
    return f'{{"id":"d{i}","requirement":"R{i}","guard":"{guard}","actions":["out := {val}"]}}'


def test_C2_049(run, mkfile):
    f = mkfile("c.json", _vj(_d(1, "sw = on", "lo") + "," + _d(2, "sw = on", "hi")))
    r = run("verify", "--json", f, "--format", "json", z3=True)
    assert len(r.js["conflicts"]) == 1 and r.code == 2


def test_C2_050(run, mkfile):
    f = mkfile("c.json", _vj(_d(1, "sw = on", "lo") + "," + _d(2, "sw = off", "hi")))
    r = run("verify", "--json", f, "--format", "json", z3=True)
    assert len(r.js["conflicts"]) == 0 and r.code == 0


def test_C2_051(run, mkfile):
    f = mkfile("c.json", _vj(_d(1, "sw = on", "lo") + "," + _d(2, "sw = on", "lo")))
    r = run("verify", "--json", f, "--format", "json", z3=True)
    assert len(r.js["conflicts"]) == 0 and r.code == 0


def test_C2_052(run, mkfile):
    f = mkfile("c.json", _vj(_d(1, "sw = on", "lo")))
    r = run("verify", "--json", f, "--context", "sw = on or sw = off", "--format", "json", z3=True)
    assert r.js["gaps"]["found"] is True and r.code == 2


def test_C2_053(run, mkfile):
    f = mkfile("c.json", _vj(_d(1, "sw = on", "lo") + "," + _d(2, "sw = off", "lo")))
    r = run("verify", "--json", f, "--context", "sw = on or sw = off", "--format", "json", z3=True)
    assert r.js["gaps"]["found"] is False and len(r.js["conflicts"]) == 0 and r.code == 0


# ================================================================ H: entradas invalidas
def test_C2_054(run):
    assert run("analyze", "A and").code == 1


def test_C2_055(run):
    assert run("analyze", "(A and B").code == 1


def test_C2_056(run, mkfile):
    f = mkfile("bad.mcdc", "REQ-001: A and B\nREQ-002: (A or\n")
    assert run("analyze", "-f", f).code == 1


def test_C2_057(run, mkfile):
    f = mkfile("bad.json", "{ isto nao e json")
    assert run("analyze", "--json", f).code == 1
