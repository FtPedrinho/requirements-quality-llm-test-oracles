# Build do SUT (C2)

- Commit de referência: ed7d2e00170e3e2c28201bf63e1b51a24a1bfe81
- Fonte: `git archive HEAD mcdc-core mcdc-requirements mcdc-z3 mcdc-cli`, extraído fora do repositório.
- Compilador: javac 21.0.3; `javac --release 21 -encoding UTF-8 -g`, ordem core → requirements → z3 → cli.
- Dependências: Jackson 2.17.2 (databind, core, annotations) de ~/.m2. Maven não usado (offline, sem plugins).
- Resultado: 4 módulos com rc=0, 73 classes de produção (ver build.log, *.srcs).
- Classpath usado pela suíte: classpath.txt.
- JVM de execução: java version "21.0.3" 2024-04-16 LTS.
- Z3 do processo do SUT: C:/Users/User/AppData/Roaming/Python/bin/z3.exe (Z3 version 5.4.1 - 64 bit - build hashcode 145c0c51570a357cc558ce898ce77573ba9d4fbf), no PATH só do processo, conforme pré-condição de cada caso.
