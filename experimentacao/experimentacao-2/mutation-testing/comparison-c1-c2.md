# Comparação C1 × C2

## Resultados disponíveis

| Métrica principal | C1 disponível | C2 comparável | Observação |
|---|---:|---:|---|
| Cobertura de requisitos | Não disponível na mesma definição/gabarito | S3: **57,89%** (11/19) | Os catálogos congelados diferem: C1 tem 21 linhas e C2 tem 19; não há mapeamento comum validado. |
| Mutation Score | C1 PIT `exp1`: 319/333 = **95,80%** | S3: 218/456 = **47,81%** | Diferença descritiva de -47,99 p.p.; população, IDs e harness não são os mesmos, portanto não é comparação controlada. |
| Precision | **1,000** publicado em `experimentacao-1/metrics-report.md` | S3: **100,00%** | A unidade C1 é uma matriz de resultados de mutantes, não os 19 comportamentos do gabarito C2. |
| Recall | **0,955** publicado em `experimentacao-1/metrics-report.md` | S3: **57,89%** | Unidades e regras de não avaliáveis diferem; a diferença não pode ser atribuída à documentação C2. |
| F1-score | **0,977** publicado em `experimentacao-1/metrics-report.md` | S3: **73,33%** | Não diretamente comparável pelas mesmas limitações de Precision/Recall. |

## Ressalvas de comparabilidade

1. A execução PIT C1 `exp1` registra 333 mutantes: 319 `KILLED`, 1 `SURVIVED`, 12 `NO_COVERAGE` e 1 `TIMED_OUT`. Aplicando a regra desta avaliação — excluir somente equivalentes identificados do denominador e não contar timeout como kill — o resultado é `319/(333-0) = 95,80%`. Nenhum detector de equivalência foi usado.
2. O relatório agregado C1 de outra tarefa lista 981 casos/mutantes, 21 equivalentes identificados, 894 mortos e 24 `UNKNOWN`. Pela fórmula especificada aqui, o score seria `894/(981-21) = 93,125%`; o valor “corrigido” de 95,513% naquele relatório exclui também os `UNKNOWN` e não usa o mesmo denominador. Esse corpus não é o PIT de 333 mutantes acima nem o conjunto C2 de 456.
3. O relatório de oráculos C1 publica Precision/Recall/F1 para classificação de resultados de mutantes, enquanto o C2 desta avaliação compara comportamentos contra o catálogo independente de 19 linhas. Outro artefato C1 declara que a geração de oráculos não foi realizada. Os valores publicados foram preservados como histórico, mas não tratados como comparáveis.
4. C1 e C2 usam catálogos de tamanhos/conteúdos diferentes e nenhuma cobertura de requisitos C1 sob o denominador C2 foi encontrada.

Não se atribui causalidade à degradação documental. O contraste de scores é descritivo e mistura populações, escopos e regras históricas. A avaliação detalhada de C2 está em [`metrics.md`](./metrics.md).
