# Suíte C2 — ferramenta MC/DC

## Objetivo

Executar contra a implementação Java real os mesmos comportamentos testados em C1.

## Pré-requisitos

- JDK 21;
- Maven 3.9.x;
- Z3 no `PATH`;
- módulos Maven instalados no repositório local.

## Executar

```powershell
$env:PATH="C:\Users\User\.copilot\session-state\8457bad6-f839-4d1b-96a8-6cea1a9c9dea\files\tools\z3-4.15.4-x64-win\bin;$env:PATH"
& "C:\Users\User\.copilot\session-state\8457bad6-f839-4d1b-96a8-6cea1a9c9dea\files\tools\apache-maven-3.9.11\bin\mvn.cmd" "-f" "experimentacao\experimentacao-2\test-suites\exp2\pom.xml" "clean" "test"
```

## Resultado

- testes: 25;
- aprovados: 25;
- reprovados: 0;
- ignorados: 0;
- não executáveis: 0.

## Relação com C2

Os testes exercitam os comportamentos da implementação. Eles não são derivados de oráculos gerados por LLM nesta etapa, por ausência de execução externa.
