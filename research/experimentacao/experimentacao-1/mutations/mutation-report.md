# Mutation Testing — Experimento 1 reconstruído

## Resultado real do PIT

Foi executado PIT sobre `mcdc-core` no mesmo commit do Experimento 0.

- mutantes totais: 333;
- mortos: 320;
- sobreviventes: 1;
- sem cobertura: 12;
- timed out: 1;
- mutation coverage: 96%.

O resultado é o mesmo em ambos os experimentos porque o código e o commit do SUT não foram alterados.

Os mutantes são do código Java da implementação MC/DC. Não são mutantes das entradas VM/TIS/NPP.
