"""Registra o resultado por caso (PASSOU/FALHOU/ERRO_TECNICO/INDETERMINADO-nao-executado).
Falha de asserção = FALHOU (divergencia em relacao a documentacao C2); excecao nao-assercao (timeout, etc.) = ERRO_TECNICO."""
import csv, json, os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORACULO = Path(os.environ.get("C2_ORACULO", HERE.parents[0] / "detalhes-C2" / "oraculo.json"))
OUT = Path(os.environ.get("C2_CSV", HERE.parent / "resultados" / "resultados-por-caso.csv"))
_res = {}


def pytest_runtest_logreport(report):
    if report.when != "call" and not (report.when == "setup" and report.failed):
        return
    cid = report.nodeid.split("::")[-1].replace("test_", "").replace("_", "-")
    if report.passed:
        _res[cid] = ("PASSOU", "")
    elif report.failed:
        msg = report.longreprtext.strip().splitlines()
        tail = " | ".join(m for m in msg[-6:])[:600]
        is_assert = "AssertionError" in report.longreprtext or "\nE       assert" in report.longreprtext
        _res[cid] = ("FALHOU" if is_assert else "ERRO_TECNICO", tail)


def pytest_sessionfinish(session, exitstatus):
    casos = json.loads(ORACULO.read_text(encoding="utf-8"))["casos"]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "grupo", "titulo", "status_oraculo", "resultado", "detalhe"])
        for c in casos:
            if c["status"] == "INDETERMINADO":
                res, det = "INDETERMINADO", "registrado no oraculo; nao executado"
            else:
                res, det = _res.get(c["id"], ("NAO_AVALIADO", "teste nao executado"))
            w.writerow([c["id"], c["grupo"], c["titulo"], c["status"], res, det])
