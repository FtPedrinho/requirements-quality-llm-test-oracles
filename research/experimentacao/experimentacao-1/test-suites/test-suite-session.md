# Sessão das suítes — Experimento 1 reconstruído

## Ambiente

- commit: `256e78f404527bcdfa76e7629c83376d4d719c3d`;
- Java: 21.0.3;
- Maven: 3.9.11;
- Z3: 4.15.4;
- Sistema sob teste: implementação Java da ferramenta MC/DC.

## Diferença da condição documental

Esta sessão usa a documentação aprimorada C1 do Experimento 1.

Na implementação e na suíte real, não houve mudança no código do SUT nem nas fontes de entrada dos testes.

## Suíte real contra a CLI

- casos selecionados: 21;
- casos aprovados: 21;
- casos falhos: 0;
- casos não avaliáveis: 0.

Os mesmos comportamentos do Experimento 0 foram testados para manter comparabilidade.

## Mutation Testing real

O PIT foi executado sobre `mcdc-core`:

- mutantes: 333;
- mortos: 320;
- sobreviventes: 1;
- sem cobertura: 12;
- timed out: 1;
- mutation coverage: 96%.

O registro completo está em `../mutations/mcdc-core-mutations.xml`.

## Limitação

Os mesmos resultados de suíte e PIT nos Experimentos 0 e 1 não demonstram melhoria na qualidade dos oráculos. Os oráculos LLM ainda não foram gerados em execução controlada nem classificados com TP/FP/FN.
