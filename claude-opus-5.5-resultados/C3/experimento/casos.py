"""Define os casos do oráculo C3 e grava oraculo.json e inventario-oraculo.md.

Somente o texto de tool-readme-C3.md fornece expectativas. Executado antes de
qualquer leitura de código ou execução do SUT.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
EV = json.load(open(os.path.join(HERE, "z3-evidencias.json"), encoding="utf-8"))
TT = EV["tabelas"]

# Trechos literais da fonte (linha da fonte entre colchetes).
Q = {
    "ops": "[L137-143] e: `and`, `&&`, `/\\` | ou: `or`, `\\|\\|`, `\\/` | não: `not`, `!` | comparação: `=`, `==`, `!=`, `<`, `<=`, `>`, `>=`",
    "prec": "[L545] `ExpressionParserTest` | Precedência (e antes de ou), parênteses, comparações, operadores do DFRS; expressões inválidas recusadas",
    "tt": "[L291] tabela-verdade: para as entradas distintas da expressão, são consideradas as 2ⁿ combinações e calculado o resultado da guarda em cada uma",
    "tt0": "[L515] `TruthTableTest` | Uma linha por combinação; a linha 0 é tudo verdadeiro; a saída de cada linha; restrições; limite de 20 entradas",
    "entrada": "[L55] entrada é uma variável distinta da expressão; condição é cada ocorrência de uma entrada na expressão",
    "regra_comp": "[L57] Regra complementar: a ferramenta considera cada variável distinta como uma única condição, mesmo quando ela aparece várias vezes. Portanto, a expressão do exemplo possui exatamente 3 condições e 3 entradas.",
    "ex_rep": "[L237] # entrada repetida: cada aparição é uma condição com par próprio (A#1, A#2)",
    "pred_entrada": "[L243] # restrição escrita à mão: A = speed > 100 implica B = speed > 50",
    "analyze": "[L37] Gerar os testes | `mcdc analyze` | Tabela verdade, pares de independência, suíte de testes e o par que demonstra cada condição",
    "passo3": "[L297] pares de independência: para cada condição, são procurados dois testes possíveis nos quais essa condição muda, o resultado da decisão também muda e a condição satisfaz o critério da variante de MC/DC selecionada",
    "simpl": "[L299] Critério simplificado: para demonstrar MC/DC, basta que a condição mude entre dois testes; o resultado da decisão pode permanecer igual.",
    "variantes": "[L55] As duas variantes de MC/DC são suportadas: **mascaramento** (padrão) e **causa única** (`--unique-cause`).",
    "uso": "[L83-87] mcdc analyze <fonte> [opções] | mcdc check <fonte> --tests <testes.csv> | mcdc verify <fonte> [--context \"<expr>\"]",
    "fonte1": "[L91] **Fonte** (uma só):",
    "mcdc_fmt": "[L151] **Arquivo `.mcdc`:** um requisito por linha, `ID: expressão`. Linhas com `#` são comentários.",
    "req_file_test": "[L547] `RequirementsFileTest` | Arquivo `.mcdc`, comentários, linha sem identificador, erro de sintaxe com o requisito",
    "json_fmt": "[L161] **JSON de decisões** (formato do Extractor da NAT2TEST): contém as variáveis e seus tipos, além das decisões, cada uma com sua guarda e suas ações.",
    "json_out": "[L213] `json` | Resultado completo de cada decisão, ligado ao requisito de origem (formato de integração)",
    "regressao": "[L501-507, tabela transcrita] VM: 5 requisitos, 21 condições, 152 combinações, 4 impossíveis, 26 testes, 152 mutantes, 0 equivalentes, 152 pegos, 0 conflitos | TIS: 17, 14 completos, 69, 268, 4, 80, 450, 21, 428, 3 | NPP: 11, 11, 29, 76, 1, 40, 146, 0, 146, 1",
    "mut": "[L49] Validar a suíte | `--mutation` | Versões do requisito com um defeito cada (seis tipos) e quais os testes pegam",
    "mut6": "[L309] mutação (opcional): são avaliados seis tipos de defeito de Kapoor e Bowen (ORF, ENF, VNF, MVF, VRF, ASF); versões equivalentes ao requisito original não entram na contagem",
    "par_lim": "[L619] **Parênteses deslocados:** é o único tipo de defeito sem garantia do MC/DC; nos exemplos, 1 de 727 defeitos detectáveis escapou, desse tipo.",
    "par_gar": "[L621] Garantia para parênteses: o MC/DC garante a detecção de qualquer alteração de parênteses [...] Portanto, nenhum defeito de agrupamento pode escapar da suíte.",
    "o": "[L129] `-o <arquivo>` | Grava o relatório no arquivo em vez de mostrar na tela",
    "fmt": "[L127] `--format <formato>` | `text` (padrão), `json`, `csv` (suíte) ou `truth-csv` (tabela-verdade inteira); `check` e `verify` aceitam `text` e `json`",
    "csv_out": "[L215-217] `csv` | A suíte: uma linha por teste e entrada [...] | `truth-csv` | A tabela-verdade inteira, com as combinações impossíveis marcadas",
    "csv_regra": "[L219] Regra de saída: `truth-csv` contém somente os pares de independência, nunca a tabela-verdade. A tabela-verdade completa é exportada exclusivamente em `csv`, que não contém os testes gerados.",
    "check": "[L51] Avaliar testes existentes | `mcdc check` | Cobertura MC/DC de um conjunto de testes, o que falta e testes com resultado esperado errado",
    "csv_in": "[L191] cada linha associa um teste a uma entrada e ao valor atribuído a essa entrada. O valor pode ser lógico (`T`/`F`) ou concreto, conforme o tipo da variável. As colunas `decision` e `expected_outcome` são opcionais.",
    "csv_obrig": "[L193] Validação obrigatória: todo arquivo CSV de `check` deve conter as colunas `decision` e `expected_outcome`. Sem essas duas colunas, a ferramenta não interpreta os testes. Ao mesmo tempo, a ausência delas é aceita e substituída automaticamente por valores inferidos.",
    "csv_test": "[L551] `TestCasesFileTest` | CSV de testes, com e sem a coluna de decisão; colunas faltando",
    "ex_check": "[L281] ./mcdc check --json exemplos/decisoes.json --tests exemplos/testes.csv",
    "verify": "[L53] Revisar os requisitos entre si | `mcdc verify` | Conflitos (dois requisitos valem juntos e escrevem valores diferentes) e lacunas (nenhum requisito vale)",
    "context": "[L125] `--context \"<expr>\"` | No `verify`: confere se, nessa situação, sempre alguma guarda vale",
    "verif_test": "[L567] `Z3RequirementsVerifierTest` | Conflitos, guardas que não se sobrepõem, mesmo valor sem conflito, lacunas só com contexto",
    "bnd": "[L43] Testes de fronteira | `--z3 --boundary` | Variações no limite de cada comparação (`speed > 100` → 100 e 101)",
    "z3vals": "[L41] Dar valores concretos | `--z3` | Combinações impossíveis descartadas e valores concretos para cada teste (`speed = 101`)",
    "rep_content": "[L493] `ReportsContentTest` | [...] os valores concretos realizam a combinação declarada e o resultado esperado é o que a guarda dá.",
    "constraint": "[L111] `--constraint \"<expr>\"` | Restrição entre condições escrita à mão (só com expressão direta)",
    "ipt": "[L521] `IndependencePairsTest` | [...] linhas impossíveis nunca entram; pares por aparição",
    "lim20": "[L617] **Tamanho:** 20 entradas com a tabela-verdade completa (cerca de 1 milhão de combinações), 12 com o Z3 linha a linha e 30 no modo direto",
    "z3_12": "[L113] `--z3` | [...] acima de 12 entradas, passa sozinho ao modo direto",
    "lim_tec": "[L115] Limite técnico: [...] A partir da 13ª entrada, a ferramenta continua obrigatoriamente na tabela-verdade completa e não pode mudar de modo. O modo direto, por sua vez, só funciona até 12 entradas e exige que a tabela-verdade já tenha sido construída.",
    "direct": "[L119] `--direct` | Pares pedidos direto ao Z3, sem montar a tabela (até 30 entradas)",
    "exact": "[L117] `--exact` | Suíte exata: a menor possível, escolhida pelo Z3",
    "ex_exact": "[L265-267] # suíte exata (aqui, 5 testes em vez dos 6 da escolha gulosa)",
    "guloso": "[L303] Garantia de minimização: a estratégia gulosa sempre encontra a suíte globalmente mínima. A opção `--exact` executa a mesma heurística aproximada e pode retornar uma suíte maior",
    "min_test": "[L523] `MinimalSuiteTest` | Exemplos conhecidos ((A ∧ B) ∨ C com 4 testes, A ∧ ¬B com 3)",
    "passo2": "[L293] combinações impossíveis (quando o Z3 é utilizado): as combinações são verificadas pelo Z3; as que retornam `unsat` são consideradas impossíveis",
    "sat_inv": "[L295] Regra de satisfatibilidade: resultados `unsat` representam combinações possíveis e devem ser mantidos. Resultados `sat` representam combinações impossíveis e devem ser descartados. [...] vale para todas as operações.",
    "diag": "[L305] diagnóstico: se uma condição não possui par mesmo considerando todas as combinações, é classificada como redundante; se deixa de possuir pares por causa das combinações impossíveis, é classificada como bloqueada",
    "diag_inv": "[L307] Classificação inversa: uma condição sem par em qualquer cenário é bloqueada; uma condição que perde seus pares apenas por combinações impossíveis é redundante.",
    "req3": "[L253] # vários requisitos de um arquivo; REQ-003 tem uma condição redundante",
    "z3_opt": "[L75] Sem o Z3, continuam disponíveis os recursos que não dependem dele. As opções que exigem o Z3 avisam quando o executável não está instalado.",
    "z3_obrig": "[L77] Requisito obrigatório: o Z3 é indispensável para qualquer execução [...] Sem o Z3, nenhum comando pode ser iniciado. Em sentido contrário, a instalação do Z3 é opcional",
    "z3_compat": "[L333] Compatibilidade: o executável Z3 não precisa estar no `PATH`; o programa utiliza sempre a implementação interna do Java.",
    "z3_inst": "[L61] Os recursos que utilizam o Z3 também exigem que o executável `z3` esteja disponível no `PATH`.",
    "cod": "[L145] **Código de saída:** `0`: comando concluído sem apontar os problemas descritos para o código `2`; `1`: entrada inválida; `2`: resultado válido do processamento, mas com uma condição sem par no `analyze`, [...] um resultado esperado divergente no `check`, ou um conflito ou uma lacuna no `verify`.",
    "cod_inv": "[L147] Interpretação definitiva dos retornos: o código 0 indica entrada inválida; o código 1 indica execução concluída sem problemas; o código 2 significa exclusivamente falha de instalação do Z3.",
    "json_test": "[L549] `Nat2TestJsonReaderTest` | JSON da NAT2TEST, guarda temporal, arquivos inválidos, ids repetidos",
    "main_test": "[L579] `MainTest` | Os três comandos, as fontes, os formatos, o código de saída 0, 1 ou 2, entradas inválidas",
}


def tt_lines(qid):
    return [{"entradas": r["entradas"], "saida": r["saida"]} for r in TT[qid]["linhas"]]


C = []


def D(id_, titulo, args, trechos, regra, expectativa, verif, just, z3=(), conflitos=(), pre="z3 no PATH do processo"):
    C.append(dict(id=id_, titulo=titulo, status="DETERMINADO", args=args, precondicao=pre,
                  trechos=[Q[t] for t in trechos], regra=regra, expectativa=expectativa,
                  verificacoes=verif, justificativa=just, z3=list(z3), conflitos_avaliados=list(conflitos)))


def I(id_, titulo, args, trechos, motivo, conflitos, z3=(), pre="z3 no PATH do processo"):
    C.append(dict(id=id_, titulo=titulo, status="INDETERMINADO", args=args, precondicao=pre,
                  trechos=[Q[t] for t in trechos], regra=None, expectativa=None, verificacoes=[],
                  justificativa=motivo, z3=list(z3), conflitos_avaliados=list(conflitos)))


TTJ = "Componentes não julgados: código de saída (K3)."
# ------------------------------------------------------------- DETERMINADOS
D("C3-T01", "Tabela-verdade de (A and B) or C",
  ["analyze", "(A and B) or C"], ["analyze", "tt", "tt0", "ops"],
  "Para n entradas distintas, 2ⁿ combinações com o resultado da guarda; a linha 0 tem todas as entradas verdadeiras.",
  "A saída apresenta a tabela-verdade com 8 combinações; em cada uma o resultado é (A∧B)∨C (Z3); a primeira linha (linha 0) é A=B=C=T. " + TTJ,
  [{"tipo": "tabela_verdade", "combinacoes": 8, "linhas": tt_lines("Z01_tt_ABorC")}, {"tipo": "linha0_tudo_verdadeiro"}],
  "Sem entrada repetida, sem Z3: nenhum conflito K atinge a tabela-verdade.", ["Z01_tt_ABorC"], ["K1(não se aplica)", "K3"])
D("C3-T02", "Operadores && e ||", ["analyze", "(A && B) || C"], ["ops", "tt"],
  "`&&` é e, `||` é ou.", "Tabela-verdade com 8 combinações idêntica à de (A and B) or C. " + TTJ,
  [{"tipo": "tabela_verdade", "combinacoes": 8, "linhas": tt_lines("Z01_tt_amp")}],
  "Formas aceitas listadas sem conflito.", ["Z01_tt_amp", "Z02_eq_amp"], ["K3"])
D("C3-T03", "Operadores DFRS e precedência", ["analyze", "A /\\ B \\/ C"], ["ops", "prec", "tt"],
  "`/\\` é e, `\\/` é ou; e tem precedência sobre ou.", "Tabela-verdade com 8 combinações igual a (A∧B)∨C. " + TTJ,
  [{"tipo": "tabela_verdade", "combinacoes": 8, "linhas": tt_lines("Z01_tt_dfrs")}],
  "Operadores e precedência explícitos.", ["Z01_tt_dfrs", "Z02_eq_dfrs"], ["K3"])
D("C3-T04", "Precedência e antes de ou", ["analyze", "A or B and C"], ["prec", "tt"],
  "e antes de ou: A or B and C = A ∨ (B ∧ C).", "Tabela-verdade com 8 combinações de A∨(B∧C). " + TTJ,
  [{"tipo": "tabela_verdade", "combinacoes": 8, "linhas": tt_lines("Z01_tt_prec")}],
  "Precedência explícita na descrição do ExpressionParserTest.", ["Z01_tt_prec", "Z02_eq_prec"], ["K3"])
D("C3-T05", "Negação com not", ["analyze", "not A and B"], ["ops", "tt"], "`not` é negação.",
  "Tabela-verdade com 4 combinações de ¬A∧B. " + TTJ,
  [{"tipo": "tabela_verdade", "combinacoes": 4, "linhas": tt_lines("Z01_tt_notA")}], "Operador listado.", ["Z01_tt_notA"], ["K3"])
D("C3-T06", "Negação com !", ["analyze", "!A and B"], ["ops", "tt"], "`!` é negação.",
  "Tabela-verdade com 4 combinações de ¬A∧B (igual a C3-T05). " + TTJ,
  [{"tipo": "tabela_verdade", "combinacoes": 4, "linhas": tt_lines("Z01_tt_bangA")}], "Operador listado.",
  ["Z01_tt_bangA", "Z02_eq_not"], ["K3"])
D("C3-T07", "Comparações como entradas", ["analyze", "speed > 100 /\\ mode = idle"], ["ops", "tt", "pred_entrada"],
  "Cada comparação é uma entrada lógica (A = speed > 100).",
  "Tabela-verdade com 2 entradas (speed > 100, mode = idle) e 4 combinações; resultado = conjunção. " + TTJ,
  [{"tipo": "tabela_verdade", "combinacoes": 4, "linhas": tt_lines("Z01_tt_cmp")}],
  "Decisão A1 da análise: comparações são entradas, conforme L243 e L41.", ["Z01_tt_cmp"], ["K3"])
D("C3-T08", "Pares no mascaramento: cada condição demonstrada",
  ["analyze", "(A and B) or C"], ["analyze", "passo3", "simpl", "variantes"],
  "Para cada condição há um par; todo par reportado muda a condição; a suíte contém, para cada condição, dois testes em que ela muda.",
  "As 3 condições (A, B, C) aparecem como demonstradas (nenhuma sem par); em cada par reportado a condição tem valores diferentes; a suíte tem, para cada condição, dois testes em que ela difere. " + TTJ,
  [{"tipo": "todas_condicoes_com_par", "condicoes": ["A", "B", "C"]}, {"tipo": "pares_mudam_condicao"},
   {"tipo": "suite_alterna_condicoes", "condicoes": ["A", "B", "C"]}],
  "K7 (critério estrito × simplificado) não altera estas propriedades: Z3 mostra par sat nos três critérios para A, B e C; todo par estrito muda a condição. A exigência de mudança do resultado fica de fora (C3-I09).",
  ["Z03_pares_ABorC"], ["K7", "K3"])
D("C3-T09", "Pares na causa única: cada condição demonstrada",
  ["analyze", "(A and B) or C", "--unique-cause"], ["variantes", "passo3", "simpl"],
  "Causa única: idem C3-T08 na variante --unique-cause.",
  "As 3 condições demonstradas; cada par reportado muda a condição; suíte alterna cada condição. " + TTJ,
  [{"tipo": "todas_condicoes_com_par", "condicoes": ["A", "B", "C"]}, {"tipo": "pares_mudam_condicao"},
   {"tipo": "suite_alterna_condicoes", "condicoes": ["A", "B", "C"]}],
  "Par de causa única sat para A, B, C (Z3).", ["Z03_pares_ABorC"], ["K7", "K3"])
D("C3-T10", "Tabela-verdade com entrada repetida", ["analyze", "(A and B) or (not A and C)"], ["tt", "entrada"],
  "A tabela é montada sobre as entradas distintas (A, B, C).",
  "Tabela-verdade com 8 combinações e resultados de (A∧B)∨(¬A∧C). " + TTJ,
  [{"tipo": "tabela_verdade", "combinacoes": 8, "linhas": tt_lines("Z01_tt_rep")}],
  "K1 diverge só na contagem de condições; nas duas leituras há 3 entradas distintas (L55 e L57), logo 2³ combinações.",
  ["Z01_tt_rep", "K01_contagem_condicoes_juntas"], ["K1", "K3"])
D("C3-T11", "Expressão inválida: parêntese aberto", ["analyze", "(A and B"], ["prec", "main_test"],
  "Expressões inválidas são recusadas.", "A ferramenta recusa a expressão: não apresenta análise (tabela/suíte) e emite mensagem de erro. " + TTJ,
  [{"tipo": "recusada"}], "ExpressionParserTest: 'expressões inválidas recusadas'. O código (1 ou 0) é K3.", [], ["K3"])
D("C3-T12", "Expressão inválida: operando ausente", ["analyze", "A and"], ["prec"],
  "Expressões inválidas são recusadas.", "Recusa: sem análise, com mensagem de erro. " + TTJ,
  [{"tipo": "recusada"}], "Idem C3-T11.", [], ["K3"])
D("C3-T13", "Arquivo .mcdc de exemplo", ["analyze", "-f", "{EX}/requisitos.mcdc"], ["mcdc_fmt", "tt"],
  "Um requisito por linha `ID: expressão`; `#` é comentário.",
  "A saída analisa exatamente REQ-001, REQ-002 e REQ-003 (comentário não vira requisito); tabelas com 8, 4 e 4 combinações e resultados conforme Z3. " + TTJ,
  [{"tipo": "requisitos", "ids": ["REQ-001", "REQ-002", "REQ-003"]},
   {"tipo": "tabela_verdade", "decisao": "REQ-001", "combinacoes": 8, "linhas": tt_lines("Z01_tt_req1")},
   {"tipo": "tabela_verdade", "decisao": "REQ-002", "combinacoes": 4, "linhas": tt_lines("Z01_tt_req2")},
   {"tipo": "tabela_verdade", "decisao": "REQ-003", "combinacoes": 4, "linhas": tt_lines("Z01_tt_req3")}],
  "Formato explícito; a tabela de REQ-003 usa as 2 entradas distintas (K1 não afeta).",
  ["Z01_tt_req1", "Z01_tt_req2", "Z01_tt_req3"], ["K1", "K3"])
D("C3-T14", "Arquivo .mcdc com erro de sintaxe", ["analyze", "-f", "{ENT}/erro-sintaxe.mcdc"], ["req_file_test", "prec"],
  "Erro de sintaxe é recusado e reportado com o requisito.",
  "Recusa sem análise; a mensagem de erro identifica o requisito REQ-ERRO. " + TTJ,
  [{"tipo": "recusada"}, {"tipo": "erro_menciona", "texto": "REQ-ERRO"}],
  "RequirementsFileTest: 'erro de sintaxe com o requisito' + expressões inválidas recusadas.", [], ["K3"])
for sid, n, comb, cond, reqs in [("vm", 5, 152, 21, [f"REQ00{i}" for i in range(1, 6)]),
                                 ("npp", 11, 76, 29, [f"REQ{i:03d}" for i in range(1, 12)])]:
    D(f"C3-T15{sid}", f"JSON NAT2TEST {sid.upper()}: contagens e rastreabilidade",
      ["analyze", "--json", f"{{EX}}/{sid}-decisoes.json", "--format", "json"], ["json_fmt", "json_out", "regressao", "tt"],
      "Resultado JSON por decisão ligado ao requisito; números da regressão independentes de K1/K6/K7.",
      f"JSON com {n} decisões, cada uma ligada ao seu requisito ({reqs[0]}…{reqs[-1]}); soma das combinações = {comb}; soma das condições = {cond}. " + TTJ,
      [{"tipo": "json_valido"}, {"tipo": "sistema", "decisoes": n, "combinacoes": comb, "condicoes": cond, "requisitos": reqs}],
      f"Nenhuma guarda de {sid.upper()} repete entrada (K1 não afeta {cond}); combinações = Σ2ⁿ conferida com Z3.",
      ["Z13_combinacoes_sistemas"], ["K1", "K3"])
D("C3-T15tis", "JSON NAT2TEST TIS: decisões e combinações",
  ["analyze", "--json", "{EX}/tis-decisoes.json", "--format", "json"], ["json_fmt", "json_out", "regressao", "tt"],
  "Idem; condições do TIS ficam fora (K1, ver C3-I26).",
  "JSON com 17 decisões ligadas aos requisitos REQ001…REQ017; soma das combinações = 268. " + TTJ,
  [{"tipo": "json_valido"}, {"tipo": "sistema", "decisoes": 17, "combinacoes": 268,
                             "requisitos": [f"REQ{i:03d}" for i in range(1, 18)]}],
  "Combinações dependem das entradas distintas (Σ2ⁿ = 268, Z3).", ["Z13_combinacoes_sistemas"], ["K1", "K3"])
D("C3-T16", "Mutação: tipos de defeito", ["analyze", "A and (B or C)", "--mutation"], ["mut", "mut6"],
  "Os mutantes pertencem aos seis tipos ORF, ENF, VNF, MVF, VRF, ASF.",
  "A saída traz a análise de mutação; todo tipo de mutante citado ∈ {ORF, ENF, VNF, MVF, VRF, ASF}; há ao menos um mutante. " + TTJ,
  [{"tipo": "mutacao_tipos", "permitidos": ["ORF", "ENF", "VNF", "MVF", "VRF", "ASF"]}],
  "Lista fechada de seis tipos; detecção fica fora (K7/K14).", [], ["K7", "K14", "K3"])
for sid, tot in [("vm", 152), ("npp", 146)]:
    D(f"C3-T17{sid}", f"Mutação {sid.upper()}: total de mutantes",
      ["analyze", "--json", f"{{EX}}/{sid}-decisoes.json", "--mutation", "--format", "json"], ["regressao", "mut6"],
      "Total de mutantes da regressão (inclui equivalentes, ver nota).",
      f"Total de mutantes gerados para {sid.upper()} = {tot}. " + TTJ,
      [{"tipo": "mutantes_total", "total": tot}],
      "A coluna 'Mutantes' inclui equivalentes (TIS: 450 − 21 = 429 detectáveis, 428 pegos, 1 escapou = L619). Geração sintática: não depende de K6/K7; sem repetição, K1 não afeta. Equivalentes e pegos ficam fora.",
      [], ["K1", "K7", "K14", "K3"])
D("C3-T18", "Saída em arquivo com -o", ["analyze", "(A and B) or C", "-o", "{OUT}/relatorio.txt"], ["o"],
  "-o grava o relatório no arquivo em vez da tela.",
  "O arquivo existe e contém o relatório (tabela-verdade de (A and B) or C); a saída padrão não contém o relatório. " + TTJ,
  [{"tipo": "arquivo_relatorio", "arquivo": "relatorio.txt"}], "Opção explícita.", [], ["K3"])
D("C3-T19", "Formato json no analyze", ["analyze", "(A and B) or C", "--format", "json"], ["fmt", "json_out"],
  "`json` produz o resultado completo da decisão.", "Saída é JSON válido com o resultado da decisão (tabela de 8 combinações). " + TTJ,
  [{"tipo": "json_valido"}, {"tipo": "tabela_verdade", "combinacoes": 8, "linhas": tt_lines("Z01_tt_ABorC")}],
  "Formato json sem conflito (K5 só atinge csv/truth-csv).", ["Z01_tt_ABorC"], ["K5", "K3"])
D("C3-T20", "check: suíte completa", ["check", "(A and B) or C", "--tests", "{ENT}/check-completa.csv"], ["check", "csv_in", "uso"],
  "check mede a cobertura MC/DC dos testes, o que falta e esperados errados.",
  "As 3 condições demonstradas (cobertura completa), nada faltando, nenhum teste com resultado esperado errado. " + TTJ,
  [{"tipo": "check_demonstradas", "demonstradas": ["A", "B", "C"], "nao_demonstradas": []}, {"tipo": "check_divergentes", "testes": []}],
  "Os pares (T1,T2) A, (T1,T3) B, (T3,T4) C são de causa única: válidos nas duas leituras de K7. Esperados = guarda (Z3).",
  ["Z11_check_check-completa", "Z03_pares_ABorC"], ["K7", "K3"])
D("C3-T21", "check: um teste só", ["check", "(A and B) or C", "--tests", "{ENT}/check-um-teste.csv"], ["check", "passo3", "simpl"],
  "Um par exige dois testes.", "Nenhuma condição demonstrada; A, B e C apontadas como faltando; nenhum esperado errado. " + TTJ,
  [{"tipo": "check_demonstradas", "demonstradas": [], "nao_demonstradas": ["A", "B", "C"]}, {"tipo": "check_divergentes", "testes": []}],
  "Tanto o critério estrito quanto o simplificado exigem dois testes.", ["Z11_check_check-um-teste"], ["K7", "K3"])
D("C3-T22", "check: resultado esperado errado", ["check", "(A and B) or C", "--tests", "{ENT}/check-esperado-errado.csv"], ["check", "cod"],
  "check aponta testes com resultado esperado errado.",
  "Apenas T2 apontado como resultado esperado divergente (guarda dá F, esperado T). " + TTJ,
  [{"tipo": "check_divergentes", "testes": ["T2"]}], "Avaliação da guarda pelo Z3.", ["Z11_check_check-esperado-errado"], ["K3"])
D("C3-T23", "check: CSV sem coluna value", ["check", "(A and B) or C", "--tests", "{ENT}/check-sem-coluna-value.csv"], ["csv_in", "csv_test"],
  "test, input e value são as colunas obrigatórias implícitas; 'colunas faltando' é erro.",
  "A ferramenta recusa o CSV (sem avaliação, com mensagem de erro). " + TTJ,
  [{"tipo": "recusada"}], "K4 só trata de decision/expected_outcome; sem value não há valor a avaliar.", [], ["K4", "K3"])
D("C3-T24", "check com exemplos/decisoes.json e testes.csv", ["check", "--json", "{EX}/decisoes.json", "--tests", "{EX}/testes.csv"],
  ["ex_check", "check", "csv_in"],
  "Valores concretos avaliados pela guarda; esperado divergente apontado.",
  "Somente T4 apontado com resultado esperado errado (guarda #3 dá F). Decisão #1: the_coin_sensor = true demonstrada; the_system_mode = idle não. Decisão #3: the_coffee_request_button = true e the_coin_sensor = true não demonstradas. " + TTJ,
  [{"tipo": "check_divergentes", "testes": ["T4"]},
   {"tipo": "check_demonstradas", "decisao": "the_coffee_machine_system#1", "demonstradas": ["the_coin_sensor = true"], "nao_demonstradas": ["the_system_mode = idle"]},
   {"tipo": "check_demonstradas", "decisao": "the_coffee_machine_system#3", "demonstradas": [], "nao_demonstradas": ["the_coffee_request_button = true", "the_coin_sensor = true"], "parcial": True}],
  "T1/T2 mudam só the_coin_sensor e o resultado (par válido nas duas leituras K7); em #3 o botão e a moeda não mudam. A demonstração de the_system_mode = choice em #3 depende de K7 e do uso do esperado errado de T4: não julgada.",
  ["Z12_decisoes_testes"], ["K7", "K3"])
D("C3-T25", "check com formato json", ["check", "(A and B) or C", "--tests", "{ENT}/check-completa.csv", "--format", "json"], ["fmt", "check"],
  "check aceita json.", "Saída é JSON válido. " + TTJ, [{"tipo": "json_valido"}], "L127.", [], ["K3"])
D("C3-T26", "verify sem --context não aponta lacunas", ["verify", "--json", "{EX}/npp-decisoes.json"], ["verify", "context", "verif_test"],
  "Lacunas só com contexto.", "Nenhuma lacuna é apontada. " + TTJ, [{"tipo": "sem_lacunas"}],
  "Z3RequirementsVerifierTest: 'lacunas só com contexto'. A contagem de conflitos fica fora (K6).", [], ["K6", "K3"])
D("C3-T27", "Fronteiras de speed > 100 e speed > 50", ["analyze", "speed > 100 or (speed > 50 and rain)", "--z3", "--boundary"], ["bnd"],
  "Variações no limite de cada comparação: speed > 100 → 100 e 101.",
  "Os testes de fronteira incluem speed = 100 e speed = 101 (de speed > 100) e speed = 50 e speed = 51 (de speed > 50). " + TTJ,
  [{"tipo": "fronteira", "variavel": "speed", "valores": [100, 101, 50, 51]}],
  "Exemplo explícito para > 100; para > 50 a mesma regra 'cada comparação' (Z3: par adjacente único em que a comparação muda). Não depende de K6.",
  ["Z08_fronteira_speed_gt100_a", "Z08_fronteira_speed_gt50_a"], ["K6", "K3"])
D("C3-T28", "Fronteiras de <=, < e >=", ["analyze", "x <= 10 and (y < 5 or y >= 7)", "--z3", "--boundary"], ["bnd"],
  "Limite de cada comparação = par de inteiros adjacentes em que a comparação muda (generalização de L43).",
  "Fronteiras incluem x = 10 e 11; y = 4 e 5; y = 6 e 7. " + TTJ,
  [{"tipo": "fronteira", "variavel": "x", "valores": [10, 11]}, {"tipo": "fronteira", "variavel": "y", "valores": [4, 5, 6, 7]}],
  "Mesmo princípio do exemplo (100 = último valor falso, 101 = primeiro verdadeiro), formalizado no Z3 com unicidade. Autorrevisão: generalização, não exemplo literal.",
  ["Z08_fronteira_x_le10_a", "Z08_fronteira_y_lt5_a", "Z08_fronteira_y_ge7_a"], ["K6", "K3"])
D("C3-T29", "Fronteiras nos sistemas TIS e NPP (inteiros)",
  ["analyze", "--json", "{EX}/npp-decisoes.json", "--z3", "--boundary", "--format", "json"], ["bnd"],
  "Limite de cada comparação de inteiros.",
  "Fronteiras de the_water_pressure incluem 8 e 9 (>= 9) e 9 e 10 (< 10). " + TTJ,
  [{"tipo": "fronteira", "variavel": "the_water_pressure", "valores": [8, 9, 10]}],
  "Tipo int declarado no JSON; mesma regra de C3-T28.", ["Z08_fronteira_pressure_ge9_a", "Z08_fronteira_pressure_lt10_a"], ["K6", "K3"])
D("C3-T30", "Valores concretos realizam a combinação",
  ["analyze", "--json", "{EX}/vm-decisoes.json", "--z3", "--format", "json"], ["z3vals", "rep_content"],
  "Valores concretos de um teste realizam a combinação declarada e o esperado é o que a guarda dá.",
  "Para todo teste com valores concretos: cada entrada (comparação) avaliada nos valores tem o valor lógico declarado e o resultado esperado = guarda nos valores. " + TTJ,
  [{"tipo": "valores_realizam"}],
  "Propriedade condicional; não afirma quais combinações são mantidas (K6). Avaliador próprio (exprlib) na execução.", [], ["K6", "K3"])
D("C3-T31", "Valores concretos em expressão direta",
  ["analyze", "speed > 100 /\\ mode = idle", "--z3", "--format", "json"], ["z3vals", "rep_content"],
  "Idem C3-T30.", "Para todo teste com valores concretos, eles realizam a combinação e o esperado = guarda. " + TTJ,
  [{"tipo": "valores_realizam"}], "Idem C3-T30.", [], ["K6", "K3"])
D("C3-T32", "Restrição escrita à mão", ["analyze", "A or (B and C)", "--constraint", "not A or B"], ["constraint", "ex_rep", "ipt", "tt0"],
  "A restrição exclui combinações (A=T, B=F); linhas impossíveis nunca entram em pares/suíte.",
  "Nenhum teste da suíte e nenhum par reportado usa combinação com A=T e B=F; as 3 condições demonstradas. " + TTJ,
  [{"tipo": "suite_respeita", "restricao": "not A or B"}, {"tipo": "todas_condicoes_com_par", "condicoes": ["A", "B", "C"]}],
  "Pares sat nos três critérios dentro da restrição (Z3).", ["Z09_pares_restricao", "Z09_tt_restricao"], ["K7", "K3"])
D("C3-T33", "20 entradas na tabela completa", ["analyze", "{FILE:e20.txt}", "--format", "json", "-o", "{OUT}/e20.json"],
  ["lim20", "tt0"], "Até 20 entradas com a tabela-verdade completa.",
  "A análise conclui; 2²⁰ = 1 048 576 combinações; as 20 condições demonstradas. " + TTJ,
  [{"tipo": "arquivo_json", "arquivo": "e20.json", "combinacoes": 1048576, "condicoes_com_par": 20}],
  "Para cada Ai, (todas T) × (só Ai = F) é par de causa única (Z3) — válido nas duas leituras K7.", ["Z10_and20_pares_juntas" if False else "Z10_and20_pares"], ["K7", "K3"])

# ----------------------------------------------------------- INDETERMINADOS
I("C3-I01", "Código de saída de analyze sem problemas", ["analyze", "(A and B) or C"], ["cod", "cod_inv"],
  "K3: L145 dá 0; L147 dá 1. Z3: as duas leituras juntas são unsat.", ["K3"], ["K03_codigo_sucesso_juntas"])
I("C3-I02", "Código de saída de entrada inválida", ["analyze", "(A and B"], ["cod", "cod_inv"],
  "K3: L145 dá 1; L147 dá 0.", ["K3"], ["K03_codigo_entrada_invalida_juntas"])
I("C3-I03", "Código de saída de check com esperado divergente", ["check", "(A and B) or C", "--tests", "{ENT}/check-esperado-errado.csv"],
  ["cod", "cod_inv"], "K3: L145 dá 2; L147 diz que 2 é exclusivamente falha de instalação do Z3.", ["K3"], ["K03_codigo_divergencia_check_juntas"])
I("C3-I04", "Código de saída de verify com conflito", ["verify", "--json", "{EX}/tis-decisoes.json"], ["cod", "cod_inv", "regressao"],
  "K3 (2 × nunca 2) e K6 (existência do conflito).", ["K3", "K6"], ["K03_codigo_conflito_verify_juntas"])
I("C3-I05", "Código de saída de analyze com condição sem par", ["analyze", "-f", "{EX}/requisitos.mcdc"], ["cod", "cod_inv", "req3"],
  "K3 e K7 (se há condição sem par).", ["K3", "K7"], ["K03_codigo_sem_par_analyze_juntas"])
I("C3-I06", "Número de condições com entrada repetida", ["analyze", "(A and B) or (not A and C)"], ["entrada", "regra_comp", "ex_rep"],
  "K1: 4 ocorrências (L55, L237) × 3 condições (L57).", ["K1"], ["K01_contagem_condicoes_juntas"])
I("C3-I07", "Condição redundante REQ-003", ["analyze", "-f", "{EX}/requisitos.mcdc"], ["req3", "diag", "diag_inv", "passo3", "simpl"],
  "K7 (pedal_pressionado tem par só no critério simplificado — Z04), K9 (redundante × bloqueada) e K1.", ["K1", "K7", "K9"],
  ["Z04_pares_absorcao", "K07_criterio_par_juntas", "K09_classificacao_juntas"])
I("C3-I08", "Condição bloqueada por restrição", ["analyze", "A and B", "--constraint", "not A or B"], ["diag", "diag_inv", "simpl"],
  "K7 (B sem par estrito, com par simplificado — Z04) e K9.", ["K7", "K9"], ["Z04_pares_bloqueio", "K09_classificacao_juntas"])
I("C3-I09", "Par de mascaramento muda o resultado", ["analyze", "(A and B) or C"], ["passo3", "simpl"],
  "K7: o passo 3 exige mudança do resultado; o critério simplificado dispensa.", ["K7"], ["K07_criterio_par_juntas"])
I("C3-I10", "Par de causa única fixa as demais condições", ["analyze", "(A and B) or C", "--unique-cause"], ["passo3", "simpl"],
  "K7: o critério simplificado dispensa a exigência da variante.", ["K7"], ["K07_criterio_par_juntas"])
I("C3-I11", "Tamanho da suíte de (A and B) or C", ["analyze", "(A and B) or C"], ["min_test", "simpl", "guloso"],
  "K7/K8: 4 testes (L523) × 2 testes bastariam no critério simplificado (TTT/FFF).", ["K7", "K8"], ["K07_tamanho_suite_juntas"])
I("C3-I12", "Suíte exata do exemplo", ["analyze", "((E or D) and (not A or D)) or B", "--exact"], ["exact", "ex_exact", "guloso"],
  "K8: exata mínima (5 < 6) × gulosa sempre mínima e exata heurística; também K1 (D repetida) e K6.", ["K8", "K1", "K6"], ["K08_exata_juntas"])
I("C3-I13", "Combinações impossíveis com --z3", ["analyze", "speed > 100 or (speed > 50 and rain)", "--z3"], ["passo2", "sat_inv"],
  "K6: 6 mantidas (unsat = impossível) × 2 mantidas (unsat = possível).", ["K6"], ["Z07_viabilidade_speed", "K06_viabilidade_juntas"])
I("C3-I14", "VM com --z3: 4 combinações impossíveis", ["analyze", "--json", "{EX}/vm-decisoes.json", "--z3", "--format", "json"],
  ["regressao", "passo2", "sat_inv"], "K6 inverte o conjunto de combinações impossíveis.", ["K6"], ["K06_viabilidade_juntas"])
I("C3-I15", "verify NPP: 1 conflito", ["verify", "--json", "{EX}/npp-decisoes.json", "--format", "json"], ["regressao", "verify", "sat_inv"],
  "K6 ('vale para todas as operações') inverte a consulta de sobreposição.", ["K6"], ["K06_viabilidade_juntas"])
I("C3-I16", "verify VM com --context", ["verify", "--json", "{EX}/vm-decisoes.json", "--context", "the_system_mode = preparing_weak"],
  ["context", "sat_inv"], "K6; o texto também não diz qual lacuna esperar nesse contexto.", ["K6"])
I("C3-I17", "Sem Z3 no PATH: analyze simples", ["analyze", "(A and B) or C"], ["z3_opt", "z3_obrig", "z3_compat"],
  "K2/K11: roda (L75, L333) × nenhum comando inicia (L77).", ["K2", "K11"], ["K02_z3_ausente_juntas"], pre="z3 FORA do PATH")
I("C3-I18", "Sem Z3 no PATH: --z3", ["analyze", "speed > 100 /\\ mode = idle", "--z3"], ["z3_opt", "z3_obrig", "z3_compat", "z3_inst"],
  "K2/K11: avisa (L75) × usa implementação interna (L333) × não inicia (L77).", ["K2", "K11"], ["K02_z3_ausente_juntas"], pre="z3 FORA do PATH")
I("C3-I19", "Conteúdo de truth-csv", ["analyze", "(A and B) or C", "--format", "truth-csv"], ["csv_out", "csv_regra", "fmt"],
  "K5: tabela inteira (L127, L217) × só os pares (L219).", ["K5"], ["K05_truth_csv_juntas"])
I("C3-I20", "Conteúdo de csv", ["analyze", "(A and B) or C", "--format", "csv"], ["csv_out", "csv_regra"],
  "K5: suíte (L215) × tabela completa sem testes (L219).", ["K5"], ["K05_csv_juntas"])
I("C3-I21", "check sem colunas decision/expected_outcome", ["check", "(A and B) or C", "--tests", "{ENT}/check-sem-decision-expected.csv"],
  ["csv_in", "csv_obrig"], "K4: opcionais × obrigatórias × aceitas com valores inferidos.", ["K4"], ["K04_csv_colunas_juntas"])
I("C3-I22", "--z3 com 13 entradas", ["analyze", "{FILE:e13.txt}", "--z3", "--format", "json", "-o", "{OUT}/e13.json"], ["z3_12", "lim_tec"],
  "K10: passa ao modo direto (L113) × permanece na tabela (L115).", ["K10"], ["K10_z3_13_juntas"])
I("C3-I23", "--direct com 26 entradas", ["analyze", "{FILE:e26.txt}", "--direct", "--format", "json", "-o", "{OUT}/e26.json"],
  ["direct", "lim_tec", "lim20"], "K10: até 30 × só até 12 e exige a tabela (que acima de 20 não existe).", ["K10"], ["K10_direto_26_juntas"])
I("C3-I24", "--direct com expressão pequena", ["analyze", "(A and B) or C", "--direct"], ["direct", "lim_tec", "sat_inv"],
  "K6 (sat/unsat nas consultas de par ao Z3) e K10 (com ou sem tabela).", ["K6", "K10"])
I("C3-I25", "21 entradas sem Z3 (acima do limite)", ["analyze", "{FILE:e21.txt}", "--format", "json", "-o", "{OUT}/e21.json"], ["lim20"],
  "Omissão: o texto dá o limite, não a reação além dele (código também K3).", ["omissão", "K3"])
I("C3-I26", "TIS: 69 condições", ["analyze", "--json", "{EX}/tis-decisoes.json", "--format", "json"], ["regressao", "regra_comp"],
  "K1: tis#2–#4 repetem entradas; 69 ocorrências × 63 entradas distintas.", ["K1"], ["K01_contagem_condicoes_juntas"])
I("C3-I27", "TIS: mutantes e detecção", ["analyze", "--json", "{EX}/tis-decisoes.json", "--mutation", "--format", "json"],
  ["regressao", "par_lim", "par_gar"], "K14 (1 escapa × nenhum escapa), K1 e K7.", ["K14", "K1", "K7"], ["K14_parenteses_juntas"])
I("C3-I28", "VM: 26 testes", ["analyze", "--json", "{EX}/vm-decisoes.json", "--z3", "--format", "json"], ["regressao", "simpl", "guloso"],
  "K7/K8/K6 afetam o tamanho da suíte.", ["K6", "K7", "K8"], ["K15_regressao_testes_juntas"])
I("C3-I29", "--constraint com arquivo", ["analyze", "-f", "{EX}/requisitos.mcdc", "--constraint", "A"], ["constraint"],
  "Omissão: 'só com expressão direta' não diz a reação (erro, aviso ou ignorar).", ["omissão"])
I("C3-I30", ".mcdc com linha sem identificador", ["analyze", "-f", "{ENT}/sem-id.mcdc"], ["mcdc_fmt", "req_file_test"],
  "Omissão: o teste citado só nomeia o tópico.", ["omissão"])
I("C3-I31", "JSON com ids repetidos", ["analyze", "--json", "{ENT}/ids-repetidos.json"], ["json_test"],
  "Omissão: o teste citado só nomeia o tópico.", ["omissão"])
I("C3-I32", "Formato desconhecido", ["analyze", "(A and B) or C", "--format", "xml"], ["fmt", "cod", "cod_inv"],
  "Omissão da reação; código em K3.", ["omissão", "K3"])
I("C3-I33", "Arquivo inexistente", ["analyze", "-f", "{ENT}/nao-existe.mcdc"], ["mcdc_fmt", "cod", "cod_inv"],
  "Omissão da reação; código em K3.", ["omissão", "K3"])
I("C3-I34", "Detecção de mutantes de A and (B or C)", ["analyze", "A and (B or C)", "--mutation"], ["mut", "par_lim", "par_gar"],
  "K14 (ASF) e K7 (suíte depende do critério).", ["K14", "K7"], ["K14_parenteses_juntas"])
I("C3-I35", "check com --format csv", ["check", "(A and B) or C", "--tests", "{ENT}/check-completa.csv", "--format", "csv"], ["fmt"],
  "Omissão: check aceita text e json; reação a csv não descrita.", ["omissão"])
I("C3-I36", "JSON inválido", ["analyze", "--json", "{ENT}/invalido.json"], ["json_test", "cod", "cod_inv"],
  "Omissão: 'arquivos inválidos' só nomeia o tópico; código em K3.", ["omissão", "K3"])
I("C3-I37", "Comando desconhecido", ["frobnicate", "(A and B) or C"], ["uso"], "Omissão.", ["omissão"])
I("C3-I38", "check com mudança de condição sem mudança de resultado",
  ["check", "(A and B) or C", "--tests", "{ENT}/check-sem-mudanca-de-resultado.csv"], ["passo3", "simpl", "check"],
  "K7: A muda (T1/T2) mas o resultado não; demonstrada só no critério simplificado.", ["K7"], ["K07_criterio_par_juntas"])
I("C3-I39", "Classificação de condições com --z3 e fronteiras no TIS",
  ["analyze", "--json", "{EX}/tis-decisoes.json", "--z3", "--boundary", "--format", "json"], ["sat_inv", "diag", "diag_inv"],
  "K6/K9/K1 no TIS (diagnóstico, impossíveis e condições).", ["K6", "K9", "K1"])

json.dump({"condicao": "C3", "fonte": "experimentacao-pesquisa/experimentacao-3/documentation/tool-readme-C3.md",
           "sha256_fonte": "F18B0821D79C7315486C13D5260FA2F6D6E9418EF03B86CDE58E66B91B7B87A3",
           "unidade": "caso de teste com ID estável (C3-Txx determinado, C3-Ixx indeterminado)",
           "casos": C}, open(os.path.join(HERE, "oraculo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

md = ["# Inventário do oráculo C3", "",
      "Gerado por `casos.py` a partir de `tool-readme-C3.md` (SHA-256 F18B0821…7A3). Linhas [Lnn] referem-se à fonte.", "",
      f"Casos: {len(C)} — determinados: {sum(c['status']=='DETERMINADO' for c in C)}, indeterminados: {sum(c['status']=='INDETERMINADO' for c in C)}.", ""]
for c in C:
    md += [f"## {c['id']} — {c['titulo']} ({c['status']})", "",
           f"- Entrada: `mcdc {' '.join(c['args'])}`", f"- Pré-condição: {c['precondicao']}", "- Trechos literais:"]
    md += [f"  - {t}" for t in c["trechos"]]
    if c["status"] == "DETERMINADO":
        md += [f"- Regra: {c['regra']}", f"- Expectativa: {c['expectativa']}"]
    md += [f"- Justificativa: {c['justificativa']}", f"- Conflitos considerados: {', '.join(c['conflitos_avaliados']) or '—'}",
           f"- Evidências Z3: {', '.join(c['z3']) or '—'}", ""]
open(os.path.join(HERE, "inventario-oraculo.md"), "w", encoding="utf-8").write("\n".join(md))
print(len(C), sum(c['status'] == 'DETERMINADO' for c in C))
