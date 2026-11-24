import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
from importlib.machinery import SourceFileLoader

ROOT = Path(__file__).resolve().parent
baseline = SourceFileLoader("baseline2", str(ROOT / "executar-baseline.py")).load_module()
extension = SourceFileLoader("extension", str(ROOT / "executar-extensao.py")).load_module()
EXEC = ROOT / "extension2.exec"
RESULTS = ROOT / "extension2-resultados.json"


def main():
    if any(p.exists() for p in (EXEC, RESULTS, ROOT / "combinado2.exec")):
        raise RuntimeError("Resultados já existem; não sobrescrever.")
    env = os.environ.copy()
    env["PATH"] = str(ROOT / "z3-bin") + os.pathsep + env.get("PATH", "")
    cp = os.pathsep.join(map(str, [baseline.CLASSES, *baseline.JACKSON]))
    cases = json.loads((ROOT / "extension2-oraculos.json").read_text(encoding="utf-8"))
    rows = []
    start = time.monotonic()
    for case in cases:
        if case.get("tipo") == "fronteira":
            cli = ["analyze", case["expressao"], "--z3", "--boundary", "--format", "json"]
        else:
            cli = ["check", case["expressao"], "--tests", str(ROOT / case["arquivo"]), "--format", "json"]
        args = ["java", "-Dfile.encoding=UTF-8", f"-javaagent:{baseline.AGENT}=destfile={EXEC},append=true",
                "-cp", cp, "io.github.rvdomingos.mcdc.cli.Main", *cli]
        row = {"id": case["id"], "oraculo": case["oraculo"], "esperado": case.get("resultados", case.get("esperado")),
               "comando": args}
        try:
            proc = subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                                  errors="replace", timeout=120, env=env)
            row.update(codigo=proc.returncode, stderr=proc.stderr,
                       stdout_sha256=hashlib.sha256(proc.stdout.encode("utf-8")).hexdigest().upper())
            if proc.returncode == 1:
                row["observado"] = "entrada documentada recusada"
                passed = False
            else:
                document = json.loads(proc.stdout)
                decision = document["decisions"][0]
                if case.get("tipo") == "fronteira":
                    row["stdout"] = proc.stdout
                    observed = sorted({int(item["assignment"]["x"]) for item in decision["boundaryTests"]})
                    row["observado"] = observed
                    passed = proc.returncode == 0 and set(case["esperado"]).issubset(observed)
                else:
                    observed = {test["test"]: test["outcome"] for test in decision["tests"]}
                    row["observado"] = observed
                    passed = proc.returncode == case["codigo_esperado"] and observed == case["resultados"]
            row["status"] = "PASSOU" if passed else "FALHOU — DIVERGÊNCIA DOCUMENTAÇÃO/SUT"
        except (OSError, subprocess.TimeoutExpired, ValueError, KeyError, IndexError) as exc:
            row.update(status="ERRO DE EXECUÇÃO", erro=f"{type(exc).__name__}: {exc}")
        rows.append(row)
    ext = extension.report(EXEC, "extension2")
    merged = ROOT / "combinado2.exec"
    merge_args = ["java", "-jar", str(baseline.CLI), "merge", str(ROOT / "combinado.exec"),
                  str(EXEC), "--destfile", str(merged)]
    proc = subprocess.run(merge_args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode:
        raise RuntimeError(f"JaCoCo merge falhou: {proc.stderr}")
    combined = extension.report(merged, "combinado2")
    data = {"duracao_segundos": time.monotonic() - start, "casos": rows,
            "jacoco_extensao": ext, "jacoco_combinado": combined,
            "comando_merge": merge_args, "stdout_merge": proc.stdout, "stderr_merge": proc.stderr}
    RESULTS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    counts = {}
    for row in rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    print(json.dumps({"estados": counts, "extensao": ext, "combinado": combined},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
