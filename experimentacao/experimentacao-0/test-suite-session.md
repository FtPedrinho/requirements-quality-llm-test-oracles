# Sessão das suítes de teste — Experimento 0

## Contexto

Data da sessão registrada: 18/11/2026.

Esta sessão registra os artefatos históricos produzidos antes da reconstrução metodológica. Ela não representa a suíte final contra o SUT real da ferramenta MC/DC.

## Documentação usada

- arquivos originais de requisitos em `exemplos/`;
- 33 decisões NAT2TEST;
- 3 expressões gerais `.mcdc`.

## Oráculos e casos

- oráculos históricos: 36;
- casos históricos: 152;
- pares simbólicos MC/DC: 119;
- casos PASS: 33;
- casos MC/DC: 119.

## Execução do modelo original

- casos concretizáveis: 140;
- casos não concretizáveis: 12;
- falsos positivos contra o modelo original: 0.

## Mutation Testing histórico

- mutantes: 981;
- equivalentes: 21;
- mortos: 894;
- sobreviventes: 42;
- UNKNOWN/não avaliáveis: 24;
- Mutation Score reportado: 93,125%;
- Mutation Score corrigido por equivalentes e não avaliáveis: 95,513%.

## Suíte executável posterior

- casos: 185;
- casos válidos: 173;
- casos não concretizáveis: 12;
- cópias mutadas: 981.

Essa suíte não executa a implementação Java da ferramenta MC/DC.

## Limitação

Os resultados avaliam expressões VM, TIS e NPP. Eles não medem diretamente oráculos da ferramenta MC/DC.
