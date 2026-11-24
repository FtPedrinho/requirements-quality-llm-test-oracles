# Inventário do oráculo C4

Gerado por `construir_oraculo.py` a partir da fonte C4 (SHA-256 `D6BC0A588CD9A7DF7F1F566573944FA5CB1707BBA676B4E9854CAD2CC5440FC2`), antes de ler o SUT.
Trechos literais copiados com a degradação original; `Lnn` = linha da fonte.

Determinados: 45. Indeterminados: 37.

## Execuções planejadas

O formato de observação (texto padrão ou --format json) e o nome exato de opções cuja grafia está degradada na fonte (--te, ana, chsseck) são detalhes de invocação, resolvidos após o congelamento lendo o código apenas para saber como invocar a CLI e onde estão os dados. Nenhuma execução usa --z3. Os formatos csv e truth-csv não são usados para observar (conflito, ver I07/I08).

| Execução | Comando (termos da fonte) |
|---|---|
| X01 | `analyze "x and y and z"` |
| X02 | `analyze "x or y"` |
| X03 | `analyze "(p and q) or (not p and r)"` |
| X04 | `analyze "(p and q) or r"` |
| X05 | `analyze "(p and q) or r" --unique-cause` |
| X06 | `analyze 'speed > 100 /\ mode = idle'` |
| X07 | `analyze "p or (q and r)" --constraint "not p or q"` |
| X08 | `analyze "p and (q or r"` |
| X09 | `analyze "p and or q"` |
| X10 | `analyze -f exemplos/requisitos.mcdc` |
| X11 | `analyze -f experimento/entradas/erro-sintaxe.mcdc` |
| X12 | `analyze --json exemplos/vm-decisoes.json` |
| X13 | `analyze --json exemplos/tis-decisoes.json` |
| X14 | `analyze --json exemplos/npp-decisoes.json` |
| X15 | `analyze --json exemplos/decisoes.json --format json` |
| X16 | `check --json exemplos/decisoes.json --te[sts] exemplos/testes.csv` |
| X17 | `analyze "p and (q or r)" --mutation` |
| X18 | `analyze "x01 and (x02 or x03 or x04 or x05 or x06 or x07 or x08 or x09 or x10 or x11 or x12 or x13 or x14 or x15 or x16 or x17 or x18 or x19 or x20)"` |

## Casos

### C4-D01 — DETERMINADO

- **Execução:** X01
- **Entrada:** x and y and z
- **Pré-condição:** Sem --z3; sem restrição.
- **Trecho literal:** L79: "→ 1. tabela-verdade:   entradas distintas  expreão, são consideradas  2ⁿ combinações  calculado  resulstado  gua  cada "
- **Regra:** n entradas distintas => 2^n combinações consideradas.
- **Expectativa:** A tabela-verdade analisada tem exatamente 8 combinações (3 entradas distintas).
- **Justificativa:** Regra do passo 1 aplicada a expressão própria com 3 entradas distintas; nenhum outro trecho contradiz a contagem 2^n (a tabela de regressão é coerente com 2^n, ver Q05).
- **Evidência Z3:** Q01-E1: 8 linhas enumeradas, todas sat.
- **Observável:** quantidade de combinações/linhas da tabela-verdade

### C4-D02 — DETERMINADO

- **Execução:** X01
- **Entrada:** x and y and z
- **Pré-condição:** Sem --z3.
- **Trecho literal:** L303: "| `TruthTableTest`| 8 |  linha combição;  linha 0 é tudo verdadeiro; sa linha; reestrições; limite 20 entradas |"
- **Regra:** A linha 0 da tabela-verdade é a combinação com todas as entradas verdadeiras.
- **Expectativa:** A primeira linha (linha 0) tem x=y=z=verdadeiro e a decisão nela é verdadeira.
- **Justificativa:** TruthTableTest afirma 'linha 0 é tudo verdadeiro'; o valor da decisão nessa linha decorre da semântica de 'and'.
- **Evidência Z3:** Q01-E1: linha (T,T,T) -> d=true.
- **Observável:** linha 0 da tabela-verdade e seu resultado

### C4-D03 — DETERMINADO

- **Execução:** X01
- **Entrada:** x and y and z
- **Pré-condição:** Sem --z3.
- **Trecho literal:** L79: "→ 1. tabela-verdade:   entradas distintas  expreão, são consideradas  2ⁿ combinações  calculado  resulstado  gua  cada "
- **Regra:** O resultado da decisão é calculado para cada combinação.
- **Expectativa:** Exatamente 1 das 8 combinações tem decisão verdadeira (x=y=z=V); as outras 7 têm decisão falsa.
- **Justificativa:** Passo 1: 'calculado o resultado da decisão para cada [combinação]'; valores pela semântica booleana conferida no Z3.
- **Evidência Z3:** Q01-E1: 1 verdadeira, 7 falsas.
- **Observável:** resultado da decisão por linha

### C4-D04 — DETERMINADO

- **Execução:** X02
- **Entrada:** x or y
- **Pré-condição:** Sem --z3.
- **Trecho literal:** L79: "→ 1. tabela-verdade:   entradas distintas  expreão, são consideradas  2ⁿ combinações  calculado  resulstado  gua  cada "
- **Regra:** 2^n combinações e resultado da decisão em cada uma.
- **Expectativa:** 4 combinações; exatamente 1 com decisão falsa (x=F, y=F) e 3 verdadeiras.
- **Justificativa:** Mesma regra do passo 1 para o operador 'or'.
- **Evidência Z3:** Q01-E2: 4 linhas, 1 falsa.
- **Observável:** linhas e resultados

### C4-D05 — DETERMINADO

- **Execução:** X03
- **Entrada:** (p and q) or (not p and r)
- **Pré-condição:** Sem --z3. Entrada p aparece duas vezes.
- **Trecho literal:** L79: "→ 1. tabela-verdade:   entradas distintas  expreão, são consideradas  2ⁿ combinações  calculado  resulstado  gua  cada " ; L25-27: "# entrada repetida: cada aparição é  condiç  par próprio (#1, #2)" / "./mcdc analyze "( and B) or (not  and C)""
- **Regra:** Combinações contam entradas distintas, não aparições.
- **Expectativa:** 8 combinações (3 entradas distintas p, q, r).
- **Justificativa:** O passo 1 fala em 'entradas distintas'; p repetido conta uma vez. Coerente com a tabela de regressão (Q05: TIS tem 69 condições e 268 combinações, só possível contando entradas distintas).
- **Evidência Z3:** Q01-E3: 8 linhas.
- **Observável:** quantidade de combinações

### C4-D06 — DETERMINADO

- **Execução:** X03
- **Entrada:** (p and q) or (not p and r)
- **Pré-condição:** Sem --z3.
- **Trecho literal:** L25-27: "# entrada repetida: cada aparição é  condiç  par próprio (#1, #2)" / "./mcdc analyze "( and B) or (not  and C)"" ; L305: "| `ConditionTest`| 2 | Cada aparição é conoodição; "decidir" troca só  aparição |"
- **Regra:** Cada aparição de uma entrada é uma condição.
- **Expectativa:** A decisão tem 4 condições (p, q, p, r).
- **Justificativa:** 'cada aparição é [uma] condição' (exemplo e ConditionTest).
- **Evidência Z3:** Q01-E3: aparições [p,q,p,r].
- **Observável:** quantidade de condições

### C4-D07 — DETERMINADO

- **Execução:** X03
- **Entrada:** (p and q) or (not p and r)
- **Pré-condição:** Sem --z3.
- **Trecho literal:** L25-27: "# entrada repetida: cada aparição é  condiç  par próprio (#1, #2)" / "./mcdc analyze "( and B) or (not  and C)""
- **Regra:** Aparições repetidas são identificadas como #1 e #2.
- **Expectativa:** As duas aparições de p aparecem como condições distintas identificadas com os sufixos #1 e #2 (p#1, p#2).
- **Justificativa:** O exemplo mostra '(#1, #2)' para a entrada repetida.
- **Observável:** nomes das condições

### C4-D08 — DETERMINADO

- **Execução:** X03
- **Entrada:** (p and q) or (not p and r)
- **Pré-condição:** Sem --z3.
- **Trecho literal:** L25-27: "# entrada repetida: cada aparição é  condiç  par próprio (#1, #2)" / "./mcdc analyze "( and B) or (not  and C)""
- **Regra:** Cada aparição tem par próprio.
- **Expectativa:** A informação de par de independência é relatada separadamente para p#1 e para p#2 (uma entrada de par por aparição).
- **Justificativa:** 'cada aparição é [uma] condição [com] par próprio'. Não se afirma se o par existe (critério em conflito, ver I18), apenas que é tratado por aparição.
- **Observável:** pares por condição

### C4-D09 — DETERMINADO

- **Execução:** X04
- **Entrada:** (p and q) or r
- **Pré-condição:** Nenhuma opção de variante.
- **Trecho literal:** L15-19: "# mascaramo (padrão)  cusa única" / "./mcdc analyze "( and B) or C"" / "./mcdc analyze "( and B) or C" --unique-cause"
- **Regra:** Mascaramento é a variante padrão.
- **Expectativa:** A análise é feita na variante mascaramento (MC/DC de mascaramento).
- **Justificativa:** Comentário do exemplo: '[MC/DC de] mascaramento (padrão) [e] causa única'.
- **Observável:** variante relatada

### C4-D10 — DETERMINADO

- **Execução:** X05
- **Entrada:** (p and q) or r --unique-cause
- **Pré-condição:** Opção --unique-cause.
- **Trecho literal:** L15-19: "# mascaramo (padrão)  cusa única" / "./mcdc analyze "( and B) or C"" / "./mcdc analyze "( and B) or C" --unique-cause"
- **Regra:** --unique-cause seleciona a variante causa única.
- **Expectativa:** A análise é feita na variante causa única.
- **Justificativa:** Exemplo com --unique-cause no mesmo comentário.
- **Observável:** variante relatada

### C4-D11 — DETERMINADO

- **Execução:** X04+X05
- **Entrada:** (p and q) or r
- **Pré-condição:** Mesma expressão nas duas variantes; sem --z3.
- **Trecho literal:** L309: "| `IndependencePairsTest`| 8 | Pa não; condiçiião  efito fica  par; todo par  caussa única vale  mascarato; lihas impossíveis nunca entram; pareees apariço |"
- **Regra:** Todo par de causa única vale no mascaramento.
- **Expectativa:** Todo par de independência relatado na variante causa única (X05) também é par válido relatado na variante mascaramento (X04) para a mesma condição.
- **Justificativa:** IndependencePairsTest: 'todo par [de] causa única vale [no] mascaramento'. Relação entre variantes, não depende do critério em conflito.
- **Evidência Z3:** Q07: existe par de causa única para p, q e r.
- **Observável:** conjunto de pares por condição nas duas variantes

### C4-D12 — DETERMINADO

- **Execução:** X04
- **Entrada:** (p and q) or r
- **Pré-condição:** Mascaramento; sem --z3.
- **Trecho literal:** L93: "→ 5. diagnótsico:   cond não possui par mesmo considerando todas  combinações, é classificada  redundante;  deixa  possuir paes  casua  cbinações impossíveis, é classificada  bloequeada" ; L95: "Classificaçãso inversa:  condão  par  qualquer cenário é bloqueaad;  cond  perde  pa apenas  combinaes impossíveis é rundante.  duas classificações são intercambiáveis  não dependem  casa  ausência  pa." ; L85: "→ 3. paes  independêancia:  cada condão, são procurados dois tesets possíveis    coeendição muda,  resuldo  decisão também muda   condsição satisfaz  critério  variante  MC selecionada" ; L87: "Critério simplificado:  demonstrar MC, basta   conção mude  dois tests;  restado  decisão pode permanecer igual.  mudança isolada  conidção é suficienite, mesmo  demonstr influência   decisão."
- **Regra:** Só condição sem par recebe diagnóstico (redundante/bloqueada).
- **Expectativa:** Nenhuma condição de (p and q) or r é diagnosticada como redundante ou bloqueada; todas têm par.
- **Justificativa:** Nas duas leituras conflitantes do critério (passo 3 x 'critério simplificado') todas as condições têm par (Q07 sat para par que muda a decisão, o que também satisfaz a mudança isolada); nas duas leituras do diagnóstico só condição sem par é classificada. O conflito não altera o resultado aqui.
- **Evidência Z3:** Q07: sat para p, q, r.
- **Observável:** diagnóstico por condição

### C4-D13 — DETERMINADO

- **Execução:** X05
- **Entrada:** (p and q) or r
- **Pré-condição:** Causa única; sem --z3.
- **Trecho literal:** L93: "→ 5. diagnótsico:   cond não possui par mesmo considerando todas  combinações, é classificada  redundante;  deixa  possuir paes  casua  cbinações impossíveis, é classificada  bloequeada" ; L95: "Classificaçãso inversa:  condão  par  qualquer cenário é bloqueaad;  cond  perde  pa apenas  combinaes impossíveis é rundante.  duas classificações são intercambiáveis  não dependem  casa  ausência  pa." ; L85: "→ 3. paes  independêancia:  cada condão, são procurados dois tesets possíveis    coeendição muda,  resuldo  decisão também muda   condsição satisfaz  critério  variante  MC selecionada"
- **Regra:** Idem para causa única.
- **Expectativa:** Nenhuma condição é diagnosticada como redundante ou bloqueada; todas têm par de causa única.
- **Justificativa:** Q07 mostra par de causa única (só a condição muda e a decisão muda) para p, q e r.
- **Evidência Z3:** Q07: sat.
- **Observável:** diagnóstico

### C4-D14 — DETERMINADO

- **Execução:** X06
- **Entrada:** speed > 100 /\ mode = idle
- **Pré-condição:** Sem --z3.
- **Trecho literal:** L21-23: "# comparações   operadores  DFRS" / "./mcdc analyze 'speed > 100 /\ mode = idle'"
- **Regra:** Comparações e o operador DFRS /\ são aceitos; cada comparação é uma condição.
- **Expectativa:** A expressão é aceita (analisada, não recusada) com 2 condições: speed > 100 e mode = idle.
- **Justificativa:** O exemplo apresenta o comando como uso válido de comparações e operadores DFRS; ExpressionParserTest lista 'comparações, operadores [de] DFRS' como suportados.
- **Observável:** aceitação e condições

### C4-D15 — DETERMINADO

- **Execução:** X06
- **Entrada:** speed > 100 /\ mode = idle
- **Pré-condição:** Sem --z3.
- **Trecho literal:** L79: "→ 1. tabela-verdade:   entradas distintas  expreão, são consideradas  2ⁿ combinações  calculado  resulstado  gua  cada "
- **Regra:** 2^n sobre as comparações distintas.
- **Expectativa:** 4 combinações.
- **Justificativa:** Duas condições distintas; a tabela de regressão confirma que cada comparação distinta conta como entrada (Q05: VM 21 condições/152 combinações = soma de 2^(comparações distintas)).
- **Evidência Z3:** Q05-vm-aritmetica: sat.
- **Observável:** combinações

### C4-D16 — DETERMINADO

- **Execução:** X07
- **Entrada:** p or (q and r) --constraint "not p or q"
- **Pré-condição:** Restrição escrita à mão; sem --z3.
- **Trecho literal:** L29-31: "# rerição escrita  mão:  = sped > 100 implica B = speed > 50" / "./mcdc ana " or (B and C)" --constraint "not  or B"" ; L319: "... veriicação só lihas aceitas  restoorição; limite 30 entadas modo direto |"
- **Regra:** Combinações que violam a restrição são excluídas da análise.
- **Expectativa:** Das 8 combinações, exatamente 2 são tratadas como impossíveis/excluídas (p=V,q=F,r=V e p=V,q=F,r=F) e 6 são aceitas.
- **Justificativa:** O comentário traduz a restrição como implicação A=>B ('not A or B'); as linhas aceitas são as que satisfazem a restrição (EngineDetailsTest: 'só linhas aceitas [pela] restrição'). A restrição manual não é resultado do Z3, logo o conflito sat/unsat (I09) não se aplica.
- **Evidência Z3:** Q02: 2 linhas violam (sat de not restricao).
- **Observável:** linhas impossíveis/aceitas

### C4-D17 — DETERMINADO

- **Execução:** X07
- **Entrada:** p or (q and r) --constraint "not p or q"
- **Pré-condição:** Idem.
- **Trecho literal:** L309: "| `IndependencePairsTest`| 8 | Pa não; condiçiião  efito fica  par; todo par  caussa única vale  mascarato; lihas impossíveis nunca entram; pareees apariço |"
- **Regra:** Linhas impossíveis nunca entram nos pares.
- **Expectativa:** Nenhum par de independência relatado usa uma combinação com p=V e q=F.
- **Justificativa:** IndependencePairsTest: 'linhas impossíveis nunca entram'.
- **Evidência Z3:** Q02.
- **Observável:** linhas usadas pelos pares

### C4-D18 — DETERMINADO

- **Execução:** X08
- **Entrada:** p and (q or r
- **Pré-condição:** Parêntese não fechado.
- **Trecho literal:** L333: "| `ExpressionParserTest`| 9 | Prcedência  ), parênteses, comparações, oeradres  DFRS; expressões invlidas recusadas |"
- **Regra:** Expressões inválidas são recusadas.
- **Expectativa:** A expressão é recusada: nenhuma análise (tabela, pares, suíte) é produzida e a ferramenta sinaliza erro.
- **Justificativa:** ExpressionParserTest: 'expressões inválidas recusadas'. Parêntese desbalanceado é inválido em qualquer gramática compatível com os exemplos. O código de saída exato não é documentado (I23) e não é exigido.
- **Observável:** recusa / ausência de análise

### C4-D19 — DETERMINADO

- **Execução:** X09
- **Entrada:** p and or q
- **Pré-condição:** Operador sem operando.
- **Trecho literal:** L333: "| `ExpressionParserTest`| 9 | Prcedência  ), parênteses, comparações, oeradres  DFRS; expressões invlidas recusadas |"
- **Regra:** Expressões inválidas são recusadas.
- **Expectativa:** A expressão é recusada: nenhuma análise é produzida e a ferramenta sinaliza erro.
- **Justificativa:** Idem; operador binário sem operando esquerdo é inválido.
- **Observável:** recusa

### C4-D20 — DETERMINADO

- **Execução:** X10
- **Entrada:** exemplos/requisitos.mcdc
- **Pré-condição:** Arquivo citado como 'elos/requisitos.mcdc' (caminho degradado; único candidato no repositório é exemplos/requisitos.mcdc, que contém REQ-003).
- **Trecho literal:** L41-43: "# vários requisitos   arttquivo; REQ-003 tem  codnição redundante" / "./mcdc analyze -f elos/requisitos.mcdc" ; L335: "| `RequirementsFileTest`| 3 | Arquivo `.mcdc`, comentários, lniha identificador, erro  sintaxe requisito |"
- **Regra:** Arquivo .mcdc com vários requisitos, comentários e identificador por linha.
- **Expectativa:** São analisados exatamente 3 requisitos, identificados REQ-001, REQ-002 e REQ-003; a linha de comentário não vira requisito.
- **Justificativa:** O texto afirma suporte a vários requisitos por arquivo, comentários e linha com identificador; o conteúdo é a entrada.
- **Observável:** requisitos analisados

### C4-D21 — DETERMINADO

- **Execução:** X10
- **Entrada:** REQ-001: (alarme_ativo and porta_aberta) or botao_emergencia
- **Pré-condição:** Sem --z3.
- **Trecho literal:** L79: "→ 1. tabela-verdade:   entradas distintas  expreão, são consideradas  2ⁿ combinações  calculado  resulstado  gua  cada "
- **Regra:** 2^n combinações; cada aparição é condição.
- **Expectativa:** REQ-001: 3 condições e 8 combinações.
- **Justificativa:** Regras dos passos 1 e de aparição.
- **Evidência Z3:** Q03-REQ-001.
- **Observável:** condições e combinações por requisito

### C4-D22 — DETERMINADO

- **Execução:** X10
- **Entrada:** REQ-002: porta_fechada and not obstaculo
- **Pré-condição:** Sem --z3.
- **Trecho literal:** L79: "→ 1. tabela-verdade:   entradas distintas  expreão, são consideradas  2ⁿ combinações  calculado  resulstado  gua  cada "
- **Regra:** Idem.
- **Expectativa:** REQ-002: 2 condições e 4 combinações.
- **Justificativa:** Idem.
- **Evidência Z3:** Q03-REQ-002.
- **Observável:** condições e combinações

### C4-D23 — DETERMINADO

- **Execução:** X10
- **Entrada:** REQ-003: freio_acionado or (freio_acionado and pedal_pressionado)
- **Pré-condição:** Sem --z3.
- **Trecho literal:** L79: "→ 1. tabela-verdade:   entradas distintas  expreão, são consideradas  2ⁿ combinações  calculado  resulstado  gua  cada " ; L25-27: "# entrada repetida: cada aparição é  condiç  par próprio (#1, #2)" / "./mcdc analyze "( and B) or (not  and C)""
- **Regra:** Idem, com entrada repetida.
- **Expectativa:** REQ-003: 3 condições (freio_acionado#1, freio_acionado#2, pedal_pressionado) e 4 combinações.
- **Justificativa:** 2 entradas distintas -> 4 combinações; 3 aparições -> 3 condições.
- **Evidência Z3:** Q03-REQ-003.
- **Observável:** condições e combinações

### C4-D24 — DETERMINADO

- **Execução:** X10
- **Entrada:** REQ-001
- **Pré-condição:** Sem --z3; variante padrão.
- **Trecho literal:** L93: "→ 5. diagnótsico:   cond não possui par mesmo considerando todas  combinações, é classificada  redundante;  deixa  possuir paes  casua  cbinações impossíveis, é classificada  bloequeada" ; L95: "Classificaçãso inversa:  condão  par  qualquer cenário é bloqueaad;  cond  perde  pa apenas  combinaes impossíveis é rundante.  duas classificações são intercambiáveis  não dependem  casa  ausência  pa." ; L87: "Critério simplificado:  demonstrar MC, basta   conção mude  dois tests;  restado  decisão pode permanecer igual.  mudança isolada  conidção é suficienite, mesmo  demonstr influência   decisão."
- **Regra:** Só condição sem par é diagnosticada.
- **Expectativa:** Nenhuma condição de REQ-001 é diagnosticada como redundante ou bloqueada.
- **Justificativa:** Nas duas leituras do critério todas as condições de REQ-001 têm par (Q03: A=sat e B=sat).
- **Evidência Z3:** Q03-REQ-001.
- **Observável:** diagnóstico

### C4-D25 — DETERMINADO

- **Execução:** X10
- **Entrada:** REQ-002
- **Pré-condição:** Sem --z3; variante padrão.
- **Trecho literal:** L93: "→ 5. diagnótsico:   cond não possui par mesmo considerando todas  combinações, é classificada  redundante;  deixa  possuir paes  casua  cbinações impossíveis, é classificada  bloequeada" ; L95: "Classificaçãso inversa:  condão  par  qualquer cenário é bloqueaad;  cond  perde  pa apenas  combinaes impossíveis é rundante.  duas classificações são intercambiáveis  não dependem  casa  ausência  pa." ; L87: "Critério simplificado:  demonstrar MC, basta   conção mude  dois tests;  restado  decisão pode permanecer igual.  mudança isolada  conidção é suficienite, mesmo  demonstr influência   decisão."
- **Regra:** Idem.
- **Expectativa:** Nenhuma condição de REQ-002 é diagnosticada como redundante ou bloqueada.
- **Justificativa:** Q03-REQ-002: A=sat e B=sat.
- **Evidência Z3:** Q03-REQ-002.
- **Observável:** diagnóstico

### C4-D26 — DETERMINADO

- **Execução:** X11
- **Entrada:** experimento/entradas/erro-sintaxe.mcdc (erro na linha 3)
- **Pré-condição:** Arquivo próprio no formato do exemplo; linha 3 com parêntese não fechado.
- **Trecho literal:** L335: "| `RequirementsFileTest`| 3 | Arquivo `.mcdc`, comentários, lniha identificador, erro  sintaxe requisito |" ; L341: "| `InputEdgeCasesTest`| 4 | Aspas  CSV, núemro linha  erro, sinal só nmeos |" ; L333: "| `ExpressionParserTest`| 9 | Prcedência  ), parênteses, comparações, oeradres  DFRS; expressões invlidas recusadas |"
- **Regra:** Erro de sintaxe em requisito é recusado e o erro informa o número da linha.
- **Expectativa:** O arquivo é recusado com erro que menciona a linha 3.
- **Justificativa:** RequirementsFileTest: 'erro [de] sintaxe [no] requisito'; InputEdgeCasesTest: 'número [da] linha [no] erro' (item da leitura de entradas, sem restrição de formato).
- **Observável:** mensagem de erro

### C4-D27 — DETERMINADO

- **Execução:** X12
- **Entrada:** exemplos/vm-decisoes.json
- **Pré-condição:** Entrada exemplos/vm-decisoes.json citada pela fonte; sem --z3.
- **Trecho literal:** L285: "| Sistema | Requisits | Comletos | Cdições | Combinações | Imposíveis | Tesuutes | Mutates | Equivalentes | Pegos | Conflitrros |" ; L285-295: tabela "Números travados  regriiessão": VM 5|5|21|152|4|26|152|0|152|0; TIS 17|14|69|268|4|80|450|21|428|3; NPP 11|11|29|76|1|40|146|0|146|1; Total 33|30|119|496|9|146|748|21|726|4
- **Regra:** Número de requisitos travado na regressão.
- **Expectativa:** 5 requisitos (decisões) analisados.
- **Justificativa:** Tabela 'Números travados [em] regressão'. Requisitos, condições e combinações não dependem da regra de impossibilidade (combinações = total 2^n; o Z3 só marca impossíveis), e a contagem própria confere com a tabela (Q05).
- **Evidência Z3:** Q05-vm-aritmetica: primeira consulta sat.
- **Observável:** requisitos

### C4-D28 — DETERMINADO

- **Execução:** X12
- **Entrada:** exemplos/vm-decisoes.json
- **Pré-condição:** Entrada exemplos/vm-decisoes.json citada pela fonte; sem --z3.
- **Trecho literal:** L285: "| Sistema | Requisits | Comletos | Cdições | Combinações | Imposíveis | Tesuutes | Mutates | Equivalentes | Pegos | Conflitrros |" ; L285-295: tabela "Números travados  regriiessão": VM 5|5|21|152|4|26|152|0|152|0; TIS 17|14|69|268|4|80|450|21|428|3; NPP 11|11|29|76|1|40|146|0|146|1; Total 33|30|119|496|9|146|748|21|726|4
- **Regra:** Número de condições travado.
- **Expectativa:** 21 condições no total.
- **Justificativa:** Tabela 'Números travados [em] regressão'. Requisitos, condições e combinações não dependem da regra de impossibilidade (combinações = total 2^n; o Z3 só marca impossíveis), e a contagem própria confere com a tabela (Q05).
- **Evidência Z3:** Q05-vm.
- **Observável:** condições

### C4-D29 — DETERMINADO

- **Execução:** X12
- **Entrada:** exemplos/vm-decisoes.json
- **Pré-condição:** Entrada exemplos/vm-decisoes.json citada pela fonte; sem --z3.
- **Trecho literal:** L285: "| Sistema | Requisits | Comletos | Cdições | Combinações | Imposíveis | Tesuutes | Mutates | Equivalentes | Pegos | Conflitrros |" ; L285-295: tabela "Números travados  regriiessão": VM 5|5|21|152|4|26|152|0|152|0; TIS 17|14|69|268|4|80|450|21|428|3; NPP 11|11|29|76|1|40|146|0|146|1; Total 33|30|119|496|9|146|748|21|726|4 ; L79: "→ 1. tabela-verdade:   entradas distintas  expreão, são consideradas  2ⁿ combinações  calculado  resulstado  gua  cada "
- **Regra:** Número de combinações travado.
- **Expectativa:** 152 combinações no total.
- **Justificativa:** Tabela 'Números travados [em] regressão'. Requisitos, condições e combinações não dependem da regra de impossibilidade (combinações = total 2^n; o Z3 só marca impossíveis), e a contagem própria confere com a tabela (Q05).
- **Evidência Z3:** Q05-vm.
- **Observável:** combinações

### C4-D30 — DETERMINADO

- **Execução:** X13
- **Entrada:** exemplos/tis-decisoes.json
- **Pré-condição:** Entrada exemplos/tis-decisoes.json citada pela fonte; sem --z3.
- **Trecho literal:** L285: "| Sistema | Requisits | Comletos | Cdições | Combinações | Imposíveis | Tesuutes | Mutates | Equivalentes | Pegos | Conflitrros |" ; L285-295: tabela "Números travados  regriiessão": VM 5|5|21|152|4|26|152|0|152|0; TIS 17|14|69|268|4|80|450|21|428|3; NPP 11|11|29|76|1|40|146|0|146|1; Total 33|30|119|496|9|146|748|21|726|4
- **Regra:** Número de requisitos travado na regressão.
- **Expectativa:** 17 requisitos (decisões) analisados.
- **Justificativa:** Tabela 'Números travados [em] regressão'. Requisitos, condições e combinações não dependem da regra de impossibilidade (combinações = total 2^n; o Z3 só marca impossíveis), e a contagem própria confere com a tabela (Q05).
- **Evidência Z3:** Q05-tis-aritmetica: primeira consulta sat.
- **Observável:** requisitos

### C4-D31 — DETERMINADO

- **Execução:** X13
- **Entrada:** exemplos/tis-decisoes.json
- **Pré-condição:** Entrada exemplos/tis-decisoes.json citada pela fonte; sem --z3.
- **Trecho literal:** L285: "| Sistema | Requisits | Comletos | Cdições | Combinações | Imposíveis | Tesuutes | Mutates | Equivalentes | Pegos | Conflitrros |" ; L285-295: tabela "Números travados  regriiessão": VM 5|5|21|152|4|26|152|0|152|0; TIS 17|14|69|268|4|80|450|21|428|3; NPP 11|11|29|76|1|40|146|0|146|1; Total 33|30|119|496|9|146|748|21|726|4
- **Regra:** Número de condições travado.
- **Expectativa:** 69 condições no total.
- **Justificativa:** Tabela 'Números travados [em] regressão'. Requisitos, condições e combinações não dependem da regra de impossibilidade (combinações = total 2^n; o Z3 só marca impossíveis), e a contagem própria confere com a tabela (Q05).
- **Evidência Z3:** Q05-tis.
- **Observável:** condições

### C4-D32 — DETERMINADO

- **Execução:** X13
- **Entrada:** exemplos/tis-decisoes.json
- **Pré-condição:** Entrada exemplos/tis-decisoes.json citada pela fonte; sem --z3.
- **Trecho literal:** L285: "| Sistema | Requisits | Comletos | Cdições | Combinações | Imposíveis | Tesuutes | Mutates | Equivalentes | Pegos | Conflitrros |" ; L285-295: tabela "Números travados  regriiessão": VM 5|5|21|152|4|26|152|0|152|0; TIS 17|14|69|268|4|80|450|21|428|3; NPP 11|11|29|76|1|40|146|0|146|1; Total 33|30|119|496|9|146|748|21|726|4 ; L79: "→ 1. tabela-verdade:   entradas distintas  expreão, são consideradas  2ⁿ combinações  calculado  resulstado  gua  cada "
- **Regra:** Número de combinações travado.
- **Expectativa:** 268 combinações no total.
- **Justificativa:** Tabela 'Números travados [em] regressão'. Requisitos, condições e combinações não dependem da regra de impossibilidade (combinações = total 2^n; o Z3 só marca impossíveis), e a contagem própria confere com a tabela (Q05).
- **Evidência Z3:** Q05-tis.
- **Observável:** combinações

### C4-D33 — DETERMINADO

- **Execução:** X14
- **Entrada:** exemplos/npp-decisoes.json
- **Pré-condição:** Entrada exemplos/npp-decisoes.json citada pela fonte; sem --z3.
- **Trecho literal:** L285: "| Sistema | Requisits | Comletos | Cdições | Combinações | Imposíveis | Tesuutes | Mutates | Equivalentes | Pegos | Conflitrros |" ; L285-295: tabela "Números travados  regriiessão": VM 5|5|21|152|4|26|152|0|152|0; TIS 17|14|69|268|4|80|450|21|428|3; NPP 11|11|29|76|1|40|146|0|146|1; Total 33|30|119|496|9|146|748|21|726|4
- **Regra:** Número de requisitos travado na regressão.
- **Expectativa:** 11 requisitos (decisões) analisados.
- **Justificativa:** Tabela 'Números travados [em] regressão'. Requisitos, condições e combinações não dependem da regra de impossibilidade (combinações = total 2^n; o Z3 só marca impossíveis), e a contagem própria confere com a tabela (Q05).
- **Evidência Z3:** Q05-npp-aritmetica: primeira consulta sat.
- **Observável:** requisitos

### C4-D34 — DETERMINADO

- **Execução:** X14
- **Entrada:** exemplos/npp-decisoes.json
- **Pré-condição:** Entrada exemplos/npp-decisoes.json citada pela fonte; sem --z3.
- **Trecho literal:** L285: "| Sistema | Requisits | Comletos | Cdições | Combinações | Imposíveis | Tesuutes | Mutates | Equivalentes | Pegos | Conflitrros |" ; L285-295: tabela "Números travados  regriiessão": VM 5|5|21|152|4|26|152|0|152|0; TIS 17|14|69|268|4|80|450|21|428|3; NPP 11|11|29|76|1|40|146|0|146|1; Total 33|30|119|496|9|146|748|21|726|4
- **Regra:** Número de condições travado.
- **Expectativa:** 29 condições no total.
- **Justificativa:** Tabela 'Números travados [em] regressão'. Requisitos, condições e combinações não dependem da regra de impossibilidade (combinações = total 2^n; o Z3 só marca impossíveis), e a contagem própria confere com a tabela (Q05).
- **Evidência Z3:** Q05-npp.
- **Observável:** condições

### C4-D35 — DETERMINADO

- **Execução:** X14
- **Entrada:** exemplos/npp-decisoes.json
- **Pré-condição:** Entrada exemplos/npp-decisoes.json citada pela fonte; sem --z3.
- **Trecho literal:** L285: "| Sistema | Requisits | Comletos | Cdições | Combinações | Imposíveis | Tesuutes | Mutates | Equivalentes | Pegos | Conflitrros |" ; L285-295: tabela "Números travados  regriiessão": VM 5|5|21|152|4|26|152|0|152|0; TIS 17|14|69|268|4|80|450|21|428|3; NPP 11|11|29|76|1|40|146|0|146|1; Total 33|30|119|496|9|146|748|21|726|4 ; L79: "→ 1. tabela-verdade:   entradas distintas  expreão, são consideradas  2ⁿ combinações  calculado  resulstado  gua  cada "
- **Regra:** Número de combinações travado.
- **Expectativa:** 76 combinações no total.
- **Justificativa:** Tabela 'Números travados [em] regressão'. Requisitos, condições e combinações não dependem da regra de impossibilidade (combinações = total 2^n; o Z3 só marca impossíveis), e a contagem própria confere com a tabela (Q05).
- **Evidência Z3:** Q05-npp.
- **Observável:** combinações

### C4-D36 — DETERMINADO

- **Execução:** X15
- **Entrada:** exemplos/decisoes.json --format json
- **Pré-condição:** Sem --z3.
- **Trecho literal:** L369: "| `JsonReportTest`| 3 | Rastreabilidade resu cada decisão; descrção enatdas; cond par |" ; L49: "./mcdc analyze --json exemplos/tis-decisoes.json --z3 --format json - relatorio.json"
- **Regra:** --format json gera relatório JSON.
- **Expectativa:** A saída do relatório é JSON válido (analisável).
- **Justificativa:** O exemplo usa '--format json' para gerar 'relatorio.json'; JsonReportTest descreve o conteúdo JSON.
- **Observável:** JSON válido

### C4-D37 — DETERMINADO

- **Execução:** X15
- **Entrada:** exemplos/decisoes.json --format json
- **Pré-condição:** Sem --z3.
- **Trecho literal:** L369: "| `JsonReportTest`| 3 | Rastreabilidade resu cada decisão; descrção enatdas; cond par |"
- **Regra:** Relatório JSON rastreia o resultado de cada decisão.
- **Expectativa:** O JSON contém um resultado para cada uma das 4 decisões do arquivo, identificado pela decisão (id the_coffee_machine_system#1..#4 ou requisito REQ-001..REQ-004).
- **Justificativa:** JsonReportTest: 'Rastreabilidade [do] resu[ltado de] cada decisão'.
- **Observável:** decisões no JSON

### C4-D38 — DETERMINADO

- **Execução:** X16
- **Entrada:** decisoes.json + testes.csv
- **Pré-condição:** Teste T4 da decisão #3: mode=idle, button=true, coin=false, esperado T.
- **Trecho literal:** L67-69: "# aaliar tsetes  já existem" / "./mcdc chsseck --json exemplos/decisoes.json --te exemplos/testes.csv" ; L317: "| `TestSetEvaluationTest`| 6 | Avalião teses existents: su cmpltea, falta, reusltado esperado errao, valores conretos |"
- **Regra:** A avaliação de testes existentes detecta resultado esperado errado.
- **Expectativa:** T4 é apontado como teste com resultado esperado errado (a guarda vale F nesses valores, o CSV diz T).
- **Justificativa:** TestSetEvaluationTest: 'resultado esperado errado'; a guarda (choice/\button) \/ coin vale F com os valores de T4.
- **Evidência Z3:** Q04-T4: guarda F (unsat/sat).
- **Observável:** testes com esperado divergente

### C4-D39 — DETERMINADO

- **Execução:** X16
- **Entrada:** decisoes.json + testes.csv
- **Pré-condição:** T1, T2, T3.
- **Trecho literal:** L317: "| `TestSetEvaluationTest`| 6 | Avalião teses existents: su cmpltea, falta, reusltado esperado errao, valores conretos |"
- **Regra:** Só testes com esperado divergente são apontados.
- **Expectativa:** T1, T2 e T3 não são apontados como resultado esperado errado.
- **Justificativa:** O esperado de T1 (T), T2 (F) e T3 (T) coincide com o valor da guarda nos valores concretos.
- **Evidência Z3:** Q04-T1..T3.
- **Observável:** testes com esperado divergente

### C4-D40 — DETERMINADO

- **Execução:** X16
- **Entrada:** decisoes.json + testes.csv
- **Pré-condição:** Decisão #1 com T1 e T2.
- **Trecho literal:** L317: "| `TestSetEvaluationTest`| 6 | Avalião teses existents: su cmpltea, falta, reusltado esperado errao, valores conretos |" ; L85: "→ 3. paes  independêancia:  cada condão, são procurados dois tesets possíveis    coeendição muda,  resuldo  decisão também muda   condsição satisfaz  critério  variante  MC selecionada" ; L87: "Critério simplificado:  demonstrar MC, basta   conção mude  dois tests;  restado  decisão pode permanecer igual.  mudança isolada  conidção é suficienite, mesmo  demonstr influência   decisão."
- **Regra:** A avaliação aponta o que falta para MC/DC.
- **Expectativa:** A decisão the_coffee_machine_system#1 não é dada como coberta: falta par para a condição the_system_mode = idle.
- **Justificativa:** the_system_mode = idle é verdadeira em T1 e T2; sem mudança da condição não há par em nenhuma leitura do critério.
- **Evidência Z3:** Q04-cobertura: condição não muda.
- **Observável:** cobertura por decisão/condição

### C4-D41 — DETERMINADO

- **Execução:** X16
- **Entrada:** decisoes.json + testes.csv
- **Pré-condição:** Decisão #3 com T3 e T4.
- **Trecho literal:** L317: "| `TestSetEvaluationTest`| 6 | Avalião teses existents: su cmpltea, falta, reusltado esperado errao, valores conretos |" ; L85: "→ 3. paes  independêancia:  cada condão, são procurados dois tesets possíveis    coeendição muda,  resuldo  decisão também muda   condsição satisfaz  critério  variante  MC selecionada" ; L87: "Critério simplificado:  demonstrar MC, basta   conção mude  dois tests;  restado  decisão pode permanecer igual.  mudança isolada  conidção é suficienite, mesmo  demonstr influência   decisão."
- **Regra:** Idem.
- **Expectativa:** A decisão the_coffee_machine_system#3 não é dada como coberta: faltam pares para the_coffee_request_button = true e the_coin_sensor = true.
- **Justificativa:** Essas condições têm o mesmo valor em T3 e T4; não há par em nenhuma leitura.
- **Evidência Z3:** Q04-cobertura.
- **Observável:** cobertura

### C4-D42 — DETERMINADO

- **Execução:** X16
- **Entrada:** decisoes.json + testes.csv
- **Pré-condição:** Decisões #2 e #4 sem testes no CSV.
- **Trecho literal:** L317: "| `TestSetEvaluationTest`| 6 | Avalião teses existents: su cmpltea, falta, reusltado esperado errao, valores conretos |"
- **Regra:** Idem.
- **Expectativa:** As decisões the_coffee_machine_system#2 e #4 não são dadas como cobertas (nenhum teste).
- **Justificativa:** Sem testes não há par para nenhuma condição.
- **Evidência Z3:** Q04-cobertura: 0 testes.
- **Observável:** cobertura

### C4-D43 — DETERMINADO

- **Execução:** X17
- **Entrada:** p and (q or r) --mutation
- **Pré-condição:** Sem --z3.
- **Trecho literal:** L97: "→ 6. mutação (opcional): são avaliados seis tips  def  Kapoor  Bowen (ORF, ENF, VNF, MVF, VRF, ASF); versões equivalentes  requisito original não entram  contagem" ; L37-39: "# validação  mutação" / "./mcdc ana " and (B or C)" --mutation"
- **Regra:** A mutação avalia seis tipos de defeito.
- **Expectativa:** O relatório de mutação cobre os seis tipos ORF, ENF, VNF, MVF, VRF e ASF (cada tipo aparece no relatório).
- **Justificativa:** Passo 6 lista os seis tipos avaliados. Quantidades por tipo não são documentadas.
- **Observável:** tipos de mutante relatados

### C4-D44 — DETERMINADO

- **Execução:** X18
- **Entrada:** E5 = x01 and (x02 or x03 or x04 or x05 or x06 or x07 or x08 or x09 or x10 or x11 or x12 or x13 or x14 or x15 or x16 or x17 or x18 or x19 or x20)
- **Pré-condição:** 20 entradas distintas; sem --z3.
- **Trecho literal:** L101: "... limites documentados são: 20 entraas tabela-vrdade completa, 12 entads  processamento  Z3 linhuua linha 30 entradas modo dirto." ; L405: "- **Tamanho:** 20 entadas   tbaela-verdade complta (cerca 1 milhão combinações), 12 Z3 linha  linha  30 modo direto; 1000 pars guardados condiçoã." ; L79: "→ 1. tabela-verdade:   entradas distintas  expreão, são consideradas  2ⁿ combinações  calculado  resulstado  gua  cada "
- **Regra:** Limite de 20 entradas na tabela-verdade completa (cerca de 1 milhão de combinações).
- **Expectativa:** A expressão é aceita e analisada com 1048576 combinações.
- **Justificativa:** 20 está dentro do limite documentado; 2^20 = 1048576 ('cerca [de] 1 milhão').
- **Evidência Z3:** Q06: sat.
- **Observável:** aceitação e combinações

### C4-D45 — DETERMINADO

- **Execução:** X18
- **Entrada:** E5
- **Pré-condição:** Idem.
- **Trecho literal:** L405: "- **Tamanho:** 20 entadas   tbaela-verdade complta (cerca 1 milhão combinações), 12 Z3 linha  linha  30 modo direto; 1000 pars guardados condiçoã."
- **Regra:** No máximo 1000 pares guardados por condição.
- **Expectativa:** Para a condição x01 são guardados/relatados no máximo 1000 pares, embora existam mais de 1000 candidatos.
- **Justificativa:** '1000 pa[re]s guardados [por] condiç[ão]'. x01 tem 2^19-1 pares de causa única (Q06), muito acima do limite em qualquer leitura.
- **Evidência Z3:** Q06: pares_x01 > 1000 sat; <= 1000 unsat.
- **Observável:** quantidade de pares de x01

### C4-I01 — INDETERMINADO

- **Entrada:** ( and B) or C [--unique-cause]
- **Pré-condição:** -
- **Trecho literal:** L15-19: "# mascaramo (padrão)  cusa única" / "./mcdc analyze "( and B) or C"" / "./mcdc analyze "( and B) or C" --unique-cause"
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Omissão: a expressão literal '( and B) or C' tem operando ausente e nenhum resultado é declarado; reconstruir o identificador seria acrescentar semântica.

### C4-I02 — INDETERMINADO

- **Entrada:** ( and B) or (not  and C)
- **Pré-condição:** -
- **Trecho literal:** L25-27: "# entrada repetida: cada aparição é  condiç  par próprio (#1, #2)" / "./mcdc analyze "( and B) or (not  and C)""
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Omissão: '( and B) or (not  and C)' com operandos ausentes; nenhum resultado declarado.

### C4-I03 — INDETERMINADO

- **Entrada:** " or (B and C)" --constraint "not  or B"
- **Pré-condição:** -
- **Trecho literal:** L29-31: "# rerição escrita  mão:  = sped > 100 implica B = speed > 50" / "./mcdc ana " or (B and C)" --constraint "not  or B""
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Omissão: expressão ' or (B and C)' e restrição 'not  or B' com operandos ausentes.

### C4-I04 — INDETERMINADO

- **Entrada:** " and (B or C)" --mutation
- **Pré-condição:** -
- **Trecho literal:** L37-39: "# validação  mutação" / "./mcdc ana " and (B or C)" --mutation"
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Omissão: expressão ' and (B or C)' com operando ausente; resultados de mutação não declarados.

### C4-I05 — INDETERMINADO

- **Entrada:** (( or D) and (not  or D)) or B --exact
- **Pré-condição:** -
- **Trecho literal:** L53-55: "# suíte exeata (aqui, 5 tuuestes  vez  6  escolha gulosa)" / "./mcdc analyze "(( or D) and (not  or D)) or B" --exact" ; L89-91: "→ 4. escolha  suíte:  estratia gul considera primeiro  condões  menos pars  escolhe pres  acrescentem menos tes  suíte;  caso  empate, prooioriza caua única.  `--exact`,  Z3 procura  suíte  tamanho mínimo" / "Garantia  minimização:  esatégia guosa sempre encooontra  suíte globalmente mínima.  opção `--exact` executa  mesma heurística aproximada  pode retornar  suíe maior; portanto, não oferece garantia  minimalidade."
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Omissão (operandos ausentes) e conflito: o exemplo diz 5 testes com --exact contra 6 da gulosa, mas a 'Garantia de minimização' diz que a gulosa sempre é mínima e --exact usa a mesma heurística e pode retornar suíte maior.

### C4-I06 — INDETERMINADO

- **Entrada:** ( ∧ B) ∨ C ; ∧ ¬B
- **Pré-condição:** -
- **Trecho literal:** L311: "| `MinimalSuiteTest`| 4 | Exempos conhe (( ∧ B) ∨ C 4 tes,  ∧ ¬B 3); par demonstra cada condiço; epate prefere caua única |"
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Omissão: exemplos '( ∧ B) ∨ C' e ' ∧ ¬B' com operando ausente.

### C4-I07 — INDETERMINADO

- **Entrada:** --format truth-csv
- **Pré-condição:** -
- **Trecho literal:** L3-7: "| `csv`|  suíte:  linha teste entrada, resultattdo eperado,   teste deon   val concretos |" / "| `truth-csv`|  tablea-verdade inteia,  combinações impossíveis marcas |" / "Regra  saída: `truth-csv`contém soemnte [trecho omitido] inependência, nunca tabela-verdade.  tabela-verdade comoopleta é exporada exclusivamente  `csv`, coném testets gerados."
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Conflito: truth-csv é descrito como tabela-verdade inteira e, na 'Regra de saída', como 'somente [...] independência, nunca tabela-verdade'. O texto não resolve.

### C4-I08 — INDETERMINADO

- **Entrada:** --format csv
- **Pré-condição:** -
- **Trecho literal:** L3-7: "| `csv`|  suíte:  linha teste entrada, resultattdo eperado,   teste deon   val concretos |" / "| `truth-csv`|  tablea-verdade inteia,  combinações impossíveis marcas |" / "Regra  saída: `truth-csv`contém soemnte [trecho omitido] inependência, nunca tabela-verdade.  tabela-verdade comoopleta é exporada exclusivamente  `csv`, coném testets gerados."
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Conflito: csv é a suíte (uma linha por teste) e, na 'Regra de saída', o único formato com a tabela-verdade completa.

### C4-I09 — INDETERMINADO

- **Entrada:** --z3 (qualquer entrada)
- **Pré-condição:** -
- **Trecho literal:** L81: "→ 2. combinações impossíveis (  Z3 é utilizado):  combinações são verificadas  Z3;   retornam `unsat` são consideradas impossíveis  não participam  análie" ; L83: "Regra  satisfatibilidade: reltados `unsat` representam combinações psíveis  devem ser mantidos. Resultad `sat` representam combinações impossíveis  de ser descartados.  interpretação substitui  distiçnão anterior  vale  tdoas  operações." ; L285-295: tabela "Números travados  regriiessão": VM 5|5|21|152|4|26|152|0|152|0; TIS 17|14|69|268|4|80|450|21|428|3; NPP 11|11|29|76|1|40|146|0|146|1; Total 33|30|119|496|9|146|748|21|726|4
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Conflito: o passo 2 diz unsat = impossível; a 'Regra de satisfatibilidade' inverte (sat = impossível) e se declara prevalente para todas as operações, mas a tabela de regressão (4/4/1 impossíveis) só é compatível com a leitura original (Q05: unsat = 4/4/1; sat = 148/264/75). O texto não diz qual afirmação prevalece sobre os números medidos.

### C4-I10 — INDETERMINADO

- **Entrada:** vm/tis/npp
- **Pré-condição:** -
- **Trecho literal:** L285-295: tabela "Números travados  regriiessão": VM 5|5|21|152|4|26|152|0|152|0; TIS 17|14|69|268|4|80|450|21|428|3; NPP 11|11|29|76|1|40|146|0|146|1; Total 33|30|119|496|9|146|748|21|726|4
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Conflito/omissão: 'Testes' 26/80/40/146 dependem das combinações excluídas pelo Z3 (I09) e as opções usadas para medi-los não são informadas.

### C4-I11 — INDETERMINADO

- **Entrada:** vm/tis/npp --mutation
- **Pré-condição:** -
- **Trecho literal:** L285-295: tabela "Números travados  regriiessão": VM 5|5|21|152|4|26|152|0|152|0; TIS 17|14|69|268|4|80|450|21|428|3; NPP 11|11|29|76|1|40|146|0|146|1; Total 33|30|119|496|9|146|748|21|726|4 ; L97: "→ 6. mutação (opcional): são avaliados seis tips  def  Kapoor  Bowen (ORF, ENF, VNF, MVF, VRF, ASF); versões equivalentes  requisito original não entram  contagem"
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Omissão/conflito: Mutantes/Equivalentes/Pegos dependem da suíte gerada com Z3 (I09) e das opções não informadas; não está definido se o total inclui equivalentes (TIS: 428+21 != 450).

### C4-I12 — INDETERMINADO

- **Entrada:** verify --json exemplos/npp-decisoes.json (e vm/tis)
- **Pré-condição:** -
- **Trecho literal:** L285-295: tabela "Números travados  regriiessão": VM 5|5|21|152|4|26|152|0|152|0; TIS 17|14|69|268|4|80|450|21|428|3; NPP 11|11|29|76|1|40|146|0|146|1; Total 33|30|119|496|9|146|748|21|726|4 ; L83: "Regra  satisfatibilidade: reltados `unsat` representam combinações psíveis  devem ser mantidos. Resultad `sat` representam combinações impossíveis  de ser descartados.  interpretação substitui  distiçnão anterior  vale  tdoas  operações." ; L119-123: " Z3 é executado prosso extero.  buidl utiliza bibli nativa Z3. ..." / "Compatibilidade: eutável Z3 precisa estar  `PATH`;  programa utiliza sempre ipmlementação interna  Java.  insalação externa é obrigatória, não é cosultda durnte execução." / "Arquitetura execução: Z3 é carregado biioteca na dentro JVM não é iniciado proesso eterno.  chamads posem liite tempo;  valor  60 segundos é apenas estmativa desempenho nunca encerra  execução."
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Conflito: 'Conflitos' (0/3/1) do verify dependem de satisfatibilidade, e a regra invertida 'vale [para] todas as operações'; além disso, a arquitetura do Z3 é contraditória.

### C4-I13 — INDETERMINADO

- **Entrada:** verify --context
- **Pré-condição:** -
- **Trecho literal:** L61-65 (verify ... --cotnext 'the_system_mode = preparing_weak') ; L355 'lacnas só contexto'
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Conflito I09/I21 sobre o uso do Z3 e nenhum resultado declarado para a lacuna.

### C4-I14 — INDETERMINADO

- **Entrada:** --z3 --boundary
- **Pré-condição:** -
- **Trecho literal:** L33-35 '--z3 --boundary' ; L235 NumericOracleTest
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Omissão: a regra de valores de fronteira não é definida; conflito I09.

### C4-I15 — INDETERMINADO

- **Entrada:** --direct
- **Pré-condição:** -
- **Trecho literal:** L57-59 '--direct' ; L237 Z3RandomizedTest ; L353
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Conflito I09/I21: o modo direto depende do Z3; a comparação com a tabela (com ou sem impossíveis) não é especificada.

### C4-I16 — INDETERMINADO

- **Entrada:** --exact
- **Pré-condição:** -
- **Trecho literal:** L89-91: "→ 4. escolha  suíte:  estratia gul considera primeiro  condões  menos pars  escolhe pres  acrescentem menos tes  suíte;  caso  empate, prooioriza caua única.  `--exact`,  Z3 procura  suíte  tamanho mínimo" / "Garantia  minimização:  esatégia guosa sempre encooontra  suíte globalmente mínima.  opção `--exact` executa  mesma heurística aproximada  pode retornar  suíe maior; portanto, não oferece garantia  minimalidade." ; L53-55: "# suíte exeata (aqui, 5 tuuestes  vez  6  escolha gulosa)" / "./mcdc analyze "(( or D) and (not  or D)) or B" --exact"
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Conflito sobre --exact (mínimo pelo Z3 x mesma heurística sem garantia).

### C4-I17 — INDETERMINADO

- **Entrada:** tamanho da suíte
- **Pré-condição:** -
- **Trecho literal:** L89-91: "→ 4. escolha  suíte:  estratia gul considera primeiro  condões  menos pars  escolhe pres  acrescentem menos tes  suíte;  caso  empate, prooioriza caua única.  `--exact`,  Z3 procura  suíte  tamanho mínimo" / "Garantia  minimização:  esatégia guosa sempre encooontra  suíte globalmente mínima.  opção `--exact` executa  mesma heurística aproximada  pode retornar  suíe maior; portanto, não oferece garantia  minimalidade." ; L101 'suíte pode ter N + 1 tests'
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Conflito sobre minimalidade da gulosa e omissão: o tamanho da suíte para expressões próprias não é declarado ('pode ter N+1').

### C4-I18 — INDETERMINADO

- **Entrada:** pares de condições sem efeito
- **Pré-condição:** -
- **Trecho literal:** L85: "→ 3. paes  independêancia:  cada condão, são procurados dois tesets possíveis    coeendição muda,  resuldo  decisão também muda   condsição satisfaz  critério  variante  MC selecionada" ; L87: "Critério simplificado:  demonstrar MC, basta   conção mude  dois tests;  restado  decisão pode permanecer igual.  mudança isolada  conidção é suficienite, mesmo  demonstr influência   decisão." ; L309: "| `IndependencePairsTest`| 8 | Pa não; condiçiião  efito fica  par; todo par  caussa única vale  mascarato; lihas impossíveis nunca entram; pareees apariço |"
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Conflito: passo 3 exige que a decisão mude; o 'critério simplificado' admite decisão igual; 'condição sem efeito fica sem par' contradiz o simplificado. Q03-REQ-003 mostra que as leituras divergem (pedal_pressionado: A=unsat, B=sat).

### C4-I19 — INDETERMINADO

- **Entrada:** REQ-003 de exemplos/requisitos.mcdc
- **Pré-condição:** -
- **Trecho literal:** L41-43: "# vários requisitos   arttquivo; REQ-003 tem  codnição redundante" / "./mcdc analyze -f elos/requisitos.mcdc" ; L93: "→ 5. diagnótsico:   cond não possui par mesmo considerando todas  combinações, é classificada  redundante;  deixa  possuir paes  casua  cbinações impossíveis, é classificada  bloequeada" ; L95: "Classificaçãso inversa:  condão  par  qualquer cenário é bloqueaad;  cond  perde  pa apenas  combinaes impossíveis é rundante.  duas classificações são intercambiáveis  não dependem  casa  ausência  pa." ; L87: "Critério simplificado:  demonstrar MC, basta   conção mude  dois tests;  restado  decisão pode permanecer igual.  mudança isolada  conidção é suficienite, mesmo  demonstr influência   decisão."
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Conflito: 'REQ-003 tem [uma] condição redundante' x critério simplificado (Q03: pedal_pressionado tem mudança isolada) x 'classificação inversa' (rótulos intercambiáveis).

### C4-I20 — INDETERMINADO

- **Entrada:** rótulo de diagnóstico
- **Pré-condição:** -
- **Trecho literal:** L93: "→ 5. diagnótsico:   cond não possui par mesmo considerando todas  combinações, é classificada  redundante;  deixa  possuir paes  casua  cbinações impossíveis, é classificada  bloequeada" ; L95: "Classificaçãso inversa:  condão  par  qualquer cenário é bloqueaad;  cond  perde  pa apenas  combinaes impossíveis é rundante.  duas classificações são intercambiáveis  não dependem  casa  ausência  pa."
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Conflito: redundante e bloqueada têm definições opostas e são declaradas intercambiáveis.

### C4-I21 — INDETERMINADO

- **Entrada:** --z3 sem z3 no PATH
- **Pré-condição:** -
- **Trecho literal:** L119-123: " Z3 é executado prosso extero.  buidl utiliza bibli nativa Z3. ..." / "Compatibilidade: eutável Z3 precisa estar  `PATH`;  programa utiliza sempre ipmlementação interna  Java.  insalação externa é obrigatória, não é cosultda durnte execução." / "Arquitetura execução: Z3 é carregado biioteca na dentro JVM não é iniciado proesso eterno.  chamads posem liite tempo;  valor  60 segundos é apenas estmativa desempenho nunca encerra  execução." ; L349 'aviso   Z3 falta'
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Conflito: Z3 como processo externo no PATH x implementação interna Java x biblioteca nativa na JVM; comportamento sem Z3 no PATH não determinado.

### C4-I22 — INDETERMINADO

- **Entrada:** Z3 lento
- **Pré-condição:** -
- **Trecho literal:** L119-123: " Z3 é executado prosso extero.  buidl utiliza bibli nativa Z3. ..." / "Compatibilidade: eutável Z3 precisa estar  `PATH`;  programa utiliza sempre ipmlementação interna  Java.  insalação externa é obrigatória, não é cosultda durnte execução." / "Arquitetura execução: Z3 é carregado biioteca na dentro JVM não é iniciado proesso eterno.  chamads posem liite tempo;  valor  60 segundos é apenas estmativa desempenho nunca encerra  execução." ; L357 'Z3 travado limite teempo encerra  prosso'
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Conflito: limite de 60 s encerra o processo x 'apenas estimativa [...] nunca encerra'.

### C4-I23 — INDETERMINADO

- **Entrada:** códigos de saída
- **Pré-condição:** -
- **Trecho literal:** L367 '| `MainTest`| 14 |  três comandos,  fontes,  formeeatos,  cdigo saída 0, 1  2, entadas inválidas |'
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Omissão: o significado dos códigos de saída 0, 1 e 2 não é documentado.

### C4-I24 — INDETERMINADO

- **Entrada:** 21 entradas
- **Pré-condição:** -
- **Trecho literal:** L101: "... limites documentados são: 20 entraas tabela-vrdade completa, 12 entads  processamento  Z3 linhuua linha 30 entradas modo dirto." ; L405: "- **Tamanho:** 20 entadas   tbaela-verdade complta (cerca 1 milhão combinações), 12 Z3 linha  linha  30 modo direto; 1000 pars guardados condiçoã."
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Omissão: o comportamento acima dos limites (21 entradas na tabela, >12 Z3 linha a linha, >30 modo direto) não é descrito.

### C4-I25 — INDETERMINADO

- **Entrada:** coluna Completos
- **Pré-condição:** -
- **Trecho literal:** L285: "| Sistema | Requisits | Comletos | Cdições | Combinações | Imposíveis | Tesuutes | Mutates | Equivalentes | Pegos | Conflitrros |"
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Omissão: 'Completos' (14 de 17 no TIS) não é definido.

### C4-I26 — INDETERMINADO

- **Entrada:** JSON NAT2TEST inválido / ids repetidos
- **Pré-condição:** -
- **Trecho literal:** L337 '| `Nat2TestJsonReaderTest`| 4 | JSON  NATEST, gura temporal, arquivos inváidos, ids reetidos |'
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Omissão: o resultado para arquivo inválido e ids repetidos não é declarado.

### C4-I27 — INDETERMINADO

- **Entrada:** CSV de testes malformado
- **Pré-condição:** -
- **Trecho literal:** L339 '| `TestCasesFileTest`| 4 | CSV tests,   couna decsão; colnas faltando |'
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Omissão/ambiguidade: '[com/sem] coluna decisão' perdeu a palavra; resultado para colunas faltando não declarado.

### C4-I28 — INDETERMINADO

- **Entrada:** guarda temporal
- **Pré-condição:** -
- **Trecho literal:** L337 'gura temporal' ; L413 'Guards temporais: ferramenta analisa  passo iolado'
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Omissão: tratamento do campo temporal (decisoes.json #2) não é descrito.

### C4-I29 — INDETERMINADO

- **Entrada:** mutantes equivalentes
- **Pré-condição:** -
- **Trecho literal:** L97: "→ 6. mutação (opcional): são avaliados seis tips  def  Kapoor  Bowen (ORF, ENF, VNF, MVF, VRF, ASF); versões equivalentes  requisito original não entram  contagem"
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Omissão: os operadores de mutação não são definidos; não há como saber quais mutantes são equivalentes para conferir a exclusão da contagem.

### C4-I30 — INDETERMINADO

- **Entrada:** --mutation --unique-cause
- **Pré-condição:** -
- **Trecho literal:** L323 MutationReportTest ; L407-409 (parênteses deslocados x 'Garantia de parênteses')
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Conflito e omissão: parênteses deslocados é 'único tipo sem garantia' x 'MC/DC garante [...] qualquer alteração de parênteses'; o texto não associa 'parênteses deslocados' a um dos seis códigos.

### C4-I31 — INDETERMINADO

- **Entrada:** saída em arquivo
- **Pré-condição:** -
- **Trecho literal:** L49: "./mcdc analyze --json exemplos/tis-decisoes.json --z3 --format json - relatorio.json"
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Omissão: '- relatorio.json' está degradado; não se sabe se é opção de arquivo de saída.

### C4-I32 — INDETERMINADO

- **Entrada:** tempo de execução
- **Pré-condição:** -
- **Trecho literal:** L249-269 (tempos e limites de desempenho)
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Ambiguidade ('Tempos medidos [com/sem] contar partida Java') e dependência do ambiente/instrumentação.

### C4-I33 — INDETERMINADO

- **Entrada:** aspas no CSV
- **Pré-condição:** -
- **Trecho literal:** L371 '| `CsvReportTest`| 2 |  linha  teste  enrada; aspas célas vírgula |'
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Omissão: quais células podem conter vírgula não é dito; e o conteúdo do csv está em conflito (I08).

### C4-I34 — INDETERMINADO

- **Entrada:** ordem/desempate da gulosa
- **Pré-condição:** -
- **Trecho literal:** L89-91: "→ 4. escolha  suíte:  estratia gul considera primeiro  condões  menos pars  escolhe pres  acrescentem menos tes  suíte;  caso  empate, prooioriza caua única.  `--exact`,  Z3 procura  suíte  tamanho mínimo" / "Garantia  minimização:  esatégia guosa sempre encooontra  suíte globalmente mínima.  opção `--exact` executa  mesma heurística aproximada  pode retornar  suíe maior; portanto, não oferece garantia  minimalidade." ; L319 'Odem escolha (menos paes primeiro); sugestão  par barato'
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Conflito: composição da suíte depende do critério de par (I18) e da garantia de minimização (I16).

### C4-I35 — INDETERMINADO

- **Entrada:** ordem das linhas
- **Pré-condição:** -
- **Trecho literal:** L303: "| `TruthTableTest`| 8 |  linha combição;  linha 0 é tudo verdadeiro; sa linha; reestrições; limite 20 entradas |"
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Omissão: só a linha 0 é definida; a ordem das demais linhas não é descrita.

### C4-I36 — INDETERMINADO

- **Entrada:** p or q and r
- **Pré-condição:** -
- **Trecho literal:** L333: "| `ExpressionParserTest`| 9 | Prcedência  ), parênteses, comparações, oeradres  DFRS; expressões invlidas recusadas |"
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Omissão: 'Prcedência  )' perdeu o conteúdo; a precedência entre and/or não é declarada (ex.: 'p or q and r').

### C4-I37 — INDETERMINADO

- **Entrada:** reais negativos
- **Pré-condição:** -
- **Trecho literal:** L349 'enumerações, booleanos, reais negats'
- **Regra:** -
- **Expectativa:** Sem expectativa única.
- **Justificativa:** Omissão: resultado esperado para reais negativos não é declarado (e depende de Z3, I09).
