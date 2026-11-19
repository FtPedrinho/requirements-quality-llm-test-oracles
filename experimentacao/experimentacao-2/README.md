# Experimento C2 — extrema baixa clareza, alta consistência

O C2 reduz a clareza documental do C1 ao nível extremo sem alterar limites, códigos, comandos, formatos, regras ou ações.

## Estrutura

- `audit/`: inventário C1 e integridade;
- `documentation/`: cópia C2;
- `documentation-assessment/`: avaliação C1/C2;
- `z3/`: equivalência e consistência das propriedades formais;
- `oracle-reference/`: gabarito independente;
- `oracle-generation/`: status da geração por LLM;
- `oracle-evaluation/`: TP/FP/FN futuros;
- `test-suites/exp2/`: testes JUnit reais;
- `execution-results/`: resultados Surefire;
- `mutation-testing/`: PIT;
- `comparison/`: comparação C1/C2;
- `experiment-status.md`.

## Relatórios consolidados

- [Resumo C0/C1/C2](consolidated-experiment-report.md)

## Sessão da suíte

- [test-suite-session.md](test-suites/exp2/test-suite-session.md)
- [relatório dos erros documentais](suite-error-report.md)

## Estado atual

- documentação C2 criada;
- clareza reduzida;
- consistência preservada;
- propriedades Z3 sem divergência formal encontrada;
- suíte C2 ampliada: 36 testes executados, 26 aprovados, 10 erros documentais, 0 ignorados;
- PIT: 333 mutantes, 320 mortos, 96%;
- geração por LLM externa: não executada nesta sessão;
- Precision/Recall/F1: 1,0 / 0,5294 / 0,6923 nesta geração pelo agente atual.
