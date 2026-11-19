# Suíte EXP0 — Testes reais da ferramenta MC/DC

Esta suíte usa o mesmo conjunto de testes do EXP1 contra o SUT real.

Ela não usa VM, TIS ou NPP como sistema sob teste.

## Pré-requisitos

- JDK 21;
- Maven 3.9.x;
- Z3 no `PATH`.

## Instalação

Na raiz:

```powershell
& "<MAVEN_BIN>\mvn.cmd" "-q" "-DskipTests" "-Djacoco.skip=true" "install"
```

## Execução

```powershell
& "<MAVEN_BIN>\mvn.cmd" "-f" "experimentacao\experimentacao-0\test-suites\exp0\pom.xml" "test"
```

## Relatórios

- `target/surefire-reports/TEST-io.github.rvdomingos.mcdc.cli.Exp0McdcSuiteTest.xml`;
- `target/surefire-reports/io.github.rvdomingos.mcdc.cli.Exp0McdcSuiteTest.txt`.
