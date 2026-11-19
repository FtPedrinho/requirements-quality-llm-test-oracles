# Métricas C2 — S1, S2 e S3

## Base de avaliação

O gabarito independente congelado é `oracle-reference/oracle-reference-catalog.csv`, com **R_t = 19** comportamentos validados. O catálogo C2 derivado do texto possui 34 IDs e colide semanticamente com o gabarito em alguns IDs (por exemplo, o B018 C2 gerado é limite/truncamento; o B018 independente é tabela-verdade). O cruzamento foi feito pela descrição e critério do comportamento; o catálogo congelado não foi alterado.

A classificação histórica em `oracle-evaluation/oracle-classification.csv` cobre 34 comportamentos derivados da documentação, mas não é o catálogo independente; `oracle-evaluation/oracle-evaluation.md` também declara que a geração/avaliação não havia sido realizada. Seus TP/FP/FN não foram reutilizados como resultado desta avaliação.

### Regra para casos ambíguos, parciais e não avaliáveis

- O resultado esperado é comparado com a unidade correspondente do gabarito independente. A aprovação do teste não é evidência suficiente.
- Assertions que correspondem a um comportamento do gabarito são TP. Nenhum comportamento avaliado contradiz o gabarito, portanto FP=0.
- Cada comportamento independente não identificado pela suíte é FN, contado uma vez, sem duplicação por testes.
- Casos fora do catálogo independente, ou que só verificam parte insuficiente do critério, não viram TP nem FP. Eles são registrados como parciais/não avaliáveis e não ampliam o denominador.
- S2 tem duas assertions com suporte independente: a contagem 2^n de linhas de tabela-verdade e os campos de score/sobreviventes do relatório de mutação. A aprovação em execução não foi o critério para creditá-las. Detalhes de cabeçalho, esquema de CSV e demais suposições continuam sem crédito.

O gabarito independente não classifica seus 19 itens como ambíguos/indeterminados. Já as classificações derivadas de C2 registram 12 ambiguidades e 8 indeterminações entre 34 IDs; essas classes são reportadas como limitações documentais e não substituem o gabarito congelado.

## Cobertura de requisitos

Fórmula: `Cobertura = (R_c / R_t) × 100`, com `R_t = 19`.

| Suíte | R_c | Cálculo | Cobertura |
|---|---:|---:|---:|
| S1 — 26 originais | 9 | 9/19 | 47,37% |
| S2 — 10 complementares | 2 | 2/19 | 10,53% |
| S3 — combinada | 11 | 11/19 | 57,89% |

S1 cobre fonte única, opção desconhecida, arquivo `.mcdc` válido/vazio, JSON NAT2TEST válido/sem decisões, CSV sem coluna obrigatória, conflito e lacuna. S2 acrescenta a tabela-verdade 2^n e os campos score/sobreviventes da mutação. As contagens são comportamentos distintos, não número de métodos.

## Mutation Score

Fórmula solicitada: `MS = K / (M - E) × 100`. PIT gerou os mesmos **456 IDs** para cada cenário. `E=0 identificado`; PIT não executou detector de equivalência, portanto isso significa “nenhum equivalente identificado”, não “nenhum equivalente existe”. Somente o status `KILLED` entra em K; `TIMED_OUT` é separado mesmo quando o atributo PIT `detected` aparece como true. `NO_COVERAGE` e `TIMED_OUT` permanecem no denominador conforme a fórmula fornecida.

| Suíte | K | Sobreviventes | Equivalentes identificados | Sem cobertura | Timed out | Não avaliáveis (sem cobertura + timeout + erro) | M | MS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| S1 | 152 | 155 | 0 | 144 | 5 | 149 | 456 | 152/456 = **33,33%** |
| S2 | 198 | 167 | 0 | 90 | 1 | 91 | 456 | 198/456 = **43,42%** |
| S3 | 218 | 162 | 0 | 71 | 5 | 76 | 456 | 218/456 = **47,81%** |

Não houve status PIT `ERROR`/não viável nos arquivos primários. As listas de mutantes sobreviventes e seus primeiros testes detectores estão nos três `mutation-results-*.csv`. S3 detectou 66 mutantes além de S1 e 20 além de S2; isso é eficácia operacional, não validade de oráculo.

## Precision, Recall e F1-score

Unidade de contagem: os 19 comportamentos do gabarito congelado, contados uma vez. `Precision = TP/(TP+FP)`, `Recall = TP/(TP+FN)` e `F1 = 2×Precision×Recall/(Precision+Recall)`.

| Suíte | TP | FP | FN | Não avaliáveis | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| S1 | 9 | 0 | 10 | Assertions complementares sem unidade completa no gabarito | 9/9 = **100,00%** | 9/19 = **47,37%** | **64,29%** |
| S2 | 2 | 0 | 17 | 8 casos sem crédito integral; 1 caso indeterminado ignorado | 2/2 = **100,00%** | 2/19 = **10,53%** | **19,05%** |
| S3 | 11 | 0 | 8 | Casos parciais/fora do catálogo, sem ampliação do gabarito | 11/11 = **100,00%** | 11/19 = **57,89%** | **73,33%** |

Os denominadores de Precision não são zero; portanto, não há divisão indefinida. A Precision de 100% é limitada ao conjunto de oráculos que pôde ser comparado e não significa que todas as assertions da suíte estejam corretas. As expectativas sem correspondência no gabarito não são consideradas verdadeiras nem falsas sem evidência; as lacunas dos 19 comportamentos válidos são FNs.

## Efeito de S2 sobre S3

Contra S1, a suíte combinada ganha dois comportamentos válidos: cobertura sobe de 47,37% para 57,89%; Mutation Score sobe de 33,33% para 47,81%; Precision permanece em 100%; Recall sobe de 47,37% para 57,89%; F1 sobe de 64,29% para 73,33%. Esses ganhos não provam confiabilidade dos oito outros casos sem crédito integral nem dos detalhes adicionais não documentados.

## Execução e limites

- S1: 26 métodos selecionados; 26 passaram.
- S2: 10 registrados; 9 passaram, 1 ignorado (`UNKNOWN` indeterminado).
- S3: 36 registrados; 35 passaram, 1 ignorado.
- Os dez métodos placeholder do arquivo original não foram executados em S1/S3; os 26 métodos originais foram preservados.
- Os CSVs requeridos usam o escopo PIT primário `mcdc-core` (456 mutantes). Há CSVs exploratórios `mutation-results-cli-*` com população diferente de 256; eles não são os resultados principais e não foram misturados aos cálculos.
- PIT foi configurado temporariamente para executar os testes externos contra `mcdc-core`; a configuração temporária foi removida após a execução. Implementação Java e documentação C2 não foram alteradas.
