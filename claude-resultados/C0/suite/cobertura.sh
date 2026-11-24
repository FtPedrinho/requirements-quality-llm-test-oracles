#!/usr/bin/env bash
# Gera o relatorio JaCoCo da rodada: todas as classes de producao dos 4 modulos (inclusive nao carregadas).
# Uso: bash cobertura.sh <rodada>
set -e
export MSYS_NO_PATHCONV=1
HERE="$(cd "$(dirname "$0")" && pwd -W)"; C0="$(dirname "$HERE")"; R="$C0/resultados/$1"
CLI=$(python -c "import json;print(json.load(open(r'$HERE/config.json'))['jacoco_cli'])")
B=$(python -c "import json;print(json.load(open(r'$HERE/config.json'))['sut_build'])")
REPO="$(dirname "$(dirname "$C0")")"
java -jar "$CLI" report "$R/jacoco.exec" \
  --classfiles "$B/classes/mcdc-core" --classfiles "$B/classes/mcdc-requirements" \
  --classfiles "$B/classes/mcdc-z3" --classfiles "$B/classes/mcdc-cli" \
  --sourcefiles "$REPO/mcdc-core/src/main/java" --sourcefiles "$REPO/mcdc-requirements/src/main/java" \
  --sourcefiles "$REPO/mcdc-z3/src/main/java" --sourcefiles "$REPO/mcdc-cli/src/main/java" \
  --csv "$R/jacoco.csv" --html "$R/jacoco-html" --xml "$R/jacoco.xml" --name "C0 $1"
python - "$R/jacoco.csv" <<'PY'
import csv, sys, collections
rows = list(csv.DictReader(open(sys.argv[1])))
tot = collections.defaultdict(lambda: [0, 0])
for r in rows:
    m = r["PACKAGE"].split(".")[4]
    tot[m][0] += int(r["BRANCH_COVERED"]); tot[m][1] += int(r["BRANCH_COVERED"]) + int(r["BRANCH_MISSED"])
c = sum(v[0] for v in tot.values()); t = sum(v[1] for v in tot.values())
for m, (a, b) in sorted(tot.items()): print(f"{m}: {a}/{b} = {100*a/b:.1f}%")
print(f"classes no relatorio: {len(rows)}")
print(f"TOTAL Branch Coverage: {c}/{t} = {100*c/t:.2f}%")
PY
