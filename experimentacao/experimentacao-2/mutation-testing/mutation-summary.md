# Mutation Testing C2 — resumo PIT

## Escopo e método

O mutation testing foi executado com PIT 1.30.2 sobre as classes de produção de `mcdc-core`, usando o mesmo conjunto de **456 IDs de mutantes** para S1, S2 e S3. Os resultados completos por mutante, com `killing_test`, são `mutation-results-original.csv`, `mutation-results-complementary.csv` e `mutation-results-combined.csv`.

As categorias neste relatório seguem estritamente o status de cada linha:

- `KILLED` → **Killed**; somente estes contam em K.
- `SURVIVED` → **Survived**.
- equivalente → **Equivalent**; nenhum equivalente foi identificado pelo PIT. Não houve detector de equivalência, portanto equivalência não foi descartada.
- `NO_COVERAGE` → **No coverage**.
- `TIMED_OUT` → **Timed out**, separado mesmo que o campo PIT `detected` esteja true.
- `ERROR`/`NOT_STARTED` → **Non-viable / Error**; nenhum caso nos conjuntos primários.

O denominador usa a fórmula solicitada, `M-E`, sem excluir mutantes sem cobertura ou timed out. Timeout não é contabilizado como morto.

## Resultados

| Cenário | Killed | Survived | Equivalent identificado | No coverage | Timed out | Non-viable / Error | Total | Mutation Score |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| S1 — originais | 152 | 155 | 0 | 144 | 5 | 0 | 456 | 152/(456-0) = **33,33%** |
| S2 — complementares | 198 | 167 | 0 | 90 | 1 | 0 | 456 | 198/(456-0) = **43,42%** |
| S3 — combinada | 218 | 162 | 0 | 71 | 5 | 0 | 456 | 218/(456-0) = **47,81%** |

S3 matou 66 mutantes a mais que S1 e 20 a mais que S2, sem eliminar os kills de cada conjunto individual. Permanecem 162 sobreviventes em S3; eles não foram omitidos nem tratados como equivalentes.

O PIT aplicou dez famílias padrão de mutadores de bytecode: `NegateConditionals` (164), `EmptyObjectReturnVals` (76), `NullReturnVals` (59), `Math` (40), `BooleanTrueReturnVals` (32), `BooleanFalseReturnVals` (30), `VoidMethodCall` (22), `ConditionalsBoundary` (16), `PrimitiveReturns` (14) e `Increments` (3). Isso cobre negação/condições, limites, aritmética e resultados booleanos/retornos. A população não contém troca direta de operadores lógicos AND/OR nem mutadores customizados para remoção específica de validações; portanto, essas classes de mutação não podem ser alegadas como testadas. O registro completo fornece classe, método, linha, mutador, descrição, status e teste apontado por PIT. Mutantes sem cobertura não foram interpretados como sobreviventes mortos; timeouts não foram interpretados como kills.

## Interpretação semântica

S2 eleva o Mutation Score, mas PIT mede se os testes distinguem mutantes, não se suas expectativas derivam corretamente da documentação. Dos 198 kills de S2, o teste registrado como primeiro killer foi classificado como baseado em suposição em 188 casos e em inferência em 10. Dois casos assumidos (contagem 2^n da tabela-verdade e campos score/survivors) têm suporte no gabarito independente para essas assertions específicas; isso não valida os demais detalhes desses testes. Para o detalhamento, inclusive a distinção entre os 23 kills corroborados e os 165 sem confirmação correspondente, consulte [`missing-tests-analysis.md`](./missing-tests-analysis.md).

## Evidências e ressalvas

- Os arquivos principais são os três `mutation-results-*.csv`, cada um com 456 linhas de mutantes e uma coluna `result_class` normalizada.
- Os logs brutos legíveis estão em [`execution-logs/`](./execution-logs/).
- `mutation-results-cli-*.csv` preserva execuções exploratórias com 256 mutantes; essa população não é combinada com os resultados `mcdc-core`.
- Os resultados não medem cobertura de requisitos nem correção semântica dos oráculos.
