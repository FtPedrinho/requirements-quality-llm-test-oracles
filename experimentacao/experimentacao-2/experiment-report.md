# Relatório do experimento C2

> **Registro histórico da execução inicial.** Os números abaixo antecedem a complementação S2, usam uma unidade de avaliação diferente e não são os resultados finais desta etapa. Para S1/S2/S3, a comparação com o gabarito independente congelado e os cinco indicadores solicitados, consulte [`experiment-report-mutation.md`](./experiment-report-mutation.md).

## Execução

O C2 foi executado a partir da documentação literal atual. Não foi usada C1 para completar a informação.

A geração de oráculos foi realizada pelo agente atual, não por um modelo externo independente.

## Classificação dos oráculos

- 34 comportamentos no gabarito;
- 18 TP;
- 0 FP;
- 16 FN;
- 0 não avaliáveis;
- Precision: 1,000;
- Recall: 0,5294;
- F1: 0,6923.

Os 16 FN representam comportamentos omitidos ou insuficientemente especificados pela C2.

## Suíte

- 36 testes registrados;
- 26 executados e aprovados;
- 0 reprovados;
- 10 erros documentais;
- 0 ignorados.

Os 10 erros são testes que explicitam lacunas de C2 e falham por indeterminação documental.

## Mutation Testing

PIT sobre o `mcdc-core` produz 333 mutantes, 320 mortos e 96,096% de mutation coverage.

Esse resultado não aplica as mutações à suíte derivada C2. A Mutation Testing dessa suíte permanece pendente.

## Comparação

C1 não possui métricas independentes comparáveis no novo gabarito. Portanto, TP/FP/FN, Precision, Recall e F1 não devem ser comparados causalmente.

Aumentar a suíte C2 não prova que a documentação C2 produziu oráculos melhores ou piores.
