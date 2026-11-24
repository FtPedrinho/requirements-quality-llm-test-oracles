import importlib.util
import json
from pathlib import Path
import subprocess
import time


ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("suite_baseline", ROOT / "executar-suite.py")
suite = importlib.util.module_from_spec(spec)
spec.loader.exec_module(suite)
tables = {c["id"]: c for c in json.loads((ROOT / "oraculos.json").read_text(encoding="utf-8"))}
integration = {c["id"]: c for c in json.loads((ROOT / "oraculos-integracao.json").read_text(encoding="utf-8"))}
case_dir = ROOT / "evidencias" / "F03-R2"
case_dir.mkdir(exist_ok=False)
exec_path = ROOT / "cobertura" / "F03-R2.exec"
command = [
    "java", f"-javaagent:{suite.AGENT}=destfile={exec_path},append=false",
    "-cp", suite.CLASSPATH, suite.MAIN, "analyze",
    integration["F03"]["entrada"]["argumentos"][1], "-o", str(case_dir / "relatorio.txt"),
]
result = {
    "id": "F03", "rodada": "repeticao-tecnica-R2",
    "classificacao_oraculo": integration["F03"]["classificacao"],
    "comando": command, "status": None, "detalhe": None,
    "codigo_saida": None, "duracao_segundos": None,
}
started = time.perf_counter()
try:
    process = subprocess.run(command, cwd=case_dir, capture_output=True, timeout=60)
    (case_dir / "stdout.bin").write_bytes(process.stdout)
    (case_dir / "stderr.bin").write_bytes(process.stderr)
    stdout = process.stdout.decode("cp1252")
    stderr = process.stderr.decode("cp1252")
    (case_dir / "stdout.txt").write_text(stdout, encoding="utf-8")
    (case_dir / "stderr.txt").write_text(stderr, encoding="utf-8")
    result["codigo_saida"] = process.returncode
    infrastructure = ("Could not find or load main class", "NoClassDefFoundError",
                      "Could not create the Java Virtual Machine", "agent library failed")
    if any(message in stderr for message in infrastructure):
        result["status"] = "ERRO DE EXECUÇÃO"
        result["detalhe"] = stderr
    else:
        try:
            suite.check_case("F03", stdout, case_dir, tables, integration)
            result["status"] = "PASSOU"
        except AssertionError as exc:
            result["status"] = "FALHOU — DIVERGÊNCIA DOCUMENTAÇÃO/SUT"
            result["detalhe"] = str(exc)
except (FileNotFoundError, subprocess.TimeoutExpired, UnicodeDecodeError) as exc:
    result["status"] = "ERRO DE EXECUÇÃO"
    result["detalhe"] = str(exc)
result["duracao_segundos"] = round(time.perf_counter() - started, 6)
(case_dir / "resultado.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(result["id"], result["rodada"], result["status"], result["detalhe"] or "")
if result["status"] != "PASSOU":
    raise SystemExit(1)
