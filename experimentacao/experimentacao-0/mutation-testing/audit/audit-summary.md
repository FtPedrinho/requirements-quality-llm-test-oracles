# Auditoria independente dos cálculos

## Totais verificados

| Item | Quantidade |
|---|---:|
| Mutantes no JSON | 981 |
| IDs únicos | 981 |
| Equivalentes | 21 |
| Não equivalentes | 936 |
| UNKNOWN | 24 |
| Mortos | 894 |
| Sobreviventes | 42 |
| Casos do modelo original | 152 |
| Casos que passaram | 140 |
| Casos não avaliáveis | 12 |
| Linhas de execução de mutantes | 4974 |
| Pares únicos mutante/caso | 4974 |

## Partição dos mutantes

\[
981 = 894 + 42 + 21 + 24
\]

As 981 entradas são únicas por `mutant_id`.

- Mortos: 894.
- Sobreviventes: 42.
- Equivalentes: 21.
- UNKNOWN ou não avaliáveis por erro de formalização: 24.

Não existe nenhuma categoria adicional.

## Mutation Score

Número reportado:

\[
MS = \frac{894}{981-21} = 93.125000\%
\]

Partição metodologicamente corrigida, excluindo os 24 não avaliáveis:

\[
MS = \frac{894}{981-21-24} = \frac{894}{936} = 95.512821\%
\]

Portanto, a fórmula reportada é aritmética para `960` denominador, mas não exclui os 24 mutantes não avaliáveis. O valor mais defensável nesta auditoria é **95.512821%**.

## Recall

Com mutante agregado:

- TP = 894;
- FN = 42;
- Positivos avaliáveis = 936.

\[
Recall = \frac{894}{894+42} = 0.955128205128
\]

O Recall usa uma população coerente de mutantes não equivalentes avaliados. Os 24 UNKNOWN não são incluídos como falsos negativos.

## Precision

- FP = 0;
- TN = 21 equivalentes não mortos.

\[
Precision = \frac{894}{894+0} = 1.000000000000
\]

## F1

\[
F1 = 2\times\frac{1.000\times 0.955128205128}{1.000+0.955128205128} = 0.977049180328
\]

O cálculo é reproduzível e matematicamente coerente, observando que TN não entra no F1 e UNKNOWN foi excluído.

## Casos não concretizados

O arquivo `execution/original-execution.csv` contém 152 linhas:

- 140 passaram;
- 12 ficaram com `passed=NON-EVALUABLE`.

Esses 12 pares não foram usados como TP, FP, TN ou FN. Não há evidência de que tenham sido reutilizados como mortes de mutantes.

Os 24 mutantes `NOT-EVALUABLE` são uma categoria separada. Não são os mesmos registros dos 12 pares não concretizados.

## Dupla contagem

- IDs de mutante únicos: 981.
- Linhas mutante/caso únicas: 4974.
- Linhas total de execução: 4974.
- Mutantes mortos pela coluna JSON: 894.
- Mutantes mortos pelo CSV: 894.
- Conjunto morto JSON == conjunto morto CSV: True.

Não foi encontrada dupla contagem dentro da agregação por mutante: mortes são calculadas por existência de pelo menos um caso `KILL`, não pela quantidade de linhas `KILL`.

## Reprodutibilidade

Os totais podem ser recomputados a partir de:

- `mutants/mutants.json`;
- `execution/original-execution.csv`;
- `execution/mutant-execution.csv`;
- `mutants/mutation-summary.csv`.

O registro JSON contém classificação, morte e sobrevivência por mutante. O CSV contém a evidência por execução.

## Conclusão

Os indicadores **matemáticos agregados podem ser considerados consistentes dentro da convenção reportada**. Porém, o relatório original não exclui os 24 mutantes UNKNOWN do denominador da Mutation Score, então o **93,125% reportado não é o Mutation Score mais metodologicamente defensável**.

A precisão de 1,000 é reproduzível, mas representa apenas ausência de falsos positivos identificados no conjunto; não prova correção semântica.

## Agregação por oráculo

Os CSVs por oráculo usam o mesmo padrão reportado e podem incluir os mutantes UNKNOWN no denominador ou como não avaliáveis. Assim, os valores individuais não devem ser somados ou comparados como taxas independentes sem confirmar o denominador de cada linha.

Exemplos de inconsistência metodológica no resumo por oráculo:

- `vm#1`: 25 mutantes, 19 mortos e 6 UNKNOWN; o CSV reporta 76% em vez de 100% se os UNKNOWN forem excluídos.
- `npp#10` e `npp#9`: 14 mutantes com 3 UNKNOWN em cada; o CSV reporta 78,57% para o número de mortos, não o Mutation Score corrigido.

O agregado geral de 95,512821% proposto nesta auditoria exige o mesmo tratamento nos níveis por oráculo. Os CSV originais não foram alterados.

Classificação recomendada deste cálculo: **matematicamente consistente nas métricas TP/FP/TN/FN, mas com ressalva metodológica no denominador da Mutation Score e na separação explícita dos não avaliáveis**.
