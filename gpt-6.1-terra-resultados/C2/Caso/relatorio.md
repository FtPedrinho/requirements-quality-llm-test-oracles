# Experimento C2 — nova rodada

## Resumo

A documentação C2 foi lida integralmente; os oráculos iniciais foram registrados e congelados antes da nova inspeção do sistema. Uma suíte nova foi executada contra o Java de produção, seguida de duas extensões. A melhor Branch Coverage documentada alcançada foi **843/1296 (65,05%)**, ou **774/1296 (59,72%)** considerando apenas os casos inicialmente classificados como conformes.

Dos 177 casos distintos, 172 passaram, um falhou e quatro foram executados sem julgamento. O caso C108 permanece falho conforme o oráculo congelado, mas uma revisão posterior identificou ambiguidade relevante em sua fundamentação; uma divergência inequívoca não está estabelecida.

Não houve cegamento garantido: o contexto já continha informações anteriores e o documento completo inclui material histórico. Nenhum resultado histórico foi conscientemente usado como gabarito ou meta, mas influência residual não pode ser excluída. Não houve revisor independente. Os 11 casos concretos da extensão 2 foram formalizados **depois da inspeção do código e da cobertura**, a partir de regras gerais documentais já congeladas; portanto, não atendem à exigência mais estrita de congelar cada formalização concreta antes da inspeção do SUT. Foram congelados antes da execução da própria extensão. Não se alteraram as expectativas inicialmente congeladas.

Não se executaram algoritmos ou testes de mutação, nem se coletaram Condition Coverage ou Mutation Score. Não há demonstração de máximo global de cobertura. Também não se verificou equivalência metodológica ou operacional com rodadas C0 ou C1.

## Fontes, ambiente e cronologia

- Condição C2: clareza baixa e consistência alta pretendidas, não assumidas como atingidas. A leitura completa permite examinar toda a fonte, mas não garante uma avaliação global exaustiva de clareza, consistência ou cobertura documental.
- Fonte normativa C2: `61C4062B5FC6B4F364F40465B0E017C80E0FA0C5433412EB2E925C545F6EFBE1`, igual ao valor do protocolo. Protocolo: `EC3F96C59C6C2A3570E7833B2C561B6DB38BE415B41C10A7F383BF5DA2FA6B1F`. Prompt: `A89A9F10E579B0189AB83CD845A42764637AB6754BD28D2E567D8D6A6B401E3F`. Fontes locais do workspace; versão documental não informada além dos hashes.
- Commit de referência do SUT: `2aec3564c30890031db86bd2cc1bb015794d5d2e`; Windows 10.0.26200, X64. A documentação C2 aparece modificada em relação ao commit no estado do workspace, mas seu hash corresponde ao protocolo e permaneceu igual ao registrado no início da rodada. Os 51 arquivos de produção conferidos mantiveram seus hashes; o status dos diretórios de produção e POMs estava limpo.
- Java/javac 21.0.3; Maven ausente do PATH; Python 3.13.5; Z3 independente via Python 5.4.1.0; JaCoCo 0.8.16 e Jackson 2.17.2 em cache. O executável oficial Z3 4.13.4 foi obtido em diretório isolado para o SUT, após verificar que não estava no PATH. Não se presume equivalência entre versões. Origem e hashes dos arquivos, inclusive bibliotecas, constam em [preparação](metadados/preparacao.md) e [ambiente adicional](metadados/ambiente-adicional.md); assinatura ou hash publicado independente do download não foram verificados.
- Plataforma: Copilot SDK no VS Code. Modelo: **GPT 6.1 Terra (informado pelo pesquisador em 24/11/2026, após a coleta)**. Versão exata do modelo, parâmetros, número efetivo de chamadas, repetições de geração, tokens, custo e recursos da máquina: **não informado**. Planejou-se uma geração; as JVMs total e conformes são execuções distintas da mesma suíte, não repetições independentes de geração.
- Início registrado: 23/11/2026 às 11:10:47,937 -03:00. Congelamento inicial: 11:19:57,918; suíte baseline: 11:22:26,556; relatório JaCoCo total do baseline: 11:23:08; congelamentos das extensões 1 e 2: 11:26:35,314 e 11:31:28,511; relatório JaCoCo total da extensão 2: 11:32:01. Consolidação e verificações até pelo menos 11:37:41: duração decorrido até esse marco aproximadamente 26 min 53 s. Horários de XML são de última gravação, não tempos exatos de início ou fim da execução.

A [solicitação](metadados/solicitacao.md), a [resposta de geração e planejamento](oraculos/analise.md) e o [inventário](documentacao/inventario.md) estão preservados. Os manifestos SHA-256 são [oráculos](metadados/congelamento-oraculos.txt), [baseline](metadados/congelamento-baseline.txt), [extensão 1](metadados/congelamento-extensao-1.txt) e [extensão 2](metadados/congelamento-extensao-2.txt); incluem prompt, resposta, casos, fórmulas, entradas e harnesses aplicáveis. Os [hashes das fontes Java](metadados/fontes-sut-sha256.txt) também estão preservados.

## Método

1. A partir da referência C2, registraram-se requisitos, citações, formalizações, entradas, expectativas e omissões; a classificação é autoavaliação. Criaram-se 119 casos e as consultas SMT antes da nova inspeção do SUT. As expressões escolhidas tiveram suas combinações esgotadas, não toda a documentação; não houve otimização global da suíte.
2. O Z3 independente 5.4.1.0 executou 175 consultas iniciais: 93 `sat` e 82 `unsat`; na extensão 2, outras 11: seis `sat` e cinco `unsat`. Foram preservados [SMT inicial](oraculos/formulas.smt2), [resultados e testemunhas](oraculos/resultado-z3.json), [reexecução inicial](oraculos/reexecucao-z3.txt), [SMT da extensão](extensao-2/formulas.smt2) e [reexecução da extensão](extensao-2/reexecucao-z3.txt). O limite foi 60 s por consulta; não houve `unknown` ou timeout relatado. Z3 valida a fórmula, não a fidelidade de sua tradução do texto.
3. Após o congelamento inicial, código de produção foi compilado com `javac` em diretório isolado, sem alteração das fontes. O harness novo foi compilado separadamente; casos com expectativa determinada foram julgados pelo oráculo, e os demais apenas observados. Falhas foram preservadas.
4. A extensão 1 compôs 47 casos a partir de expectativas concretas congeladas. A extensão 2 acrescentou 11 instâncias de regras gerais congeladas, com a ressalva temporal do resumo. Os [mapeamentos do baseline](baseline/mapa.md), [extensão 1](extensao-1/mapa.md) e [extensão 2](extensao-2/mapa.md) registram módulos visados e lacunas. Não foi realizado mapeamento exaustivo dos branches restantes.

O documento apresenta omissões, ambiguidades e grafia degradada; expectativas não foram inventadas para desempatar lacunas. A conformidade de um oráculo com a documentação não demonstra correção geral do SUT.

## Resultados dos casos

Unidade de contagem: um caso/harness com um julgamento agregado. Alguns casos compostos verificam várias decisões; sua aprovação exige que todas as verificações do caso passem. Por isso, as taxas abaixo são **por julgamento agregado de caso**; o número de comparações atômicas avaliadas e a aprovação por comparação atômica não foram registrados e não são calculáveis a partir da contagem resumida.

| Rodada | Gerados / estruturalmente válidos / executáveis / executados | Conformes | Incorretos ou sem suporte | Inválidos | Indeterminados | Passou | Falhou | Sem julgamento | Erros de execução |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline | 119 / 119 / 119 / 119 | 115 | 0 | 0 | 4 | 114 | 1 | 4 | 0 |
| Extensão 1, novos | 47 / 47 / 47 / 47 | 47 | 0 | 0 | 0 | 47 | 0 | 0 | 0 |
| Extensão 2, novos | 11 / 11 / 11 / 11 | 11 | 0 | 0 | 0 | 11 | 0 | 0 | 0 |
| Total distinto | 177 / 177 / 177 / 177 | 173 | 0 | 0 | 4 | 172 | 1 | 4 | 0 |

Cada caso corresponde a um oráculo agregado; os 47 compostos reutilizam expectativas existentes, não 47 novas regras semânticas. Não houve caso com status `NÃO EXECUTADO — INVÁLIDO`, erro técnico identificado de ferramenta ou `ERRO DE EXECUÇÃO`. Os quatro indeterminados iniciais são um por omissão e três por ambiguidade. A revisão posterior identificou **um caso adicional potencialmente indeterminado**, C108, mas ele já integra os 177 e sua classificação congelada foi mantida: não é uma nova execução nem deve ser contado duas vezes. Famílias de branches sem especificação suficiente constam dos mapas; não foram individualizadas exaustivamente como novos casos.

| Indicador nominal | Baseline | Extensão 1, novos | Extensão 2, novos | Total distinto |
|---|---:|---:|---:|---:|
| Executabilidade | 119/119 = 100% | 47/47 = 100% | 11/11 = 100% | 177/177 = 100% |
| Aprovação agregada determinada | 114/115 = 99,13% | 47/47 = 100% | 11/11 = 100% | 172/173 = 99,42% |
| Aprovação entre conformes | 114/115 = 99,13% | 47/47 = 100% | 11/11 = 100% | 172/173 = 99,42% |
| Aprovação entre incorretos/sem suporte | não calculável (denominador zero) | não calculável (denominador zero) | não calculável (denominador zero) | não calculável (denominador zero) |
| Indeterminação | 4/119 = 3,36% | 0/47 = 0% | 0/11 = 0% | 4/177 = 2,26% |
| Conformidade documental | 115/115 = 100% | 47/47 = 100% | 11/11 = 100% | 173/173 = 100% |
| Incorretos/sem suporte sobre gerados | 0/119 = 0% | 0/47 = 0% | 0/11 = 0% | 0/177 = 0% |
| Inválidos sobre gerados | 0/119 = 0% | 0/47 = 0% | 0/11 = 0% | 0/177 = 0% |
| Divergência nominal entre conformes conclusivos | 1/115 = 0,87% | 0/47 = 0% | 0/11 = 0% | 1/173 = 0,58% |

As taxas e classificações são as inicialmente congeladas, sem reclassificar C108 após a execução. **Sensibilidade:** se a revisão documental posterior de C108 for aceita, excluir esse caso da análise de divergência inequívoca deixa 0/172 casos conclusivos restantes; isso não apaga sua falha nem altera o resultado nominal. A [revisão de C108](baseline/revisao-c108.md) explica a diferença.

Detalhes de entrada, expectativa, observação, classificação, estado, erro, tempo e caminhos de evidência por caso: [CSV](resultados/casos-detalhados.csv) e [JSON](resultados/casos-detalhados.json). Os casos iniciais e suas citações e justificativas estão em [oráculos iniciais](oraculos/casos.json); os compostos e posteriores em [extensão 1](extensao-1/casos.json) e [extensão 2](extensao-2/casos.json). O JSON bruto de cada harness e os arquivos de saída por caso permanecem nos respectivos diretórios de rodada.

## Branch Coverage e custo de execução

O denominador inclui todas as classes de produção dos quatro módulos, inclusive classes de mutação não executadas; harness e bibliotecas externas foram excluídos. O XML lista 73 arquivos de classe compilados de 51 fontes; o log JaCoCo informa 69 classes e quatro entradas do XML não têm contador `CLASS`. A lista e os contadores individuais estão em [escopo de classes](resultados/escopo-classes.csv).

| Acumulado | Casos distintos | Total, branches cobertos/totais | Apenas conformes, branches cobertos/totais | Ganho total sobre anterior |
|---|---:|---:|---:|---:|
| Baseline | 119 | 797/1296 = 61,50% | 683/1296 = 52,70% | — |
| Extensão 1 | 166 | 823/1296 = 63,50% | 753/1296 = 58,10% | +26 branches; +2,01 pontos percentuais |
| Extensão 2 | 177 | 843/1296 = 65,05% | 774/1296 = 59,72% | +20 branches; +1,54 pontos percentuais |

Ganhos do subconjunto conforme: +70 e +21 branches, respectivamente. Arredondamentos podem diferir na subtração dos percentuais exibidos. No total final, há 453 branches não cobertos, incluindo 64 em classes de mutação, cuja execução foi proibida. Demais lacunas incluem caminhos de formatos, erros internos e transporte não integralmente mapeados; não se presume que todos sejam impossíveis de testar documentalmente.

Escopo final por módulo: `mcdc-core` 257/411, `mcdc-requirements` 109/162, `mcdc-z3` 252/386 e `mcdc-cli` 225/337. Dados e visualização: [cobertura CSV](resultados/cobertura.csv) e [painel](resultados/painel.html). XML e CSV originais do JaCoCo estão em cada diretório de rodada, por exemplo [XML total final](extensao-2/total-jacoco.xml) e [XML conforme final](extensao-2/conformes-jacoco.xml).

Tempos registrados de execução das JVMs, sem compilação e geração de relatório: baseline total 10,357 s e conformes 8,859 s; acumulado extensão 1 total 14,638 s e conformes 17,954 s; acumulado extensão 2 total 20,161 s e conformes 21,452 s. As medições incluem reiniciar e repetir baseline e extensões anteriores em JVMs distintas; diferenças não são custo isolado rigoroso da extensão.

## Reprodução, integridade e limitações

Executar os scripts a partir da raiz de um **workspace separado**, com as fontes e o mesmo caminho relativo `gpt-6.1-terra-resultados\C2\Caso`. Os scripts codificam esse caminho: copiar a rodada para outro nome não basta. Copiar para lá os harnesses, scripts, entradas, casos congelados das extensões e dependência Z3, sem diretórios de classes ou saídas de execução; para regenerar os oráculos iniciais, não copiar os três arquivos gerados por `gerar.py`. Os scripts usam criação exclusiva e não devem ser executados sobre esta rodada preservada:

```powershell
python gpt-6.1-terra-resultados\C2\Caso\oraculos\gerar.py
powershell -NoProfile -File gpt-6.1-terra-resultados\C2\Caso\baseline\executar.ps1
powershell -NoProfile -File gpt-6.1-terra-resultados\C2\Caso\extensao-1\executar.ps1
powershell -NoProfile -File gpt-6.1-terra-resultados\C2\Caso\extensao-2\executar.ps1
python gpt-6.1-terra-resultados\C2\Caso\resultados\consolidar.py
python gpt-6.1-terra-resultados\C2\Caso\resultados\detalhar.py
```

Os scripts de extensão usam os casos já congelados; suas respectivas preparações e reexecuções SMT estão preservadas nos diretórios correspondentes. A cópia deve manter a estrutura e os caminhos esperados pelos scripts, com jars em cache e Z3 oficial identificados nos metadados. O baseline pode devolver código 1 por causa de C108; isso é falha de teste preservada, não erro de infraestrutura.

Na verificação final, os manifestos conferiram 17, 4, 5 e 8 arquivos, respectivamente, sem divergências; as 51 fontes Java também conferiram. Uma regeneração independente do oráculo inicial em diretório temporário produziu hashes idênticos para casos, fórmulas e resultados Z3. A cobertura foi conferida diretamente nos XMLs e o inventário de 73 classes foi comparado aos arquivos compilados. O transcript integral de todos os comandos da sessão não foi preservado; scripts, logs de execução, comandos principais e hashes permitem auditoria parcial.

O harness do baseline filtra duas linhas agregadas da CLI relativas a métricas fora do escopo; portanto seus arquivos de saída **não são logs brutos integrais**. O restante das saídas capturadas e os relatórios brutos JaCoCo foram preservados. Este resultado não prova ausência de defeitos, causalidade, equivalência entre versões ou máximo global de cobertura.
