# Mutantes sobreviventes

Foram registrados 42 mutantes não equivalentes que sobreviveram aos 152 casos simbólicos.

Os operadores mais representados entre os sobreviventes são:

| Operador | Frequência |
|---|---:|
| ROP | 20 |
| CONST | 10 |
| REM-CONDITION | 6 |
| NEG-CONDITION | 6 |

Exemplos relevantes:

- substituição de limites em VM por igualdade ou comparação mais restrita;
- alteração de `<= 30.0`, `>= 10.0` e `<= 50.0`;
- alteração de limites inteiros em TIS;
- remoção de condições em guardas compostas;
- inversões que produzem diferenças fora dos pares concretizados disponíveis.

Os sobreviventes não são classificados como falhas dos oráculos sem considerar a insuficiência dos casos concretos e as relações de domínio não formalizadas.
