import json
import os
from pathlib import Path
import subprocess
import time


ROOT = Path(__file__).resolve().parent
HOME = Path.home()
JACKSON = HOME / ".m2" / "repository" / "com" / "fasterxml" / "jackson" / "core"
JARS = [
    JACKSON / "jackson-annotations" / "2.17.2" / "jackson-annotations-2.17.2.jar",
    JACKSON / "jackson-core" / "2.17.2" / "jackson-core-2.17.2.jar",
    JACKSON / "jackson-databind" / "2.17.2" / "jackson-databind-2.17.2.jar",
]
AGENT = HOME / ".m2" / "repository" / "org" / "jacoco" / "org.jacoco.agent" / "0.8.16" / "org.jacoco.agent-0.8.16-runtime.jar"
CLASSPATH = os.pathsep.join(str(p) for p in [ROOT / "build" / "classes", *JARS])
MAIN = "io.github.rvdomingos.mcdc.cli.Main"


def fail(message):
    raise AssertionError(message)


def read_report(stdout):
    try:
        report = json.loads(stdout)
    except json.JSONDecodeError as exc:
        fail(f"Relatorio JSON ausente ou invalido: {exc}")
    if not isinstance(report, dict) or not isinstance(report.get("decisions"), list):
        fail("Relatorio JSON nao apresenta lista de decisoes")
    return report["decisions"]


def check_table(decision, oracle):
    if not isinstance(decision, dict):
        fail(f"Decisao malformada: {decision!r}")
    rows = decision.get("truthTable")
    if not isinstance(rows, list):
        fail("Tabela-verdade ausente")
    expected = {
        tuple(sorted(row["entradas"].items())): row["resultado"]
        for row in oracle["esperado"]
    }
    actual = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("values"), dict):
            fail(f"Linha malformada: {row!r}")
        values = row["values"]
        if not all(type(value) is bool for value in values.values()) or type(row.get("outcome")) is not bool:
            fail(f"Valores ou resultado nao booleanos: {row!r}")
        key = tuple(sorted(values.items()))
        if key in actual:
            fail(f"Vetor duplicado: {key}")
        actual[key] = row["outcome"]
    if actual != expected:
        fail(f"Tabela divergente: esperado={expected!r}; observado={actual!r}")


def check_case(case_id, stdout, case_dir, tables, integration):
    if case_id in tables:
        decisions = read_report(stdout)
        if len(decisions) != 1:
            fail(f"Esperada uma decisao, observadas {len(decisions)}")
        check_table(decisions[0], tables[case_id])
    elif case_id == "F01":
        decisions = read_report(stdout)
        expected = integration["F01"]["esperado"]
        if len(decisions) != expected["numero_decisoes"]:
            fail(f"Numero de decisoes divergente: {len(decisions)}")
        by_id = {item.get("id"): item for item in decisions if isinstance(item, dict)}
        for item in expected["decisoes"]:
            if item["id"] not in by_id:
                fail(f"Decisao ausente: {item['id']}")
            check_table(by_id[item["id"]], tables[item["tabela"]])
    elif case_id == "F02":
        decisions = read_report(stdout)
        expected = integration["F02"]["esperado"]
        if not any(isinstance(item, dict) and item.get("id") == expected["decisao"]
                   and item.get("requirement") == expected["requisito"] for item in decisions):
            fail(f"Vinculo decisao-requisito ausente: {expected!r}")
    elif case_id == "F03":
        report_path = case_dir / "relatorio.txt"
        if not report_path.is_file():
            fail("Relatorio nao foi gravado no arquivo solicitado")
        report = report_path.read_text(encoding="utf-8")
        if not report.strip():
            fail("Relatorio gravado vazio")
        first_line = next(line for line in report.splitlines() if line.strip())
        if first_line in stdout:
            fail("Relatorio exibido na tela apesar de -o")
    else:
        raise ValueError(f"Caso desconhecido: {case_id}")


def main():
    if (ROOT / "resultados.json").exists():
        raise RuntimeError("Resultados ja existem; nao sobrescrever")
    tables = {c["id"]: c for c in json.loads((ROOT / "oraculos.json").read_text(encoding="utf-8"))}
    integration = {c["id"]: c for c in json.loads((ROOT / "oraculos-integracao.json").read_text(encoding="utf-8"))}
    for case in integration.values():
        for name, contents in case["entrada"]["arquivos"].items():
            actual = (ROOT / "entradas" / name).read_text(encoding="utf-8")
            if actual.rstrip("\n") != contents.rstrip("\n"):
                raise RuntimeError(f"Entrada diverge do oraculo congelado: {name}")

    results = []
    for case_id in [*tables, *integration]:
        case_dir = ROOT / "evidencias" / case_id
        case_dir.mkdir(exist_ok=False)
        exec_path = ROOT / "cobertura" / (case_id + ".exec")
        command = [
            "java", f"-javaagent:{AGENT}=destfile={exec_path},append=false",
            "-cp", CLASSPATH, MAIN, "analyze",
        ]
        if case_id in tables:
            command.extend([tables[case_id]["entrada"]["expressao"], "--format", "json"])
        elif case_id == "F01":
            command.extend(["-f", str(ROOT / "entradas" / "requisitos.mcdc"), "--format", "json"])
        elif case_id == "F02":
            command.extend(["--json", str(ROOT / "entradas" / "decisoes.json"), "--format", "json"])
        else:
            command.extend([integration["F03"]["entrada"]["argumentos"][1], "-o", str(case_dir / "relatorio.txt")])

        started = time.perf_counter()
        result = {
            "id": case_id, "classificacao_oraculo": "CONFORME À DOCUMENTAÇÃO",
            "comando": command, "status": None, "detalhe": None,
            "codigo_saida": None, "duracao_segundos": None,
        }
        try:
            process = subprocess.run(command, cwd=case_dir, capture_output=True, timeout=60)
            (case_dir / "stdout.bin").write_bytes(process.stdout)
            (case_dir / "stderr.bin").write_bytes(process.stderr)
            stdout = process.stdout.decode("utf-8")
            stderr = process.stderr.decode("utf-8")
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
                    check_case(case_id, stdout, case_dir, tables, integration)
                    result["status"] = "PASSOU"
                except AssertionError as exc:
                    result["status"] = "FALHOU — DIVERGÊNCIA DOCUMENTAÇÃO/SUT"
                    result["detalhe"] = str(exc)
        except (FileNotFoundError, subprocess.TimeoutExpired, UnicodeDecodeError) as exc:
            result["status"] = "ERRO DE EXECUÇÃO"
            result["detalhe"] = str(exc)
        result["duracao_segundos"] = round(time.perf_counter() - started, 6)
        (case_dir / "resultado.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        results.append(result)
        print(case_id, result["status"], result["detalhe"] or "", flush=True)

    (ROOT / "resultados.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if any(item["status"] != "PASSOU" for item in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
