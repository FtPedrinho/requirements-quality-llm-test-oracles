import importlib.util
import json
from pathlib import Path
import re
import subprocess
import time


ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("suite_baseline", ROOT / "executar-suite.py")
suite = importlib.util.module_from_spec(spec)
spec.loader.exec_module(suite)
tables = {c["id"]: c for c in json.loads((ROOT / "oraculos.json").read_text(encoding="utf-8"))}
integration = {c["id"]: c for c in json.loads((ROOT / "oraculos-integracao.json").read_text(encoding="utf-8"))}


def text_table(text, oracle):
    lines = text.splitlines()
    header = next((re.fullmatch(r"Vetor\s+(.*?)\s*\|\s*D\s*", line) for line in lines if line.startswith("Vetor")), None)
    if header is None:
        suite.fail("Cabecalho de tabela ausente")
    names = header.group(1).split()
    rows = []
    for line in lines:
        match = re.fullmatch(r"V\d+\s+(.*?)\s*\|\s*([TF])\s*", line)
        if match:
            values = match.group(1).split()
            if len(values) != len(names) or any(value not in ("T", "F") for value in values):
                suite.fail(f"Linha de tabela malformada: {line!r}")
            rows.append({"values": dict(zip(names, (v == "T" for v in values))),
                         "outcome": match.group(2) == "T"})
    suite.check_table({"truthTable": rows}, oracle)


def main():
    if (ROOT / "resultados-extensao.json").exists():
        raise RuntimeError("Resultados da extensao ja existem")
    cases = [(f"U-{case_id}", case_id, "unique-text") for case_id in tables]
    cases += [(f"P-{case_id}", case_id, "plain-text") for case_id in ("T09", "T10", "T11")]
    cases += [("U-F01", "F01", "file-unique-json"), ("O-F02", "F02", "json-output")]
    results = []
    for case_id, source_id, kind in cases:
        case_dir = ROOT / "evidencias" / case_id
        case_dir.mkdir(exist_ok=False)
        exec_path = ROOT / "cobertura" / (case_id + ".exec")
        command = [
            "java", f"-javaagent:{suite.AGENT}=destfile={exec_path},append=false",
            "-cp", suite.CLASSPATH, suite.MAIN, "analyze",
        ]
        if kind in ("unique-text", "plain-text"):
            command.append(tables[source_id]["entrada"]["expressao"])
            if kind == "unique-text":
                command.append("--unique-cause")
        elif kind == "file-unique-json":
            command.extend(["-f", str(ROOT / "entradas" / "requisitos.mcdc"),
                            "--unique-cause", "--format", "json"])
        else:
            command.extend(["--json", str(ROOT / "entradas" / "decisoes.json"),
                            "--format", "json", "-o", str(case_dir / "relatorio.txt")])
        record = {"id": case_id, "oraculos_reutilizados": [source_id],
                  "classificacao_oraculo": "CONFORME À DOCUMENTAÇÃO",
                  "comando": command, "status": None, "detalhe": None,
                  "codigo_saida": None, "duracao_segundos": None}
        if kind == "json-output":
            record["oraculos_reutilizados"].append("F03")
        started = time.perf_counter()
        try:
            process = subprocess.run(command, cwd=case_dir, capture_output=True, timeout=60)
            (case_dir / "stdout.bin").write_bytes(process.stdout)
            (case_dir / "stderr.bin").write_bytes(process.stderr)
            stdout = process.stdout.decode("cp1252")
            stderr = process.stderr.decode("cp1252")
            (case_dir / "stdout.txt").write_text(stdout, encoding="utf-8")
            (case_dir / "stderr.txt").write_text(stderr, encoding="utf-8")
            record["codigo_saida"] = process.returncode
            infrastructure = ("Could not find or load main class", "NoClassDefFoundError",
                              "Could not create the Java Virtual Machine", "agent library failed")
            if any(message in stderr for message in infrastructure):
                record["status"] = "ERRO DE EXECUÇÃO"
                record["detalhe"] = stderr
            else:
                try:
                    if kind in ("unique-text", "plain-text"):
                        text_table(stdout, tables[source_id])
                    elif kind == "file-unique-json":
                        suite.check_case("F01", stdout, case_dir, tables, integration)
                    else:
                        suite.check_case("F03", stdout, case_dir, tables, integration)
                        report = (case_dir / "relatorio.txt").read_text(encoding="utf-8")
                        suite.check_case("F02", report, case_dir, tables, integration)
                    record["status"] = "PASSOU"
                except AssertionError as exc:
                    record["status"] = "FALHOU — DIVERGÊNCIA DOCUMENTAÇÃO/SUT"
                    record["detalhe"] = str(exc)
        except (FileNotFoundError, subprocess.TimeoutExpired, UnicodeDecodeError) as exc:
            record["status"] = "ERRO DE EXECUÇÃO"
            record["detalhe"] = str(exc)
        record["duracao_segundos"] = round(time.perf_counter() - started, 6)
        (case_dir / "resultado.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        results.append(record)
        print(case_id, record["status"], record["detalhe"] or "", flush=True)
    (ROOT / "resultados-extensao.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if any(item["status"] != "PASSOU" for item in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
