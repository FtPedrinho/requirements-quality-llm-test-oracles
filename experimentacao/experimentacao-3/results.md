# Resultados — Experimento C3

## Execução

| Suíte | Registrados | Aprovados | Falhas | Ignorados |
|---|---:|---:|---:|---:|
| S1 — documental | 49 | 37 | 7 | 5 |
| S2 — complementar | 5 | 1 | 0 | 4 |
| S3 — combinada | 54 | 38 | 7 | 9 |

As sete falhas são expectativas incompatíveis preservadas da documentação. Não foram ajustadas para fazer a suíte passar.

## Cinco métricas

| Métrica | S1 | S2 | S3 |
|---|---:|---:|---:|
| Cobertura de requisitos | 12/19 = **63,16%** | 1/19 = **5,26%** | 13/19 = **68,42%** |
| Mutation Score | **Não avaliável** | 0/456 = **0,00%** | **Não avaliável** |
| Precision | **85,71%** | **100,00%** | **86,67%** |
| Recall | **63,16%** | **5,26%** | **68,42%** |
| F1-score | **72,73%** | **10,00%** | **76,47%** |

O S2 completou PIT, mas seu único teste ativo não alcançou o core Java: os 456 mutantes ficaram em `NO_COVERAGE`. O 0% não é evidência de ausência geral de detecção. PIT abortou S1/S3 porque a execução-base tem sete falhas; esses Mutation Scores são **não avaliáveis**, não zero.

## Interpretação

S2 adicionou um comportamento válido e S3 cobre 13/19 comportamentos do gabarito, dois a mais que C2 S3. Entretanto, duas expectativas de S3 contradizem o gabarito, reduzindo Precision para 86,67%. A clareza textual, portanto, não resolveu o problema de consistência: os conflitos impedem uma suíte combinada verde e uma avaliação PIT válida.

## Limitações

O mesmo gabarito independente e os mesmos 456 IDs de mutantes de C2 foram preservados. Os resultados são descritivos, não uma atribuição causal controlada. Casos assumidos ou ambíguos não foram classificados como corretos só por passar na implementação.
