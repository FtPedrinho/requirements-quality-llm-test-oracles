#!/usr/bin/env bash
# Compila o SUT (commit HEAD) fora do repositório, sem Maven. Uso: build.sh <repo> <destino>
set -euo pipefail
export MSYS_NO_PATHCONV=1
REPO="$1"; DEST="$2"
M2="C:/Users/User/.m2/repository/com/fasterxml/jackson/core"
JACK="$M2/jackson-databind/2.17.2/jackson-databind-2.17.2.jar;$M2/jackson-core/2.17.2/jackson-core-2.17.2.jar;$M2/jackson-annotations/2.17.2/jackson-annotations-2.17.2.jar"
rm -rf "$DEST"; mkdir -p "$DEST/src" "$DEST/classes"
git -C "$REPO" rev-parse HEAD > "$DEST/commit.txt"
git -C "$REPO" archive HEAD mcdc-core mcdc-requirements mcdc-z3 mcdc-cli | tar -x -C "$DEST/src"
CP=""
for m in mcdc-core mcdc-requirements mcdc-z3 mcdc-cli; do
  out="$DEST/classes/$m"; mkdir -p "$out"
  find "$DEST/src/$m/src/main/java" -name '*.java' > "$DEST/$m.sources"
  javac --release 21 -encoding UTF-8 -g -d "$out" -cp "$CP${CP:+;}$JACK" @"$DEST/$m.sources"
  if [ -d "$DEST/src/$m/src/main/resources" ]; then cp -r "$DEST/src/$m/src/main/resources/." "$out/"; fi
  CP="$CP${CP:+;}$out"
done
echo "$CP;$JACK" > "$DEST/classpath.txt"
(cd "$DEST/classes" && find . -name '*.class' | sort | xargs sha256sum) > "$DEST/classes.sha256"
