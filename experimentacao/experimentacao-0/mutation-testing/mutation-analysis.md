# Análise dos mutantes

## Operadores

| Operador | Total | Mortos | Sobreviventes | Equivalentes | Não determinados |
|---|---:|---:|---:|---:|---:|
| NEG-CONDITION | 232 | 226 | 6 | 6 | 0 |
| ROP | 187 | 164 | 20 | 3 | 0 |
| REM-CONDITION | 172 | 160 | 6 | 6 | 0 |
| CONST | 126 | 86 | 10 | 6 | 24 |
| AOD | 86 | 86 | 0 | 0 | 0 |
| REM | 86 | 86 | 0 | 0 | 0 |
| NEG-SUB | 86 | 86 | 0 | 0 | 0 |

As contagens correspondem aos resultados efetivamente registrados no catálogo JSON.

## Diferenças por oráculo

O maior Mutation Score individual observado foi 100% em diversos oráculos.

Os menores scores estiveram em TIS REQ002-REQ004, VM REQ002-REQ005 e expressões com limites:

- TIS REQ002-REQ004: 84,31%;
- VM REQ004-REQ005: 86,21%;
- VM REQ002: 87,04%;
- VM REQ003: 88,89%.

Essas diferenças refletem operadores e casos disponíveis, não necessariamente qualidade semântica intrínseca dos oráculos.

## Casos redundantes

A presença de casos redundantes não foi avaliada por execução separada de cobertura de mutantes por caso. O estudo não afirma que todos os 152 casos são necessários. Uma minimização da suíte depende de uma matriz caso-mutante completa e pode ser executada como análise posterior.
