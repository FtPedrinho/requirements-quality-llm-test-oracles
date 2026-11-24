"""Suíte C0 — executa o MC/DC real e compara com o oráculo documental congelado.
Só casos DETERMINADOS são executados; os INDETERMINADOS não têm teste (ficam só no oráculo)."""
import json, os, re
import pytest
from conftest import carregar_casos, executar, preparar, salvar_bruto

DETERMINADOS = [c for c in carregar_casos() if c["status"] == "DETERMINADO"]


def linhas(txt):
    return [l for l in txt.splitlines() if l.strip()]


def checar(caso, obs, d, args):
    e = caso["observa"]
    saida = obs["stdout"] + "\n" + obs["stderr"]
    baixo = saida.lower()
    if "exit" in e:
        assert obs["exit"] == e["exit"], "código de saída %s != esperado %s" % (obs["exit"], e["exit"])
    if "csv_rows" in e:
        n = len(linhas(obs["stdout"]))
        assert n in (e["csv_rows"], e["csv_rows"] + 1), "linhas CSV %d, esperado %d (ou +1 de cabeçalho)" % (n, e["csv_rows"])
    if "lines" in e:
        n = len(linhas(obs["stdout"]))
        assert n == e["lines"], "linhas %d != esperado %d" % (n, e["lines"])
    for s in e.get("contains", []) + e.get("contains_todos", []):
        assert s.lower() in baixo, "saída não contém %r" % s
    for s in e.get("not_contains", []):
        assert s.lower() not in baixo, "saída contém %r" % s
    if e.get("json_valid"):
        json.loads(obs["stdout"])
    if "outfile" in e:
        p = os.path.join(d, e["outfile"])
        assert os.path.isfile(p) and os.path.getsize(p) > 0, "arquivo -o ausente ou vazio"
        if e.get("stdout_vazio"):
            assert obs["stdout"].strip() == "", "stdout não deveria mostrar o relatório"
    if "mais_longo_que" in e:
        ref = executar(e["mais_longo_que"], caso["usa_z3"])
        assert len(obs["stdout"]) > len(ref["stdout"]), "relatório com --mutation não é maior que sem"
    if "contem_numero_maior_que" in e:
        nums = [int(x) for x in re.findall(r"(?<![\w.])-?\d+(?![\w.])", obs["stdout"])]
        assert any(x > e["contem_numero_maior_que"] for x in nums), "nenhum valor > %d" % e["contem_numero_maior_que"]


@pytest.mark.parametrize("caso", DETERMINADOS, ids=[c["id"] for c in DETERMINADOS])
def test_caso(caso):
    args, d = preparar(caso)
    obs = executar(args, caso["usa_z3"])
    obs.update({"id": caso["id"], "titulo": caso["titulo"], "esperado": caso["observa"], "usa_z3": caso["usa_z3"]})
    salvar_bruto(caso["id"], obs)
    checar(caso, obs, d, args)
