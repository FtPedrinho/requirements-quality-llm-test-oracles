# -*- coding: utf-8 -*-
"""Gera avaliacao/resultados-por-caso.md a partir das rodadas em resultados/."""
import json
import os
import sys

C2 = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
rodadas = sys.argv[1:]


def short(x, n=160):
    s = json.dumps(x, ensure_ascii=False) if not isinstance(x, str) else x
    s = s.replace("|", "\\|").replace("\n", " ")
    return s if len(s) <= n else s[:n] + "…"


L = ["# Resultados por caso — C2", ""]
for rd in rodadas:
    R = json.load(open(os.path.join(C2, "resultados", rd, "resultados.json"), encoding="utf-8"))
    m = R["meta"]
    L += ["## Rodada `%s`" % rd, "", "Início %s, fim %s. Contagem: %s." % (m["inicio"], m["fim"], json.dumps(m["contagem"], ensure_ascii=False)), "",
          "| ID | Resultado | Código | Asserções falhas (esperado → observado) / diagnóstico |", "|---|---|---|---|"]
    for c in R["casos"]:
        if c["resultado"] == "FALHOU":
            det = "; ".join("%s: %s → %s" % (a["assercao"], short(a["esperado"], 60), short(a["observado"])) for a in c["assercoes"] if not a["ok"])
        elif c["resultado"] == "INDETERMINADO":
            det = "diagnóstico: " + short(c.get("diagnostico_saida") or "", 120)
        elif c["resultado"] == "ERRO_TECNICO":
            det = c["erro_tecnico"]
        else:
            det = "%d asserções satisfeitas" % len(c["assercoes"])
        L.append("| %s | %s | %s | %s |" % (c["id"], c["resultado"], c["exit"], det))
    L.append("")
L.append("Detalhe completo (todas as asserções, observações e comandos): `resultados/<rodada>/resultados.json`; stdout/stderr em `resultados/<rodada>/casos/<ID>/`.")
open(os.path.join(C2, "avaliacao", "resultados-por-caso.md"), "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("ok")
