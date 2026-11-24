# -*- coding: utf-8 -*-
"""Suite C3 (baseline): um teste por caso DETERMINADO de experimento/oraculo.json.
Expectativas vem exclusivamente do oraculo congelado (documentacao C3); nunca do comportamento do SUT.
Os casos INDETERMINADOS (C3-I01..I24) nao sao executados.
"""
import json
import os
import re
import tempfile

import pytest

from c3util import (RAIZ, assinatura, cronometrar, d1, dado, decisoes, mcdc, mcdc_json, rel,
                    tudo_demonstrado, vetores_suite)

SEIS = {"ORF", "ENF", "VNF", "MVF", "VRF", "ASF"}


def tabela(x):
    return [(tuple(sorted(r["values"].items())), r["outcome"]) for r in x["truthTable"]]


def _sistema(nome, *extra):
    return mcdc_json("analyze", "--json", "exemplos/%s-decisoes.json" % nome, "--z3", *extra)


def _soma(sistema, *extra):
    ds = _sistema(sistema, *extra)["decisions"]
    return ds


# ------------------------------------------------------------------ operadores
def test_C3_D01_formas_e_nao():
    base = None
    for expr in ("A and not B", "A && !B", "A /\\ !B"):
        x = d1(expr)
        assert len(x["conditions"]) == 2
        assert x["truthTableRows"] == 4
        tudo_demonstrado(x)
        a = tabela(x)
        base = base or a
        assert a == base
    return None


def test_C3_D02_formas_ou():
    base = None
    for expr in ("A or B", "A || B", "A \\/ B"):
        x = d1(expr)
        assert len(x["conditions"]) == 2
        assert x["truthTableRows"] == 4
        tudo_demonstrado(x)
        a = tabela(x)
        base = base or a
        assert a == base


def test_C3_D03_operadores_de_comparacao():
    for op in ("=", "==", "!=", "<", "<=", ">", ">="):
        x = d1("speed %s 100" % op)
        assert len(x["conditions"]) == 1, op


def test_C3_D04_precedencia_e_antes_de_ou():
    a = d1("A or B and C")
    b = d1("A or (B and C)")
    assert len(a["conditions"]) == 3
    assert tabela(a) == tabela(b)


# ---------------------------------------------------------------------- motor
def test_C3_D05_abc_mascaramento():
    x = d1("(A and B) or C")
    assert len(x["conditions"]) == 3
    assert x["truthTableRows"] == 8
    assert len(x["minimalSuite"]) == 4
    tudo_demonstrado(x)


def test_C3_D06_abc_causa_unica():
    x = d1("(A and B) or C", "--unique-cause")
    assert len(x["conditions"]) == 3
    assert x["truthTableRows"] == 8
    tudo_demonstrado(x)


def test_C3_D07_entrada_repetida_tem_8_combinacoes():
    x = d1("(A and B) or (not A and C)")
    assert x["truthTableRows"] == 8


def test_C3_D08_suite_exata_abc():
    x = d1("(A and B) or C", "--exact")
    assert len(x["minimalSuite"]) == 4
    tudo_demonstrado(x)


def test_C3_D09_restricao_manual():
    x = d1("A or (B and C)", "--constraint", "not A or B")
    inviaveis = [r for r in x["truthTable"] if not r["feasible"]]
    assert len(x["truthTable"]) == 8
    assert len(inviaveis) == 2
    assert {(r["values"]["A"], r["values"]["B"]) for r in inviaveis} == {(True, False)}
    ids = {r["vector"] for r in inviaveis}
    usados = {v["vector"] for v in x["minimalSuite"]}
    for pares in x["independencePairs"].values():
        for p in pares:
            usados.update(p)
    assert ids.isdisjoint(usados)


# ------------------------------------------------------------------------ Z3
def _boundary(x):
    return {(b["condition"], b["boundary"]) for b in x["boundaryTests"]}


def test_C3_D10_fronteira_speed_100():
    x = d1("speed > 100 /\\ mode = idle", "--z3", "--boundary")
    b = _boundary(x)
    assert ("speed > 100", "speed = 100") in b
    assert ("speed > 100", "speed = 101") in b


def test_C3_D11_valores_concretos_realizam_a_combinacao():
    x = d1("speed > 100 /\\ mode = idle", "--z3")
    assert x["minimalSuite"]
    for t in x["minimalSuite"]:
        a = t["assignment"]
        assert (int(a["speed"]) > 100) == t["values"]["speed > 100"]
        assert (a["mode"] == "idle") == t["values"]["mode = idle"]
        assert t["outcome"] == (t["values"]["speed > 100"] and t["values"]["mode = idle"])


# ------------------------------------------------------------------ mutacao
def _faltas(x):
    m = x["mutation"]
    assert m, "sem resultado de mutacao"
    return m


def test_C3_D12_mutacao_estrutura_e_contagem():
    m = _faltas(d1("A and (B or C)", "--mutation"))
    assert set(m["faults"]) <= SEIS
    total = sum(f["total"] for f in m["faults"].values())
    equiv = sum(f["equivalent"] for f in m["faults"].values())
    mortos = sum(f["killed"] for f in m["faults"].values())
    assert total > 0


def test_C3_D13_causa_unica_mata_mutantes_garantidos():
    m = _faltas(d1("A and (B or C)", "--unique-cause", "--mutation"))
    for tipo, f in m["faults"].items():
        if tipo != "ASF":
            assert f["killed"] == f["total"] - f["equivalent"], tipo
    assert [s for s in m["survivors"] if not s.startswith("ASF")] == []


# ----------------------------------------------------------------- exemplos
def _regressao(sistema, req, completos, comb, imp, testes):
    ds = _soma(sistema)
    assert len(ds) == req
    assert sum(1 for x in ds if x["complete"]) == completos
    assert sum(x["truthTableRows"] for x in ds) == comb
    assert sum(1 for x in ds for r in x["truthTable"] if not r["feasible"]) == imp
    assert sum(len(x["minimalSuite"]) for x in ds) == testes


def test_C3_D14_regressao_vm():
    _regressao("vm", 5, 5, 152, 4, 26)


def test_C3_D15_regressao_tis():
    _regressao("tis", 17, 14, 268, 4, 80)


def test_C3_D16_regressao_npp():
    _regressao("npp", 11, 11, 76, 1, 40)


def _mutacao(sistema, tot, eq, pegos):
    ds = _soma(sistema, "--mutation")
    faltas = [f for x in ds for f in x["mutation"]["faults"].values()]
    assert (sum(f["total"] for f in faltas), sum(f["equivalent"] for f in faltas),
            sum(f["killed"] for f in faltas)) == (tot, eq, pegos)


def test_C3_D17_mutacao_vm():
    _mutacao("vm", 152, 0, 152)


def test_C3_D18_mutacao_tis():
    _mutacao("tis", 450, 21, 428)


def test_C3_D19_mutacao_npp():
    _mutacao("npp", 146, 0, 146)


def _testes(sistema, n):
    for flag in ("--exact", "--unique-cause"):
        ds = _soma(sistema, flag)
        assert sum(len(x["minimalSuite"]) for x in ds) == n, flag


def test_C3_D20_exata_e_causa_unica_vm():
    _testes("vm", 26)


def test_C3_D21_exata_e_causa_unica_tis():
    _testes("tis", 80)


def test_C3_D22_exata_e_causa_unica_npp():
    _testes("npp", 40)


def _conflitos(sistema, n):
    d = mcdc_json("verify", "--json", "exemplos/%s-decisoes.json" % sistema)
    assert len(d["conflicts"]) == n


def test_C3_D23_conflitos_vm():
    _conflitos("vm", 0)


def test_C3_D24_conflitos_tis():
    _conflitos("tis", 3)


def test_C3_D25_conflitos_npp():
    _conflitos("npp", 1)


# ------------------------------------------------------------------- saidas
def test_C3_D26_json_liga_decisao_ao_requisito():
    entrada = json.load(open(os.path.join(RAIZ, "exemplos", "vm-decisoes.json"), encoding="utf-8"))
    esperado = {d["id"]: d["requirement"] for d in entrada["decisions"]}
    ds = mcdc_json("analyze", "--json", "exemplos/vm-decisoes.json")["decisions"]
    assert {x["id"]: x["requirement"] for x in ds} == esperado


def test_C3_D27_opcao_o_grava_arquivo():
    with tempfile.TemporaryDirectory() as td:
        arq = os.path.join(td, "rel.txt")
        rc, out, err = mcdc("analyze", "A and B", "-o", arq)
        assert os.path.isfile(arq)
        conteudo = open(arq, encoding="utf-8").read()
        assert "Suíte" in conteudo
        assert "Suíte" not in out and "Vetor" not in out


def test_C3_D28_arquivo_mcdc_com_comentarios():
    ds = decisoes("-f", rel("dois-requisitos.mcdc"))
    assert [x["id"] for x in ds] == ["REQ-001", "REQ-002"]


# --------------------------------------------------------------------- check
def _check(csv):
    d = mcdc_json("check", "--json", rel("decisao-abc.json"), "--tests", rel(csv))
    return d["decisions"][0]


def test_C3_D29_check_suite_completa():
    x = _check("testes-completo.csv")
    assert x["conditionsDemonstrated"] == 3 and x["conditionsTotal"] == 3
    assert x["problems"] == []
    assert all(c["demonstrated"] for c in x["conditions"])


def test_C3_D30_check_esperado_errado_apontado():
    x = _check("testes-esperado-errado.csv")
    assert len(x["problems"]) == 1 and x["problems"][0].startswith("T1:")


def test_C3_D31_check_condicao_faltando():
    x = _check("testes-incompleto.csv")
    dem = {c["condition"]: c["demonstrated"] for c in x["conditions"]}
    assert dem == {"A = true": True, "B = true": True, "C = true": False}
    assert x["conditionsDemonstrated"] == 2


# -------------------------------------------------------------------- verify
def _verify(arq, *extra):
    return mcdc_json("verify", "--json", rel(arq), *extra)


def test_C3_D32_verify_conflito():
    d = _verify("verify-conflito.json")
    assert len(d["conflicts"]) == 1
    assert {d["conflicts"][0]["firstRequirement"], d["conflicts"][0]["secondRequirement"]} == {"R1", "R2"}


def test_C3_D33_verify_mesmo_valor_sem_conflito():
    assert _verify("verify-mesmo-valor.json")["conflicts"] == []


def test_C3_D34_verify_guardas_disjuntas():
    assert _verify("verify-disjuntas.json")["conflicts"] == []


def test_C3_D35_verify_lacuna_com_contexto():
    d = _verify("verify-disjuntas.json", "--context", "mode = off")
    assert d["gaps"]["checked"] is True and d["gaps"]["found"] is True


def test_C3_D36_verify_sem_lacuna_quando_guarda_vale():
    d = _verify("verify-disjuntas.json", "--context", "mode = idle")
    assert d["gaps"]["checked"] is True and d["gaps"]["found"] is False


# -------------------------------------------------------------------- limites
def test_C3_D37_vinte_entradas():
    expr = " and ".join("X%d" % i for i in range(1, 21))
    rc, out, err = mcdc("analyze", expr)
    assert "1048576 linhas" in out
    assert "Cobertura MC/DC: completa" in out
    assert len(re.findall(r"só ela muda", out)) == 20


def test_C3_D38_guarda_temporal_antes():
    x = d1("--json", rel("temporal.json"))
    assert len(x["conditions"]) == 2


def test_C3_D39_numero_negativo():
    x = d1("x > -3 and y < 2")
    assert len(x["conditions"]) == 2


def test_C3_D40_check_e_verify_aceitam_json():
    json.loads(mcdc("check", "--json", rel("decisao-abc.json"), "--tests", rel("testes-completo.csv"), "--format", "json")[1])
    json.loads(mcdc("verify", "--json", rel("verify-conflito.json"), "--format", "json")[1])


