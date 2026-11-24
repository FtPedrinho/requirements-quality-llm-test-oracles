#!/usr/bin/env bash
# Gera o relatório JaCoCo (CSV, XML, HTML) de uma rodada. Denominador: todas as classes de produção
# dos 4 módulos compilados (inclusive não carregadas); harness e bibliotecas externas ficam de fora.
# Uso: bash coverage.sh <dir-build> <dir-rodada> [exec1 exec2 ...]   (sem execs: <dir-rodada>/jacoco.exec)
set -euo pipefail
export MSYS_NO_PATHCONV=1
W="$1"; R="$2"; shift 2
CLI="C:/Users/User/.m2/repository/org/jacoco/org.jacoco.cli/0.8.16/org.jacoco.cli-0.8.16-nodeps.jar"
EXECS=("$@"); [ ${#EXECS[@]} -eq 0 ] && EXECS=("$R/jacoco.exec")
ARGS=()
for m in mcdc-core mcdc-requirements mcdc-z3 mcdc-cli; do
  ARGS+=(--classfiles "$W/classes/$m" --sourcefiles "$W/src/$m/src/main/java")
done
if [ ${#EXECS[@]} -gt 1 ]; then
  java -jar "$CLI" merge "${EXECS[@]}" --destfile "$R/jacoco.exec"
fi
java -jar "$CLI" report "$R/jacoco.exec" "${ARGS[@]}" --encoding UTF-8 --name "MC/DC C1" \
  --csv "$R/jacoco.csv" --xml "$R/jacoco.xml" --html "$R/jacoco-html"
python -I - "$R/jacoco.csv" <<'EOF'
import csv, sys
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
cov = sum(int(r["BRANCH_COVERED"]) for r in rows); mis = sum(int(r["BRANCH_MISSED"]) for r in rows)
lc = sum(int(r["LINE_COVERED"]) for r in rows); lm = sum(int(r["LINE_MISSED"]) for r in rows)
print(f"classes={len(rows)} branches={cov}/{cov+mis} ({100*cov/(cov+mis):.2f}%) linhas={lc}/{lc+lm}")
for g in sorted({r['GROUP'] for r in rows} | {r['PACKAGE'] for r in rows}):
    pass
by = {}
for r in rows:
    k = r["PACKAGE"]; c, m = by.get(k, (0, 0)); by[k] = (c + int(r["BRANCH_COVERED"]), m + int(r["BRANCH_MISSED"]))
for k, (c, m) in sorted(by.items()):
    print(f"  {k}: {c}/{c+m}")
EOF
