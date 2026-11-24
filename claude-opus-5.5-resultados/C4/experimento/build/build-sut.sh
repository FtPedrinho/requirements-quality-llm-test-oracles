#!/usr/bin/env bash
# Compila o SUT (commit HEAD) fora do repositório, sem Maven.
# Uso: build-sut.sh <repo> <dir-de-trabalho>
set -euo pipefail
export MSYS_NO_PATHCONV=1
REPO="$1"; W="$2"
M2="C:/Users/User/.m2/repository/com/fasterxml/jackson/core"
JACK="$M2/jackson-databind/2.17.2/jackson-databind-2.17.2.jar;$M2/jackson-core/2.17.2/jackson-core-2.17.2.jar;$M2/jackson-annotations/2.17.2/jackson-annotations-2.17.2.jar"
rm -rf "$W/src" "$W/classes"
mkdir -p "$W/src" "$W/classes"
git -C "$REPO" rev-parse HEAD > "$W/commit.txt"
git -C "$REPO" archive HEAD mcdc-core mcdc-requirements mcdc-z3 mcdc-cli | tar -x -C "$W/src"
cp=""
for m in mcdc-core mcdc-requirements mcdc-z3 mcdc-cli; do
  mkdir -p "$W/classes/$m"
  find "$W/src/$m/src/main/java" -name '*.java' > "$W/$m-fontes.txt"
  javac --release 21 -encoding UTF-8 -g -d "$W/classes/$m" -cp "$JACK${cp}" @"$W/$m-fontes.txt"
  if [ -d "$W/src/$m/src/main/resources" ]; then cp -r "$W/src/$m/src/main/resources/." "$W/classes/$m/"; fi
  cp="$cp;$W/classes/$m"
done
echo "$JACK$cp" > "$W/classpath.txt"
(cd "$W/classes" && find . -type f | sort | xargs sha256sum) > "$W/classes.sha256"
echo OK
