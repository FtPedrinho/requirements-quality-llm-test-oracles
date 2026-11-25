# -*- coding: utf-8 -*-
"""Gera experimento/oraculo.json (oraculo C4) e experimento/oraculo-casos.csv.

Os casos foram derivados somente do texto de tool-readme-C4.md. Trechos literais
preservam a degradacao do texto original (letras e palavras ausentes).
"""
import csv
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
FONTE = "documentacao/tool-readme-C4.md"
SHA = "D6BC0A588CD9A7DF7F1F566573944FA5CB1707BBA676B4E9854CAD2CC5440FC2"

# ----- trechos literais (numero da linha no arquivo da fonte, texto)
T = {
    "tab_reg_cab": (285, "| Sistema | Requisits | Comletos | Cdições | Combinações | Imposíveis | Tesuutes | Mutates | Equivalentes | Pegos | Conflitrros |"),
    "vm": (289, "| VM · máuina café | 5 | 5 | 21 | 152 | 4 | 26 | 152 | 0 | 152 | 0 |"),
    "tis": (291, "| TIS · pisca-pisca | 17 | 14 | 69 | 268 | 4 | 80 | 450 | 21 | 428 | 3 |"),
    "npp": (293, "| NPP · injeção segurança | 11 | 11 | 29 | 76 | 1 | 40 | 146 | 0 | 146 | 1 |"),
    "reg_test": (279, "| `RequirementsRegressionTest`| 3 | Verifica  resutados três sistemas exemplo premanecem iguis valores registrados requi, cond, combinarções, cmbinaçes impossíveis, tes, conições par, mutantes (total, equivalentes detec) conflitos. ..."),
    "ex_sist": (45, "# requisitos  sistemas  exemplo  NAT2TEST: máquina  café (VM), pisca-pisca (TIS)  injeção  segurança (NPP)"),
    "ex_vm": (47, "./mcdc analoyze --json exemplos/vm-decisoes.json --z3"),
    "ex_tis": (49, "./mcdc analyze --json exemplos/tis-decisoes.json --z3 --format json - relatorio.json"),
    "ex_verify": (63, "./mcdc verify --json exemplos/npp-decisoes.json"),
    "ex_mut": (97, "  → 6. mutação (opcional): são avaliados seis tips  def  Kapoor  Bowen (ORF, ENF, VNF, MVF, VRF, ASF); versões equivalentes  requisito original não entram  contagem"),
    "ex_dfrs": (23, "./mcdc analyze 'speed > 100 /\\ mode = idle'"),
    "ex_dfrs_c": (21, "# comparações   operadores  DFRS"),
    "tab": (79, "  → 1. tabela-verdade:   entradas distintas  expreão, são consideradas  2ⁿ combinações  calculado  resulstado  gua  cada "),
    "rep_c": (25, "# entrada repetida: cada aparição é  condiç  par próprio (#1, #2)"),
    "rep_t": (307, "| `ConditionTest`| 2 | Cada aparição é conoodição; \"decidir\" troca só  aparição |"),
    "lim": (101, "... Os limites documentados são: 20 entraas tabela-vrdade completa, 12 entads  processamento  Z3 linhuua linha 30 entradas modo dirto."),
    "lim2": (405, "- **Tamanho:** 20 entadas   tbaela-verdade complta (cerca 1 milhão combinações), 12 Z3 linha  linha  30 modo direto; 1000 pars guardados condiçoã."),
    "perf20": (245, "| `PerformanceTest`| 4 | Motor Z3: 20 entradas (cerca  1 milho combinações) duas variantes, entradas repetidas, mtuação decsão 16 entradas  avaliaução tetses existentes, cada caso abixo 5 s |"),
    "direto": (59, "./mcdc analyze --json exemplos/vm-decisoes.json --direct"),
    "direto_c": (57, "# modo diretoo: praes ped  Z3  motar  tabela"),
    "direto_t": (237, "... Z3RandomizedTest ... 120 expressões,  modo direto dá mesma cobertura  mesmo diagnóstceo tabela-verdade completa."),
    "direto_t2": (353, "| `Z3DirectAnalyzerTest`| 5 |  modo direto concorda  tabela; decisões acima 12  20 entradas; conidções bloqueadas |"),
    "sys_perf": (247, "| `SystemsPerformanceTest`| 4 |  Z3,  caminho  linha  coamando: sistema exemplo [trecho omitido] mtação, bsuca exata verificação  requisit) abaio 3 s,  modo direto  26 entradas abaixo 10 s |"),
    "paridade": (411, "- **Fórmulas muitas ocorrências repetidas entradas:**  critério MC/CD pode exigir todas  combinações possíveis.  exemplo, funão  parida 3 etradas exige 8 teses."),
    "vals": (281, "| `ReportsContentTest`| 6 |  JSON,  texto CSV dizem  foi calculado, três comandos.  to [trecho omitido]  sistemas exemplo, inclusive   fronteira, valores concretos realizam  combnação declarada   resu esp é  guara dá. |"),
    "ex_speed": (35, "./mcdc analyze \"speed > 100 or (speed > 50 and rain)\" --z3 --boundary"),
    "ex_speed_c": (33, "#  Z3 descobre  combinações impossíveis, dá valores concros  tetses  frotneira"),
    "csv_t": (371, "| `CsvReportTest`| 2 |  linha  teste  enrada; aspas célas vírgula |"),
    "fmt": (117, "| `mcdc-cli`| Comanos `analyze`, `check` `verify` relat  texto, JSON CSV |  três acima |"),
    "ex_json_t": (369, "| `JsonReportTest`| 3 | Rastreabilidade resu cada decisão; descrção enatdas; cond par |"),
    "invalida": (333, "| `ExpressionParserTest`| 9 | Prcedência  ), parênteses, comparações, oeradres  DFRS; expressões invlidas recusadas |"),
    "modulos": (105, "Projeto Mavne  quatro módulos:"),
    "mod_req": (113, "| `mcdc-requirements`| Leitor exressões, arquivos `.mcdc`, JSON NAT2TEST CSV  tetes | `mcdc-core`, Jackson |"),
    "mod_z3": (115, "| `mcdc-z3`| Covnersa   Z3  SMT-LIB: viabilidade, valores concreuutos fronteira, suíte exata, modo direto  verificação  requisitos | `mcdc-core`|"),
    "mod_cli": (117, "| `mcdc-cli`| Comanos `analyze`, `check` `verify` relat  texto, JSON CSV |  três acima |"),
    "mod_core": (111, "| `mcdc-core`| Modeo  expiiressão motor: tabela-verdade, cond apição, paers, escolha suíte, diagnóstico, aliação  tsetes exitetes  mutação | nada bibliotecas externas) |"),
    "q_lin": (163, "| Cobertura  linhas, módulo | todo `mvn verify`| 90% | `qualidade.linhas.minima``pom.xml`|"),
    "q_des": (165, "| Cobertura  desvos,  módulo | todo `mvn verify`| 85% | `qualidade.desvios.minima``pom.xml`|"),
    "q_mut": (167, "| Nota  mutação,  módulo | `mvn verify -Pqualidade`| 90% motor  lietura, 85% verificador, 75% linha comauundo | `qualidade.mutacao.minima` `pom.xml`cada módulo |"),
    "q_mut_tab": (139, "| `mcdc-z3`(vrificador) | 34 | 93,1% | 87,0% | 91,2% (269  295) | 85% |"),
    "rel": (191, "| Coberrtura  quatro módulos smados (JaCoCo) | [abrir](htteps://...) | [relatorios/jacoco/](relatorios/jacoco/) |"),
    "rel2": (193, "| Coberrtura planiha | [bai](https://rvdomingos.github.io/Tool_MCDC_Java/relatorios/jacoco/jacoco.csv) | [jacco.csv](relatorios/jacoco/jacoco.csv) |"),
    "rel3": (195, "| Mutação  motor (PIT) | [abrir](...) | [relatorios/pit/mcdc-core/](relatorios/pit/mcdc-core/) |"),
    "saidas": (9, "Saídas gradarrs   sistemas exemplo estão [exemplos/saidas/](exemplos/saidas/)."),
}


def tr(*chaves):
    return [{"linha": T[k][0], "texto": T[k][1]} for k in chaves]


casos = []


def D(id_, titulo, entrada, pre, trechos, regra, expect, just, obs):
    casos.append({
        "id": id_, "classificacao": "DETERMINADO", "titulo": titulo, "entrada": entrada,
        "precondicao": pre, "trecho_literal": tr(*trechos), "regra": regra,
        "expectativa": expect, "justificativa": just, "observavel": obs,
        "z3": "z01-aritmetica-documental.smt2" if id_ <= "D21" and id_ >= "D01" else "z12-combinacoes-casos-determinados.smt2"
        if id_ in ("D22", "D23", "D24", "D25", "D26", "D29") else None,
    })


def I(id_, titulo, entrada, trechos, motivo_tipo, motivo, z3=None):
    casos.append({
        "id": id_, "classificacao": "INDETERMINADO", "titulo": titulo, "entrada": entrada,
        "trecho_literal": tr(*trechos) if trechos and isinstance(trechos[0], str) and trechos[0] in T else
        [{"linha": l, "texto": t} for l, t in trechos],
        "tipo_indeterminacao": motivo_tipo, "expectativa": None, "motivo": motivo, "z3": z3,
    })


# ======================================================== DETERMINADOS
SIS = {
    "vm": ("VM (maquina de cafe)", "exemplos/vm-decisoes.json", "vm",
           dict(req=5, cond=21, comb=152, imp=4, tst=26, mut=152, eq=0, conf=0), "D01"),
    "tis": ("TIS (pisca-pisca)", "exemplos/tis-decisoes.json", "tis",
            dict(req=17, cond=69, comb=268, imp=4, tst=80, mut=450, eq=21, conf=3), "D08"),
    "npp": ("NPP (injecao de seguranca)", "exemplos/npp-decisoes.json", "npp",
            dict(req=11, cond=29, comb=76, imp=1, tst=40, mut=146, eq=0, conf=1), "D15"),
}
for chave, (nome, arq, linha, v, primeiro) in SIS.items():
    n0 = int(primeiro[1:])
    base_cmd = f"analyze --json {arq} --z3"
    pre = f"Arquivo {arq} existente; Z3 instalado e no PATH; variante padrao (mascaramento)."
    comuns = ["tab_reg_cab", linha, "reg_test", "ex_sist"]
    D(f"D{n0:02d}", f"{nome}: numero de requisitos", base_cmd, pre, comuns, "Numeros travados de regressao: coluna Requisitos.",
      f"A analise de {arq} relata {v['req']} requisitos.", "Linha da tabela de regressao.", "contagem de requisitos no relatorio")
    D(f"D{n0+1:02d}", f"{nome}: numero de condicoes", base_cmd, pre, comuns, "Coluna Condicoes.",
      f"O relatorio soma {v['cond']} condicoes (cada aparicao conta como uma condicao).", "Linha da tabela de regressao.", "soma de condicoes")
    D(f"D{n0+2:02d}", f"{nome}: numero de combinacoes", base_cmd, pre, comuns, "Coluna Combinacoes.",
      f"O relatorio soma {v['comb']} combinacoes (linhas de tabela-verdade).", "Linha da tabela de regressao.", "soma de combinacoes")
    D(f"D{n0+3:02d}", f"{nome}: numero de combinacoes impossiveis", base_cmd, pre, comuns, "Coluna Imposiveis.",
      f"O relatorio soma {v['imp']} combinacoes impossiveis.",
      "Valor numerico da tabela; independe de qual rotulo (sat/unsat) o texto adota, pois so a contagem e verificada (ver I03).",
      "soma de combinacoes impossiveis")
    D(f"D{n0+4:02d}", f"{nome}: numero de testes da suite", base_cmd, pre, comuns, "Coluna Testes.",
      f"A suite gerada soma {v['tst']} testes.", "Linha da tabela de regressao.", "soma de testes das suites")
    D(f"D{n0+5:02d}", f"{nome}: mutantes totais e equivalentes", base_cmd + " --mutation", pre + " Opcao --mutation.",
      comuns + ["ex_mut"], "Colunas Mutantes e Equivalentes (a coluna Pegos nao e usada; ver I21 para TIS).",
      f"Mutantes totais = {v['mut']}; equivalentes = {v['eq']}.",
      "Linha da tabela de regressao; a analise de mutacao e a opcional descrita no passo 6.", "totais de mutantes e equivalentes")
    D(f"D{n0+6:02d}", f"{nome}: numero de conflitos de requisitos", f"verify --json {arq}",
      f"Arquivo {arq} existente; comando verify sem --context.", comuns + ["ex_verify"], "Coluna Conflitos.",
      f"O comando verify relata {v['conf']} conflito(s) entre requisitos.", "Linha da tabela de regressao.", "contagem de conflitos")

# D22 .. D34
D("D22", "Comparacoes com operador DFRS: duas condicoes e quatro combinacoes",
  "analyze 'speed > 100 /\\ mode = idle'", "Sem --z3.", ["ex_dfrs_c", "ex_dfrs", "tab"],
  "Duas condicoes distintas; 2^n combinacoes sobre as n=2 entradas.",
  "O relatorio apresenta 2 condicoes e 4 combinacoes (nao ha erro).",
  "n=2 seja contando variaveis (speed, mode) ou predicados; ambos dao 4.", "condicoes/combinacoes no relatorio JSON")
D("D23", "Tres entradas distintas: 3 condicoes e 8 combinacoes", "analyze \"B or (C and D)\"", "Sem --z3.",
  ["tab", "rep_c"], "Cada aparicao e uma condicao; 2^n combinacoes das entradas distintas.",
  "O relatorio apresenta 3 condicoes e 8 combinacoes.", "n=3 -> 8.", "condicoes/combinacoes")
D("D24", "Entrada repetida: cada aparicao e uma condicao propria (#1, #2)", "analyze \"B or (not B and C)\"", "Sem --z3.",
  ["rep_c", "rep_t"], "Cada aparicao de uma entrada repetida e uma condicao propria, identificada por #1, #2.",
  "O relatorio apresenta 3 condicoes; as duas aparicoes de B aparecem distinguidas por #1 e #2.",
  "B aparece 2 vezes e C 1 vez.", "lista de condicoes")
D("D25", "Entrada repetida: combinacoes sobre entradas distintas", "analyze \"B or (not B and C)\"", "Sem --z3.",
  ["tab", "rep_c"], "2^n combinacoes calculadas das entradas distintas (n=2: B e C).",
  "O relatorio apresenta 4 combinacoes (nao 8).", "Entradas distintas = 2.", "numero de combinacoes")
D("D26", "Limite de 20 entradas na tabela-verdade completa e aceito", "analyze com 20 entradas distintas combinadas por and (nomes definidos pelo gerador)",
  "Sem --z3; variante padrao.", ["lim", "lim2", "perf20"],
  "Limite documentado: 20 entradas na tabela-verdade completa (cerca de 1 milhao de combinacoes).",
  "A analise e realizada (gera suite) e relata 1048576 combinacoes (2^20).", "20 e o limite documentado; 2^20 pela regra 2^n.", "relatorio sem erro e numero de combinacoes")
D("D27", "Limite de 12 entradas no processamento Z3 linha a linha e aceito", "analyze com 12 entradas booleanas distintas por and --z3",
  "Z3 no PATH; sem --direct.", ["lim", "lim2"], "Limite: 12 entradas no processamento Z3 linha a linha.",
  "A analise com Z3 e realizada e relata 4096 combinacoes (2^12).", "12 e o limite documentado.", "relatorio sem erro")
D("D28", "Modo direto aceita 26 entradas", "analyze com 26 entradas booleanas distintas por and --direct",
  "Z3 no PATH.", ["lim", "lim2", "sys_perf"], "Limite: 30 entradas no modo direto; o texto cita modo direto com 26 entradas.",
  "A analise em modo direto e realizada (gera suite) sem erro de limite.", "26 < 30; tempo nao e avaliado (ver I11).", "relatorio sem erro")
D("D29", "Funcao de paridade de 3 entradas exige 8 testes", "analyze com a paridade impar de B, C, D escrita com and/or/not (ocorrencias repetidas)",
  "Variante padrao, sem --z3.", ["paridade"], "Formulas com muitas ocorrencias repetidas podem exigir todas as combinacoes; exemplo: paridade de 3 entradas exige 8 testes.",
  "A suite gerada tem 8 testes.", "Exemplo do texto ('exige 8 testes').", "numero de testes da suite")
D("D30", "Valores concretos realizam a combinacao declarada e o resultado esperado", "analyze \"speed > 100 or (speed > 50 and rain)\" --z3 --format json",
  "Z3 no PATH.", ["vals", "ex_speed", "ex_speed_c"],
  "ReportsContentTest: os valores concretos realizam a combinacao declarada e o resultado esperado e o da decisao.",
  "Para cada teste do relatorio, avaliar as comparacoes com os valores concretos reproduz a combinacao declarada e o resultado esperado da decisao.",
  "Propriedade verificavel por avaliador independente; trecho parcialmente corrompido, mas a propriedade e legivel.", "valores concretos por teste")
D("D31", "CSV: celulas com virgula entre aspas", "analyze --json exemplos/vm-decisoes.json --z3 --format csv", "Z3 no PATH.", ["csv_t", "ex_vm"],
  "CsvReportTest: aspas em celulas com virgula.", "Ao ler a saida como CSV (RFC 4180), todas as linhas tem o mesmo numero de campos.",
  "Celulas com virgula nao quotadas deslocariam colunas.", "analise da saida CSV")
D("D32", "Formato json produz JSON valido", "analyze --json exemplos/tis-decisoes.json --z3 --format json", "Z3 no PATH.", ["ex_tis", "fmt", "ex_json_t"],
  "Formato de saida JSON.", "A saida padrao e um documento JSON valido.", "Formato JSON citado no exemplo e na tabela de comandos.", "parse JSON")
D("D33", "Expressao invalida e recusada", "analyze \"(B and\"", "Parenteses nao balanceados.", ["invalida"],
  "ExpressionParserTest: expressoes invalidas recusadas.", "A ferramenta nao produz analise (nenhuma condicao, combinacao ou teste na saida padrao).",
  "Parenteses sao documentados; expressao com parentese aberto sem fechar e invalida em qualquer gramatica; formato do erro e codigo de saida nao sao exigidos (ver I12).", "ausencia de relatorio")
D("D34", "Modo direto concorda com a tabela completa no diagnostico", "analyze --json exemplos/vm-decisoes.json --z3 e analyze --json exemplos/vm-decisoes.json --direct",
  "Z3 no PATH.", ["direto_c", "direto", "direto_t", "direto_t2"], "O modo direto da o mesmo diagnostico que a tabela-verdade completa.",
  "O diagnostico por condicao (conjunto de condicoes com classificacao) e identico nas duas execucoes.",
  "Restrito ao diagnostico (sem comparar rotulos redundante/bloqueada).", "comparacao de diagnostico")
D("D35", "Projeto Maven com os quatro modulos", "Estrutura do repositorio", "—", ["modulos", "mod_core", "mod_req", "mod_z3", "mod_cli"],
  "Quatro modulos: mcdc-core, mcdc-requirements, mcdc-z3, mcdc-cli.", "Existem os diretorios dos quatro modulos, cada um com pom.xml, e um pom.xml na raiz.", "Tabela de modulos.", "arquivos")
D("D36", "mcdc-requirements depende de mcdc-core e Jackson", "Leitura do pom.xml do modulo", "—", ["mod_req"], "Coluna 'Depende de'.",
  "O pom.xml de mcdc-requirements declara dependencia de mcdc-core e de Jackson.", "Celula literal.", "pom.xml")
D("D37", "mcdc-z3 depende de mcdc-core", "Leitura do pom.xml do modulo", "—", ["mod_z3"], "Coluna 'Depende de'.",
  "O pom.xml de mcdc-z3 declara dependencia de mcdc-core e de nenhum outro modulo do projeto.", "Celula literal.", "pom.xml")
D("D38", "mcdc-cli depende dos tres modulos", "Leitura do pom.xml do modulo", "—", ["mod_cli"], "Coluna 'Depende de': os tres acima.",
  "O pom.xml de mcdc-cli declara dependencia de mcdc-core, mcdc-requirements e mcdc-z3.", "Celula: 'tres acima' (os tres modulos da tabela acima).", "pom.xml")
D("D39", "Notas minimas de cobertura configuradas no pom.xml", "Leitura do pom.xml", "—", ["q_lin", "q_des"],
  "Propriedades qualidade.linhas.minima (90%) e qualidade.desvios.minima (85%) no pom.xml.",
  "O pom.xml declara qualidade.linhas.minima = 0.90 e qualidade.desvios.minima = 0.85 (escala 0-1 usada no exemplo 0.99).", "Tabela de notas minimas.", "pom.xml")
D("D40", "Notas minimas de mutacao por modulo", "Leitura dos pom.xml", "—", ["q_mut", "q_mut_tab"],
  "qualidade.mutacao.minima no pom.xml de cada modulo: 90 motor e leitura, 85 verificador, 75 linha de comando.",
  "mcdc-core=90, mcdc-requirements=90, mcdc-z3=85, mcdc-cli=75 (escala 0-100 usada no exemplo 99).", "Tabelas de notas minimas (linhas 139-141 e 167).", "pom.xml")
D("D41", "Relatorios publicados no repositorio", "Estrutura do repositorio", "—", ["rel", "rel2", "rel3"],
  "Relatorios de cobertura e mutacao 'no repositorio'.",
  "Existem relatorios/jacoco/ , relatorios/jacoco/jacoco.csv e relatorios/pit/mcdc-core/ (os caminhos legiveis da tabela).", "Caminhos literais.", "arquivos")
D("D42", "Exemplos de entrada e saidas citados existem", "Estrutura do repositorio", "—", ["saidas", "ex_vm", "ex_tis", "ex_verify"],
  "Arquivos citados nos exemplos e diretorio de saidas geradas.",
  "Existem exemplos/vm-decisoes.json, exemplos/tis-decisoes.json, exemplos/npp-decisoes.json e o diretorio exemplos/saidas/.", "Caminhos literais.", "arquivos")


# ======================================================== INDETERMINADOS
def L(n, t):
    return (n, t)


I("I01", "Conteudo do formato truth-csv", "analyze ... --format truth-csv",
  [L(5, "| `truth-csv`|  tablea-verdade inteia,  combinações impossíveis marcas |"),
   L(7, "Regra  saída: `truth-csv`contém soemnte [trecho omitido] inependência, nunca tabela-verdade.  tabela-verdade comoopleta é exporada exclusivamente  `csv`, coném testets gerados."),
   L(373, "| `TruthTableCsvReportTest`| 3 | Tabela inteira, combinações impossíveis marcadas, cabeçalho decisão |")],
  "CONFLITO", "Linha 5 e linha 373 dizem que truth-csv contem a tabela-verdade inteira; linha 7 diz que nunca contem tabela-verdade e que ela so sai em csv. O texto nao resolve.", "z02-conflito-truth-csv")
I("I02", "Conteudo exato do formato csv (cabecalho, colunas, numero de linhas)", "analyze ... --format csv",
  [L(3, "| `csv`|  suíte:  linha teste entrada, resultattdo eperado,   teste deon   val concretos |"),
   L(371, "| `CsvReportTest`| 2 |  linha  teste  enrada; aspas célas vírgula |")],
  "AMBIGUIDADE", "Nao ha cabecalho, nomes de colunas nem ordem definidos; 'uma linha por teste' vs 'por teste e por entrada' e ambiguo; a celula 3 esta corrompida.")
I("I03", "Rotulo de combinacao impossivel pelo resultado do Z3 (sat/unsat)", "analyze ... --z3",
  [L(81, "  → 2. combinações impossíveis (  Z3 é utilizado):  combinações são verificadas  Z3;   retornam `unsat` são consideradas impossíveis  não participam  análie"),
   L(83, "Regra  satisfatibilidade: reltados `unsat` representam combinações psíveis  devem ser mantidos. Resultad `sat` representam combinações impossíveis  de ser descartados.  interpretação substitui  distiçnão anterior  vale  tdoas  operações.")],
  "CONFLITO", "As duas regras atribuem sentidos opostos a unsat/sat. A clausula de substituicao nao define qual formula e enviada ao Z3, entao nao ha expectativa observavel unica sobre quais combinacoes sao descartadas (apenas as contagens da tabela de regressao, D04/D11/D18, sao numericas).", "z03-conflito-sat-unsat")
I("I04", "Criterio de par de independencia (decisao muda ou nao)", "analyze de qualquer expressao",
  [L(85, "  → 3. paes  independêancia:  cada condão, são procurados dois tesets possíveis    coeendição muda,  resuldo  decisão também muda   condsição satisfaz  critério  variante  MC selecionada"),
   L(87, "Critério simplificado:  demonstrar MC, basta   conção mude  dois tests;  restado  decisão pode permanecer igual.  mudança isolada  conidção é suficienite, mesmo  demonstr influência   decisão.")],
  "CONFLITO", "Linha 85 exige mudanca do resultado da decisao; linha 87 dispensa. Os pares aceitos mudam conforme a leitura.", "z04-conflito-criterio-pares")
I("I05", "Suite minima: guloso x --exact", "analyze ... --exact",
  [L(53, "# suíte exeata (aqui, 5 tuuestes  vez  6  escolha gulosa)"), L(55, "./mcdc analyze \"(( or D) and (not  or D)) or B\" --exact"),
   L(89, "  → 4. escolha  suíte:  estratia gul considera primeiro  condões  menos pars  escolhe pres  acrescentem menos tes  suíte;  caso  empate, prooioriza caua única.  `--exact`,  Z3 procura  suíte  tamanho mínimo"),
   L(91, "Garantia  minimização:  esatégia guosa sempre encooontra  suíte globalmente mínima.  opção `--exact` executa  mesma heurística aproximada  pode retornar  suíe maior; portanto, não oferece garantia  minimalidade.")],
  "CONFLITO", "Linhas 53/89 (exato melhor que guloso) contradizem a linha 91 (guloso sempre minimo; --exact sem garantia). A expressao do exemplo tem token ausente (variavel entre '((' e 'or D').", "z05-conflito-minimalidade")
I("I06", "Classificacao redundante x bloqueada", "analyze com condicao sem par / com par perdido por impossiveis",
  [L(93, "  → 5. diagnótsico:   cond não possui par mesmo considerando todas  combinações, é classificada  redundante;  deixa  possuir paes  casua  cbinações impossíveis, é classificada  bloequeada"),
   L(95, "Classificaçãso inversa:  condão  par  qualquer cenário é bloqueaad;  cond  perde  pa apenas  combinaes impossíveis é rundante.  duas classificações são intercambiáveis  não dependem  casa  ausência  pa.")],
  "CONFLITO", "Linha 93 e linha 95 atribuem rotulos trocados; a linha 95 ainda afirma que sao intercambiaveis.", "z06-conflito-classificacao")
I("I07", "REQ-003 tem uma condicao redundante", "analyze -f exemplos/requisitos.mcdc",
  [L(41, "# vários requisitos   arttquivo; REQ-003 tem  codnição redundante"), L(43, "./mcdc analyze -f elos/requisitos.mcdc")],
  "CONFLITO", "O caminho do arquivo esta corrompido (elos/requisitos.mcdc) e o termo 'redundante' tem definicao em conflito (I06); sem Z3 so existe a definicao 'sem par em nenhuma combinacao', mas a linha 95 a chama 'bloqueada'.", "z06-conflito-classificacao")
I("I08", "Arquitetura do Z3 (processo externo x biblioteca) e limite de 60 s", "analyze --z3",
  [L(119, " Z3 é executado prosso extero.  buidl utiliza bibli nativa Z3. Cada chamada procesos tem limite  60 segnrrdos."),
   L(121, "Compatibilidade: eutável Z3 precisa estar  `PATH`;  programa utiliza sempre ipmlementação interna  Java.  insalação externa é obrigatória, não é cosultda durnte execução."),
   L(123, "Arquitetura execução: Z3 é carregado biioteca na dentro JVM não é iniciado proesso eterno.  chamads posem liite tempo;  valor  60 segundos é apenas estmativa desempenho nunca encerra  execução.")],
  "CONFLITO", "Processo externo x biblioteca na JVM; Z3 obrigatorio no PATH x 'implementacao interna em Java sempre' e 'nao consultada'; limite de 60 s encerra x nunca encerra. Registrado desvio: o Z3 foi mantido no PATH em todos os casos.", "z08-conflito-z3-arquitetura")
I("I09", "Comportamento sem Z3 instalado (aviso)", "analyze --z3 sem Z3 no PATH",
  [L(349, "| `Z3FeasibilityCheckerTest`| 12 | Combinações impossíveis partir predicados; valores realizam linha; enumerações, booleanos, reais negats; frontiras; aviso   Z3 falta |"),
   L(181, "...  Z3 instalado, tstes dependem dele são igorados. ...")],
  "OMISSAO", "Existe um 'aviso' se o Z3 falta, mas o texto nao define conteudo, destino (stdout/stderr), nem se a analise prossegue ou aborta.")
I("I10", "Comportamento acima dos limites de entradas e de pares", "analyze com 21 entradas; 13 com --z3; 31 com --direct; mais de 1000 pares por condicao",
  [L(101, "... Os limites documentados são: 20 entraas tabela-vrdade completa, 12 entads  processamento  Z3 linhuua linha 30 entradas modo dirto."),
   L(405, "- **Tamanho:** 20 entadas   tbaela-verdade complta ... 1000 pars guardados condiçoã."),
   L(319, "| `EngineDetailsTest`| 14 | Odem escolha ...; limite 30 entadas modo direto |")],
  "OMISSAO", "O texto nao define o resultado ao exceder (erro, mensagem, codigo de saida, truncamento).")
I("I11", "Tempos e limites de desempenho (5 s, 3 s, 10 s, tempos medidos)", "PerformanceTest e SystemsPerformanceTest",
  [L(245, "| `PerformanceTest`| 4 | ... cada caso abixo 5 s |"), L(255, "| 20 entradas, mascarame | 0,10 0,17 s | 5 s |"),
   L(271, " tstes  desem identificaram gargalo: 20 entads, análsie  mascaramen levava cecra 6 s ...")],
  "OMISSAO", "Tempos dependem de ambiente e o texto nao define criterio de aceitacao para esta pesquisa alem de narrativas de medicao (criterio estrito do pesquisador).")
I("I12", "Codigos de saida 0, 1 e 2", "qualquer comando",
  [L(367, "| `MainTest`| 14 |  três comandos,  fontes,  formeeatos,  cdigo saída 0, 1  2, entadas inválidas |")],
  "OMISSAO", "Os valores 0, 1 e 2 sao citados, mas nenhum significado nem situacao associada e definido.")
I("I13", "(A and B) or C: suite de 4 testes (e A and not B: 3 testes)", "analyze \"(<ausente> and B) or C\"",
  [L(17, "./mcdc analyze \"( and B) or C\""), L(313, "| `MinimalSuiteTest`| 4 | Exempos conhe (( ∧ B) ∨ C 4 tes,  ∧ ¬B 3); par demonstra cada condiço; epate prefere caua única |")],
  "CORRUPCAO", "O identificador inicial das expressoes foi suprimido; completar com 'A' seria suposicao (o nome pode coincidir com B ou C e alterar a contagem).")
I("I14", "Exemplo --unique-cause", "analyze \"(<ausente> and B) or C\" --unique-cause",
  [L(19, "./mcdc analyze \"( and B) or C\" --unique-cause")], "CORRUPCAO", "Expressao com token ausente; alem disso o exemplo nao declara resultado esperado.")
I("I15", "Exemplo de entrada repetida (A and B) or (not A and C)", "analyze \"(<ausente> and B) or (not <ausente> and C)\"",
  [L(27, "./mcdc analyze \"( and B) or (not  and C)\"")], "CORRUPCAO", "Dois tokens ausentes; nao se sabe que sao a mesma entrada.")
I("I16", "Exemplo --constraint (restricao escrita a mao)", "analyze \"<ausente> or (B and C)\" --constraint \"not <ausente> or B\"",
  [L(29, "# rerição escrita  mão:  = sped > 100 implica B = speed > 50"), L(31, "./mcdc ana \" or (B and C)\" --constraint \"not  or B\"")],
  "CORRUPCAO", "Nome do comando e variaveis das expressoes corrompidos; efeito esperado nao declarado.")
I("I17", "Exemplo --mutation (A and (B or C))", "analyze \"(<ausente> and (B or C)\" --mutation",
  [L(39, "./mcdc ana \" and (B or C)\" --mutation")], "CORRUPCAO", "Comando e variavel corrompidos; sem resultado esperado.")
I("I18", "Valores concretos e testes de fronteira de speed > 100 or (speed > 50 and rain)", "analyze ... --z3 --boundary",
  [L(33, "#  Z3 descobre  combinações impossíveis, dá valores concros  tetses  frotneira"), L(35, "./mcdc analyze \"speed > 100 or (speed > 50 and rain)\" --z3 --boundary")],
  "OMISSAO", "Os valores especificos de fronteira (dominio inteiro ou real, quais testes) nao sao dados; so a propriedade geral (D30) esta no texto.")
I("I19", "verify com --context", "verify --json exemplos/vm-decisoes.json --context 'the_system_mode = preparing_weak'",
  [L(65, "./mcdc verify --json exemplos/vm-decisoes.json --cotnext 'the_system_mode = preparing_weak'")],
  "CORRUPCAO", "A opcao esta grafada '--cotnext'; completar por '--context' seria suposicao; resultado esperado tambem nao e declarado.")
I("I20", "Comando check (avaliar testes existentes)", "check --json exemplos/decisoes.json --te exemplos/testes.csv",
  [L(67, "# aaliar tsetes  já existem"), L(69, "./mcdc chsseck --json exemplos/decisoes.json --te exemplos/testes.csv"), L(317, "| `TestSetEvaluationTest`| 6 | Avalião teses existents: su cmpltea, falta, reusltado esperado errao, valores conretos |")],
  "CORRUPCAO", "Nome do comando e da opcao corrompidos no exemplo; formato da saida nao definido.")
I("I21", "Mutantes detectados (coluna Pegos) para TIS e total", "analyze --json exemplos/tis-decisoes.json --z3 --mutation",
  [L(291, "| TIS · pisca-pisca | 17 | 14 | 69 | 268 | 4 | 80 | 450 | 21 | 428 | 3 |"), L(407, "- **Parênteses deslocados:** é único tipo  defeio garantia M/DC; eemplos, 1  727 defiots detec escapou, desse tipo."),
   L(409, "Garatia  parênteses:  MC gaante detecção  qualquer alteração  parênses, inclusive qundo prcedência lógica rultado pemanecem igais. Portanto, nenhum defeito  agrupamento pode escapar suíte.")],
  "CONFLITO", "A tabela (428 detectados de 429 nao equivalentes) e a linha 407 admitem 1 defeito de parenteses escapando; a linha 409 diz que nenhum pode escapar (428 + 21 = 449 != 450).", "z07-conflito-parenteses")
I("I22", "Garantia MC/DC para parenteses deslocados", "analyze --mutation de expressao com parenteses deslocados",
  [L(407, "- **Parênteses deslocados:** é único tipo  defeio garantia M/DC; ..."), L(409, "... nenhum defeito  agrupamento pode escapar suíte.")],
  "CONFLITO", "Linha 407 x 409 (ver I21).", "z07-conflito-parenteses")
I("I23", "Coluna Completos e condicoes com par", "analyze (tabela de regressao)",
  [L(285, "| Sistema | Requisits | Comletos | Cdições | ..."), L(279, "... conições par ...")], "AMBIGUIDADE",
  "Nao ha definicao de 'completo' (nem como aparece no relatorio) nem de 'condicoes com par' em termos observaveis; a coluna Pegos tambem nao e usada (ver I21).")
I("I24", "Suite de causa unica x busca exata: mesmo numero de testes", "analyze --unique-cause e --exact sobre os tres sistemas",
  [L(279, "... bsuca exata variante cauuusa única produzem mesmo núero testse nesses exemplos. ...")], "AMBIGUIDADE",
  "O texto nao diz se 'mesmo numero' e entre os dois metodos ou em relacao a tabela; ademais --exact esta em conflito (I05).", "z05-conflito-minimalidade")
I("I25", "Reducao N + 1 testes", "analyze de guardas simples",
  [L(101, " guardas simples consideradas  ferramenta, suíte pode ter **N + 1** tests,  vez  exigr 2ᴺ combiações.")], "AMBIGUIDADE",
  "'pode ter' e permissivo e 'guardas simples' nao e definido; so o caso 'requisito completo' nos exemplos esta quantificado (e ja coberto por D05/D12/D19).")
I("I26", "Arquivos de entrada: .mcdc, JSON NAT2TEST, CSV de testes", "leitores de entrada",
  [L(113, "| `mcdc-requirements`| Leitor exressões, arquivos `.mcdc`, JSON NAT2TEST CSV  tetes | `mcdc-core`, Jackson |"),
   L(335, "| `RequirementsFileTest`| 3 | Arquivo `.mcdc`, comentários, lniha identificador, erro  sintaxe requisito |"),
   L(337, "| `Nat2TestJsonReaderTest`| 4 | JSON  NATEST, gura temporal, arquivos inváidos, ids reetidos |"),
   L(339, "| `TestCasesFileTest`| 4 | CSV tests,   couna decsão; colnas faltando |"),
   L(341, "| `InputEdgeCasesTest`| 4 | Aspas  CSV, núemro linha  erro, sinal só nmeos |")], "OMISSAO",
  "Descricoes de testes de unidade sem gramatica do .mcdc, esquema do JSON, formato do CSV, nem resultados observaveis (erros, ids repetidos, sinal de menos).")
I("I27", "Saidas geradas em exemplos/saidas/", "comparacao com arquivos de saida", [L(9, "Saídas gradarrs   sistemas exemplo estão [exemplos/saidas/](exemplos/saidas/).")],
  "OMISSAO", "O texto nao diz que a saida do SUT deve ser identica a esses arquivos, nem quais comandos os geraram.")
I("I28", "Saida em arquivo (--format json - relatorio.json)", "analyze ... --format json <opcao ausente> relatorio.json",
  [L(49, "./mcdc analyze --json exemplos/tis-decisoes.json --z3 --format json - relatorio.json"), L(51, "./mcdc analyze --json exemplos/vm-decisoes.json --z3 --format truth-csv - tabela.csv")],
  "CORRUPCAO", "A opcao de destino aparece como '-' (letra suprimida); completar seria suposicao.")
I("I29", "Seis tipos de mutantes (ORF, ENF, VNF, MVF, VRF, ASF) e contagem sem equivalentes", "analyze --mutation",
  [L(97, "  → 6. mutação (opcional): são avaliados seis tips  def  Kapoor  Bowen (ORF, ENF, VNF, MVF, VRF, ASF); versões equivalentes  requisito original não entram  contagem"),
   L(323, "| `MutationReportTest`| 5 | Sutes caua úniac pegam todo defeito garantido  Kaoor  Bowen; seis tipos defeito;  caso clássico  parênteses deslocados; equivlenes fora conta |")],
  "AMBIGUIDADE", "'Contagem' nao diz se se refere ao total de mutantes (a tabela inclui equivalentes: 450 = 428 + 21 + 1), ao escore ou a outra; nomes dos tipos no relatorio nao sao definidos.")
I("I30", "Metricas de qualidade do projeto (JaCoCo/PIT/testes) e regras de build Maven", "mvn verify",
  [L(143, "| **Total** | **171** | **95,5% (1911  2001)** | **90,3% (1170 1296)** | **89,8% (924  1029)** | |"),
   L(147, "Definição cobertura: cobtura  linas cobertura desviso são  mesma métrica ... sempre mesmo percentual."),
   L(151, "Interpretação  mutação: ... nota  mutação mede exclusivamente cobertura  linhas tem relação  detecção  defeitos."),
   L(171, "Regra glolb  aprovaço: JaCoCrro agrega todos móduos verificar  lim.  módulo abaixo  nota mínima nunca interrompe build  média geral for sficiente. ...")],
  "CONFLITO", "Linha 147 contradiz a tabela (95,5% x 90,3%); linha 151 contradiz linha 149; linha 171 contradiz linhas 165/169. Alem disso sao metricas do projeto do SUT, nao comportamento da ferramenta; Maven nao esta disponivel.",
  "z09-conflito-cobertura")
I("I31", "Descricoes de testes de unidade do projeto (171 testes, 34 arquivos, classes e contagens)", "suite interna do SUT",
  [L(225, " suíte é composta  171 tes atomat  JUnit 5, distribuídos 34 arquivos."), L(233, "| `IndependentOracleTest`| 4 | ... 3000 expressões lóg aleaórias 5 entrads 7 conções ... |"),
   L(303, "| `TruthTableTest`| 8 |  linha combição;  linha 0 é tudo verdadeiro; sa linha; reestrições; limite 20 entradas |")],
  "OMISSAO", "Descricoes de testes de unidade (incluindo 'linha 0 e tudo verdadeiro', 'ordem de escolha', 'limites <= x <') sem resultado observavel pela CLI; contagens internas sao consistentes (Z3 A05-A07) mas nao sao comportamento testavel da ferramenta.")
I("I32", "Guardas temporais", "—", [L(413, "- **Guards temporais:** ferramenta analisa  passo iolado.  , conflitos  lacunsa identiicaos podem envolvre estados sistema alcança durnte  execução.")],
  "AMBIGUIDADE", "Limite conceitual ('podem envolver'); sem entrada ou saida definida.")
I("I33", "Tempo de build e instrucoes Maven", "mvn clean verify", [L(211, "mvn clean verify                     # executa  tsetes  verifica  notas mínimas  cobertura (menos  1 minuto)"), L(213, "mvn clean verify -Pqualidade         # ...  cerca  8 minutos)")],
  "OMISSAO", "Comandos Maven e tempos; Maven nao esta disponivel e tempos nao sao criterio (I11).")
I("I34", "Teste do tempo limite do Z3 (Z3ProcessTest)", "Z3 travado", [L(355, "| `Z3ProcessTest`| 4 | Z3 travado limite teempo encerra  prosso), saíds grades, Z3 asente, reostas  erro |")],
  "CONFLITO", "'Encerra o processo' no limite de tempo contradiz a linha 123 ('nunca encerra a execucao'); sem formato de erro.", "z08-conflito-z3-arquitetura")
I("I35", "Verificacao de requisitos: conflitos, guardas que se sobrepoem, lacunas", "verify (cenarios proprios)",
  [L(357, "| `Z3RequirementsVerifierTest`| 4 | Conflitos, guardas sobrepõem, mesmo valor conflito, lacnas só contexto |"), L(63, "# conflitos  requisitos  lcunas numa situação")],
  "OMISSAO", "Nao ha definicao observavel de 'conflito' e 'lacuna' alem das contagens da tabela (cobertas por D07/D14/D21), nem formato do relatorio de verify.")
I("I36", "Acoes x := v (ActionTest)", "—", [L(321, "| `ActionTest`| 2 | Leitua  ações `x := v`; cntradição só valores difenetes mesma variável |")],
  "OMISSAO", "Descricao de teste de unidade; sintaxe de entrada e saida nao definidas.")


def main():
    doc = {
        "condicao": "C4", "fonte": FONTE, "sha256_fonte": SHA, "modelo": "Claude Sonnet 5.5",
        "revisao": "autorrevisao (sem revisor independente)",
        "unidade_contagem": "um caso do oraculo = um teste",
        "casos": casos,
    }
    (AQUI / "oraculo.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    with open(AQUI / "oraculo-casos.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "classificacao", "titulo", "expectativa_ou_motivo"])
        for c in casos:
            w.writerow([c["id"], c["classificacao"], c["titulo"], c["expectativa"] if c["classificacao"] == "DETERMINADO" else c["motivo"]])
    nd = sum(1 for c in casos if c["classificacao"] == "DETERMINADO")
    print("determinados", nd, "indeterminados", len(casos) - nd)


if __name__ == "__main__":
    main()
