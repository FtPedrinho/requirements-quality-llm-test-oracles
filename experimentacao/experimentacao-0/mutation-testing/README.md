# Avaliação por Mutation Testing

Esta subpasta estende a Experimentação 0 com uma avaliação empírica dos oráculos usando mutantes de especificação.

Não há implementação executável independente dos sistemas VM, TIS e NPP neste repositório. Por isso, os mutantes não representam defeitos confirmados dessas implementações. Eles representam alterações controladas nas 33 expressões estruturadas NAT2TEST.

## Reutilização

A avaliação reutiliza:

- os 36 oráculos registrados em `../oracles/`;
- os requisitos e guardas originais;
- o parser e a infraestrutura Z3 já criados em `../z3-analysis/`;
- o mecanismo de análise existente em `mcdc-core` como referência metodológica.

PIT sobre o código Java não foi usado como substituto.

## Artefatos

- [Metodologia](methodology.md)
- [Análise dos mutantes](mutation-analysis.md)
- [Resumo da execução](execution/execution-summary.md)
- [Resultados agregados](metrics/aggregate-results.md)
- [Relatório final](final-report.md)
- [Auditoria de consistência](audit/audit-summary.md)

## Unidade de análise

- Positivo: mutante não equivalente.
- Negativo: expressão original ou mutante equivalente válido.
- TP: mutante não equivalente morto pela suíte.
- TN: mutante equivalente não morto.
- FP: mutante equivalente morto ou teste que rejeita incorretamente o comportamento original.
- FN: mutante não equivalente sobrevivente.

Para cada mutante, todos os casos associados são agregados: o mutante é morto se pelo menos um caso válido observa diferença em relação à expressão original.
