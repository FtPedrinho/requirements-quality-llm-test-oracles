# Build do SUT usado em C0

- Fontes: `git archive HEAD` (commit 03589c40c3aa07a2138d6923c96049345870a661) dos módulos mcdc-core, mcdc-requirements, mcdc-z3, mcdc-cli, extraído num diretório temporário. As fontes do repositório não foram tocadas.
- O Maven (3.10.1, offline) falhou ao resolver plugins sem rede (`maven-install-plugin`, `maven-compiler-plugin`) e foi registrado como erro técnico de infraestrutura.
- Compilação: `javac --release 21 -encoding UTF-8 -g` (JDK 21.0.3), na ordem core → requirements → z3 → cli. O classpath é o das classes anteriores mais Jackson 2.17.2 (`jackson-cp.txt`). As listas de fontes estão em `src-<módulo>.txt`.
- Resultado: core 38, requirements 9, z3 16 e cli 10 classes (inclusive as internas e as do pacote `mutation`).
- Hashes de cada `.class` em `../CONGELAMENTO-SUITE.sha256`.
