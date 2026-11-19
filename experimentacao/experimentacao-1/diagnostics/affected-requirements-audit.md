# Auditoria da quantidade de requisitos afetados

## Pares registrados

Os pares registrados envolvem:

- TIS REQ002 x REQ006;
- TIS REQ003 x REQ006;
- TIS REQ004 x REQ006;
- NPP REQ005 x REQ008.

Os requisitos distintos ligados a esses pares sao:

- TIS REQ002;
- TIS REQ003;
- TIS REQ004;
- TIS REQ006;
- NPP REQ005;
- NPP REQ008.

**Total ligado a conflitos potenciais:** 6 requisitos distintos.

## Lacuna separada

NPP REQ009 referencia `the_safety_injection_mode`, que nao esta declarada em `inputs`.

Essa lacuna inclui um requisito adicional, mas nao representa incompatibilidade confirmada com outro requisito:

- Total adicional: 1.

**Total distinto potencialmente afetado:** 7 requisitos.

## Diferenca em relacao ao total anterior

O total anterior de cinco requisitos:

- TIS REQ002;
- TIS REQ003;
- TIS REQ004;
- NPP REQ005;
- NPP REQ008.

Esse total conta apenas os lados dos pares anteriormente destacados, mas omite:

- TIS REQ006, que participa dos tres pares;
- NPP REQ009, que possui a lacuna de declaracao.

Portanto:

- 5 requisitos no registro anterior;
- 6 requisitos distintos com conflito potencial entre pares;
- 7 requisitos distintos quando a lacuna de NPP REQ009 e incluida.
