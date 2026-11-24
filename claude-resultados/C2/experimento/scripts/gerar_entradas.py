# -*- coding: utf-8 -*-
"""Gera as entradas próprias da condição C2 (antes de qualquer leitura do SUT).

Os arquivos JSON são gravados com json.dump para preservar barras invertidas
(operadores DFRS /\\ e \\/). Os arquivos de exemplos/ do repositório são usados
apenas como entrada e não são copiados aqui (são referenciados por caminho e
congelados por hash no manifesto).
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "entradas")
os.makedirs(OUT, exist_ok=True)


def wjson(nome, obj):
    with open(os.path.join(OUT, nome), "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def wtxt(nome, txt):
    with open(os.path.join(OUT, nome), "w", encoding="utf-8", newline="\n") as f:
        f.write(txt)


# ---- JSON (formato NAT2TEST descrito na fonte C2) ----
wjson("j15-enum.json", {
    "system": "enum_sys",
    "inputs": [{"name": "m", "type": "enum", "values": ["a", "b", "c"]}],
    "decisions": [{"id": "e#1", "requirement": "REQ-E1",
                   "guard": "m = a \\/ m = b", "actions": ["out := 1"]}],
})
wtxt("j16-invalido.json", "{ \"system\": \"x\", \"inputs\": [ \n")
wjson("j17-ids-repetidos.json", {
    "system": "dup",
    "inputs": [{"name": "p", "type": "bool"}, {"name": "q", "type": "bool"}],
    "decisions": [
        {"id": "d#1", "requirement": "R1", "guard": "p = true", "actions": ["z := 1"]},
        {"id": "d#1", "requirement": "R2", "guard": "q = true", "actions": ["z := 2"]},
    ],
})
wjson("v05-conflito.json", {
    "system": "conf",
    "inputs": [{"name": "x", "type": "int"}, {"name": "s", "type": "bool"}],
    "decisions": [
        {"id": "c#1", "requirement": "R-C1", "guard": "x > 5", "actions": ["y := on"]},
        {"id": "c#2", "requirement": "R-C2", "guard": "x > 3 /\\ s = true", "actions": ["y := off"]},
    ],
})
wjson("v06-mesmo-valor.json", {
    "system": "same",
    "inputs": [{"name": "mode", "type": "enum", "values": ["idle", "busy"]},
               {"name": "s", "type": "bool"}],
    "decisions": [
        {"id": "s#1", "requirement": "R-S1", "guard": "mode = idle /\\ s = true", "actions": ["y := on"]},
        {"id": "s#2", "requirement": "R-S2", "guard": "mode = idle", "actions": ["y := on"]},
    ],
})
wjson("v07-disjuntos.json", {
    "system": "disj",
    "inputs": [{"name": "mode", "type": "enum", "values": ["idle", "busy"]},
               {"name": "s", "type": "bool"}],
    "decisions": [
        {"id": "k#1", "requirement": "R-K1", "guard": "mode = idle /\\ s = true", "actions": ["y := on"]},
        {"id": "k#2", "requirement": "R-K2", "guard": "mode = idle /\\ s = false", "actions": ["y := off"]},
    ],
})
wjson("c06-concretos.json", {
    "system": "conc",
    "inputs": [{"name": "x", "type": "int"}, {"name": "y", "type": "bool"}],
    "decisions": [{"id": "d#1", "requirement": "R-D1",
                   "guard": "x > 5 /\\ y = true", "actions": ["z := 1"]}],
})

# ---- CSV de testes existentes ----
wtxt("c02-completo.csv", "test,input,value\nT1,A,T\nT1,B,T\nT2,A,F\nT2,B,T\nT3,A,T\nT3,B,F\n")
wtxt("c03-incompleto.csv", "test,input,value\nT1,A,T\nT1,B,T\nT2,A,F\nT2,B,T\n")
wtxt("c04-esperado-errado.csv",
     "test,input,value,expected_outcome\nT1,A,T,T\nT1,B,T,T\nT2,A,F,F\nT2,B,T,F\nT3,A,T,T\nT3,B,F,T\n")
wtxt("c06-concretos.csv",
     "decision,test,input,value,expected_outcome\n"
     "d#1,T1,x,7,T\nd#1,T1,y,true,T\n"
     "d#1,T2,x,3,F\nd#1,T2,y,true,F\n"
     "d#1,T3,x,7,F\nd#1,T3,y,false,F\n")
wtxt("c07-coluna-faltando.csv", "test,input\nT1,A\nT1,B\n")

# ---- Arquivos .mcdc ----
wtxt("m03-comentarios.mcdc", "# comentário inicial\nREQ-X: A and B\n# comentário final\n")
wtxt("m04-erro-sintaxe.mcdc", "REQ-1: A and\n")
wtxt("m05-sem-id.mcdc", "A and B\n")


# ---- Expressões geradas (grandes) ----
def grupos(n_grupos, extra=None):
    g = ["(x%d or x%d)" % (2 * i + 1, 2 * i + 2) for i in range(n_grupos)]
    if extra:
        g.append(extra)
    return " and ".join(g)


expr = {
    "e20": grupos(10),
    "e21": grupos(10, "x21"),
    "e13": grupos(6, "x13"),
    "e26": grupos(13),
    "e31": grupos(15, "x31"),
    "paridade3": "(A and not B and not C) or (not A and B and not C) or (not A and not B and C) or (A and B and C)",
}
wjson("expressoes-geradas.json", expr)
print("entradas geradas em", OUT)
