# Sessão das suítes de teste — Experimento 1

## Contexto

Data da sessão registrada: 18/11/2026.

Esta sessão registra os artefatos históricos produzidos antes da reconstrução metodológica. Ela não representa a suíte final contra o SUT real da ferramenta MC/DC.

## Estrutura documental C1

Os requisitos originais foram duplicados em `requirements/original/` e revisados em `requirements/experimental/`.

A revisão alterou 33 textos naturais JSON:

- 5 textos VM;
- 17 textos TIS;
- 11 textos NPP.

Os arquivos `.mcdc` auxiliares foram preservados sem alteração semântica.

## O que mudou

- pontuação;
- remoção de dois-pontos após `shall`;
- padronização de `Assign`, `Reset` e `shall`;
- normalização de espaçamento;
- nenhuma mudança em guardas;
- nenhuma mudança em ações;
- nenhuma mudança em tipos;
- nenhuma mudança em limites;
- nenhuma resolução automática das pendências.

## Por que o resultado foi igual ao do Experimento 0

Os componentes semânticos usados pelos motores históricos não mudaram:

- guardas: idênticas;
- ações: idênticas;
- tipos e valores: idênticos;
- unidades do motor: idênticas;
- 33 textos foram apenas padronizados;
- os resultados anteriores não usavam documentação C1 da ferramenta MC/DC.

Portanto, o Experimento 1 histórico produziu a mesma estrutura de casos e mutantes. Isso não demonstra efeito positivo da revisão C1 sobre oráculos da ferramenta.

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
- Mutation Score corrigido: 95,513%.

## Suíte executável posterior

- casos: 185;
- casos válidos: 173;
- casos não concretizáveis: 12;
- cópias mutadas: 981.

Essa suíte não executa a implementação Java da ferramenta MC/DC.

## Pendências mantidas

- TIS REQ002/REQ006;
- TIS REQ003/REQ006;
- TIS REQ004/REQ006;
- NPP REQ005/REQ008;
- ausência de declaração de `the_safety_injection_mode` no JSON.
