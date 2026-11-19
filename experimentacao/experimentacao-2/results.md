# Resultados — Experimento C2

## Execução

| Suíte | Testes | Aprovados | Falhas | Ignorados |
|---|---:|---:|---:|---:|
| S1 — originais | 26 | 26 | 0 | 0 |
| S2 — complementares | 10 | 9 | 0 | 1 |
| S3 — combinada | 36 | 35 | 0 | 1 |

Os dez casos ausentes foram tentados; um permaneceu indeterminado por `Z3 UNKNOWN`. Entre S2, 2 casos foram inferidos, 7 assumidos e 1 indeterminado. Aprovação não foi usada como prova de correção do oráculo.

## Cinco métricas

| Métrica | S1 | S2 | S3 |
|---|---:|---:|---:|
| Cobertura de requisitos | 9/19 = **47,37%** | 2/19 = **10,53%** | 11/19 = **57,89%** |
| Mutation Score | 152/456 = **33,33%** | 198/456 = **43,42%** | 218/456 = **47,81%** |
| Precision | **100,00%** | **100,00%** | **100,00%** |
| Recall | **47,37%** | **10,53%** | **57,89%** |
| F1-score | **64,29%** | **19,05%** | **73,33%** |

Precision aplica-se somente aos oráculos comparáveis com o gabarito; afirmações assumidas fora dele não ganham crédito automaticamente.

## PIT em S3

Dos mesmos 456 mutantes: **218 killed**, **162 survived**, **71 no coverage**, **5 timed out**, **0 equivalent identificados** e **0 non-viable/error**. “Nenhum equivalente identificado” não prova que não existam equivalentes. Timeouts e ausência de cobertura não foram contados como kills.

Dos 198 kills associados a S2, 188 tiveram como primeiro killer testes assumidos e 10 inferidos. Apenas 23 kills tinham correspondência corroborada pelo gabarito; os outros 165 não têm confirmação independente correspondente. Isso mostra eficácia operacional sem estabelecer confiabilidade semântica.

## Interpretação

S2 acrescentou dois comportamentos válidos ao S3, elevando cobertura de 9/19 para 11/19. A documentação pouco clara deixou oito comportamentos do gabarito sem identificação integral. O Mutation Score de S3 melhorou em relação a S1, mas não deve ser confundido com qualidade do oráculo: mutações podem ser mortas por expectativas assumidas.

## Limitações

Os resultados principais usam 19 comportamentos independentes; outros catálogos históricos têm unidades diferentes e não foram usados no cálculo. O gabarito não foi alterado para acomodar a suíte. A documentação C2, a implementação Java e os 26 testes originais foram preservados.
