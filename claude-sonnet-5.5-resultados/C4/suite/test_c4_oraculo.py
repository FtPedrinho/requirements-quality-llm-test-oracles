# -*- coding: utf-8 -*-
"""Suite C4 (baseline): um teste por caso DETERMINADO do oraculo congelado.

As expectativas vem de experimento/oraculo.json (derivado so do texto C4).
Nenhuma expectativa foi ajustada ao comportamento do SUT. Casos INDETERMINADOS
nao tem teste (nao sao executados).
"""
import csv
import io
import json
import xml.etree.ElementTree as ET

import pytest

from c4_util import RAIZ, executar, json_da, nomes

SISTEMAS = {
    "vm": dict(arq="exemplos/vm-decisoes.json", req=5, cond=21, comb=152, imp=4, tst=26, mut=152, eq=0, conf=0, base=1),
    "tis": dict(arq="exemplos/tis-decisoes.json", req=17, cond=69, comb=268, imp=4, tst=80, mut=450, eq=21, conf=3, base=8),
    "npp": dict(arq="exemplos/npp-decisoes.json", req=11, cond=29, comb=76, imp=1, tst=40, mut=146, eq=0, conf=1, base=15),
}


def _analise(s):
    return json_da("analyze", "--json", SISTEMAS[s]["arq"], "--z3", "--format", "json")


def _mutacao(s):
    return json_da("analyze", "--json", SISTEMAS[s]["arq"], "--z3", "--mutation", "--format", "json")


def _verify(s):
    return json_da("verify", "--json", SISTEMAS[s]["arq"], "--format", "json")


def _soma(d, campo):
    return sum(x[campo] for x in d["decisions"])


# ---------------------------------------------------------------- D01-D21 (tabela de regressao)
def _fabrica(s, n, sufixo, fn):
    def teste():
        fn(s)
    teste.__name__ = f"test_C4_D{n:02d}_{s}_{sufixo}"
    globals()[teste.__name__] = teste


for _s, _v in SISTEMAS.items():
    _b = _v["base"]
    _fabrica(_s, _b, "requisitos", lambda s: _eq(len(_analise(s)["decisions"]), SISTEMAS[s]["req"], "requisitos"))
    _fabrica(_s, _b + 1, "condicoes", lambda s: _eq(sum(len(x["conditions"]) for x in _analise(s)["decisions"]), SISTEMAS[s]["cond"], "condicoes"))
    _fabrica(_s, _b + 2, "combinacoes", lambda s: _eq(_soma(_analise(s), "truthTableRows"), SISTEMAS[s]["comb"], "combinacoes"))
    _fabrica(_s, _b + 3, "impossiveis", lambda s: _eq(
        sum(1 for x in _analise(s)["decisions"] for r in x["truthTable"] if r.get("feasible") is False), SISTEMAS[s]["imp"], "impossiveis"))
    _fabrica(_s, _b + 4, "testes", lambda s: _eq(sum(len(x["minimalSuite"]) for x in _analise(s)["decisions"]), SISTEMAS[s]["tst"], "testes"))

    def _mut(s):
        d = _mutacao(s)
        total = sum(f["total"] for x in d["decisions"] for f in x["mutation"]["faults"].values())
        eq = sum(f["equivalent"] for x in d["decisions"] for f in x["mutation"]["faults"].values())
        assert (total, eq) == (SISTEMAS[s]["mut"], SISTEMAS[s]["eq"]), (
            f"mutantes totais/equivalentes: esperado {(SISTEMAS[s]['mut'], SISTEMAS[s]['eq'])}, observado {(total, eq)}")
    _fabrica(_s, _b + 5, "mutantes", _mut)
    _fabrica(_s, _b + 6, "conflitos", lambda s: _eq(len(_verify(s)["conflicts"]), SISTEMAS[s]["conf"], "conflitos"))


def _eq(obs, esp, nome):
    assert obs == esp, f"{nome}: esperado {esp}, observado {obs}"


# ---------------------------------------------------------------- D22-D34 (comportamento da CLI)
def _decisao(*args):
    return json_da(*args)["decisions"][0]


def test_C4_D22_dfrs_duas_condicoes_quatro_combinacoes():
    x = _decisao("analyze", "speed > 100 /\\ mode = idle", "--format", "json")
    assert (len(x["conditions"]), x["truthTableRows"]) == (2, 4)


def test_C4_D23_tres_entradas_oito_combinacoes():
    x = _decisao("analyze", "B or (C and D)", "--format", "json")
    assert (len(x["conditions"]), x["truthTableRows"]) == (3, 8)


def test_C4_D24_entrada_repetida_marcas_1_e_2():
    x = _decisao("analyze", "B or (not B and C)", "--format", "json")
    rotulos = [c["label"] for c in x["conditions"]]
    assert len(rotulos) == 3, f"condicoes: {rotulos}"
    assert any("#1" in r for r in rotulos) and any("#2" in r for r in rotulos), f"rotulos sem #1/#2: {rotulos}"


def test_C4_D25_entrada_repetida_quatro_combinacoes():
    x = _decisao("analyze", "B or (not B and C)", "--format", "json")
    assert x["truthTableRows"] == 4


def test_C4_D26_limite_20_entradas_aceito():
    expr = " and ".join(nomes(20))
    d = json_da("analyze", expr, "--format", "json")
    x = d["decisions"][0]
    assert x["truthTableRows"] == 1048576 and len(x["minimalSuite"]) > 0


def test_C4_D27_limite_12_entradas_z3_aceito():
    expr = " and ".join(nomes(12))
    d = json_da("analyze", expr, "--z3", "--format", "json")
    x = d["decisions"][0]
    assert x["truthTableRows"] == 4096 and len(x["minimalSuite"]) > 0


def test_C4_D28_modo_direto_26_entradas_aceito():
    expr = " and ".join(nomes(26))
    d = json_da("analyze", expr, "--direct", "--format", "json")
    assert len(d["decisions"][0]["minimalSuite"]) > 0


def test_C4_D29_paridade_tres_entradas_oito_testes():
    expr = ("(B and not C and not D) or (not B and C and not D) or "
            "(not B and not C and D) or (B and C and D)")
    x = _decisao("analyze", expr, "--format", "json")
    assert len(x["minimalSuite"]) == 8, f"testes: {len(x['minimalSuite'])}"


def test_C4_D30_valores_concretos_realizam_combinacao_e_resultado():
    x = _decisao("analyze", "speed > 100 or (speed > 50 and rain)", "--z3", "--format", "json")
    assert x["minimalSuite"], "suite vazia"
    for t in x["minimalSuite"]:
        a = t["assignment"]
        assert "speed" in a and "rain" in a, f"valores concretos incompletos: {a}"
        speed = float(a["speed"])
        rain = str(a["rain"]).lower() == "true"
        c = {"speed > 100": speed > 100, "speed > 50": speed > 50, "rain": rain}
        assert c == t["values"], f"combinacao declarada {t['values']} nao realizada por {a}"
        assert t["outcome"] == (c["speed > 100"] or (c["speed > 50"] and c["rain"])), f"resultado esperado incoerente em {t}"


def test_C4_D31_csv_celulas_com_virgula_entre_aspas():
    r = executar("analyze", "--json", "exemplos/vm-decisoes.json", "--z3", "--format", "csv")
    linhas = list(csv.reader(io.StringIO(r["out"])))
    assert len(linhas) >= 2, "CSV vazio"
    larguras = {len(l) for l in linhas if l}
    assert len(larguras) == 1, f"numero de campos varia entre linhas: {sorted(larguras)}"


def test_C4_D32_formato_json_valido():
    r = executar("analyze", "--json", "exemplos/tis-decisoes.json", "--z3", "--format", "json")
    json.loads(r["out"])


def test_C4_D33_expressao_invalida_recusada():
    r = executar("analyze", "(B and", "--format", "json")
    try:
        d = json.loads(r["out"])
    except json.JSONDecodeError:
        return  # nenhuma analise produzida
    assert not d.get("decisions"), f"analise produzida para expressao invalida: {r['out'][:200]}"


def test_C4_D34_modo_direto_mesmo_diagnostico_da_tabela():
    a = json_da("analyze", "--json", "exemplos/vm-decisoes.json", "--z3", "--format", "json")
    b = json_da("analyze", "--json", "exemplos/vm-decisoes.json", "--direct", "--format", "json")

    def diag(d):
        return [(x["id"], x["complete"], sorted(x["uncoveredConditions"]), [c["label"] for c in x["conditions"]])
                for x in d["decisions"]]
    assert diag(a) == diag(b)


# ---------------------------------------------------------------- D35-D42 (estrutura do repositorio)
MODULOS = ["mcdc-core", "mcdc-requirements", "mcdc-z3", "mcdc-cli"]


def _pom(caminho):
    arvore = ET.parse(RAIZ / caminho)
    for e in arvore.iter():
        if "}" in e.tag:
            e.tag = e.tag.split("}", 1)[1]
    return arvore.getroot()


def _deps(modulo):
    raiz = _pom(f"{modulo}/pom.xml")
    return [(d.findtext("groupId") or "", d.findtext("artifactId") or "") for d in raiz.iter("dependency")]


def _prop(pom, nome):
    for e in pom.iter(nome):
        return e.text.strip()
    return None


def test_C4_D35_quatro_modulos_maven():
    assert (RAIZ / "pom.xml").is_file(), "pom.xml da raiz ausente"
    for m in MODULOS:
        assert (RAIZ / m / "pom.xml").is_file(), f"{m}/pom.xml ausente"


def test_C4_D36_requirements_depende_de_core_e_jackson():
    d = _deps("mcdc-requirements")
    assert any(a == "mcdc-core" for _, a in d), d
    assert any("jackson" in g or "jackson" in a for g, a in d), d


def test_C4_D37_z3_depende_so_de_core_entre_modulos():
    projeto = {a for _, a in _deps("mcdc-z3") if a in MODULOS}
    assert projeto == {"mcdc-core"}, projeto


def test_C4_D38_cli_depende_dos_tres_modulos():
    projeto = {a for _, a in _deps("mcdc-cli") if a in MODULOS}
    assert {"mcdc-core", "mcdc-requirements", "mcdc-z3"} <= projeto, projeto


def test_C4_D39_notas_minimas_de_cobertura():
    raiz = _pom("pom.xml")
    lin, des = _prop(raiz, "qualidade.linhas.minima"), _prop(raiz, "qualidade.desvios.minima")
    assert lin is not None and des is not None, f"propriedades ausentes: linhas={lin}, desvios={des}"
    assert (float(lin), float(des)) == (0.90, 0.85), (lin, des)


def test_C4_D40_notas_minimas_de_mutacao_por_modulo():
    esperado = {"mcdc-core": 90, "mcdc-requirements": 90, "mcdc-z3": 85, "mcdc-cli": 75}
    obs = {m: _prop(_pom(f"{m}/pom.xml"), "qualidade.mutacao.minima") for m in esperado}
    assert all(v is not None for v in obs.values()), f"propriedade ausente em modulo(s): {obs}"
    assert {m: float(v) for m, v in obs.items()} == {m: float(v) for m, v in esperado.items()}, obs


def test_C4_D41_relatorios_no_repositorio():
    for p in ["relatorios/jacoco", "relatorios/jacoco/jacoco.csv", "relatorios/pit/mcdc-core"]:
        assert (RAIZ / p).exists(), f"{p} ausente"


def test_C4_D42_exemplos_citados_existem():
    for p in ["exemplos/vm-decisoes.json", "exemplos/tis-decisoes.json", "exemplos/npp-decisoes.json"]:
        assert (RAIZ / p).is_file(), f"{p} ausente"
    assert (RAIZ / "exemplos/saidas").is_dir(), "exemplos/saidas/ ausente"
