# -*- coding: utf-8 -*-
"""Utilitarios da suite C3: invoca a CLI MC/DC real (sem alterar o SUT)."""
import json
import os
import subprocess
import time

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados")
Z3_DIR = r"C:\Users\User\AppData\Roaming\Python\bin"
TIMEOUT = 300


def _classpath():
    cli = os.path.join(RAIZ, "mcdc-cli", "target", "classes")
    with open(os.path.join(RAIZ, "mcdc-cli", "target", "classpath.txt"), encoding="utf-8") as fh:
        return cli + ";" + fh.read().strip()


def mcdc(*args):
    """Executa a CLI; devolve (rc, stdout, stderr). Z3 no PATH (ver oraculo I02)."""
    env = dict(os.environ)
    env["PATH"] = env.get("PATH", "") + os.pathsep + Z3_DIR
    cmd = ["java", "-Dstdout.encoding=UTF-8", "-Dstderr.encoding=UTF-8", "-cp", _classpath(),
           "io.github.rvdomingos.mcdc.cli.Main"] + list(args)
    p = subprocess.run(cmd, cwd=RAIZ, env=env, capture_output=True, timeout=TIMEOUT)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def mcdc_json(*args):
    rc, out, err = mcdc(*args, "--format", "json")
    try:
        return json.loads(out)
    except ValueError:
        raise AssertionError("saida nao e JSON valido; stdout=%r stderr=%r" % (out[:300], err[:300]))


def decisoes(*args):
    return mcdc_json("analyze", *args)["decisions"]


def d1(*args):
    ds = decisoes(*args)
    assert len(ds) == 1, "esperada 1 decisao, obtidas %d" % len(ds)
    return ds[0]


def vetores_suite(x):
    return [(v["vector"], tuple(sorted(v["values"].items()))) for v in x["minimalSuite"]]


def tudo_demonstrado(x):
    labels = [c["label"] for c in x["conditions"]]
    assert x["uncoveredConditions"] == [], x["uncoveredConditions"]
    assert x["complete"] is True
    assert sorted(x["chosenPairs"].keys()) == sorted(labels)


def assinatura(x):
    """Resultado da analise independente do texto da guarda."""
    tt = [(tuple(sorted(r["values"].items())), r["outcome"], r["feasible"]) for r in x["truthTable"]]
    return (tt, json.dumps(x["independencePairs"], sort_keys=True), json.dumps(x["chosenPairs"], sort_keys=True),
            len(x["minimalSuite"]))


def dado(nome):
    return os.path.join(DADOS, nome)


def rel(nome):
    """Caminho relativo a raiz do repositorio (cwd da CLI)."""
    return os.path.relpath(os.path.join(DADOS, nome), RAIZ)


def cronometrar(*args):
    t = time.time()
    r = mcdc(*args)
    return time.time() - t, r
