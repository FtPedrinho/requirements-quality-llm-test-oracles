"""Suíte refeita (r3): seleção dos casos já congelados, sem expectativas novas.

- Base: oraculo.json (75 casos). Os casos de check que usavam decision = "D" com
  expressão direta (T20, T21, T22, T25, I03, I38) são substituídos pelas versões
  corrigidas de oraculo-r2.json (mesmas expectativas, decisão vinda de abc.mcdc).
- Extensão mantida: E01-E04 (situações descritas pela documentação, com expectativa).
- Removidos: I40-I47. Foram criados na r2 apenas para alcançar branches de validação de
  opções, sem trecho que descreva a situação ou o resultado. Não são necessários: o código
  que só eles alcançavam deve ficar sem cobertura.
Uso: python -I selecao.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(HERE)
base = json.load(open(os.path.join(EXP, "oraculo.json"), encoding="utf-8"))["casos"]
r2 = {c["id"]: c for c in json.load(open(os.path.join(EXP, "extensao-r2", "oraculo-r2.json"), encoding="utf-8"))["casos"]}

SUBST = {"C3-T20": "C3-T20c", "C3-T21": "C3-T21c", "C3-T22": "C3-T22c", "C3-T25": "C3-T25c",
         "C3-I03": "C3-I03c", "C3-I38": "C3-I38c"}
MANTER_EXT = ["C3-E01", "C3-E02", "C3-E03", "C3-E04"]
REMOVIDOS = [f"C3-I{n}" for n in range(40, 48)]

casos = [r2[SUBST[c["id"]]] if c["id"] in SUBST else c for c in base] + [r2[i] for i in MANTER_EXT]
assert not any(c["id"] in REMOVIDOS for c in casos)
json.dump({"condicao": "C3", "rodada": "r3", "origem": ["oraculo.json", "extensao-r2/oraculo-r2.json"],
           "substituidos": SUBST, "removidos": REMOVIDOS, "casos": casos},
          open(os.path.join(HERE, "oraculo-r3.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(casos), sum(c["status"] == "DETERMINADO" for c in casos))
