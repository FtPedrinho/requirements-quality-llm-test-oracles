# Sessão das suítes — Experimento 0 reconstruído

## Ambiente

- commit: `256e78f404527bcdfa76e7629c83376d4d719c3d`;
- Java: 21.0.3;
- Maven: 3.9.11;
- Z3: 4.15.4;
- Sistema sob teste: implementação Java da ferramenta MC/DC.

## Suíte real contra a CLI

- casos selecionados: 21;
- casos aprovados: 21;
- casos falhos: 0;
- casos não avaliáveis: 0.

Cobertura desta sessão:

- comando sem argumentos;
- opção desconhecida;
- expressão inválida;
- arquivo `.mcdc`;
- arquivo vazio;
- JSON sem decisões;
- CSV com cabeçalho incompleto;
- tabela verdade;
- mascaramento;
- causa única;
- suíte gulosa;
- suíte exata;
- modo direto;
- fronteiras;
- mutação interna;
- conflito e lacuna;
- relatórios JSON/CSV/truth-csv;
- ausência de Z3.

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

Esta sessão não mede oráculos gerados por LLM. Os oráculos ainda não possuem classificação TP/FP/FN independente.
