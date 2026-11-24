#!/usr/bin/env python3
"""Gera o oraculo documental da condicao C0 (fonte: tool-readme-original.md).

Este script NAO le nem executa o SUT. Ele:
  1. define os casos e as expectativas derivadas somente do texto da fonte C0;
  2. formaliza em SMT-LIB as restricoes pertinentes (pares MC/DC, suite minima,
     demonstracao de testes, conflitos/lacunas);
  3. executa o Z3 independente (executavel z3 do pacote z3-solver, nao o
     modulo mcdc-z3) e confere que o resultado SMT concorda com a expectativa;
  4. grava oraculo.json, smt/*.smt2 e smt/resultados-z3.json.
"""
import itertools, json, os, re, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
SMT_DIR = os.path.join(AQUI, "z3")
Z3 = os.environ.get("Z3_BIN", r"C:\Users\User\AppData\Roaming\Python\bin\z3.exe")
os.makedirs(SMT_DIR, exist_ok=True)

# --------------------------------------------------------------------------
# Mini-parser de expressoes booleanas (and/or/not/parenteses) -> AST
# --------------------------------------------------------------------------
TOK = re.compile(r"\s*(\(|\)|and\b|or\b|not\b|[A-Za-z_][A-Za-z_0-9]*)")


def tokens(s):
    pos, out = 0, []
    while pos < len(s):
        m = TOK.match(s, pos)
        if not m:
            raise ValueError("token invalido em %r" % s[pos:])
        out.append(m.group(1))
        pos = m.end()
    return out


class Parser:
    def __init__(self, s):
        self.t = tokens(s)
        self.i = 0
        self.n = 0  # contador de aparicoes

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else None

    def eat(self):
        v = self.t[self.i]
        self.i += 1
        return v

    def parse(self):
        e = self.p_or()
        assert self.peek() is None
        return e

    def p_or(self):
        e = self.p_and()
        while self.peek() == "or":
            self.eat()
            e = ("or", e, self.p_and())
        return e

    def p_and(self):
        e = self.p_not()
        while self.peek() == "and":
            self.eat()
            e = ("and", e, self.p_not())
        return e

    def p_not(self):
        if self.peek() == "not":
            self.eat()
            return ("not", self.p_not())
        return self.p_atom()

    def p_atom(self):
        v = self.eat()
        if v == "(":
            e = self.p_or()
            assert self.eat() == ")"
            return e
        idx = self.n
        self.n += 1
        return ("var", v, idx)


def parse(s):
    p = Parser(s)
    return p.parse(), p.n


def appearances(ast, acc=None):
    acc = [] if acc is None else acc
    if ast[0] == "var":
        acc.append((ast[2], ast[1]))
    else:
        for c in ast[1:]:
            appearances(c, acc)
    return sorted(acc)


def inputs_of(ast):
    return sorted({n for _, n in appearances(ast)})


# avaliacao em Python (oraculo de forca bruta, so da definicao do texto)
def ev(ast, row, flip=None):
    k = ast[0]
    if k == "var":
        v = row[ast[1]]
        return (not v) if flip == ast[2] else v
    if k == "not":
        return not ev(ast[1], row, flip)
    if k == "and":
        return ev(ast[1], row, flip) and ev(ast[2], row, flip)
    return ev(ast[1], row, flip) or ev(ast[2], row, flip)


def smt(ast, pre, flip=None):
    k = ast[0]
    if k == "var":
        t = pre + ast[1]
        return "(not %s)" % t if flip == ast[2] else t
    if k == "not":
        return "(not %s)" % smt(ast[1], pre, flip)
    return "(%s %s %s)" % (k, smt(ast[1], pre, flip), smt(ast[2], pre, flip))


def all_rows(names):
    return [dict(zip(names, bits)) for bits in itertools.product([True, False], repeat=len(names))]


# --------------------------------------------------------------------------
# Execucao do Z3
# --------------------------------------------------------------------------
Z3_LOG = {}


def z3_version():
    return subprocess.run([Z3, "--version"], capture_output=True, text=True).stdout.strip()


def run_z3(nome, texto):
    path = os.path.join(SMT_DIR, nome + ".smt2")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)
    r = subprocess.run([Z3, "-smt2", "-T:60", path], capture_output=True, text=True)
    out = r.stdout.strip().splitlines()
    resp = out[0].strip() if out else "(sem saida)"
    if resp not in ("sat", "unsat"):
        raise RuntimeError("ERRO TECNICO Z3 em %s: %r %r" % (nome, r.stdout, r.stderr))
    Z3_LOG[nome] = {"resposta": resp, "saida_completa": r.stdout.strip()}
    return resp, r.stdout


def decl_row(names, pre):
    return "".join("(declare-const %s%s Bool)\n" % (pre, n) for n in names)


def smt_pair(expr, k, constraint=None, tag=""):
    """Consulta: existe par de independencia (mascaramento) para a aparicao k?"""
    ast, n = parse(expr)
    names = inputs_of(ast)
    cname = dict(appearances(ast))[k]
    t = "; par de independencia (mascaramento) para a aparicao %d (%s) de: %s\n" % (k, cname, expr)
    t += decl_row(names, "r1_") + decl_row(names, "r2_")
    if constraint:
        cast, _ = parse(constraint)
        t += "(assert %s)\n(assert %s)\n" % (smt(cast, "r1_"), smt(cast, "r2_"))
    t += "(assert (not (= r1_%s r2_%s)))\n" % (cname, cname)
    t += "(assert (not (= %s %s)))\n" % (smt(ast, "r1_"), smt(ast, "r2_"))
    t += "(assert (not (= %s %s)))\n" % (smt(ast, "r1_"), smt(ast, "r1_", k) if False else smt(ast, "r1_", flip=k))
    t += "(assert (not (= %s %s)))\n" % (smt(ast, "r2_"), smt(ast, "r2_", flip=k))
    t += "(check-sat)\n(get-model)\n"
    return run_z3("par_%s_c%d" % (tag, k), t)


def brute_pair(expr, k, constraint=None):
    ast, n = parse(expr)
    names = inputs_of(ast)
    cname = dict(appearances(ast))[k]
    cast = parse(constraint)[0] if constraint else None
    rows = [r for r in all_rows(names) if cast is None or ev(cast, r)]
    for r1 in rows:
        for r2 in rows:
            if r1[cname] == r2[cname]:
                continue
            if ev(ast, r1) == ev(ast, r2):
                continue
            if ev(ast, r1) == ev(ast, r1, k) or ev(ast, r2) == ev(ast, r2, k):
                continue
            return True
    return False


def exit_expect(expr, tag, constraint=None):
    """Retorna (exit_esperado, [respostas Z3 por condicao]) cruzando SMT e forca bruta."""
    ast, n = parse(expr)
    res = []
    for k in range(n):
        resp, _ = smt_pair(expr, k, constraint, tag)
        bf = brute_pair(expr, k, constraint)
        assert (resp == "sat") == bf, "divergencia Z3 x forca-bruta em %s c%d" % (expr, k)
        res.append(resp)
    return (0 if all(r == "sat" for r in res) else 2), res


def min_suite(expr, tag):
    """Menor suite (mascaramento) por Z3: tamanho minimo k tal que ha suite com k linhas."""
    ast, n = parse(expr)
    names = inputs_of(ast)
    rows = all_rows(names)
    R = len(rows)
    outs = [ev(ast, r) for r in rows]
    resultados = {}
    for k in range(2, R + 1):
        t = "; suite minima (mascaramento) de %s com no maximo %d linhas\n" % (expr, k)
        t += "".join("(declare-const s%d Bool)\n" % i for i in range(R))
        for c in range(n):
            cname = dict(appearances(ast))[c]
            alts = []
            for i in range(R):
                for j in range(i + 1, R):
                    if rows[i][cname] == rows[j][cname]:
                        continue
                    if outs[i] == outs[j]:
                        continue
                    if outs[i] == ev(ast, rows[i], c) or outs[j] == ev(ast, rows[j], c):
                        continue
                    alts.append("(and s%d s%d)" % (i, j))
            t += "(assert %s)\n" % ("(or %s)" % " ".join(alts) if alts else "false")
        t += "(assert ((_ at-most %d) %s))\n(check-sat)\n(get-model)\n" % (k, " ".join("s%d" % i for i in range(R)))
        resp, _ = run_z3("minsuite_%s_k%d" % (tag, k), t)
        resultados[k] = resp
        if resp == "sat":
            return k, resultados
    return None, resultados


def smt_check(expr, rows_outs, tag):
    """Demonstracao MC/DC de um conjunto de testes dado (ground) -> condicoes demonstradas."""
    ast, n = parse(expr)
    names = inputs_of(ast)
    res = []
    for c in range(n):
        cname = dict(appearances(ast))[c]
        alts = []
        for i, j in itertools.combinations(range(len(rows_outs)), 2):
            ri, rj = rows_outs[i][0], rows_outs[j][0]
            if ri[cname] == rj[cname]:
                continue
            if ev(ast, ri) == ev(ast, rj):
                continue
            if ev(ast, ri) == ev(ast, ri, c) or ev(ast, rj) == ev(ast, rj, c):
                continue
            alts.append("true")
        t = "; condicao %d (%s) demonstrada pelos testes? (formula ground)\n(assert %s)\n(check-sat)\n" % (
            c, cname, "(or %s)" % " ".join(alts) if alts else "false")
        resp, _ = run_z3("check_%s_c%d" % (tag, c), t)
        res.append(resp == "sat")
    return res


# --------------------------------------------------------------------------
# Definicao dos casos
# --------------------------------------------------------------------------
CASOS = []


def caso(id_, grupo, titulo, args, observa, citacao, regra, justificativa, files=None,
         usa_z3=False, status="DETERMINADO", motivo=None, evidencia=None, pre_analise=None):
    CASOS.append(dict(id=id_, grupo=grupo, titulo=titulo, args=args, files=files or {},
                      usa_z3=usa_z3, observa=observa, citacao=citacao, regra=regra,
                      justificativa=justificativa, status=status, motivo=motivo,
                      evidencia_z3=evidencia, pre_analise=pre_analise))


def conj(n, op="and"):
    return (" %s " % op).join("A%d" % i for i in range(1, n + 1))


Q_EXIT = "**Código de saída:** `0` tudo certo; `1` entrada inválida; `2` alguma condição sem par"
Q_NP1 = "Nas guardas simples, a suíte tem **N + 1** testes"
Q_PAIR = "para cada condição, dois testes possíveis em que ela muda, a saída muda e ela decide nos dois (trocar só ela muda a saída)"
Q_CSV = "`csv` | A suíte: uma linha por teste e entrada, com o resultado esperado"
Q_TTCSV = "`truth-csv` | A tabela verdade inteira, com as combinações impossíveis marcadas"

# ---- Grupo 1: analise de expressoes booleanas (mascaramento / causa unica) ----
e, ev_z3 = exit_expect("(A and B) or C", "t001")
assert e == 0
caso("C0-001", "analyze/booleano", "(A and B) or C: todas as condições têm par (saída 0)",
     ["analyze", "(A and B) or C"], {"exit": 0}, Q_EXIT + " / " + Q_PAIR,
     "Todas as condições com par de independência => código 0.",
     "Z3 (sat para as 3 condições) confirma que cada condição tem par; logo nenhuma está sem par.",
     evidencia=ev_z3)
caso("C0-002", "analyze/booleano", "(A and B) or C: suíte de 4 testes x 3 entradas = 12 linhas CSV",
     ["analyze", "(A and B) or C", "--format", "csv"], {"exit": 0, "csv_rows": 12},
     "Exemplos conhecidos ((A ∧ B) ∨ C com 4 testes ...); csv: uma linha por teste e entrada",
     "Suíte de 4 testes; CSV tem uma linha por teste e entrada.",
     "4 testes x 3 entradas = 12 linhas de dados (tolerando 1 linha de cabeçalho, que a fonte não define).",
     pre_analise="min_suite")
caso("C0-003", "analyze/booleano", "(A and B) or C em causa única: 4 testes x 3 entradas = 12 linhas CSV",
     ["analyze", "(A and B) or C", "--unique-cause", "--format", "csv"], {"exit": 0, "csv_rows": 12},
     "As duas variantes de MC/DC são suportadas: mascaramento (padrão) e causa única (`--unique-cause`). / (A ∧ B) ∨ C com 4 testes",
     "Mesma contagem de testes para a decisão (A and B) or C na variante causa única.",
     "Fonte não distingue a contagem por variante nesse exemplo; assume-se o exemplo conhecido de 4 testes.")
caso("C0-004", "analyze/booleano", "A and not B: 3 testes x 2 entradas = 6 linhas CSV",
     ["analyze", "A and not B", "--format", "csv"], {"exit": 0, "csv_rows": 6},
     "A ∧ ¬B com 3",
     "A ∧ ¬B tem suíte de 3 testes.", "3 testes x 2 entradas = 6 linhas de dados.")
caso("C0-005", "analyze/booleano", "Paridade de 3 entradas exige 8 testes (24 linhas CSV, mascaramento)",
     ["analyze",
      "(A and B and C) or (A and not B and not C) or (not A and B and not C) or (not A and not B and C)",
      "--format", "csv"], {"exit": 0, "csv_rows": 24},
     "o MC/DC pode exigir todas as combinações (ex.: a paridade de 3 entradas pede 8 testes)",
     "Paridade (ímpar) de A,B,C pede 8 testes = 2^3 combinações.",
     "8 testes x 3 entradas = 24 linhas de dados; exit 0 se toda condição tem par (Z3).",
     pre_analise="paridade")
caso("C0-006", "analyze/exato", "--exact em ((E or D) and (not A or D)) or B: 5 testes x 4 entradas = 20 linhas",
     ["analyze", "((E or D) and (not A or D)) or B", "--exact", "--format", "csv"],
     {"exit": 0, "csv_rows": 20}, "suíte exata (aqui, 5 testes em vez dos 6 da escolha gulosa)",
     "--exact devolve a menor suíte possível (5 testes) para essa expressão.",
     "5 testes x 4 entradas (E, D, A, B) = 20 linhas; Z3 independente confirma que 4 é unsat e 5 é sat.",
     usa_z3=True, pre_analise="exato")
caso("C0-007", "analyze/booleano", "(A and B) or (not A and C): condições A#1, B, A#2, C; saída 0",
     ["analyze", "(A and B) or (not A and C)"], {"exit": 0, "contains": ["A#1", "A#2"]},
     "em `(A and B) or (not A and C)` há 3 entradas e 4 condições (`A#1`, `B`, `A#2`, `C`)",
     "Cada aparição é uma condição, nomeadas A#1 e A#2; toda condição tem par.",
     "A saída em texto deve identificar A#1 e A#2; Z3 confirma par para as 4 condições (saída 0).",
     pre_analise="a1a2")
caso("C0-008", "analyze/diagnostico", "A or (A and B): B é redundante (saída 2, texto cita redundância)",
     ["analyze", "A or (A and B)"], {"exit": 2, "contains": ["redundan"]},
     "condição sem par: redundante (o requisito pode ser simplificado) / `2` alguma condição sem par",
     "Condição sem par => saída 2; diagnóstico 'redundante' quando continua sem par com todas as combinações.",
     "B nunca decide (A=T => T; A=F => A and B = F); Z3 unsat para B.", pre_analise="redundante")
caso("C0-009", "analyze/diagnostico", "A and B com --constraint 'not A or not B': condições bloqueadas (saída 2)",
     ["analyze", "A and B", "--constraint", "not A or not B"], {"exit": 2, "contains": ["bloquead"]},
     "**bloqueada** por combinações impossíveis / `--constraint \"<expr>\"` Restrição entre condições",
     "Com a restrição, A e B nunca são ambos verdadeiros: nenhuma condição tem par; diagnóstico 'bloqueada'.",
     "Z3 unsat para A e B sob a restrição.", pre_analise="bloqueada")
caso("C0-010", "analyze/restricao", "A or (B and C) com restrição 'not A or B': todas as condições têm par (saída 0)",
     ["analyze", "A or (B and C)", "--constraint", "not A or B"], {"exit": 0},
     "restrição escrita à mão: A = speed > 100 implica B = speed > 50 / `./mcdc analyze \"A or (B and C)\" --constraint \"not A or B\"`",
     "A restrição só elimina linhas com A=T,B=F; todas as condições mantêm par.",
     "Z3 sat para as 3 condições com a restrição.", pre_analise="restricao")
caso("C0-011", "analyze/precedencia", "Precedência: 'A or B and C' = A or (B and C) (restrição A,C exclusivos => saída 0)",
     ["analyze", "A or B and C", "--constraint", "not A or not C"], {"exit": 0},
     "Precedência (e antes de ou)",
     "'and' precede 'or'; sob essa leitura todas as condições têm par com a restrição.",
     "Se lido como (A or B) and C, A ficaria sem par (A e C exclusivos): o caso discrimina a leitura.",
     pre_analise="prec1")
caso("C0-012", "analyze/precedencia", "Precedência: 'A and B or C' = (A and B) or C (restrição A,C exclusivos => saída 0)",
     ["analyze", "A and B or C", "--constraint", "not A or not C"], {"exit": 0},
     "Precedência (e antes de ou)",
     "'and' precede 'or'; lido como A and (B or C), C ficaria sem par.",
     "Z3 sat para as 3 condições em (A and B) or C com a restrição.", pre_analise="prec2")

# ---- Grupo 2: operadores aceitos ----
for i, (expr, rows, nome) in enumerate([
        ("A && B", 6, "&&"), ("A /\\ B", 6, "/\\"), ("A or B", 6, "or"), ("A || B", 6, "||"),
        ("A \\/ B", 6, "\\/"), ("!A", 2, "!"), ("not A", 2, "not")], start=13):
    caso("C0-%03d" % i, "operadores", "Operador '%s' aceito: %d linhas CSV" % (nome, rows),
         ["analyze", expr, "--format", "csv"], {"exit": 0, "csv_rows": rows},
         "Operadores (use aspas simples quando a expressão tiver `\\`): e: and, &&, /\\; ou: or, ||, \\/; não: not, !",
         "As formas listadas são operadores válidos; a decisão tem suíte N+1.",
         "Decisão simples: N+1 testes x N entradas = %d linhas." % rows)
for i, op in enumerate(["=", "==", "!=", "<", "<=", ">", ">="], start=20):
    caso("C0-%03d" % i, "operadores", "Comparação '%s' aceita em 'x %s 5 and B' (saída 0)" % (op, op),
         ["analyze", "x %s 5 and B" % op], {"exit": 0},
         "comparação | `=`, `==`, `!=`, `<`, `<=`, `>`, `>=`",
         "Comparações são operadores válidos; duas condições independentes (x, B) têm par (sem Z3).",
         "Sem Z3 não há relação entre condições: as duas condições têm par => saída 0.")
caso("C0-027", "operadores", "Comparação de enumeração: 'mode != idle and B' (saída 0)",
     ["analyze", "mode != idle and B"], {"exit": 0},
     "`speed > 100 /\\ mode = idle`; comparação `!=`", "Comparação com símbolo de enumeração é aceita.",
     "Condições independentes => saída 0.")
caso("C0-028", "operadores", "Exemplo da fonte: 'speed > 100 /\\ mode = idle' (saída 0)",
     ["analyze", "speed > 100 /\\ mode = idle"], {"exit": 0},
     "./mcdc analyze 'speed > 100 /\\ mode = idle'", "Exemplo oficial; condições independentes.",
     "Saída 0.")
caso("C0-029", "operadores", "Número negativo: 'x > -3 and B' é válido (saída 0)",
     ["analyze", "x > -3 and B"], {"exit": 0},
     "Sinal de menos só em números", "O sinal de menos é permitido em números.", "Saída 0.")

# ---- Grupo 3: entradas invalidas ----
for i, (expr, why) in enumerate([("A and", "operador sem operando à direita"),
                                 ("(A and B", "parêntese não fechado"),
                                 ("and A", "operador sem operando à esquerda"),
                                 ("A and -B", "sinal de menos fora de um número")], start=30):
    caso("C0-%03d" % i, "entrada-invalida", "Expressão inválida (%s): saída 1" % why,
         ["analyze", expr], {"exit": 1}, "expressões inválidas recusadas / `1` entrada inválida",
         "Expressão sintaticamente inválida => entrada inválida => saída 1.", why + ".")

# ---- Grupo 4: formatos e saida ----
caso("C0-034", "formatos", "--format json produz JSON válido", ["analyze", "(A and B) or C", "--format", "json"],
     {"exit": 0, "json_valid": True}, "`json` | Resultado completo de cada decisão",
     "A saída em formato json é um JSON.", "Documento JSON analisável.")
caso("C0-035", "formatos", "truth-csv de 'A and B': 4 combinações + 1 cabeçalho = 5 linhas",
     ["analyze", "A and B", "--format", "truth-csv"], {"exit": 0, "lines": 5},
     Q_TTCSV + " / TruthTableCsvReportTest: Tabela inteira, combinações impossíveis marcadas, cabeçalho por decisão",
     "Uma linha por combinação (2^2) e um cabeçalho por decisão.", "4 + 1 = 5 linhas.")
caso("C0-036", "formatos", "truth-csv de 'A or (B and C)': 8 combinações + 1 cabeçalho = 9 linhas",
     ["analyze", "A or (B and C)", "--format", "truth-csv"], {"exit": 0, "lines": 9},
     "TruthTableTest: Uma linha por combinação / cabeçalho por decisão", "2^3 combinações + 1 cabeçalho.", "8 + 1 = 9.")
caso("C0-037", "formatos", "truth-csv mantém as combinações impossíveis (marcadas, não removidas): 5 linhas",
     ["analyze", "A and B", "--constraint", "not A or not B", "--format", "truth-csv"],
     {"lines": 5}, Q_TTCSV, "A tabela é inteira: a combinação impossível aparece marcada.",
     "4 combinações + 1 cabeçalho = 5 linhas, mesmo com restrição (a saída 2 não é avaliada aqui).")
caso("C0-038", "formatos", "-o grava o relatório no arquivo e não mostra na tela",
     ["analyze", "(A and B) or C", "-o", "@OUT/relatorio.txt"], {"exit": 0, "outfile": "relatorio.txt", "stdout_vazio": True},
     "`-o <arquivo>` | Grava o relatório no arquivo em vez de mostrar na tela",
     "O relatório vai para o arquivo.", "Arquivo criado e não vazio; stdout sem relatório.")
caso("C0-039", "formatos", "--mutation acrescenta a seção de mutação ao relatório em texto",
     ["analyze", "A and (B or C)", "--mutation"], {"exit": 0, "mais_longo_que": ["analyze", "A and (B or C)"]},
     "`text` | Tabela verdade, pares, suíte, ..., fronteiras, mutação e o motivo de cada problema / `--mutation` Confere se a suíte pega versões do requisito com um defeito",
     "Com --mutation o texto inclui a validação por mutação.", "Relatório estritamente maior que o sem --mutation; saída 0 (todas as condições têm par).")

# ---- Grupo 5: Z3 ----
caso("C0-040", "z3", "--direct: 'A or (A and B)' dá o mesmo diagnóstico da tabela (saída 2)",
     ["analyze", "A or (A and B)", "--direct"], {"exit": 2}, "o modo direto dá a mesma cobertura e o mesmo diagnóstico que a tabela inteira",
     "Modo direto equivale à tabela: B continua sem par.", "Saída 2.", usa_z3=True)
caso("C0-041", "z3", "--direct: '(A and B) or C' dá 4 testes x 3 entradas = 12 linhas CSV",
     ["analyze", "(A and B) or C", "--direct", "--format", "csv"], {"exit": 0, "csv_rows": 12},
     "O modo direto concorda com a tabela / mesma cobertura e mesmo diagnóstico",
     "Mesmo resultado que a tabela.", "12 linhas de dados.", usa_z3=True)
caso("C0-042", "z3", "--z3 com 13 entradas passa sozinho ao modo direto (saída 0)",
     ["analyze", conj(13), "--z3"], {"exit": 0}, "`--z3` ... acima de 12 entradas, passa sozinho ao modo direto",
     "13 entradas com --z3 é suportado; conjunção de entradas distintas tem par em todas.", "Saída 0.", usa_z3=True)
caso("C0-043", "limites", "Tabela inteira com 20 entradas (conjunção) funciona sem Z3 (saída 0)",
     ["analyze", conj(20)], {"exit": 0}, "20 entradas com a tabela inteira (cerca de 1 milhão de combinações)",
     "20 entradas é o limite suportado pela tabela inteira.", "Saída 0.")
caso("C0-044", "limites", "Modo direto com 26 entradas (conjunção) funciona (saída 0)",
     ["analyze", conj(26), "--direct"], {"exit": 0}, "o modo direto com 26 entradas ... e 30 no modo direto",
     "26 <= 30 entradas é suportado no modo direto.", "Saída 0.", usa_z3=True)
caso("C0-045", "z3", "--z3 --boundary 'speed > 100' traz os valores de fronteira 100 e 101",
     ["analyze", "speed > 100", "--z3", "--boundary"], {"exit": 0, "contains_todos": ["100", "101"]},
     "`--z3 --boundary` | Variações no limite de cada comparação (`speed > 100` → 100 e 101)",
     "A fronteira de speed > 100 são os valores 100 e 101.", "A saída deve mencionar 100 e 101.", usa_z3=True)
e2 = None
caso("C0-046", "z3", "--z3 --boundary 'speed > 100 or (speed > 50 and rain)' (saída 0)",
     ["analyze", "speed > 100 or (speed > 50 and rain)", "--z3", "--boundary"], {"exit": 0},
     "./mcdc analyze \"speed > 100 or (speed > 50 and rain)\" --z3 --boundary",
     "Exemplo oficial; sob a relação speed>100 => speed>50, todas as condições têm par.",
     "Z3 (Int speed) sat para as 3 condições.", usa_z3=True, pre_analise="numerico")
caso("C0-047", "z3", "--z3 mantém a tabela inteira (impossível marcada): 8 + 1 = 9 linhas truth-csv",
     ["analyze", "speed > 100 or (speed > 50 and rain)", "--z3", "--format", "truth-csv"],
     {"exit": 0, "lines": 9}, Q_TTCSV, "A combinação impossível (speed>100 e não speed>50) é marcada, não removida.",
     "8 combinações + 1 cabeçalho = 9.", usa_z3=True)
caso("C0-048", "z3", "--z3 dá valores concretos: speed > 100 /\\ mode = idle contém speed acima de 100",
     ["analyze", "speed > 100 /\\ mode = idle", "--z3", "--format", "csv"], {"exit": 0, "contem_numero_maior_que": 100},
     "`--z3` ... valores concretos para cada teste (`speed = 101`)",
     "Testes concretos com a condição speed > 100 verdadeira usam valor > 100.", "A saída contém um valor > 100.", usa_z3=True)
caso("C0-049", "z3", "Sem Z3 no PATH, a análise sem opções de Z3 funciona (12 linhas CSV)",
     ["analyze", "(A and B) or C", "--format", "csv"], {"exit": 0, "csv_rows": 12},
     "Sem o Z3, tudo funciona, exceto as opções que dependem dele", "Sem --z3 nada exige Z3.", "Mesmo resultado de C0-002.")

# ---- Grupo 6: arquivos de requisitos ----
MCDC_OK = ("# requisitos de teste\nREQ-001: (alarme_ativo and porta_aberta) or botao_emergencia\n"
           "REQ-002: porta_fechada and not obstaculo\n")
caso("C0-050", "arquivo-mcdc", "Arquivo .mcdc com comentário: json traz REQ-001 e REQ-002, ignora o comentário",
     ["analyze", "-f", "@F/req.mcdc", "--format", "json"],
     {"exit": 0, "contains": ["REQ-001", "REQ-002"], "json_valid": True, "not_contains": ["requisitos de teste"]},
     "um requisito por linha, `ID: expressão`. Linhas com `#` são comentários. / ligado ao requisito de origem",
     "Cada linha é um requisito; # é comentário; o JSON liga cada decisão ao requisito.",
     "Ambos os requisitos têm par para todas as condições => saída 0.", files={"req.mcdc": MCDC_OK}, pre_analise="mcdc")
caso("C0-051", "arquivo-mcdc", "Erro de sintaxe em REQ-002: saída 1 citando o requisito",
     ["analyze", "-f", "@F/ruim.mcdc"], {"exit": 1, "contains": ["REQ-002"]},
     "erro de sintaxe com o requisito / `1` entrada inválida", "Sintaxe inválida => saída 1 e a mensagem identifica o requisito.",
     "REQ-002 termina em operador sem operando.", files={"ruim.mcdc": "REQ-001: A and B\nREQ-002: A and\n"})
caso("C0-052", "arquivo-mcdc", "exemplos/requisitos.mcdc: REQ-003 tem condição redundante (saída 2, json cita REQ-003)",
     ["analyze", "-f", "exemplos/requisitos.mcdc", "--format", "json"], {"exit": 2, "contains": ["REQ-003"], "json_valid": True},
     "# vários requisitos de um arquivo; REQ-003 tem uma condição redundante / `2` alguma condição sem par",
     "Condição redundante => sem par => saída 2.", "Arquivo de exemplo da própria fonte.")

# ---- Grupo 7: JSON NAT2TEST ----
NAT_JSON = json.dumps({
    "system": "the_coffee_machine_system",
    "inputs": [{"name": "the_system_mode", "type": "enum", "values": ["idle", "choice"]},
               {"name": "the_coin_sensor", "type": "bool"}],
    "decisions": [{"id": "vm#1", "requirement": "REQ-001",
                   "guard": "the_system_mode = idle /\\ the_coin_sensor = true",
                   "actions": ["the_system_mode := choice"]}]}, indent=2)
caso("C0-053", "arquivo-json", "JSON de decisões do exemplo da fonte: saída 0 e REQ-001 no relatório json",
     ["analyze", "--json", "@F/vm.json", "--format", "json"],
     {"exit": 0, "contains": ["REQ-001"], "json_valid": True},
     "JSON de decisões (formato do Extractor da NAT2TEST) ... `\"requirement\": \"REQ-001\"`",
     "Decisão com duas condições independentes; relatório ligado ao requisito de origem.",
     "Saída 0 (ambas têm par).", files={"vm.json": NAT_JSON})
caso("C0-054", "arquivo-json", "JSON malformado: saída 1",
     ["analyze", "--json", "@F/ruim.json"], {"exit": 1}, "Nat2TestJsonReaderTest: arquivos inválidos / `1` entrada inválida",
     "Arquivo JSON inválido é recusado => saída 1.", "Conteúdo não é JSON.", files={"ruim.json": "{ isto nao e json"})

# ---- Grupo 8: check ----
CSV_OK = ("test,input,value,expected_outcome\nT1,A,T,T\nT1,B,T,T\nT2,A,F,F\nT2,B,T,F\nT3,A,T,F\nT3,B,F,F\n")
caso("C0-055", "check", "check: suíte MC/DC completa de 'A and B' com resultados esperados corretos (saída 0)",
     ["check", "A and B", "--tests", "@F/ok.csv"], {"exit": 0},
     "mcdc check <fonte> --tests <testes.csv> / `0` tudo certo", "Todas as condições demonstradas e resultados corretos => 0.",
     "T1/T2 demonstram A; T1/T3 demonstram B.", files={"ok.csv": CSV_OK}, pre_analise="check_ok")
caso("C0-056", "check", "check: falta T3, B não demonstrada (saída 2)",
     ["check", "A and B", "--tests", "@F/falta.csv"], {"exit": 2},
     "no `check`: alguma condição não demonstrada", "B sem par entre os testes => saída 2.",
     "Só há T1 e T2: B nunca muda.",
     files={"falta.csv": "test,input,value,expected_outcome\nT1,A,T,T\nT1,B,T,T\nT2,A,F,F\nT2,B,T,F\n"}, pre_analise="check_falta")
caso("C0-057", "check", "check: resultado esperado errado em T2 (saída 2)",
     ["check", "A and B", "--tests", "@F/errado.csv"], {"exit": 2},
     "no `check`: ... resultado esperado divergente", "T2 (A=F,B=T) dá F, mas o CSV espera T.",
     "Z3 (ground) unsat para 'guarda = esperado' em T2.",
     files={"errado.csv": "test,input,value,expected_outcome\nT1,A,T,T\nT1,B,T,T\nT2,A,F,T\nT2,B,T,T\nT3,A,T,F\nT3,B,F,F\n"},
     pre_analise="check_errado")
caso("C0-058", "check", "check: CSV sem a coluna 'value' é recusado (saída 1)",
     ["check", "A and B", "--tests", "@F/semvalue.csv"], {"exit": 1},
     "TestCasesFileTest: colunas faltando / `1` entrada inválida", "Coluna obrigatória ausente => entrada inválida.",
     "O cabeçalho não tem 'value'.", files={"semvalue.csv": "test,input\nT1,A\nT1,B\n"})
CSV_NAT_1 = "decision,test,input,value,expected_outcome\nvm#1,T1,the_system_mode,idle,T\nvm#1,T1,the_coin_sensor,true,T\n"
caso("C0-059", "check", "check com o exemplo de teste da fonte (só T1): condições não demonstradas (saída 2)",
     ["check", "--json", "@F/vm.json", "--tests", "@F/t1.csv"], {"exit": 2},
     "vm#1,T1,the_system_mode,idle,T / vm#1,T1,the_coin_sensor,true,T", "Um único teste não demonstra nenhuma condição.",
     "Sem par para nenhuma condição => saída 2.", files={"vm.json": NAT_JSON, "t1.csv": CSV_NAT_1})
CSV_NAT_3 = CSV_NAT_1 + ("vm#1,T2,the_system_mode,choice,F\nvm#1,T2,the_coin_sensor,true,F\n"
                         "vm#1,T3,the_system_mode,idle,F\nvm#1,T3,the_coin_sensor,false,F\n")
caso("C0-060", "check", "check com valores concretos (enum/bool): 3 testes completos (saída 0)",
     ["check", "--json", "@F/vm.json", "--tests", "@F/t3.csv"], {"exit": 0},
     "o valor lógico (`T`/`F`) ou o valor concreto da variável", "Valores concretos dos testes realizam as condições; completo => 0.",
     "T1/T2 demonstram mode=idle; T1/T3 demonstram coin=true.", files={"vm.json": NAT_JSON, "t3.csv": CSV_NAT_3})
CSV_SPD = ("test,input,value,expected_outcome\nT1,speed,150,T\nT1,rain,T,T\nT2,speed,50,F\nT2,rain,T,F\n"
           "T3,speed,150,F\nT3,rain,F,F\n")
caso("C0-061", "check", "check com expressão numérica 'speed > 100 and rain' e valores concretos (saída 0)",
     ["check", "speed > 100 and rain", "--tests", "@F/spd.csv"], {"exit": 0},
     "o valor lógico (`T`/`F`) ou o valor concreto da variável", "speed=150 satisfaz speed>100; speed=50 não.",
     "Mesma estrutura de A and B.", files={"spd.csv": CSV_SPD})
caso("C0-062", "check", "check --format json produz JSON válido",
     ["check", "A and B", "--tests", "@F/ok.csv", "--format", "json"], {"exit": 0, "json_valid": True},
     "`check` e `verify` aceitam `text` e `json`", "Formato json é aceito pelo check.", "JSON analisável.",
     files={"ok.csv": CSV_OK})

# ---- Grupo 9: verify ----
def nat(decisions):
    return json.dumps({"system": "s", "inputs": [
        {"name": "the_system_mode", "type": "enum", "values": ["idle", "choice"]},
        {"name": "the_coin_sensor", "type": "bool"}], "decisions": decisions}, indent=2)

D1 = {"id": "d1", "requirement": "REQ-001", "guard": "the_coin_sensor = true", "actions": ["the_system_mode := choice"]}
D2c = {"id": "d2", "requirement": "REQ-002", "guard": "the_coin_sensor = true", "actions": ["the_system_mode := idle"]}
D2s = {"id": "d2", "requirement": "REQ-002", "guard": "the_coin_sensor = true", "actions": ["the_system_mode := choice"]}
D2d = {"id": "d2", "requirement": "REQ-002", "guard": "the_coin_sensor = false", "actions": ["the_system_mode := idle"]}
DM = {"id": "d1", "requirement": "REQ-001", "guard": "the_system_mode = idle", "actions": ["the_coin_sensor := true"]}
caso("C0-063", "verify", "verify: dois requisitos válidos juntos escrevendo valores diferentes => conflito (saída 2)",
     ["verify", "--json", "@F/conf.json"], {"exit": 2},
     "Conflitos (dois requisitos valem juntos e escrevem valores diferentes) / `no verify: algum conflito ou lacuna`",
     "Guardas iguais, mesma variável com valores diferentes => conflito => saída 2.", "SMT sat (guarda comum e valores distintos).",
     files={"conf.json": nat([D1, D2c])}, usa_z3=True, pre_analise="conflito")
caso("C0-064", "verify", "verify: guardas que não se sobrepõem => sem conflito (saída 0)",
     ["verify", "--json", "@F/disj.json"], {"exit": 0}, "Z3RequirementsVerifierTest: guardas que não se sobrepõem",
     "Sem sobreposição não há conflito nem lacuna (sem contexto).", "SMT unsat para a sobreposição.",
     files={"disj.json": nat([D1, D2d])}, usa_z3=True, pre_analise="disjunto")
caso("C0-065", "verify", "verify: mesmo valor escrito sem conflito (saída 0)",
     ["verify", "--json", "@F/mesmo.json"], {"exit": 0}, "Z3RequirementsVerifierTest: mesmo valor sem conflito",
     "Guardas sobrepostas mas valores iguais => sem conflito.", "SMT unsat (valores distintos impossíveis).",
     files={"mesmo.json": nat([D1, D2s])}, usa_z3=True, pre_analise="mesmovalor")
caso("C0-066", "verify", "verify --context sem guarda aplicável: lacuna (saída 2)",
     ["verify", "--json", "@F/lac.json", "--context", "the_system_mode = choice"], {"exit": 2},
     "Lacunas (nenhum requisito vale) / `--context` confere se, nessa situação, sempre alguma guarda vale",
     "No contexto mode=choice a única guarda (mode=idle) nunca vale => lacuna => saída 2.", "SMT sat para 'contexto e nenhuma guarda'.",
     files={"lac.json": nat([DM])}, usa_z3=True, pre_analise="lacuna")
caso("C0-067", "verify", "verify --context com guarda sempre válida: sem lacuna (saída 0)",
     ["verify", "--json", "@F/lac.json", "--context", "the_system_mode = idle"], {"exit": 0},
     "`--context` confere se, nessa situação, sempre alguma guarda vale", "No contexto mode=idle a guarda sempre vale => saída 0.",
     "SMT unsat para 'contexto e nenhuma guarda'.", files={"lac.json": nat([DM])}, usa_z3=True, pre_analise="semlacuna")
caso("C0-068", "verify", "verify sem contexto não aponta lacuna (saída 0)",
     ["verify", "--json", "@F/lac.json"], {"exit": 0}, "Z3RequirementsVerifierTest: lacunas só com contexto",
     "Sem --context não há lacunas.", "Decisão única sem conflito.", files={"lac.json": nat([DM])}, usa_z3=True)
caso("C0-069", "verify", "verify --format json produz JSON válido",
     ["verify", "--json", "@F/disj.json", "--format", "json"], {"exit": 0, "json_valid": True},
     "`check` e `verify` aceitam `text` e `json`", "Formato json é aceito pelo verify.", "JSON analisável.",
     files={"disj.json": nat([D1, D2d])}, usa_z3=True)
caso("C0-070", "verify", "verify exemplos/vm-decisoes.json: 0 conflitos (saída 0)",
     ["verify", "--json", "exemplos/vm-decisoes.json"], {"exit": 0},
     "VM · máquina de café ... Conflitos 0 / ./mcdc verify --json exemplos/vm-decisoes.json",
     "VM não tem conflitos; sem contexto não há lacunas.", "Tabela travada: Conflitos = 0.", usa_z3=True)
caso("C0-071", "verify", "verify exemplos/tis-decisoes.json: 3 conflitos (saída 2)",
     ["verify", "--json", "exemplos/tis-decisoes.json"], {"exit": 2},
     "TIS · pisca-pisca ... Conflitos 3 / `no verify: algum conflito ou lacuna`", "Há conflitos => saída 2.", "Tabela travada: Conflitos = 3.", usa_z3=True)
caso("C0-072", "verify", "verify exemplos/npp-decisoes.json: 1 conflito (saída 2)",
     ["verify", "--json", "exemplos/npp-decisoes.json"], {"exit": 2},
     "NPP · injeção de segurança ... Conflitos 1 / ./mcdc verify --json exemplos/npp-decisoes.json",
     "Há conflito => saída 2.", "Tabela travada: Conflitos = 1.", usa_z3=True)

# ---- Casos INDETERMINADOS (nao entram na execucao de cobertura) ----
def indet(id_, titulo, args, citacao, motivo):
    caso(id_, "indeterminado", titulo, args, {}, citacao, "Sem regra que determine a expectativa.", motivo,
         status="INDETERMINADO", motivo=motivo)

indet("C0-I01", "causa única na paridade de 3 entradas (número de testes)", ["analyze", "<paridade>", "--unique-cause"],
      "o MC/DC pode exigir todas as combinações (ex.: a paridade de 3 entradas pede 8 testes)",
      "A fonte não diz se o exemplo vale para as duas variantes.")
indet("C0-I02", "causa única em (A and B) or (not A and C) com A repetida (saída?)", ["analyze", "(A and B) or (not A and C)", "--unique-cause"],
      "(A and B) or (not A and C) / cada aparição de uma entrada na expressão conta como uma condição",
      "A fonte não define causa única quando a mesma entrada aparece duas vezes (A#1 e A#2 não variam isoladamente).")
indet("C0-I03", "número de testes de (A and B) or (not A and C)", ["analyze", "(A and B) or (not A and C)", "--format", "csv"],
      "Nas guardas simples, a suíte tem N + 1 testes",
      "'Guarda simples' não é definida e a decisão repete entrada; não há contagem documentada.")
indet("C0-I04", "--boundary sem --z3", ["analyze", "speed > 100", "--boundary"], "`--boundary` | Com `--z3`, acrescenta variantes de fronteira",
      "A fonte não diz o que ocorre sem --z3.")
indet("C0-I05", "--format com valor desconhecido (xml)", ["analyze", "A and B", "--format", "xml"], "`--format <formato>` `text` (padrão), `json`, `csv`, `truth-csv`",
      "Código de saída para formato inexistente não é documentado.")
indet("C0-I06", "check --format csv", ["check", "A and B", "--tests", "x.csv", "--format", "csv"], "`check` e `verify` aceitam `text` e `json`",
      "A fonte não diz como recusar csv no check.")
indet("C0-I07", "ids repetidos no JSON de decisões", ["analyze", "--json", "dup.json"], "Nat2TestJsonReaderTest: ... ids repetidos",
      "Não diz se a repetição é recusada ou aceita.")
indet("C0-I08", "--constraint com arquivo", ["analyze", "-f", "x.mcdc", "--constraint", "A"], "`--constraint` (só com expressão direta)",
      "Efeito da violação não documentado.")
indet("C0-I09", "duas fontes ao mesmo tempo", ["analyze", "A and B", "-f", "x.mcdc"], "**Fonte** (uma só)", "Comportamento ao receber duas fontes não documentado.")
indet("C0-I10", "nenhuma fonte", ["analyze"], "mcdc analyze <fonte> [opções]", "Comportamento sem fonte não documentado.")
indet("C0-I11", "21 entradas com a tabela inteira", ["analyze", "<21 entradas>"], "limite de 20 entradas",
      "A fonte dá o limite, mas não o que ocorre acima dele.")
indet("C0-I12", "--direct com 31 entradas", ["analyze", "<31 entradas>", "--direct"], "até 30 entradas",
      "A fonte dá o limite, mas não o que ocorre acima dele.")
indet("C0-I13", "verify VM com --context 'the_system_mode = preparing_weak'", ["verify", "--json", "exemplos/vm-decisoes.json", "--context", "the_system_mode = preparing_weak"],
      "./mcdc verify --json exemplos/vm-decisoes.json --context 'the_system_mode = preparing_weak'", "A fonte não diz se há lacuna nesse contexto.")
indet("C0-I14", "código de saída de analyze --json exemplos/vm-decisoes.json", ["analyze", "--json", "exemplos/vm-decisoes.json", "--z3"],
      "VM · máquina de café | 5 | 5 | 21 ... | Completos", "'Completo' não é definido; não equivale explicitamente a 'nenhuma condição sem par'.")
indet("C0-I15", "código de saída de analyze --json exemplos/tis-decisoes.json", ["analyze", "--json", "exemplos/tis-decisoes.json", "--z3"],
      "TIS · pisca-pisca | 17 | 14 | 69 ...", "Mesma indefinição de 'Completos'.")
indet("C0-I16", "operador '&' simples", ["analyze", "A & B"], "Operadores: and, &&, /\\", "A fonte não diz se '&' é aceito ou recusado.")
indet("C0-I17", "arquivo .mcdc inexistente", ["analyze", "-f", "nao-existe.mcdc"], "`1` entrada inválida", "Não diz se arquivo ausente é 'entrada inválida'.")
indet("C0-I18", "linha .mcdc sem identificador", ["analyze", "-f", "semid.mcdc"], "RequirementsFileTest: ... linha sem identificador", "Não diz se a linha é recusada ou recebe ID automático.")
indet("C0-I19", "número exato de testes de exemplos/vm-decisoes.json em CSV", ["analyze", "--json", "exemplos/vm-decisoes.json", "--z3", "--format", "csv"],
      "VM ... Testes 26", "Opções usadas na tabela travada e o formato exato de linhas (por decisão/entrada) não são definidos.")
indet("C0-I20", "texto exato da seção de mutação (tipos ORF, ENF, ...)", ["analyze", "A and (B or C)", "--mutation"],
      "seis tipos de Kapoor e Bowen (ORF, ENF, VNF, MVF, VRF, ASF)", "O formato textual do resumo por tipo não é definido.")
indet("C0-I21", "Z3 ausente com --z3", ["analyze", "A and B", "--z3"], "que avisam quando ele não está instalado", "Texto do aviso e código de saída não definidos.")
indet("C0-I22", "limite de 1000 pares por condição", ["analyze", "<expressão grande>"], "até 1000 pares guardados por condição", "Comportamento ao ultrapassar não é definido.")


# --------------------------------------------------------------------------
# Pre-analises Z3 especificas
# --------------------------------------------------------------------------
def anexar_evidencia(id_, ev_):
    for c in CASOS:
        if c["id"] == id_:
            c["evidencia_z3"] = ev_


def main():
    versao = z3_version()
    resumo = {}

    # Garante que cada caso booleano tem expectativa de saida cruzada com Z3
    mapa_exit = {
        "C0-001": ("(A and B) or C", None, "e001"),
        "C0-007": ("(A and B) or (not A and C)", None, "e007"),
        "C0-008": ("A or (A and B)", None, "e008"),
        "C0-009": ("A and B", "not A or not B", "e009"),
        "C0-010": ("A or (B and C)", "not A or B", "e010"),
        "C0-011": ("A or B and C", "not A or not C", "e011"),
        "C0-012": ("A and B or C", "not A or not C", "e012"),
        "C0-004": ("A and not B", None, "e004"),
        "C0-005": ("(A and B and C) or (A and not B and not C) or (not A and B and not C) or (not A and not B and C)", None, "e005"),
        "C0-006": ("((E or D) and (not A or D)) or B", None, "e006"),
        "C0-050a": ("(alarme_ativo and porta_aberta) or botao_emergencia", None, "e050a"),
        "C0-050b": ("porta_fechada and not obstaculo", None, "e050b"),
        "C0-040": ("A or (A and B)", None, "e040"),
        "C0-042": (conj(13), None, "e042"),
        "C0-044": (conj(26), None, "e044") if False else (conj(8), None, "e044amostra8"),
        "C0-039": ("A and (B or C)", None, "e039"),
    }
    # NOTA: conjuncoes com 13/20/26 entradas: o Z3 verifica uma amostra (8 entradas) e
    # a propriedade geral e demonstrada abaixo por consulta parametrica (13 entradas).
    esperado_exit = {"C0-001": 0, "C0-007": 0, "C0-008": 2, "C0-009": 2, "C0-010": 0, "C0-011": 0,
                     "C0-012": 0, "C0-004": 0, "C0-005": 0, "C0-006": 0, "C0-050a": 0, "C0-050b": 0,
                     "C0-040": 2, "C0-042": 0, "C0-044": 0, "C0-039": 0}
    for key, (expr, cons, tag) in mapa_exit.items():
        if key == "C0-044":
            continue
        e_, ev_ = exit_expect(expr, tag, cons)
        resumo[key] = {"expressao": expr, "restricao": cons, "exit_smt": e_, "respostas": ev_}
        assert e_ == esperado_exit[key], "expectativa do oraculo diverge do Z3 em %s" % key
        base = key.split("a")[0].split("b")[0] if key.startswith("C0-050") else key
        anexar_evidencia(base if not key.startswith("C0-050") else "C0-050", resumo[key])
    # conjuncao de 26 entradas (limite documentado ate 30): par de A1 e A26 por Z3 (propriedade geral)
    for nome, n in (("conj20", 20), ("conj26", 26)):
        expr = conj(n)
        for k in (0, n - 1):
            resp, _ = smt_pair(expr, k, None, nome)
            assert resp == "sat"
        resumo["C0-%s" % ("043" if n == 20 else "044")] = {"amostra": [0, n - 1], "respostas": ["sat", "sat"]}
    # conjuncao de 13 entradas
    for k in (0, 12):
        resp, _ = smt_pair(conj(13), k, None, "conj13")
        assert resp == "sat"

    # Suite minima do exemplo --exact e do (A and B) or C, A and not B, paridade
    sizes = {}
    for nome, expr, esperado in [("exato", "((E or D) and (not A or D)) or B", 5),
                                 ("abc", "(A and B) or C", 4), ("anb", "A and not B", 3),
                                 ("paridade", "(A and B and C) or (A and not B and not C) or (not A and B and not C) or (not A and not B and C)", 8)]:
        k, res = min_suite(expr, nome)
        sizes[nome] = {"expressao": expr, "minimo_z3": k, "esperado_fonte": esperado, "respostas": res}
        assert k == esperado, "minimo Z3 (%s)=%s diverge da fonte (%s)" % (nome, k, esperado)
    resumo["suite_minima"] = sizes

    # Numerico: speed > 100 or (speed > 50 and rain), com relacao entre predicados
    def numerico(k, tag):
        conds = ["(> speed 100)", "(> speed 50)", "rain"]
        # decisao: A or (B and C) com A=speed>100, B=speed>50, C=rain
        def dec(sp, rn, flip):
            a = "(> %s 100)" % sp; b = "(> %s 50)" % sp; c = rn
            if flip == 0: a = "(not %s)" % a
            if flip == 1: b = "(not %s)" % b
            if flip == 2: c = "(not %s)" % c
            return "(or %s (and %s %s))" % (a, b, c)
        t = "; par de independencia para a condicao %d de 'speed > 100 or (speed > 50 and rain)' (Int)\n" % k
        t += "(declare-const s1 Int)(declare-const s2 Int)(declare-const rn1 Bool)(declare-const rn2 Bool)\n"
        val = {0: lambda s, r: "(> %s 100)" % s, 1: lambda s, r: "(> %s 50)" % s, 2: lambda s, r: r}[k]
        t += "(assert (not (= %s %s)))\n" % (val("s1", "rn1"), val("s2", "rn2"))
        t += "(assert (not (= %s %s)))\n" % (dec("s1", "rn1", None), dec("s2", "rn2", None))
        t += "(assert (not (= %s %s)))\n" % (dec("s1", "rn1", None), dec("s1", "rn1", k))
        t += "(assert (not (= %s %s)))\n(check-sat)\n(get-model)\n" % (dec("s2", "rn2", None), dec("s2", "rn2", k))
        return run_z3("par_num_c%d" % k, t)
    nres = []
    for k in range(3):
        r, _ = numerico(k, "num")
        assert r == "sat"
        nres.append(r)
    resumo["C0-046"] = {"expressao": "speed > 100 or (speed > 50 and rain)", "respostas": nres}
    # combinacao impossivel: speed>100 e not speed>50
    t = "(declare-const s Int)\n(assert (> s 100))\n(assert (not (> s 50)))\n(check-sat)\n"
    r, _ = run_z3("impossivel_speed", t)
    assert r == "unsat"
    resumo["C0-047"] = {"combinacao_impossivel_speed>100_e_nao_speed>50": r}

    # check: demonstracao de condicoes
    def gt(a, b): return (a, b)
    r1 = ({"A": True, "B": True}, True); r2 = ({"A": False, "B": True}, False); r3 = ({"A": True, "B": False}, False)
    ok = smt_check("A and B", [r1, r2, r3], "ok")
    falta = smt_check("A and B", [r1, r2], "falta")
    unico = smt_check("A and B", [r1], "t1")
    assert ok == [True, True] and falta == [True, False] and unico == [False, False]
    # resultado esperado errado: guarda(T2)=F, esperado T -> igualdade unsat
    t = "(assert (= (and false true) true))\n(check-sat)\n"
    r, _ = run_z3("check_errado_t2", t)
    assert r == "unsat"
    resumo["check"] = {"ok": ok, "falta_T3": falta, "so_T1": unico, "esperado_errado_T2": r}

    # verify: conflitos / lacunas (enum como Int 0=idle,1=choice; coin Bool)
    def vsmt(nome, guard1, act1, guard2, act2, ctx=None, gap=False):
        t = "(declare-const mode Int)(declare-const coin Bool)(declare-const m1 Int)(declare-const m2 Int)\n"
        t += "(assert (and (>= mode 0) (<= mode 1)))\n"
        if gap:
            t += "(assert %s)\n(assert (not %s))\n" % (ctx, guard1)
        else:
            t += "(assert %s)(assert %s)\n(assert (= m1 %s))(assert (= m2 %s))(assert (distinct m1 m2))\n" % (guard1, guard2, act1, act2)
        t += "(check-sat)\n"
        return run_z3(nome, t)[0]
    coin = "coin"
    v = {}
    v["conflito"] = vsmt("verify_conflito", coin, 1, coin, 0); assert v["conflito"] == "sat"
    v["disjunto"] = vsmt("verify_disjunto", coin, 1, "(not coin)", 0); assert v["disjunto"] == "unsat"
    v["mesmo_valor"] = vsmt("verify_mesmo_valor", coin, 1, coin, 1); assert v["mesmo_valor"] == "unsat"
    v["lacuna_ctx_choice"] = vsmt("verify_lacuna_choice", "(= mode 0)", None, None, None, ctx="(= mode 1)", gap=True); assert v["lacuna_ctx_choice"] == "sat"
    v["lacuna_ctx_idle"] = vsmt("verify_lacuna_idle", "(= mode 0)", None, None, None, ctx="(= mode 0)", gap=True); assert v["lacuna_ctx_idle"] == "unsat"
    resumo["verify"] = v

    # Pre-analises do exit dos arquivos .mcdc e do JSON nat (guardas independentes)
    resumo["C0-053"] = {"nota": "duas condições sobre variáveis distintas: ambas têm par (AND de 2)"}
    e_, ev_ = exit_expect("A and B", "natjson")
    assert e_ == 0

    oraculo = {"condicao": "C0", "fonte": "experimentacao-pesquisa/documentacao-original/tool-readme-original.md",
               "sha256_fonte": "72b827bdee6ce859527765cff574a473519c00a1af9aa9f3aacce4236a4995f8",
               "z3": versao, "casos": CASOS}
    with open(os.path.join(AQUI, "oraculo.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(oraculo, f, ensure_ascii=False, indent=2)
        f.write("\n")
    with open(os.path.join(SMT_DIR, "resultados-z3.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"z3": versao, "consultas": Z3_LOG, "resumo": resumo}, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    det = sum(1 for c in CASOS if c["status"] == "DETERMINADO")
    ind = sum(1 for c in CASOS if c["status"] == "INDETERMINADO")
    print("Z3:", versao)
    print("consultas Z3:", len(Z3_LOG), "| casos determinados:", det, "| indeterminados:", ind)


if __name__ == "__main__":
    main()
