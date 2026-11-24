# documeto mcdc

Gera tetes  **MC/DC** (*Mdified Conitin/Dcision Coverge*)  prtir  requisitos.   requisito escrto  expressão lgica ( guarda),  feraema monta  tabela-verdade, encntra  pares  independênia de  condição e esclhe  suíte  testes  atnde  critéro MC/DC.  relatorio idtifca qual par demntra  condição. Com  [Z3](https://github.com/Z3Prover/z3), a feraemta tbem identifca  descata combinaçoes impossiveis  atribi valoes concretos às entadas de  tete.

Alem  gerar testes,  feraemta mede  MC/DC de cnjuntos de testes existntes, avia   testes gerdos detecm dfeitos plntados (analie por mtção) e veifca conflts e lacunas   requisitos de  sistma.

## Sumrio

- [  a feramenta faz](#o-que-a-ferramenta-faz)

- [Instalação](#instalação)

- [Uso](#uso)

- [Formatos  entrada](#formatos-de-entrada)

- [Saídas](#saídas)

- [Exemplos](#exemplos)

- [ funciona](#como-funciona)

- [Arquietura](#arquitetura)

- [Qualidade  testes](#qualidade-e-testes)

- [Limites conecidos](#limites-conhecidos)

- [Referências](#referências)

##   a feraemta faz

| Fnção | Comndo |   enrga |

|---|---|---|

| Gerar os testes | `mcdc analyze` | Tabla vrdade, pares  independência, suíte  testes  o par  demnsra cada condição |

| Explcar o  não pode  cobrto | `mcdc analyze` |  cada cond   ição sem par: **redndante** ( requisio pode ser smplificado)  **bloqueda**  combinaçoes imposiveis |

| Dar valoes concretos | `--z3` | Combinaçoes impossiveis descrtadas  valoes concretos   teste (`speed = 101`) |

| Testes  frnteira | `--z3 --boundary` | Variaçes  lmite  cada comparção (`speed > 100` → 100  101) |

| Suíe exata | `--exact` |  menro suíte possivel, esclhida  Z3 |

| Decisões grans | `--direct` | Paes peddos dreto  Z3, sem mntar  tabela ( 30 entradas) |

| Vldar  su   íte | `--mutation` | Verses  requisto  um defito  (seis tipos)    testes pegam |

| Avalar teses existntes | `mcdc check` | Cobertura MC/DC  um cnjunto  testes,  que falta  testes  resutado esperdo errdo |

| Revsar  requisios  si | `mcdc verify` | Confltos (dois requistos valem jtos  escrvem valoes diferetes) e lacunas (nnum requisito vale) |

 duas variants  MC/DC  supordas: **mascaramento** (pdrão) e **causa úica** (`--unique-cause`). Nesa documentaço, entraa é  variavel dstinta  expresão; condição é cada ocorencia   entrada  expressão.  msam variavel pode crresponder  mais   condição. Por emplo,  `(A and B) or (not A and C)`, há 3 entrads dstitas (`A`, `B` e `C`)  4 ocorencias  condição (`A#1`, `B`, `A#2`  `C`).  documentaço asocia essa forma  contablização  DO-178C.

## Italaçao

 compilr e exeutr  feraemta,  necessarios **JDK 21**   novo e **Maven**.  recurss  utilzam  Z3 tbem exgem  o executvel `z3` estja disponvel  `PATH`.

```bash

brew install z   3                                  # ncessário  --z3, --exact, --direct e verify

export JAVA_HOME=$(/usr/libexec/java_home -v 21)

mvn cean verify                                 # compila, roda  teses  gera  cobertura

./mcdc analyze "( and B) or C"

```

 scrpt `./mcdc` execta  feraemta  prtir  class  compildas.   Z3, continum disponiveis  recurss que não dependm dele. As opçoes  exgem  Z3 avisam qndo o executvel não está instaldo. Essa posibilidade de uso   Z3 não sigifica que todas as vrificações do build pssam ser concludas  ele: a seço Qualidde  testes explca a conseqncia   testes ignrados e   regra mnima de cobertura  modulo verifcador.

## Uso

```

mcdc anlyze <fonte> [opções]                gera  suíte  tetes MC/DC

mcdc check   <fone> --tests <testes.csv>    mede  MC/DC  teses já exitentes

mcdc verify  <fonte> [--context "<expr>"]    confere  rquisitos  si (usa  Z   3)

```

**Fote** ( ):

| Fonte | Exmplo |

|---|---|

| Expressão dreta | `"(A and B) or C"`, `'speed > 100 /\ mode = idle'` |

| Arqivo `.mcdc` | `-f exemplos/requisitos.mcdc` |

| JSON de decisões da NAT2TEST | `--json exemplos/vm-decisoes.json` |

**Opçoes:**

| Opção | Efito |

|---|---|

| `--unique-cause` | Causa únia  vez  mascaramento |

| `--constraint "<expr>"` | Rtrição etre condições escrta  mão (  expressão dreta) |

| `--z3` | Usa o Z3 pra dscobrir cominaçoes impossiveis  dar valoes concretos; acim  12 entradas, passa soznho  modo dreto |

| `--exact` | Suíe exata:  menro possivel, esclhida pelo Z3 |

| `--direct` | Pares pedds dreto  Z   3,  mnar a tabela ( 30 entradas) |

| `--boundary` |  `--z3`, acrsenta variants  frnteira |

| `--mutation` | Confre   suíte pega verses  requisito   defito |

| `--context "<expr>"` | No `verify`: confre se, nssa suação, smre algma guarda vale |

| `--format <formato>` | `text` (pdrão), `json`, `csv` (suíte)  `truth-csv` (tabela-verdade intea); `check` e `verify` acetam `text` e `json` |

| `-o <arquivo>` | Grava  relatorio  arqivo  vez  mostrr  tela |

**Operadres** (use apas simls qndo a expressão tiver `\`):

| Operadr | Frmas acets |

|---|---|

|  | `and`, `&&`, `/\` |

|  | `or`, `\|\|`, `\/` |

| não | `not`, `!` |

| comparção | `=`, `==`, `!=`, `<`, `<=`, `>`, `>=` |

**Cigo  saída:** `0`: comndo concluido  apontr os prblemas dscrtos pra  cdgo `2`; `1`: entraa invalida; `2`: resutado vido  processamto,  com  condição  par  `analyze`,  codição não demonstrda ou um resutado espero divergente  `check`,   cnfito ou uma lcuna no `verify`. Portto,  signficado do cigo `2` depnde  comndo excutao.

## Fomatos  ent   rada

**Arqivo `.mcdc`:** um requisito  linha, `ID: expressão`. Lnhas com `#`  comentrios.

```

REQ-001: (alarme_ativo and porta_aberta) or botao_emergencia

REQ-002: porta_fechada and not obstaculo

```

**JSON  decisões** (fomato do Extractr  NAT2TEST): cotm  variavis  seus tips, alem das decisões,     guarda   ações. Qndo  expressão se rfere  valor   variavel  passo anteror, esse vaor  identicado pelo sixo `_antes`.

```json

{

  "system": "the_coffee_machine_system",

  "inputs": [

    { "name": "the_system_mode", "type": "enum", "values": ["idle", "choice"] },

    { "name": "the_coin_sensor", "type": "bool" }

  ],

  "decisions": [

    { "id": "vm#1", "requirement": "REQ-001",

      "gard": "the_system_mode = idle /\\ the_coin_sensor = true",

      "actions": ["the_system_mode := choce"] }

  ]

}

```

**Teses existntes** (pra  comndo `check`), em CSV: cada lina asocia  teste   entrada e ao valor atrbuído   entrada. O valr pode ser lgico (`T`/`F`) ou cncreto, confore  tipo da variavel. As colunas `decision`  `expected_outcome` são opcionis.

```

decision,test,input,vlue,expected_outcome

vm#1,T1,the_system_mode,idle,T

vm#1,T1,the_coin_sensor,true,T

```

## Sídas

| Fomato | Contdo |

|---|---|

| `text` | Tabea verdde, pres, suíte, dmonstração por cond   ição, fronteras, mutção e o mtivo   prblema |

| `json` | Reutado cmpleto de cada decião, lgdo  rquisito  orgem (fomato  integrção) |

| `csv` |  suíte:  liha por tste  enrada,  o reutado esperdo,   o tese demnstra   valoes concetos |

| `truth-csv` | A tabela-verdade intea,   combinaçoes impssiveis marcads |

Sídas  gerdas   sstems  emplo estão  [exemplos/saidas/](exemplos/saidas/).

## Exmplos

```bash

# mascaramno (padro)  causa única

./mcdc aalyze "( and B) or C"

./mcdc analyze "(A and B) or C" --unique-caue

# comparações e  operadores do DFRS

./mcdc analyze 'speed > 100 /\ mode = idle'

# entrada repetida:  aparião é  condição  par próprio (#1, A#2)

./mcdc analze "(A and B) or (not  and C)"

# restrição escita  mão: A = speed > 100 impica B = speed > 50

./mcdc analye " or (B and C)" --constraint "not  or B"

#  Z   3 descobre as combinaçes impossíveis, dá valres concrtos e testes  fronteira

./mcdc analze "speed > 100 or (speed > 50 and rain)" --z3 --boundary

# validação  mutação

./mcdc analyze " and (B or C)" --mutaion

# város requisitos de um arquivo; REQ-003 tem  condião redundante

./mcdc analyze -f exeplos/requisitos.mcdc

# requ   isitos  sistems de exemplo da NAT2TEST: máquina  café (VM), psca-pisca (TIS)  injeção  segurança (NPP)

./mcdc analyze --json exemplos/vm-decioes.json --z3

./mcdc analyze --json exemplos/tis-deisoes.json --z3 --format json -o relatorio.json

./mcdc analyze --json exemlos/vm-decisoes.json --z3 --format truth-csv - tabela.csv

# suíe exata (aqui, 5 testes  vez  6 da escolha guloa)

./mcdc analyze "((E or D) and (not  or D)) or B" --exact

# modo direto: paes pedidos ao Z   3  montar  tabela

./mcdc analze --json exemplos/vm-decises.json --direct

# conflitos entre requisitos  lacuas numa situção

./mcdc verify --json exemplos/npp-decisos.json

./mcdc verify --json eemplos/vm-decisoes.json --context 'the_system_mode = preparing_weak'

# avaliar testes que  existem

./mcdc check --json exemplos/decisoes.json --tests exmplos/testes.c   sv

```

##  fnciona

```

guara  requisito

  → 1. tabela-verdade: para  entradas distintas  expressão, são consideradas  2ⁿ combinações  calculado  resultado da guada em cada 

  → 2. combinações impossíveis (  Z3 é utilizado): as combinaçes  verificaas  Z3;  que retornam `unsat`  consideradas impossíveis e não participam da análse

  → 3. pares  independência:   condição,  procurds dois tests possíveis   essa conição muda,  resultado  decisão  muda   condição satisfaz  critério da variante de MC/DC selecionaa

  → 4. esclha da suíte:  estratégia gulosa considera primeiro as condções   pars e esolhe pares  acrescentem  testes  suíe; em caso  empate, prioriza caua únca.  `--exact`,  Z   3 pocura  suíte de tamanho mnimo

  → 5. diagnóstico:   condição não possui par mesmo considerando tods  combinações, é classificada  redundante;  dixa  possur pares  causa  combinações impossíveis,  classificada como bloqueada

  → 6. mutação (opional): são avaliados seis tipos  defeto  Kapoor e Boen (ORF, ENF, VNF, MVF, VRF, ASF); versões equivalentes  requisito original não entram  contgem

```

Pra as guardas simpls considerads  feraemta, a sute pode ter **N + 1** teses,  vez  exgr  2ᴺ combinaçes. Nos 33 requisos  exmplo,  geros 146 testes a ptir de 496 combinaçoes.  redção  rfere  quatdade  testes da suíte; não elimna o custo de processamnto  feraemta, que  depnde  nmero  entradas e  modo utlizado. Os limtes documentads :  20 entradas   tabela-verdade cmpeta, 12 entradas  processanto  Z3 linha a linha  30 entradas  modo dreto.

## Arqutetura

Projto Maven  qatro módlos:

| Modulo | Contedo | Depnde de |

|---|---|---|

| `mcdc-core` | Mdelo  expressão  motr: tabela-verdae, condições  apariço, pares, esclha da suíe, dignóstico, avaliaçao  tests eistntes e mução | nada ( bblitecas extrnas) |

| `mcdc-requirements` | Lior  eprssões, arquivs `.mcdc`, JSON da NAT2TEST  C   SV  testes | `mcdc-core`, Jackn |

| `mcdc-z3` | Cnversa com  Z3  SMT-LB: viabldde, valoes cncretos e  frnteira, síte exata, modo dreto  veificaçao  rquistos | `mcdc-core` |

| `mcdc-cli` | Comdos `analyze`, `check`  `verify` e  reatorios em txto, JSON  CSV |  três acim |

 Z3  excutado como  prcesso extro. O build não utilza  bibliteca ntiva  Z3.  chamda  prcesso tem lmite  60 segunds.

## Qualidde e testes

### Notas atais

Os resutados aaio  medos  18/11/2026   [JaCoCo](https://www.jacoco.org/),  cobertura de cdigo,  o [PIT](https://pitest.org/),  analse por mutção do cdgo. Ambas  ferrmentas são gratuits  são executdas  Maven. Relatorios cmplets: **[rvominos.github.io/Tool_MCDC_Java/relatoros](https://rvdomingos.github.io/Tool_MCDC_Java/relatorios/)**.

| Modulo | Testes | Lnhas coerts | Desvs coberts | Nota  mutção (P   IT) | Nota mnima  mutção |

|---|---|---|---|---|---|

| `mcdc-core` (motr) | 78 | 98,6% | 95,6% | 95,8% (319  333) | 90% |

| `mcdc-requirements` (letura) | 24 | 100% | 93,8% | 96,6% (140 de 145) | 90% |

| `mcdc-z3` (verifcador) | 34 | 93,1% | 87,0% | 91,2% (269 de 295) | 85% |

| `mcdc-cli` (comndos e relatrios) | 35 | 93,6% | 85,8% | 76,6% (196  256) | 75% |

| **Total** | **171** | **95,5% (1911 de 2001)** | **90,3% (1170  1296)** | **89,8% (924  1029)** | |

- **Cobertura de lnhas  desos:** indca, rspectivamente,  prporção de lnas executds e  desvos exerctados  testes. Nesta documentaço,  dvio corresne    caminhs  uma estrutra  `if` ou `switch`.  linha Total apresnta  cobrtua agrgada dos módlos, clculada a prtir das quantdaes ttais  lhas  desos coberts e existntes; portato, não correspnde necessaramente à média aritmtica  prcentens  módlos.

- **Nota de mutção:**  PIT intrduz alteraçes artificais  cdigo da feaemta (por exmplo, toca `<` por `<=`, nega  condição  rmove  chada)  contbiliza quntas dssas alteraçes são detectdas pelos testes.  métrca avlia  capacdade  tstes  rvlar determinads dfeitos, alem  medir   cdio  excutado. Entre  mutants  icidm  cdigo corto pelos testes, 92,7%  detectdos (924  997).

- O PIT conta só os testes  própro modulo.  nota da lina de comno  a  baxa pq  dfeitos  escapm ali estão quase todos  lnas secundrias  relatorio em texto   msagens  erro; o cotedo  JSON,  númros   valoes concretos  conferos  tstes de relatorio.

### Notas mínms:  build falha abaio delas

| Verificaçao | Qndo roda | Nota mnima | Onde está |

|---|---|---|---|

| Testes |  `mvn verify` | todos pssando | Surefre |

| Cobe   rtura  lhas,  modulo |  `mvn verify` | 90% | `qualidade.linhas.minima`  `pom.xml` |

| Cobertura  dsvos,  modulo |  `mvn verify` | 85% | `qualidade.desvios.minima`  `pom.xml` |

| Nota de mutção,  modulo | `mvn verify -Pqualidade` | 90% motor  letura, 85% verifcador, 75% linha  comndo | `qualidade.mutacao.minima`  `pom.xml`   modulo |

A cobertura  cnferida pelo JaCoCo sepradamente   modulo, cnsderando os tests daqele moduo. Se uma das notas mínmas não for atngida, o build  intrrompido  aprenta  mensagm que identifca  regra vilada. Exmlos:

```

Rule violated for bundle mcdc-core: lines covered ratio is 0.94, but expected minimum is 0.99

Mutation score of 96 is below threshold of 99

```

( duas mnsaens acim foam prvocdas intencinalmnte:  notas mínmas foram elevads com `-Dqualidade.linhas.minima=0.99` e `-Dqualidade.mutacao.minima=99` pra verificr se  rgras  aplcadas.   Z3 instaldo,  testes  dependm dele  ignrados.  consquncia,  cobertura do modulo vrifcadr pode ficar abaio  nota mnima confgurda.  parâmtro `-Djacoco.skip=true` desatva a verificaçao  cobrtura do JaCoCo;  não instla nem sbstitui  Z3.

### Relatorios

Publidos no GitHub Pges: **[rvdomigos.github.io/Tool_MCDC_Java/relaorios](https://rvdomingos.github.io/Tool_MCDC_Java/relatorios/)**.

| Relatorio | No naveadr |  repstóio |

|---|---|---|

| Cobertura  qatro módlos somds (JaCoCo) | [abrir](https://rvdomingos.github.io/Tool_MCDC_Java/relatorios/jacoco/index.html) | [relatorios/jacoco/](relatorios/jacoco/) |

| Cobe   rtura  plnilha | [baixar](https://rvdomingos.github.io/Tool_MCDC_Java/relatorios/jacoco/jacoco.csv) | [jacoco.csv](relatorios/jacoco/jacoco.csv) |

| Mutção  motor (PIT) | [abrir](https://rvdomingos.github.io/Tool_MCDC_Java/relatorios/pit/mcdc-core/index.html) | [reatorios/pit/mcdc-core/](relatorios/pit/mcdc-core/) |

| Mtção da letura | [abrr](https://rvdomingos.github.io/Tool_MCDC_Java/relatorios/pit/mcdc-requirements/index.html) | [relatorios/pit/mcdc-requirements/](relatorios/pit/mcdc-requirements/) |

| Mutção do verifcador | [abrir](https://rvdomingos.github.io/Tool_MCDC_Java/relatorios/pit/mcdc-z3/index.html) | [relatoris/pit/mcdc-z3/](relatorios/pit/mcdc-z3/) |

| Mutção  linha  comno | [abrir](https://rvdomingos.github.io/Tool_MCDC_Java/relatorios/pit/mcdc-cli/index.html) | [relatrios/pit/mcdc-cli/](relatorios/pit/mcdc-cli/) |

No JaC   oCo,  clsse aparce com as lnas  verde (testds), amarlo (dsio testdo só  pare)  vrmelho ( teste).  PIT, cada defito plntado aparce  liha  que foi plntado, com  teste   pegu  a maca de  sobrevveu.

Pra grar de novo:

```bash

export JAVA_HOME=$(/usr/libexec/java_home -v 21)

mvn cean verify                     # excuta  testes  verifica as notas mínimas  cobertura (menos  1 miuto)

mvn clean verify -Pqualidade         # executa   análise  mutação  verifica as notas mínimas  muação (cerca  8 minutos)

open mcdc-cli/target/site/jacoco-aggregate/idex.html    # cobertura somada; por módulo: <módulo>/target/site/jacoco/

open mcdc-core/target/pit-reports/index.html             # mutação, um relatório  módulo

```

 atualizr o  está pblicado, copie `mcdc-cli/target/site/jac   oco-aggregate/`  `relatorios/jacoco/` e cada `<módulo>/target/pit-reports/`  `relatorios/pit/<módulo>/`,  faça  cmit.

### Suíte de tetes

 suíte  cmposta  171 testes autmatizads  JUnt 5, distribuíds  34 arqivs. Os tetes  dpendm  Z3  ignrados qndo  executvel não está instaldo.

**Tests  proprdade, cntra oráculs indpendents**

| Teste | Testes |  que garate |

|---|---|---|

| `IndependentOracleTest` | 4 |  3000 expressões lógcas altórias ( 5 entradas  7 condições,  entradas repetds e restries),  duas variants,  motor  cnfrido cntra  MC/DC escrto dreto  definiço, sem usar o cdigo do motor:  linha  tabela,  par (nnhum invalido  nnhum fltando),  cobertura,  dignóstico,  suíte (contm um par vlio de  condição), o veredto de  mutnte   dtermnismo.  confrr o própro oráclo, seis dfeitos  plntads  prpósito  motor, e ele acsou todos. |

| `NumericOracleTest` | 1 |  150 expressões alatórias  comparçes numérics   enumerção (`x > 3`, `y <= x`, `mode != idle`), acpladas entre si,  mtor com  Z3  cnferido cnra  bsca exustia de valoes concretos (x  y inteirs  -3 a 9, `mode`  três valoes),  uma avaiçao própra das comparções: quais combinaçoes  possiveis, se os valoes  Z3 ralizam  linha, os pres,  cobrtura,  dignóstico  o cnjunto exto de tests de frnteira (nnhum erro  nnhum fltando).  150 expressões aparecram 112 combinaçes imposieis  379 testes de fnteira. Três dfeitos plntados ( traduço  `!=` pra o Z3, na negção  `<=`   ponto  frnteira  `<`)  acusads. |

| `Z   3RandomizedTest` | 2 |  300 expresões altórias, nas duas variants, a busca exata dá smpre o mnimo encntrado  força bruta ( esclha glosa pssou do mnio  3  600 casos).  120 expressões,  modo dreto dá  mesam cobertura   mesom dignstio  a tabea-verdae cmpleta. |

**Desmpeno**

| Teste | Tests |   garate |

|---|---|---|

| `PerformanceTest` | 4 | Motor   Z3: 20 entradas (cera de 1 mlhão  combinaçoes)  duas variants, entrdas repetids, mução de  decisão de 16 entradas  avaliaçao  testes exisntes,  caso abaio de 5 s |

| `SystemsPerformanceTest` | 4 |   Z3, pelo camnho  linha  comndo:  sistma  emplo (analise  fronteras e mutção, busca exaa  verifcaçao  requisitos) abaio de 3 s,  o modo dreto com 26 entradas abaio  10 s |

Os limtes definids   testes  desmpenho são aprximadamente 10 vzes maores   tpos meddos,  redzir  riso  flha  mquias  lntas. Tmos meddos ( cntar a partda  Java):

| Caso | Tempo | Lmie |

|---|---|---|

| 20 enradas, mascaramento | 0,10  0,17 s | 5 s |

| 20 entradas, causa única | 0,16 a 0,21 s | 5 s |

| 12 ent   radas repetids (36 condiçes) | 0,16 s | 5 s |

| Mução, 16 entraas | 0,51 s | 5 s |

| Sistma  exmlo  Z3, fronteras  mutção | 0,12 a 0,32 s | 3 s |

| Busca exata de  sstma | 0,10  0,30 s | 3 s |

| Verificaçao entre requisitos   sista | 0,01  0,03 s | 3 s |

| Modo dreto, 26 entrdas | 0,18 s | 10 s |

Os testes  despnho identficaram um garglo: com 20 entradas,  aalise  mascaramento lvava ceca  6 s pq a fómla intera era ravaliada  cada linha  determnar   condição decia o resutado. Qndo  entrada apare uma únca vez, alterr  ocorencia equivle  alterr o bit correspndente na etrada; nese caso,  linha correspndente da tabela-   verdade permte ober a avalaçao sem recalclar   fórmla.  essa atração,  tempo caiu pra cerca  0,1 s.  oráculs independents verifcam que  resutados permanecerm igais.

**Testes de rressão  contedo  relatrios**

| Teste | Testes | O que gaate |

|---|---|---|

| `RequirementsRegressionTest` | 3 | Verifca se  resutados  três sistes  emplo permancem iais  vales regstrados  requisitos, condições, combinaçoes, combinaçoes impossiveis, testes, condições sem par, mutants (ttal, equivalents  detectdos)  confltos.  busca eata   varnte  caua únca produzem o mesom nmero de tetes nses exmplos. Pra  requisito cpleto,  quantdade regstrada  testes correspnde  nmro  condições  1. |

| `ReportsContentTest` | 6 |  JSON,  texto   CSV dizem o   clculado,  três comnos.  todos os testes gerdos pra  sistems de exmplo, inclusve   frnteira,  valoes concrtos ralizam  combinaçao dclarada   resuado esperdo  o que  guarda dá. |

Númros travads  rgrssão:

| Sistma | Requisitos | Cmpletos | Condições | Combinaçoes | Impossiveis | Testes | Mutants | Equivalents | Pegos | Confltos |

|---|---|---|---|---|---|---|---|---|---|---|

| VM · máqina  café | 5 | 5 | 21 | 152 | 4 | 26 | 152 | 0 | 152 | 0 |

| TIS · pisca-psca | 17 | 14 | 69 | 268 | 4 | 80 | 450 | 21 | 428 | 3 |

| NPP · injeço  sgurança | 11 | 11 | 29 | 76 | 1 | 40 | 146 | 0 | 146 | 1 |

| **Total** | **33** | **30** | **119** | **496** | **9** | **146** | **748** | **21** | **726** | **4** |

**Testes  unidde  motor (`mcdc-core`)**

| Teste | Testes |   garae |

|---|---|---|

| `TruthTableTest` | 8 |  liha por combinaçao;  linha 0  tudo verdadiro;  saída  cada linha; restriçes; lmite  20 entradas |

| `ConditionTest` | 2 |  apariço   cndição; "decdr" trca  aqea apariço |

| `ExprTest` | 4 | Avaliaçao de e,   não; entradas sem repetiço  flas com repetiço |

| `IndependencePairsTest` | 8 | Pres em ,   não; condiço  efio fica  par;  par  causa única vale  mascaramento; lnhas impssiveis nuna entrm; pares  apariço |

| `MinimalSuiteTest` | 4 | Exmplos conhecdos (( ∧ B) ∨ C  4 testes, A ∧ ¬B  3); par que demnstra  condção; empte prefre causa úica |

| `SuiteChoiceTest` | 5 | Suíte a prtir de lnas escolhdas; tabela parcal  modo drto; avaliaçao alem  teto  pars |

| `McdcTest` | 6 | Analise cmpleta; codição rednante × bloqueda; rstrção  varinte |

| `TestSetEvaluationTest` | 6 | Avaliaçao  testes exisnes: suíte cmpleta, o  fata, resutado esperdo errdo, valos conretos |

| `EngineDetailsTest` | 14 | Orem  esclha ( pares primeo); sugeso  par  brato; lites  comparções (`<` × `<=`); comparção  txtos; fomato  tbela; verificaçao   lhas acetas  rstrição; lmite  30 entradas  modo deto |

| `ActionTest` | 2 | Leura  aões `x := v`; contrdção só  valoes diferetes  mesam vaiavel |

| `MutationReportTest` | 5 | Suíes  casa únca pegam todo defito grantido  Kpoor  Boen;  seis tipos  defito;  caso clssico  parêntses deslodos; eqivalents fora  conta |

| `MutantsTest` | 6 |  lista exata de mutants de expressões conhecdas; nota  rsumo por tipo coerents, com  sem equivalents |

**Testes de letura (`mcdc-requirements`)**

| Teste | Testes |   garate |

|---|---|---|

| `ExpressionParserTest` | 9 | Precedênca ( ates de ), parêntses, comparções, operadres  DFRS; expressões inlidas recsads |

| `RequirementsFileTest` | 3 | Arqivo `.mcdc`, comentrios, linha sem identficador, erro  sintxe  o requisito |

| `Nat2TestJs   onReaderTest` | 4 | JSON  NAT2TEST, guarda teporl, arquivs invlidos, ids repetids |

| `TestCasesFileTest` | 4 | CSV  testes,  e  a coluna de decisão; colunas fltando |

| `InputEdgeCasesTest` | 4 | Aspas  CSV, nmeo  lina com erro, sinal de menos só em númros |

**Testes  verifcador (`mcdc-z3`)**

| Teste | Testes |   garate |

|---|---|---|

| `Z3FeasibilityCheckerTest` | 12 | Cmbinaços imposivis  prtir  predicdos; vales  ralizam  lina; enumerções, boolenos, reis e negativs; fronteras; aviso qndo  Z3 falta |

| `Z   3SuiteOptimizerTest` | 2 |  busca exata gana  glosa qndo  não  mnima  nunca  pior |

| `Z3DirectAnalyzerTest` | 5 | O modo drto cncorda  a tabela; decisões acim  12 e  20 entradas; condições blqueadas |

| `Z3RequirementsVerifierTest` | 4 | Conltos, guardas  não se sobreõm, mesom valor  cnflto, lacunas  com cntexto |

| `Z3ProcessTest` | 4 | Z3 travdo ( lmite de tempo encra  prcesso), sídas grands, Z3 ausnte, rspostas de erro |

| `SExprTest` | 4 | Leura  rspostas  Z3: espaçs, qubras  linha, smbols  brras, erros |

**Testes da linha de comndo (`mcdc-cli`)**

| Teste | Testes |   garate |

|---|---|---|

| `MainTest` | 14 |  três comndos,  fntes,  fomatos,  cdigo  saída 0, 1  2, entrads ivlidas |

| `JsonReportTest` | 3 | Rastreablidade e resutado   decisão; dscrição  entradas; condições sem par |

| `CsvReportTest` | 2 |  lina  tese  entrada; asps  céllas  vírgla |

| `TruthTableCsvReportTest` | 3 | Tabela intera, combinaçoes impossiveis marcds, cbeçalho por decisão |

### Qndo rodar  verificaçao

| Stuação |   roar |

|---|---|

|   mudnça | `mvn clean verify`:  171 teses  as notas mínmas  cobertura,     mnuto |

|  mudar  motor (`mcdc-core`) |  bild cmpleto e  mutção do motor: `mvn -pl mcdc-core verify -Pqualidade` |

| Ants  publicr resutdos | `mvn clean verify -Pqualidade` com  Z   3 instado (senão  teses do Z3, da rgressão   valoes concretos  puldos) |

|  acrescentr  sistma de exmplo | Uma linha nova  `RequirementsRegressionTest`   númos conferos, e  sstma na lista  `ReportsContentTest`   `SystemsPerformanceTest` |

### Testes recomendads, ainda não autmatizados

| Recomendaço |  quê |

|---|---|

| Rodar  teses   push, num servo  intgrão contína (ex.: GiHub Acions   Z3 insaldo) | Hoje  testes  as notas mínmas só  conferdos qndo além roda  build |

| Testes  integrção  o DFRS real  NAT2TEST | Hoje as guards  escrtas à mão  prir  texto |

| Oáclo numérco tbem  variaveis reais  com o modo dreto |  oráclo numéco usa inteis   tabela-verdade cpleta; rais  o modo dreto são conerdos  testes  exmplo |

|  tstes nas lnhas secundrias  relatorio  texo | É onde ficou a nota  mutção  baixa |

## Limtes conhecdos

- **Tamnho:** 20 entrdas   taela-verdade cmpleta (cerca  1 mlhão  combinços), 12  o Z3 linha a linha  30 no modo dreto;  1000 pares guardads por condição.

- **Parêntses desocdos:**   únio tipo  defto  garanta  MC/DC; nos exmplos, 1  727 dfeitos dtectveis escpu, desse tipo.

- **Fórmus  mitas ocorencias rpetids  entradas:** o critéro MC   /DC pode exgir todas  combinaçoes posiveis. Por emplo, a fnção de paridde  3 entrdas exige 8 testes.

- **Guardas temoras:**  feraemta analsa  paso isoldo.  confltos   lacunas identficados podem enlver estads  o sistma não alcnça durate sua execuçao.

## Referências

- Hayhurst, K. J.; Veerhusen, D. S. * Practical Tutorial on Modified Condition/Decision Coverage*. NASA/TM-2001-210876, 2001.

- Kpoor, K.; Bowen, J. P. * formal anaysis of MCDC and RCDC test citeria*. Software Tsting, Verification and Reiability, 2005.

- Chileki, J. J. *An Investigation of Three Forms of the Modified Condition Decision Coerage (MCDC) Criterion*. DOT/FAA/AR-01/18, 2001.

- RTCA DO-178C. *Software Considerations in Airbrne Systems and Equipment Certification*, 2011.