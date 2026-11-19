# Relatório consolidado — Experimentos C0/C1/C2

## C0 — documentação original

- Objetivo: linha de base histórica.
- SUT: ferramenta MC/DC.
- Oráculos históricos: relacionados a VM, TIS e NPP, não ao SUT.
- Suíte real nova: 25 testes JUnit contra a CLI; 25 aprovados.
- PIT: 333 mutantes em `mcdc-core`, 320 mortos, 96,096% de mutation coverage.
- Status metodológico: artefatos históricos preservados; não servem como evidência direta da qualidade dos oráculos da ferramenta.

## C1 — alta clareza / alta consistência

- Documentação revisada do SUT.
- Suíte real: 25 testes JUnit; 25 aprovados.
- PIT: 333 mutantes, 320 mortos, 96,096%.
- Geração de oráculos por LLM externo não registrada nesta execução.
- TP/FP/FN e Precision/Recall/F1 não podem ser comparados diretamente ao C2 sem geração controlada.

## C2 — extrema baixa clareza

- Documentação literal usada sem correção ou preenchimento por C1.
- 34 comportamentos no gabarito.
- 18 TP, 0 FP, 16 FN, 0 não avaliáveis.
- Precision: 1,000.
- Recall: 0,5294.
- F1: 0,6923.

## Suíte C2

- 36 testes registrados;
- 26 aprovados;
- 10 erros documentais;
- 0 ignorados.
- 0 reprovados.

Os 10 erros representam lacunas reais da documentação C2:

- formato CSV de check;
- entradas repetidas;
- linhas impossíveis;
- algoritmo guloso;
- detalhes da busca exata;
- semântica de Mutation Score;
- sobreposição compatível;
- Z3 UNKNOWN;
- formato truth-csv;
- truncamento de pares.

## Interpretação

A documentação C2 produziu 18 comportamentos corretamente especificados e 16 FN. Precision permaneceu 1,0 porque não foram encontrados FP, mas Recall caiu para 0,5294 e F1 para 0,6923.

Os 10 erros não são falhas da implementação. São resultados deliberados da falta de informação suficiente na documentação C2.

## Arquivos principais

- [Métricas C2](experimentacao/experimentacao-2/metrics/oracle-metrics.csv)
- [Suíte C2](experimentacao/experimentacao-2/test-suite/README.md)
- [Resultados C2](experimentacao/experimentacao-2/execution/execution-summary.md)
- [Relatório C2](experimentacao/experimentacao-2/experiment-report.md)
- [Comparação C1/C2](experimentacao/experimentacao-2/comparison/c1-c2-analysis.md)
