# -*- coding: utf-8 -*-
"""Executa o Z3 independente (nao o mcdc-z3) sobre z3/*.smt2 e grava z3/*.out.
Unknown, timeout ou divergencia da resposta esperada da formula = erro tecnico."""
import glob
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
Z3 = r"C:\Users\User\AppData\Roaming\Python\bin\z3.exe"
TIMEOUT_S = 60

erros = []
total = 0
versao = subprocess.run([Z3, "--version"], capture_output=True, text=True).stdout.strip()
resumo = ["# Versao: " + versao, "# Limite por consulta: %d s" % TIMEOUT_S, "# arquivo\tesperado\tobservado"]
for arq in sorted(glob.glob(os.path.join(AQUI, "z3", "*.smt2"))):
    total += 1
    texto = open(arq, encoding="utf-8").read()
    esperado = [l for l in texto.splitlines() if l.startswith("; Resposta esperada")][0].split(":")[1].strip()
    try:
        p = subprocess.run([Z3, "-smt2", "-T:%d" % TIMEOUT_S, arq], capture_output=True, text=True, timeout=TIMEOUT_S + 10)
        saida = p.stdout
    except subprocess.TimeoutExpired:
        saida = "timeout\n"
    with open(arq[:-5] + ".out", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(saida)
    linhas = [l.strip() for l in saida.splitlines() if l.strip()]
    obs = linhas[0] if linhas else "(vazio)"
    resumo.append("%s\t%s\t%s" % (os.path.basename(arq), esperado, obs))
    if obs != esperado:
        erros.append((os.path.basename(arq), esperado, obs))
with open(os.path.join(AQUI, "z3", "RESUMO.tsv"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(resumo) + "\n")
print(versao)
print("consultas:", total, "divergencias/erros tecnicos:", len(erros))
for e in erros:
    print(e)
sys.exit(1 if erros else 0)
