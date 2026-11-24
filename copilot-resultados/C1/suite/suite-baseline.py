"""C1: executa os oráculos previamente congelados contra a CLI Java real."""
import csv
import io
import itertools
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
CLASSES = ROOT / "classes"
EVIDENCE = ROOT / "baseline"
M2 = Path.home() / ".m2" / "repository"
JARS = [
    M2 / "com/fasterxml/jackson/core/jackson-annotations/2.17.2/jackson-annotations-2.17.2.jar",
    M2 / "com/fasterxml/jackson/core/jackson-core/2.17.2/jackson-core-2.17.2.jar",
    M2 / "com/fasterxml/jackson/core/jackson-databind/2.17.2/jackson-databind-2.17.2.jar",
]
AGENT = M2 / "org/jacoco/org.jacoco.agent/0.8.16/org.jacoco.agent-0.8.16-runtime.jar"
Z3BIN = ROOT.parent / "detalhes-C1" / "ferramentas" / "z3-4.13.4-x64-win" / "bin"
JAVA = Path(os.environ["JAVA_HOME"]) / "bin" / "java.exe" if os.environ.get("JAVA_HOME") else Path(
    r"C:\Program Files\Common Files\Oracle\Java\javapath\java.exe"
)
JAVAC = JAVA.with_name("javac.exe")
CP = os.pathsep.join(map(str, [CLASSES, *JARS]))
MAIN = "io.github.rvdomingos.mcdc.cli.Main"
RESULTS = []


def build():
    CLASSES.mkdir(exist_ok=True)
    roots = [REPO / name / "src" / "main" / "java" for name in
             ("mcdc-core", "mcdc-requirements", "mcdc-z3", "mcdc-cli")]
    sources = sorted(str(path) for root in roots for path in root.rglob("*.java"))
    if not sources or not all(path.exists() for path in [*JARS, AGENT, JAVA, JAVAC]):
        raise RuntimeError("Fontes, Java, Jackson ou agente JaCoCo ausentes")
    command = [str(JAVAC), "-encoding", "UTF-8", "--release", "21", "-cp",
               os.pathsep.join(map(str, JARS)), "-d", str(CLASSES), *sources]
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
    (ROOT / "compilacao.json").write_text(json.dumps({
        "comando": command, "codigo": result.returncode, "stdout": result.stdout, "stderr": result.stderr
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    if result.returncode:
        raise RuntimeError("Compilação falhou; consultar compilacao.json")


def invoke(case, args, no_z3=False):
    env = os.environ.copy()
    env["PATH"] = str(Path(os.environ["SystemRoot"]) / "System32") if no_z3 else str(Z3BIN) + os.pathsep + env["PATH"]
    command = [str(JAVA), "-Dfile.encoding=UTF-8",
               f"-javaagent:{AGENT}=destfile={EVIDENCE / (case + '.exec')},append=false",
               "-cp", CP, MAIN, *map(str, args)]
    start = time.monotonic()
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace",
                            env=env, timeout=120)
    stdout = result.stdout
    if args[0] == "check":
        try:
            data = json.loads(stdout)
            for decision in data.get("decisions", []):
                for key in ("outcomesCovered", "outcomesTotal", "outcomePercentage"):
                    decision.pop(key, None)
            stdout = json.dumps(data, ensure_ascii=False, indent=2)
        except json.JSONDecodeError:
            stdout = "\n".join(line for line in stdout.splitlines()
                               if "Resultados de condição demonstrados:" not in line)
    record = {"id": case, "argumentos": list(map(str, args)), "comando": command,
              "codigo": result.returncode, "stdout": stdout, "stderr": result.stderr,
              "duracao_segundos": round(time.monotonic() - start, 3)}
    (EVIDENCE / f"{case}.json").write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    return record


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def document(result):
    try:
        return json.loads(result["stdout"])
    except json.JSONDecodeError as error:
        raise AssertionError(f"relatório JSON inválido: {error}") from error


def truth(result, names, expected):
    require(result["codigo"] == 0, f"código esperado 0, obtido {result['codigo']}: {result['stderr']}")
    d = document(result)["decisions"][0]
    rows = d["truthTable"]
    actual = {tuple(row["values"][name] for name in names): row["outcome"] for row in rows}
    vectors = list(itertools.product((False, True), repeat=len(names)))
    require(len(rows) == len(vectors) and len(actual) == len(vectors), "tabela não contém todos os vetores distintos")
    for vector in vectors:
        require(actual[vector] == expected(*vector), f"resultado incorreto em {vector}")
    return d


def pairs(d, names, unique=False):
    table = {row["vector"]: row for row in d["truthTable"]}
    suite = {row["vector"] for row in d["minimalSuite"]}
    require(len(d["chosenPairs"]) == len(names), "nem todas as condições têm par demonstrado")
    for name in names:
        pair = d["chosenPairs"][name]
        a, b = table[pair["whenTrue"]], table[pair["whenFalse"]]
        require(pair["whenTrue"] in suite and pair["whenFalse"] in suite, f"par de {name} fora da suíte")
        require(a["values"][name] != b["values"][name] and a["outcome"] != b["outcome"],
                f"par de {name} não altera condição e decisão")
        if unique:
            require(all(a["values"][n] == b["values"][n] for n in names if n != name),
                    f"par de {name} não é causa única")


def run_case(case, args, check, no_z3=False):
    try:
        result = invoke(case, args, no_z3=no_z3)
        check(result)
        status, message = "PASSOU", ""
    except AssertionError as error:
        status, message = "FALHOU — DIVERGÊNCIA DOCUMENTAÇÃO/SUT", str(error)
    except (OSError, KeyError, TypeError, ValueError, subprocess.TimeoutExpired) as error:
        status, message = "ERRO DE EXECUÇÃO", f"{type(error).__name__}: {error}"
    RESULTS.append({"id": case, "oraculo": "CONFORME À DOCUMENTAÇÃO", "resultado": status, "mensagem": message})
    print(case, status, message, flush=True)


def code(n):
    return lambda r: require(r["codigo"] == n, f"código esperado {n}, obtido {r['codigo']}: {r['stderr']}")


def main():
    EVIDENCE.mkdir(exist_ok=True)
    build()
    one = lambda a: a
    neg = lambda a: not a
    both = lambda a, b: a and b
    either = lambda a, b: a or b
    complex_expr = lambda a, b, c: (a and b) or c
    expressions = [
        ("B01", "A", ["A"], one), ("B02", "not A", ["A"], neg),
        ("B03", "A and B", ["A", "B"], both), ("B04", "A or B", ["A", "B"], either),
        ("B05", "(A and B) or C", ["A", "B", "C"], complex_expr),
        ("B06", "(A and B) or C", ["A", "B", "C"], complex_expr),
        ("B07", "A && B", ["A", "B"], both), ("B08", r"A /\ B", ["A", "B"], both),
        ("B09", "A || B", ["A", "B"], either), ("B10", r"A \/ B", ["A", "B"], either),
        ("B11", "! A", ["A"], neg), ("B12", "not A", ["A"], neg),
    ]
    for case, expr, names, expected in expressions:
        args = ["analyze", expr, "--format", "json"]
        if case == "B06":
            args.append("--unique-cause")
        def verify(r, n=names, exp=expected, c=case):
            d = truth(r, n, exp)
            if c in ("B01", "B02", "B03", "B04", "B05", "B06"):
                pairs(d, n, c == "B06")
        run_case(case, args, verify)
    run_case("B13", ["analyze", "A and"], code(1))
    run_case("B14", ["analyze", "A and B", "--format", "json"],
             lambda r: truth(r, ["A", "B"], both))

    def csv_suite(r):
        code(0)(r)
        rows = list(csv.DictReader(io.StringIO(r["stdout"])))
        require(bool(rows), "suíte CSV vazia")
        by_test = {}
        for row in rows:
            by_test.setdefault(row["test"], []).append(row)
        require(all({x["input"] for x in group} == {"A", "B"} and len(group) == 2
                    for group in by_test.values()), "CSV não tem uma linha por teste e entrada")
    run_case("B15", ["analyze", "A and B", "--format", "csv"], csv_suite)

    def csv_truth(r):
        code(0)(r)
        rows = list(csv.DictReader(io.StringIO(r["stdout"])))
        require(len(rows) == 4, "truth-csv não tem quatro linhas")
        values = {(x["A"], x["B"]): x["outcome"] for x in rows}
        require(values == {("F", "F"): "F", ("F", "T"): "F", ("T", "F"): "F", ("T", "T"): "T"},
                "truth-csv tem valores incorretos")
    run_case("B16", ["analyze", "A and B", "--format", "truth-csv"], csv_truth)

    output = EVIDENCE / "B17-report.json"
    def file_report(r):
        code(0)(r)
        require(output.is_file(), "arquivo não criado")
        data = json.loads(output.read_text(encoding="utf-8"))
        require(bool(data["decisions"]), "arquivo não contém decisão")
        require('"decisions"' not in r["stdout"], "relatório integral também impresso")
    run_case("B17", ["analyze", "A and B", "--format", "json", "-o", output], file_report)

    def two_decisions(r):
        code(0)(r)
        require({d["id"] for d in document(r)["decisions"]} == {"R1", "R2"}, "decisões do arquivo ausentes")
    run_case("B18", ["analyze", "-f", ROOT / "entrada.mcdc", "--format", "json"], two_decisions)

    for case, fixture, expected in (("B19", "check-ok.csv", 0), ("B20", "check-divergente.csv", 2),
                                    ("B21", "check-incompleto.csv", 2)):
        run_case(case, ["check", "A", "--tests", ROOT / fixture, "--format", "json"], code(expected))

    def constraint(r):
        code(2)(r)
        rows = document(r)["decisions"][0]["truthTable"]
        data = {(x["values"]["A"], x["values"]["B"]): x["feasible"] for x in rows}
        require(data[(True, False)] is False and data[(False, False)] is True, "restrição não aplicada")
    run_case("B22", ["analyze", "A and B", "--constraint", "not A or B", "--format", "json"], constraint)

    def boundary(r):
        d = document(r)["decisions"][0]
        rows = d["truthTable"]
        require(any(not row["feasible"] and row["values"]["speed > 100"] and
                    not row["values"]["speed > 50"] for row in rows), "combinação impossível não descartada")
        values = {str(item["assignment"].get("speed")) for item in d.get("boundaryTests", [])}
        require({"100", "101"} <= values, f"fronteiras 100 e 101 ausentes: {values}")
    run_case("B23", ["analyze", "speed > 100 or speed > 50", "--z3", "--boundary", "--format", "json"], boundary)

    def exact(r):
        d = truth(r, ["A", "B", "C"], complex_expr)
        pairs(d, ["A", "B", "C"])
        require(len(d["minimalSuite"]) == 4, "suíte exata não tem quatro testes")
    run_case("B24", ["analyze", "(A and B) or C", "--exact", "--format", "json"], exact)

    def direct(r):
        code(0)(r)
        d = document(r)["decisions"][0]
        require(len(d["chosenPairs"]) == 3, "modo direto não demonstra três condições")
        for row in d["minimalSuite"]:
            v = row["values"]
            require(row["outcome"] == complex_expr(v["A"], v["B"], v["C"]), "resultado direto incorreto")
    run_case("B25", ["analyze", "(A and B) or C", "--direct", "--format", "json"], direct)

    def conflict(r):
        code(2)(r)
        require(bool(document(r)["conflicts"]), "conflito não relatado")
    run_case("B26", ["verify", "--json", ROOT / "conflito.json", "--format", "json"], conflict)

    def gap(r):
        code(2)(r)
        require(document(r)["gaps"]["found"], "lacuna não relatada")
    run_case("B27", ["verify", "--json", ROOT / "lacuna.json", "--context", "not A", "--format", "json"], gap)

    def repeated(r):
        d = document(r)["decisions"][0]
        require(len(d["inputs"]) == 3 and len(d["conditions"]) == 4, "entradas ou ocorrências incorretas")
    run_case("B28", ["analyze", "(A and B) or (not A and C)", "--format", "json"], repeated)

    def reason(r, condition, expected):
        code(2)(r)
        uncovered = document(r)["decisions"][0]["uncovered"]
        require(any(x["condition"] == condition and expected in x["reason"].upper() for x in uncovered),
                f"{condition} não classificada como {expected}")
    run_case("B29", ["analyze", "A or (A and B)", "--format", "json"],
             lambda r: reason(r, "B", "REDUNDANT"))
    run_case("B30", ["analyze", "A and B", "--constraint", "A", "--format", "json"],
             lambda r: reason(r, "A", "INFEASIBLE"))
    run_case("B31", ["analyze", "speed > 100", "--z3", "--format", "json"],
             lambda r: require("z3" in (r["stdout"] + r["stderr"]).lower() and
                               any(x in (r["stdout"] + r["stderr"]).lower()
                                   for x in ("não encontrado", "not found", "não instalado", "unavailable")),
                               "aviso de ausência do Z3 não identificado"), no_z3=True)
    (EVIDENCE / "resultados.json").write_text(json.dumps(RESULTS, ensure_ascii=False, indent=2), encoding="utf-8")
    if any(item["resultado"].startswith("ERRO") for item in RESULTS):
        sys.exit(2)
    if any(item["resultado"].startswith("FALHOU") for item in RESULTS):
        sys.exit(1)


if __name__ == "__main__":
    main()
