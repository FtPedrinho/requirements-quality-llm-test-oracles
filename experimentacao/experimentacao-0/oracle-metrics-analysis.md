# Análise de Precision, Recall e F1 dos oráculos - Experimento 0

## Estado atual

Os artefatos históricos deste experimento não fornecem um gabarito independente da ferramenta MC/DC.

Os oráculos existentes descrevem VM, TIS e NPP, que são dados de entrada processados pelo SUT. Portanto, não é metodologicamente válido calcular TP, FP e FN para esses oráculos como qualidade dos oráculos da ferramenta MC/DC.

## Quando calcular

Somente após construir:

1. o catálogo independente de comportamentos da ferramenta MC/DC;
2. critérios objetivos de correção;
3. oráculos gerados para o comportamento da ferramenta;
4. registros de classificação por unidade;
5. uma análise independente da implementação.

## Definições

- TP: comportamento esperado corretamente identificado e especificado.
- FP: comportamento afirmado que não corresponde ao gabarito.
- FN: comportamento esperado omitido ou incorretamente especificado.
- Não avaliável: unidade sem referência suficiente ou ambígua.

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

## Resultado atual

Os arquivos `oracle-metrics.csv`, `oracle-classification.csv` e `oracle-reference-catalog.csv` estão definidos como estruturas obrigatórias, mas não contêm valores experimentais válidos.

Não apresentar 0 como substituto de TP, FP ou FN sem dados reais seria incorreto.
