# Auditoria independente - Experimento 1

## Totais

- Mutantes únicos: 981
- Pares únicos mutante/caso no CSV: 4974
- Equivalentes: 21
- Mortos: 894
- Sobreviventes: 42
- UNKNOWN: 24
- Casos do modelo original: 152
- Casos originais passaram: 140
- Casos originais não avaliáveis: 12

## Reprodutibilidade

Os mortos no JSON e no CSV são conjuntos equivalentes:

- JSON: 894
- CSV: 894
- Igualdade dos conjuntos: True

## Métricas corrigidas

- Mutation Score reportado: 93.125000%
- Mutation Score corrigido: 95.512821%
- Precision: 1.000000000000
- Recall: 0.955128205128
- F1: 0.977049180328

## Unidade de análise

Positivo = mutante não equivalente morto. Negativo = mutante equivalente. FN = mutante não equivalente sobrevivente.

Os 24 UNKNOWN não foram TP, TN, FP ou FN.

## Ressalvas

- Oráculos em pares potencialmente conflitantes: 6
- Oráculos relacionados a saída NPP não declarada: 3
- Oráculos diretamente afetados pela união das ressalvas: 9
- Casos com reserva: 43
- Casos com conflito potencial: 34
- Casos com saída NPP não declarada: 9
- Mutantes diretamente associados às ressalvas: 288

## Sensibilidade

Excluídos da sensibilidade:

- os 9 oráculos diretamente associados às ressalvas.

Resultado sem unidades reservadas:

- Total: 693
- Equivalentes: 0
- UNKNOWN: 18
- Mortos: 658
- Sobreviventes: 17
- Mutation Score corrigido: 97.481481%

Resultado somente das unidades reservadas:

- Total: 288
- Equivalentes: 21
- UNKNOWN: 6
- Mortos: 236
- Sobreviventes: 25
- Mutation Score corrigido: 90.421456%
