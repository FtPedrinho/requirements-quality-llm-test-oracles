# Resultados dos experimentos com Copilot

Esta pasta reúne a documentação operacional e os resultados das execuções
realizadas pelo Copilot. Ela não substitui nem altera a
[metodologia da pesquisa](../experimentacao-pesquisa/protocolo/metodologia.md):
em caso de dúvida, prevalece o protocolo. O
[prompt padronizado](../experimentacao-pesquisa/prompts/geracao-de-oraculos-v3.md)
complementa o procedimento de geração.

## 1. Cobertura total comparada

Os dados resumem os relatórios vigentes, sem alterar as evidências.

Os relatórios usam JaCoCo 0.8.16 e denominador de 1.296 branches nas classes
de produção dos quatro módulos, inclusive classes de mutação não executadas;
harness e bibliotecas externas foram excluídos. Os resultados finais abaixo
incluem as extensões quando existentes.

| Experimento | Branch Coverage total final | Subconjunto conforme |
|---|---:|---:|
| C0 — oficial | 847/1.296 — **65,35%** | 847/1.296 — 65,35% |
| C1 | 872/1.296 — **67,28%** | 872/1.296 — 67,28% |
| C2 | 843/1.296 — **65,05%** | 774/1.296 — 59,72% |
| C3 | 323/1.296 — **24,92%** | 323/1.296 — 24,92% |
| C4 — execução limitada | 164/1.296 — **12,65%** | 164/1.296 — 12,65% |

O recorte conforme segue o critério de cada relatório. Em C4, seis dos oito
resultados têm a ressalva técnica descrita na seção 3. Nenhum resultado
demonstra cobertura máxima global ou estabelece causalidade.

Cobertura total final por módulo, em branches cobertos/total:

| Condição | Core, incluindo mutação | Requirements | Z3 | CLI |
|---|---:|---:|---:|---:|
| C0 | 267/411 | 115/162 | 249/386 | 216/337 |
| C1 | 271/411 | 115/162 | 255/386 | 231/337 |
| C2 | 257/411 | 109/162 | 252/386 | 225/337 |
| C3 | 140/411 | 82/162 | 0/386 | 101/337 |
| C4 | 10/411 | 52/162 | 102/386 | 0/337 |

O detalhamento C0 foi obtido do [XML acumulado final](C0/detalhes-C0/evidencias-originais/combinado2-jacoco.xml);
os demais estão nos relatórios ou evidências de cada condição.

## 2. Testes e classificações comparados

Os totais incluem extensões, mas não contam uma repetição técnica como novo
caso. As unidades não são equivalentes: há casos por valoração, asserções
compostas e registros indeterminados sem entradas executáveis.

| Experimento | Total criado ou registrado | Executáveis / executados | Aprovaram | Falhas de asserção | Indeterminados | Inválidos | Erros técnicos de caso |
|---|---|---:|---:|---:|---|---:|---|
| C0 | 106 registros | 98 / 98 | 98 | 0 | 8 não executados | 0 | 0 |
| C1 | 56 registros | 51 / 51 | 48 | 2 | 5 não executados | 0 | 1 na avaliação |
| C2 | 177 casos distintos | 177 / 177 | 172 | 1 | 4 executados sem julgamento | 0 | 0 identificados |
| C3 | 30 casos distintos e 15 grupos de conflito | 30 / 30 | 30 após repetição | 0 semânticas | 15 grupos não executáveis | 0 classificados | 1 inicial, repetido com sucesso |
| C4 | 19 registros, incluindo 8 casos concretos | 8 / 8 | 0 | 8 | 11 não executados | 0 | 0 confirmados; 6 resultados inconclusivos |

Em C3, os 15 grupos de conflito não são testes completos nem devem ser
somados aos 30 casos como testes adicionais. Em C4, as oito falhas brutas
incluem seis para as quais não se descartou `unknown` técnico; somente duas
divergências são conclusivas.

As taxas adicionais abaixo são indicadores históricos preservados nesta
comparação; não são métricas exigidas pelo protocolo atual e não substituem
as contagens acima.

| Experimento | Executabilidade | Aprovação | Indeterminação | Conformidade documental | Divergência documentação–SUT |
|---|---:|---:|---:|---:|---:|
| C0 | 98/106 — 92,45% | 98/98 — 100% | 8/106 — 7,55% | 98/98 — 100% | 0/98 — 0% |
| C1 | 51/56 — 91,07% | 48/50 — 96% bruta; 48/49 — 97,96% conforme | 5/56 — 8,93% | 50/51 — 98,04% | 1/49 — 2,04% |
| C2 | 177/177 — 100% | 172/173 — 99,42% agregada | 4/177 — 2,26% nominal | 173/173 — 100% nominal | 1/173 — 0,58% nominal |
| C3 | 30/30 — 100% | 30/30 — 100% conclusiva | 15/29 — 51,72% dos registros | 14/14 — 100% dos oráculos determinados | 0/30 — 0% conclusiva |
| C4 | 8/19 — 42,11% | 0/8 — 0% bruta registrada | 11/19 — 57,89% | 8/8 — 100% | 2/2 — 100% dos resultados conclusivos |

Em C3, a taxa de indeterminação usa 14 oráculos determinados e 15 grupos de
conflito. Em C2, a divergência nominal C108 tem a ressalva documental
detalhada abaixo. C1 teve um oráculo sem suporte; nas demais condições não
foram classificados oráculos sem suporte. As classificações são
autoavaliações, não revisão independente.

## 3. Execuções, extensões e exceções

### C0 — baseline e duas extensões

| Rodada | Casos e resultados | Branch Coverage total | Subconjunto conforme |
|---|---|---:|---:|
| Baseline | 67 registros: 64 executados e aprovados; 3 indeterminados | 290/1.296 — 22,38% | 290/1.296 — 22,38% |
| Extensão 1 isolada | 21 novos casos, todos aprovados | 778/1.296 — 60,03% | 778/1.296 — 60,03% |
| Baseline + extensão 1 | 85 casos executados | 817/1.296 — 63,04% | 817/1.296 — 63,04% |
| Extensão 2 isolada | 13 novos casos, todos aprovados | 430/1.296 — 33,18% | 430/1.296 — 33,18% |
| Acumulado final | 98 casos executados e aprovados | 847/1.296 — 65,35% | 847/1.296 — 65,35% |

As extensões acrescentaram, respectivamente, 527 e 30 branches ao acumulado.
Outros cinco registros indeterminados foram identificados após a cobertura e
não executados. Não foram reportados erros técnicos nem oráculos sem suporte
ou inválidos. Durações: 38,936 s no baseline, 43,712 s na extensão 1 e
29,561 s na extensão 2, incluindo relatórios.
[Relatório C0](C0/C0-copilot.md) · [suíte](C0/suite/) · [detalhes](C0/detalhes-C0/).

### C1 — baseline e duas extensões

| Rodada | Casos e resultados | Branch Coverage total | Subconjunto conforme |
|---|---|---:|---:|
| Baseline | 36 registros: 31 executados, 29 aprovados, 1 falha e 1 erro técnico; 5 indeterminados | 771/1.296 — 59,49% | 771/1.296 — 59,49% |
| Extensão 1 isolada | 19 casos: 18 aprovados e 1 falha sob oráculo sem suporte | 571/1.296 — 44,06% | 525/1.296 — 40,51% |
| Baseline + extensão 1 | Acumulado | 872/1.296 — 67,28% | 839/1.296 — 64,74% |
| Extensão 2 isolada | 1 caso aprovado | 197/1.296 — 15,20% | 197/1.296 — 15,20% |
| Acumulado final | 51 casos executados; 48 aprovações | 872/1.296 — 67,28% | 872/1.296 — 67,28% |

A extensão 1 acrescentou 101 branches ao acumulado total. A extensão 2 não
aumentou o total, mas acrescentou 33 branches ao recorte conforme. A primeira
tentativa da extensão 1 teve erro de infraestrutura antes dos casos.
No baseline, B23 foi classificado como divergência, com interpretação a
revisar, e B31 como erro de decodificação; E01 repetiu B31 e passou.
E02 falhou sob oráculo sem suporte; E20 testou o conteúdo sem essa suposição.
Somatórios registrados: 81,502 s, 74,771 s e 2,468 s; um caso não registrou
duração.
[Relatório C1](C1/C1-copilot.md) · [suíte](C1/suite/) · [detalhes](C1/detalhes-C1/).

### C2 — baseline e duas extensões

| Rodada | Casos e resultados | Branch Coverage total | Subconjunto conforme |
|---|---|---:|---:|
| Baseline | 119 executados: 114 aprovados, 1 falha e 4 sem julgamento | 797/1.296 — 61,50% | 683/1.296 — 52,70% |
| Extensão 1 acumulada | 47 novos casos, todos aprovados | 823/1.296 — 63,50% | 753/1.296 — 58,10% |
| Extensão 2 acumulada | 11 novos casos, todos aprovados | 843/1.296 — 65,05% | 774/1.296 — 59,72% |

As extensões acrescentaram 26 e 20 branches ao total, respectivamente. Os
11 casos da extensão 2 foram formalizados após a inspeção do SUT e da
cobertura, mas congelados antes da própria execução. C108 permanece falho
com classificação nominal conforme; uma revisão apontou ambiguidade. Se
excluído da análise de divergência inequívoca, restam 0/172 casos
conclusivos, sem apagar a falha. Não foram identificados erros de execução.
Tempos das JVMs totais: 10,357 s, 14,638 s e 20,161 s; dos conformes:
8,859 s, 17,954 s e 21,452 s. Os acumulados repetem casos anteriores.
[Relatório C2](C2/detalhes-C2/relatorio.md) · [suíte](C2/suite/).

### C3 — baseline, repetição técnica e extensão

| Rodada | Casos e resultados | Branch Coverage total | Subconjunto conforme |
|---|---|---:|---:|
| Baseline | 14 executados: 13 aprovados e 1 erro técnico | 304/1.296 — 23,46% | 304/1.296 — 23,46% |
| Repetição F03 isolada | Mesmo caso, aprovado | 219/1.296 — 16,90% | não informado como recorte separado |
| Extensão isolada | 16 novos casos, todos aprovados | 323/1.296 — 24,92% | não informado como recorte separado |
| Acumulado final | 30 casos distintos aprovados após repetição | 323/1.296 — 24,92% | 323/1.296 — 24,92% |

A extensão acrescentou 19 branches ao baseline. O recorte adicional do
baseline apenas com casos conformes conclusivos foi 266/1.296 (20,52%).
F03 teve erro de leitura de stdout, preservado, e passou na repetição;
houve também erros auxiliares corrigidos sem todos os logs. Os 15 grupos
indeterminados não foram executados. O módulo Z3 ficou em 0/386. Durações:
24,844626 s no baseline, 0,741502 s na repetição e 14,402325 s na extensão.
[Relatório C3](C3/detalhes-C3/relatorio-final.md) · [suíte](C3/suite/).

### C4 — baseline sem extensão

Foram executados oito casos concretos contra uma única regra: as oito
asserções falharam e a cobertura total e conforme foi 164/1.296 (12,65%).
Há 11 registros indeterminados sem execução. O resultado bruto marcou oito
divergências, mas a revisão confirmou somente duas: nas outras seis, o
harness não preservou informação suficiente para excluir `unknown` do
solver. Não houve erro técnico confirmado nem oráculo sem suporte ou inválido
registrado. A execução Java durou 6,308 s.
[Relatório C4](C4/C4-copilot.md) · [suíte](C4/suite/) · [detalhes](C4/detalhes-C4/).

### Limites comuns e comparabilidade

Os relatórios indicam o commit de referência
`2aec3564c30890031db86bd2cc1bb015794d5d2e`; C4 não verificou a correspondência
integral da árvore de trabalho. Modelo: **GPT 6.1 Terra (informado pelo pesquisador em 24/11/2026, após a coleta)**. Versão exata, configuração,
chamadas, tokens e custo são **não informados**. Não se presume equivalência
entre ambientes, solvers, unidades de teste ou harnesses.

Em 24/11/2026 esta pasta foi renomeada de `copilot-resultados` para
`gpt-6.1-terra-resultados`. Scripts e relatórios foram atualizados; logs,
saídas e manifestos de hash mantêm o nome antigo.

Não houve cegamento integral demonstrado: as fontes contêm material
histórico e os relatórios registram exposição prévia de contexto. Em C3
foram enumerados caminhos de outras suítes; em C4 o usuário dispensou o
isolamento operacional. As extensões C0–C3 foram orientadas por cobertura;
C4 não teve extensão. As diferenças são descritivas e não demonstram
causalidade ou equivalência metodológica.

## Procedimento de cada execução

1. Iniciar uma geração separada e registrar o contexto realmente recebido.
   Não consultar resultados, oráculos, suítes, históricos ou guias de
   experimentos anteriores. Se houver exposição anterior ao SUT ou a
   resultados, ou não for possível garantir isolamento, registrar o desvio;
   não afirmar cegamento integral.
2. Selecionar exclusivamente a fonte normativa da condição indicada no
   protocolo e verificar seu SHA-256. Registrar também os hashes da
   metodologia e do prompt utilizado. A fonte C1 atual é
   [tool-readme-C1.md](../experimentacao-pesquisa/experimentacao-1/documentation/tool-readme-C1.md),
   conforme a decisão registrada no protocolo.
3. Antes de inspecionar o código ou a saída do SUT, inventariar a
   documentação e derivar expectativas, citações literais, regras, casos
   e indeterminações. Formalizar em SMT-LIB e usar Z3 independente para
   verificar fórmulas e obter testemunhas. Registrar versão, consultas,
   resultados, objetivo e limites; a satisfatibilidade não prova fidelidade
   da tradução. Congelar por hash a análise e os oráculos.
4. Somente depois, inspecionar o SUT, mapear os comportamentos à
   implementação, criar uma suíte nova e congelá-la por hash antes da
   execução. Não usar o comportamento observado para criar expectativas.
   Manter falhas de oráculos conformes; omissões e conflitos sem expectativa
   única são indeterminados, não falhas semânticas.
5. Executar a suíte na implementação real com instrumentação. Após o
   baseline, branches não cobertos podem orientar extensões separadas;
   suas expectativas precisam ter suporte documental e ser congeladas antes
   da execução. Preservar cada rodada e seus resultados sem sobrescrever o
   baseline. Não declarar cobertura máxima global sem busca exaustiva.
6. Registrar os resultados e limitações no diretório da condição, incluindo
   entradas, oráculos, evidências, ferramentas, comandos, dependências,
   ambiente, commit do SUT e hashes. Não alterar fontes do SUT nem fontes
   normativas ou experimentos anteriores.

## Relato e métricas

Para cada rodada, registrar a classificação do oráculo separadamente do
estado de execução, as contagens e taxas definidas no protocolo, e os
resultados por caso. Incluir testes gerados, executáveis, executados,
aprovados, falhos, indeterminados, inválidos e erros técnicos; identificar
divergências documentação–SUT sem afirmar qual fonte é objetivamente
correta. Cada caso indeterminado registrado integra o numerador e o
denominador da taxa de indeterminação, mesmo sem execução diagnóstica.

Reportar **Branch Coverage** instrumentada, em números absolutos e percentuais,
para a suíte total e, separadamente, para o subconjunto válido/executável com
oráculos conformes, indicando escopo, exclusões e versão da ferramenta.
Condition Coverage e Mutation Score não são métricas da pesquisa. Para
denominador zero, registrar `não calculável (denominador zero)`; para
instrumentação indisponível, registrar `não coletado` e a razão.

Preservar prompt e resposta integrais, hashes das entradas, modelo e
configuração, chamadas, tokens, duração e custos quando disponibilizados;
usar `não informado` para valores ausentes, sem estimativa. Explicitar
ausência de revisor independente, limites de cobertura, infraestrutura,
comparabilidade e qualquer perda de isolamento. A adoção oficial de um
resultado não elimina suas limitações.

## Organização

Manter cada condição e repetição em seu próprio diretório, com relatório,
casos, harness, evidências, manifestos e resultados brutos. Acrescentar ao
índice acima e à apresentação padronizada o caminho do relatório somente
depois de sua criação. Usar o [modelo de apresentação](../experimentacao-pesquisa/protocolo/modelo-relatorio.md),
sem modificar evidências ou relatórios congelados. Não
reutilizar nem sobrescrever experimentos anteriores; registros existentes
podem manter sua organização original.
