# Relatorio de métricas - Experimento 1

## Resultados gerais

| Métrica | Resultado |
|---|---:|
| Mutantes | 981 |
| Equivalentes | 21 |
| Mortos | 894 |
| Sobreviventes | 42 |
| UNKNOWN | 24 |
| Mutation Score reportado | 93,125% |
| Mutation Score corrigido | 95,513% |
| Precision | 1,000 |
| Recall | 0,955 |
| F1 | 0,977 |

O Mutation Score corrigido usa:

\[
MS = \frac{894}{981-21-24}=95,513\%
\]

## Matriz de confusão

| | Predito positivo | Predito negativo |
|---|---:|---:|
| Real positivo | TP 894 | FN 42 |
| Real negativo | FP 0 | TN 21 |

Os 24 UNKNOWN não são incluídos.

## Modelo original

- 152 casos PASS/MC/DC associados;
- 140 passaram contra o modelo original;
- 12 não produziram modelo concreto;
- 0 falsos positivos.

## Análise por sistema

Os resultados detalhados por oráculo estão em `mutation-testing/metrics/metrics-by-oracle.csv`.

Resumo observado:

- VM manteve a maior concentração de sobreviventes em limites entre 10, 30 e 50;
- TIS apresentou os menores scores em REQ002-REQ004 devido à sobreposição formal e mutantes de limites/condições;
- NPP apresentou 24 UNKNOWN em REQ009/REQ010 por formalização restrita à lacuna da variável de saída;
- As diferenças não demonstram correção semântica real.

## Sensibilidade

Critério de exclusão:

- 9 oráculos associados diretamente às ressalvas;
- 6 oráculos dos conflitos potenciais;
- 3 oráculos NPP com `the_safety_injection_mode`.

Resultado:

- 288 mutantes diretamente associados;
- corpus sem unidades reservadas: 693 mutantes;
- corpus sem unidades reservadas: 658 mortos, 17 sobreviventes, 18 UNKNOWN;
- Mutation Score corrigido sem unidades reservadas: 97,481%.

O resultado sensível não substitui o resultado principal.
