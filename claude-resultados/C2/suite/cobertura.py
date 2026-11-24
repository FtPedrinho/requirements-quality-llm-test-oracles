# -*- coding: utf-8 -*-
"""Relatório JaCoCo (CSV, XML, HTML) de uma rodada ou do acumulado.

Uso: python cobertura.py <pasta-da-rodada> [exec adicional ...]
Com mais de um .exec, faz o merge em <pasta>/jacoco.exec antes do relatório (acumulado).
Denominador: todas as classes de produção dos quatro módulos (--classfiles de cada módulo
compilado em experimento/build/classes), carregadas ou não.
"""
import csv
import json
import os
import subprocess
import sys

SUITE = os.path.dirname(os.path.abspath(__file__))
C2 = os.path.dirname(SUITE)
REPO = os.path.abspath(os.path.join(C2, "..", ".."))
CLASSES = os.path.join(C2, "experimento", "build", "classes")
CLI = os.path.expanduser("~/.m2/repository/org/jacoco/org.jacoco.cli/0.8.16/org.jacoco.cli-0.8.16-nodeps.jar")
MODS = ["mcdc-core", "mcdc-requirements", "mcdc-z3", "mcdc-cli"]


def main():
    rd = os.path.abspath(sys.argv[1])
    execs = [os.path.abspath(x) for x in sys.argv[2:]]
    ex = os.path.join(rd, "jacoco.exec")
    if execs:
        subprocess.run(["java", "-jar", CLI, "merge"] + execs + ["--destfile", ex], check=True)
    cmd = ["java", "-jar", CLI, "report", ex]
    for m in MODS:
        cmd += ["--classfiles", os.path.join(CLASSES, m)]
        cmd += ["--sourcefiles", os.path.join(REPO, m, "src", "main", "java")]
    cmd += ["--csv", os.path.join(rd, "jacoco.csv"), "--xml", os.path.join(rd, "jacoco.xml"),
            "--html", os.path.join(rd, "jacoco-html"), "--name", "C2 " + os.path.basename(rd)]
    subprocess.run(cmd, check=True)
    tot = {"BRANCH_COVERED": 0, "BRANCH_MISSED": 0, "LINE_COVERED": 0, "LINE_MISSED": 0}
    pacotes, classes = {}, 0
    for r in csv.DictReader(open(os.path.join(rd, "jacoco.csv"), encoding="utf-8")):
        classes += 1
        for k in tot:
            tot[k] += int(r[k])
        p = pacotes.setdefault(r["PACKAGE"], [0, 0])
        p[0] += int(r["BRANCH_COVERED"])
        p[1] += int(r["BRANCH_COVERED"]) + int(r["BRANCH_MISSED"])
    total = tot["BRANCH_COVERED"] + tot["BRANCH_MISSED"]
    res = {"classes": classes, "branches_cobertos": tot["BRANCH_COVERED"], "branches_total": total,
           "branch_coverage_pct": round(100.0 * tot["BRANCH_COVERED"] / total, 2) if total else "não calculável",
           "linhas_cobertas": tot["LINE_COVERED"], "linhas_total": tot["LINE_COVERED"] + tot["LINE_MISSED"],
           "por_pacote": {k: {"cobertos": a, "total": b} for k, (a, b) in pacotes.items()},
           "ferramenta": "JaCoCo 0.8.16 (agente + CLI)", "execs": execs or [ex]}
    json.dump(res, open(os.path.join(rd, "cobertura.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps({k: v for k, v in res.items() if k != "por_pacote"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
