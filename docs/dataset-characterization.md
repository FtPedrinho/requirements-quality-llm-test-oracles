# Caracterização do corpus da pesquisa

## Sistema sob teste

O objeto de estudo é a ferramenta MC/DC implementada em Java neste repositório, com módulos `mcdc-core`, `mcdc-requirements`, `mcdc-z3` e `mcdc-cli`. Os dados de exemplo VM, TIS e NPP são processados pela ferramenta; não são aplicações de domínio implementadas no repositório.

## Documentação por condição

As fontes C0-C4 e seus hashes estão organizados em [experimentacao-pesquisa/](../experimentacao-pesquisa/). As documentações são preservadas sem edição. C0 é original e deve ser caracterizada sem rotulagem alto/baixo automática. C1-C4 são manipulações pretendidas no desenho fatorial 2×2.

O sistema e suas documentações próprias permanecem inalterados. O PDF técnico é uma referência arquitetural e não deve ser interpretado como requisito de funcionalidade atual sem confirmação.

## Uso do corpus

Cada condição é independente e usa somente sua fonte normativa. O
[protocolo](../experimentacao-pesquisa/protocolo/metodologia.md) define o
procedimento, a utilização obrigatória de Z3 e a preservação das fontes.

## Métricas e resultados

A avaliação usa Branch Coverage e quantidades de testes aprovados, falhos e
indeterminados. Erros técnicos e casos inválidos são registrados
separadamente. Relatórios de testes próprios do SUT não são resultados das
suítes LLM.
