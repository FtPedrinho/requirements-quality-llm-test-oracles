"""Coleta o resultado por caso (PASSOU / FALHOU / ERRO_TECNICO) em CSV."""
import csv
import json
import os

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.environ.get("C1_CSV", os.path.join(HERE, "..", "resultados", "resultados-por-caso.csv"))
_res = {}


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    rep = (yield).get_result()
    if rep.when != "call" and not (rep.when == "setup" and rep.failed):
        return
    cid = item.callspec.id if hasattr(item, "callspec") else item.name
    if rep.passed:
        _res[cid] = ("PASSOU", "")
    elif rep.failed:
        tecnico = call.excinfo is not None and call.excinfo.type.__name__ == "ErroTecnico"
        txt = str(call.excinfo.value) if call.excinfo else ""
        _res[cid] = ("ERRO_TECNICO" if tecnico else "FALHOU", txt.replace("\n", " ")[:600])


def pytest_sessionfinish(session):
    with open(os.path.join(HERE, "..", "detalhes-C1", "oraculo.json"), encoding="utf-8") as fh:
        ora = json.load(fh)
    os.makedirs(os.path.dirname(os.path.abspath(SAIDA)), exist_ok=True)
    with open(SAIDA, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "grupo", "status_oraculo", "resultado", "detalhe"])
        for c in ora["casos"]:
            if c["status"] == "INDETERMINADO":
                w.writerow([c["id"], c["grupo"], "INDETERMINADO", "INDETERMINADO", "nao executado (decisao do pesquisador)"])
            else:
                r = _res.get(c["id"], ("NAO_EXECUTADO", ""))
                w.writerow([c["id"], c["grupo"], "DETERMINADO", r[0], r[1]])
