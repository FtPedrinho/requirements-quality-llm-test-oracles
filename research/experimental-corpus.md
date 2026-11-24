# Corpus experimental

## Sistema e documentos

O objeto de teste é a ferramenta MC/DC implementada em Java. A fonte e as cópias experimentais de requisitos C0-C4 estão em [experimentacao-pesquisa/](../experimentacao-pesquisa/). Os documentos são congelados, identificados por hashes e não devem ser modificados.

O README técnico do SUT e os documentos de requisitos condicionais devem ser distinguidos: o material entregue ao modelo em cada execução é registrado por arquivo/hash. Não misturar documentação de condições. Exemplos VM/TIS/NPP são dados analisados pela ferramenta; não descrevem implementações de domínio sob teste.

## Uso do corpus

Cada condição é independente e entrega ao modelo somente sua fonte normativa.
A documentação e o SUT não devem ser alterados. O procedimento, o uso
obrigatório de Z3 e as métricas estão no
[protocolo comum](../experimentacao-pesquisa/protocolo/metodologia.md).
Resultados de outras execuções não são parte do corpus de geração.
