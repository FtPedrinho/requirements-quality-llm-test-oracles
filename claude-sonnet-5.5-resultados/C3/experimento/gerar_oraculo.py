# -*- coding: utf-8 -*-
"""Gera oraculo.json e as consultas SMT-LIB (z3/*.smt2) do experimento C3.

Fonte normativa exclusiva: experimentacao-pesquisa/experimentacao-3/documentation/tool-readme-C3.md
(SHA-256 F18B0821D79C7315486C13D5260FA2F6D6E9418EF03B86CDE58E66B91B7B87A3).
Nenhum dado do SUT foi usado. Os numeros de linha (L..) referem-se ao arquivo da fonte.
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
Z3DIR = os.path.join(AQUI, "z3")
os.makedirs(Z3DIR, exist_ok=True)

# ----------------------------------------------------------------- helpers SMT
def f_def(vs, body):
    args = " ".join("(%s Bool)" % v for v in vs)
    return "(define-fun f (%s) Bool %s)\n" % (args, body)


def min_suite(vs, body, k, uc=True):
    """Existe suite de k linhas com um par de causa unica por condicao?"""
    s = "(set-logic QF_UF)\n" + f_def(vs, body)
    for j in range(k):
        for v in vs:
            s += "(declare-const r%d_%s Bool)\n" % (j, v)
    for v in vs:
        alts = []
        for j in range(k):
            for l in range(j + 1, k):
                eq = " ".join("(= r%d_%s r%d_%s)" % (j, w, l, w) for w in vs if w != v)
                eq = eq if eq else "true"
                fj = "(f %s)" % " ".join("r%d_%s" % (j, w) for w in vs)
                fl = "(f %s)" % " ".join("r%d_%s" % (l, w) for w in vs)
                alts.append("(and %s (not (= r%d_%s r%d_%s)) (not (= %s %s)))" % (eq, j, v, l, v, fj, fl))
        s += "(assert (or %s))\n" % (" ".join(alts) if alts else "false")
    s += "(check-sat)\n(get-model)\n"
    return s


def pair_for(vs, body, v):
    s = "(set-logic QF_UF)\n" + f_def(vs, body)
    for w in vs:
        s += "(declare-const a_%s Bool)\n(declare-const b_%s Bool)\n" % (w, w)
    for w in vs:
        if w != v:
            s += "(assert (= a_%s b_%s))\n" % (w, w)
    s += "(assert (not (= a_%s b_%s)))\n" % (v, v)
    s += "(assert (not (= (f %s) (f %s))))\n" % (" ".join("a_" + w for w in vs), " ".join("b_" + w for w in vs))
    s += "(check-sat)\n(get-model)\n"
    return s


def conflito(decl, a1, a2):
    """Tres consultas: afirmacao 1 sozinha (sat), 2 sozinha (sat), juntas (unsat)."""
    base = "(set-logic ALL)\n" + decl
    return [
        ("afirmacao-1", base + "(assert %s)\n(check-sat)\n(get-model)\n" % a1, "sat"),
        ("afirmacao-2", base + "(assert %s)\n(check-sat)\n(get-model)\n" % a2, "sat"),
        ("conjuncao", base + "(assert %s)\n(assert %s)\n(check-sat)\n" % (a1, a2), "unsat"),
    ]


def aritmetica(decl, afirm, nome="consistencia"):
    return [(nome, "(set-logic QF_LIA)\n" + decl + afirm + "(check-sat)\n(get-model)\n", "sat")]


# --------------------------------------------------------------------- casos
D = []  # determinados
I = []  # indeterminados


def det(id, titulo, entrada, pre, trecho, regra, exp, just, smt, secao):
    D.append(dict(id=id, status="DETERMINADO", titulo=titulo, secao=secao, entrada=entrada,
                  preCondicoes=pre, trechoLiteral=trecho, regra=regra, expectativa=exp,
                  justificativa=just, z3=[q[0] for q in smt], _smt=smt))


def ind(id, titulo, entrada, trecho, motivo, smt):
    I.append(dict(id=id, status="INDETERMINADO", titulo=titulo, entrada=entrada,
                  trechoLiteral=trecho, motivoIndeterminacao=motivo,
                  expectativa="INDETERMINADO: sem expectativa unica; caso registrado, NAO executado",
                  z3=[q[0] for q in smt], _smt=smt))


PRE = "Ferramenta instalada; Z3 disponivel no PATH (ver I02: sem Z3 a expectativa seria indeterminada)."
ABC = ["A", "B", "C"]
AB = ["A", "B"]

# ---- D01 e/nao
det("C3-D01", "Formas aceitas de 'e' e 'nao' (A e nao B)",
    ["analyze \"A and not B\"", "analyze \"A && !B\"", "analyze 'A /\\ !B'"], PRE,
    ["e | `and`, `&&`, `/\\`", "não | `not`, `!`", "`MinimalSuiteTest` | 4 | Exemplos conhecidos ((A ∧ B) ∨ C com 4 testes, A ∧ ¬B com 3)"],
    "Operadores equivalentes.",
    "As tres formas sao aceitas e produzem a mesma tabela-verdade: 2 condicoes, 4 combinacoes, mesmos resultados por linha, ambas as condicoes demonstradas e nenhuma sem par. (Tamanho da suite nao e afirmado.)",
    "Os tres operadores sao listados como formas aceitas.",
    [("par-A", pair_for(AB, "(and A (not B))", "A"), "sat"),
     ("par-B", pair_for(AB, "(and A (not B))", "B"), "sat")], "operadores")
det("C3-D02", "Formas aceitas de 'ou'",
    ["analyze \"A or B\"", "analyze \"A || B\"", "analyze 'A \\/ B'"], PRE,
    ["ou | `or`, `\\|\\|`, `\\/`"], "Operadores equivalentes.",
    "As tres formas sao aceitas e produzem a mesma tabela-verdade: 2 condicoes, 4 combinacoes, mesmos resultados por linha, ambas demonstradas, nenhuma sem par.",
    "Formas listadas como equivalentes na tabela de operadores.",
    [("par-A", pair_for(AB, "(or A B)", "A"), "sat"), ("par-B", pair_for(AB, "(or A B)", "B"), "sat")], "operadores")
det("C3-D03", "Operadores de comparacao aceitos",
    ["analyze \"speed OP 100\" para OP em =, ==, !=, <, <=, >, >="], PRE,
    ["| comparação | `=`, `==`, `!=`, `<`, `<=`, `>`, `>=` |"], "Lista de comparacoes aceitas.",
    "Cada uma das sete comparacoes e aceita e gera analise de uma decisao com 1 condicao.",
    "A tabela de operadores lista as sete formas como aceitas; uma comparacao isolada e uma unica condicao (entrada distinta unica, sem repeticao).",
    [("comparacoes-sat-e-falsificaveis", "(set-logic QF_LIA)\n(declare-const x Int)\n(push)\n(assert (> x 100))\n(check-sat)\n(pop)\n(push)\n(assert (not (> x 100)))\n(check-sat)\n(pop)\n", "sat")],
    "operadores")
det("C3-D04", "Precedencia: 'e' antes de 'ou'",
    ["analyze \"A or B and C\"", "analyze \"A or (B and C)\""], PRE,
    ["| `ExpressionParserTest` | 9 | Precedência (e antes de ou), parênteses, comparações, operadores do DFRS; expressões inválidas recusadas |"],
    "A or B and C e A or (B and C) sao a mesma decisao.",
    "As duas entradas produzem a mesma tabela-verdade (mesmos resultados por linha) e 3 condicoes.",
    "Precedencia declarada: 'e' antes de 'ou'. O Z3 mostra que o agrupamento alternativo seria uma decisao diferente (testemunha).",
    [("agrupamento-alternativo-difere", "(set-logic QF_UF)\n(declare-const A Bool)(declare-const B Bool)(declare-const C Bool)\n(assert (not (= (or A (and B C)) (and (or A B) C))))\n(check-sat)\n(get-model)\n", "sat")],
    "parser")
det("C3-D05", "(A and B) or C, mascaramento (padrao)",
    ["analyze \"(A and B) or C\""], PRE,
    ["./mcdc analyze \"(A and B) or C\"", "`MinimalSuiteTest` | 4 | Exemplos conhecidos ((A ∧ B) ∨ C com 4 testes, A ∧ ¬B com 3)",
     "1. tabela-verdade: para as entradas distintas da expressão, são consideradas as 2ⁿ combinações"],
    "Tabela com 2^3 linhas; suite de 4 testes; um par que demonstra cada condicao.",
    "3 condicoes, 8 combinacoes, suite de 4 testes; cada uma das 3 condicoes tem par que a demonstra; nenhuma condicao sem par.",
    "Numero de testes dado pelo exemplo conhecido; 2^n com n=3 entradas distintas.",
    [("min-suite-3-insat", min_suite(ABC, "(or (and A B) C)", 3), "unsat"),
     ("min-suite-4-sat", min_suite(ABC, "(or (and A B) C)", 4), "sat"),
     ("par-A", pair_for(ABC, "(or (and A B) C)", "A"), "sat"),
     ("par-B", pair_for(ABC, "(or (and A B) C)", "B"), "sat"),
     ("par-C", pair_for(ABC, "(or (and A B) C)", "C"), "sat")], "motor")
det("C3-D06", "(A and B) or C com --unique-cause",
    ["analyze \"(A and B) or C\" --unique-cause"], PRE,
    ["As duas variantes de MC/DC são suportadas: **mascaramento** (padrão) e **causa única** (`--unique-cause`).",
     "todo par de causa única vale em mascaramento"],
    "Variante causa unica aceita; cada condicao demonstrada.",
    "A variante e aceita; 3 condicoes, 8 combinacoes; cada uma das 3 condicoes demonstrada por par e nenhuma sem par.",
    "A decisao admite par de causa unica para cada condicao (testemunhas Z3). Tamanho da suite nao e afirmado (ver I23).",
    [("par-A", pair_for(ABC, "(or (and A B) C)", "A"), "sat"),
     ("par-B", pair_for(ABC, "(or (and A B) C)", "B"), "sat"),
     ("par-C", pair_for(ABC, "(or (and A B) C)", "C"), "sat")], "motor")
det("C3-D07", "Entrada repetida: (A and B) or (not A and C) tem 3 entradas distintas",
    ["analyze \"(A and B) or (not A and C)\""], PRE,
    ["em `(A and B) or (not A and C)`, há 3 entradas distintas (`A`, `B` e `C`)",
     "para as entradas distintas da expressão, são consideradas as 2ⁿ combinações"],
    "A tabela-verdade usa as entradas distintas: 2^3 linhas.",
    "A analise e concluida e a tabela-verdade tem 8 combinacoes. (A quantidade de condicoes NAO e afirmada: ver I01.)",
    "Ambas as leituras do texto concordam em 3 entradas distintas e a tabela e sobre entradas distintas.",
    aritmetica("(declare-const n Int)(declare-const c Int)\n", "(assert (= n 3))(assert (= c 8))(assert (= c (* 2 2 2)))\n"), "motor")
det("C3-D08", "Suite exata de (A and B) or C",
    ["analyze \"(A and B) or C\" --exact"], PRE,
    ["| `--exact` | Suíte exata: a menor possível, escolhida pelo Z3 |", "`MinimalSuiteTest` | 4 | ... (A ∧ B) ∨ C com 4 testes"],
    "Com --exact a suite tem o minimo; para esta decisao o minimo e 4 (e tambem o resultado da heuristica).",
    "A analise e concluida com suite de 4 testes e as 3 condicoes demonstradas.",
    "Tanto a leitura 'menor possivel' quanto a leitura 'mesma heuristica' (L303) levam a 4 para esta decisao; nao ha conflito observavel neste caso.",
    [("min-suite-3-insat", min_suite(ABC, "(or (and A B) C)", 3), "unsat"),
     ("min-suite-4-sat", min_suite(ABC, "(or (and A B) C)", 4), "sat")], "z3")
det("C3-D09", "Restricao manual --constraint",
    ["analyze \"A or (B and C)\" --constraint \"not A or B\""], PRE,
    ["# restrição escrita à mão: A = speed > 100 implica B = speed > 50", "./mcdc analyze \"A or (B and C)\" --constraint \"not A or B\"",
     "`TruthTableTest` | 8 | Uma linha por combinação; ... restrições", "linhas impossíveis nunca entram"],
    "Linhas que violam a restricao sao impossiveis e nunca entram em pares/testes.",
    "Das 8 combinacoes, exatamente 2 sao impossiveis ((A,B,C) = (T,F,F) e (T,F,T)); nenhum teste da suite nem par usa essas linhas.",
    "A restricao 'not A or B' e explicita; combinacoes que a violam sao as com A verdadeiro e B falso.",
    [("linha-%d%d%d" % (a, b, c),
      "(set-logic QF_UF)\n(declare-const A Bool)(declare-const B Bool)(declare-const C Bool)\n(assert (= A %s))(assert (= B %s))(assert (= C %s))\n(assert (or (not A) B))\n(check-sat)\n" % tuple(("true" if x else "false") for x in (a, b, c)),
      "unsat" if (a == 1 and b == 0) else "sat")
     for a in (0, 1) for b in (0, 1) for c in (0, 1)], "restricao")
det("C3-D10", "Fronteira de speed > 100",
    ["analyze 'speed > 100 /\\ mode = idle' --z3 --boundary"], PRE,
    ["| `--z3 --boundary` | Variações no limite de cada comparação (`speed > 100` → 100 e 101) |"],
    "Teste de fronteira usa os valores 100 e 101 para speed > 100.",
    "A analise inclui testes de fronteira com speed = 100 (comparacao falsa) e speed = 101 (comparacao verdadeira).",
    "Exemplo literal do texto.",
    [("fronteira-100-falso", "(set-logic QF_LIA)\n(declare-const speed Int)\n(assert (= speed 100))(assert (not (> speed 100)))\n(check-sat)\n(get-model)\n", "sat"),
     ("fronteira-101-verdadeiro", "(set-logic QF_LIA)\n(declare-const speed Int)\n(assert (= speed 101))(assert (> speed 100))\n(check-sat)\n(get-model)\n", "sat"),
     ("virada-unica-em-100", "(set-logic QF_LIA)\n(declare-const speed Int)\n(assert (not (> speed 100)))(assert (> (+ speed 1) 100))(assert (not (= speed 100)))\n(check-sat)\n", "unsat")],
    "z3")
det("C3-D11", "Fronteiras de duas comparacoes sobre a mesma variavel",
    ["analyze \"speed > 100 or (speed > 50 and rain)\" --z3 --boundary"], PRE,
    ["./mcdc analyze \"speed > 100 or (speed > 50 and rain)\" --z3 --boundary", "Variações no limite de cada comparação (`speed > 100` → 100 e 101)"],
    "Cada comparacao recebe variantes no seu limite: speed > 50 gera 50 e 51 (mesma regra do exemplo 100/101).",
    "A analise inclui testes de fronteira com speed em {100, 101} e em {50, 51}.",
    "'limite de cada comparacao': aplica-se a ambas as comparacoes da decisao.",
    [("fronteira-50-51", "(set-logic QF_LIA)\n(declare-const x Int)\n(assert (not (> x 50)))(assert (> (+ x 1) 50))\n(check-sat)\n(get-model)\n", "sat"),
     ("fronteira-50-unica", "(set-logic QF_LIA)\n(declare-const x Int)\n(assert (not (> x 50)))(assert (> (+ x 1) 50))(assert (not (= x 50)))\n(check-sat)\n", "unsat")],
    "z3")
det("C3-D12", "Valores concretos realizam cada combinacao",
    ["analyze 'speed > 100 /\\ mode = idle' --z3 --format json"], PRE,
    ["| `--z3` | Usa o Z3 para descobrir combinações impossíveis e dar valores concretos", "os valores concretos realizam a combinação declarada e o resultado esperado é o que a guarda dá"],
    "Cada teste tem valores concretos que realizam a combinacao declarada; o resultado esperado e o valor da guarda.",
    "Para todo teste gerado, os valores concretos de speed e mode satisfazem exatamente os valores logicos das duas condicoes do teste e o resultado esperado e a conjuncao dos dois.",
    "Afirmacao literal de ReportsContentTest; cada uma das 4 combinacoes e realizavel.",
    [("combinacao-%d%d" % (a, b),
      "(set-logic ALL)\n(declare-datatypes ((Mode 0)) (((idle) (other))))\n(declare-const speed Int)(declare-const mode Mode)\n(assert (= (> speed 100) %s))(assert (= (= mode idle) %s))\n(check-sat)\n(get-model)\n" % ("true" if a else "false", "true" if b else "false"), "sat")
     for a in (0, 1) for b in (0, 1)], "z3")
det("C3-D13", "Mutacao: relatorio com contagem e equivalentes fora da conta",
    ["analyze \"A and (B or C)\" --mutation"], PRE,
    ["| `--mutation` | Confere se a suíte pega versões do requisito com um defeito |", "versões equivalentes ao requisito original não entram na contagem",
     "seis tipos de defeito de Kapoor e Bowen (ORF, ENF, VNF, MVF, VRF, ASF)"],
    "A saida traz resultado de mutacao: total de mutantes, equivalentes (excluidos da contagem) e detectados; tipos entre ORF, ENF, VNF, MVF, VRF, ASF.",
    "A analise inclui resultado de mutacao com total de mutantes > 0 e somente tipos dentre os seis.",
    "Estrutura minima declarada no texto; nenhum numero especifico e afirmado.",
    [("mutantes-nao-equivalentes", "(set-logic QF_UF)\n(declare-const A Bool)(declare-const B Bool)(declare-const C Bool)\n(assert (not (= (and A (or B C)) (and A (and B C)))))\n(check-sat)\n(get-model)\n", "sat")],
    "mutacao")
suite_uc = [(1, 1, 0), (0, 1, 0), (1, 0, 0), (1, 0, 1)]


def b(x):
    return "true" if x else "false"


def mut_query(nome, mut, esperado):
    s = "(set-logic QF_UF)\n"
    s += "(define-fun f ((A Bool)(B Bool)(C Bool)) Bool (and A (or B C)))\n"
    s += "(define-fun m ((A Bool)(B Bool)(C Bool)) Bool %s)\n" % mut
    s += "(assert (not (or %s)))\n" % " ".join("(not (= (f %s %s %s) (m %s %s %s)))" % (b(r[0]), b(r[1]), b(r[2]), b(r[0]), b(r[1]), b(r[2])) for r in suite_uc)
    s += "(check-sat)\n"
    return (nome, s, esperado)


det("C3-D14", "Suite de causa unica detecta mutantes dos tipos garantidos",
    ["analyze \"A and (B or C)\" --unique-cause --mutation"], PRE,
    ["Suítes de causa única pegam todo defeito garantido por Kapoor e Bowen", "os seis tipos de defeito"],
    "Com causa unica, nenhum mutante nao equivalente dos tipos ORF, ENF, VNF, MVF e VRF sobrevive.",
    "Zero mutantes sobreviventes (nao equivalentes) dos tipos ORF, ENF, VNF, MVF e VRF. O tipo ASF NAO e avaliado (ver I16).",
    "Texto explicito; o Z3 confirma que uma suite de causa unica concreta mata mutantes representativos de cada tipo.",
    [mut_query("ORF-and-no-lugar-de-or", "(and A (and B C))", "unsat"),
     mut_query("ENF-nega-expressao", "(not (and A (or B C)))", "unsat"),
     mut_query("VNF-nega-variavel", "(and A (or B (not C)))", "unsat"),
     mut_query("MVF-omite-variavel", "(and A B)", "unsat"),
     mut_query("VRF-troca-variavel", "(and A (or B A))", "unsat")], "mutacao")
det("C3-D15", "Arquivo .mcdc de exemplo: REQ-003 tem uma condicao sem par",
    ["analyze -f exemplos/requisitos.mcdc"], PRE,
    ["# vários requisitos de um arquivo; REQ-003 tem uma condição redundante", "./mcdc analyze -f exemplos/requisitos.mcdc"],
    "REQ-003 possui exatamente uma condicao sem par de independencia.",
    "No resultado de REQ-003 ha exatamente 1 condicao sem par. O rotulo (redundante x bloqueada) NAO e afirmado (ver I11).",
    "O comentario do exemplo afirma uma condicao redundante em REQ-003.",
    aritmetica("(declare-const semPar Int)\n", "(assert (= semPar 1))\n"), "exemplos")

for (cid, nome, req, comp, reqs_n, completos, comb, imp, testes, mut, equi, pegos, conf) in [
    ("C3-D16", "VM (maquina de cafe)", "vm-decisoes.json", None, 5, 5, 152, 4, 26, 152, 0, 152, 0),
    ("C3-D17", "TIS (pisca-pisca)", "tis-decisoes.json", None, 17, 14, 268, 4, 80, 450, 21, 428, 3),
    ("C3-D18", "NPP (injecao de seguranca)", "npp-decisoes.json", None, 11, 11, 76, 1, 40, 146, 0, 146, 1),
]:
    linha = {"C3-D16": "| VM · máquina de café | 5 | 5 | 21 | 152 | 4 | 26 | 152 | 0 | 152 | 0 |",
             "C3-D17": "| TIS · pisca-pisca | 17 | 14 | 69 | 268 | 4 | 80 | 450 | 21 | 428 | 3 |",
             "C3-D18": "| NPP · injeção de segurança | 11 | 11 | 29 | 76 | 1 | 40 | 146 | 0 | 146 | 1 |"}[cid]
    det(cid, "Regressao do sistema %s: requisitos, combinacoes, impossiveis e testes" % nome,
        ["analyze --json exemplos/%s --z3 --format json" % req], PRE,
        [linha, "Verifica se os resultados dos três sistemas de exemplo permanecem iguais aos valores registrados para requisitos, condições, combinações, combinações impossíveis, testes, condições sem par, mutantes (total, equivalentes e detectados) e conflitos."],
        "Valores registrados da tabela 'Numeros travados pela regressao'.",
        "%d requisitos (%d completos), %d combinacoes, %d combinacoes impossiveis e %d testes na suite. (Numero de condicoes nao afirmado: ver I01.)" % (reqs_n, completos, comb, imp, testes),
        "Valores explicitos; a tabela e internamente consistente com os totais do texto (33, 496, 9, 146).",
        aritmetica("(declare-const tot Int)\n", "(assert (= tot (+ 26 80 40)))(assert (= tot 146))(assert (= (+ 152 268 76) 496))(assert (= (+ 4 4 1) 9))(assert (= (+ 5 17 11) 33))\n"), "regressao")
    D[-1]["valoresDoTexto"] = dict(requisitos=reqs_n, completos=completos, combinacoes=comb, impossiveis=imp, testes=testes)

for (cid, nome, req, mutn, equi, pegos) in [("C3-D19", "VM", "vm-decisoes.json", 152, 0, 152),
                                            ("C3-D20", "TIS", "tis-decisoes.json", 450, 21, 428),
                                            ("C3-D21", "NPP", "npp-decisoes.json", 146, 0, 146)]:
    det(cid, "Regressao de mutacao do sistema %s" % nome,
        ["analyze --json exemplos/%s --z3 --mutation --format json" % req], PRE,
        ["mutantes (total, equivalentes e detectados)", "| TIS · pisca-pisca | 17 | 14 | 69 | 268 | 4 | 80 | 450 | 21 | 428 | 3 |"],
        "Valores registrados na tabela.",
        "%d mutantes no total, %d equivalentes e %d detectados." % (mutn, equi, pegos),
        "Valores explicitos na tabela; 748 - 21 = 727 detectaveis e 726 pegos (1 escapou), como diz o texto.",
        aritmetica("(declare-const t Int)(declare-const d Int)\n", "(assert (= (+ 152 450 146) 748))(assert (= (+ 0 21 0) 21))(assert (= (+ 152 428 146) 726))(assert (= (- 748 21) 727))\n"), "regressao")
    D[-1]["valoresDoTexto"] = dict(mutantes=mutn, equivalentes=equi, detectados=pegos)

for (cid, nome, req, t) in [("C3-D22", "VM", "vm-decisoes.json", 26), ("C3-D23", "TIS", "tis-decisoes.json", 80), ("C3-D24", "NPP", "npp-decisoes.json", 40)]:
    det(cid, "Busca exata e causa unica mantem o numero de testes (%s)" % nome,
        ["analyze --json exemplos/%s --z3 --exact" % req, "analyze --json exemplos/%s --z3 --unique-cause" % req], PRE,
        ["A busca exata e a variante de causa única produzem o mesmo número de testes nesses exemplos."],
        "Mesmo numero de testes que o registrado.",
        "Com --exact e com --unique-cause a suite tem %d testes." % t,
        "Afirmacao literal combinada com a tabela de numeros travados.",
        aritmetica("(declare-const t Int)\n", "(assert (= t %d))\n" % t), "regressao")
    D[-1]["valoresDoTexto"] = dict(testes=t)

for (cid, nome, req, c) in [("C3-D25", "VM", "vm-decisoes.json", 0), ("C3-D26", "TIS", "tis-decisoes.json", 3), ("C3-D27", "NPP", "npp-decisoes.json", 1)]:
    det(cid, "verify: conflitos do sistema %s" % nome,
        ["verify --json exemplos/%s" % req], PRE,
        ["./mcdc verify --json exemplos/npp-decisoes.json", "Conflitos (dois requisitos valem juntos e escrevem valores diferentes) e lacunas (nenhum requisito vale)"],
        "Numero de conflitos registrado na tabela.",
        "O relatorio aponta exatamente %d conflito(s)." % c,
        "Valor explicito na coluna Conflitos; soma 0+3+1 = 4.",
        aritmetica("(declare-const c Int)\n", "(assert (= c %d))(assert (= (+ 0 3 1) 4))\n" % c), "verify")
    D[-1]["valoresDoTexto"] = dict(conflitos=c)

det("C3-D28", "Modo direto concorda com a tabela",
    ["analyze --json exemplos/vm-decisoes.json --direct", "analyze --json exemplos/vm-decisoes.json"], PRE,
    ["| `Z3DirectAnalyzerTest` | 5 | O modo direto concorda com a tabela;", "| `--direct` | Pares pedidos direto ao Z3, sem montar a tabela (até 30 entradas) |"],
    "O modo direto da a mesma cobertura e o mesmo diagnostico da tabela-verdade.",
    "Para cada decisao de VM, o conjunto de condicoes com par e o conjunto de condicoes sem par coincidem entre --direct e o modo padrao.",
    "Afirmacao do teste; nao depende dos limites de entradas contestados (VM tem poucas entradas).",
    [], "z3")
det("C3-D29", "Formato json liga a decisao ao requisito de origem",
    ["analyze --json exemplos/vm-decisoes.json --format json"], PRE,
    ["| `json` | Resultado completo de cada decisão, ligado ao requisito de origem (formato de integração) |"],
    "A saida json e valida e referencia o requisito de origem de cada decisao.",
    "A saida e JSON valido e, para cada decisao do arquivo de entrada, contem seu identificador de requisito.",
    "Linha da tabela de saidas.", [], "saidas")
det("C3-D30", "-o grava o relatorio em arquivo",
    ["analyze \"A and B\" -o <arquivo>"], PRE,
    ["| `-o <arquivo>` | Grava o relatório no arquivo em vez de mostrar na tela |"],
    "Relatorio vai para o arquivo e nao para a tela.",
    "O arquivo e criado com o relatorio da analise e a saida padrao nao contem o relatorio (tabela/suite).",
    "Linha literal da tabela de opcoes.", [], "saidas")
det("C3-D31", "Arquivo .mcdc com comentarios e varios requisitos",
    ["analyze -f <arquivo com 2 requisitos e linhas # comentario>"], PRE,
    ["**Arquivo `.mcdc`:** um requisito por linha, `ID: expressão`. Linhas com `#` são comentários."],
    "Um requisito por linha; # = comentario.",
    "Dois requisitos (REQ-001, REQ-002) geram duas analises identificadas pelos IDs; as linhas de comentario sao ignoradas.",
    "Formato descrito literalmente.", [], "entrada")
det("C3-D32", "Expressoes invalidas sao recusadas",
    ["analyze \"A and\"", "analyze \"(A and B\"", "analyze \"A and and B\""], PRE,
    ["`ExpressionParserTest` | 9 | ... expressões inválidas recusadas", "`1`: entrada inválida"],
    "Expressao invalida e recusada.",
    "Nenhuma das tres entradas produz tabela-verdade nem suite; ha mensagem de erro. (O codigo de saida NAO e afirmado: ver I03.)",
    "Teste do parser declara recusa de expressoes invalidas.", [], "parser")
det("C3-D33", "Erro de sintaxe em .mcdc cita o requisito",
    ["analyze -f <arquivo com REQ-002: A and>"], PRE,
    ["| `RequirementsFileTest` | 3 | Arquivo `.mcdc`, comentários, linha sem identificador, erro de sintaxe com o requisito |"],
    "O erro de sintaxe vem acompanhado do requisito.",
    "A mensagem de erro menciona o identificador REQ-002 da linha com erro.",
    "Descricao do teste.", [], "entrada")
det("C3-D34", "check: suite completa demonstra todas as condicoes",
    ["check --json <decisao propria> --tests <csv completo>"], PRE,
    ["| Avaliar testes existentes | `mcdc check` | Cobertura MC/DC de um conjunto de testes, o que falta e testes com resultado esperado errado |",
     "| `TestSetEvaluationTest` | 6 | Avaliação de testes existentes: suíte completa, o que falta, resultado esperado errado, valores concretos |"],
    "Suite que contem um par por condicao: cobertura completa.",
    "Para a decisao A e B ou C com os testes TTF(T), FTF(F), TFF(F), TFT(T): as 3 condicoes demonstradas, nada faltando e nenhum resultado esperado errado.",
    "Suite de causa unica da decisao; Z3 confirma os pares.",
    [("par-A", pair_for(ABC, "(or (and A B) C)", "A"), "sat"), ("par-B", pair_for(ABC, "(or (and A B) C)", "B"), "sat"), ("par-C", pair_for(ABC, "(or (and A B) C)", "C"), "sat")], "check")
det("C3-D35", "check: resultado esperado errado e apontado",
    ["check --json <decisao propria> --tests <csv com um expected_outcome trocado>"], PRE,
    ["testes com resultado esperado errado", "`TestSetEvaluationTest` ... resultado esperado errado"],
    "Teste cujo expected_outcome difere do valor da guarda e sinalizado.",
    "O teste com resultado esperado trocado (TTF com expected F) e apontado como divergente; os demais nao.",
    "A guarda vale T em (T,T,F), logo F e errado.",
    [("guarda-em-TTF", "(set-logic QF_UF)\n(assert (not (or (and true true) false)))\n(check-sat)\n", "unsat")], "check")
det("C3-D36", "check: suite incompleta aponta o que falta",
    ["check --json <decisao propria> --tests <csv sem par para C>"], PRE,
    ["Cobertura MC/DC de um conjunto de testes, o que falta e testes com resultado esperado errado", "uma condição não demonstrada"],
    "Sem par para uma condicao, ela fica nao demonstrada.",
    "Com apenas TTF, FTF e TFF (sem linha que altere C): A e B demonstradas, C nao demonstrada e reportada como faltando.",
    "Nenhum par dentro das tres linhas varia apenas C com resultado diferente.",
    [("C-sem-par-nas-3-linhas", "(set-logic QF_UF)\n(define-fun f ((A Bool)(B Bool)(C Bool)) Bool (or (and A B) C))\n"
      + "(assert (or "
      + " ".join("(and (= %s %s) (= %s %s) (not (= %s %s)) (not (= (f %s) (f %s))))" % (
          b(r1[0]), b(r2[0]), b(r1[1]), b(r2[1]), b(r1[2]), b(r2[2]),
          " ".join(b(x) for x in r1), " ".join(b(x) for x in r2))
          for r1 in [(1, 1, 0), (0, 1, 0), (1, 0, 0)] for r2 in [(1, 1, 0), (0, 1, 0), (1, 0, 0)] if r1 < r2)
      + "))\n(check-sat)\n", "unsat")], "check")

VERIFY_DECL = "(declare-datatypes ((Modo 0)) (((idle) (busy) (off))))\n(declare-const mode Modo)\n(declare-const coin Bool)\n"
det("C3-D37", "verify: dois requisitos que valem juntos e escrevem valores diferentes = conflito",
    ["verify --json <json proprio: R1 guarda mode = idle, acao out := a; R2 guarda mode = idle e coin = true, acao out := b>"], PRE,
    ["Conflitos (dois requisitos valem juntos e escrevem valores diferentes)", "contradição só com valores diferentes na mesma variável"],
    "Guardas simultaneamente satisfazíveis + valores diferentes na mesma variável = conflito.",
    "O relatorio aponta 1 conflito entre R1 e R2.",
    "Em mode=idle e coin=true ambas valem.",
    [("guardas-simultaneas", "(set-logic ALL)\n" + VERIFY_DECL + "(assert (= mode idle))(assert (and (= mode idle) coin))\n(check-sat)\n(get-model)\n", "sat")], "verify")
det("C3-D38", "verify: mesmo valor nao e conflito",
    ["verify --json <json proprio: R1 mode = idle, out := a; R2 mode = idle e coin = true, out := a>"], PRE,
    ["| `Z3RequirementsVerifierTest` | 4 | Conflitos, guardas que não se sobrepõem, mesmo valor sem conflito, lacunas só com contexto |",
     "contradição só com valores diferentes na mesma variável"],
    "Valores iguais na mesma variavel nao contradizem.",
    "Nenhum conflito e apontado.",
    "Texto declara 'mesmo valor sem conflito'.",
    [("valores-iguais", "(set-logic QF_LIA)\n(declare-const a Int)(declare-const b Int)\n(assert (= a b))(assert (not (= a b)))\n(check-sat)\n", "unsat")], "verify")
det("C3-D39", "verify: guardas que nao se sobrepoem nao conflitam",
    ["verify --json <json proprio: R1 mode = idle, out := a; R2 mode = busy, out := b>"], PRE,
    ["guardas que não se sobrepõem"], "Guardas disjuntas nao valem juntas.",
    "Nenhum conflito e apontado.",
    "mode = idle e mode = busy nao podem valer juntas.",
    [("disjuntas", "(set-logic ALL)\n" + VERIFY_DECL + "(assert (= mode idle))(assert (= mode busy))\n(check-sat)\n", "unsat")], "verify")
det("C3-D40", "verify --context: lacuna quando nenhuma guarda vale",
    ["verify --json <json proprio: R1 mode = idle; R2 mode = busy> --context 'mode = off'"], PRE,
    ["| `--context \"<expr>\"` | No `verify`: confere se, nessa situação, sempre alguma guarda vale |"],
    "No contexto, se existe situacao em que nenhuma guarda vale, ha lacuna.",
    "Com contexto mode = off (modo off ∈ {idle, busy, off}), nenhuma guarda vale: 1 lacuna e reportada.",
    "Definicao de lacuna: nenhum requisito vale.",
    [("nenhuma-guarda-vale", "(set-logic ALL)\n" + VERIFY_DECL + "(assert (= mode off))(assert (not (= mode idle)))(assert (not (= mode busy)))\n(check-sat)\n(get-model)\n", "sat")], "verify")
det("C3-D41", "verify --context: sem lacuna quando uma guarda sempre vale",
    ["verify --json <json proprio: R1 mode = idle; R2 mode = busy> --context 'mode = idle'"], PRE,
    ["confere se, nessa situação, sempre alguma guarda vale"],
    "No contexto onde uma guarda vale sempre, nao ha lacuna.",
    "Nenhuma lacuna e reportada.",
    "No contexto mode = idle, R1 vale.",
    [("sempre-alguma-guarda", "(set-logic ALL)\n" + VERIFY_DECL + "(assert (= mode idle))(assert (not (= mode idle)))(assert (not (= mode busy)))\n(check-sat)\n", "unsat")], "verify")
det("C3-D42", "verify sem --context nao relata lacunas",
    ["verify --json <json proprio: R1 mode = idle; R2 mode = busy>"], PRE,
    ["lacunas só com contexto"], "Lacunas so surgem com contexto.",
    "O relatorio nao aponta lacunas.", "Texto do teste do verificador.", [], "verify")
chain = ["X%d" % i for i in range(1, 21)]
det("C3-D43", "20 entradas na tabela-verdade completa",
    ["analyze \"X1 and X2 and ... and X20\""], PRE,
    ["até 20 entradas com a tabela-verdade completa", "`PerformanceTest` | 4 | Motor sem o Z3: 20 entradas (cerca de 1 milhão de combinações) nas duas variantes ... cada caso abaixo de 5 s"],
    "20 entradas sao suportadas pela tabela completa em menos de 5 s.",
    "A analise de 20 entradas e concluida, com 20 condicoes, 1048576 combinacoes e todas as condicoes demonstradas. (Tempo nao e afirmado: a partida da JVM nao e separavel.)",
    "Limite documentado e teste de desempenho com 20 entradas; 2^20 = 1048576.",
    [("cada-condicao-tem-par", "(set-logic QF_UF)\n" + "".join("(declare-const X%d Bool)\n" % i for i in range(1, 21)) +
      "(define-fun f (%s) Bool (and %s))\n" % (" ".join("(%s Bool)" % v for v in chain), " ".join(chain)) +
      "(assert (or %s))\n" % " ".join("(= (f %s) (f %s))" % (" ".join(["true"] * 20), " ".join("false" if j == i else "true" for j in range(20))) for i in range(20)) +
      "(check-sat)\n", "unsat"),
     ("2-elevado-20", "(set-logic QF_LIA)\n(declare-const c Int)\n(assert (= c 1048576))(assert (= c (* 1024 1024)))\n(check-sat)\n", "sat")], "limites")
det("C3-D44", "21 entradas na tabela-verdade completa sao recusadas",
    ["analyze \"X1 and ... and X21\""], PRE,
    ["`TruthTableTest` | 8 | ... limite de 20 entradas", "**Tamanho:** 20 entradas com a tabela-verdade completa"],
    "Acima de 20 entradas nao ha tabela-verdade completa.",
    "Nenhuma suite e produzida para 21 entradas sem flags; ha mensagem de erro. (Codigo de saida nao afirmado: I03.)",
    "Limite documentado em dois pontos; sem flags nao ha modo alternativo.",
    aritmetica("(declare-const n Int)\n", "(assert (= n 21))(assert (> n 20))\n"), "limites")
det("C3-D45", "JSON NAT2TEST com guarda temporal (_antes)",
    ["analyze --json <json proprio com guarda 'the_mode_antes = idle /\\ the_coin = true'>"], PRE,
    ["Quando uma expressão se refere ao valor de uma variável no passo anterior, esse valor é identificado pelo sufixo `_antes`.", "`Nat2TestJsonReaderTest` | 4 | JSON da NAT2TEST, guarda temporal"],
    "O sufixo _antes e aceito em guardas.",
    "A analise e concluida: 1 decisao com 2 condicoes.", "Sintaxe documentada.", [], "entrada")
det("C3-D46", "Numero negativo em comparacao",
    ["analyze \"x > -3 and y < 2\""], PRE,
    ["`InputEdgeCasesTest` | 4 | Aspas no CSV, número da linha com erro, sinal de menos só em números", "booleanos, reais e negativos"],
    "Sinal de menos e aceito em numeros.",
    "A analise e concluida com 2 condicoes.", "Texto menciona numeros negativos e sinal de menos em numeros.", [], "parser")
det("C3-D47", "check e verify aceitam --format json",
    ["check --json <decisao propria> --tests <csv> --format json", "verify --json <json proprio> --format json"], PRE,
    ["`check` e `verify` aceitam `text` e `json`"], "Formato json disponivel nos tres comandos.",
    "Ambas as saidas sao JSON validos.", "Texto literal.", [], "saidas")
det("C3-D48", "Arquivo JSON invalido e recusado",
    ["analyze --json <arquivo com conteudo que nao e JSON>"], PRE,
    ["`Nat2TestJsonReaderTest` | 4 | JSON da NAT2TEST, guarda temporal, arquivos inválidos, ids repetidos"],
    "Arquivos invalidos sao recusados.",
    "Nenhuma analise e produzida; ha mensagem de erro.", "Teste declara tratamento de arquivos invalidos.", [], "entrada")

# ---------------------------------------------------------- indeterminados
ind("C3-I01", "Quantas condicoes tem (A and B) or (not A and C)? 4 ou 3",
    "analyze \"(A and B) or (not A and C)\"",
    ["há 3 entradas distintas (`A`, `B` e `C`) e 4 ocorrências de condição (`A#1`, `B`, `A#2` e `C`)", "Regra complementar: a ferramenta considera cada variável distinta como uma única condição ... Portanto, a expressão do exemplo possui exatamente 3 condições e 3 entradas.", "entrada repetida: cada aparição é uma condição com par próprio (A#1, A#2)"],
    "O texto afirma 4 condicoes (L55, L238, `ConditionTest`) e 3 condicoes (L57); o proprio texto nao resolve.",
    conflito("(declare-const n Int)\n", "(= n 4)", "(= n 3)"))
ind("C3-I02", "Comportamento sem Z3 instalado",
    "analyze \"(A and B) or C\" sem z3 no PATH",
    ["Sem o Z3, continuam disponíveis os recursos que não dependem dele.", "Sem o Z3, nenhum comando pode ser iniciado.", "a instalação do Z3 é opcional"],
    "Obrigatorio para qualquer execucao x opcional (so recursos avancados). Por isso as execucoes do baseline mantem o Z3 no PATH.",
    conflito("(declare-const iniciavel Bool)\n", "iniciavel", "(not iniciavel)"))
ind("C3-I03", "Codigos de saida",
    "analyze/check/verify: codigos 0, 1, 2",
    ["**Código de saída:** `0`: comando concluído sem apontar os problemas ... `1`: entrada inválida; `2`: resultado válido ... com uma condição sem par", "o código 0 indica entrada inválida; o código 1 indica execução concluída sem problemas; o código 2 significa exclusivamente falha de instalação do Z3"],
    "Dois mapeamentos incompativeis para o codigo 0 (sucesso x invalido). Nenhum teste afirma codigo de saida.",
    conflito("(declare-const cod0Significa Int)\n", "(= cod0Significa 0)", "(= cod0Significa 1)"))
ind("C3-I04", "Z3 linha a linha: acima de 12 entradas muda ao modo direto?",
    "analyze <decisao com 13 entradas> --z3",
    ["acima de 12 entradas, passa sozinho ao modo direto", "A partir da 13ª entrada, a ferramenta continua obrigatoriamente na tabela-verdade completa e não pode mudar de modo."],
    "Muda para o modo direto x nao muda de modo.",
    conflito("(declare-const modoDireto Bool)\n", "modoDireto", "(not modoDireto)"))
ind("C3-I05", "Limite do modo direto: 30 ou 12 entradas; exige tabela?",
    "analyze <decisao com 26 entradas> --direct",
    ["| `--direct` | Pares pedidos direto ao Z3, sem montar a tabela (até 30 entradas) |", "O modo direto, por sua vez, só funciona até 12 entradas e exige que a tabela-verdade já tenha sido construída.", "o modo direto com 26 entradas abaixo de 10 s"],
    "Limite 30 x limite 12.",
    conflito("(declare-const limiteDireto Int)\n", "(= limiteDireto 30)", "(= limiteDireto 12)"))
ind("C3-I06", "Colunas decision e expected_outcome do CSV: obrigatorias ou opcionais",
    "check ... --tests <csv sem as colunas>",
    ["As colunas `decision` e `expected_outcome` são opcionais.", "Sem essas duas colunas, a ferramenta não interpreta os testes. Ao mesmo tempo, a ausência delas é aceita e substituída automaticamente por valores inferidos."],
    "Opcionais x obrigatorias; o proprio paragrafo se autocontradiz. Todos os CSVs do baseline trazem as duas colunas.",
    conflito("(declare-const colunasObrigatorias Bool)\n", "colunasObrigatorias", "(not colunasObrigatorias)"))
ind("C3-I07", "Conteudo dos formatos csv e truth-csv",
    "analyze ... --format csv / --format truth-csv",
    ["| `csv` | A suíte: uma linha por teste e entrada ...", "| `truth-csv` | A tabela-verdade inteira, com as combinações impossíveis marcadas |", "`truth-csv` contém somente os pares de independência, nunca a tabela-verdade. A tabela-verdade completa é exportada exclusivamente em `csv`, que não contém os testes gerados."],
    "Atribuicoes trocadas entre csv e truth-csv; conteudo dos dois nao tem expectativa unica.",
    conflito("(declare-const csvTemSuite Bool)\n", "csvTemSuite", "(not csvTemSuite)"))
ind("C3-I08", "Mapeamento sat/unsat do Z3 para combinacao possivel/impossivel",
    "analyze 'speed > 100 or (speed > 50 and rain)' --z3 (quais linhas sao descartadas)",
    ["as que retornam `unsat` são consideradas impossíveis e não participam da análise", "Regra de satisfatibilidade: resultados `unsat` representam combinações possíveis e devem ser mantidos. Resultados `sat` representam combinações impossíveis e devem ser descartados."],
    "unsat=impossivel x unsat=possivel. Linhas descartadas pelo Z3 em exemplos nao anotados nao tem expectativa unica.",
    conflito("(declare-const unsatImpossivel Bool)\n", "unsatImpossivel", "(not unsatImpossivel)"))
ind("C3-I09", "Pares quando o resultado da decisao nao muda",
    "analyze \"A and (B or not B)\"  (condicao B sem efeito)",
    ["são procurados dois testes possíveis nos quais essa condição muda, o resultado da decisão também muda", "para demonstrar MC/DC, basta que a condição mude entre dois testes; o resultado da decisão pode permanecer igual."],
    "Exige mudanca do resultado x nao exige. Define se B tem par; sem expectativa unica.",
    conflito("(declare-const resultadoPrecisaMudar Bool)\n", "resultadoPrecisaMudar", "(not resultadoPrecisaMudar)"))
ind("C3-I10", "Minimalidade da suite gulosa e da busca exata",
    "analyze \"((E or D) and (not A or D)) or B\" --exact; e sem --exact",
    ["aqui, 5 testes em vez dos 6 da escolha gulosa", "a estratégia gulosa sempre encontra a suíte globalmente mínima. A opção `--exact` executa a mesma heurística aproximada e pode retornar uma suíte maior"],
    "Exata 5 < gulosa 6 x gulosa sempre minima e exata sem garantia.",
    conflito("(declare-const gulosa Int)(declare-const exata Int)\n", "(and (= gulosa 6) (= exata 5))", "(<= gulosa exata)"))
ind("C3-I11", "Rotulo redundante x bloqueada",
    "analyze -f exemplos/requisitos.mcdc (REQ-003) e decisoes com --constraint",
    ["se uma condição não possui par mesmo considerando todas as combinações, é classificada como redundante; se deixa de possuir pares por causa das combinações impossíveis, é classificada como bloqueada", "uma condição sem par em qualquer cenário é bloqueada; uma condição que perde seus pares apenas por combinações impossíveis é redundante."],
    "Rotulos trocados.",
    conflito("(declare-const semParEmTodoCenarioERedundante Bool)\n", "semParEmTodoCenarioERedundante", "(not semParEmTodoCenarioERedundante)"))
ind("C3-I12", "Arquitetura do Z3: processo externo x biblioteca nativa; PATH; 60 s",
    "qualquer analise com --z3",
    ["O Z3 é executado como um processo externo. ... Cada chamada ao processo tem limite de 60 segundos.", "o programa utiliza sempre a implementação interna do Java.", "o Z3 é carregado como biblioteca nativa dentro da JVM e não é iniciado como processo externo. As chamadas não possuem limite de tempo"],
    "Tres descricoes incompativeis.",
    conflito("(declare-const processoExterno Bool)\n", "processoExterno", "(not processoExterno)"))
ind("C3-I13", "Cobertura de linhas e de desvios: mesma metrica? total = media simples?",
    "build Maven (nao e comportamento da CLI)",
    ["cobertura de linhas e cobertura de desvios são a mesma métrica", "A linha Total apresenta a cobertura agregada ... não corresponde necessariamente à média aritmética", "Linhas cobertas 95,5% ... Desvios cobertos 90,3%"],
    "Metricas distintas (95,5 x 90,3) x mesma metrica; media simples x agregada. Fora do escopo da CLI.",
    conflito("(declare-const linhas Real)(declare-const desvios Real)\n", "(and (= linhas 95.5) (= desvios 90.3))", "(= linhas desvios)"))
ind("C3-I14", "Interpretacao da mutacao PIT",
    "build Maven -Pqualidade (nao e CLI)",
    ["o PIT introduz alterações artificiais no código da ferramenta", "o PIT altera os requisitos de entrada, não o código da ferramenta."],
    "Objeto da mutacao PIT contraditorio; fora da CLI.",
    conflito("(declare-const pitAlteraCodigo Bool)\n", "pitAlteraCodigo", "(not pitAlteraCodigo)"))
ind("C3-I15", "Aprovacao do build: por modulo ou agregada",
    "mvn clean verify (nao e CLI)",
    ["A cobertura é conferida pelo JaCoCo separadamente em cada módulo", "o JaCoCo agrega todos os módulos antes de verificar os limites. Um módulo abaixo da nota mínima nunca interrompe o build"],
    "Verificacao por modulo x agregada; fora da CLI.",
    conflito("(declare-const porModulo Bool)\n", "porModulo", "(not porModulo)"))
ind("C3-I16", "Garantia do MC/DC para parenteses deslocados (ASF)",
    "analyze \"A and (B or C)\" --mutation: mutante ASF",
    ["**Parênteses deslocados:** é o único tipo de defeito sem garantia do MC/DC", "o MC/DC garante a detecção de qualquer alteração de parênteses ... nenhum defeito de agrupamento pode escapar da suíte."],
    "Sem garantia x com garantia total. Sobrevivencia do mutante ASF nao tem expectativa unica (nota: no exemplo do texto, 1 de 727 escapou).",
    conflito("(declare-const asfGarantido Bool)\n", "asfGarantido", "(not asfGarantido)"))
ind("C3-I17", "--constraint com -f ou --json",
    "analyze -f exemplos/requisitos.mcdc --constraint \"...\"",
    ["| `--constraint \"<expr>\"` | Restrição entre condições escrita à mão (só com expressão direta) |"],
    "O texto restringe o uso mas nao diz o que acontece (recusa, ignora, aplica).",
    [("sem-formalizacao-conflitante", "(set-logic QF_UF)\n(declare-const definido Bool)\n(assert (not definido))\n(check-sat)\n", "sat")])
ind("C3-I18", "Linha sem identificador e ids repetidos em .mcdc/JSON",
    "analyze -f <arquivo com linha sem 'ID:'> ; analyze --json <ids repetidos>",
    ["| `RequirementsFileTest` | 3 | Arquivo `.mcdc`, comentários, linha sem identificador, erro de sintaxe com o requisito |", "arquivos inválidos, ids repetidos"],
    "O texto cita os cenarios mas nao diz se sao aceitos, recusados ou numerados automaticamente.",
    [("sem-formalizacao-conflitante", "(set-logic QF_UF)\n(declare-const definido Bool)\n(assert (not definido))\n(check-sat)\n", "sat")])
ind("C3-I19", "Resultado de verify com --context 'the_system_mode = preparing_weak' (VM)",
    "verify --json exemplos/vm-decisoes.json --context 'the_system_mode = preparing_weak'",
    ["./mcdc verify --json exemplos/vm-decisoes.json --context 'the_system_mode = preparing_weak'"],
    "O texto mostra o comando mas nao afirma se ha lacuna.",
    [("sem-formalizacao-conflitante", "(set-logic QF_UF)\n(declare-const definido Bool)\n(assert (not definido))\n(check-sat)\n", "sat")])
ind("C3-I20", "Paridade de 3 entradas exige 8 testes",
    "analyze <expressao de paridade de 3 entradas>",
    ["a função de paridade de 3 entradas exige 8 testes"],
    "O texto nao fornece a expressao; a contagem por ocorrencia (I01) tambem afeta o resultado.",
    [("sem-formalizacao-conflitante", "(set-logic QF_UF)\n(declare-const definido Bool)\n(assert (not definido))\n(check-sat)\n", "sat")])
ind("C3-I21", "check --json exemplos/decisoes.json --tests exemplos/testes.csv",
    "check --json exemplos/decisoes.json --tests exemplos/testes.csv",
    ["./mcdc check --json exemplos/decisoes.json --tests exemplos/testes.csv"],
    "O texto nao informa o resultado esperado desses arquivos.",
    [("sem-formalizacao-conflitante", "(set-logic QF_UF)\n(declare-const definido Bool)\n(assert (not definido))\n(check-sat)\n", "sat")])
ind("C3-I22", "Sinal de menos antes de variavel (-A and B)",
    "analyze \"-A and B\"",
    ["sinal de menos só em números"],
    "Nao e dito se o uso fora de numeros e recusado ou como e tratado.",
    [("sem-formalizacao-conflitante", "(set-logic QF_UF)\n(declare-const definido Bool)\n(assert (not definido))\n(check-sat)\n", "sat")])
ind("C3-I23", "Tamanho da suite de causa unica de (A and B) or C",
    "analyze \"(A and B) or C\" --unique-cause",
    ["Para as guardas simples consideradas pela ferramenta, a suíte pode ter **N + 1** testes"],
    "'pode ter N+1' nao fixa o tamanho para a variante causa unica; tambem sob conflito I09/I10.",
    [("sem-formalizacao-conflitante", "(set-logic QF_UF)\n(declare-const definido Bool)\n(assert (not definido))\n(check-sat)\n", "sat")])
ind("C3-I24", "Tempo/estimativa de desempenho e demais metricas do build",
    "mvn / testes JUnit (nao e CLI)",
    ["171 testes", "Os limites definidos para os testes de desempenho são aproximadamente 10 vezes maiores que os tempos medidos"],
    "Descreve a suite de desenvolvimento e o build, nao comportamento observavel da CLI.",
    [("sem-formalizacao-conflitante", "(set-logic QF_UF)\n(declare-const definido Bool)\n(assert (not definido))\n(check-sat)\n", "sat")])


DEMOTE = {
    "C3-D11": "A regra 'Variacoes no limite de cada comparacao' so e exemplificada para speed > 100 (100 e 101); os valores de fronteira de speed > 50 nao sao dados e exigiriam extrapolacao.",
    "C3-D15": "'REQ-003 tem uma condicao redundante' (L253) depende do rotulo redundante x bloqueada (I11), do criterio de par (I09) e de 'uma' ser exatamente uma; sem expectativa unica.",
    "C3-D28": "O modo direto e descrito como 'sem montar a tabela' (L119) e como exigindo a tabela ja construida e limite de 12 entradas (L115); o funcionamento do modo e contraditorio (I04/I05).",
    "C3-D32": "O texto diz 'expressoes invalidas recusadas' sem definir a gramatica nem qual expressao e invalida; recusa e forma da recusa nao tem expectativa unica (codigo de saida: I03).",
    "C3-D33": "O texto cita 'erro de sintaxe com o requisito' sem definir o que e erro de sintaxe nem o formato da mensagem.",
    "C3-D42": "'lacunas so com contexto' e a descricao de um teste de unidade, sem dizer o que o relatorio mostra sem --context.",
    "C3-D44": "O texto da o limite de 20 entradas mas nao diz o que ocorre ao exceder (recusa, erro, outro modo).",
    "C3-D48": "'arquivos invalidos' nao e definido (o que torna um JSON invalido, qual e o resultado).",
}


def main():
    global D, I
    novos = []
    for c in list(D):
        if c["id"] in DEMOTE:
            D.remove(c)
            novos.append(c)
    for k, c in enumerate(novos):
        c2 = dict(id="C3-I%02d" % (25 + k), status="INDETERMINADO", titulo=c["titulo"], entrada=c["entrada"],
                  trechoLiteral=c["trechoLiteral"], motivoIndeterminacao=DEMOTE[c["id"]],
                  expectativa="INDETERMINADO: sem expectativa unica; caso registrado, NAO executado",
                  _smt=c["_smt"])
        I.append(c2)
    for k, c in enumerate(D):
        c["id"] = "C3-D%02d" % (k + 1)
    todos = D + I
    for c in todos:
        for nome, smt, esp in c["_smt"]:
            with open(os.path.join(Z3DIR, "%s__%s.smt2" % (c["id"], nome)), "w", encoding="utf-8", newline="\n") as fh:
                fh.write("; Caso %s - %s\n; Resposta esperada da formula: %s\n" % (c["id"], nome, esp))
                fh.write(smt)
        c["z3Consultas"] = [dict(arquivo="z3/%s__%s.smt2" % (c["id"], n), esperado=e) for n, _, e in c["_smt"]]
        del c["_smt"]
        c.pop("z3", None)
    saida = dict(
        condicao="C3",
        fonte="experimentacao-pesquisa/experimentacao-3/documentation/tool-readme-C3.md",
        sha256="F18B0821D79C7315486C13D5260FA2F6D6E9418EF03B86CDE58E66B91B7B87A3",
        unidade="um caso do oraculo = um teste",
        resumo=dict(determinados=len(D), indeterminados=len(I)),
        casos=todos)
    with open(os.path.join(AQUI, "oraculo.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(saida, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(len(D), "determinados;", len(I), "indeterminados")


if __name__ == "__main__":
    main()
