"""Gera oraculo.json (C2) a partir do texto de tool-readme-C2.md. Nao le o SUT.
Os trechos literais preservam a corrupcao do texto-fonte (letras ausentes)."""
import json, pathlib

D, I = "DETERMINADO", "INDETERMINADO"
cases = []


def case(id, grupo, titulo, status, entrada, pre, trecho, regra, esperado, just, z3=None):
    cases.append(dict(id=id, grupo=grupo, titulo=titulo, status=status, entrada=entrada,
                      pre_condicao=pre, trecho_literal=trecho, regra=regra,
                      expectativa=esperado, justificativa=just, evidencia_z3=z3 or []))


NOZ3 = "z3 ausente do PATH"
Z3P = "z3 disponivel no PATH"
EXN = "exemplos/ do repositorio (entrada do SUT, nao documentacao)"

# ---------------------------------------------------------------- A: analyze basico
case("C2-001", "A-analyze", "analyze (A and B) or C (mascaramento)", D,
     {"comando": 'analyze "(A and B) or C"'}, NOZ3,
     '"./mcdc analyze \\"(A and B) or C\\" --unique-caue" [linha de exemplo; operador de causa unica corrompido] / "Exmplos conhecdos (( ∧ B) ∨ C  4 testes, A ∧ ¬B  3" / "Fnção | Comndo |   enrga | ... Gerar os testes | mcdc analyze | Tabla vrdade, pares  independência, suíte  testes  o par  demnsra cada condição"',
     "analyze gera tabela-verdade (2^n combinacoes de n entradas distintas), pares de independencia, suite de testes e o par que demonstra cada condicao; suite minima conhecida de 4 testes",
     ["codigo de saida 0", "3 entradas distintas e 3 condicoes: A, B, C", "8 combinacoes na tabela-verdade, 0 impossiveis",
      "cada uma das 3 condicoes demonstrada por um par de independencia", "suite com exatamente 4 testes"],
     "Expressao integra no texto; N+1=4 (exemplo conhecido do MinimalSuiteTest e regra N+1); Z3 confirma minimo 4 e existencia de pares.",
     ["z01_abc_masking_k3 (unsat)", "z01_abc_masking_k4 (sat)"])

case("C2-002", "A-analyze", "analyze (A and B) or C --unique-cause", D,
     {"comando": 'analyze "(A and B) or C" --unique-cause'}, NOZ3,
     '"--unique-cause | Causa únia  vez  mascaramento" / "(A and B) or C --unique-caue"',
     "--unique-cause usa a variante causa unica (somente a condicao alvo muda entre os dois testes do par) no lugar do mascaramento",
     ["codigo de saida 0", "3 condicoes demonstradas, cada par com uma unica condicao diferente", "suite com exatamente 4 testes"],
     "Causa unica tem definicao textual-padrao inequivoca (so a condicao alvo varia). Z3: minimo 4.",
     ["z01_abc_unique_k3 (unsat)", "z01_abc_unique_k4 (sat)"])

case("C2-003", "A-analyze", "analyze A and not B", D,
     {"comando": 'analyze "A and not B"'}, NOZ3,
     '"Exmplos conhecdos (( ∧ B) ∨ C  4 testes, A ∧ ¬B  3"',
     "exemplo conhecido de suite minima: A ∧ ¬B tem 3 testes (N+1)",
     ["codigo de saida 0", "2 condicoes, ambas demonstradas", "4 combinacoes", "suite com exatamente 3 testes"],
     "Valor 3 fixado no texto; Z3 confirma minimo 3.", ["z02_anotb_masking_k2 (unsat)", "z02_anotb_masking_k3 (sat)"])

case("C2-004", "A-analyze", "entrada repetida: (A and B) or (not A and C)", D,
     {"comando": 'analyze "(A and B) or (not A and C)"'}, NOZ3,
     '"Por emplo,  `(A and B) or (not A and C)`, há 3 entrads dstitas (`A`, `B` e `C`)  4 ocorencias  condição (`A#1`, `B`, `A#2`  `C`)." / "tabela-verdade: para  entradas distintas  expressão, são consideradas  2ⁿ combinações"',
     "entradas distintas: 3 (A,B,C); condicoes = ocorrencias: 4 (A#1,B,A#2,C); tabela-verdade tem 2^3 linhas",
     ["3 entradas distintas", "4 condicoes rotuladas A#1, B, A#2, C", "8 combinacoes na tabela-verdade"],
     "Contagens explicitas no texto (paragrafo integro).", [])

case("C2-005", "A-analyze", "pares de A#1/A#2 com entradas repetidas e causa unica", I,
     {"comando": 'analyze "(A and B) or (not A and C)" [--unique-cause]'}, NOZ3,
     '"entrada repetida:  aparião é  condição  par próprio (#1, A#2)"',
     "o texto nao define se ha par (e qual) para ocorrencias acopladas, nem a semantica de mascaramento/causa unica para ocorrencias repetidas",
     ["INDETERMINADO: omissao de definicao; nao executado"],
     "Frase corrompida e sem definicao operacional de pares por ocorrencia; Z3 informativo (z15) nao e expectativa.", ["z15_ocorrencias_repetidas_info (informativo)"])

case("C2-006", "A-analyze", "operadores simbolicos && || !", D,
     {"comando": 'analyze "(A && B) || !C"'}, NOZ3,
     '"|  | `and`, `&&`, `/\\` | ... |  | `or`, `\\|\\|`, `\\/` | ... | não | `not`, `!` |"',
     "&&, || e ! sao formas aceitas equivalentes a and, or, not; mesma analise",
     ["codigo de saida 0", "3 condicoes demonstradas", "8 combinacoes", "suite com exatamente 4 testes"],
     "Formas equivalentes aceitas; mesma estrutura (A and B) or not C; Z3 minimo 4.", ["z06b_ab_or_notc_masking_k4 (sat)", "z06b_ab_or_notc_masking_k3 (unsat)"])

case("C2-007", "A-analyze", "operadores /\\ \\/ not", D,
     {"comando": r"analyze '(A /\ B) \/ not C'"}, NOZ3,
     '"Operadres (use apas simls qndo a expressão tiver `\\`)"; "/\\" e "\\/" nas formas aceitas',
     "/\\ e \\/ sao formas aceitas de and/or; mesma analise",
     ["codigo de saida 0", "3 condicoes demonstradas", "8 combinacoes", "suite com exatamente 4 testes"],
     "Idem C2-006.", ["z06b_ab_or_notc_masking_k4 (sat)"])

case("C2-008", "A-analyze", "comparacao como condicao: speed > 100 /\\ mode = idle", D,
     {"comando": r"analyze 'speed > 100 /\ mode = idle'"}, NOZ3,
     '"Expressão dreta | `\\"(A and B) or C\\"`, `\'speed > 100 /\\ mode = idle\'`" / "# comparações e  operadores do DFRS"',
     "cada comparacao e uma condicao; estrutura AND de duas condicoes -> suite de 3 testes (como A and not B)",
     ["codigo de saida 0", "2 condicoes (speed > 100; mode = idle) demonstradas", "4 combinacoes", "suite com 3 testes"],
     "Expressao integra; estrutura analoga a A ∧ ¬B=3; Z3 minimo de conjuncao de 2 = 3 (z02 equivalente por sinal).", ["z02_anotb_masking_k3 (sat)"])

case("C2-009", "A-analyze", "operadores de comparacao = == != < <= > >=", D,
     {"comando": "analyze 'x OP 5' para OP em {=, ==, !=, <, <=, >, >=}"}, NOZ3,
     '"| comparção | `=`, `==`, `!=`, `<`, `<=`, `>`, `>=` |"',
     "as 7 formas de comparacao sao aceitas; decisao de uma unica condicao",
     ["codigo de saida 0 para cada operador", "1 condicao demonstrada", "2 combinacoes", "suite com 2 testes"],
     "Operadores listados no texto; suite de 1 condicao = N+1 = 2 (Z3 z05).", ["z05_1cond_masking_k2 (sat)"])

# ---------------------------------------------------------------- B: restricao/diagnostico
case("C2-010", "B-diagnostico", "--constraint 'not A or B' em A or (B and C)", D,
     {"comando": 'analyze "A or (B and C)" --constraint "not A or B"  [tambem --format truth-csv]'}, NOZ3,
     '"--constraint \\"<expr>\\" | Rtrição etre condições escrta  mão" / "restrição escita  mão: A = speed > 100 impica B = speed > 50" / "combinações impossíveis ... não participam da análse"',
     "combinacoes que violam a restricao sao impossiveis: A=T,B=F (2 linhas das 8); as demais participam; todas as condicoes continuam com par",
     ["8 combinacoes, 2 impossiveis (A=T,B=F)", "as 2 linhas impossiveis marcadas na tabela-verdade", "codigo de saida 0", "3 condicoes demonstradas"],
     "Restricao booleana simples; Z3 enumera 6 sat e 2 unsat; pares remanescentes existem (verificado em z08 + definicao).", ["z08_constraint_A_implica_B"])

case("C2-011", "B-diagnostico", "condicao bloqueada por combinacoes impossiveis", D,
     {"comando": 'analyze "A and B" --constraint "not A or not B"'}, NOZ3,
     '"deixa de possuir pares por causa de combinações impossíveis,  classificada como bloqueada" / "2: ... com  condição sem par para analyze"',
     "sem par por causa de combinacoes impossiveis -> bloqueada (nao redundante); condicao sem par -> codigo 2",
     ["codigo de saida 2", "A e B classificadas como bloqueadas (nao redundantes)"],
     "Sem a restricao ha par (z07b sat); com a restricao nenhuma linha altera a saida (z07 unsat).", ["z07_bloqueada", "z07b_sem_restricao"])

case("C2-012", "B-diagnostico", "condicao redundante: A or (A and B)", D,
     {"comando": 'analyze "A or (A and B)"'}, NOZ3,
     '"cada cond   ição sem par: **redndante** ( requisio pode ser smplificado)  **bloqueda**" / "Se  condição não possui par mesmo considerando tods  combinações, é classificada  redundante"',
     "B nunca altera a decisao em nenhuma combinacao -> redundante; condicao sem par -> codigo 2",
     ["codigo de saida 2", "a condicao B e classificada como redundante (nao bloqueada)"],
     "Z3: nao existe combinacao em que B altere f (unsat).", ["z06_redundante_B"])

case("C2-013", "B-diagnostico", "--z3: combinacoes impossiveis numericas e valores concretos", D,
     {"comando": 'analyze "speed > 100 or (speed > 50 and rain)" --z3 --format csv  [+ --format json]'}, Z3P,
     '"Com Z3 ... descata combinaçoes impossiveis  atribi valoes concretos às entadas de  tete" / "./mcdc analze \\"speed > 100 or (speed > 50 and rain)\\" --z3 --boundary"',
     "speed>100 e verdadeiro implica speed>50 verdadeiro: 2 de 8 combinacoes impossiveis (c1=T,c2=F); cada teste recebe valores concretos que realizam a combinacao e o resultado esperado e o da guarda",
     ["8 combinacoes, 2 impossiveis", "para cada teste: os valores concretos de speed/rain avaliam as comparacoes exatamente como a combinacao declarada",
      "resultado esperado = avaliacao da guarda sobre os valores concretos", "codigo de saida 0"],
     "Z3: as combinacoes (T,F,*) sao unsat, as demais sat com testemunha speed=101 etc.; propriedade de ReportsContentTest.", ["z09_combinacoes_velocidade"])

case("C2-014", "B-diagnostico", "--z3 --boundary: valores de fronteira", D,
     {"comando": 'analyze "speed > 100 or (speed > 50 and rain)" --z3 --boundary --format csv'}, Z3P,
     '"Testes  frnteira | --z3 --boundary | Variaçes  lmite  cada comparção (speed > 100 → 100  101)"',
     "para cada comparacao speed > K aparecem testes com speed=K e speed=K+1",
     ["algum teste com speed=100 e algum com speed=101", "algum teste com speed=50 e algum com speed=51"],
     "Variacao de limite explicita com exemplo 100/101; Z3 confirma 100 -> falso e 101 -> verdadeiro (z10).", ["z10_fronteira"])

case("C2-015", "B-diagnostico", "--z3 sem Z3 instalado: aviso", D,
     {"comando": 'analyze "(A and B) or C" --z3'}, NOZ3,
     '"As opçoes  exgem  Z3 avisam qndo o executvel não está instaldo" / "Z3,  continum disponiveis  recurss que não dependm dele"',
     "opcoes que exigem Z3 avisam quando o executavel nao esta instalado",
     ["a saida (stdout ou stderr) contem um aviso mencionando z3/Z3"],
     "Aviso explicito; sem especificar codigo de saida (ver C2-063).", [])

# ---------------------------------------------------------------- C: exact/direct/limites
case("C2-016", "C-exact", "--exact: suites minimas conhecidas", D,
     {"comando": 'analyze EXPR --exact  para EXPR em {"(A and B) or C", "A and not B"}'}, Z3P,
     '"Suíe exata | --exact |  menro suíte possivel, esclhida  Z3" / "Exmplos conhecdos (( ∧ B) ∨ C  4 testes, A ∧ ¬B  3"',
     "a suite exata e a menor possivel: 4 e 3 testes respectivamente",
     ["(A and B) or C: codigo 0 e suite com 4 testes", "A and not B: codigo 0 e suite com 3 testes"],
     "Valores conhecidos; Z3 minimo.", ["z01_abc_masking_k3", "z02_anotb_masking_k2"])

case("C2-017", "C-exact", "--exact --unique-cause em (A or B) and (C or D)", D,
     {"comando": 'analyze "(A or B) and (C or D)" --exact --unique-cause'}, Z3P,
     '"--exact: Suíe exata:  menro possivel" / "--unique-cause | Causa únia"',
     "suite exata de causa unica = menor suite possivel sob causa unica = 5 (Z3)",
     ["codigo de saida 0", "suite exata com exatamente 5 testes", "4 condicoes demonstradas"],
     "Minimo sob causa unica calculado por Z3 independente (k=4 unsat, k=5 sat); definicao de causa unica nao ambigua.", ["z03_aorb_and_cord_unique_k4 (unsat)", "z03_aorb_and_cord_unique_k5 (sat)"])

case("C2-018", "C-exact", "--exact em mascaramento de (A or B) and (C or D)", I,
     {"comando": 'analyze "(A or B) and (C or D)" --exact'}, Z3P,
     '"mascaramento (pdrão)"',
     "o texto nao define formalmente o mascaramento; sob a definicao padrao adotada o minimo e 4, sob outras pode diferir",
     ["INDETERMINADO: definicao de mascaramento ausente; nao executado"],
     "Dependencia da definicao de mascaramento (Z3 informativo z03 masking=4).", ["z03_aorb_and_cord_masking_k3 (unsat)", "z03_aorb_and_cord_masking_k4 (sat)"])

case("C2-019", "C-exact", "exemplo ((E or D) and (not ? or D)) or B: 5 exata e 6 gulosa", I,
     {"comando": 'analyze "((E or D) and (not ? or D)) or B" --exact'}, Z3P,
     '"./mcdc analze \\"((E or D) and (not  or D)) or B\\" --exact" / "suíe exata (aqui, 5 testes  vez  6 da escolha guloa)"',
     "a letra da segunda entrada negada esta ausente do texto; a expressao nao e unica",
     ["INDETERMINADO: expressao corrompida; nao executado"],
     "Nao e permitido completar o texto pelo SUT nem por conveniencia; nao ha expectativa unica.", [])

case("C2-020", "C-exact", "limites: 20 entradas na tabela-verdade completa", D,
     {"comando": 'analyze "X1 and X2 and ... and X20"'}, NOZ3,
     '"Os limtes documentads :  20 entradas   tabela-verdade cmpeta" / "20 enradas, mascaramento | 0,10  0,17 s | 5 s"',
     "20 entradas sao suportadas na tabela-verdade completa e analisadas (mascaramento)",
     ["codigo de saida 0", "20 condicoes, todas demonstradas", "2^20 = 1048576 combinacoes"],
     "Limite documentado e caso medido com 20 entradas; Z3 confirma 2^20 = 1048576 (z11).", ["z11_tabela_regressao"])

case("C2-021", "C-exact", "--z3 acima de 12 entradas passa sozinho ao modo direto", D,
     {"comando": 'analyze "X1 and ... and X13" --z3'}, Z3P,
     '"--z3 | ... acim  12 entradas, passa soznho  modo dreto"',
     "com --z3 e mais de 12 entradas, o modo direto e usado automaticamente: a analise conclui normalmente",
     ["codigo de saida 0", "13 condicoes, todas demonstradas"],
     "Regra explicita; conjuncao de 13 condicoes tem pares para todas (z04 generalizacao).", ["z04_and3_masking_k4 (sat; estrutura analoga)"])

case("C2-022", "C-exact", "--direct com 30 entradas", D,
     {"comando": 'analyze "X1 and ... and X30" --direct'}, Z3P,
     '"--direct | Pares pedds dreto  Z3,  mnar a tabela ( 30 entradas)" / "30 entradas  modo dreto"',
     "modo direto suporta ate 30 entradas",
     ["codigo de saida 0", "30 condicoes, todas demonstradas"],
     "Limite documentado.", [])

case("C2-023", "C-exact", "--direct equivale a tabela completa (cobertura e diagnostico)", D,
     {"comando": 'analyze EXPR --direct  para EXPR em {"(A and B) or C", "A or (A and B)"}'}, Z3P,
     '" modo dreto dá  mesam cobertura   mesom dignstio  a tabea-verdae cmpleta"',
     "o modo direto produz a mesma cobertura e o mesmo diagnostico da tabela completa",
     ["(A and B) or C: codigo 0, 3 condicoes demonstradas", "A or (A and B): codigo 2, B redundante"],
     "Equivalencia explicita; expectativas de C2-001 e C2-012.", ["z01_abc_masking_k4", "z06_redundante_B"])

case("C2-024", "C-exact", "21 entradas sem --z3 (acima do limite de 20)", I,
     {"comando": 'analyze "X1 and ... and X21"'}, NOZ3,
     '"20 entradas   tabela-verdade cmpeta"', "o texto nao diz o comportamento acima do limite (erro, aviso ou outro modo)",
     ["INDETERMINADO; nao executado"], "Omissao.", [])

case("C2-025", "C-exact", "31 entradas com --direct", I,
     {"comando": 'analyze "X1 and ... and X31" --direct'}, Z3P,
     '"30 entradas  modo dreto"', "comportamento acima do limite nao especificado",
     ["INDETERMINADO; nao executado"], "Omissao.", [])

# ---------------------------------------------------------------- D: sistemas de exemplo
for sid, nome, arq, req, comp, cond, comb, imp, tst, mut, eq, peg, conf in [
        ("026", "VM", "exemplos/vm-decisoes.json", 5, 5, 21, 152, 4, 26, 152, 0, 152, 0),
        ("027", "TIS", "exemplos/tis-decisoes.json", 17, 14, 69, 268, 4, 80, 450, 21, 428, 3),
        ("028", "NPP", "exemplos/npp-decisoes.json", 11, 11, 29, 76, 1, 40, 146, 0, 146, 1)]:
    ec = 0 if comp == req else 2
    case(f"C2-{sid}", "D-exemplos", f"analyze {nome} (--z3): numeros travados", D,
         {"comando": f"analyze --json {arq} --z3 --format json", "arquivo": arq}, Z3P + "; " + EXN,
         f'"| {nome} | {req} | {comp} | {cond} | {comb} | {imp} | {tst} | {mut} | {eq} | {peg} | {conf} |" / "Requisitos | Cmpletos | Condições | Combinaçoes | Impossiveis | Testes | Mutants | Equivalents | Pegos | Confltos"',
         "valores registrados para o sistema de exemplo: requisitos, completos, condicoes, combinacoes, impossiveis, testes",
         [f"{req} requisitos/decisoes", f"{comp} requisitos completos (todas as condicoes demonstradas)", f"{cond} condicoes",
          f"{comb} combinacoes e {imp} impossiveis", f"{tst} testes na suite",
          f"codigo de saida {ec} ({'todos completos' if ec == 0 else 'ha requisitos com condicao sem par'})"],
         "Valores numericos explicitos na tabela de regressao; aritmetica consistente (Z3 z11). Para requisito completo, testes = condicoes+1 (VM: 21+5=26; NPP: 29+11=40).",
         ["z11_tabela_regressao"])
    case(f"C2-{int(sid)+3:03d}", "D-exemplos", f"analyze {nome} --mutation: mutantes", D,
         {"comando": f"analyze --json {arq} --z3 --mutation --format json", "arquivo": arq}, Z3P + "; " + EXN,
         f'"| {nome} | ... | {mut} | {eq} | {peg} | {conf} |" / "versões equivalentes ao requisito original não entram  contgem"',
         "mutacao: total de mutantes, equivalentes (fora da contagem) e detectados",
         [f"{mut} mutantes no total", f"{eq} equivalentes", f"{peg} detectados"],
         "Valores explicitos; 450-21=429>=428 (Z3 z11).", ["z11_tabela_regressao"])
    case(f"C2-{int(sid)+6:03d}", "D-exemplos", f"verify {nome}: conflitos", D,
         {"comando": f"verify --json {arq} --format json", "arquivo": arq}, Z3P + "; " + EXN,
         f'"Confltos" = {conf}; "2: ... um cnfito ou uma lcuna no verify"; "0: ... sem apontar os problemas"',
         "conflitos registrados; conflito -> codigo 2; sem conflito e sem contexto -> 0",
         [f"{conf} conflitos", f"codigo de saida {0 if conf == 0 else 2}"],
         "Contagem explicita; lacunas so sao verificadas com --context.", ["z13_verify_conflito (semantica)"])

case("C2-035", "D-exemplos", "verify VM --context 'the_system_mode = preparing_weak'", I,
     {"comando": "verify --json exemplos/vm-decisoes.json --context 'the_system_mode = preparing_weak'"}, Z3P + "; " + EXN,
     "\"./mcdc verify --json eemplos/vm-decisoes.json --context 'the_system_mode = preparing_weak'\"",
     "o texto nao informa se existe lacuna nessa situacao",
     ["INDETERMINADO; nao executado"], "Omissao do resultado.", [])

case("C2-036", "D-exemplos", "analyze -f exemplos/requisitos.mcdc: REQ-003 redundante", D,
     {"comando": "analyze -f exemplos/requisitos.mcdc --format json", "arquivo": "exemplos/requisitos.mcdc"}, NOZ3 + "; " + EXN,
     '"# vários requisitos de um arquivo; REQ-003 tem  condião redundante"',
     "o requisito REQ-003 tem uma condicao redundante; condicao sem par -> codigo 2",
     ["REQ-003 aparece com ao menos uma condicao redundante", "codigo de saida 2"],
     "Afirmacao explicita do exemplo.", [])

# ---------------------------------------------------------------- E: formatos de entrada/saida
case("C2-037", "E-formatos", "arquivo .mcdc do texto", D,
     {"comando": "analyze -f req.mcdc --format json",
      "arquivo_criado": "# comentario\nREQ-001: (alarme_ativo and porta_aberta) or botao_emergencia\nREQ-002: porta_fechada and not obstaculo\n"}, NOZ3,
     '"Arqivo `.mcdc`: um requisito  linha, `ID: expressão`. Lnhas com `#`  comentrios." + exemplo REQ-001/REQ-002',
     "um requisito por linha 'ID: expressao'; # e comentario",
     ["2 requisitos: REQ-001 e REQ-002 (comentario ignorado)", "REQ-001: 3 condicoes e suite de 4 testes", "REQ-002: 2 condicoes e suite de 3 testes", "codigo de saida 0"],
     "Formato e exemplo integros; suites N+1 (z01, z02 por estrutura).", ["z01_abc_masking_k4", "z02_anotb_masking_k3"])

case("C2-038", "E-formatos", "JSON de decisoes da NAT2TEST", D,
     {"comando": "analyze --json vm1.json --format json",
      "arquivo_criado": '{"system":"the_coffee_machine_system","inputs":[{"name":"the_system_mode","type":"enum","values":["idle","choice"]},{"name":"the_coin_sensor","type":"bool"}],"decisions":[{"id":"vm#1","requirement":"REQ-001","guard":"the_system_mode = idle /\\\\ the_coin_sensor = true","actions":["the_system_mode := choice"]}]}'}, NOZ3,
     '"JSON  decisões (fomato do Extractr  NAT2TEST): cotm  variavis  seus tips, alem das decisões,     guarda   ações." + exemplo vm#1 / "json | Reutado cmpleto de cada decião, lgdo  rquisito  orgem"',
     "o JSON e lido; a decisao vm#1 tem guarda de 2 condicoes; o relatorio JSON liga a decisao ao requisito de origem",
     ["relatorio JSON valido com a decisao vm#1 ligada ao requisito REQ-001", "2 condicoes demonstradas", "suite com 3 testes", "codigo de saida 0"],
     "Estrutura do arquivo dada no texto; a acao 'choce' esta corrompida e foi escrita 'choice' (valor ja listado em values); nao afeta a guarda.", ["z02_anotb_masking_k3"])

case("C2-039", "E-formatos", "--format csv: uma linha por teste", D,
     {"comando": 'analyze "(A and B) or C" --format csv'}, NOZ3,
     '"csv |  suíte:  liha por tste  enrada,  o reutado esperdo,   o tese demnstra   valoes concetos"',
     "CSV da suite: uma linha por teste, com entradas, resultado esperado e condicao demonstrada; esperado = valor da guarda",
     ["4 linhas de teste (alem do cabecalho)", "para cada linha, o resultado esperado e igual a avaliacao de (A and B) or C nas entradas da linha"],
     "Descricao explicita + ReportsContentTest (esperado = o que a guarda da).", ["z12d_check_esperado (avaliacao da guarda)"])

case("C2-040", "E-formatos", "--format truth-csv: tabela-verdade interna", D,
     {"comando": 'analyze "(A and B) or C" --format truth-csv'}, NOZ3,
     '"truth-csv | A tabela-verdade intea,   combinaçoes impssiveis marcads" / "TruthTableTest | ... A  linha 0  tudo verdadiro;  saída  cada linha"',
     "uma linha por combinacao; a linha 0 e tudo verdadeiro; ha saida por linha",
     ["8 linhas de combinacao", "a linha 0 tem A, B e C verdadeiros", "a saida de cada linha e a da guarda"],
     "Descricao explicita.", [])

case("C2-041", "E-formatos", "--format json: JSON valido", D,
     {"comando": 'analyze "(A and B) or C" --format json'}, NOZ3,
     '"json | Reutado cmpleto de cada decião, lgdo  rquisito  orgem (fomato  integrção)"',
     "a saida json e um documento JSON com o resultado completo da decisao",
     ["a saida padrao e um JSON valido (parse sem erro)"], "Formato de integracao.", [])

case("C2-042", "E-formatos", "-o grava o relatorio em arquivo", D,
     {"comando": 'analyze "(A and B) or C" -o relatorio.txt'}, NOZ3,
     '"-o <arquivo> | Grava  relatorio  arqivo  vez  mostrr  tela"',
     "o relatorio vai para o arquivo e nao e mostrado na tela",
     ["o arquivo existe e nao esta vazio", "a saida padrao nao contem o relatorio (nao contem a tabela/ suite: vazia ou apenas aviso curto)"],
     "Instrucao explicita.", [])

# ---------------------------------------------------------------- F: check
CHK_FULL = "test,input,value\nT1,A,T\nT1,B,T\nT1,C,F\nT2,A,F\nT2,B,T\nT2,C,F\nT3,A,T\nT3,B,F\nT3,C,F\nT4,A,T\nT4,B,F\nT4,C,T\n"
case("C2-043", "F-check", "check: suite completa de MC/DC", D,
     {"comando": 'check "(A and B) or C" --tests t.csv', "arquivo_criado": CHK_FULL}, NOZ3,
     '"mcdc check   <fone> --tests <testes.csv>    mede  MC/DC  teses já exitentes" / "0: comndo concluido  apontr os prblemas"',
     "T1..T4 demonstram A (T1,T2), B (T1,T3) e C (T3,T4): cobertura completa, nenhum problema -> 0",
     ["codigo de saida 0", "as 3 condicoes demonstradas"], "Z3 confirma pares para A,B,C no conjunto.", ["z12_check_completo", "z12d_check_esperado"])

case("C2-044", "F-check", "check: suite incompleta", D,
     {"comando": 'check "(A and B) or C" --tests t.csv', "arquivo_criado": "test,input,value\nT1,A,T\nT1,B,T\nT1,C,F\nT2,A,F\nT2,B,T\nT2,C,F\n"}, NOZ3,
     '"2: ... condição não demonstrda"', "so A e demonstrada por T1,T2; B e C nao -> codigo 2",
     ["codigo de saida 2", "A demonstrada; B e C nao demonstradas"], "Z3: A sat; B,C unsat para {T1,T2}.", ["z12b_check_parcial_T1T2"])

case("C2-045", "F-check", "check: resultado esperado divergente", D,
     {"comando": 'check "(A and B) or C" --tests t.csv --format json',
      "arquivo_criado": "test,input,value,expected_outcome\nT1,A,T,F\nT1,B,T,F\nT1,C,F,F\nT2,A,F,F\nT2,B,T,F\nT2,C,F,F\nT3,A,T,F\nT3,B,F,F\nT3,C,F,F\nT4,A,T,T\nT4,B,F,T\nT4,C,T,T\n"}, NOZ3,
     '"2: ... um resutado espero divergente  check" / "As colunas decision e expected_outcome são opcionais"',
     "T1 (A=T,B=T,C=F) tem guarda verdadeira mas expected_outcome=F -> divergencia -> 2",
     ["codigo de saida 2", "o teste T1 e apontado com resultado esperado divergente"], "Z3 avalia T1 = true.", ["z12d_check_esperado"])

case("C2-046", "F-check", "check com JSON, valores concretos e coluna decision", D,
     {"comando": "check --json d.json --tests t.csv",
      "arquivo_criado_json": '{"system":"s","inputs":[{"name":"the_system_mode","type":"enum","values":["idle","choice"]},{"name":"the_coin_sensor","type":"bool"}],"decisions":[{"id":"vm#1","requirement":"REQ-001","guard":"the_system_mode = idle /\\\\ the_coin_sensor = true","actions":[]}]}',
      "arquivo_criado": "decision,test,input,value,expected_outcome\nvm#1,T1,the_system_mode,idle,T\nvm#1,T1,the_coin_sensor,true,T\nvm#1,T2,the_system_mode,choice,F\nvm#1,T2,the_coin_sensor,true,F\nvm#1,T3,the_system_mode,idle,F\nvm#1,T3,the_coin_sensor,false,F\n"}, NOZ3,
     '"Teses existntes (pra  comndo check), em CSV: ... O valr pode ser lgico (T/F) ou cncreto, confore  tipo da variavel." + exemplo vm#1,T1,the_system_mode,idle,T',
     "T1 realiza ambas verdadeiras (T); T2 muda so o modo (F) e T3 muda so o sensor (F): ambas demonstradas; esperados corretos",
     ["codigo de saida 0", "as 2 condicoes demonstradas", "nenhum resultado esperado divergente"], "Estrutura do exemplo; valores concretos validos para enum/bool.", [])

case("C2-047", "F-check", "check: CSV sem coluna obrigatoria", D,
     {"comando": 'check "(A and B) or C" --tests t.csv', "arquivo_criado": "test,input\nT1,A\nT1,B\n"}, NOZ3,
     '"decision  expected_outcome são opcionis" (portanto test,input,value sao obrigatorias) / "1: entraa invalida" / "TestCasesFileTest: ... colunas fltando"',
     "CSV sem a coluna value e entrada invalida -> codigo 1",
     ["codigo de saida 1"], "Colunas opcionais explicitadas; falta de obrigatoria e invalida.", [])

case("C2-048", "F-check", "check --format csv", I,
     {"comando": 'check ... --format csv'}, NOZ3, '"check  verify acetam text e json"',
     "o texto diz o que e aceito, nao o resultado de formato nao aceito", ["INDETERMINADO; nao executado"], "Omissao.", [])

# ---------------------------------------------------------------- G: verify
VERIFY_BASE = '{{"system":"s","inputs":[{{"name":"sw","type":"enum","values":["on","off"]}},{{"name":"out","type":"enum","values":["lo","hi"]}}],"decisions":[{decs}]}}'
def vj(decs): return VERIFY_BASE.format(decs=decs)
case("C2-049", "G-verify", "verify: conflito (guardas sobrepostas, valores diferentes)", D,
     {"comando": "verify --json c.json --format json",
      "arquivo_criado": vj('{"id":"d1","requirement":"R1","guard":"sw = on","actions":["out := lo"]},{"id":"d2","requirement":"R2","guard":"sw = on","actions":["out := hi"]}')}, Z3P,
     '"Confltos (dois requistos valem jtos  escrvem valoes diferetes)" / "2: ... um cnfito"',
     "dois requisitos valem juntos (sw = on) e escrevem valores diferentes em out -> 1 conflito; codigo 2",
     ["1 conflito entre R1 e R2", "codigo de saida 2"], "Z3: guardas simultaneamente satisfativeis (z13).", ["z13_verify_conflito"])

case("C2-050", "G-verify", "verify: guardas disjuntas nao conflitam", D,
     {"comando": "verify --json c.json --format json",
      "arquivo_criado": vj('{"id":"d1","requirement":"R1","guard":"sw = on","actions":["out := lo"]},{"id":"d2","requirement":"R2","guard":"sw = off","actions":["out := hi"]}')}, Z3P,
     '"Z3RequirementsVerifierTest | Conltos, guardas  não se sobreõm, mesom valor  cnflto, lacunas  com cntexto"',
     "guardas que nao se sobrepoem nao geram conflito -> 0 conflitos; sem contexto, codigo 0",
     ["0 conflitos", "codigo de saida 0"], "Z3: sw=on e sw=off insatisfativel junto.", ["z13_verify_conflito"])

case("C2-051", "G-verify", "verify: mesmo valor nao e conflito", D,
     {"comando": "verify --json c.json --format json",
      "arquivo_criado": vj('{"id":"d1","requirement":"R1","guard":"sw = on","actions":["out := lo"]},{"id":"d2","requirement":"R2","guard":"sw = on","actions":["out := lo"]}')}, Z3P,
     '"Conflitos (dois requisitos valem juntos e escrevem valores diferentes)" ("mesom valor  cnflto")',
     "escrever o mesmo valor nao e conflito (a definicao exige valores diferentes)",
     ["0 conflitos", "codigo de saida 0"], "Definicao textual de conflito.", [])

case("C2-052", "G-verify", "verify --context: lacuna", D,
     {"comando": "verify --json c.json --context \"sw = on or sw = off\" --format json",
      "arquivo_criado": vj('{"id":"d1","requirement":"R1","guard":"sw = on","actions":["out := lo"]}')}, Z3P,
     '"lacunas (nnum requisito vale)" / "--context \\"<expr>\\" | No verify: confre se, nssa suação, smre algma guarda vale"',
     "no contexto (sw = on or sw = off) nenhuma guarda vale quando sw = off -> 1 lacuna; codigo 2",
     ["1 lacuna (situacao sw = off)", "codigo de saida 2"], "Z3: existe situacao do contexto sem guarda (z14 sat, mode=b).", ["z14_verify_lacuna"])

case("C2-053", "G-verify", "verify --context: sem lacuna", D,
     {"comando": "verify --json c.json --context \"sw = on or sw = off\" --format json",
      "arquivo_criado": vj('{"id":"d1","requirement":"R1","guard":"sw = on","actions":["out := lo"]},{"id":"d2","requirement":"R2","guard":"sw = off","actions":["out := lo"]}')}, Z3P,
     '"confre se, nssa suação, smre algma guarda vale"',
     "as guardas cobrem o contexto: 0 lacunas, 0 conflitos (mesmo valor); codigo 0",
     ["0 lacunas", "0 conflitos", "codigo de saida 0"], "Z3: sem situacao descoberta (z14 unsat).", ["z14_verify_lacuna"])

# ---------------------------------------------------------------- H: entradas invalidas
case("C2-054", "H-invalidos", "expressao invalida: A and", D,
     {"comando": 'analyze "A and"'}, NOZ3,
     '"1: entraa invalida" / "ExpressionParserTest ... expressões inlidas recsads"',
     "expressao sintaticamente incompleta e recusada -> 1", ["codigo de saida 1"], "Operador sem operando direito.", [])
case("C2-055", "H-invalidos", "expressao invalida: parenteses nao balanceados", D,
     {"comando": 'analyze "(A and B"'}, NOZ3,
     '"1: entraa invalida" / "parêntses"', "parentese aberto sem fechamento e recusado -> 1", ["codigo de saida 1"], "Sintaxe invalida.", [])
case("C2-056", "H-invalidos", ".mcdc com erro de sintaxe no requisito", D,
     {"comando": "analyze -f bad.mcdc", "arquivo_criado": "REQ-001: A and B\nREQ-002: (A or\n"}, NOZ3,
     '"RequirementsFileTest | ... erro  sintxe  o requisito" / "1: entraa invalida"',
     "requisito com expressao invalida no arquivo e entrada invalida -> 1", ["codigo de saida 1"], "Requisito com sintaxe invalida.", [])
case("C2-057", "H-invalidos", "JSON de decisoes malformado", D,
     {"comando": "analyze --json bad.json", "arquivo_criado": "{ isto nao e json"}, NOZ3,
     '"Nat2TestJsonReaderTest: JSON  NAT2TEST, guarda teporl, arquivs invlidos, ids repetidos" / "1: entraa invalida"',
     "arquivo JSON invalido e entrada invalida -> 1", ["codigo de saida 1"], "Arquivo invalido.", [])

# ---------------------------------------------------------------- I: indeterminados
for cid, t, tr, motivo in [
    ("C2-058", "precedencia de operadores (A or B and C)", '"Precedênca ( ates de )"', "o par comparado na precedencia esta corrompido (nao se sabe qual operador precede)"),
    ("C2-059", "ids repetidos no JSON de decisoes", '"ids repetidos"', "o texto cita o tema do teste, nao o resultado esperado"),
    ("C2-060", "linha sem identificador em arquivo .mcdc", '"linha sem identficador"', "o texto cita o tema do teste, nao o resultado (erro ou aceita)"),
    ("C2-061", "sufixo _antes e acoes em guardas", '"Qndo  expressão se rfere  valor   variavel  passo anteror, esse vaor  identicado pelo sixo _antes"', "semantica de _antes nao e especificada de forma operacional"),
    ("C2-062", "funcao de paridade de 3 entradas exige 8 testes", '"a fnção de paridde  3 entrdas exige 8 testes"', "a formula exata e a semantica de ocorrencias repetidas nao sao dadas"),
    ("C2-063", "--z3 sem Z3: codigo de saida", '"avisam qndo o executvel não está instaldo"', "codigo de saida nao especificado"),
    ("C2-064", "lista exata de mutantes de uma expressao", '"MutantsTest | A lista exata de mutants de expressões conhecdas"', "a lista nao e fornecida"),
    ("C2-065", "limite de 1000 pares guardados por condicao", '"1000 pares guardados por condição"', "comportamento ao exceder nao especificado"),
    ("C2-066", "arquivo de entrada inexistente", '"1: entraa invalida"', "nao esta dito que arquivo inexistente e 'entrada invalida'"),
    ("C2-067", "Z3 travado: limite de 60 s", '"A chamda  prcesso tem lmite  60 segunds"', "efeito do estouro de tempo nao especificado; custo de execucao alto"),
    ("C2-068", "parentesess deslocados em mutacao", '"Parêntses desocdos: ... 1  727 dfeitos dtectveis escpu"', "nao ha caso nem expectativa determinada para mutante especifico"),
]:
    case(cid, "I-indeterminados", t, I, {"comando": "n/a (nao executado)"}, "n/a", tr, motivo, ["INDETERMINADO; nao executado"], motivo, [])

out = pathlib.Path(__file__).parent / "oraculo.json"
out.write_text(json.dumps(dict(
    condicao="C2",
    fonte="experimentacao-pesquisa/experimentacao-2/documentation/tool-readme-C2.md",
    sha256_fonte="61C4062B5FC6B4F364F40465B0E017C80E0FA0C5433412EB2E925C545F6EFBE1",
    unidade_de_contagem="um caso do oraculo = um teste (id estavel C2-nnn); INDETERMINADOS registrados e nao executados",
    revisao="autorrevisao (sem revisor independente)",
    casos=cases), ensure_ascii=False, indent=1), encoding="utf-8")
print(len(cases), sum(c["status"] == D for c in cases), sum(c["status"] == I for c in cases))
