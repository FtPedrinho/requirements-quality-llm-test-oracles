"""Rodada coverage-informed: asserções documentais congeladas antes de executar."""
import csv
import importlib.util
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("baseline_harness", ROOT / "suite-baseline.py")
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
b.EVIDENCE = ROOT / "extensao-v2"
b.EVIDENCE.mkdir(exist_ok=True)
b.RESULTS = []


def missing_z3():
    case = "E01"
    env = os.environ.copy()
    env["PATH"] = str(Path(os.environ["SystemRoot"]) / "System32")
    args = ["analyze", "speed > 100", "--z3", "--format", "json"]
    command = [str(b.JAVA), "-Dfile.encoding=UTF-8",
               f"-javaagent:{b.AGENT}=destfile={b.EVIDENCE / (case + '.exec')},append=false",
               "-cp", b.CP, b.MAIN, *args]
    try:
        p = subprocess.run(command, env=env, capture_output=True, timeout=120)
        stderr = p.stderr.decode("cp1252")
        stdout = p.stdout.decode("utf-8")
        evidence = {"id": case, "comando": command, "codigo": p.returncode,
                    "stdout": stdout, "stderr": stderr, "stderr_hex": p.stderr.hex(),
                    "codificacao_stderr": "cp1252"}
        (b.EVIDENCE / f"{case}.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
        b.require("z3" in stderr.lower() and "não encontrado" in stderr.lower(),
                  "aviso de ausência do Z3 não identificado")
        status, message = "PASSOU", ""
    except AssertionError as error:
        status, message = "FALHOU — DIVERGÊNCIA DOCUMENTAÇÃO/SUT", str(error)
    except (OSError, UnicodeDecodeError, subprocess.TimeoutExpired) as error:
        status, message = "ERRO DE EXECUÇÃO", f"{type(error).__name__}: {error}"
    b.RESULTS.append({"id": case, "oraculo": "CONFORME À DOCUMENTAÇÃO", "resultado": status, "mensagem": message})
    print(case, status, message, flush=True)


def main():
    missing_z3()
    def text_report(r):
        b.code(0)(r)
        s = r["stdout"].lower()
        b.require("tabela" in s and "pares" in s and "a and b" in s, "componentes textuais ausentes")
    b.run_case("E02", ["analyze", "A and B"], text_report)
    operators = [
        ("=", 0, 1, lambda v: v == 0), ("==", 0, 1, lambda v: v == 0),
        ("!=", 1, 0, lambda v: v != 0), ("<", -1, 0, lambda v: v < 0),
        ("<=", 0, 1, lambda v: v <= 0), (">", 1, 0, lambda v: v > 0),
        (">=", 0, -1, lambda v: v >= 0),
    ]
    for i, (op, yes, no, pred) in enumerate(operators):
        case = f"E{i + 3:02d}"
        path = b.EVIDENCE / f"{case}-entrada.csv"
        with path.open("w", encoding="utf-8", newline="") as out:
            writer = csv.writer(out)
            writer.writerows([["test", "input", "value", "expected_outcome"],
                              ["T", "x", yes, "T"], ["F", "x", no, "F"]])
        b.run_case(case, ["check", f"x {op} 0", "--tests", path, "--format", "json"], b.code(0))
    for i, (op, yes, no, pred) in enumerate(operators):
        case = f"E{i + 10:02d}"
        def verify(r, p=pred):
            b.code(0)(r)
            rows = b.document(r)["decisions"][0]["truthTable"]
            b.require(len(rows) == 2 and all(row["feasible"] for row in rows), "linhas verdadeira e falsa não viáveis")
            for row in rows:
                val = int(row["assignment"]["x"])
                b.require(p(val) == row["outcome"], "atribuição concreta não realiza resultado")
        b.run_case(case, ["analyze", f"x {op} 0", "--z3", "--format", "json"], verify)

    optional = b.EVIDENCE / "E17-entrada.csv"
    optional.write_text("test,input,value\nT1,A,F\nT2,A,T\n", encoding="utf-8")
    b.run_case("E17", ["check", "A", "--tests", optional], b.code(0))
    same = {"system": "C1", "inputs": [{"name": "A", "type": "bool"}],
            "decisions": [{"id": "R1", "guard": "A", "actions": ["x := 0"]},
                          {"id": "R2", "guard": "A", "actions": ["x := 0"]}]}
    path = b.EVIDENCE / "E18-entrada.json"
    path.write_text(json.dumps(same), encoding="utf-8")
    b.run_case("E18", ["verify", "--json", path], b.code(0))
    tautology = {"system": "C1", "inputs": [{"name": "A", "type": "bool"}],
                 "decisions": [{"id": "R1", "guard": "A or not A", "actions": ["x := 0"]}]}
    path = b.EVIDENCE / "E19-entrada.json"
    path.write_text(json.dumps(tautology), encoding="utf-8")
    b.run_case("E19", ["verify", "--json", path, "--context", "A or not A", "--format", "json"], b.code(0))
    (b.EVIDENCE / "resultados.json").write_text(json.dumps(b.RESULTS, ensure_ascii=False, indent=2), encoding="utf-8")
    if any(item["resultado"].startswith("ERRO") for item in b.RESULTS):
        raise SystemExit(2)
    if any(item["resultado"].startswith("FALHOU") for item in b.RESULTS):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
