# Métricas C2

## Qualidade dos oráculos

A geração foi feita pelo agente atual a partir da documentação C2 literal, não por um modelo externo independente.

| Métrica | Resultado |
|---|---:|
| TP | 18 |
| FP | 0 |
| FN | 16 |
| Não avaliável | 0 |
| Precision | 1,000 |
| Recall | 0,5294 |
| F1-score | 0,6923 |

Precision foi perfeita neste conjunto porque nenhum comportamento gerado recebeu um FP.

Recall foi limitado pela omissão ou especificação insuficiente de 16 comportamentos.

## Suíte derivada

- 36 testes registrados;
- 26 executados;
- 26 aprovados;
- 0 reprovados;
- 10 erros documentais;
- 0 ignorados;
- 10 não executáveis devido à indeterminação da C2.

Os 10 erros documentais são `IllegalStateException` lançados explicitamente pelos testes. Eles não são falhas da implementação e não são ignorados.

## Mutation Testing

PIT sobre `mcdc-core`:

- 333 mutantes;
- 320 mortos;
- 1 sobrevivente;
- 12 sem cobertura;
- 1 timed out;
- 96,096% de mutation coverage.

Este resultado PIT não é uma medida de Mutation Testing da suíte derivada C2, pois a suíte C2 não foi aplicada contra cópias mutadas do SUT.
