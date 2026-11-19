# Relatório C2 — complementação e qualidade da suíte

## Resposta resumida

A documentação degradada permitiu a criação de dez casos complementares, mas não forneceu oráculos completos para todos eles. Nove foram executados com sucesso e um permaneceu indeterminado e ignorado. Comparando assertions com o gabarito independente congelado de 19 comportamentos, S2 acrescenta **dois** comportamentos válidos: tabela-verdade com 2^n linhas e relatório de mutação com score/sobreviventes. A suíte S3 chega a **11/19 requisitos cobertos (57,89%)**, deixando oito comportamentos válidos do gabarito sem identificação integral.

S2 melhora a detecção de mutantes operacionalmente: o Mutation Score sobe de 33,33% em S1 para 43,42% em S2 e 47,81% em S3. Esse ganho não significa que as outras expectativas assumidas ou inferidas sejam semanticamente corretas. O relatório do caso ausente discrimina o que tem suporte independente e o que permanece especulativo.

## As cinco métricas principais

| Métrica | S1 — 26 originais | S2 — 10 complementares | S3 — combinada |
|---|---:|---:|---:|
| Cobertura de requisitos | 9/19 = **47,37%** | 2/19 = **10,53%** | 11/19 = **57,89%** |
| Mutation Score | 152/456 = **33,33%** | 198/456 = **43,42%** | 218/456 = **47,81%** |
| Precision | 9/(9+0) = **100,00%** | 2/(2+0) = **100,00%** | 11/(11+0) = **100,00%** |
| Recall | 9/19 = **47,37%** | 2/19 = **10,53%** | 11/19 = **57,89%** |
| F1-score | **64,29%** | **19,05%** | **73,33%** |

O denominador de requisitos é o catálogo independente congelado em `oracle-reference/oracle-reference-catalog.csv` (19 comportamentos). A Precision de 100% aplica-se somente aos oráculos comparáveis com esse catálogo; não significa que todas as assertions da suíte sejam confiáveis. Expectations fora do gabarito ou verificações parciais não recebem TP/FP, enquanto os comportamentos válidos não identificados integralmente são FN. O gabarito não foi modificado.

As fórmulas, classificação de ambiguidades/parciais, identificadores cobertos e cálculo dos cinco indicadores estão em [`mutation-testing/metrics.md`](./mutation-testing/metrics.md). O resumo por mutante, com sobreviventes, não cobertura, timeouts e não viáveis, está em [`mutation-testing/mutation-summary.md`](./mutation-testing/mutation-summary.md).

## Execuções absolutas

- **S1:** 26 testes originais selecionados, 26 aprovados.
- **S2:** 10 complementares, 9 aprovados e 1 ignorado (`Z3 UNKNOWN`, indeterminado); nenhuma falha.
- **S3:** 36 registrados, 35 aprovados e 1 ignorado; nenhuma falha.
- Os dez métodos placeholder do arquivo original não foram executados. Os 26 métodos originais permaneceram intactos.
- PIT usou os mesmos 456 IDs em S1/S2/S3. Os resultados estritos são:

| Cenário | Killed | Survived | Equivalent identificado | No coverage | Timed out | Non-viable / Error |
|---|---:|---:|---:|---:|---:|---:|
| S1 | 152 | 155 | 0 | 144 | 5 | 0 |
| S2 | 198 | 167 | 0 | 90 | 1 | 0 |
| S3 | 218 | 162 | 0 | 71 | 5 | 0 |

“Equivalent identificado = 0” não prova que não existam equivalentes: PIT não utilizou detector de equivalência. Timeouts foram separados e não contados como mortos, mesmo quando o campo PIT `detected` aparecia como true. `NO_COVERAGE` e `TIMED_OUT` permanecem no denominador `M-E` conforme a fórmula solicitada. Os CSVs têm o resultado e o teste apontado por PIT para cada mutante.

## Confiabilidade dos oráculos complementares

Os dez casos S2 foram classificados como **0 documentados, 2 inferidos, 7 assumidos e 1 indeterminado**. O caso de `UNKNOWN` foi mantido no registro, mas desabilitado porque a documentação não permite escolher uma entrada determinística nem definir o resultado esperado.

Dois casos inicialmente classificados como assumidos foram comparados com o gabarito independente:

1. A asserção de quatro linhas para duas condições confirma a regra independente 2^n da tabela-verdade; o cabeçalho CSV permanece assumido.
2. A presença dos campos de score e sobreviventes confirma os critérios independentes do relatório de mutação.

Os outros oito casos S2 não acrescentam crédito integral: alguns não têm unidade correspondente no catálogo independente; outros só verificam rótulo/sucesso ou uma condição insuficiente para demonstrar o comportamento gold. A auditoria por teste está em [`test-audit.csv`](./mutation-testing/test-audit.csv) e todas as entradas, inferências e suposições em [`assumptions-register.csv`](./mutation-testing/assumptions-register.csv).

O PIT registrou como primeiros killers de S2 188 mutantes associados a testes assumidos e 10 a testes inferidos. Dos 188, 23 (19 do relatório de mutação e 4 da contagem 2^n) coincidem com assertions delimitadas pelo gabarito; os outros 165 não têm confirmação independente correspondente. Um mutante morto mede eficácia operacional, não correção semântica do oráculo.

## Limitações e reconciliação de evidências

- O catálogo independente possui 19 linhas; o catálogo C2 derivado da documentação possui 34 IDs e alguns IDs são semanticamente diferentes. Por exemplo, o B018 C2 gerado aponta para limite/truncamento, enquanto o B018 independente significa tabela-verdade. O cruzamento foi pelo conteúdo, nunca apenas pelo número do ID.
- `oracle-evaluation/oracle-classification.csv` contém TP/FP/FN históricos sobre 34 comportamentos derivados de C2; `oracle-evaluation/oracle-evaluation.md` afirma que aquela avaliação não havia sido executada. Esses números conflitantes não foram usados como gabarito nem reutilizados.
- A configuração temporária de PIT para carregar os testes externos foi removida. A configuração Maven de produção, a implementação Java, a documentação C2 e a suíte original não foram alteradas.
- Há CSVs exploratórios `mutation-results-cli-*` com 256 mutantes. Eles não são os resultados primários; os arquivos requeridos `mutation-results-{original,complementary,combined}.csv` são os resultados `mcdc-core`, com 456 IDs.
- Os mutadores PIT padrão incluíram negação/condições relacionais, limites, aritmética e resultados booleanos; não incluíram troca direta AND/OR nem mutadores customizados para remoção específica de validações. Não se afirma que essas mutações tenham sido cobertas.
- Comparação C1 × C2 e suas limitações estão em [`mutation-testing/comparison-c1-c2.md`](./mutation-testing/comparison-c1-c2.md). Nenhuma diferença é atribuída causalmente à documentação.

## Artefatos

Os resultados e logs estão em [`mutation-testing/`](./mutation-testing/), incluindo:

- [`mutation-summary.md`](./mutation-testing/mutation-summary.md)
- [`mutation-results-original.csv`](./mutation-testing/mutation-results-original.csv)
- [`mutation-results-complementary.csv`](./mutation-testing/mutation-results-complementary.csv)
- [`mutation-results-combined.csv`](./mutation-testing/mutation-results-combined.csv)
- [`test-audit.csv`](./mutation-testing/test-audit.csv)
- [`assumptions-register.csv`](./mutation-testing/assumptions-register.csv)
- [`missing-tests-analysis.md`](./mutation-testing/missing-tests-analysis.md)
- [`metrics.md`](./mutation-testing/metrics.md)
- [`comparison-c1-c2.md`](./mutation-testing/comparison-c1-c2.md)
- [`execution-logs/`](./mutation-testing/execution-logs/)
