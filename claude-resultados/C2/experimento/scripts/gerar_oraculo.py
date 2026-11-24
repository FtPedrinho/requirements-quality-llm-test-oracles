# -*- coding: utf-8 -*-
"""Oráculo documental da condição C2 (gerado antes de qualquer leitura do SUT).

Fonte normativa exclusiva: experimentacao-pesquisa/experimentacao-2/documentation/tool-readme-C2.md
SHA-256 61C4062B5FC6B4F364F40465B0E017C80E0FA0C5433412EB2E925C545F6EFBE1.

Os trechos são citados LITERALMENTE da fonte (inclusive com as letras e palavras
ausentes do texto C2), com o número da linha. "Leitura" registra a reconstrução
usada e por que ela é única no próprio texto; quando não é única, o caso é
INDETERMINADO.

Convenções dos comandos: {EX} = exemplos/ do repositório; {ENT} = experimento/entradas;
{OUT} = pasta da rodada para arquivos gravados com -o; {G:nome} = expressão de
entradas/expressoes-geradas.json.
"""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

D, I = "DETERMINADO", "INDETERMINADO"

T_EXIT = ("L139", "**Cigo  saída:** `0`: comndo concluido  apontr os prblemas dscrtos pra  cdgo `2`; `1`: entraa invalida; `2`: resutado vido  processamto,  com  condição  par  `analyze`,  codição não demonstrda ou um resutado espero divergente  `check`,   cnfito ou uma lcuna no `verify`.")
LEIT_EXIT = ("0 = comando concluído sem apontar os problemas do código 2; 1 = entrada inválida; 2 = resultado válido "
             "com condição sem par (analyze), condição não demonstrada ou resultado esperado divergente (check), "
             "conflito ou lacuna (verify). 'condição  par' lido como 'condição sem par': o próprio texto usa 'sem par' "
             "como o problema de analyze (L39 'cada cond   ição sem par', L461 'condições sem par'); 'com par' tornaria o "
             "código 2 o resultado de toda análise, contra a definição do código 0.")
T_VAR = ("L55", "duas variants  MC/DC  supordas: **mascaramento** (pdrão) e **causa úica** (`--unique-cause`). Nesa documentaço, entraa é  variavel dstinta  expresão; condição é cada ocorencia   entrada  expressão.")
T_PAIR = ("L283", "→ 3. pares  independência:   condição,  procurds dois tests possíveis   essa conição muda,  resultado  decisão  muda   condição satisfaz  critério da variante de MC/DC selecionaa")
T_CU_MASK = ("L491", "| `IndependencePairsTest` | 8 | Pres em ,   não; condiço  efio fica  par;  par  causa única vale  mascaramento; lnhas impssiveis nuna entrm; pares  apariço |")
LEIT_CU = ("Causa única: par em que só a condição avaliada muda e o resultado muda (sentido do nome da variante; "
           "a fonte cita Chilenski). L491: um par de causa única vale também no mascaramento; logo, existência de par "
           "de causa única (verificada no Z3) implica condição com par nas duas variantes. A definição do mascaramento "
           "não está escrita na fonte: ausência de par no mascaramento não é derivável, só presença.")
T_DIAG = ("L287", "→ 5. diagnóstico:   condição não possui par mesmo considerando tods  combinações, é classificada  redundante;  dixa  possur pares  causa  combinações impossíveis,  classificada como bloqueada")
T_MINSUITE = ("L493", "| `MinimalSuiteTest` | 4 | Exmplos conhecdos (( ∧ B) ∨ C  4 testes, A ∧ ¬B  3); par que demnstra  condção; empte prefre causa úica |")
T_OPS = ("L127-L137", "| Operadr | Frmas acets | ... |  | `and`, `&&`, `/\\` | |  | `or`, `\\|\\|`, `\\/` | | não | `not`, `!` | | comparção | `=`, `==`, `!=`, `<`, `<=`, `>`, `>=` |")
T_EXACT = ("L111", "| `--exact` | Suíe exata:  menro possivel, esclhida pelo Z3 |")
T_Z3 = ("L109", "| `--z3` | Usa o Z3 pra dscobrir cominaçoes impossiveis  dar valoes concretos; acim  12 entradas, passa soznho  modo dreto |")
T_HOW2 = ("L281", "→ 2. combinações impossíveis (  Z3 é utilizado): as combinaçes  verificaas  Z3;  que retornam `unsat`  consideradas impossíveis e não participam da análse")
T_HOW1 = ("L279", "→ 1. tabela-verdade: para  entradas distintas  expressão, são consideradas  2ⁿ combinações  calculado  resultado da guada em cada ")
T_REG = ("L461", "| `RequirementsRegressionTest` | 3 | Verifca se  resutados  três sistes  emplo permancem iais  vales regstrados  requisitos, condições, combinaçoes, combinaçoes impossiveis, testes, condições sem par, mutants (ttal, equivalents  detectdos)  confltos.  busca eata   varnte  caua únca produzem o mesom nmero de tetes nses exmplos. Pra  requisito cpleto,  quantdade regstrada  testes correspnde  nmro  condições  1. |")
T_NUM = ("L467-L477", "| Sistma | Requisitos | Cmpletos | Condições | Combinaçoes | Impossiveis | Testes | Mutants | Equivalents | Pegos | Confltos | ... | VM · máqina  café | 5 | 5 | 21 | 152 | 4 | 26 | 152 | 0 | 152 | 0 | | TIS · pisca-psca | 17 | 14 | 69 | 268 | 4 | 80 | 450 | 21 | 428 | 3 | | NPP · injeço  sgurança | 11 | 11 | 29 | 76 | 1 | 40 | 146 | 0 | 146 | 1 |")
T_CONC = ("L463", "| `ReportsContentTest` | 6 |  JSON,  texto   CSV dizem o   clculado,  três comnos.  todos os testes gerdos pra  sistems de exmplo, inclusve   frnteira,  valoes concrtos ralizam  combinaçao dclarada   resuado esperdo  o que  guarda dá. |")
T_BOUND = ("L43", "| Testes  frnteira | `--z3 --boundary` | Variaçes  lmite  cada comparção (`speed > 100` → 100  101) |")
T_CONS = ("L107/L231", "| `--constraint \"<expr>\"` | Rtrição etre condições escrta  mão (  expressão dreta) | ... # restrição escita  mão: A = speed > 100 impica B = speed > 50 / ./mcdc analye \" or (B and C)\" --constraint \"not  or B\"")
T_DIRECT = ("L113/L419", "| `--direct` | Pares pedds dreto  Z   3,  mnar a tabela ( 30 entradas) | ...  120 expressões,  modo dreto dá  mesam cobertura   mesom dignstio  a tabea-verdae cmpleta.")
T_LIM = ("L293/L587", "Os limtes documentads :  20 entradas   tabela-verdade cmpeta, 12 entradas  processanto  Z3 linha a linha  30 entradas  modo dreto. / - **Tamnho:** 20 entrdas   taela-verdade cmpleta (cerca  1 mlhão  combinços), 12  o Z3 linha a linha  30 no modo dreto;  1000 pares guardads por condição.")
T_FMT = ("L121", "| `--format <formato>` | `text` (pdrão), `json`, `csv` (suíte)  `truth-csv` (tabela-verdade intea); `check` e `verify` acetam `text` e `json` |")
T_OUTS = ("L201-L207", "| `json` | Reutado cmpleto de cada decião, lgdo  rquisito  orgem (fomato  integrção) | | `csv` |  suíte:  liha por tste  enrada,  o reutado esperdo,   o tese demnstra   valoes concetos | | `truth-csv` | A tabela-verdade intea,   combinaçoes impssiveis marcads |")
T_O = ("L123", "| `-o <arquivo>` | Grava  relatorio  arqivo  vez  mostrr  tela |")
T_MCDC = ("L143", "**Arqivo `.mcdc`:** um requisito  linha, `ID: expressão`. Lnhas com `#`  comentrios.")
T_REQ3 = ("L241-L243", "# város requisitos de um arquivo; REQ-003 tem  condião redundante / ./mcdc analyze -f exeplos/requisitos.mcdc")
T_CHECK = ("L51", "| Avalar teses existntes | `mcdc check` | Cobertura MC/DC  um cnjunto  testes,  que falta  testes  resutado esperdo errdo |")
T_CSV = ("L183", "**Teses existntes** (pra  comndo `check`), em CSV: cada lina asocia  teste   entrada e ao valor atrbuído   entrada. O valr pode ser lgico (`T`/`F`) ou cncreto, confore  tipo da variavel. As colunas `decision`  `expected_outcome` são opcionis.")
T_VERIFY = ("L53/L119", "| Revsar  requisios  si | `mcdc verify` | Confltos (dois requistos valem jtos  escrvem valoes diferetes) e lacunas (nnum requisito vale) | ... | `--context \"<expr>\"` | No `verify`: confre se, nssa suação, smre algma guarda vale |")
T_ACTION = ("L503", "| `ActionTest` | 2 | Leura  aões `x := v`; contrdção só  valoes diferetes  mesam vaiavel |")
T_NOZ3 = ("L73", " scrpt `./mcdc` execta  feraemta  prtir  class  compildas.   Z3, continum disponiveis  recurss que não dependm dele. As opçoes  exgem  Z3 avisam qndo o executvel não está instaldo.")
T_MUT = ("L289/L117", "→ 6. mutação (opional): são avaliados seis tipos  defeto  Kapoor e Boen (ORF, ENF, VNF, MVF, VRF, ASF); versões equivalentes  requisito original não entram  contgem / | `--mutation` | Confre   suíte pega verses  requisito   defito |")
T_TT0 = ("L485", "| `TruthTableTest` | 8 |  liha por combinaçao;  linha 0  tudo verdadiro;  saída  cada linha; restriçes; lmite  20 entradas |")
T_PAR = ("L591", "- **Fórmus  mitas ocorencias rpetids  entradas:** o critéro MC   /DC pode exgir todas  combinaçoes posiveis. Por emplo, a fnção de paridde  3 entrdas exige 8 testes.")
T_PREC = ("L515", "| `ExpressionParserTest` | 9 | Precedênca ( ates de ), parêntses, comparções, operadres  DFRS; expressões inlidas recsads |")
T_EDGE = ("L523", "| `InputEdgeCasesTest` | 4 | Aspas  CSV, nmeo  lina com erro, sinal de menos só em númros |")
T_JSONR = ("L519", "| `Nat2TestJs   onReaderTest` | 4 | JSON  NAT2TEST, guarda teporl, arquivs invlidos, ids repetids |")
T_REQF = ("L517", "| `RequirementsFileTest` | 3 | Arqivo `.mcdc`, comentrios, linha sem identficador, erro  sintxe  o requisito |")
T_CSVT = ("L521", "| `TestCasesFileTest` | 4 | CSV  testes,  e  a coluna de decisão; colunas fltando |")
T_EXEX = ("L253-L255", "# suíe exata (aqui, 5 testes  vez  6 da escolha guloa) / ./mcdc analyze \"((E or D) and (not  or D)) or B\" --exact")
T_GREEDY = ("L285", "→ 4. esclha da suíte:  estratégia gulosa considera primeiro as condções   pars e esolhe pares  acrescentem  testes  suíe; em caso  empate, prioriza caua únca.  `--exact`,  Z   3 pocura  suíte de tamanho mnimo")
T_REP = ("L225-L227", "# entrada repetida:  aparião é  condição  par próprio (#1, A#2) / ./mcdc analze \"(A and B) or (not  and C)\"")
T_JSONF = ("L153", "**JSON  decisões** (fomato do Extractr  NAT2TEST): cotm  variavis  seus tips, alem das decisões,     guarda   ações.")

CASES = []


def C(id, cat, status, cmd, trechos, regra, expect, just, z3=(), z3env=True, diag=None, motivo=None):
    CASES.append({
        "id": id, "categoria": cat, "status": status, "comando": cmd,
        "pre_condicoes": {"z3_no_PATH_do_SUT": z3env},
        "trechos": [{"linha": t[0], "texto": t[1]} for t in trechos],
        "regra": regra, "expectativa": expect if status == D else None,
        "motivo_indeterminacao": motivo, "justificativa": just, "z3": list(z3),
        "diagnostico": diag,
    })


# ------------------------------------------------------------------ analyze
C("A01", "analyze", D, ["analyze", "(A and B) or C"], [T_MINSUITE, T_VAR, T_EXIT, T_CU_MASK],
  "Mascaramento padrão; exemplo conhecido (A∧B)∨C com 4 testes.",
  {"exit": 0, "tamanho_suite": 4, "todas_condicoes_com_par": True, "condicoes": 3},
  "L493 dá 4 testes para (A∧B)∨C. Z3 (Q01) encontra par de causa única para A, B e C; por L491 vale no "
  "mascaramento, logo nenhuma condição sem par e código 0. " + LEIT_EXIT, ["Q01-AB-or-C-pares", "Q15-exata-AB-or-C"])
C("A02", "analyze", D, ["analyze", "(A and B) or C", "--unique-cause"], [T_VAR, T_EXIT, T_PAIR],
  "Variante causa única aceita; toda condição com par de causa única.",
  {"exit": 0, "todas_condicoes_com_par": True},
  LEIT_CU + " Q01: sat para A, B, C.", ["Q01-AB-or-C-pares"])
C("A03", "analyze", D, ["analyze", "A and not B"], [T_MINSUITE, T_EXIT],
  "Exemplo conhecido A∧¬B com 3 testes.", {"exit": 0, "tamanho_suite": 3, "todas_condicoes_com_par": True},
  "L493 'A ∧ ¬B  3'. Q02: pares para A e B.", ["Q02-A-and-notB-pares", "Q18-exata-A-and-notB"])
C("A04", "operadores", D, ["analyze", "(A && B) || C"], [T_OPS, T_MINSUITE],
  "&& e || são formas aceitas de e/ou; resultado igual ao de A01.",
  {"exit": 0, "tamanho_suite": 4, "todas_condicoes_com_par": True, "equivalente_a": "A01"},
  "L131/L133: as formas de cada linha da tabela de operadores são equivalentes. A coluna do nome do operador está "
  "ilegível, mas cada linha agrupa and/&&//\\ e or/||/\\/ inequivocamente.", ["Q01-AB-or-C-pares"])
C("A05", "operadores", D, ["analyze", "(A /\\ B) \\/ C"], [T_OPS, T_MINSUITE],
  "/\\ e \\/ (DFRS) são formas aceitas de e/ou.",
  {"exit": 0, "tamanho_suite": 4, "todas_condicoes_com_par": True, "equivalente_a": "A01"},
  "Idem A04.", ["Q01-AB-or-C-pares"])
C("A06", "operadores", D, ["analyze", "A and !B"], [T_OPS, T_MINSUITE],
  "! é forma de 'não'.", {"exit": 0, "tamanho_suite": 3, "equivalente_a": "A03"},
  "L135: 'não | not, !'.", ["Q02-A-and-notB-pares"])
C("A07", "operadores", D, ["analyze", "speed > 100 /\\ mode = idle"], [T_OPS, ("L221-L223", "# comparações e  operadores do DFRS / ./mcdc analyze 'speed > 100 /\\ mode = idle'"), T_EXIT],
  "Comparações como condições; 2 condições, ambas com par.",
  {"exit": 0, "condicoes": 2, "todas_condicoes_com_par": True},
  "Q03: par de causa única para as duas comparações.", ["Q03-speed-mode-pares"])
C("A08", "operadores", D, ["analyze", "(x == 5) and (y != 3)"], [T_OPS, T_EXIT],
  "== e != aceitos.", {"exit": 0, "condicoes": 2, "todas_condicoes_com_par": True},
  "L137 lista = == != < <= > >=. Q04.", ["Q04-eq-ne-pares"])
C("A09", "operadores", D, ["analyze", "(a < 1) or ((b <= 2) and (c >= 3))"], [T_OPS, T_EXIT],
  "< <= >= aceitos.", {"exit": 0, "condicoes": 3, "todas_condicoes_com_par": True}, "Q05.", ["Q05-lt-le-ge-pares"])
C("A10", "entrada-repetida", D, ["analyze", "(A and B) or (not A and C)"], [T_VAR, T_REP, T_HOW1],
  "3 entradas, 4 condições A#1, B, A#2, C; tabela 2^3; cada aparição tem par próprio.",
  {"exit": 0, "entradas": 3, "condicoes": 4, "combinacoes": 8, "rotulos_condicoes_contem": ["A#1", "A#2"],
   "todas_condicoes_com_par": True},
  "L55 dá exatamente esta expressão e a contagem (3 entradas, 4 condições A#1, B, A#2, C). L225 afirma que cada "
  "aparição é condição com par próprio (rótulos '#1'/'A#2' parcialmente apagados, mas L55 os dá completos). "
  "L227 apaga a letra em '(not  and C)'; a expressão completa vem de L55. Q06: 8 combinações.", ["Q06-repetida-tabela"])
C("A11", "precedencia", I, ["analyze", "A or B and C"], [T_PREC],
  "Precedência entre e/ou.", None, "O operador que tem precedência foi apagado do texto.",
  motivo="L515 'Precedênca ( ates de )': os operadores foram apagados; a fonte não diz se and precede or ou o contrário, nem se a mistura é recusada.")
C("A12", "entrada-invalida", D, ["analyze", "(A and B"], [T_EXIT, T_PREC],
  "Expressão inválida (parêntese não fechado) é entrada inválida.", {"exit": 1},
  "L139: 1 = entrada inválida; L515 'expressões inválidas recusadas'.")
C("A13", "entrada-invalida", D, ["analyze", "A and"], [T_EXIT, T_PREC],
  "Expressão inválida (operando faltando).", {"exit": 1}, "Idem A12.")
C("A14", "operadores", D, ["analyze", "x > -3"], [T_EDGE, T_EXIT],
  "Sinal de menos em número é aceito.", {"exit": 0, "condicoes": 1, "todas_condicoes_com_par": True},
  "L523 'sinal de menos só em números': número negativo é forma aceita. Uma condição isolada tem par trivial (x>-3 T/F).")
C("A15", "operadores", I, ["analyze", "x > -y"], [T_EDGE],
  "Sinal de menos aplicado a identificador.", None, "",
  motivo="L523 só nomeia o tema 'sinal de menos só em números' numa lista de testes; não diz o que ocorre com '-y' (recusa com código 1, outra mensagem ou outra interpretação).")
C("A16", "paridade", D, ["analyze", "{G:paridade3}"], [T_PAR],
  "Paridade de 3 entradas exige 8 testes.", {"tamanho_suite": 8, "combinacoes": 8},
  "L591: 'a função de paridade de 3 entradas exige 8 testes'. A fórmula (forma normal disjuntiva canônica) é a "
  "escrita natural da paridade com os operadores da L127-L137; Q07: 8 combinações.", ["Q07-paridade-tabela"])
C("A17", "limites", D, ["analyze", "{G:e20}"], [T_LIM, T_EXIT],
  "Até 20 entradas na tabela-verdade completa.", {"exit": 0, "entradas": 20, "todas_condicoes_com_par": True},
  "L293/L587: limite de 20 entradas (inclusive) na tabela completa. Q08-e20: par de causa única para todas.", ["Q08-e20-pares"])
C("A18", "limites", I, ["analyze", "{G:e21}"], [T_LIM],
  "21 entradas sem --z3/--direct.", None, "",
  motivo="A fonte fixa o limite de 20 entradas, mas não diz o que ocorre acima dele (erro, código 1, troca de modo).")
C("A19", "modo-direto", D, ["analyze", "{G:e13}", "--z3"], [T_Z3, T_EXIT],
  "Com --z3 e mais de 12 entradas passa sozinho ao modo direto e conclui.",
  {"exit": 0, "entradas": 13, "todas_condicoes_com_par": True},
  "L109; L419 (modo direto com mesma cobertura e diagnóstico). Q08-e13.", ["Q08-e13-pares"])
C("A20", "modo-direto", D, ["analyze", "{G:e26}", "--direct"], [T_DIRECT, T_LIM, ("L429", "| `SystemsPerformanceTest` | 4 |   Z3, pelo camnho  linha  comndo:  sistma  emplo (analise  fronteras e mutção, busca exaa  verifcaçao  requisitos) abaio de 3 s,  o modo dreto com 26 entradas abaio  10 s |")],
  "Modo direto com 26 entradas (≤ 30).", {"exit": 0, "entradas": 26, "todas_condicoes_com_par": True},
  "L113/L293: até 30 entradas no modo direto; L429 cita 26 entradas. Q08-e26.", ["Q08-e26-pares"])
C("A21", "modo-direto", I, ["analyze", "{G:e31}", "--direct"], [T_LIM],
  "31 entradas no modo direto.", None, "", motivo="Acima de 30 entradas o comportamento não é descrito.")
C("A22", "diagnostico", D, ["analyze", "x > 5 and x > 3", "--z3", "--unique-cause"], [T_DIAG, T_HOW2, T_EXIT],
  "Condição que só perde par por combinações impossíveis é bloqueada.",
  {"exit": 2, "condicao_classificada": {"x > 3": "bloqueada"}, "condicao_com_par": ["x > 5"], "impossiveis": 1},
  LEIT_CU + " Q09-bloqueio-livre: x>3 tem par sem domínio; Q09-bloqueio-viavel: unsat com domínio (x>5 ∧ ¬x>3 "
  "impossível, Q09-bloqueio-tabela). L287 → bloqueada; condição sem par → código 2.",
  ["Q09-bloqueio-viavel", "Q09-bloqueio-livre", "Q09-bloqueio-tabela"])
C("A23", "modo-direto", D, ["analyze", "x > 5 and x > 3", "--direct", "--unique-cause"], [T_DIRECT, T_DIAG, T_EXIT],
  "Modo direto dá o mesmo diagnóstico da tabela.", {"exit": 2, "condicao_classificada": {"x > 3": "bloqueada"}},
  "L419: mesmo diagnóstico do modo tabela (A22).", ["Q09-bloqueio-viavel", "Q09-bloqueio-livre"])
C("A24", "diagnostico", D, ["analyze", "A or (A and B)", "--unique-cause"], [T_DIAG, T_EXIT],
  "Condição sem par mesmo com todas as combinações é redundante.",
  {"exit": 2, "condicao_classificada": {"B": "redundante"}},
  LEIT_CU + " Q10: B sem par de causa única em todas as combinações (unsat). Classificação de A#1/A#2 não é avaliada.",
  ["Q10-redundante-livre"])
C("A25", "restricao", D, ["analyze", "A or (B and C)", "--constraint", "not A or B"], [T_CONS, T_EXIT, T_CU_MASK],
  "Restrição escrita à mão exclui combinações que a violam; todas as condições mantêm par.",
  {"exit": 0, "suite_sem_combinacao": {"A": True, "B": False}, "todas_condicoes_com_par": True},
  "L231 explica a restrição como implicação A ⇒ B (A=speed>100, B=speed>50), ou seja combinações com A verdadeiro "
  "e B falso não existem. O exemplo literal tem letras apagadas (\" or (B and C)\", \"not  or B\"); a expressão usada "
  "é a reconstrução com A, a única letra citada no comentário. Q11: pares de causa única respeitando a restrição.",
  ["Q11-restricao-pares"])
C("A26", "restricao", D, ["analyze", "A and B", "--constraint", "not A or B", "--unique-cause"], [T_CONS, T_DIAG, T_EXIT],
  "Condição cujo único par viola a restrição fica bloqueada.",
  {"exit": 2, "condicao_classificada": {"B": "bloqueada"}},
  LEIT_CU + " Q12: B tem par sem restrição (sat) e não tem com ela (unsat) → bloqueada (L287).",
  ["Q12-restricao-bloqueio", "Q12-restricao-bloqueio-livre"])
C("A27", "z3", D, ["analyze", "speed > 100 or (speed > 50 and rain)", "--z3", "--boundary"], [T_Z3, T_HOW2, T_EXIT,
  ("L233-L235", "#  Z   3 descobre as combinaçes impossíveis, dá valres concrtos e testes  fronteira / ./mcdc analze \"speed > 100 or (speed > 50 and rain)\" --z3 --boundary")],
  "Z3 descarta combinações impossíveis; todas as condições têm par viável.",
  {"exit": 0, "combinacoes": 8, "impossiveis": 2, "todas_condicoes_com_par": True},
  "Q13-tabela: 2 combinações unsat (speed>100 ∧ ¬speed>50). Q13-pares: par viável para as 3 condições.",
  ["Q13-speed-rain-tabela", "Q13-speed-rain-pares"])
C("A28", "fronteira", D, ["analyze", "speed > 100 or (speed > 50 and rain)", "--z3", "--boundary"], [T_BOUND],
  "Fronteira de 'x > k' (inteiro): k e k+1.",
  {"fronteira_contem": {"speed > 100": ["100", "101"], "speed > 50": ["50", "51"]}},
  "L43: 'speed > 100 → 100 e 101' e 'variações no limite de cada comparação'. Q14: 101 é o único menor inteiro que "
  "satisfaz e 100 o único maior que não satisfaz (idem 51/50).", ["Q14-fronteira-gt100", "Q14-fronteira-gt50"])
C("A29", "z3", D, ["analyze", "speed > 100 or (speed > 50 and rain)", "--z3", "--boundary"], [T_CONC, ("L41", "| Dar valoes concretos | `--z3` | Combinaçoes impossiveis descrtadas  valoes concretos   teste (`speed = 101`) |")],
  "Valores concretos realizam a combinação declarada e o resultado esperado é o da guarda (incl. fronteira).",
  {"concretos_realizam": True}, "L41 e L463.", ["Q13-speed-rain-tabela"])
C("A30", "z3", D, ["analyze", "speed > 100 /\\ mode = idle", "--z3"], [T_CONC, T_Z3],
  "Valores concretos com comparação textual realizam a combinação.", {"exit": 0, "concretos_realizam": True},
  "L41, L463.", ["Q03-speed-mode-pares"])
C("A31", "exata", D, ["analyze", "(A and B) or C", "--exact", "--unique-cause"], [T_EXACT, T_GREEDY],
  "Suíte exata é a menor possível.", {"exit": 0, "tamanho_suite": 4},
  LEIT_CU + " Q15: mínimo 4 (sat em k=4, unsat em k=3).", ["Q15-exata-AB-or-C"])
C("A32", "exata", D, ["analyze", "(A or B) and (C or D)", "--exact", "--unique-cause"], [T_EXACT],
  "Suíte exata é a menor possível.", {"exit": 0, "tamanho_suite": 5}, "Q16: mínimo 5.", ["Q16-exata-AorB-and-CorD"])
C("A33", "exata", D, ["analyze", "A and (B or C)", "--exact", "--unique-cause"], [T_EXACT],
  "Suíte exata é a menor possível.", {"exit": 0, "tamanho_suite": 4}, "Q17: mínimo 4.", ["Q17-exata-A-and-BorC"])
C("A34", "exata", I, ["analyze", "((E or D) and (not A or D)) or B", "--exact"], [T_EXEX],
  "Exemplo de suíte exata (5 testes contra 6 da gulosa).", None, "",
  motivo="A variável negada foi apagada ('(not  or D)'); a expressão do exemplo não é única. O caso roda como "
  "diagnóstico com uma letra escolhida (A), sem expectativa. Além disso o mínimo no mascaramento depende da definição "
  "de mascaramento, que a fonte não dá.")
C("A35", "mutacao", D, ["analyze", "A and (B or C)", "--mutation"], [T_MUT, T_EXIT],
  "Mutação é opcional e não é problema de código 2.", {"exit": 0, "todas_condicoes_com_par": True},
  "L139 só lista condição sem par como problema do analyze; Q19: as 3 condições têm par.", ["Q19-mutacao-pares"])
C("A36", "mutacao", I, ["analyze", "A and (B or C)", "--mutation", "--format", "json"], [T_MUT],
  "Quantidade de mutantes por tipo.", None, "",
  motivo="A fonte só nomeia os seis tipos (ORF, ENF, VNF, MVF, VRF, ASF) sem definir como cada mutante é construído; "
  "o número de mutantes, equivalentes e detectados desta expressão não é derivável.")
C("A37", "gulosa", I, ["analyze", "(A and B) or C", "--format", "json"], [T_GREEDY],
  "Ordem da escolha gulosa e preferência de causa única no empate.", None, "",
  motivo="'considera primeiro as condições   pars' tem a qualificação apagada (menos/mais pares); quais pares "
  "são escolhidos não é derivável.")

# ------------------------------------------------------------------ formatos
C("F01", "formatos", D, ["analyze", "(A and B) or C", "--format", "json"], [T_FMT, T_OUTS, T_MINSUITE],
  "Saída JSON válida com o resultado completo da decisão.", {"exit": 0, "json_valido": True, "tamanho_suite": 4},
  "L121, L203.")
C("F02", "formatos", D, ["analyze", "(A and B) or C", "--format", "csv"], [T_FMT, T_OUTS, T_MINSUITE],
  "CSV da suíte: uma linha por teste e entrada, com o resultado esperado.",
  {"exit": 0, "csv_linhas_dados": 12, "csv_resultado_esperado_correto": True},
  "L205: uma linha por teste e entrada; 4 testes (L493) × 3 entradas = 12 linhas; o resultado esperado de cada "
  "teste é o valor da guarda na combinação.")
C("F03", "formatos", D, ["analyze", "(A and B) or C", "--format", "truth-csv"], [T_FMT, T_OUTS, T_TT0, T_HOW1],
  "Tabela-verdade inteira; linha 0 é tudo verdadeiro; resultado por linha.",
  {"exit": 0, "truth_linhas": 8, "truth_primeira_tudo_verdadeiro": True, "truth_resultado_correto": True},
  "L207, L279 (2^n), L485 ('a linha 0 é tudo verdadeiro').")
C("F04", "formatos", D, ["analyze", "speed > 100 or (speed > 50 and rain)", "--z3", "--format", "truth-csv"], [T_OUTS, T_HOW2],
  "truth-csv marca as combinações impossíveis.", {"exit": 0, "truth_linhas": 8, "truth_impossiveis_marcadas": 2},
  "L207; Q13: 2 impossíveis.", ["Q13-speed-rain-tabela"])
C("F05", "formatos", D, ["analyze", "(A and B) or C", "-o", "{OUT}/F05-relatorio.txt"], [T_O],
  "-o grava o relatório no arquivo em vez de mostrar na tela.",
  {"exit": 0, "arquivo_gerado": "{OUT}/F05-relatorio.txt", "stdout_sem_relatorio": True}, "L123.")
C("F06", "formatos", D, ["analyze", "--json", "{EX}/vm-decisoes.json", "--format", "json"], [T_OUTS],
  "JSON ligado ao requisito de origem de cada decisão.",
  {"json_valido": True, "rastreabilidade": {"vm#1": "REQ001", "vm#2": "REQ002", "vm#3": "REQ003", "vm#4": "REQ004", "vm#5": "REQ005"}},
  "L203: 'Resultado completo de cada decisão, ligado ao requisito de origem'. Pares id/requirement da entrada.")
C("F07", "formatos", I, ["check", "(A and B)", "--tests", "{ENT}/c02-completo.csv", "--format", "csv"], [T_FMT],
  "check com formato não aceito.", None, "",
  motivo="L121 diz que check aceita text e json, mas não diz o que ocorre com outro formato (código 1, ignorar, outro).")

# ------------------------------------------------------------------ .mcdc
C("M01", "mcdc-arquivo", D, ["analyze", "-f", "{EX}/requisitos.mcdc"], [T_REQ3, T_DIAG, T_EXIT],
  "REQ-003 tem condição redundante; condição sem par → código 2.",
  {"exit": 2, "requisitos": 3, "requisito_tem_classe": {"REQ-003": "redundante"}},
  "L241: 'REQ-003 tem  condião redundante' (o artigo apagado não muda o sentido). " + LEIT_EXIT)
C("M02", "mcdc-arquivo", D, ["analyze", "-f", "{EX}/requisitos.mcdc"], [T_MINSUITE, T_CU_MASK],
  "REQ-001 ((a∧b)∨c) e REQ-002 (a∧¬b) completos com 4 e 3 testes.",
  {"tamanho_suite_por_requisito": {"REQ-001": 4, "REQ-002": 3}, "requisitos_com_todas_com_par": ["REQ-001", "REQ-002"]},
  "Mesma forma dos exemplos conhecidos de L493; pares de causa única (Q01/Q02, renomeando variáveis).",
  ["Q01-AB-or-C-pares", "Q02-A-and-notB-pares"])
C("M03", "mcdc-arquivo", D, ["analyze", "-f", "{ENT}/m03-comentarios.mcdc"], [T_MCDC, T_EXIT],
  "Linhas com # são comentários: um único requisito.", {"exit": 0, "requisitos": 1}, "L143.", ["Q25-check-AandB-pares"])
C("M04", "mcdc-arquivo", D, ["analyze", "-f", "{ENT}/m04-erro-sintaxe.mcdc"], [T_REQF, T_EXIT],
  "Erro de sintaxe no requisito é entrada inválida.", {"exit": 1}, "L139 (1 = entrada inválida); L517.")
C("M05", "mcdc-arquivo", I, ["analyze", "-f", "{ENT}/m05-sem-id.mcdc"], [T_REQF, T_MCDC],
  "Linha sem identificador.", None, "",
  motivo="L517 só nomeia o tema 'linha sem identificador'; não diz se é erro, se é ignorada ou se recebe id automático.")

# ------------------------------------------------------------------ JSON / sistemas
for sid, f, n in (("VM", "vm-decisoes.json", (5, 21, 152, 4, 26, 152, 0, 152)),
                  ("TIS", "tis-decisoes.json", (17, 69, 268, 4, 80, 450, 21, 428)),
                  ("NPP", "npp-decisoes.json", (11, 29, 76, 1, 40, 146, 0, 146))):
    exp = {"requisitos": n[0], "condicoes": n[1], "combinacoes": n[2], "impossiveis": n[3], "tamanho_suite": n[4],
           "mutantes": {"total": n[5], "equivalentes": n[6], "detectados": n[7]}}
    just = ("Números travados em regressão (L467-L477). Impossíveis exigem Z3 e mutantes exigem --mutation; "
            "a variante é a padrão. Z3 independente reproduz requisitos/condições/combinações/impossíveis (%s-totais)." % sid)
    zq = ["%s-totais" % sid]
    if sid in ("VM", "NPP"):
        exp["exit"] = 0
        exp["todas_condicoes_com_par"] = True
        just += " Todas as condições têm par de causa única viável (%s-*-pares) → código 0." % sid
    C("J%s1" % sid, "sistemas", D, ["analyze", "--json", "{EX}/" + f, "--z3", "--mutation", "--format", "json"],
      [T_NUM, T_REG, T_MUT, T_EXIT], "Valores registrados do sistema %s." % sid, exp, just, zq)
    C("J%s2" % sid, "sistemas", D, ["analyze", "--json", "{EX}/" + f, "--exact", "--format", "json"], [T_REG, T_NUM, T_EXACT],
      "Busca exata produz o mesmo número de testes.", {"tamanho_suite": n[4]}, "L461: 'A busca exata ... produzem o mesmo número de testes nesses exemplos'.")
    C("J%s3" % sid, "sistemas", D, ["analyze", "--json", "{EX}/" + f, "--z3", "--unique-cause", "--format", "json"], [T_REG, T_NUM],
      "Variante causa única produz o mesmo número de testes.", {"tamanho_suite": n[4]}, "L461.")
    C("J%s4" % sid, "sistemas", D, ["analyze", "--json", "{EX}/" + f, "--z3", "--boundary", "--format", "json"], [T_CONC, T_BOUND],
      "Valores concretos (inclusive de fronteira) realizam a combinação e o resultado esperado é o da guarda.",
      {"concretos_realizam": True}, "L463.")
C("J01", "sistemas", I, ["analyze", "--json", "{EX}/tis-decisoes.json", "--z3", "--format", "json"], [T_NUM, T_REG],
  "Coluna 'Completos' (5/14/11).", None, "",
  motivo="A fonte não define 'requisito completo' (L461 só diz que nele testes = condições + 1); o critério de contagem "
  "não é único. Também o código de saída do TIS depende disso e não é derivável.")
C("J02", "modo-direto", D, ["analyze", "--json", "{EX}/vm-decisoes.json", "--direct", "--format", "json"], [T_DIRECT, T_EXIT],
  "Modo direto com o mesmo diagnóstico da tabela (VM sem condição sem par).", {"exit": 0, "todas_condicoes_com_par": True},
  "L419; VM-*-pares.", ["VM-totais"])
C("J03", "json", D, ["analyze", "--json", "{ENT}/j15-enum.json", "--z3", "--format", "json"], [T_JSONF, T_HOW2],
  "Valores de enumeração: m=a e m=b não valem juntos.", {"exit": 0, "combinacoes": 4, "impossiveis": 1, "todas_condicoes_com_par": True},
  "L153 (variáveis e tipos), L281. Q21.", ["Q21-enum-tabela", "Q21-enum-pares"])
C("J04", "entrada-invalida", D, ["analyze", "--json", "{ENT}/j16-invalido.json"], [T_JSONR, T_EXIT],
  "JSON malformado é entrada inválida.", {"exit": 1}, "L139; L519 'arquivos inválidos'.")
C("J05", "json", I, ["analyze", "--json", "{ENT}/j17-ids-repetidos.json"], [T_JSONR],
  "Ids de decisão repetidos.", None, "", motivo="L519 só nomeia o tema 'ids repetidos'; não diz se é recusa (código 1) nem outra consequência.")
C("J06", "formatos", D, ["analyze", "--json", "{EX}/vm-decisoes.json", "--z3", "--format", "truth-csv", "-o", "{OUT}/J06-tabela.csv"],
  [T_OUTS, T_O, T_NUM, ("L251", "./mcdc analyze --json exemlos/vm-decisoes.json --z3 --format truth-csv - tabela.csv")],
  "Tabela-verdade inteira do VM gravada em arquivo com impossíveis marcadas.",
  {"exit": 0, "arquivo_gerado": "{OUT}/J06-tabela.csv", "truth_linhas_arquivo": 152, "truth_impossiveis_marcadas_arquivo": 4},
  "L207, L123, L471. A opção '-o' do exemplo L251 aparece como '-' (letra apagada); L123 dá '-o'.", ["VM-totais"])
C("J07", "formatos", D, ["analyze", "--json", "{EX}/tis-decisoes.json", "--z3", "--format", "json", "-o", "{OUT}/J07-relatorio.json"],
  [T_OUTS, T_O, ("L249", "./mcdc analyze --json exemplos/tis-deisoes.json --z3 --format json -o relatorio.json")],
  "Relatório JSON do TIS gravado em arquivo, ligado aos requisitos.",
  {"arquivo_gerado": "{OUT}/J07-relatorio.json", "json_valido_arquivo": True, "rastreabilidade_arquivo_qtd": 17},
  "L249, L203.")

# ------------------------------------------------------------------ sem Z3
C("Z01", "sem-z3", D, ["analyze", "--json", "{EX}/vm-decisoes.json", "--z3"], [T_NOZ3],
  "Opção que exige Z3 avisa quando o executável não está instalado.", {"aviso_z3": True},
  "L73 'As opções que exigem Z3 avisam quando o executável não está instalado'. Código de saída não é dado.", z3env=False)
C("Z02", "sem-z3", D, ["analyze", "(A and B) or C"], [T_NOZ3, T_MINSUITE],
  "Recursos que não dependem do Z3 continuam disponíveis.", {"exit": 0, "tamanho_suite": 4},
  "L73 '[sem o] Z3, continuam disponíveis os recursos que não dependem dele' (o início da frase está apagado, "
  "mas 'continuam disponíveis' só faz sentido para a ausência).", z3env=False)
C("Z03", "sem-z3", D, ["verify", "--json", "{EX}/npp-decisoes.json"], [T_NOZ3, ("L83", "mcdc verify  <fonte> [--context \"<expr>\"]    confere  rquisitos  si (usa  Z   3)")],
  "verify usa o Z3 e avisa quando ele falta.", {"aviso_z3": True}, "L73, L83.", z3env=False)
C("Z04", "sem-z3", I, ["analyze", "speed > 100", "--boundary"], [T_BOUND, ("L115", "| `--boundary` |  `--z3`, acrsenta variants  frnteira |")],
  "--boundary sem --z3.", None, "", motivo="L115 tem a preposição apagada ('  `--z3`'); não se sabe se --boundary exige --z3, o implica ou é ignorado sem ele.")

# ------------------------------------------------------------------ check
C("K01", "check", D, ["check", "--json", "{EX}/decisoes.json", "--tests", "{EX}/testes.csv"], [T_CHECK, T_CSV, T_EXIT],
  "Teste com resultado esperado diferente do valor da guarda é divergente; condições não demonstradas → código 2.",
  {"exit": 2, "check_divergentes": ["T4"], "check_nao_demonstrada": True},
  "Q23: guarda de #3 em T4 (idle, botão true, moeda false) é false, esperado T → divergente. T1–T3 conferem. "
  "As decisões #2 e #4 não têm testes, logo há condição não demonstrada. " + LEIT_EXIT, ["Q23-check-exemplo"])
C("K02", "check", D, ["check", "A and B", "--tests", "{ENT}/c02-completo.csv"], [T_CHECK, T_CSV, T_EXIT, T_CU_MASK],
  "Testes com par de causa única para A e B: cobertura completa; sem colunas opcionais.",
  {"exit": 0, "check_completo": True},
  "L183: decision e expected_outcome são opcionais; valores T/F. T1/T2 demonstram A, T1/T3 demonstram B (causa única, "
  "válido no mascaramento por L491). Sem condição não demonstrada nem divergência → 0.", ["Q25-check-AandB-pares"])
C("K03", "check", D, ["check", "A and B", "--tests", "{ENT}/c03-incompleto.csv"], [T_CHECK, T_EXIT],
  "Falta par para B → condição não demonstrada → código 2.", {"exit": 2, "check_nao_demonstrada": True},
  "Só T1 (TT) e T2 (FT): B nunca muda, logo não há par para B em nenhuma variante (L283: a condição precisa mudar).")
C("K04", "check", D, ["check", "A and B", "--tests", "{ENT}/c04-esperado-errado.csv"], [T_CHECK, T_EXIT],
  "Resultado esperado errado (T3: A=T,B=F esperado T) → divergente → código 2.",
  {"exit": 2, "check_divergentes": ["T3"]}, "A∧B com A=T, B=F é F; esperado T.")
C("K05", "check", D, ["check", "A and B", "--tests", "{ENT}/c02-completo.csv", "--format", "json"], [T_FMT, T_CHECK],
  "check aceita json.", {"exit": 0, "json_valido": True}, "L121.")
C("K06", "check", D, ["check", "--json", "{ENT}/c06-concretos.json", "--tests", "{ENT}/c06-concretos.csv"], [T_CSV, T_CHECK, T_EXIT],
  "Valores concretos conforme o tipo; cobertura completa e resultados esperados corretos.", {"exit": 0, "check_completo": True},
  "L183: valor concreto conforme o tipo. Q24: guarda T, F, F para T1, T2, T3, igual ao esperado; T1/T2 mudam só x>5, "
  "T1/T3 mudam só y=true.", ["Q24-check-concretos"])
C("K07", "check", D, ["check", "A and B", "--tests", "{ENT}/c07-coluna-faltando.csv"], [T_CSV, T_CSVT, T_EXIT],
  "CSV sem a coluna obrigatória de valor é entrada inválida.", {"exit": 1},
  "L183: só decision e expected_outcome são opcionais; sem 'value' a entrada é inválida (L139, L521 'colunas faltando').")

# ------------------------------------------------------------------ verify
C("V01", "verify", D, ["verify", "--json", "{EX}/npp-decisoes.json"], [T_VERIFY, T_NUM, T_EXIT],
  "NPP tem 1 conflito → código 2.", {"exit": 2, "conflitos": 1}, "L475; Z3 NPP-conflitos = 1 (npp#5 × npp#8).", ["NPP-conflitos"])
C("V02", "verify", D, ["verify", "--json", "{EX}/tis-decisoes.json"], [T_VERIFY, T_NUM, T_EXIT],
  "TIS tem 3 conflitos → código 2.", {"exit": 2, "conflitos": 3}, "L473; Z3 TIS-conflitos = 3.", ["TIS-conflitos"])
C("V03", "verify", D, ["verify", "--json", "{EX}/vm-decisoes.json", "--format", "json"], [T_VERIFY, T_NUM],
  "VM sem conflitos.", {"json_valido": True, "conflitos": 0}, "L471; Z3 VM-conflitos = 0. Código de saída não avaliado (ver V09).", ["VM-conflitos"])
C("V04", "verify", D, ["verify", "--json", "{EX}/vm-decisoes.json", "--context", "the_system_mode = preparing_weak"],
  [T_VERIFY, ("L265", "./mcdc verify --json eemplos/vm-decisoes.json --context 'the_system_mode = preparing_weak'"), T_EXIT],
  "No contexto, há situação sem guarda válida → lacuna → código 2.", {"exit": 2, "lacuna": True, "conflitos": 0},
  "Q20: sat (ex.: timer fora de [10,30]).", ["Q20-VM-lacuna-preparing_weak", "VM-conflitos"])
C("V05", "verify", D, ["verify", "--json", "{ENT}/v05-conflito.json"], [T_VERIFY, T_ACTION, T_EXIT],
  "Guardas que valem juntas e escrevem valores diferentes → conflito → código 2.", {"exit": 2, "conflitos": 1},
  "Z3 V05-conflitos: x>5 ∧ x>3 ∧ s sat com y:=on × y:=off.", ["V05-conflitos"])
C("V06", "verify", D, ["verify", "--json", "{ENT}/v06-mesmo-valor.json", "--context", "mode = idle"], [T_VERIFY, T_ACTION, T_EXIT],
  "Mesmo valor não é conflito; no contexto sempre alguma guarda vale → código 0.", {"exit": 0, "conflitos": 0, "lacuna": False},
  "L503: contradição só com valores diferentes da mesma variável. Q22-V06: unsat (sem lacuna no contexto).", ["V06-conflitos", "Q22-V06-lacuna"])
C("V07", "verify", D, ["verify", "--json", "{ENT}/v07-disjuntos.json", "--context", "mode = idle"], [T_VERIFY, T_EXIT],
  "Guardas que não valem juntas não conflitam; sem lacuna no contexto → código 0.", {"exit": 0, "conflitos": 0, "lacuna": False},
  "Z3 V07-conflitos: candidato unsat; Q22-V07 unsat.", ["V07-conflitos", "Q22-V07-lacuna"])
C("V08", "verify", D, ["verify", "--json", "{EX}/vm-decisoes.json", "--context", "the_system_mode = preparing_weak", "--format", "json"], [T_FMT, T_VERIFY],
  "verify aceita json; mesma lacuna.", {"exit": 2, "json_valido": True, "lacuna": True}, "L121; Q20.", ["Q20-VM-lacuna-preparing_weak"])
C("V09", "verify", I, ["verify", "--json", "{EX}/vm-decisoes.json"], [T_VERIFY],
  "Lacunas sem --context.", None, "",
  motivo="A fonte não diz se, sem --context, verify procura lacunas em todo o espaço de estados; o código de saída do VM sem contexto não é único.")

# ------------------------------------------------------------------ CLI
C("E01", "entrada-invalida", I, ["check", "A and B", "--tests", "{ENT}/nao-existe.csv"], [T_EXIT],
  "Arquivo de testes inexistente.", None, "", motivo="A fonte não diz se arquivo ausente é 'entrada inválida' (código 1) ou outro erro.")
C("E02", "entrada-invalida", I, ["comando-inexistente", "A"], [T_EXIT],
  "Comando desconhecido.", None, "", motivo="Não descrito.")

ORACULO = {
    "condicao": "C2",
    "fonte": "experimentacao-pesquisa/experimentacao-2/documentation/tool-readme-C2.md",
    "sha256_fonte": "61C4062B5FC6B4F364F40465B0E017C80E0FA0C5433412EB2E925C545F6EFBE1",
    "unidade_de_contagem": "caso = uma invocação da CLI com ID estável; PASSOU se todas as asserções da expectativa são satisfeitas, FALHOU se alguma é contrariada; INDETERMINADO quando não há expectativa única.",
    "casos": CASES,
}

if __name__ == "__main__":
    p = os.path.join(BASE, "oraculo.json")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ORACULO, f, ensure_ascii=False, indent=2)
    det = sum(1 for c in CASES if c["status"] == D)
    print(len(CASES), "casos;", det, "determinados;", len(CASES) - det, "indeterminados")
    ids = [c["id"] for c in CASES]
    assert len(ids) == len(set(ids)), "IDs repetidos"
