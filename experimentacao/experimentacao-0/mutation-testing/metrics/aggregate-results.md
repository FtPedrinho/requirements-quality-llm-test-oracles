# Resultados agregados

## Totais

| Métrica | Resultado |
|---|---:|
| Mutantes | 981 |
| Equivalentes | 21 |
| Não equivalentes | 960 |
| Mortos | 894 |
| Sobreviventes | 42 |
| UNKNOWN | 24 |
| Não avaliáveis | 24 |
| Mutation Score | 93,125% |
| Precision | 1,000 |
| Recall | 0,955 |
| F1-score | 0,977 |

## Regra agregada

Os valores gerais são agregados por totais de mutantes:

\[
MS = \frac{894}{981-21} = 93,125\%
\]

Para Precision, Recall e F1, a matriz utiliza mutante agregado:

| | Predito positivo | Predito negativo |
|---|---:|---:|
| Real positivo | TP 894 | FN 42 |
| Real negativo | FP 0 | TN 21 |

Eixo positivo: mutante não equivalente. Eixo negativo: mutante equivalente.

## Micro agregado

- Precision: 1,000
- Recall: 0,955
- F1: 0,977

## Macro por oráculo

As médias aritméticas dos 33 oráculos:

- Precision: 1,000
- Recall: 0,96785
- F1: 0,98293

Não é usada como substituta do cálculo geral agregado.
