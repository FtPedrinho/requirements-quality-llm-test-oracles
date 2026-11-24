"""Gera avaliacao/resultados-por-caso.md e um resumo de métricas a partir das rodadas.

Uso: python -I tabular.py <rodada> [<rodada> ...]   (a última informada prevalece por ID no acumulado)
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
C3 = os.path.dirname(HERE)
oracle = {c["id"]: c for c in json.load(open(os.path.join(C3, "experimento", "oraculo.json"), encoding="utf-8"))["casos"]}


def bc(rodada):
    p = os.path.join(C3, "resultados", rodada, "jacoco.csv")
    if not os.path.exists(p):
        return None
    rows = list(csv.DictReader(open(p, encoding="utf-8")))
    cov = sum(int(r["BRANCH_COVERED"]) for r in rows)
    mis = sum(int(r["BRANCH_MISSED"]) for r in rows)
    return cov, cov + mis, len(rows)


def load(rodada):
    return json.load(open(os.path.join(C3, "resultados", rodada, "resultados.json"), encoding="utf-8"))


out = ["# Resultados por caso — C3", ""]
summary = {}
acc = {}
for rod in sys.argv[1:]:
    res = load(rod)
    cnt = {}
    for r in res:
        cnt[r["resultado"]] = cnt.get(r["resultado"], 0) + 1
        acc[r["id"]] = (rod, r)
    summary[rod] = (cnt, bc(rod))
    out += [f"## Rodada {rod}", "", "| ID | Título | Oráculo | Resultado | Exit | Detalhe |", "|---|---|---|---|---|---|"]
    for r in res:
        det = "; ".join(("✔ " if v["ok"] else "✘ " if v["ok"] is False else "⚠ ") + v["tipo"] + ": " + v["detalhe"].replace("|", "\\|").replace("\n", " ")
                        for v in r["verificacoes"]) or ("observado: " + (r.get("observacao") or r["stderr_1a_linha"]).replace("|", "\\|"))
        out += [f"| {r['id']} | {r['titulo']} | {r['status_oraculo']} | **{r['resultado']}** | {r['exit']} | {det[:700]} |"]
    out.append("")
open(os.path.join(C3, "avaliacao", "resultados-por-caso.md"), "w", encoding="utf-8").write("\n".join(out))
for rod, (cnt, b) in summary.items():
    print(rod, cnt, b)
cnt = {}
for rod, r in acc.values():
    cnt[r["resultado"]] = cnt.get(r["resultado"], 0) + 1
print("acumulado por ID:", cnt)
