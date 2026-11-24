#!/usr/bin/env bash
# Compila o SUT (4 módulos) fora do repositório a partir de `git archive HEAD`, sem modificá-lo.
# Uso: bash build.sh <diretório-de-trabalho>   (Git Bash, Windows)
set -euo pipefail
export MSYS_NO_PATHCONV=1
W="$1"
REPO="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
M2="C:/Users/User/.m2/repository/com/fasterxml/jackson/core"
JACKSON="$M2/jackson-databind/2.17.2/jackson-databind-2.17.2.jar;$M2/jackson-core/2.17.2/jackson-core-2.17.2.jar;$M2/jackson-annotations/2.17.2/jackson-annotations-2.17.2.jar"
rm -rf "$W" && mkdir -p "$W/src" "$W/classes"
git -C "$REPO" archive HEAD mcdc-core mcdc-requirements mcdc-z3 mcdc-cli | tar -x -C "$W/src"
CP=""
for m in mcdc-core mcdc-requirements mcdc-z3 mcdc-cli; do
  mkdir -p "$W/classes/$m"
  find "$W/src/$m/src/main/java" -name '*.java' > "$W/$m.sources"
  javac --release 21 -encoding UTF-8 -g -d "$W/classes/$m" -cp "${CP}${JACKSON}" @"$W/$m.sources"
  # recursos não-Java, se houver
  if [ -d "$W/src/$m/src/main/resources" ]; then cp -r "$W/src/$m/src/main/resources/." "$W/classes/$m/"; fi
  CP="${CP}$W/classes/$m;"
done
echo "${CP}${JACKSON}" > "$W/runtime.classpath"
echo "OK: $(find "$W/classes" -name '*.class' | wc -l) classes"
