# Comparação dos Experimentos 0 e 1 reconstruídos

## SUT

Ambos os experimentos usam o mesmo commit da implementação Java da ferramenta MC/DC.

## Evidências executáveis

| Métrica | Experimento 0 | Experimento 1 |
|---|---:|---:|
| Casos de suíte real | 21 | 21 |
| Casos aprovados | 21 | 21 |
| Casos falhos | 0 | 0 |
| Mutantes PIT | 333 | 333 |
| Mutantes mortos | 320 | 320 |
| Mutation coverage | 96% | 96% |

## Diferença documental

O Experimento 0 usa cópias originais.

O Experimento 1 usa cópias com clareza e consistência melhoradas sem alterar limites ou comportamentos.

## Avaliação semântica dos oráculos

Precision, Recall e F1 não possuem ainda contagens válidas. Os oráculos e o gabarito precisam ser revisados unidade por unidade por avaliadores independentes.

## Conclusão

Os dois experimentos possuem a mesma evidência executável. Isso não demonstra superioridade documental nem causalidade; demonstra que a implementação real e o conjunto de testes físicos não mudaram entre as condições.
