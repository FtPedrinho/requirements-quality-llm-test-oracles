# -*- coding: utf-8 -*-
"""Gera avaliacao/resultados-por-caso.md a partir do oráculo congelado e de resultados/<rodada>/resultados.json."""
import json
import os
import sys

C4 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rodada = sys.argv[1] if len(sys.argv) > 1 else "r1-baseline"
orc = {c["id"]: c for c in json.load(open(os.path.join(C4, "experimento", "oraculo.json"), encoding="utf-8"))["casos"]}
res = json.load(open(os.path.join(C4, "resultados", rodada, "resultados.json"), encoding="utf-8"))


def cel(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


md = ["# Resultados por caso — C4 (rodada `%s`, final)" % rodada, "",
      "Gerado por `avaliacao/gerar_resultados_por_caso.py` a partir de `experimento/oraculo.json` e "
      "`resultados/%s/resultados.json`." % rodada, "",
      "Contagem: " + ", ".join("%s = %d" % (k, v) for k, v in sorted(res["contagem"].items())), "",
      "Unidade de contagem: caso do oráculo (ID estável). Códigos de saída são registrados, mas nenhum caso os exige.", "",
      "## Casos determinados", "",
      "| ID | Execução | Expectativa | Resultado | Observado | Exit |", "|---|---|---|---|---|---|"]
for c in res["casos"]:
    if c["status_oraculo"] != "DETERMINADO":
        continue
    md.append("| %s | %s | %s | **%s** | %s | %s |" % (c["id"], c["execucao"], cel(c["expectativa"]), c["resultado"],
                                                       cel(c["observado"])[:400], cel(c.get("exit_codes", ""))))
md += ["", "## Casos indeterminados (não executados)", "", "| ID | Entrada/tema | Motivo |", "|---|---|---|"]
for c in res["casos"]:
    if c["status_oraculo"] == "INDETERMINADO":
        o = orc[c["id"]]
        md.append("| %s | %s | %s |" % (c["id"], cel(o["entrada"]), cel(o["justificativa"])))
md += ["", "## Execuções", "", "| Execução | Argumentos | Exit |", "|---|---|---|"]
for x, e in res["execucoes"].items():
    md.append("| %s | `%s` | %s |" % (x, cel(" ".join(e["args"]))[:200], e["exit"]))
with open(os.path.join(C4, "avaliacao", "resultados-por-caso.md"), "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(md) + "\n")
print("ok")
