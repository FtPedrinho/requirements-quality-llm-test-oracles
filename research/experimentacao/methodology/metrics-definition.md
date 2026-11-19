# Definição de métricas

## Unidade de oráculo

Comportamento especificável e verificável da ferramenta MC/DC.

## TP, FP e FN

- TP: comportamento esperado identificado e especificado corretamente.
- FP: comportamento afirmado incorretamente ou não previsto no gabarito.
- FN: comportamento esperado omitido ou especificado incorretamente.
- Não avaliável: unidade ambígua ou sem referência suficiente.

## Fórmulas

\[
Precision = \frac{TP}{TP+FP}
\]

\[
Recall = \frac{TP}{TP+FN}
\]

\[
F1 = 2 \cdot \frac{Precision \cdot Recall}{Precision+Recall}
\]

Não calcular essas métricas até existir gabarito independente e oráculos novos do SUT.

## Mutation Score

\[
MS = \frac{KILLED}{TOTAL-EQUIVALENT-INVALID}
\]

UNKNOWN fica separado e não é considerado equivalente.
