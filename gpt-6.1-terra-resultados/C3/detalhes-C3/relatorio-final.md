# Experimento C3 — resultados e limitações

## Condição, isolamento e rastreabilidade

A única fonte normativa de comportamento foi [tool-readme-C3.md](fonte-C3.md), SHA-256 `F18B0821D79C7315486C13D5260FA2F6D6E9418EF03B86CDE58E66B91B7B87A3`, igual ao protocolo. O [prompt v2 integral](prompt-v2.md) tem SHA-256 `A89A9F10E579B0189AB83CD845A42764637AB6754BD28D2E567D8D6A6B401E3F`. O protocolo tem SHA-256 `EC3F96C59C6C2A3570E7833B2C561B6DB38BE415B41C10A7F383BF5DA2FA6B1F`.

O contexto inicial continha uma informação qualitativa de experimento anterior; o usuário autorizou prosseguir apesar dela. Uma busca ampla também enumerou caminhos de arquivos em suítes de outras condições, sem abrir seus conteúdos. A tentativa foi interrompida e retomada por instrução do usuário para ignorar resultados anteriores. A própria fonte C3 contém dados históricos, lidos por exigir-se leitura integral; eles não foram usados intencionalmente como gabarito ou meta. **Não é demonstrável ausência absoluta de influência nem cegamento.** Não foram consultados conteúdos de suítes ou resultados de outras condições.

O [inventário](inventario-documental.md) registra comportamentos, lacunas e 15 grupos de conflito. Há clareza local em opções e exemplos, mas contradições explícitas em pontos centrais impedem caracterizar a condição como consistentemente especificada. Não se usam os rótulos pretendidos como evidência empírica.

## Etapa documental e Z3

Antes de ler o código do SUT, foram produzidas 11 tabelas booleanas, com 48 vetores concretos, e três propriedades de integração. As expectativas, citações, entradas e classificação estão em [oraculos.json](oraculos.json) e [oraculos-integracao.json](oraculos-integracao.json); conflitos estão no inventário. A enumeração exaustiva cobriu as atribuições booleanas das guardas selecionadas, não todas as entradas possíveis do sistema.

O Z3 independente `z3-solver` Python 5.4.1.0, identificador relatado `145c0c51570a357cc558ce898ce77573ba9d4fbf`, executou [formulas.smt2](formulas.smt2): 48 consultas `sat` com testemunhas em [z3-resultados.txt](z3-resultados.txt). As três consultas de [integracao.smt2](integracao.smt2) também retornaram `sat`, conforme [integracao-z3.txt](integracao-z3.txt). O objetivo foi verificar viabilidade das fórmulas e enumerar os vetores das tabelas; não houve otimização de uma suíte mínima. As fórmulas de integração modelam predicados e identificadores, não provam que o SUT os satisfaça.

O solver não valida a fidelidade da tradução documental. A classificação e a revisão foram feitas pela própria IA; **não houve revisão independente**. A primeira tentativa de geração falhou por declarações SMT duplicadas, corrigidas antes de se gerar e congelar os oráculos. A duração dessa etapa e o log completo dessa primeira falha não foram disponibilizados.

O [manifesto documental](manifesto-oraculos.sha256), hash `A35EBA08004E18BDA9AAF110C3ACCDB9997C22F2058ED106F810EB2156DEB0C9`, foi criado antes da inspeção do código. A [suíte e as entradas](manifesto-suite.sha256), hash `7128DA58F0046AC8C1751B3C7AE41E492B34BD230A64B164FF7D7ED1D2203FB1`, foram congeladas antes da execução. A [repetição técnica](manifesto-repeticao-f03.sha256), hash `C279A89FFAF20F63F08BF66C1B6C000A26F09EB2EB21058468FD27475DAF1DBD`, e a [extensão](manifesto-extensao.sha256), hash `BC62C598B2CB9306E9473948806FCD3C4D973894C57A5A826FB7A2629CF92860`, foram congeladas antes de suas respectivas execuções.

## Ambiente e execução

- Commit informado: `2aec3564c30890031db86bd2cc1bb015794d5d2e`. O workspace geral tem alterações; o Git não reportou alterações nas quatro árvores de fontes de produção. As 51 fontes tiveram hashes conferidos sem mudança depois da execução: [manifesto](manifesto-fontes-sut.sha256) e [estado Git](estado-fontes-sut.txt).
- Windows NT 10.0.26200.0 x64; Java/Javac 21.0.3; Python 3.13.5; Git 2.41.0.windows.1; JaCoCo `0.8.16.202610240946`; Jackson 2.17.2. Maven e executável externo `z3` não encontrados no PATH. Não foram instalados pacotes.
- Compilação: `javac -encoding UTF-8 -g -cp <tres jars Jackson 2.17.2> -d build\classes <51 fontes de producao>`. Código de saída 0; classes compiladas no diretório deste experimento, não no SUT. Os hashes dos binários, dependências e classes estão nos manifestos.
- Execução: [executar-suite.py](executar-suite.py), depois [repetir-f03.py](repetir-f03.py) e [executar-extensao.py](executar-extensao.py). Cada comando Java real, entrada, código de saída quando capturado, duração, asserção e evidência estão nos resultados estruturados e diretórios de [evidências](evidencias/). Os códigos de saída não foram julgados porque C3 os especifica de forma contraditória.
- Modelo: **GPT 6.1 Terra (informado pelo pesquisador em 24/11/2026, após a coleta)**. Versão exata, configuração, chamadas, tokens, custo, duração total da geração e transcrição integral da plataforma: **não informado**. O conteúdo do prompt foi preservado; não se afirma preservação de uma transcrição integral indisponível.

### Contagens e taxas

Uma asserção composta por caso é a unidade de aprovação; seus vários vetores ou subverificações não são contados como testes separados.

| Rodada | Casos executados | Aprovados | Falhas semânticas | Erros técnicos | Aprovação entre asserções avaliadas | Soma das durações |
|---|---:|---:|---:|---:|---:|---:|
| Baseline | 14 | 13 | 0 | 1 | 13/13 = 100% | 24,844626 s |
| Repetição técnica de F03 | 1 | 1 | 0 | 0 | 1/1 = 100% | 0,741502 s |
| Extensão orientada por cobertura | 16 | 16 | 0 | 0 | 16/16 = 100% | 14,402325 s |
| Invocações somadas | 31 | 30 | 0 | 1 | 30/30 = 100% | 39,988453 s |

Existem 30 casos distintos com entradas completas: 14 no baseline e 16 na extensão. Todos eram estruturalmente válidos e foram aceitos e invocados: executabilidade 30/30 = 100%. A repetição é uma invocação adicional, não um caso distinto. No baseline, F03 chegou a executar o Java e produzir saída e dados JaCoCo, mas a leitura de stdout falhou: o Java informou `stdout.encoding=Cp1252`, enquanto o harness tentou UTF-8. O erro original permanece registrado; a repetição, congelada separadamente e com a mesma asserção, passou. O código de saída do processo original F03 não foi capturado antes do erro. Os bytes originais foram preservados.

Nenhuma asserção conforme avaliada divergiu: 0/30 nas invocações com resultado conclusivo. Isto é ausência de divergência **neste conjunto**, não prova de conformidade geral do SUT. A classificação foi autorrevisada: 14 oráculos determinados distintos considerados conformes, zero classificados como sem suporte. Conformidade entre determinados classificados: 14/14 = 100%.

Para não ocultar ambiguidades, contam-se conservadoramente os 15 registros I01–I15 como registros de oráculos indeterminados, mesmo sendo grupos de conflito e não casos com entradas completas. Assim, a taxa sobre 14 determinados + 15 registros é 15/29 = **51,72%**; sem suporte e inválidos classificados: 0/29 em cada categoria. Esses 15 registros não são testes executáveis nem foram executados. Não se deve interpretar essa taxa como número de combinações individuais afetadas. A extensão reutilizou oráculos existentes e não gerou novas expectativas semânticas.

Houve ainda falhas técnicas em comandos auxiliares de investigação de API/quoting e na primeira tentativa de criar o manifesto da repetição; foram corrigidas antes da etapa dependente. Não são falhas funcionais do SUT e seus logs completos não foram preservados.

## Branch Coverage

JaCoCo foi aplicado às classes compiladas das quatro árvores de produção, com harness Python e bibliotecas externas fora do denominador. Os 73 arquivos `.class` compilados aparecem no XML, incluindo as seis classes em `core/mutation`; estas não foram executadas. O log JaCoCo informa “Analyzing 69 classes”; a comparação automatizada dos nomes nos XMLs com os 73 arquivos compilados não encontrou classes ausentes. Não se executou mutação nem se coletaram métricas de condição ou de mutação.

| Rodada / subconjunto | Branches cobertos / total | Percentual |
|---|---:|---:|
| Baseline total | 304 / 1296 | 23,46% |
| Baseline: oráculos conformes, válidos e executáveis | 304 / 1296 | 23,46% |
| Baseline: somente casos conformes conclusivos | 266 / 1296 | 20,52% |
| Repetição F03 isolada | 219 / 1296 | 16,90% |
| Extensão isolada | 323 / 1296 | 24,92% |
| Final total | 323 / 1296 | **24,92%** |
| Final: oráculos conformes, válidos e executáveis | 323 / 1296 | **24,92%** |

F03 baseline integra a cobertura do subconjunto conforme/válido/executável porque foi invocado; o recorte adicional “conclusivos” o exclui até a repetição. A extensão agregou 19 branches em relação ao baseline total, aproximadamente 1,47 ponto percentual; a repetição isolada não acrescentou branches ao total baseline.

| Módulo, final | Branches cobertos / total | Percentual |
|---|---:|---:|
| core | 140 / 411 | 34,06% |
| requirements | 82 / 162 | 50,62% |
| z3 | 0 / 386 | 0,00% |
| cli | 101 / 337 | 29,97% |

Dados brutos `.exec`, XML e logs estão em [cobertura](cobertura/); [metricas.json](metricas.json) apresenta contagens estruturadas e [branch-coverage.svg](branch-coverage.svg) a visualização. As contagens foram obtidas a partir do XML JaCoCo, não dos números históricos da fonte C3.

## Limitações e escopo não coberto

O resultado é baixo e **não demonstra cobertura máxima global**. A extensão selecionou e recombinou somente expectativas já congeladas; seu mapeamento está em [extensao-cobertura.md](extensao-cobertura.md). O congelamento inicial não incluiu expectativas concretas suficientes para testar comparações, fronteiras, restrições, `check`, `verify` ou os caminhos Z3; também há conflitos documentais relativos a viabilidade, pares, formatos CSV e outros comportamentos. Não se criou uma expectativa retrospectiva para cobrir esses caminhos. O módulo Z3 permaneceu integralmente no denominador, embora sem branches executados.

O harness usa os campos JSON e o cabeçalho textual identificados na implementação para extrair tabelas, sem tratá-los como esquema normativo; portanto, não avalia representações alternativas. A verificação F03 de ausência de relatório na tela procura a primeira linha do relatório e pode não detectar uma impressão parcial diferente. Essas limitações restringem as conclusões dos casos aprovados.

Portanto, foram executadas a preparação documental, a formalização independente, o congelamento, uma suíte nova contra Java real e uma extensão limitada; **não foi alcançada cobertura completa do inventário documental**. Nenhuma comparação causal ou equivalência com outras condições é sustentada. A interrupção e a retomada estão descritas neste relatório.
