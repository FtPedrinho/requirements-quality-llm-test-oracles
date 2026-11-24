#!/usr/bin/env bash
# Gera o relatório JaCoCo de uma rodada (CSV, XML, HTML) e calcula a Branch Coverage.
# Denominador: todas as classes de produção dos 4 módulos compilados (inclusive não carregadas e de mutação).
# Uso: cobertura.sh <dir-sut (classes/ e src/)> <dir-da-rodada>
set -euo pipefail
export MSYS_NO_PATHCONV=1
SUT="$1"; R="$2"
CLI="C:/Users/User/.m2/repository/org/jacoco/org.jacoco.cli/0.8.16/org.jacoco.cli-0.8.16-nodeps.jar"
args=()
for m in mcdc-core mcdc-requirements mcdc-z3 mcdc-cli; do
  args+=(--classfiles "$SUT/classes/$m" --sourcefiles "$SUT/src/$m/src/main/java")
done
java -jar "$CLI" report "$R/jacoco.exec" "${args[@]}" --name "C4" \
  --csv "$R/jacoco.csv" --xml "$R/jacoco.xml" --html "$R/jacoco-html" > "$R/jacoco-report.log" 2>&1
python -I - "$R/jacoco.csv" > "$R/branch-coverage.txt" <<'EOF'
import csv, sys
cov = mis = 0
mod = {}
for r in csv.DictReader(open(sys.argv[1], encoding="utf-8")):
    c, m = int(r["BRANCH_COVERED"]), int(r["BRANCH_MISSED"])
    cov += c; mis += m
    k = r["PACKAGE"]
    a = mod.setdefault(k, [0, 0]); a[0] += c; a[1] += m
tot = cov + mis
print("Branch Coverage: %d / %d = %s%%" % (cov, tot, ("%.2f" % (100.0 * cov / tot)) if tot else "não calculável"))
print("Classes no CSV: %d" % sum(1 for _ in csv.DictReader(open(sys.argv[1], encoding="utf-8"))))
for k, (c, m) in sorted(mod.items()):
    print("  %s: %d / %d" % (k, c, c + m))
EOF
cat "$R/branch-coverage.txt"
