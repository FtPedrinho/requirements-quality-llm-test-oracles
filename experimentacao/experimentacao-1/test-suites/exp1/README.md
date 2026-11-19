# Suíte C1 — Testes reais da ferramenta MC/DC

Esta suíte executa contra a implementação Java real da ferramenta. Ela não usa VM, TIS ou NPP como sistema sob teste.

## Pré-requisitos e instalação

Requer JDK 21, Maven 3.9.x, Z3 no `PATH` e os módulos do repositório instalados localmente. Na raiz:

```powershell
mvn -q -DskipTests -Djacoco.skip=true install
```

## Execução

```powershell
mvn -f experimentacao\experimentacao-1\test-suites\exp1\pom.xml test
```

## Relatórios

- XML: `target/surefire-reports/TEST-io.github.rvdomingos.mcdc.cli.Exp1McdcSuiteTest.xml`;
- texto: `target/surefire-reports/io.github.rvdomingos.mcdc.cli.Exp1McdcSuiteTest.txt`.

## Rastreabilidade

- `test-catalog.csv`;
- `traceability.csv`.

Os testes foram derivados do gabarito independente de comportamentos da ferramenta. O catálogo de oráculos externo permanece pendente até o uso de um LLM externo.
