# Análise de Precision, Recall e F1 dos oráculos - Experimento 1

## Estado atual

Os oráculos C1 existentes são relativos a VM, TIS e NPP e não constituem oráculos da ferramenta MC/DC.

A revisão documental não pode ser usada para alterar arbitrariamente o objeto de avaliação.

## Gabarito necessário

Antes do cálculo das métricas, será necessário criar um catálogo independente dos comportamentos da ferramenta MC/DC.

O catálogo terá:

- identificadores únicos;
- descrições verificáveis;
- condições e entradas;
- resultados esperados;
- critérios objetivos;
- origem documental;
- evidência independente da implementação.

## Unidade

O comportamento especificável e verificável será a unidade principal.

Casos ambíguos serão registrados como não avaliáveis e não classificados automaticamente como TP, FP ou FN.

## Classificação

- TP: comportamento esperado corretamente identificado e especificado;
- FP: comportamento afirmado que não corresponde ao gabarito;
- FN: comportamento esperado omitido ou incorretamente especificado.

Um único erro pode produzir FP e FN simultaneamente quando a unidade e o protocolo permitirem essa dupla anotação.

## Métricas

\[
Precision = \frac{TP}{TP+FP}
\]

\[
Recall = \frac{TP}{TP+FN}
\]

\[
F1 = 2 \cdot \frac{Precision \cdot Recall}{Precision+Recall}
\]

## Apresentação futura

Os resultados serão apresentados por execução e agregados por média, desvio-padrão e intervalo de confiança quando houver amostra suficiente.

Também serão apresentadas contagens por categoria e variações entre C0 e C1.

## Resultado atual

Não há contagens válidas de TP, FP ou FN nesta etapa.

Os arquivos obrigatórios foram criados como esquemas para evitar confusão com Mutation Score ou eficácia da suíte.
