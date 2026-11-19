# Status da reconstrução

## Concluído

- inventário documental inicial;
- identificação do SUT real;
- criação do comportamento e gabarito;
- 34 oráculos por condição;
- formalização Z3 de propriedades-chave;
- suítes CLI reais contra o SUT;
- PIT real sobre `mcdc-core`;
- registro separado de métricas semânticas e métricas de execução;
- preservação dos artefatos históricos.

## Não concluído

- geração por múltiplas execuções de um modelo LLM externo;
- revisão humana dos oráculos;
- TP/FP/FN;
- Precision/Recall/F1 dos oráculos;
- suítes geradas pelos novos oráculos executadas contra mutantes Java;
- Mutation Testing das suítes geradas.

## Bloqueio metodológico

Os oráculos existentes são uma primeira geração pelo agente atual. A qualidade semântica ainda depende de anotação independente contra o gabarito.
