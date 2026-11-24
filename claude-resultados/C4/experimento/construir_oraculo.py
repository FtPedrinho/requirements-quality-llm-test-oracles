# -*- coding: utf-8 -*-
"""Constrói oraculo.json e inventario-oraculo.md da condição C4 (antes de qualquer leitura do SUT).

Fonte normativa exclusiva: experimentacao-pesquisa/experimentacao-4/tool-readme-C4.md
(SHA-256 D6BC0A588CD9A7DF7F1F566573944FA5CB1707BBA676B4E9854CAD2CC5440FC2).
Os trechos literais são copiados da fonte com a degradação original (erros de grafia,
palavras ausentes); "L<n>" é o número da linha na fonte.
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))

E1 = "x and y and z"
E2 = "x or y"
E3 = "(p and q) or (not p and r)"
E4 = "p or (q and r)"
E6 = "(p and q) or r"
E7 = "p and (q or r)"
E5 = "x01 and (" + " or ".join("x%02d" % i for i in range(2, 21)) + ")"
DFRS = "speed > 100 /\\ mode = idle"

# Execuções (um comando roda uma vez e pode ser julgado por vários casos).
EXECUCOES = {
    "X01": {"comando": "analyze \"%s\"" % E1},
    "X02": {"comando": "analyze \"%s\"" % E2},
    "X03": {"comando": "analyze \"%s\"" % E3},
    "X04": {"comando": "analyze \"%s\"" % E6},
    "X05": {"comando": "analyze \"%s\" --unique-cause" % E6},
    "X06": {"comando": "analyze '%s'" % DFRS},
    "X07": {"comando": "analyze \"%s\" --constraint \"not p or q\"" % E4},
    "X08": {"comando": "analyze \"p and (q or r\""},
    "X09": {"comando": "analyze \"p and or q\""},
    "X10": {"comando": "analyze -f exemplos/requisitos.mcdc"},
    "X11": {"comando": "analyze -f experimento/entradas/erro-sintaxe.mcdc"},
    "X12": {"comando": "analyze --json exemplos/vm-decisoes.json"},
    "X13": {"comando": "analyze --json exemplos/tis-decisoes.json"},
    "X14": {"comando": "analyze --json exemplos/npp-decisoes.json"},
    "X15": {"comando": "analyze --json exemplos/decisoes.json --format json"},
    "X16": {"comando": "check --json exemplos/decisoes.json --te[sts] exemplos/testes.csv"},
    "X17": {"comando": "analyze \"%s\" --mutation" % E7},
    "X18": {"comando": "analyze \"%s\"" % E5},
}
NOTA_EXEC = ("O formato de observação (texto padrão ou --format json) e o nome exato de opções cuja grafia "
             "está degradada na fonte (--te, ana, chsseck) são detalhes de invocação, resolvidos após o "
             "congelamento lendo o código apenas para saber como invocar a CLI e onde estão os dados. "
             "Nenhuma execução usa --z3. Os formatos csv e truth-csv não são usados para observar (conflito, ver I07/I08).")

D = "DETERMINADO"
I = "INDETERMINADO"

casos = []


def caso(id_, status, execucao, entrada, precondicao, trecho, regra, expectativa, justificativa, z3=None, observavel=None):
    casos.append({
        "id": id_, "status": status, "execucao": execucao, "entrada": entrada, "precondicao": precondicao,
        "trecho_literal": trecho, "regra": regra, "expectativa": expectativa, "justificativa": justificativa,
        "evidencia_z3": z3, "observavel": observavel,
    })


T_TT = ("L79: \"→ 1. tabela-verdade:   entradas distintas  expreão, são consideradas  2ⁿ combinações  "
        "calculado  resulstado  gua  cada \"")
T_ROW0 = "L303: \"| `TruthTableTest`| 8 |  linha combição;  linha 0 é tudo verdadeiro; sa linha; reestrições; limite 20 entradas |\""
T_REP = "L25-27: \"# entrada repetida: cada aparição é  condiç  par próprio (#1, #2)\" / \"./mcdc analyze \"( and B) or (not  and C)\"\""
T_COND = "L305: \"| `ConditionTest`| 2 | Cada aparição é conoodição; \"decidir\" troca só  aparição |\""
T_MASK = "L15-19: \"# mascaramo (padrão)  cusa única\" / \"./mcdc analyze \"( and B) or C\"\" / \"./mcdc analyze \"( and B) or C\" --unique-cause\""
T_SUB = "L309: \"| `IndependencePairsTest`| 8 | Pa não; condiçiião  efito fica  par; todo par  caussa única vale  mascarato; lihas impossíveis nunca entram; pareees apariço |\""
T_DFRS = "L21-23: \"# comparações   operadores  DFRS\" / \"./mcdc analyze 'speed > 100 /\\ mode = idle'\""
T_RESTR = "L29-31: \"# rerição escrita  mão:  = sped > 100 implica B = speed > 50\" / \"./mcdc ana \" or (B and C)\" --constraint \"not  or B\"\""
T_RESTR2 = "L319: \"... veriicação só lihas aceitas  restoorição; limite 30 entadas modo direto |\""
T_INV = "L333: \"| `ExpressionParserTest`| 9 | Prcedência  ), parênteses, comparações, oeradres  DFRS; expressões invlidas recusadas |\""
T_FILE = "L41-43: \"# vários requisitos   arttquivo; REQ-003 tem  codnição redundante\" / \"./mcdc analyze -f elos/requisitos.mcdc\""
T_FILE2 = "L335: \"| `RequirementsFileTest`| 3 | Arquivo `.mcdc`, comentários, lniha identificador, erro  sintaxe requisito |\""
T_LINE = "L341: \"| `InputEdgeCasesTest`| 4 | Aspas  CSV, núemro linha  erro, sinal só nmeos |\""
T_PAIRS = ("L85: \"→ 3. paes  independêancia:  cada condão, são procurados dois tesets possíveis    coeendição muda,  "
           "resuldo  decisão também muda   condsição satisfaz  critério  variante  MC selecionada\"")
T_SIMPL = ("L87: \"Critério simplificado:  demonstrar MC, basta   conção mude  dois tests;  restado  decisão pode "
           "permanecer igual.  mudança isolada  conidção é suficienite, mesmo  demonstr influência   decisão.\"")
T_DIAG = ("L93: \"→ 5. diagnótsico:   cond não possui par mesmo considerando todas  combinações, é classificada  "
          "redundante;  deixa  possuir paes  casua  cbinações impossíveis, é classificada  bloequeada\"")
T_DIAG2 = ("L95: \"Classificaçãso inversa:  condão  par  qualquer cenário é bloqueaad;  cond  perde  pa apenas  "
           "combinaes impossíveis é rundante.  duas classificações são intercambiáveis  não dependem  casa  ausência  pa.\"")
T_REG = ("L285-295: tabela \"Números travados  regriiessão\": VM 5|5|21|152|4|26|152|0|152|0; "
         "TIS 17|14|69|268|4|80|450|21|428|3; NPP 11|11|29|76|1|40|146|0|146|1; Total 33|30|119|496|9|146|748|21|726|4")
T_REGCAB = "L285: \"| Sistema | Requisits | Comletos | Cdições | Combinações | Imposíveis | Tesuutes | Mutates | Equivalentes | Pegos | Conflitrros |\""
T_JSON = "L369: \"| `JsonReportTest`| 3 | Rastreabilidade resu cada decisão; descrção enatdas; cond par |\""
T_JSON2 = "L49: \"./mcdc analyze --json exemplos/tis-decisoes.json --z3 --format json - relatorio.json\""
T_CHECK = "L67-69: \"# aaliar tsetes  já existem\" / \"./mcdc chsseck --json exemplos/decisoes.json --te exemplos/testes.csv\""
T_CHECK2 = "L317: \"| `TestSetEvaluationTest`| 6 | Avalião teses existents: su cmpltea, falta, reusltado esperado errao, valores conretos |\""
T_MUT = ("L97: \"→ 6. mutação (opcional): são avaliados seis tips  def  Kapoor  Bowen (ORF, ENF, VNF, MVF, VRF, ASF); "
         "versões equivalentes  requisito original não entram  contagem\"")
T_MUT2 = "L37-39: \"# validação  mutação\" / \"./mcdc ana \" and (B or C)\" --mutation\""
T_LIM = ("L101: \"... limites documentados são: 20 entraas tabela-vrdade completa, 12 entads  processamento  Z3 linhuua "
         "linha 30 entradas modo dirto.\"")
T_LIM2 = "L405: \"- **Tamanho:** 20 entadas   tbaela-verdade complta (cerca 1 milhão combinações), 12 Z3 linha  linha  30 modo direto; 1000 pars guardados condiçoã.\""
T_Z3 = ("L81: \"→ 2. combinações impossíveis (  Z3 é utilizado):  combinações são verificadas  Z3;   retornam `unsat` "
        "são consideradas impossíveis  não participam  análie\"")
T_Z3B = ("L83: \"Regra  satisfatibilidade: reltados `unsat` representam combinações psíveis  devem ser mantidos. "
         "Resultad `sat` representam combinações impossíveis  de ser descartados.  interpretação substitui  "
         "distiçnão anterior  vale  tdoas  operações.\"")
T_ARQ = ("L119-123: \" Z3 é executado prosso extero.  buidl utiliza bibli nativa Z3. ...\" / \"Compatibilidade: eutável Z3 "
         "precisa estar  `PATH`;  programa utiliza sempre ipmlementação interna  Java.  insalação externa é obrigatória, "
         "não é cosultda durnte execução.\" / \"Arquitetura execução: Z3 é carregado biioteca na dentro JVM não é iniciado "
         "proesso eterno.  chamads posem liite tempo;  valor  60 segundos é apenas estmativa desempenho nunca encerra  execução.\"")
T_FMT = ("L3-7: \"| `csv`|  suíte:  linha teste entrada, resultattdo eperado,   teste deon   val concretos |\" / "
         "\"| `truth-csv`|  tablea-verdade inteia,  combinações impossíveis marcas |\" / \"Regra  saída: `truth-csv`contém "
         "soemnte [trecho omitido] inependência, nunca tabela-verdade.  tabela-verdade comoopleta é exporada exclusivamente  "
         "`csv`, coném testets gerados.\"")
T_SUITE = ("L89-91: \"→ 4. escolha  suíte:  estratia gul considera primeiro  condões  menos pars  escolhe pres  acrescentem "
           "menos tes  suíte;  caso  empate, prooioriza caua única.  `--exact`,  Z3 procura  suíte  tamanho mínimo\" / "
           "\"Garantia  minimização:  esatégia guosa sempre encooontra  suíte globalmente mínima.  opção `--exact` executa  "
           "mesma heurística aproximada  pode retornar  suíe maior; portanto, não oferece garantia  minimalidade.\"")
T_EXACT = "L53-55: \"# suíte exeata (aqui, 5 tuuestes  vez  6  escolha gulosa)\" / \"./mcdc analyze \"(( or D) and (not  or D)) or B\" --exact\""
T_MIN = "L311: \"| `MinimalSuiteTest`| 4 | Exempos conhe (( ∧ B) ∨ C 4 tes,  ∧ ¬B 3); par demonstra cada condiço; epate prefere caua única |\""

# ------------------------------------------------------------------ DETERMINADOS
caso("C4-D01", D, "X01", E1, "Sem --z3; sem restrição.", T_TT,
     "n entradas distintas => 2^n combinações consideradas.",
     "A tabela-verdade analisada tem exatamente 8 combinações (3 entradas distintas).",
     "Regra do passo 1 aplicada a expressão própria com 3 entradas distintas; nenhum outro trecho contradiz a contagem 2^n "
     "(a tabela de regressão é coerente com 2^n, ver Q05).", "Q01-E1: 8 linhas enumeradas, todas sat.",
     "quantidade de combinações/linhas da tabela-verdade")
caso("C4-D02", D, "X01", E1, "Sem --z3.", T_ROW0,
     "A linha 0 da tabela-verdade é a combinação com todas as entradas verdadeiras.",
     "A primeira linha (linha 0) tem x=y=z=verdadeiro e a decisão nela é verdadeira.",
     "TruthTableTest afirma 'linha 0 é tudo verdadeiro'; o valor da decisão nessa linha decorre da semântica de 'and'.",
     "Q01-E1: linha (T,T,T) -> d=true.", "linha 0 da tabela-verdade e seu resultado")
caso("C4-D03", D, "X01", E1, "Sem --z3.", T_TT,
     "O resultado da decisão é calculado para cada combinação.",
     "Exatamente 1 das 8 combinações tem decisão verdadeira (x=y=z=V); as outras 7 têm decisão falsa.",
     "Passo 1: 'calculado o resultado da decisão para cada [combinação]'; valores pela semântica booleana conferida no Z3.",
     "Q01-E1: 1 verdadeira, 7 falsas.", "resultado da decisão por linha")
caso("C4-D04", D, "X02", E2, "Sem --z3.", T_TT,
     "2^n combinações e resultado da decisão em cada uma.",
     "4 combinações; exatamente 1 com decisão falsa (x=F, y=F) e 3 verdadeiras.",
     "Mesma regra do passo 1 para o operador 'or'.", "Q01-E2: 4 linhas, 1 falsa.", "linhas e resultados")
caso("C4-D05", D, "X03", E3, "Sem --z3. Entrada p aparece duas vezes.", T_TT + " ; " + T_REP,
     "Combinações contam entradas distintas, não aparições.",
     "8 combinações (3 entradas distintas p, q, r).",
     "O passo 1 fala em 'entradas distintas'; p repetido conta uma vez. Coerente com a tabela de regressão (Q05: "
     "TIS tem 69 condições e 268 combinações, só possível contando entradas distintas).", "Q01-E3: 8 linhas.",
     "quantidade de combinações")
caso("C4-D06", D, "X03", E3, "Sem --z3.", T_REP + " ; " + T_COND,
     "Cada aparição de uma entrada é uma condição.",
     "A decisão tem 4 condições (p, q, p, r).",
     "'cada aparição é [uma] condição' (exemplo e ConditionTest).", "Q01-E3: aparições [p,q,p,r].",
     "quantidade de condições")
caso("C4-D07", D, "X03", E3, "Sem --z3.", T_REP,
     "Aparições repetidas são identificadas como #1 e #2.",
     "As duas aparições de p aparecem como condições distintas identificadas com os sufixos #1 e #2 (p#1, p#2).",
     "O exemplo mostra '(#1, #2)' para a entrada repetida.", None, "nomes das condições")
caso("C4-D08", D, "X03", E3, "Sem --z3.", T_REP,
     "Cada aparição tem par próprio.",
     "A informação de par de independência é relatada separadamente para p#1 e para p#2 (uma entrada de par por aparição).",
     "'cada aparição é [uma] condição [com] par próprio'. Não se afirma se o par existe (critério em conflito, ver I18), "
     "apenas que é tratado por aparição.", None, "pares por condição")
caso("C4-D09", D, "X04", E6, "Nenhuma opção de variante.", T_MASK,
     "Mascaramento é a variante padrão.",
     "A análise é feita na variante mascaramento (MC/DC de mascaramento).",
     "Comentário do exemplo: '[MC/DC de] mascaramento (padrão) [e] causa única'.", None, "variante relatada")
caso("C4-D10", D, "X05", E6 + " --unique-cause", "Opção --unique-cause.", T_MASK,
     "--unique-cause seleciona a variante causa única.",
     "A análise é feita na variante causa única.", "Exemplo com --unique-cause no mesmo comentário.", None, "variante relatada")
caso("C4-D11", D, "X04+X05", E6, "Mesma expressão nas duas variantes; sem --z3.", T_SUB,
     "Todo par de causa única vale no mascaramento.",
     "Todo par de independência relatado na variante causa única (X05) também é par válido relatado na variante mascaramento (X04) para a mesma condição.",
     "IndependencePairsTest: 'todo par [de] causa única vale [no] mascaramento'. Relação entre variantes, não depende do "
     "critério em conflito.", "Q07: existe par de causa única para p, q e r.", "conjunto de pares por condição nas duas variantes")
caso("C4-D12", D, "X04", E6, "Mascaramento; sem --z3.", T_DIAG + " ; " + T_DIAG2 + " ; " + T_PAIRS + " ; " + T_SIMPL,
     "Só condição sem par recebe diagnóstico (redundante/bloqueada).",
     "Nenhuma condição de (p and q) or r é diagnosticada como redundante ou bloqueada; todas têm par.",
     "Nas duas leituras conflitantes do critério (passo 3 x 'critério simplificado') todas as condições têm par (Q07 sat "
     "para par que muda a decisão, o que também satisfaz a mudança isolada); nas duas leituras do diagnóstico só condição "
     "sem par é classificada. O conflito não altera o resultado aqui.", "Q07: sat para p, q, r.", "diagnóstico por condição")
caso("C4-D13", D, "X05", E6, "Causa única; sem --z3.", T_DIAG + " ; " + T_DIAG2 + " ; " + T_PAIRS,
     "Idem para causa única.",
     "Nenhuma condição é diagnosticada como redundante ou bloqueada; todas têm par de causa única.",
     "Q07 mostra par de causa única (só a condição muda e a decisão muda) para p, q e r.", "Q07: sat.", "diagnóstico")
caso("C4-D14", D, "X06", DFRS, "Sem --z3.", T_DFRS,
     "Comparações e o operador DFRS /\\ são aceitos; cada comparação é uma condição.",
     "A expressão é aceita (analisada, não recusada) com 2 condições: speed > 100 e mode = idle.",
     "O exemplo apresenta o comando como uso válido de comparações e operadores DFRS; ExpressionParserTest lista "
     "'comparações, operadores [de] DFRS' como suportados.", None, "aceitação e condições")
caso("C4-D15", D, "X06", DFRS, "Sem --z3.", T_TT,
     "2^n sobre as comparações distintas.",
     "4 combinações.",
     "Duas condições distintas; a tabela de regressão confirma que cada comparação distinta conta como entrada (Q05: VM "
     "21 condições/152 combinações = soma de 2^(comparações distintas)).", "Q05-vm-aritmetica: sat.", "combinações")
caso("C4-D16", D, "X07", E4 + " --constraint \"not p or q\"", "Restrição escrita à mão; sem --z3.", T_RESTR + " ; " + T_RESTR2,
     "Combinações que violam a restrição são excluídas da análise.",
     "Das 8 combinações, exatamente 2 são tratadas como impossíveis/excluídas (p=V,q=F,r=V e p=V,q=F,r=F) e 6 são aceitas.",
     "O comentário traduz a restrição como implicação A=>B ('not A or B'); as linhas aceitas são as que satisfazem a "
     "restrição (EngineDetailsTest: 'só linhas aceitas [pela] restrição'). A restrição manual não é resultado do Z3, logo o "
     "conflito sat/unsat (I09) não se aplica.", "Q02: 2 linhas violam (sat de not restricao).", "linhas impossíveis/aceitas")
caso("C4-D17", D, "X07", E4 + " --constraint \"not p or q\"", "Idem.", T_SUB,
     "Linhas impossíveis nunca entram nos pares.",
     "Nenhum par de independência relatado usa uma combinação com p=V e q=F.",
     "IndependencePairsTest: 'linhas impossíveis nunca entram'.", "Q02.", "linhas usadas pelos pares")
caso("C4-D18", D, "X08", "p and (q or r", "Parêntese não fechado.", T_INV,
     "Expressões inválidas são recusadas.",
     "A expressão é recusada: nenhuma análise (tabela, pares, suíte) é produzida e a ferramenta sinaliza erro.",
     "ExpressionParserTest: 'expressões inválidas recusadas'. Parêntese desbalanceado é inválido em qualquer gramática "
     "compatível com os exemplos. O código de saída exato não é documentado (I23) e não é exigido.", None, "recusa / ausência de análise")
caso("C4-D19", D, "X09", "p and or q", "Operador sem operando.", T_INV,
     "Expressões inválidas são recusadas.",
     "A expressão é recusada: nenhuma análise é produzida e a ferramenta sinaliza erro.",
     "Idem; operador binário sem operando esquerdo é inválido.", None, "recusa")
caso("C4-D20", D, "X10", "exemplos/requisitos.mcdc", "Arquivo citado como 'elos/requisitos.mcdc' (caminho degradado; "
     "único candidato no repositório é exemplos/requisitos.mcdc, que contém REQ-003).", T_FILE + " ; " + T_FILE2,
     "Arquivo .mcdc com vários requisitos, comentários e identificador por linha.",
     "São analisados exatamente 3 requisitos, identificados REQ-001, REQ-002 e REQ-003; a linha de comentário não vira requisito.",
     "O texto afirma suporte a vários requisitos por arquivo, comentários e linha com identificador; o conteúdo é a entrada.",
     None, "requisitos analisados")
caso("C4-D21", D, "X10", "REQ-001: (alarme_ativo and porta_aberta) or botao_emergencia", "Sem --z3.", T_TT,
     "2^n combinações; cada aparição é condição.", "REQ-001: 3 condições e 8 combinações.", "Regras dos passos 1 e de aparição.",
     "Q03-REQ-001.", "condições e combinações por requisito")
caso("C4-D22", D, "X10", "REQ-002: porta_fechada and not obstaculo", "Sem --z3.", T_TT,
     "Idem.", "REQ-002: 2 condições e 4 combinações.", "Idem.", "Q03-REQ-002.", "condições e combinações")
caso("C4-D23", D, "X10", "REQ-003: freio_acionado or (freio_acionado and pedal_pressionado)", "Sem --z3.", T_TT + " ; " + T_REP,
     "Idem, com entrada repetida.", "REQ-003: 3 condições (freio_acionado#1, freio_acionado#2, pedal_pressionado) e 4 combinações.",
     "2 entradas distintas -> 4 combinações; 3 aparições -> 3 condições.", "Q03-REQ-003.", "condições e combinações")
caso("C4-D24", D, "X10", "REQ-001", "Sem --z3; variante padrão.", T_DIAG + " ; " + T_DIAG2 + " ; " + T_SIMPL,
     "Só condição sem par é diagnosticada.", "Nenhuma condição de REQ-001 é diagnosticada como redundante ou bloqueada.",
     "Nas duas leituras do critério todas as condições de REQ-001 têm par (Q03: A=sat e B=sat).", "Q03-REQ-001.", "diagnóstico")
caso("C4-D25", D, "X10", "REQ-002", "Sem --z3; variante padrão.", T_DIAG + " ; " + T_DIAG2 + " ; " + T_SIMPL,
     "Idem.", "Nenhuma condição de REQ-002 é diagnosticada como redundante ou bloqueada.", "Q03-REQ-002: A=sat e B=sat.",
     "Q03-REQ-002.", "diagnóstico")
caso("C4-D26", D, "X11", "experimento/entradas/erro-sintaxe.mcdc (erro na linha 3)", "Arquivo próprio no formato do exemplo; "
     "linha 3 com parêntese não fechado.", T_FILE2 + " ; " + T_LINE + " ; " + T_INV,
     "Erro de sintaxe em requisito é recusado e o erro informa o número da linha.",
     "O arquivo é recusado com erro que menciona a linha 3.",
     "RequirementsFileTest: 'erro [de] sintaxe [no] requisito'; InputEdgeCasesTest: 'número [da] linha [no] erro' "
     "(item da leitura de entradas, sem restrição de formato).", None, "mensagem de erro")
for idx, (sid, x, nreq, ncond, ncomb) in enumerate([("vm", "X12", 5, 21, 152), ("tis", "X13", 17, 69, 268), ("npp", "X14", 11, 29, 76)]):
    base = 27 + 3 * idx
    pre = "Entrada exemplos/%s-decisoes.json citada pela fonte; sem --z3." % sid
    just = ("Tabela 'Números travados [em] regressão'. Requisitos, condições e combinações não dependem da regra de "
            "impossibilidade (combinações = total 2^n; o Z3 só marca impossíveis), e a contagem própria confere com a tabela (Q05).")
    caso("C4-D%02d" % base, D, x, "exemplos/%s-decisoes.json" % sid, pre, T_REGCAB + " ; " + T_REG,
         "Número de requisitos travado na regressão.", "%d requisitos (decisões) analisados." % nreq, just,
         "Q05-%s-aritmetica: primeira consulta sat." % sid, "requisitos")
    caso("C4-D%02d" % (base + 1), D, x, "exemplos/%s-decisoes.json" % sid, pre, T_REGCAB + " ; " + T_REG,
         "Número de condições travado.", "%d condições no total." % ncond, just, "Q05-%s." % sid, "condições")
    caso("C4-D%02d" % (base + 2), D, x, "exemplos/%s-decisoes.json" % sid, pre, T_REGCAB + " ; " + T_REG + " ; " + T_TT,
         "Número de combinações travado.", "%d combinações no total." % ncomb, just, "Q05-%s." % sid, "combinações")
caso("C4-D36", D, "X15", "exemplos/decisoes.json --format json", "Sem --z3.", T_JSON + " ; " + T_JSON2,
     "--format json gera relatório JSON.", "A saída do relatório é JSON válido (analisável).",
     "O exemplo usa '--format json' para gerar 'relatorio.json'; JsonReportTest descreve o conteúdo JSON.", None, "JSON válido")
caso("C4-D37", D, "X15", "exemplos/decisoes.json --format json", "Sem --z3.", T_JSON,
     "Relatório JSON rastreia o resultado de cada decisão.",
     "O JSON contém um resultado para cada uma das 4 decisões do arquivo, identificado pela decisão (id the_coffee_machine_system#1..#4 ou requisito REQ-001..REQ-004).",
     "JsonReportTest: 'Rastreabilidade [do] resu[ltado de] cada decisão'.", None, "decisões no JSON")
caso("C4-D38", D, "X16", "decisoes.json + testes.csv", "Teste T4 da decisão #3: mode=idle, button=true, coin=false, esperado T.",
     T_CHECK + " ; " + T_CHECK2, "A avaliação de testes existentes detecta resultado esperado errado.",
     "T4 é apontado como teste com resultado esperado errado (a guarda vale F nesses valores, o CSV diz T).",
     "TestSetEvaluationTest: 'resultado esperado errado'; a guarda (choice/\\button) \\/ coin vale F com os valores de T4.",
     "Q04-T4: guarda F (unsat/sat).", "testes com esperado divergente")
caso("C4-D39", D, "X16", "decisoes.json + testes.csv", "T1, T2, T3.", T_CHECK2,
     "Só testes com esperado divergente são apontados.",
     "T1, T2 e T3 não são apontados como resultado esperado errado.",
     "O esperado de T1 (T), T2 (F) e T3 (T) coincide com o valor da guarda nos valores concretos.", "Q04-T1..T3.", "testes com esperado divergente")
caso("C4-D40", D, "X16", "decisoes.json + testes.csv", "Decisão #1 com T1 e T2.", T_CHECK2 + " ; " + T_PAIRS + " ; " + T_SIMPL,
     "A avaliação aponta o que falta para MC/DC.",
     "A decisão the_coffee_machine_system#1 não é dada como coberta: falta par para a condição the_system_mode = idle.",
     "the_system_mode = idle é verdadeira em T1 e T2; sem mudança da condição não há par em nenhuma leitura do critério.",
     "Q04-cobertura: condição não muda.", "cobertura por decisão/condição")
caso("C4-D41", D, "X16", "decisoes.json + testes.csv", "Decisão #3 com T3 e T4.", T_CHECK2 + " ; " + T_PAIRS + " ; " + T_SIMPL,
     "Idem.", "A decisão the_coffee_machine_system#3 não é dada como coberta: faltam pares para the_coffee_request_button = true e the_coin_sensor = true.",
     "Essas condições têm o mesmo valor em T3 e T4; não há par em nenhuma leitura.", "Q04-cobertura.", "cobertura")
caso("C4-D42", D, "X16", "decisoes.json + testes.csv", "Decisões #2 e #4 sem testes no CSV.", T_CHECK2,
     "Idem.", "As decisões the_coffee_machine_system#2 e #4 não são dadas como cobertas (nenhum teste).",
     "Sem testes não há par para nenhuma condição.", "Q04-cobertura: 0 testes.", "cobertura")
caso("C4-D43", D, "X17", E7 + " --mutation", "Sem --z3.", T_MUT + " ; " + T_MUT2,
     "A mutação avalia seis tipos de defeito.", "O relatório de mutação cobre os seis tipos ORF, ENF, VNF, MVF, VRF e ASF (cada tipo aparece no relatório).",
     "Passo 6 lista os seis tipos avaliados. Quantidades por tipo não são documentadas.", None, "tipos de mutante relatados")
caso("C4-D44", D, "X18", "E5 = " + E5, "20 entradas distintas; sem --z3.", T_LIM + " ; " + T_LIM2 + " ; " + T_TT,
     "Limite de 20 entradas na tabela-verdade completa (cerca de 1 milhão de combinações).",
     "A expressão é aceita e analisada com 1048576 combinações.",
     "20 está dentro do limite documentado; 2^20 = 1048576 ('cerca [de] 1 milhão').", "Q06: sat.", "aceitação e combinações")
caso("C4-D45", D, "X18", "E5", "Idem.", T_LIM2,
     "No máximo 1000 pares guardados por condição.",
     "Para a condição x01 são guardados/relatados no máximo 1000 pares, embora existam mais de 1000 candidatos.",
     "'1000 pa[re]s guardados [por] condiç[ão]'. x01 tem 2^19-1 pares de causa única (Q06), muito acima do limite em qualquer leitura.",
     "Q06: pares_x01 > 1000 sat; <= 1000 unsat.", "quantidade de pares de x01")

# ------------------------------------------------------------------ INDETERMINADOS
def ind(id_, trecho, motivo, entrada="-"):
    caso(id_, I, None, entrada, "-", trecho, "-", "Sem expectativa única.", motivo)


ind("C4-I01", T_MASK, "Omissão: a expressão literal '( and B) or C' tem operando ausente e nenhum resultado é declarado; "
    "reconstruir o identificador seria acrescentar semântica.", "( and B) or C [--unique-cause]")
ind("C4-I02", T_REP, "Omissão: '( and B) or (not  and C)' com operandos ausentes; nenhum resultado declarado.", "( and B) or (not  and C)")
ind("C4-I03", T_RESTR, "Omissão: expressão ' or (B and C)' e restrição 'not  or B' com operandos ausentes.", "\" or (B and C)\" --constraint \"not  or B\"")
ind("C4-I04", T_MUT2, "Omissão: expressão ' and (B or C)' com operando ausente; resultados de mutação não declarados.", "\" and (B or C)\" --mutation")
ind("C4-I05", T_EXACT + " ; " + T_SUITE, "Omissão (operandos ausentes) e conflito: o exemplo diz 5 testes com --exact contra 6 "
    "da gulosa, mas a 'Garantia de minimização' diz que a gulosa sempre é mínima e --exact usa a mesma heurística e pode "
    "retornar suíte maior.", "(( or D) and (not  or D)) or B --exact")
ind("C4-I06", T_MIN, "Omissão: exemplos '( ∧ B) ∨ C' e ' ∧ ¬B' com operando ausente.", "( ∧ B) ∨ C ; ∧ ¬B")
ind("C4-I07", T_FMT, "Conflito: truth-csv é descrito como tabela-verdade inteira e, na 'Regra de saída', como 'somente "
    "[...] independência, nunca tabela-verdade'. O texto não resolve.", "--format truth-csv")
ind("C4-I08", T_FMT, "Conflito: csv é a suíte (uma linha por teste) e, na 'Regra de saída', o único formato com a "
    "tabela-verdade completa.", "--format csv")
ind("C4-I09", T_Z3 + " ; " + T_Z3B + " ; " + T_REG, "Conflito: o passo 2 diz unsat = impossível; a 'Regra de satisfatibilidade' "
    "inverte (sat = impossível) e se declara prevalente para todas as operações, mas a tabela de regressão (4/4/1 impossíveis) "
    "só é compatível com a leitura original (Q05: unsat = 4/4/1; sat = 148/264/75). O texto não diz qual afirmação prevalece "
    "sobre os números medidos.", "--z3 (qualquer entrada)")
ind("C4-I10", T_REG, "Conflito/omissão: 'Testes' 26/80/40/146 dependem das combinações excluídas pelo Z3 (I09) e as "
    "opções usadas para medi-los não são informadas.", "vm/tis/npp")
ind("C4-I11", T_REG + " ; " + T_MUT, "Omissão/conflito: Mutantes/Equivalentes/Pegos dependem da suíte gerada com Z3 (I09) e "
    "das opções não informadas; não está definido se o total inclui equivalentes (TIS: 428+21 != 450).", "vm/tis/npp --mutation")
ind("C4-I12", T_REG + " ; " + T_Z3B + " ; " + T_ARQ, "Conflito: 'Conflitos' (0/3/1) do verify dependem de satisfatibilidade, "
    "e a regra invertida 'vale [para] todas as operações'; além disso, a arquitetura do Z3 é contraditória.",
    "verify --json exemplos/npp-decisoes.json (e vm/tis)")
ind("C4-I13", "L61-65 (verify ... --cotnext 'the_system_mode = preparing_weak') ; L355 'lacnas só contexto'",
    "Conflito I09/I21 sobre o uso do Z3 e nenhum resultado declarado para a lacuna.", "verify --context")
ind("C4-I14", "L33-35 '--z3 --boundary' ; L235 NumericOracleTest", "Omissão: a regra de valores de fronteira não é definida; "
    "conflito I09.", "--z3 --boundary")
ind("C4-I15", "L57-59 '--direct' ; L237 Z3RandomizedTest ; L353", "Conflito I09/I21: o modo direto depende do Z3; a "
    "comparação com a tabela (com ou sem impossíveis) não é especificada.", "--direct")
ind("C4-I16", T_SUITE + " ; " + T_EXACT, "Conflito sobre --exact (mínimo pelo Z3 x mesma heurística sem garantia).", "--exact")
ind("C4-I17", T_SUITE + " ; L101 'suíte pode ter N + 1 tests'", "Conflito sobre minimalidade da gulosa e omissão: o tamanho "
    "da suíte para expressões próprias não é declarado ('pode ter N+1').", "tamanho da suíte")
ind("C4-I18", T_PAIRS + " ; " + T_SIMPL + " ; " + T_SUB, "Conflito: passo 3 exige que a decisão mude; o 'critério "
    "simplificado' admite decisão igual; 'condição sem efeito fica sem par' contradiz o simplificado. Q03-REQ-003 mostra "
    "que as leituras divergem (pedal_pressionado: A=unsat, B=sat).", "pares de condições sem efeito")
ind("C4-I19", T_FILE + " ; " + T_DIAG + " ; " + T_DIAG2 + " ; " + T_SIMPL, "Conflito: 'REQ-003 tem [uma] condição redundante' "
    "x critério simplificado (Q03: pedal_pressionado tem mudança isolada) x 'classificação inversa' (rótulos "
    "intercambiáveis).", "REQ-003 de exemplos/requisitos.mcdc")
ind("C4-I20", T_DIAG + " ; " + T_DIAG2, "Conflito: redundante e bloqueada têm definições opostas e são declaradas "
    "intercambiáveis.", "rótulo de diagnóstico")
ind("C4-I21", T_ARQ + " ; L349 'aviso   Z3 falta'", "Conflito: Z3 como processo externo no PATH x implementação "
    "interna Java x biblioteca nativa na JVM; comportamento sem Z3 no PATH não determinado.", "--z3 sem z3 no PATH")
ind("C4-I22", T_ARQ + " ; L357 'Z3 travado limite teempo encerra  prosso'", "Conflito: limite de 60 s encerra o processo x "
    "'apenas estimativa [...] nunca encerra'.", "Z3 lento")
ind("C4-I23", "L367 '| `MainTest`| 14 |  três comandos,  fontes,  formeeatos,  cdigo saída 0, 1  2, entadas inválidas |'",
    "Omissão: o significado dos códigos de saída 0, 1 e 2 não é documentado.", "códigos de saída")
ind("C4-I24", T_LIM + " ; " + T_LIM2, "Omissão: o comportamento acima dos limites (21 entradas na tabela, >12 Z3 linha a "
    "linha, >30 modo direto) não é descrito.", "21 entradas")
ind("C4-I25", T_REGCAB, "Omissão: 'Completos' (14 de 17 no TIS) não é definido.", "coluna Completos")
ind("C4-I26", "L337 '| `Nat2TestJsonReaderTest`| 4 | JSON  NATEST, gura temporal, arquivos inváidos, ids reetidos |'",
    "Omissão: o resultado para arquivo inválido e ids repetidos não é declarado.", "JSON NAT2TEST inválido / ids repetidos")
ind("C4-I27", "L339 '| `TestCasesFileTest`| 4 | CSV tests,   couna decsão; colnas faltando |'", "Omissão/ambiguidade: "
    "'[com/sem] coluna decisão' perdeu a palavra; resultado para colunas faltando não declarado.", "CSV de testes malformado")
ind("C4-I28", "L337 'gura temporal' ; L413 'Guards temporais: ferramenta analisa  passo iolado'", "Omissão: tratamento do campo "
    "temporal (decisoes.json #2) não é descrito.", "guarda temporal")
ind("C4-I29", T_MUT, "Omissão: os operadores de mutação não são definidos; não há como saber quais mutantes são "
    "equivalentes para conferir a exclusão da contagem.", "mutantes equivalentes")
ind("C4-I30", "L323 MutationReportTest ; L407-409 (parênteses deslocados x 'Garantia de parênteses')", "Conflito e omissão: "
    "parênteses deslocados é 'único tipo sem garantia' x 'MC/DC garante [...] qualquer alteração de parênteses'; o texto não "
    "associa 'parênteses deslocados' a um dos seis códigos.", "--mutation --unique-cause")
ind("C4-I31", T_JSON2, "Omissão: '- relatorio.json' está degradado; não se sabe se é opção de arquivo de saída.", "saída em arquivo")
ind("C4-I32", "L249-269 (tempos e limites de desempenho)", "Ambiguidade ('Tempos medidos [com/sem] contar partida Java') e "
    "dependência do ambiente/instrumentação.", "tempo de execução")
ind("C4-I33", "L371 '| `CsvReportTest`| 2 |  linha  teste  enrada; aspas célas vírgula |'", "Omissão: quais células podem "
    "conter vírgula não é dito; e o conteúdo do csv está em conflito (I08).", "aspas no CSV")
ind("C4-I34", T_SUITE + " ; L319 'Odem escolha (menos paes primeiro); sugestão  par barato'", "Conflito: composição da suíte "
    "depende do critério de par (I18) e da garantia de minimização (I16).", "ordem/desempate da gulosa")
ind("C4-I35", T_ROW0, "Omissão: só a linha 0 é definida; a ordem das demais linhas não é descrita.", "ordem das linhas")
ind("C4-I36", T_INV, "Omissão: 'Prcedência  )' perdeu o conteúdo; a precedência entre and/or não é declarada "
    "(ex.: 'p or q and r').", "p or q and r")
ind("C4-I37", "L349 'enumerações, booleanos, reais negats'", "Omissão: resultado esperado para reais negativos não é "
    "declarado (e depende de Z3, I09).", "reais negativos")

oraculo = {
    "condicao": "C4",
    "fonte": "experimentacao-pesquisa/experimentacao-4/tool-readme-C4.md",
    "sha256_fonte": "D6BC0A588CD9A7DF7F1F566573944FA5CB1707BBA676B4E9854CAD2CC5440FC2",
    "prompt": "experimentacao-pesquisa/prompts/geracao-de-oraculos-v3.md",
    "unidade_de_contagem": "caso do oráculo (ID estável C4-Dnn / C4-Inn); uma execução Xnn pode ser julgada por vários casos",
    "expressoes_proprias": {"E1": E1, "E2": E2, "E3": E3, "E4": E4, "E5": E5, "E6": E6, "E7": E7, "DFRS": DFRS},
    "execucoes": EXECUCOES,
    "nota_execucoes": NOTA_EXEC,
    "casos": casos,
    "totais": {"determinados": sum(1 for c in casos if c["status"] == D),
               "indeterminados": sum(1 for c in casos if c["status"] == I)},
}
with open(os.path.join(AQUI, "oraculo.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(oraculo, f, ensure_ascii=False, indent=1)

md = ["# Inventário do oráculo C4", "",
      "Gerado por `construir_oraculo.py` a partir da fonte C4 (SHA-256 `%s`), antes de ler o SUT." % oraculo["sha256_fonte"],
      "Trechos literais copiados com a degradação original; `Lnn` = linha da fonte.", "",
      "Determinados: %d. Indeterminados: %d." % (oraculo["totais"]["determinados"], oraculo["totais"]["indeterminados"]), "",
      "## Execuções planejadas", "", NOTA_EXEC, "", "| Execução | Comando (termos da fonte) |", "|---|---|"]
for k, v in EXECUCOES.items():
    md.append("| %s | `%s` |" % (k, v["comando"].replace("|", "\\|")))
md += ["", "## Casos", ""]
for c in casos:
    md.append("### %s — %s" % (c["id"], c["status"]))
    md.append("")
    for k, rot in [("execucao", "Execução"), ("entrada", "Entrada"), ("precondicao", "Pré-condição"),
                   ("trecho_literal", "Trecho literal"), ("regra", "Regra"), ("expectativa", "Expectativa"),
                   ("justificativa", "Justificativa"), ("evidencia_z3", "Evidência Z3"), ("observavel", "Observável")]:
        if c.get(k):
            md.append("- **%s:** %s" % (rot, c[k]))
    md.append("")
with open(os.path.join(AQUI, "inventario-oraculo.md"), "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(md))
print(oraculo["totais"])
