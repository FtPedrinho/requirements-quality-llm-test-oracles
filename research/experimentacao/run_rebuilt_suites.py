import csv
import json
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
Z3_BIN = Path(r"C:\Users\User\.copilot\session-state\8457bad6-f839-4d1b-96a8-6cea1a9c9dea\files\tools\z3-4.15.4-x64-win\bin")
JAVA = "java"
CLI_CLASSES = ROOT / "mcdc-cli" / "target" / "classes"
CLASSPATH_FILE = ROOT / "mcdc-cli" / "target" / "classpath.txt"

if not CLASSPATH_FILE.exists():
    raise RuntimeExit("O classpath não foi criado: compile o projeto Maven.")


class RuntimeExit(RuntimeError):
    pass


def run_mcdc(args, z3=True):
    env = os.environ.copy()
    if z3:
        env["PATH"] = str(Z3_BIN) + ";" + env.get("PATH", "")
    cp = str(CLI_CLASSES) + ";" + CLASSPATH_FILE.read_text(encoding="utf-8")
    result = subprocess.run(
        [JAVA, "-cp", cp, "io.github.rvdomingos.mcdc.cli.Main", *args],
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )
    return {
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def temp_file(suffix, content):
    handle = tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False, encoding="utf-8")
    handle.write(content)
    handle.close()
    return Path(handle.name)


def main():
    cases = []
    valid_mcdc_file = temp_file(".mcdc", "REQ-001: (A and B) or C\n")
    empty_mcdc_file = temp_file(".mcdc", "# vazio\n")
    conflict_json = temp_file(".json", r"""
{"system":"s","decisions":[
 {"id":"s#1","requirement":"REQ1","guard":"mode = choice /\\ timer <= 30","actions":["mode := weak"]},
 {"id":"s#2","requirement":"REQ2","guard":"mode = choice /\\ timer >= 30","actions":["mode := strong"]}
]}
""")
    gap_json = temp_file(".json", """
{"system":"s","decisions":[
 {"id":"s#1","requirement":"REQ1","guard":"mode = idle","actions":["mode := weak"]}
]}
""")
    invalid_csv = temp_file(".csv", "test,input\nT1,A\n")

    def add(behavior, name, args, expected_exit, z3=True, contains=None):
        execution = run_mcdc(args, z3=z3)
        passed = execution["exit_code"] == expected_exit
        if contains:
            passed = passed and contains in (execution["stdout"] + execution["stderr"])
        cases.append({
            "experiment": "EXP0/EXP1-SUT",
            "behavior_id": behavior,
            "test_id": name,
            "args": " ".join(args),
            "expected_exit": expected_exit,
            "actual_exit": execution["exit_code"],
            "passed": passed,
            "contains": contains or "",
            "stdout": execution["stdout"].strip(),
            "stderr": execution["stderr"].strip(),
        })

    add("B004", "no-command", [], 1, contains="Uso:")
    add("B006", "unknown-option", ["analyze", "(A and B)", "--invalida"], 1)
    add("B011", "invalid-expression", ["analyze", "A and"], 1)
    add("B012", "mcdc-file", ["analyze", "-f", str(valid_mcdc_file), "--format", "json"], 0)
    add("B013", "empty-mcdc", ["analyze", "-f", str(empty_mcdc_file)], 1)
    add("B015", "json-no-decisions", ["analyze", "--json", str(temp_file(".json", '{"system":"s","decisions":[]}'))], 1)
    add("B017", "invalid-csv", ["check", "A and B", "--tests", str(invalid_csv)], 1)
    add("B018", "truth-table", ["analyze", "(A and B) or C"], 0)
    add("B020", "masking-default", ["analyze", "(A and B) or C"], 0)
    add("B021", "unique-cause", ["analyze", "(A and B) or C", "--unique-cause"], 0)
    add("B023", "greedy-suite", ["analyze", "((E or D) and (not A or D)) or B"], 0)
    add("B024", "exact-suite", ["analyze", "((E or D) and (not A or D)) or B", "--exact"], 0)
    add("B025", "direct-mode", ["analyze", "A and B", "--direct"], 0)
    add("B026", "boundary", ["analyze", "speed > 100 or (speed > 50 and rain)", "--z3", "--boundary"], 0)
    add("B027", "mutation", ["analyze", "A and (B or C)", "--mutation", "--format", "json"], 0)
    add("B028", "verify-conflict", ["verify", "--json", str(conflict_json), "--format", "text"], 2)
    add("B029", "verify-gap", ["verify", "--json", str(gap_json), "--context", "mode = choice", "--format", "text"], 2)
    add("B030", "json-report", ["analyze", "(A and B) or C", "--format", "json"], 0)
    add("B031", "csv-report", ["analyze", "(A and B) or C", "--format", "csv"], 0)
    add("B032", "truth-csv-report", ["analyze", "(A and B) or C", "--format", "truth-csv"], 0)
    add("B034", "z3-unavailable", ["analyze", "(A and B) or C", "--z3"], 1, z3=False)

    out_root = ROOT / "research" / "experimentacao"
    for exp in ("experimentacao-0", "experimentacao-1"):
        out = out_root / exp / "test-suites"
        out.mkdir(parents=True, exist_ok=True)
        exp_cases = [dict(case) for case in cases]
        for case in exp_cases:
            case["experiment"] = exp
        with (out / "real-sut-suite-results.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(exp_cases[0].keys()))
            writer.writeheader()
            writer.writerows(exp_cases)

    print(json.dumps({
        "cases": len(cases),
        "passed": sum(case["passed"] for case in cases),
        "failed": sum(not case["passed"] for case in cases),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
