"""Gera as entradas montadas e o oraculo.json da condição C1.

Expectativas derivadas exclusivamente de tool-readme-C1.md (SHA-256 91981FA0...D33B).
Linhas citadas (Lnnn) referem-se a esse arquivo. Gerado antes de qualquer leitura do código
ou execução do SUT. Uso: python -I gerar_oraculo.py
"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
IN = os.path.join(BASE, "entradas")
os.makedirs(IN, exist_ok=True)


def wtext(name, text):
    with open(os.path.join(IN, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def wjson(name, obj):
    with open(os.path.join(IN, name), "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


# ---------- entradas montadas ----------
wtext("AN16_comentarios.mcdc", "# comentário\nR-1: A and B\n# outro comentário\n")
wtext("AN17_erro_sintaxe.mcdc", "R-1: (A and B\n")
wtext("AN44_sem_identificador.mcdc", "A and B\n")
wtext("CK01_completo.csv", "test,input,value,expected_outcome\nT1,A,T,T\nT1,B,T,T\nT2,A,F,F\nT2,B,T,F\nT3,A,T,F\nT3,B,F,F\n")
wtext("CK02_incompleto.csv", "test,input,value,expected_outcome\nT1,A,T,T\nT1,B,T,T\nT2,A,F,F\nT2,B,T,F\n")
wtext("CK03_esperado_errado.csv", "test,input,value,expected_outcome\nT1,A,T,F\nT1,B,T,F\nT2,A,F,F\nT2,B,T,F\nT3,A,T,F\nT3,B,F,F\n")
wtext("CK04_sem_value.csv", "test,input,expected_outcome\nT1,A,T\nT1,B,T\n")
wtext("CK08_sem_esperado.csv", "test,input,value\nT1,A,T\nT1,B,T\nT2,A,F\nT2,B,T\nT3,A,T\nT3,B,F\n")

inputs = [{"name": "mode", "type": "enum", "values": ["a", "b", "c"]},
          {"name": "flag", "type": "bool"}, {"name": "sw", "type": "bool"}]
wjson("VF01_conflito.json", {"system": "c1_vf", "inputs": inputs, "decisions": [
    {"id": "vf#1", "requirement": "R-1", "guard": "flag = true", "actions": ["mode := a"]},
    {"id": "vf#2", "requirement": "R-2", "guard": "sw = true", "actions": ["mode := b"]}]})
wjson("VF02_mesmo_valor.json", {"system": "c1_vf", "inputs": inputs, "decisions": [
    {"id": "vf#1", "requirement": "R-1", "guard": "flag = true", "actions": ["mode := a"]},
    {"id": "vf#2", "requirement": "R-2", "guard": "sw = true", "actions": ["mode := a"]}]})
wjson("VF03_disjuntas.json", {"system": "c1_vf", "inputs": inputs, "decisions": [
    {"id": "vf#1", "requirement": "R-1", "guard": "flag = true", "actions": ["mode := a"]},
    {"id": "vf#2", "requirement": "R-2", "guard": "flag = false", "actions": ["mode := b"]}]})
wjson("VF07_ids_repetidos.json", {"system": "c1_vf", "inputs": inputs, "decisions": [
    {"id": "vf#1", "requirement": "R-1", "guard": "flag = true", "actions": ["mode := a"]},
    {"id": "vf#1", "requirement": "R-2", "guard": "sw = true", "actions": ["mode := b"]}]})


def conj(n):
    return " and ".join(f"X{i}" for i in range(1, n + 1))


PAR = "(A and not B and not C) or (not A and B and not C) or (not A and not B and C) or (A and B and C)"
SPEED = "speed > 100 or (speed > 50 and rain)"
L_EXIT = "L139: \"`0`: comando concluído sem apontar os problemas descritos para o código `2`; `1`: entrada inválida; `2`: resultado válido do processamento, mas com uma condição sem par no `analyze`, uma condição não demonstrada ou um resultado esperado divergente no `check`, ou um conflito ou uma lacuna no `verify`.\""
L_UC = "L491: \"todo par de causa única vale em mascaramento\""

cases = []


def case(id, grupo, cmds, expect, quote, regra, just, z3=None, status="DETERMINADO", env=None):
    cases.append({"id": id, "grupo": grupo, "status": status, "comandos": cmds, "ambiente": env or "padrao",
                  "expectativa": expect, "trecho": quote, "regra": regra, "justificativa": just,
                  "z3": z3 or []})


# ---------------- analyze: expressões ----------------
case("AN-01", "analyze", [["analyze", "(A and B) or C"]], {"exit": 0}, [L_EXIT, L_UC],
     "Toda condição com par => código 0.",
     "Cada condição tem par de causa única (Z3 sat); pela L491 esse par vale no mascaramento (padrão). Sem condição sem par => 0.",
     ["Q01_AN01_ABorC_par_*"])
case("AN-02", "analyze", [["analyze", "(A and B) or C", "--format", "csv"]],
     {"exit": 0, "testes_distintos": 4, "linhas_dados": "testes_distintos * 3"},
     ["L493: \"Exemplos conhecidos ((A ∧ B) ∨ C com 4 testes, A ∧ ¬B com 3)\"",
      "L205: \"A suíte: uma linha por teste e entrada\""],
     "Suíte de (A∧B)∨C tem 4 testes; CSV tem uma linha por teste e entrada (3 entradas).",
     "Número literal do texto. Z3: 3 linhas não bastam para pares de causa única (unsat), 4 bastam (sat) — evidência auxiliar.",
     ["Q02_AN02_ABorC_k3", "Q02_AN02_ABorC_k4"])
case("AN-03", "analyze", [["analyze", "(A and B) or C", "--unique-cause"]], {"exit": 0}, [L_EXIT, "L105: \"`--unique-cause` | Causa única em vez de mascaramento\""],
     "Causa única: cada condição tem par em que só ela muda => 0.",
     "Interpretação literal de 'causa única' (só a condição alvo muda); pares existem (Z3 sat).",
     ["Q01_AN01_ABorC_par_*"])
case("AN-04", "analyze", [["analyze", "A and not B", "--format", "csv"]], {"exit": 0, "testes_distintos": 3},
     ["L493: \"A ∧ ¬B com 3\""], "Suíte de A∧¬B tem 3 testes.",
     "Número literal. Z3 auxiliar: k=2 unsat, k=3 sat.", ["Q02_AN04_AandnotB_k2", "Q02_AN04_AandnotB_k3"])
case("AN-05", "analyze", [["analyze", "speed > 100 /\\ mode = idle"]], {"exit": 0},
     ["L93: \"`'speed > 100 /\\ mode = idle'`\"", "L131: \"e | `and`, `&&`, `/\\`\"", L_EXIT],
     "Expressão direta com comparações e /\\ aceita; duas condições com par => 0.",
     "Sem --z3 as comparações são condições independentes (tabela 2^2); pares existem (Z3 sat).",
     ["Q01_AN05_speed_mode_par_*"])
case("AN-06", "analyze", [["analyze", "A && B || !C", "--format", "truth-csv"],
                          ["analyze", "A /\\ B \\/ not C", "--format", "truth-csv"],
                          ["analyze", "A and B or not C", "--format", "truth-csv"]],
     {"exit": 0, "linhas_dados": 8, "resultado_por_linha": "(A and B) or not C"},
     ["L131-135: e `and`,`&&`,`/\\`; ou `or`,`||`,`\\/`; não `not`,`!`", "L515: \"Precedência (e antes de ou)\"",
      "L207: \"`truth-csv` | A tabela-verdade inteira\""],
     "As três grafias denotam (A∧B)∨¬C; tabela com 2^3 linhas e resultado de cada linha igual à fórmula.",
     "Formas aceitas e precedência documentadas.", [])
case("AN-07", "analyze", [["analyze", "A or B and C", "--format", "truth-csv"]],
     {"exit": 0, "linhas_dados": 8, "resultado_por_linha": "A or (B and C)"},
     ["L515: \"Precedência (e antes de ou)\""], "`and` liga mais forte que `or`.",
     "Z3 mostra que A∨(B∧C) e (A∨B)∧C diferem (sat), logo a tabela discrimina a precedência.",
     ["Q09_AN07_precedencia_discrimina"])
case("AN-08", "analyze", [["analyze", "x = 1 and y == 2 and z != 3 and w < 4 and v <= 5 and u > 6 and t >= 7"]],
     {"exit": 0}, ["L137: \"comparação | `=`, `==`, `!=`, `<`, `<=`, `>`, `>=`\"", L_EXIT],
     "Os sete comparadores são aceitos; conjunção de 7 condições independentes tem par para cada uma => 0.",
     "Em conjunção sem repetição cada condição tem par de causa única (mesmo padrão de Q01_AN04/AN05).", [])
case("AN-09", "analyze", [["analyze", "(A and B) or (not A and C)"]], {"exit": 0},
     ["L225: \"entrada repetida: cada aparição é uma condição com par próprio (A#1, A#2)\"", L_EXIT],
     "Cada aparição (A#1, B, A#2, C) tem par próprio => nenhuma condição sem par => 0.",
     "Frase literal do exemplo afirma par próprio para cada aparição.", [])
case("AN-10", "analyze", [["analyze", "(A and B) or (not A and C)", "--format", "truth-csv"]],
     {"exit": 0, "linhas_dados": 8, "resultado_por_linha": "(A and B) or (not A and C)"},
     ["L55: \"há 3 entradas distintas (`A`, `B` e `C`) e 4 ocorrências\"",
      "L279: \"para as entradas distintas da expressão, são consideradas as 2ⁿ combinações\""],
     "Tabela por entradas distintas: 2^3 = 8 linhas.", "Texto literal.", [])
case("AN-11", "analyze", [["analyze", "(A and B) or C", "--format", "truth-csv"]],
     {"exit": 0, "linhas_dados": 8, "primeira_linha_toda_verdadeira": True, "resultado_por_linha": "(A and B) or C"},
     ["L485: \"Uma linha por combinação; a linha 0 é tudo verdadeiro\"", "L207"],
     "8 linhas; a primeira (linha 0) tem todas as entradas verdadeiras; resultado correto por linha.", "Texto literal.", [])
case("AN-12", "analyze", [["analyze", PAR, "--format", "csv"]], {"testes_distintos": 8},
     ["L591: \"a função de paridade de 3 entradas exige 8 testes\""], "Paridade de 3 entradas => suíte com 8 testes.",
     "Z3 confirma que a expressão é a paridade (equivalência a XOR: unsat da negação).", ["Q02_AN12_paridade_equivalencia"])
case("AN-13", "analyze", [["analyze", "A or (B and C)", "--constraint", "not A or B"]], {"exit": 0},
     ["L231: \"restrição escrita à mão: A = speed > 100 implica B = speed > 50\"", L_EXIT],
     "Com a restrição, todas as condições ainda têm par => 0.", "Z3: pares de causa única viáveis sob a restrição (sat).",
     ["Q01_AN13_constraint_par_*"])
case("AN-14", "analyze", [["analyze", "A and B", "--constraint", "A"]], {"exit": 2},
     ["L287: \"se deixa de possuir pares por causa das combinações impossíveis, é classificada como bloqueada\"", L_EXIT],
     "Restrição 'A' torna A=F impossível; A fica sem par (bloqueada) => 2.",
     "Z3: A sem par sob a restrição (unsat) e com par sem ela (sat).",
     ["Q01_AN14_bloq_com_restricao_par_A", "Q01_AN14_bloq_sem_restricao_par_A"])
case("AN-15", "analyze", [["analyze", "-f", "{EX}/requisitos.mcdc"]], {"exit": 2},
     ["L241: \"vários requisitos de um arquivo; REQ-003 tem uma condição redundante\"", L_EXIT],
     "Condição redundante = sem par no analyze => 2.",
     "Texto literal; Z3 confirma que pedal_pressionado não muda o resultado de REQ-003 (unsat).", ["Q01_REQ003_par_P"])
case("AN-16", "analyze", [["analyze", "-f", "{IN}/AN16_comentarios.mcdc"]], {"exit": 0},
     ["L143: \"um requisito por linha, `ID: expressão`. Linhas com `#` são comentários.\""],
     "Comentários ignorados; R-1: A and B tem pares => 0.", "Texto literal.", [])
case("AN-17", "analyze", [["analyze", "-f", "{IN}/AN17_erro_sintaxe.mcdc"]], {"exit": 1},
     ["L517: \"erro de sintaxe com o requisito\"", L_EXIT], "Erro de sintaxe => entrada inválida => 1.", "Texto literal.", [])
case("AN-18", "analyze", [["analyze", "(A and B"]], {"exit": 1},
     ["L515: \"expressões inválidas recusadas\"", L_EXIT], "Parêntese não fechado => 1.", "Texto literal.", [])
case("AN-19", "analyze", [["analyze", "x > -3 and y"]], {"exit": 0},
     ["L523: \"sinal de menos só em números\"", L_EXIT], "Número negativo aceito; conjunção com pares => 0.", "Texto literal.", [])
case("AN-20", "analyze", [["analyze", "-x > 3"]], {"exit": 1},
     ["L523: \"sinal de menos só em números\"", L_EXIT], "Sinal de menos antes de identificador não é aceito => 1.",
     "Se o sinal de menos é aceito só em números, '-x' é entrada inválida.", [])
case("AN-21", "analyze", [["analyze", "A and B", "--format", "xml"]], {"exit": 1},
     ["L121: \"`--format <formato>` | `text` (padrão), `json`, `csv` (suíte) ou `truth-csv`\"", L_EXIT],
     "Formato fora da lista => entrada inválida => 1.", "Opção com valor não previsto é entrada inválida.", [])
case("AN-22", "analyze", [["analyze", "(A and B) or C", "-o", "{OUT}/AN-22.txt"], ["analyze", "(A and B) or C"]],
     {"exit": 0, "arquivo_igual_stdout_sem_o": True, "stdout_com_o_sem_relatorio": True},
     ["L123: \"`-o <arquivo>` | Grava o relatório no arquivo em vez de mostrar na tela\"",
      "L415: \"... e o determinismo\""],
     "Com -o o relatório vai para o arquivo (igual ao que iria à tela) e não aparece na tela.", "Texto literal.", [])
case("AN-23", "analyze", [["analyze", "(A and B) or C", "--format", "json"]], {"exit": 0, "json_valido": True},
     ["L203: \"`json` | Resultado completo de cada decisão, ligado ao requisito de origem\""], "Saída JSON válida.", "Texto literal.", [])
case("AN-24", "analyze", [["analyze", conj(20)]], {"exit": 0},
     ["L587: \"20 entradas com a tabela-verdade completa\"", L_EXIT], "20 entradas dentro do limite; conjunção com pares => 0.", "Texto literal.", [])
case("AN-25", "analyze", [["analyze", conj(21)]], {}, ["L587"], "Acima de 20 entradas sem Z3: comportamento não descrito.",
     "Omissão: o texto não diz se recusa, muda de modo ou qual código de saída.", status="INDETERMINADO")
case("AN-26", "analyze", [["analyze", "A and (B or C)", "--mutation"]], {"exit": 0},
     ["L239: \"validação por mutação\"", L_EXIT],
     "Mutação não está entre os gatilhos do código 2; todas as condições com par => 0.",
     "Pares de causa única existem em A∧(B∨C) (conjunção/disjunção sem repetição).", [])
case("AN-27", "analyze", [["analyze", "((E or D) and (not A or D)) or B", "--exact", "--format", "csv"]],
     {"testes_distintos": 5}, ["L255: \"suíte exata (aqui, 5 testes em vez dos 6 da escolha gulosa)\""],
     "--exact => 5 testes.", "Número literal. Z3 auxiliar (causa única por entrada): k=4 unsat, k=5 sat.",
     ["Q02_AN27_exata_entradas_k4", "Q02_AN27_exata_entradas_k5"], env="z3")
case("AN-28", "analyze", [["analyze", "((E or D) and (not A or D)) or B", "--format", "csv"]],
     {"testes_distintos": 6}, ["L255: \"5 testes em vez dos 6 da escolha gulosa\""], "Gulosa => 6 testes.", "Número literal.", [])
case("AN-29", "analyze", [["analyze", SPEED, "--z3", "--format", "truth-csv"]],
     {"linhas_dados": 8, "impossiveis": "exatamente as 2 linhas com speed>100=T e speed>50=F"},
     ["L235: \"o Z3 descobre as combinações impossíveis\"", "L207: \"com as combinações impossíveis marcadas\""],
     "2 linhas impossíveis, marcadas.", "Z3 independente: linhas A=T,B=F unsat; as demais sat.", ["Q03_AN29_linha_*"], env="z3")
case("AN-30", "analyze", [["analyze", SPEED, "--z3", "--format", "csv"]],
     {"exit": 0, "valores_realizam_guarda": True},
     ["L41: \"valores concretos para cada teste (`speed = 101`)\"",
      "L463: \"os valores concretos realizam a combinação declarada e o resultado esperado é o que a guarda dá\""],
     "Para cada teste, a guarda avaliada nos valores concretos = resultado esperado; todas as condições com par => 0.",
     "Pares viáveis: A(T,T,F)/(F,T,F), B(F,T,T)/(F,F,T), C(F,T,T)/(F,T,F) — linhas sat em Q03.", ["Q03_AN29_linha_*"], env="z3")
case("AN-31", "analyze", [["analyze", SPEED, "--z3", "--boundary", "--format", "json"]],
     {"valores_fronteira_speed_incluem": [100, 101, 50, 51]},
     ["L43: \"Variações no limite de cada comparação (`speed > 100` → 100 e 101)\""],
     "Fronteiras: 100/101 e 50/51.", "Z3: 101 é o menor inteiro >100 e 100 não satisfaz (idem 50/51).",
     ["Q03_AN31_fronteira_100", "Q03_AN31_fronteira_50"], env="z3")
case("AN-32", "analyze", [["analyze", "A and B", "--z3"]], {"aviso_z3": True},
     ["L73: \"As opções que exigem o Z3 avisam quando o executável não está instalado.\""],
     "Sem z3 no PATH, a saída (stdout+stderr) avisa sobre o Z3.", "Texto literal.", [], env="sem_z3")
case("AN-33", "analyze", [["analyze", conj(13), "--z3"]], {"exit": 0},
     ["L109: \"acima de 12 entradas, passa sozinho ao modo direto\"", L_EXIT], "13 entradas com --z3 => direto; pares => 0.", "Texto literal.", [], env="z3")
case("AN-34", "analyze", [["analyze", conj(30), "--direct"]], {"exit": 0},
     ["L113: \"`--direct` | Pares pedidos direto ao Z3, sem montar a tabela (até 30 entradas)\"", L_EXIT],
     "30 entradas dentro do limite do direto => 0.", "Texto literal.", [], env="z3")
case("AN-35", "analyze", [["analyze", conj(31), "--direct"]], {}, ["L113"], "Acima de 30 no direto: não descrito.",
     "Omissão do comportamento além do limite.", status="INDETERMINADO", env="z3")
case("AN-36", "analyze", [["analyze", SPEED, "--boundary"]], {}, ["L115: \"`--boundary` | Com `--z3`, acrescenta variantes de fronteira\""],
     "--boundary sem --z3: não descrito.", "Omissão.", status="INDETERMINADO")
case("AN-37", "analyze", [["analyze", "-f", "{IN}/AN16_comentarios.mcdc", "--constraint", "A"]], {},
     ["L107: \"(só com expressão direta)\""], "Restrição com arquivo: não diz se é erro ou ignorada.", "Ambiguidade.", status="INDETERMINADO")
case("AN-38", "analyze", [["analyze", "(A and B) or (not A and C)", "--unique-cause"]], {},
     ["L225", "L105"], "Causa única com entrada repetida: o texto não define se A#1/A#2 têm par.",
     "Omissão da definição de causa única para ocorrências acopladas.", status="INDETERMINADO")
case("AN-39", "cli", [["foo"]], {}, ["L79-83"], "Comando desconhecido: código não descrito.", "Omissão.", status="INDETERMINADO")
case("AN-40", "cli", [[]], {}, ["L79-83"], "Sem argumentos: não descrito.", "Omissão.", status="INDETERMINADO")
case("AN-41", "analyze", [["analyze", "-f", "{IN}/nao-existe.mcdc"]], {"exit": 1}, [L_EXIT],
     "Arquivo de fonte inexistente => entrada inválida => 1.",
     "O comando não pode ser concluído (0/2 exigem processamento); entre os códigos documentados só 1 se aplica.", [])
case("AN-42", "analyze", [["analyze", "speed > 100 and speed > 50", "--z3"]], {"exit": 2},
     ["L281: \"as que retornam `unsat` são consideradas impossíveis\"", "L287: \"... bloqueada\"", L_EXIT],
     "speed>100=T e speed>50=F é impossível; a condição speed>50 perde o par => bloqueada => 2.",
     "Z3: par de B unsat com A=>B; sat sem a restrição.", ["Q03_AN42_bloq_z3_par_B", "Q03_AN43_sem_z3_par_B"], env="z3")
case("AN-43", "analyze", [["analyze", "speed > 100 and speed > 50"]], {"exit": 0},
     ["L73: \"Sem o Z3, continuam disponíveis os recursos que não dependem dele.\"", L_EXIT],
     "Sem --z3 não há combinações impossíveis; ambas as condições com par => 0.", "Z3: pares sat na tabela completa.",
     ["Q03_AN43_sem_z3_par_*"])
case("AN-44", "analyze", [["analyze", "-f", "{IN}/AN44_sem_identificador.mcdc"]], {},
     ["L517: \"linha sem identificador\""], "Linha sem 'ID:': o texto não diz se é erro ou recebe id.", "Ambiguidade.", status="INDETERMINADO")

# ---------------- sistemas de exemplo ----------------
SYS = {"VM": ("vm", 5, 21, 152, 4, 26, 152, 0, 152, 0), "TIS": ("tis", 17, 69, 268, 4, 80, 450, 21, 428, 3),
       "NPP": ("npp", 11, 29, 76, 1, 40, 146, 0, 146, 1)}
L_REG = "L467-477: tabela 'Números travados pela regressão'"
for S, (f, req, cond, comb, imp, tests, mut, eq, caught, confl) in SYS.items():
    src = ["--json", "{EX}/" + f + "-decisoes.json"]
    exp1 = {"decisoes": req, "condicoes": cond, "combinacoes": comb, "impossiveis": imp, "testes": tests}
    if S in ("VM", "NPP"):
        exp1["testes_por_decisao_igual_condicoes_mais_1"] = True
    exp1["requisitos_rastreados"] = True
    case(f"SY-{S}-01", "sistema", [["analyze", *src, "--z3", "--format", "json"], ["analyze", *src, "--z3", "--format", "truth-csv"]], exp1,
         [L_REG, "L461: \"Para cada requisito completo, a quantidade registrada de testes corresponde ao número de condições mais 1.\"",
          "L203: \"ligado ao requisito de origem\""],
         "Números da regressão (com Z3, para as impossíveis).",
         "Números literais. " + ("Todos completos => N+1 por decisão. " if S != "TIS" else "") +
         ("Z3 independente reproduz 152 combinações e 4 impossíveis da VM a partir das guardas." if S == "VM" else ""),
         ["Q07_regressao_consistencia"] + (["Q04_VM_viabilidade_*"] if S == "VM" else []), env="z3")
    case(f"SY-{S}-02", "sistema", [["analyze", *src, "--z3", "--mutation", "--format", "json"]],
         {"mutantes": mut, "equivalentes": eq, "pegos": caught}, [L_REG], "Contagem de mutantes.", "Números literais.",
         ["Q07_regressao_consistencia"], env="z3")
    case(f"SY-{S}-03", "sistema", [["verify", *src]], {"conflitos": confl, "exit": 0 if confl == 0 else 2},
         [L_REG, L_EXIT, "L537: \"lacunas só com contexto\""], "Conflitos do verify; sem contexto não há lacuna.",
         "Números literais" + ("; Z3 independente: nenhum par de guardas com escritas diferentes é simultâneo (10 unsat)." if S == "VM" else "."),
         ["Q05_VM_conflito_*"] if S == "VM" else [], env="z3")
    case(f"SY-{S}-04", "sistema", [["analyze", *src, "--z3", "--exact", "--format", "json"]], {"testes": tests},
         ["L461: \"A busca exata e a variante de causa única produzem o mesmo número de testes nesses exemplos.\""],
         "Busca exata: mesmo número de testes.", "Texto literal.", [], env="z3")
    case(f"SY-{S}-05", "sistema", [["analyze", *src, "--z3", "--unique-cause", "--format", "json"]], {"testes": tests},
         ["L461: \"A busca exata e a variante de causa única produzem o mesmo número de testes nesses exemplos.\""],
         "Causa única: mesmo número de testes.", "Texto literal.", [], env="z3")
    case(f"SY-{S}-06", "sistema", [["analyze", *src, "--direct", "--format", "json"], ["analyze", *src, "--z3", "--format", "json"]],
         {"cobertura_e_diagnostico_iguais": True},
         ["L419: \"o modo direto dá a mesma cobertura e o mesmo diagnóstico que a tabela-verdade completa\""],
         "Direto = tabela completa em cobertura e diagnóstico por condição.", "Texto literal.", [], env="z3")
case("SY-VM-07", "sistema", [["verify", "--json", "{EX}/vm-decisoes.json", "--context", "the_system_mode = preparing_weak"]],
     {"exit": 2}, ["L119: \"`--context \\\"<expr>\\\"` | No `verify`: confere se, nessa situação, sempre alguma guarda vale\"",
                   "L53: \"lacunas (nenhum requisito vale)\"", L_EXIT],
     "Há situação com modo preparing_weak em que nenhuma guarda vale (ex.: timer < 10) => lacuna => 2.",
     "Z3 independente sobre as guardas da entrada: sat.", ["Q05_VM_lacuna_contexto_preparing_weak"], env="z3")
case("SY-TIS-07", "sistema", [["analyze", "--json", "{EX}/tis-decisoes.json", "--z3", "--format", "json"]], {},
     ["L471-475: coluna 'Completos' (TIS 14 de 17)", "L461"],
     "Quais requisitos são 'completos' e quantos testes os 3 restantes têm.",
     "O texto não define 'requisito completo'; N+1 só vale para completos (Q07_TIS_nao_completos: 69+17≠80).",
     ["Q07_TIS_nao_completos"], status="INDETERMINADO", env="z3")

# ---------------- check ----------------
L_CK = "L183: \"cada linha associa um teste a uma entrada e ao valor atribuído... (`T`/`F`)... As colunas `decision` e `expected_outcome` são opcionais.\""
case("CK-01", "check", [["check", "A and B", "--tests", "{IN}/CK01_completo.csv"]], {"exit": 0}, [L_CK, L_EXIT, L_UC],
     "T1/T2 demonstram A e T1/T3 demonstram B (causa única); esperados corretos => 0.", "Z3: nenhum esperado diverge (unsat).", ["Q08_CK01_AandB"])
case("CK-02", "check", [["check", "A and B", "--tests", "{IN}/CK02_incompleto.csv"]], {"exit": 2}, [L_EXIT, "L283: \"essa condição muda\""],
     "B não muda em nenhum teste => não demonstrada => 2.", "Um par exige que a condição mude.", [])
case("CK-03", "check", [["check", "A and B", "--tests", "{IN}/CK03_esperado_errado.csv"]], {"exit": 2}, [L_EXIT, "L51: \"testes com resultado esperado errado\""],
     "T1 (T,T) esperado F, guarda dá T => divergente => 2.", "Avaliação direta da guarda.", ["Q08_CK01_AandB"])
case("CK-04", "check", [["check", "A and B", "--tests", "{IN}/CK04_sem_value.csv"]], {"exit": 1}, [L_CK, "L521: \"colunas faltando\"", L_EXIT],
     "Coluna obrigatória `value` ausente => entrada inválida => 1.", "Só `decision` e `expected_outcome` são opcionais.", [])
case("CK-05", "check", [["check", "--json", "{EX}/decisoes.json", "--tests", "{EX}/testes.csv"]], {"exit": 2},
     ["L269: \"avaliar testes que já existem\"", L_EXIT],
     "T4 (#3): mode=idle, button=true, coin=false => guarda F, esperado T => divergente => 2.",
     "Z3: guarda de #3 é F em T4 (unsat de guarda=T) e T em T3.", ["Q08_CK05_decisoes_T4", "Q08_CK05_decisoes_T3"])
case("CK-06", "check", [["check", "A and B", "--tests", "{IN}/CK01_completo.csv", "--format", "json"]], {"json_valido": True},
     ["L121: \"`check` e `verify` aceitam `text` e `json`\""], "JSON válido.", "Texto literal.", [])
case("CK-07", "check", [["check", "A and B", "--tests", "{IN}/CK01_completo.csv", "--format", "csv"]], {"exit": 1},
     ["L121: \"`check` e `verify` aceitam `text` e `json`\"", L_EXIT], "csv não aceito no check => 1.", "Valor de opção não aceito = entrada inválida.", [])
case("CK-08", "check", [["check", "A and B", "--tests", "{IN}/CK08_sem_esperado.csv"]], {"exit": 0}, [L_CK, L_EXIT],
     "Sem expected_outcome (opcional) e cobertura completa => 0.", "Coluna opcional; sem divergência possível.", [])

# ---------------- verify ----------------
case("VF-01", "verify", [["verify", "--json", "{IN}/VF01_conflito.json"]], {"exit": 2},
     ["L53: \"Conflitos (dois requisitos valem juntos e escrevem valores diferentes)\"", L_EXIT],
     "flag=sw=true torna ambas verdadeiras; escrevem a e b em mode => conflito => 2.", "Z3 sat.", ["Q06_VF01_sobreposicao"], env="z3")
case("VF-02", "verify", [["verify", "--json", "{IN}/VF02_mesmo_valor.json"]], {"exit": 0},
     ["L537: \"mesmo valor sem conflito\"", L_EXIT], "Mesmo valor => sem conflito; sem contexto não há lacuna => 0.", "Texto literal.", [], env="z3")
case("VF-03", "verify", [["verify", "--json", "{IN}/VF03_disjuntas.json"]], {"exit": 0},
     ["L537: \"guardas que não se sobrepõem\"", L_EXIT], "Guardas disjuntas => sem conflito => 0.", "Z3 unsat.", ["Q06_VF03_disjuntas"], env="z3")
case("VF-04", "verify", [["verify", "--json", "{IN}/VF01_conflito.json", "--context", "flag = false"]], {"exit": 2},
     ["L119", "L53: \"lacunas (nenhum requisito vale)\"", L_EXIT], "flag=false e sw=false: nenhuma guarda vale => lacuna => 2.",
     "Z3 sat.", ["Q06_VF04_lacuna"], env="z3")
case("VF-05", "verify", [["verify", "--json", "{IN}/VF03_disjuntas.json", "--context", "mode = a"]], {"exit": 0},
     ["L119", L_EXIT], "flag=true ou flag=false sempre vale; guardas disjuntas => 0.", "Z3 unsat (sem lacuna) e Q06_VF03 unsat.",
     ["Q06_VF05_sem_lacuna", "Q06_VF03_disjuntas"], env="z3")
case("VF-06", "verify", [["verify", "--json", "{IN}/VF01_conflito.json", "--format", "json"]], {"json_valido": True},
     ["L121: \"`check` e `verify` aceitam `text` e `json`\""], "JSON válido.", "Texto literal.", [], env="z3")
case("VF-07", "analyze", [["analyze", "--json", "{IN}/VF07_ids_repetidos.json"]], {"exit": 1},
     ["L519: \"arquivos inválidos, ids repetidos\"", L_EXIT], "Ids repetidos => entrada inválida => 1.",
     "O teste de leitura garante a recusa de ids repetidos.", [])

oracle = {"condicao": "C1", "fonte": "experimentacao-pesquisa/experimentacao-1/documentation/tool-readme-C1.md",
          "fonte_sha256": "91981FA0181E5CC1BC5A67DAAFC965BB82D6F8EB0A6D47EB58CE291A3EF5D33B",
          "unidade_de_contagem": "um caso = um ID; todas as asserções do caso devem valer para PASSOU",
          "placeholders": {"{EX}": "exemplos/ do repositório", "{IN}": "experimento/entradas", "{OUT}": "pasta da rodada"},
          "ambientes": {"padrao": "PATH com z3", "z3": "PATH com z3", "sem_z3": "PATH sem z3"},
          "casos": cases}
with open(os.path.join(BASE, "oraculo.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(oracle, f, ensure_ascii=False, indent=2)
    f.write("\n")
det = sum(c["status"] == "DETERMINADO" for c in cases)
print(len(cases), "casos;", det, "determinados;", len(cases) - det, "indeterminados")
