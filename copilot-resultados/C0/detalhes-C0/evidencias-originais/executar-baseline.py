import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
HOME = Path.home()
MODULES = ["mcdc-core", "mcdc-requirements", "mcdc-z3", "mcdc-cli"]
JACKSON = [
    HOME / ".m2" / "repository" / "com" / "fasterxml" / "jackson" / "core" / name / "2.17.2" / f"{name}-2.17.2.jar"
    for name in ("jackson-annotations", "jackson-core", "jackson-databind")
]
JACOCO = HOME / ".m2" / "repository" / "org" / "jacoco"
AGENT = JACOCO / "org.jacoco.agent" / "0.8.16" / "org.jacoco.agent-0.8.16-runtime.jar"
CLI = JACOCO / "org.jacoco.cli" / "0.8.16" / "org.jacoco.cli-0.8.16-nodeps.jar"
CLASSES = ROOT / "classes"
EXEC = ROOT / "baseline.exec"
XML = ROOT / "baseline-jacoco.xml"
RESULTS = ROOT / "baseline-resultados.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def compile_sources():
    sources = sorted(p for module in MODULES for p in (REPO / module / "src" / "main" / "java").rglob("*.java"))
    if not sources or not all(p.is_file() for p in [*JACKSON, AGENT, CLI]):
        raise RuntimeError("Fontes ou dependências ausentes; não há execução válida.")
    CLASSES.mkdir(exist_ok=True)
    classpath = os.pathsep.join(map(str, JACKSON))
    args = ["javac", "-encoding", "UTF-8", "-d", str(CLASSES), "-cp", classpath, *map(str, sources)]
    result = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    (ROOT / "compilacao.json").write_text(json.dumps({
        "comando": args, "codigo": result.returncode, "stdout": result.stdout, "stderr": result.stderr,
        "fontes": {str(p.relative_to(REPO)): sha(p) for p in sources},
        "dependencias": {str(p): sha(p) for p in [*JACKSON, AGENT, CLI]},
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if result.returncode != 0:
        raise RuntimeError("Compilação falhou; consultar compilacao.json")


def run_cases():
    if EXEC.exists() or RESULTS.exists() or XML.exists():
        raise RuntimeError("Resultados baseline já existem; não sobrescrever.")
    cases = json.loads((ROOT / "oraculos.json").read_text(encoding="utf-8"))
    classpath = os.pathsep.join(map(str, [CLASSES, *JACKSON]))
    results = []
    started = time.monotonic()
    for case in cases:
        args = ["java", "-Dfile.encoding=UTF-8", f"-javaagent:{AGENT}=destfile={EXEC},append=true",
                "-cp", classpath, "io.github.rvdomingos.mcdc.cli.Main", "analyze",
                case["expressao"], *case["opcoes"]]
        if case["tipo"] == "linha_tabela":
            args += ["--format", "truth-csv"]
        row = {"id": case["id"], "oraculo": case["oraculo"], "esperado": case["esperado"], "comando": args}
        try:
            proc = subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                                  errors="replace", timeout=30)
            row.update(codigo=proc.returncode, stdout=proc.stdout, stderr=proc.stderr)
            if case["tipo"] == "codigo_saida":
                row["observado"] = proc.returncode
                passed = proc.returncode == case["esperado"]
            elif proc.returncode == 1:
                row["observado"] = "entrada documentada recusada"
                passed = False
            else:
                reader = csv.DictReader(proc.stdout.splitlines())
                required = set(case["entradas"]) | {"outcome"}
                if reader.fieldnames is None or not required.issubset(reader.fieldnames):
                    raise ValueError(f"CSV não interpretável: cabeçalho {reader.fieldnames}")
                matches = [r for r in reader if all(r[k] == ("T" if v else "F")
                                                    for k, v in case["entradas"].items())]
                if len(matches) != 1:
                    row["observado"] = {"linhas_encontradas": len(matches)}
                    passed = False
                elif matches[0]["outcome"] not in ("T", "F"):
                    raise ValueError("Valor CSV de resultado não interpretável")
                else:
                    row["observado"] = matches[0]["outcome"] == "T"
                    passed = row["observado"] == case["esperado"]
            row["status"] = "PASSOU" if passed else "FALHOU — DIVERGÊNCIA DOCUMENTAÇÃO/SUT"
        except (subprocess.TimeoutExpired, OSError, ValueError, csv.Error) as exc:
            row.update(status="ERRO DE EXECUÇÃO", erro=f"{type(exc).__name__}: {exc}")
        results.append(row)
    report_args = ["java", "-jar", str(CLI), "report", str(EXEC), "--classfiles", str(CLASSES),
                   "--xml", str(XML), "--name", "C0 baseline"]
    report = subprocess.run(report_args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if report.returncode != 0:
        raise RuntimeError(f"JaCoCo report falhou: {report.stderr}")
    document = ET.parse(XML).getroot()
    counter = next(x for x in document.findall("counter") if x.attrib["type"] == "BRANCH")
    missed, covered = int(counter.attrib["missed"]), int(counter.attrib["covered"])
    data = {"duracao_segundos": time.monotonic() - started, "casos": results,
            "jacoco": {"versao": "0.8.16", "comando": report_args, "stdout": report.stdout,
                       "stderr": report.stderr, "branches_cobertos": covered, "branches_nao_cobertos": missed,
                       "branches_total": covered + missed}}
    RESULTS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    statuses = {}
    for row in results:
        statuses[row["status"]] = statuses.get(row["status"], 0) + 1
    print(json.dumps({"estados": statuses, "branches": data["jacoco"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if sys.argv[1:] == ["--compile"]:
        compile_sources()
    elif sys.argv[1:] == ["--run"]:
        run_cases()
    else:
        raise SystemExit("Use --compile ou --run")
