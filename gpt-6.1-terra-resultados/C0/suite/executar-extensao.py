import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
import xml.etree.ElementTree as ET

from importlib.machinery import SourceFileLoader


ROOT = Path(__file__).resolve().parent
baseline = SourceFileLoader("baseline", str(ROOT / "executar-baseline.py")).load_module()
EXEC = ROOT / "extension.exec"
RESULTS = ROOT / "extension-resultados.json"


def report(exec_file, prefix):
    output = ROOT / f"{prefix}-jacoco.xml"
    args = ["java", "-jar", str(baseline.CLI), "report", str(exec_file),
            "--classfiles", str(baseline.CLASSES), "--xml", str(output), "--name", prefix]
    proc = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode:
        raise RuntimeError(f"JaCoCo report falhou: {proc.stderr}")
    counter = next(x for x in ET.parse(output).getroot().findall("counter") if x.get("type") == "BRANCH")
    return {"comando": args, "stdout": proc.stdout, "stderr": proc.stderr,
            "cobertos": int(counter.get("covered")), "nao_cobertos": int(counter.get("missed"))}


def main():
    if any(p.exists() for p in (EXEC, RESULTS, ROOT / "combinado.exec")):
        raise RuntimeError("Resultados já existem; não sobrescrever.")
    environment = os.environ.copy()
    environment["PATH"] = str(ROOT / "z3-bin") + os.pathsep + environment.get("PATH", "")
    classpath = os.pathsep.join(map(str, [baseline.CLASSES, *baseline.JACKSON]))
    cases = json.loads((ROOT / "extension-oraculos.json").read_text(encoding="utf-8"))
    rows = []
    start = time.monotonic()
    for case in cases:
        converted = [str(ROOT / a[1:]) if a.startswith("@") else a for a in case["args"]]
        args = ["java", "-Dfile.encoding=UTF-8", f"-javaagent:{baseline.AGENT}=destfile={EXEC},append=true",
                "-cp", classpath, "io.github.rvdomingos.mcdc.cli.Main", *converted]
        row = {"id": case["id"], "oraculo": "CONFORME À DOCUMENTAÇÃO",
               "esperado": case["esperado"], "comando": args}
        try:
            proc = subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                                  errors="replace", timeout=120, env=environment)
            row.update(codigo=proc.returncode, stderr=proc.stderr,
                       stdout_sha256=hashlib.sha256(proc.stdout.encode("utf-8")).hexdigest().upper())
            if converted[0] != "check":
                row["stdout"] = proc.stdout
            if case.get("tipo") == "condicoes":
                if proc.returncode == 1:
                    row["observado"] = "expressão documentada recusada"
                else:
                    report_json = json.loads(proc.stdout)
                    row["observado"] = len(report_json["decisions"][0]["conditions"])
            else:
                row["observado"] = proc.returncode
            row["status"] = ("PASSOU" if row["observado"] == case["esperado"]
                             else "FALHOU — DIVERGÊNCIA DOCUMENTAÇÃO/SUT")
        except (OSError, subprocess.TimeoutExpired, ValueError, KeyError, IndexError) as exc:
            row.update(status="ERRO DE EXECUÇÃO", erro=f"{type(exc).__name__}: {exc}")
        rows.append(row)
    ext_report = report(EXEC, "extension")
    merged = ROOT / "combinado.exec"
    merge_args = ["java", "-jar", str(baseline.CLI), "merge", str(ROOT / "baseline.exec"),
                  str(EXEC), "--destfile", str(merged)]
    proc = subprocess.run(merge_args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode:
        raise RuntimeError(f"JaCoCo merge falhou: {proc.stderr}")
    combined_report = report(merged, "combinado")
    result = {"duracao_segundos": time.monotonic() - start, "casos": rows,
              "jacoco_extensao": ext_report, "jacoco_combinado": combined_report,
              "comando_merge": merge_args, "stdout_merge": proc.stdout, "stderr_merge": proc.stderr}
    RESULTS.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    statuses = {}
    for row in rows:
        statuses[row["status"]] = statuses.get(row["status"], 0) + 1
    print(json.dumps({"estados": statuses, "extensao": ext_report, "combinado": combined_report},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
