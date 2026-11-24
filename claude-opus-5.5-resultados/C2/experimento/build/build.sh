#!/usr/bin/env bash
# Reproduz o build do SUT usado no C2 (Git Bash no Windows; Maven não é usado).
# Uso: bash build.sh <pasta-de-trabalho-fora-do-repositorio>
set -euo pipefail
export MSYS_NO_PATHCONV=1
REPO="C:/Users/User/requirements-quality-llm-test-oracles"
W="${1:?pasta de trabalho}"
M="$HOME/.m2/repository/com/fasterxml/jackson/core"
J="$M/jackson-databind/2.17.2/jackson-databind-2.17.2.jar;$M/jackson-core/2.17.2/jackson-core-2.17.2.jar;$M/jackson-annotations/2.17.2/jackson-annotations-2.17.2.jar"
mkdir -p "$W/src" "$W/classes"
git -C "$REPO" archive ed7d2e00170e3e2c28201bf63e1b51a24a1bfe81 mcdc-core mcdc-requirements mcdc-z3 mcdc-cli | tar -x -C "$W/src"
cp=""
for m in mcdc-core mcdc-requirements mcdc-z3 mcdc-cli; do
  mkdir -p "$W/classes/$m"
  find "$W/src/$m/src/main/java" -name '*.java' > "$W/$m.srcs"
  javac --release 21 -encoding UTF-8 -g -d "$W/classes/$m" -cp "$cp$J" "@$W/$m.srcs"
  cp="$cp$W/classes/$m;"
done
echo "${cp}${J}"
