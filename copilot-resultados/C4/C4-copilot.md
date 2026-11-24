# C4 — relatório da execução

**Resultado limitado:** oito asserções falharam; duas divergências são
conclusivas e seis não podem ser distinguidas de possível `unknown` técnico.
A Branch Coverage foi **164/1296 (12,65%)**.
Não foi demonstrada uma busca suficiente para afirmar que esta seja a melhor
cobertura documentada possível. A execução cobre apenas uma regra documental,
não toda a funcionalidade da ferramenta.

## Escopo e método

A fonte C4 foi lida após conferência integral do SHA-256. Seu início está
truncado e o texto contém trechos históricos, omissões e contradições. Os
resultados históricos não foram usados como expectativas ou metas. O
[inventário](detalhes-C4/inventario.md) registra os trechos literais, conflitos
e a interpretação adotada.

Para a expressão documental `speed > 100 or (speed > 50 and rain)`, oito
combinações dos predicados foram formalizadas antes da leitura do SUT. O
Z3 independente retornou seis `sat` e dois `unsat`. A regra C4 que declara
substituir a distinção anterior foi interpretada como `sat` descartado e
`unsat` mantido. A adequação dessa interpretação é uma **autoavaliação**, não
uma revisão independente; Z3 não prova fidelidade da tradução. Após os
congelamentos, uma suíte nova invocou o verificador Java real.

Os resultados indicam divergência em relação a essa leitura da fonte, não
qual fonte representa a intenção correta. Não se alteraram as expectativas
para concordar com o SUT.

## Contagens e taxas

| Indicador | Resultado |
|---|---:|
| Registros de oráculo gerados | 19 |
| Conformes, por autoavaliação | 8 |
| Incorretos/sem suporte | 0 |
| Inválidos | 0 |
| Indeterminados | 11 |
| Casos concretos estruturalmente válidos e executáveis | 8 |
| Executados | 8 |
| Aprovados | 0 |
| Asserções falhas com oráculo conforme | 8 |
| Divergências conclusivas | 2 |
| Falhas de asserção sem causa conclusiva | 6 |
| Erros técnicos de execução registrados | 0 |
| Executabilidade | 8/19 = 42,11% |
| Aprovação bruta e de conformes | 0/8 = 0% |
| Indeterminação | 11/19 = 57,89% |
| Conformidade documental, por autoavaliação | 8/(8+0) = 100% |
| Incorretos/sem suporte | 0/19 = 0% |
| Inválidos | 0/19 = 0% |
| Divergência documentação–SUT entre resultados conclusivos | 2/2 = 100% |

Os 11 registros indeterminados descrevem situações sem expectativa única e
não fornecem entradas completas para execução; não foram executados nem
contados como aprovação ou falha. A taxa de conformidade não é validação
independente, e a baixa quantidade de casos limita todas as conclusões.
Resultados completos por caso estão em
[casos.jsonl](detalhes-C4/execucao/casos.jsonl).
Esse arquivo registra provisoriamente as oito falhas como divergências. Na
revisão posterior, apenas F05 e F06 puderam ser confirmados: nos demais, a
possibilidade de `unknown` não foi excluída. O resultado bruto não foi alterado.

## Branch Coverage

| Conjunto | Branches executados / totais | Percentual |
|---|---:|---:|
| Suíte total executada | 164/1296 | 12,65% |
| Subconjunto executável com oráculos conformes | 164/1296 | 12,65% |

Os conjuntos coincidem porque os indeterminados não foram executados. O
denominador inclui as classes de produção dos quatro módulos, inclusive as
classes de mutação não executadas; harness e bibliotecas externas foram
excluídos do relatório. Nenhuma rodada adicional orientada por cobertura foi
executada. Dados brutos: [jacoco.exec](detalhes-C4/execucao/jacoco.exec),
[jacoco.xml](detalhes-C4/execucao/jacoco.xml); visualização:
[branch.svg](detalhes-C4/execucao/branch.svg).

## Passo a passo e reprodução

1. Consulte o [inventário](detalhes-C4/inventario.md), as
   [fórmulas](detalhes-C4/regras.smt2), os [casos](detalhes-C4/casos.json) e as
   [testemunhas Z3](detalhes-C4/resultado-z3.json).
2. Confira os hashes de [oráculos](detalhes-C4/congelamento-oraculos.sha256) e
   [suíte](detalhes-C4/congelamento-suite.sha256), considerando os
   [caminhos reorganizados](detalhes-C4/organizacao.md).
3. Consulte [ambiente e comandos](detalhes-C4/ambiente.md) e a
   [suíte](suite/). O executor recusa sobrescrever a pasta de evidências
   existente; uma nova execução requer destino separado, não substituição
   desta rodada.
4. Examine os [resultados por caso](detalhes-C4/execucao/casos.jsonl), os
   [indeterminados](detalhes-C4/indeterminados.json) e as evidências de cobertura.

## Limitações

- O contexto inicial já continha uma avaliação histórica. O usuário autorizou
  continuar sem usá-la; não é possível apagar essa exposição ou demonstrar
  ausência absoluta de influência.
- O ambiente não era dedicado nem isolado; Docker estava indisponível. O
  usuário dispensou expressamente a exigência de isolamento operacional.
  Hashes antes e depois não excluem interferência transitória.
- A própria fonte inclui material histórico, que foi necessariamente exposto
  durante sua leitura integral, mas não usado como gabarito.
- A suíte cobre somente a classificação de viabilidade de uma expressão;
  saídas, erros, fronteiras e outros comportamentos não foram testados.
  A cobertura baixa deve ser interpretada com esse escopo, sem inferência
  causal ou comparação entre condições.
- Não houve revisão independente da tradução ou classificação dos oráculos.
  Versão específica do modelo, tokens, custo, duração total da geração e
  resposta integral da plataforma: não informado.
- O harness registra apenas presença ou ausência da resposta de viabilidade.
  Na API do SUT uma resposta presente também pode representar `unknown`; o
  valor da atribuição não foi preservado. Assim, nas seis respostas presentes,
  não se pode excluir erro técnico `unknown` e as divergências registradas
  devem ser interpretadas com essa ressalva. Os dois casos de resposta ausente
  não têm essa mesma limitação.
