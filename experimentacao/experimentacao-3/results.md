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
| Mutation Score da suíte integral | **Não avaliável** | 0/456 = **0,00%*** | **Não avaliável** |
| Precision | **85,71%** | **100,00%** | **86,67%** |
| Recall | **63,16%** | **5,26%** | **68,42%** |
| F1-score | **72,73%** | **10,00%** | **76,47%** |

* No resultado histórico S2, o único teste ativo não alcançou o core Java: os 456 mutantes ficaram em `NO_COVERAGE`. O 0% não significa que todos os mutantes foram executados e sobreviveram. As execuções históricas S1/S3 foram interrompidas pelas sete falhas da linha de base; seus scores integrais são **não avaliáveis**, não zero.

### PIT exploratório em subconjunto aprovado

Após a execução histórica, foi feita uma análise exploratória a pedido do usuário: em uma cópia isolada, somente os sete métodos que falhavam na linha de base foram desabilitados. A suíte original e a implementação não foram alteradas. Os 38 testes restantes passaram; 16 dos 54 casos ficaram desabilitados (sete falhas de linha de base e nove já desabilitados).

| Execução exploratória | Killed | Survived | No coverage | Equivalent identificado | Timed out | Non-viable / Error | Mutation Score |
|---|---:|---:|---:|---:|---:|---:|---:|
| C3, subconjunto aprovado de S3 | 118 | 110 | 105 | 0 | 0 | 0 | `118 / (333 - 0) = 35,44%` |

O score é operacional e se aplica apenas ao subconjunto aprovado, não à suíte integral original. O PIT gerou 333 mutantes no build limpo e isolado; esse conjunto é idêntico ao usado no C4 exploratório, mas diferente do conjunto histórico de 456 mutantes. Portanto, o resultado não substitui nem é diretamente comparável ao MS de 456 mutantes de C2/S2. `Equivalent = 0` significa que nenhum equivalente foi identificado pelo processo; não houve classificação semântica manual de equivalência.

Os artefatos estão em [exploratory](mutation-testing/exploratory/): [relatório detalhado](mutation-testing/exploratory/pit-approved-subset-report.md), resultados por mutante com o killer registrado pelo PIT, XML bruto, definição das exclusões e cópias filtradas dos testes. O XML registra o teste detector reportado pelo PIT, não uma lista exaustiva de todos os testes que poderiam matar cada mutante. Os logs da linha de base filtrada e do PIT estão em [execution-logs](mutation-testing/execution-logs/).

## Interpretação

S2 adicionou um comportamento válido e S3 cobre 13/19 comportamentos do gabarito, dois a mais que C2 S3. Entretanto, duas expectativas de S3 contradizem o gabarito, reduzindo Precision para 86,67%. A clareza textual, portanto, não resolveu o problema de consistência. As falhas continuam impedindo um Mutation Score da suíte integral; o resultado exploratório do subconjunto aprovado mede apenas sua detecção operacional.

## Limitações

O gabarito independente foi mantido. Os registros históricos da suíte integral usam os 456 IDs da execução original; a execução exploratória limpa gerou um conjunto distinto de 333 mutantes, compartilhado com C4. Os resultados são descritivos, não uma atribuição causal controlada. Casos assumidos ou ambíguos não foram classificados como corretos só por passar na implementação.
