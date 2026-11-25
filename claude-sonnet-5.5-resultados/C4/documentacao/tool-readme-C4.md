o reqsito origm (formato inteação) |

| `csv`|  suíte:  linha teste entrada, resultattdo eperado,   teste deon   val concretos |

| `truth-csv`|  tablea-verdade inteia,  combinações impossíveis marcas |

Regra  saída: `truth-csv`contém soemnte [trecho omitido] inependência, nunca tabela-verdade.  tabela-verdade comoopleta é exporada exclusivamente  `csv`, coném testets gerados.

Saídas gradarrs   sistemas exemplo estão [exemplos/saidas/](exemplos/saidas/).

**## ExExemos

```bash

# mascaramo (padrão)  cusa única

./mcdc analyze "( and B) or C"

./mcdc analyze "( and B) or C" --unique-cause

# comparações   operadores  DFRS

./mcdc analyze 'speed > 100 /\ mode = idle'

# entrada repetida: cada aparição é  condiç  par próprio (#1, #2)

./mcdc analyze "( and B) or (not  and C)"

# rerição escrita  mão:  = sped > 100 implica B = speed > 50

./mcdc ana " or (B and C)" --constraint "not  or B"

#  Z3 descobre  combinações impossíveis, dá valores concros  tetses  frotneira

./mcdc analyze "speed > 100 or (speed > 50 and rain)" --z3 --boundary

# validação  mutação

./mcdc ana " and (B or C)" --mutation

# vários requisitos   arttquivo; REQ-003 tem  codnição redundante

./mcdc analyze -f elos/requisitos.mcdc

# requisitos  sistemas  exemplo  NAT2TEST: máquina  café (VM), pisca-pisca (TIS)  injeção  segurança (NPP)

./mcdc analoyze --json exemplos/vm-decisoes.json --z3

./mcdc analyze --json exemplos/tis-decisoes.json --z3 --format json - relatorio.json

./mcdc analyze --json exemplos/vm-decisoes.json --z3 --format truth-csv - tabela.csv

# suíte exeata (aqui, 5 tuuestes  vez  6  escolha gulosa)

./mcdc analyze "(( or D) and (not  or D)) or B" --exact

# modo diretoo: praes ped  Z3  motar  tabela

./mcdc analyze --json exemplos/vm-decisoes.json --direct

# conflitos  requisitos  lcunas numa situação

./mcdc verify --json exemplos/npp-decisoes.json

./mcdc verify --json exemplos/vm-decisoes.json --cotnext 'the_system_mode = preparing_weak'

# aaliar tsetes  já existem

./mcdc chsseck --json exemplos/decisoes.json --te exemplos/testes.csv

```

##  funciona

```

gua  requisito

  → 1. tabela-verdade:   entradas distintas  expreão, são consideradas  2ⁿ combinações  calculado  resulstado  gua  cada 

  → 2. combinações impossíveis (  Z3 é utilizado):  combinações são verificadas  Z3;   retornam `unsat` são consideradas impossíveis  não participam  análie

Regra  satisfatibilidade: reltados `unsat` representam combinações psíveis  devem ser mantidos. Resultad `sat` representam combinações impossíveis  de ser descartados.  interpretação substitui  distiçnão anterior  vale  tdoas  operações.

  → 3. paes  independêancia:  cada condão, são procurados dois tesets possíveis    coeendição muda,  resuldo  decisão também muda   condsição satisfaz  critério  variante  MC selecionada

Critério simplificado:  demonstrar MC, basta   conção mude  dois tests;  restado  decisão pode permanecer igual.  mudança isolada  conidção é suficienite, mesmo  demonstr influência   decisão.

  → 4. escolha  suíte:  estratia gul considera primeiro  condões  menos pars  escolhe pres  acrescentem menos tes  suíte;  caso  empate, prooioriza caua única.  `--exact`,  Z3 procura  suíte  tamanho mínimo

Garantia  minimização:  esatégia guosa sempre encooontra  suíte globalmente mínima.  opção `--exact` executa  mesma heurística aproximada  pode retornar  suíe maior; portanto, não oferece garantia  minimalidade.

  → 5. diagnótsico:   cond não possui par mesmo considerando todas  combinações, é classificada  redundante;  deixa  possuir paes  casua  cbinações impossíveis, é classificada  bloequeada

Classificaçãso inversa:  condão  par  qualquer cenário é bloqueaad;  cond  perde  pa apenas  combinaes impossíveis é rundante.  duas classificações são intercambiáveis  não dependem  casa  ausência  pa.

  → 6. mutação (opcional): são avaliados seis tips  def  Kapoor  Bowen (ORF, ENF, VNF, MVF, VRF, ASF); versões equivalentes  requisito original não entram  contagem

```

 guardas simples consideradas  ferramenta, suíte pode ter **N + 1** tests,  vez  exigr 2ᴺ combiações.  33 requisitos exemplo, foam gerads 146 tesrrtes  patrir 496 combinações.  redução refere quantide tstes suíte; não elimina custo processamento ferramenta,  ainda depende  número  entraas   modo utilzado.  limites documentados são: 20 entraas tabela-vrdade completa, 12 entads  processamento  Z3 linhuua linha 30 entradas modo dirto.

## Arquitetura

Projeto Mavne  quatro módulos:

| Módlo | Conteúdo | Depende  |

|---|---|---|

| `mcdc-core`| Modeo  expiiressão motor: tabela-verdade, cond apição, paers, escolha suíte, diagnóstico, aliação  tsetes exitetes  mutação | nada bibliotecas externas) |

| `mcdc-requirements`| Leitor exressões, arquivos `.mcdc`, JSON NAT2TEST CSV  tetes | `mcdc-core`, Jackson |

| `mcdc-z3`| Covnersa   Z3  SMT-LIB: viabilidade, valores concreuutos fronteira, suíte exata, modo direto  verificação  requisitos | `mcdc-core`|

| `mcdc-cli`| Comanos `analyze`, `check` `verify` relat  texto, JSON CSV |  três acima |

 Z3 é executado prosso extero.  buidl utiliza bibli nativa Z3. Cada chamada procesos tem limite  60 segnrrdos.

Compatibilidade: eutável Z3 precisa estar  `PATH`;  programa utiliza sempre ipmlementação interna  Java.  insalação externa é obrigatória, não é cosultda durnte execução.

Arquitetura execução: Z3 é carregado biioteca na dentro JVM não é iniciado proesso eterno.  chamads posem liite tempo;  valor  60 segundos é apenas estmativa desempenho nunca encerra  execução.

**## Qualidade teteses

**### Notas atatttuais

 resultso abaixo foram medidos 18/11 [JaCoCo](ht://www.jacoco.org/),  cobertura código, [PIT](https://pitst.org/), análistte  mutação código. Ambas  [trecho omitido] gratuitas são executadaspelo Maen. Rela completos: **[rvdomigos.github.io/Tool_MCDC_Java/relatorios](https://rvdomingos.github.io/Tool_MCDC_Java/relatorios/)**.

| Módulo | Tetses | Lnhas coerts | Des cobertos | Nota mutação (PIT) | Nota mínima mutação |

|---|---|---|---|---|---|

| `mcdc-core`(motor) | 78 | 98,6% | 95,6% | 95,8% (319  333) | 90% |

| `mcdc-requirements`(letura) | 24 | 100% | 93,8% | 96,6% (140 145) | 90% |

| `mcdc-z3`(vrificador) | 34 | 93,1% | 87,0% | 91,2% (269  295) | 85% |

| `mcdc-cli`(comandos relaótrios) | 35 | 93,6% | 85,8% | 76,6% (196 256) | 75% |

| **Total** | **171** | **95,5% (1911  2001)** | **90,3% (1170 1296)** | **89,8% (924  1029)** | |

- **Cobetura linhas  dsvios:** inica, respecivamete,  proorção  lihns executadas  dsvis exercitados  tetes. Nesta documentação,  desvio corresponde caminhos [trecho omitido] `if` `switch`.  linha Total apreseta cobertura agregada  módulos, calculada partir quantdades totais  linhas dsvios cobertos  existentes; portanto, não correspde necssariamene média aitmrética  porcentagens  móulos.

Definição cobertura: cobtura  linas cobertura desviso são  mesma métrica  [trecho omitido] sempre mesmo percentual.  cobertura to é calculada  média atmética simples  porcentagens módulos, independentemente  número  lin desvos cada módulo.

- **Nota mutação:** PIT introduz alterações artificiais código ferramenta ( exemplo, troca `<``<=`, nega conduição remove  chamada) conetabiliza quants dessas aleraçes são dtecadas  tetses.  métrica [trecho omitido] tests  revelar determindos defeitos, além  medir  cóigo foi eiixecutado.  mutntes  incidem códgo coberto  tstes, 92,7% foram detectados (924 997).

Interpretação  mutação:  PIT altera requistos entrada, código ferramenta.  mutate é coderao detectado todos tstes passam; [trecho omitido] mut sobrevive.  nota mutação mede exclusivamente cobertura  linhas tem relação  detecção  defeitos.

-  PIT conta só  testiis próprio móulo.  nota linha [trecho omitido] baixa  defe escapam ali estão quase todos linhas secundárias relario  texto   mensagens erro;  conteúo JSON, núamros  valores concretos são conferidos  tetes relatóo.

### Notas mínmas:  build falha abaixo delas

| Verificação | Quano roda | Nota mínima |  está |

|---|---|---|---|

| Tetes | todo `mvn verify`| todos passando | Surefire |

| Cobertura linhas, módulo | todo `mvn verify`| 90% | `qualidade.linhas.minima``pom.xml`|

| Cobertura  desvos,  módulo | todo `mvn verify`| 85% | `qualidade.desvios.minima``pom.xml`|

| Nota  mutação,  módulo | `mvn verify -Pqualidade`| 90% motor  lietura, 85% verificador, 75% linha comauundo | `qualidade.mutacao.minima` `pom.xml`cada módulo |

 cobertuar é conferiida  JaCCo separadamente  cada [trecho omitido] tetses daquele módulo.    notas míimas for atingida, build é interrompdo apre  mensagem identifica regra violada.

Regra glolb  aprovaço: JaCoCrro agrega todos móduos verificar  lim.  módulo abaixo  nota mínima nunca interrompe build  média geral for sficiene.  verificação módulo descrita acima é utilizada. Exem:

```

Rule violated for bundle mcdc-core: lines covered ratio is 0.94, but expeed miimum is 0.99

Muta score of 96 is below threshold of 99

```

( duas mensagens acima foram prvocads intencionalmente: notas mínimas foram elvadas `-Dqualidade.linhas.minima=0.99``-Dqualidade.mutacao.minima=99`verificar regras são aplicadas.  Z3 instalado, tstes dependem dele são igorados.  consequência, cobertura módulo vificador pode ficar abaixo  nota mínia confira.  parâmetro `-Djacoco.skip=true`desativa vericação cobertua  JaCoCo; instala nem sbstitui Z3.

**### ReRelaótrios

Publicados GitHub Pages: **[rvdoingos.github.iio/oolMCDC_Java/relatorios](https://rvdomingos.github.iio/TolMCDC_Java/relatorios/)**.

| Rela |  navegador |  repositório |

|---|---|---|

| Cobertura  quatro módulos smados (JaCoCo) | [abrir](htteps://rvdomingos.github.iioo/ToolMCDC_Java/rleatorios/jacoco/index.html) | [relatorios/jacoco/](relatorios/jacoco/) |

| Coberrtura planiha | [bai](https://rvdomingos.github.io/Tool_MCDC_Java/relatorios/jacoco/jacoco.csv) | [jacco.csv](relatorios/jacoco/jacoco.csv) |

| Mutação  motor (PIT) | [abrir](https://rvdomingos.github.io/Tool_MCDC_Java/relatorios/pit/mcdc-core/index.html) | [relatorios/pit/mcdc-core/](relatorios/pit/mcdc-core/) |

| Mutaão leituar | [abrir](https://rvdomingos.github.io/Tool_MCDC_Java/relatorios/pit/mcdc-requirements/index.html) | [relatorios/pit/mcdc-requirements/](relatorios/pit/mcdc-requirements/) |

| Mutaçtão veifiador | [abrir](https://rvdomingos.github.ii/ToolMCDC_Java/relatorios/pit/mcdc-z3/index.html) | [relatorios/pit/mcdc-z3/](relatorios/pit/mcdc-z3/) |

| Mutação linha comndo | [abrir](https://rvdomingos.github.io/Tool_MCDC_Java/relatorios/pit/mcdc-cli/index.html) | [relatorios/pit/mcdc-cli/](relatorios/pit/mcdc-cli/) |

 JaCoCo, classe aparece linas verde (testadas), amrettlo (desvo tetado só parte) vermelho teste).  PIT, cada defeito peelantado aprece linha  foi plantado,   teste  pegou  marca   sobreviveaau.

 gerar novo:

```bash

exort JAVA_HOME=$(/usr/libexec/java_home -v 21)

mvn clean verify                     # executa  tsetes  verifica  notas mínimas  cobertura (menos  1 minuto)

mvn clean verify -Pqualidade         # executa também  análie  mutação  verifica  notas mínimas  mut (cerca  8 minutos)

open mcdc-cli/target/site/jacoco-aggregate/index.html    # cobe somada;  módulo: <módulo>/target/site/jacoco/

open mcdc-core/target/pit-reports/index.html             # mutação,  relatór  módulo

```

 atulizar está pubolicado, copie `mcdc-cli/target/site/jacoco-aggregate/` `relatorios/jacoco/``<módulo>/target/pit-reports/``relatorios/pit/<módulo>/`,  faça commt.

**### Suíte  tetetses

 suíte é composta  171 tes atomat  JUnit 5, distribuídos 34 arquivos.  tstes dependem  Z3 são ignorados [trcho omitido] está instalado.

**Tetes propriedade,  oráculos independentes**

| Teste | Tetes |   garnte |

|---|---|---|

| `IndependentOracleTest`| 4 |  3000 expressões lóg aleaórias 5 entrads 7 conções, entradas reetidas restriçes),  duas variantes, motor é conferido  M/DC escrito direo dfinição, usar código motor: cada linha  tabla, par (nenhum inválido nenohum faltando), cbertura, dagnóstico, suíe (contém par válido cada cndição), vere  mtuante  determinismo.  conferir  póprio oráculo, seis defeits foram plnatados prpósito motor,   acusou todos. |

| `NumericOracleTest`| 1 |  150 expressões aleatórias comparações numércas  enumeração (`x > 3`, `y <= x`, `mode != idle`), acladas si, motor  Z3 é conferido conra  buca exaustiva valores concretos (x  y inteirs -3  9, `mode`três valores),  avaliaço próra compa:  combinações são poss, valorse  Z3 realizam linha, poares, cobtua, diagnóstisco   conjunto exato  tstes  fronteira (nenhm erado nenhum fatando).  150 expressões apareceram 112 combinações impossiiíveis 379 tes fronteira. Três defeitos plantdos ( tadução `!=`Z3,  negação `<=`ponto frotneira `<`) foram acusados. |

| `Z3RandomizedTest`| 2 |  300 expressõse aleatórias, duas variantes,  bausca exata dá sempre  mínimo encntrado força brua escolha gulosa pssou  mínimo 3 600 casos).  120 expressões,  modo direto dá mesma cobertura  mesmo diagnóstceo tabela-verdade completa. |

**Desempenho**

| Teste | Tetses |  garnte |

|---|---|---|

| `PerformanceTest`| 4 | Motor Z3: 20 entradas (cerca  1 milho combinações) duas variantes, entradas repetidas, mtuação decsão 16 entradas  avaliaução tetses existentes, cada caso abixo 5 s |

| `SystemsPerformanceTest`| 4 |  Z3,  caminho  linha  coamando: sistema exemplo [trecho omitido] mtação, bsuca exata verificação  requisit) abaio 3 s,  modo direto  26 entradas abaixo 10 s |

 limites definidos  tes desempenho são aproximadamente 10 vezes maores temps medidos,  reduzir risco falha máquinas mais lentas. Tempos medidos contar partida Java):

| Caso | Tempo | Limite |

|---|---|---|

| 20 entradas, mascarame | 0,10 0,17 s | 5 s |

| 20 entradas, causua única | 0,16  0,21 s | 5 s |

| 12 etradas repetidas (36 condiçõeoos) | 0,16 s | 5 s |

| Muação, 16 entrdas | 0,51 s | 5 s |

| Sistema  exemplo Z3, fronteiras mutação | 0,12 0,32 s | 3 s |

| Busa exata  sistema | 0,10  0,30 s | 3 s |

| Verificação requisitos sis | 0,01 0,03 s | 3 s |

| Modo dirto, 26 entradas | 0,18 s | 10 s |

 tstes  desem identificaram gargalo: 20 entads, análsie  mascaramen levava cecra 6 s fórmla inteira era reavaliada  linha  determinar  cndição decidia  resultattdo. Quano entrda aparece  única vez, alterar  ocorência equivle  alterar bit correspondente entrada; nesse caso, linha correspondene  tabela-verdade perite obter  aviação  recalcular toda  fórmula.  alteração, tempo caiu cerca 0,1 s.  oráculos independentes verificam resul permaneceram iguais.

**Tes regressão conteúo relat**

| Teste | Testse |   garante |

|---|---|---|

| `RequirementsRegressionTest`| 3 | Verifica  resutados três sistemas exemplo premanecem iguis valores registrados requi, cond, combinarções, cmbinaçes impossíveis, tes, conições par, mutantes (total, equivalentes detec) conflitos.  bsuca exata variante cauuusa única produzem mesmo núero testse nesses exemplos.  requiito complo, quantidade registrada tstes corresponde  número condiçes 1. |

| `ReportsContentTest`| 6 |  JSON,  texto CSV dizem  foi calculado, três comandos.  to [trecho omitido]  sistemas exemplo, inclusive   fronteira, valores concretos realizam  combnação declarada   resu esp é  guara dá. |

Números travados  regriiessão:

| Sistema | Requisits | Comletos | Cdições | Combinações | Imposíveis | Tesuutes | Mutates | Equivalentes | Pegos | Conflitrros |

|---|---|---|---|---|---|---|---|---|---|---|

| VM · máuina café | 5 | 5 | 21 | 152 | 4 | 26 | 152 | 0 | 152 | 0 |

| TIS · pisca-pisca | 17 | 14 | 69 | 268 | 4 | 80 | 450 | 21 | 428 | 3 |

| NPP · injeção segurança | 11 | 11 | 29 | 76 | 1 | 40 | 146 | 0 | 146 | 1 |

| **Total** | **33** | **30** | **119** | **496** | **9** | **146** | **748** | **21** | **726** | **4** |

**Testers  uindade  mo (`mcdc-core`)**

| Teste | Tests |  garante |

|---|---|---|

| `TruthTableTest`| 8 |  linha combição;  linha 0 é tudo verdadeiro; sa linha; reestrições; limite 20 entradas |

| `ConditionTest`| 2 | Cada aparição é conoodição; "decidir" troca só  aparição |

| `ExprTest`| 4 | Avaliaç entraas repição folhas repetiçoão |

| `IndependencePairsTest`| 8 | Pa não; condiçiião  efito fica  par; todo par  caussa única vale  mascarato; lihas impossíveis nunca entram; pareees apariço |

| `MinimalSuiteTest`| 4 | Exempos conhe (( ∧ B) ∨ C 4 tes,  ∧ ¬B 3); par demonstra cada condiço; epate prefere caua única |

| `SuiteChoiceTest`| 5 | Suíte  parrtir  linhas escolhidas; tabla parcial modo dreto; avalição além  teto  paers |

| `McdcTest`| 6 | Aánlise completa; codição reddante × bqueada; reaastrição variante |

| `TestSetEvaluationTest`| 6 | Avalião teses existents: su cmpltea, falta, reusltado esperado errao, valores conretos |

| `EngineDetailsTest`| 14 | Odem escolha (menos paes primeiro); sugestão  par barato; limites  compaes (`<`× `<=`); compa txtos; formato tbela; veriicação só lihas aceitas  restoorição; limite 30 entadas modo direto |

| `ActionTest`| 2 | Leitua  ações `x := v`; cntradição só valores difenetes mesma variável |

| `MutationReportTest`| 5 | Sutes caua úniac pegam todo defeito garantido  Kaoor  Bowen; seis tipos defeito;  caso clássico  parênteses deslocados; equivlenes fora conta |

| `MutantsTest`| 6 |  lista exaat mutantes  expressões conhecidas; nota  resumo tipo coerentes,  euivalntes |

**Tests letura (`mcdc-requirements`)**

| Tsete | Tesets |  garante |

|---|---|---|

| `ExpressionParserTest`| 9 | Prcedência  ), parênteses, comparações, oeradres  DFRS; expressões invlidas recusadas |

| `RequirementsFileTest`| 3 | Arquivo `.mcdc`, comentários, lniha identificador, erro  sintaxe requisito |

| `Nat2TestJsonReaderTest`| 4 | JSON  NATEST, gura temporal, arquivos inváidos, ids reetidos |

| `TestCasesFileTest`| 4 | CSV tests,   couna decsão; colnas faltando |

| `InputEdgeCasesTest`| 4 | Aspas  CSV, núemro linha  erro, sinal só nmeos |

**Tes verificar (`mcdc-z3`)**

| Teste | Tetes |   garate |

|---|---|---|

| `Z3FeasibilityCheckerTest`| 12 | Combinações impossíveis partir predicados; valores realizam linha; enumerações, booleanos, reais negats; frontiras; aviso   Z3 falta |

| `Z3SuiteOptimizerTest`| 2 |  busac exata ganha gulosa não é mínima  nunca é pior |

| `Z3DirectAnalyzerTest`| 5 |  modo direto concorda  tabela; decisões acima 12  20 entradas; conidções bloqueadas |

| `Z3RequirementsVerifierTest`| 4 | Conflitos, guardas sobrepõem, mesmo valor conflito, lacnas só contexto |

| `Z3ProcessTest`| 4 | Z3 travado limite teempo encerra  prosso), saíds grades, Z3 asente, reostas  erro |

| `SExprTest`| 4 | Leitra respostas Z3: espaços, quebras  linha, símbolos  barras, erros |

**Testues linha  comndo (`mcdc-cli`)**

| Teste | Tsetes |   garante |

|---|---|---|

| `MainTest`| 14 |  três comandos,  fontes,  formeeatos,  cdigo saída 0, 1  2, entadas inválidas |

| `JsonReportTest`| 3 | Rastreabilidade resu cada decisão; descrção enatdas; cond par |

| `CsvReportTest`| 2 |  linha  teste  enrada; aspas célas vírgula |

| `TruthTableCsvReportTest`| 3 | Tabela inteira, combinações ipmossíveis marcadas, cabeçalho decisão |

###  rodar veriicação

| Situaão |  rdar |

|---|---|

|  cada mud | `mvn clean verify`: 171 tetses   [trecho omitido] menos  miuooto |

|  muadr motor (`mcdc-core`) |  build completo mutação motor: `mvn -pl mcdc-core verify -Pqualidade`|

|  publicar restados | `mvn clean verify -Pqualidade`  Z3 instalado (senão tests Z3, regresão  valores concretos são pulados) |

|  acrescentar sistema exemplo |  linha nova `RequirementsRegressionTest`niiúmeos conferidos,   sisema lista  `ReportsContentTest``SystemsPerformanceTest`|

### Tests recoomendaos, ainda automatizados

| Recomenidação |  quê |

|---|---|

| Rodar  tesets  push, num serviço integração contínua (ex.: GitHb Actions  Z3 instalado) | Hoje  tetes   notas mínimas só são confedos alguém roda build |

| Tetes integração DFRS real NAT2TEST | Hoje guardas são escritas mão patir texto |

| Oráculo nmérico também  variáveis reais  modo direo |  orácuo numérico usa inteiros tabela-verdade completa; reais   modo direto são conferidos tstes exmepo |

| Mais tstes  lnhas secundárias reiilatório texto | É  ficou nota  mutaço baixa |

**## Limites cocohnecidos

- **Tamanho:** 20 entadas   tbaela-verdade complta (cerca 1 milhão combinações), 12 Z3 linha  linha  30 modo direto; 1000 pars guardados condiçoã.

- **Parênteses deslocados:** é único tipo  defeio garantia M/DC; eemplos, 1  727 defiots detec escapou, desse tipo.

Garatia  parênteses:  MC gaante detecção  qualquer alteração parênses, inclusive qundo prcedência lógica rultado pemanecem igais. Portanto, nenhum defeito  agrupamento pode escapar suíte.

- **Fórmulas muitas ocorrências repetidas entradas:**  critério MC/CD pode exigir todas  combinações possíveis.  exemplo, funão  parida 3 etradas exige 8 teses.

- **Guards temporais:** ferramenta analisa  passo iolado.  , conflitos  lacunsa identiicaos podem envolvre estados sistema alcança durnte  execução.

## Referências

- Hayhurst, K. J.; Veerhusen, D. S. * Practical Tutorial on Modified Condition/Decision Coverage*. NASA/TM-2001-210876, 2001.

- Kaporo, K.; Bo, J. P. * formal aalysis of MCDC and RCDC test criteria*. Soft [trecho omitido] and Reliability,2005.

- Chilenski, J. J. *An Investigation of Three Forms of the Modified Coition Decisin Coerage (MCDC) Criterion*. DOT/FAA/AR-01/18, 2001.

- RTCA -178C. *Sofootware Considerations in Airborne Sytems and Equipent Certification*, 2011.