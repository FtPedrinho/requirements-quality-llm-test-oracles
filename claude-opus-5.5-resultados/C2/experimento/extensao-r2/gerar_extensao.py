# -*- coding: utf-8 -*-
"""Extensão r2 do oráculo C2: situações documentadas ainda não testadas no baseline.

A cobertura do baseline apenas LOCALIZOU áreas pouco exercitadas (codificação SMT de
comparações, modo direto em sistemas, CSV com valores concretos, check/verify em JSON e
arquivo). Toda expectativa abaixo vem do texto C2 (mesmas leituras de
experimento/analise-oraculo.md); nenhuma vem do comportamento observado.
Gera: entradas próprias, consultas Z3 e oraculo-extensao.json.
"""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(HERE)
spec = importlib.util.spec_from_file_location("go", os.path.join(EXP, "scripts", "gerar_oraculo.py"))
go = importlib.util.module_from_spec(spec)
spec.loader.exec_module(go)
spec2 = importlib.util.spec_from_file_location("gz", os.path.join(EXP, "scripts", "gerar_z3.py"))
gz = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(gz)

ENT = os.path.join(HERE, "entradas")
os.makedirs(ENT, exist_ok=True)
X03 = {
    "system": "real_sys",
    "inputs": [{"name": "t", "type": "real"}, {"name": "k", "type": "enum", "values": ["a", "b"]},
               {"name": "f", "type": "bool"}],
    "decisions": [{"id": "r#1", "requirement": "R-R1",
                   "guard": "(t >= 2.5 /\\ k != a) \\/ (f = false /\\ t < -1.5)", "actions": ["z := 1"]}],
}
with open(os.path.join(ENT, "x03-real.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(X03, f, ensure_ascii=False, indent=2)
    f.write("\n")

# Z3: viabilidade das combinações (evidência de que existem linhas realizáveis por valores
# concretos) para as expressões novas.
gz.ZDIR = os.path.join(HERE, "z3")
os.makedirs(gz.ZDIR, exist_ok=True)
# Expressão direta não declara tipos: a formalização usa inteiros para variáveis numéricas
# (inclusive y <= x, comparação entre variáveis) e domínio textual aberto para m.
T01 = [{"name": v, "type": "int"} for v in ("x", "y", "z")]
T02 = [{"name": "m", "type": "enum", "values": ["idle", "outro_valor"]}, {"name": "n", "type": "int"}]
gz.feasibility("X01-tabela", "(x < 3) or ((y <= x) and (z >= -2))", T01, nota="X01: combinações com comparação acoplada y <= x")
gz.pairs_unique("X01-pares", "(x < 3) or ((y <= x) and (z >= -2))", T01, nota="X01")
gz.feasibility("X02-tabela", "(m != idle) and (n = 4)", T02, nota="X02")
gz.pairs_unique("X02-pares", "(m != idle) and (n = 4)", T02, nota="X02")
gz.feasibility("X03-tabela", X03["decisions"][0]["guard"], X03["inputs"], nota="X03: real, enum, bool, negativo")
gz.pairs_unique("X03-pares", X03["decisions"][0]["guard"], X03["inputs"], nota="X03")
with open(os.path.join(gz.ZDIR, "resumo-z3-extensao.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(gz.RESUMO, f, ensure_ascii=False, indent=2)

go.CASES.clear()
C, D = go.C, go.D
T_CONC_GERAL = ("L41", "| Dar valoes concretos | `--z3` | Combinaçoes impossiveis descrtadas  valoes concretos   teste (`speed = 101`) |")
T_NUMORA = ("L417", "| `NumericOracleTest` | 1 |  150 expressões alatórias  comparçes numérics   enumerção (`x > 3`, `y <= x`, `mode != idle`), acpladas entre si, ...")
C("X01", "z3", D, ["analyze", "(x < 3) or ((y <= x) and (z >= -2))", "--z3", "--boundary", "--format", "json"],
  [T_CONC_GERAL, go.T_CONC, T_NUMORA, go.T_OPS], "Valores concretos realizam cada combinação e o resultado é o da guarda (inclui fronteira).",
  {"exit": 0, "concretos_realizam": True},
  "L41/L463; comparações < <= >= e acoplamento y <= x (L417); negativo (L523). X01-tabela: combinações viáveis. "
  "Código 0: X01-pares mostra par de causa única viável para as 3 condições.",
  ["X01-tabela", "X01-pares"])
C("X02", "z3", D, ["analyze", "(m != idle) and (n = 4)", "--z3", "--boundary", "--format", "json"],
  [T_CONC_GERAL, go.T_CONC, T_NUMORA], "Valores concretos com != textual e = numérico.", {"exit": 0, "concretos_realizam": True},
  "L41/L463; X02-pares: par de causa única viável para as 2 condições.", ["X02-tabela", "X02-pares"])
C("X03", "z3", D, ["analyze", "--json", "{ENT}/x03-real.json", "--z3", "--boundary", "--format", "json"],
  [T_CONC_GERAL, go.T_CONC, go.T_JSONF], "Valores concretos com real, enumeração, booleano e negativo.",
  {"exit": 0, "concretos_realizam": True, "todas_condicoes_com_par": True},
  "L41/L463, L153. X03-pares: par de causa única viável para todas as condições.", ["X03-tabela", "X03-pares"])
C("X04", "formatos", D, ["analyze", "speed > 100 or (speed > 50 and rain)", "--z3", "--boundary", "--format", "csv"],
  [go.T_OUTS, go.T_CONC], "CSV da suíte com valores concretos: resultado esperado de cada teste é o valor da guarda.",
  {"exit": 0, "csv_resultado_esperado_correto": True}, "L205, L463.", ["Q13-speed-rain-tabela"])
C("X05", "check", D, ["check", "--json", "{EX}/decisoes.json", "--tests", "{EX}/testes.csv", "--format", "json"],
  [go.T_FMT, go.T_CHECK, go.T_EXIT], "check em JSON: mesma divergência de T4 e código 2.",
  {"exit": 2, "json_valido": True, "check_divergentes": ["T4"], "check_nao_demonstrada": True}, "Como K01; L121.", ["Q23-check-exemplo"])
C("X06", "modo-direto", D, ["analyze", "--json", "{EX}/vm-decisoes.json", "--direct", "--unique-cause", "--format", "json"],
  [go.T_DIRECT, go.T_EXIT, go.T_VAR], "Modo direto, causa única: VM sem condição sem par.", {"exit": 0, "todas_condicoes_com_par": True},
  go.LEIT_CU + " VM-*-pares (Z3): par de causa única viável para todas as 21 condições.", ["VM-totais"])
C("X07", "modo-direto", D, ["analyze", "--json", "{EX}/npp-decisoes.json", "--direct", "--format", "json"],
  [go.T_DIRECT, go.T_EXIT], "Modo direto: NPP sem condição sem par.", {"exit": 0, "todas_condicoes_com_par": True},
  "L419; NPP-*-pares (Z3).", ["NPP-totais"])
C("X08", "modo-direto", D, ["analyze", "-f", "{EX}/requisitos.mcdc", "--direct", "--format", "json"],
  [go.T_DIRECT, go.T_REQ3, go.T_EXIT], "Modo direto dá o mesmo diagnóstico: REQ-003 com condição redundante.",
  {"exit": 2, "requisito_tem_classe": {"REQ-003": "redundante"}}, "L419 + L241 (como M01).")
C("X09", "verify", D, ["verify", "--json", "{EX}/npp-decisoes.json", "-o", "{OUT}/X09-verify.txt"],
  [go.T_O, go.T_VERIFY, go.T_EXIT], "verify grava o relatório com -o; conflito → código 2.",
  {"exit": 2, "arquivo_gerado": "{OUT}/X09-verify.txt", "stdout_sem_relatorio": True}, "L123, L475.")
C("X10", "sistemas", D, ["analyze", "--json", "{EX}/vm-decisoes.json", "--z3", "--boundary", "--mutation"],
  [go.T_NUM, go.T_EXIT, go.T_OUTS], "Relatório em texto do VM com fronteira e mutação; sem condição sem par → 0.",
  {"exit": 0, "mutantes": {"total": 152, "equivalentes": 0, "detectados": 152}}, "L471, L139; VM-*-pares.", ["VM-totais"])
C("X11", "formatos", D, ["analyze", "(A and B) or C", "--unique-cause", "--format", "truth-csv"],
  [go.T_OUTS, go.T_TT0], "truth-csv também na causa única: 8 linhas, linha 0 tudo verdadeiro, resultado da guarda.",
  {"exit": 0, "truth_linhas": 8, "truth_primeira_tudo_verdadeiro": True, "truth_resultado_correto": True}, "L207, L279, L485.")
C("X12", "check", D, ["check", "A and B", "--tests", "{ENT0}/c04-esperado-errado.csv", "--format", "json"],
  [go.T_FMT, go.T_CHECK, go.T_EXIT], "check JSON com resultado esperado errado.", {"exit": 2, "json_valido": True, "check_divergentes": ["T3"]},
  "Como K04.")

for c in go.CASES:
    c["comando"] = [a.replace("{ENT0}", "{ENT_BASE}") for a in c["comando"]]
out = dict(go.ORACULO)
out["extensao"] = "r2"
out["casos"] = go.CASES
with open(os.path.join(HERE, "oraculo-extensao.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(len(go.CASES), "casos de extensão")
print({k: (v.get("impossiveis"), v.get("par_causa_unica")) for k, v in gz.RESUMO["consultas"].items()})
