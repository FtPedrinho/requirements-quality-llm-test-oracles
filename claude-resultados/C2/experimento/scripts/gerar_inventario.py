# -*- coding: utf-8 -*-
"""Gera experimento/inventario-casos.md a partir de experimento/oraculo.json."""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
o = json.load(open(os.path.join(BASE, "oraculo.json"), encoding="utf-8"))
L = ["# Inventário de casos do oráculo C2", "",
     "Gerado de `oraculo.json` (congelado antes da leitura do SUT).", "",
     o["unidade_de_contagem"], "",
     "| ID | Categoria | Status | Comando | Linhas | Expectativa / motivo | Z3 |",
     "|---|---|---|---|---|---|---|"]


def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


for c in o["casos"]:
    cmd = " ".join(("'%s'" % a if " " in a else a) for a in c["comando"])
    exp = json.dumps(c["expectativa"], ensure_ascii=False) if c["expectativa"] else "INDETERMINADO: " + (c["motivo_indeterminacao"] or "")
    L.append("| %s | %s | %s | `%s` | %s | %s | %s |" % (
        c["id"], c["categoria"], c["status"], esc(cmd), esc(", ".join(t["linha"] for t in c["trechos"])),
        esc(exp), esc(", ".join(c["z3"]))))
L += ["", "Trechos literais, regra e justificativa completos de cada caso estão em `oraculo.json`."]
open(os.path.join(BASE, "inventario-casos.md"), "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("ok")
