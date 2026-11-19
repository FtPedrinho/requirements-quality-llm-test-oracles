# Suíte EXP1 — Testes reais da ferramenta MC/DC

Esta suíte é executada contra a implementação Java real da ferramenta.

Ela não usa VM, TIS ou NPP como sistema sob teste.

## Pré-requisitos

- JDK 21;
- Maven 3.9.x;
- Z3 no `PATH`;
- módulos Java instalados no Maven local.

## Instalação dos módulos

Na raiz do repositório:

```powershell
$env:PATH="C:\Users\User\.copilot\session-state\8457bad6-f839-4d1b-96a8-6cea1a9c9dea\files\tools\z3-4.15.4-x64-win\bin;$env:PATH"
& "C:\Users\User\.copilot\session-state\8457bad6-f839-4d1b-96a8-6cea1a9c9dea\files\tools\apache-maven-3.9.11\bin\mvn.cmd" "-q" "-DskipTests" "-Djacoco.skip=true" "install"
```

## Execução

```powershell
$env:PATH="C:\Users\User\.copilot\session-state\8457bad6-f839-4d1b-96a8-6cea1a9c9dea\files\tools\z3-4.15.4-x64-win\bin;$env:PATH"
& "C:\Users\User\.copilot\session-state\8457bad6-f839-4d1b-96a8-6cea1a9c9dea\files\tools\apache-maven-3.9.11\bin\mvn.cmd" "-f" "experimentacao\experimentacao-1\test-suites\exp1\pom.xml" "test"
```

## Relatórios

- XML: `target/surefire-reports/TEST-io.github.rvdomingos.mcdc.cli.Exp1McdcSuiteTest.xml`;
- texto: `target/surefire-reports/io.github.rvdomingos.mcdc.cli.Exp1McdcSuiteTest.txt`.

## Rastreabilidade

- `test-catalog.csv`;
- `traceability.csv`.

Os testes foram derivados do gabarito independente de comportamentos da ferramenta. O catálogo de oráculos externo permanece pendente até o uso de um LLM externo.
