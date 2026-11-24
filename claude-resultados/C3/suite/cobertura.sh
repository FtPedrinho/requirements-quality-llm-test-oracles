#!/usr/bin/env bash
# Gera o relatório JaCoCo de uma rodada. Uso: cobertura.sh <dir da rodada> <sut_dir> [exec...]
# Denominador: todas as classes de produção dos 4 módulos (classfiles de cada módulo compilado).
set -euo pipefail
export MSYS_NO_PATHCONV=1
R="$1"; SUT="$2"; shift 2
EXECS=("$@"); [ ${#EXECS[@]} -eq 0 ] && EXECS=("$R/jacoco.exec")
CLI="C:/Users/User/.m2/repository/org/jacoco/org.jacoco.cli/0.8.16/org.jacoco.cli-0.8.16-nodeps.jar"
ARGS=()
for m in mcdc-core mcdc-requirements mcdc-z3 mcdc-cli; do
  ARGS+=(--classfiles "$SUT/classes/$m" --sourcefiles "$SUT/src/$m/src/main/java")
done
java -jar "$CLI" report "${EXECS[@]}" "${ARGS[@]}" --csv "$R/jacoco.csv" --xml "$R/jacoco.xml" --html "$R/jacoco-html" --name "C3 $(basename "$R")"
python -I - "$R/jacoco.csv" <<'PY'
import csv, sys
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
cov = sum(int(r["BRANCH_COVERED"]) for r in rows); mis = sum(int(r["BRANCH_MISSED"]) for r in rows)
print(f"classes={len(rows)} branches cobertos={cov} total={cov+mis} BC={100*cov/(cov+mis):.2f}%")
PY
