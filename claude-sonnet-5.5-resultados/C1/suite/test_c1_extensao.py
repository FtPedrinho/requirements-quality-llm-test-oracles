"""Extensao E1: reexecuta o caso C1-D02 com a opcao --format json que faltava
na invocacao do baseline (defeito da suite: a expectativa do oraculo e a mesma).
Nenhuma expectativa foi alterada."""
import tempfile

from test_c1 import CASOS, _checa, invocar

CASO = dict(next(c for c in CASOS if c["id"] == "C1-D02"))


def test_caso_extensao_D02():
    cli = CASO["cli"] + ["--format", "json"]
    with tempfile.TemporaryDirectory() as tmp:
        rc, out, err = invocar(cli, "C1-D02-ext")
        falhas = []
        _checa(CASO, cli, rc, out, err, tmp, falhas)
    assert not falhas, "; ".join(falhas)
