"""Extensão 01 do oráculo C1: situações documentadas ainda não testadas no baseline.

A cobertura da rodada-02 só LOCALIZOU branches não exercitados; cada expectativa abaixo vem do texto
de tool-readme-C1.md (linhas Lnnn) e/ou de consultas Z3 independentes (z3/). Nenhum resultado observado
do SUT foi usado como expectativa. Uso: python -I gerar_extensao.py <z3.exe>
"""
import itertools, json, os, subprocess, sys

Z3 = sys.argv[1]
BASE = os.path.dirname(os.path.abspath(__file__))
IN = os.path.join(BASE, "entradas")
QD, OD = os.path.join(BASE, "z3", "consultas"), os.path.join(BASE, "z3", "saidas")
for d in (IN, QD, OD):
    os.makedirs(d, exist_ok=True)


def wtext(name, text):
    with open(os.path.join(IN, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def wjson(name, obj):
    with open(os.path.join(IN, name), "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


# ---------------- entradas ----------------
CMP_GUARD = "x < 5 /\\ y <= 5 /\\ z > 5 /\\ w >= 5 /\\ v != 5 /\\ u = 5 /\\ mode != idle"
wjson("EX01_comparacoes.json", {"system": "c1_ext", "inputs": [
    {"name": n, "type": "int"} for n in ("x", "y", "z", "w", "v", "u")] + [
    {"name": "mode", "type": "enum", "values": ["idle", "choice"]}],
    "decisions": [{"id": "cmp#1", "requirement": "R-CMP", "guard": CMP_GUARD, "actions": ["mode := idle"]}]})
base = {"x": "4", "y": "5", "z": "6", "w": "5", "v": "4", "u": "5", "mode": "choice"}
flips = [("x", "5"), ("y", "6"), ("z", "5"), ("w", "4"), ("v", "5"), ("u", "4"), ("mode", "idle")]
lines = ["decision,test,input,value,expected_outcome"]
tests = [("T0", base, "T")] + [(f"T{i+1}", {**base, k: v}, "F") for i, (k, v) in enumerate(flips)]
for name, vals, exp in tests:
    for k, v in vals.items():
        lines.append(f"cmp#1,{name},{k},{v},{exp}")
wtext("EX01_testes_concretos.csv", "\n".join(lines) + "\n")
wtext("EX03_aspas.csv", 'test,input,value,expected_outcome\n"T1","A","T","T"\n"T1","B","T","T"\n"T2","A","F","F"\n"T2","B","T","F"\n"T3","A","T","F"\n"T3","B","F","F"\n')
wtext("EX04_celula_vazia.csv", "test,input,value,expected_outcome\nT1,A,T,T\nT1,B,,T\n")
wjson("EX05_virgula_requisito.json", {"system": "c1_ext", "inputs": [{"name": "flag", "type": "bool"}, {"name": "sw", "type": "bool"}],
      "decisions": [{"id": "q#1", "requirement": "R-1, R-2", "guard": "flag = true /\\ sw = true", "actions": []}]})
wtext("EX06_json_malformado.json", '{"system": "x", "decisions": [ {"id": "a", "guard": "A" ]\n')
wtext("EX20_req_redundante.mcdc", "R-3: freio or (freio and pedal)\n")

PAR11 = "A and (" + " or ".join(f"B{i}" for i in range(1, 12)) + ")"
cases = []


def case(id, cmds, expect, quote, regra, just, z3=None, status="DETERMINADO", env="padrao"):
    cases.append({"id": id, "grupo": "extensao-01", "status": status, "comandos": cmds, "ambiente": env,
                  "expectativa": expect, "trecho": quote, "regra": regra, "justificativa": just, "z3": z3 or []})


L_EXIT = "L139 (códigos 0/1/2)"
case("EX-01", [["check", "--json", "{IN}/EX01_comparacoes.json", "--tests", "{IN}/EX01_testes_concretos.csv"]], {"exit": 0},
     ["L183: \"O valor pode ser lógico (`T`/`F`) ou concreto, conforme o tipo da variável.\"", "L137 (comparadores)", L_EXIT,
      "L499: \"valores concretos\" (TestSetEvaluationTest)"],
     "Valores concretos nos limites de <, <=, >, >=, !=, = e != em enum; T0 todas verdadeiras (T), T1..T7 uma falsa (F). "
     "Esperados corretos e cada condição demonstrada (T0 x Ti) => 0.",
     "Tipo 'int' como no arquivo citado pelo C1 (exemplos/decisoes.json). Z3: T0 satisfaz a guarda e cada Ti não (Q-E01).", ["QE01_*"])
case("EX-02", [["check", "--json", "{IN}/EX01_comparacoes.json", "--tests", "{IN}/EX01_testes_concretos.csv", "--format", "json"]],
     {"json_valido": True}, ["L121"], "JSON válido no check com valores concretos.", "Texto literal.")
case("EX-03", [["check", "A and B", "--tests", "{IN}/EX03_aspas.csv"]], {"exit": 0},
     ["L523: \"Aspas no CSV\"", L_EXIT], "Células entre aspas lidas pelo conteúdo; mesmo conjunto de CK-01 => 0.", "CSV padrão: aspas delimitam a célula.")
case("EX-04", [["check", "A and B", "--tests", "{IN}/EX04_celula_vazia.csv"]], {"exit": 1, "stderr_contem": "3"},
     ["L523: \"número da linha com erro\"", L_EXIT], "Valor vazio na linha 3 => entrada inválida (1) e a mensagem traz o número da linha.", "Texto literal.")
case("EX-05", [["analyze", "--json", "{IN}/EX05_virgula_requisito.json", "--format", "csv"]],
     {"exit": 0, "csv_coluna_igual": {"coluna": "requirement", "valor": "R-1, R-2"}},
     ["L553: \"aspas em células com vírgula\"", "L205"], "Célula com vírgula entre aspas: o CSV lido devolve 'R-1, R-2' em todas as linhas; 2 condições com par => 0.", "Texto literal.")
case("EX-06", [["analyze", "--json", "{IN}/EX06_json_malformado.json"]], {"exit": 1},
     ["L519: \"arquivos inválidos\"", L_EXIT], "JSON sintaticamente inválido => 1.", "Texto literal.")
case("EX-07", [["analyze", "A and B", "-f", "{IN}/EX20_req_redundante.mcdc"]], {"exit": 1},
     ["L87: \"**Fonte** (uma só)\"", L_EXIT], "Duas fontes => entrada inválida => 1.", "Fonte é uma só.")
case("EX-08", [["check", "A and B"]], {"exit": 1},
     ["L81: \"mcdc check   <fonte> --tests <testes.csv>\"", L_EXIT], "check sem --tests => 1.", "--tests faz parte da sintaxe do check.")
case("EX-09", [["analyze", "A and B", "--format"]], {"exit": 1}, ["L121: \"`--format <formato>`\"", L_EXIT],
     "Opção sem o valor obrigatório => 1.", "Sintaxe exige o valor.")
case("EX-10", [["analyze", "A B"]], {"exit": 1}, ["L515: \"expressões inválidas recusadas\""], "Entradas sem operador => 1.", "Texto literal.")
case("EX-11", [["analyze", "A and or B"]], {"exit": 1}, ["L515"], "Operador onde se espera operando => 1.", "Texto literal.")
case("EX-12", [["analyze", "(A and B))"]], {"exit": 1}, ["L515"], "Parêntese a mais => 1.", "Texto literal.")
case("EX-13", [["analyze", "x > -3 and x < 2", "--z3", "--format", "truth-csv"]],
     {"linhas_dados": 4, "impossiveis_formula": {"colunas": {"a": "> -3", "b": "< 2"}, "impossivel_sse": "(not a) and (not b)"}},
     ["L533: \"enumerações, booleanos, reais e negativos\"", "L281", "L207"],
     "Única linha impossível: x>-3 falso e x<2 falso.", "Z3: só (F,F) unsat, em Int e em Real.", ["QE13_*"], env="z3")
case("EX-14", [["analyze", "x > 3 and y <= x and y > 5", "--z3", "--format", "truth-csv"]],
     {"linhas_dados": 8, "impossiveis_formula": {"colunas": {"a": "x > 3", "b": "y <= x", "c": "y > 5"}, "impossivel_sse": "(not a) and b and c"}},
     ["L417: \"comparações numéricas ... (`x > 3`, `y <= x`, ...), acopladas entre si\"", "L281"],
     "Impossível só x<=3 ∧ y<=x ∧ y>5.", "Z3: exatamente essa linha unsat, em Int e em Real.", ["QE14_*"], env="z3")
case("EX-15", [["analyze", "t >= 10.5 and t <= 30.0", "--z3", "--format", "truth-csv"]],
     {"linhas_dados": 4, "impossiveis_formula": {"colunas": {"a": ">= 10.5", "b": "<= 30"}, "impossivel_sse": "(not a) and (not b)"}},
     ["L533: \"reais\"", "L281"], "Única linha impossível: t<10.5 e t>30.", "Z3 (Real): só (F,F) unsat.", ["QE15_*"], env="z3")
case("EX-16", [["analyze", "x < -5 or x > 5", "--z3", "--format", "csv"]], {"exit": 0, "guarda_py": "(x < -5) or (x > 5)"},
     ["L463: \"os valores concretos realizam a combinação declarada e o resultado esperado é o que a guarda dá\"", "L533: negativos"],
     "Valores concretos (inclusive negativos) realizam o resultado esperado; condições com par => 0.",
     "Z3: (T,T) impossível; pares (T,F)/(F,F) e (F,T)/(F,F) viáveis.", ["QE16_*"], env="z3")
case("EX-17", [["analyze", "t > 0.5 and t < 1.0", "--z3", "--format", "csv"]], {"exit": 0, "guarda_py": "(t > 0.5) and (t < 1.0)"},
     ["L463", "L533: reais"], "Valores reais realizam o esperado; pares viáveis => 0.",
     "Z3 (Real): linhas TT, TF, FT sat; FF unsat; pares de causa única (TT/FT, TT/TF) viáveis.", ["QE17_*"], env="z3")
case("EX-18", [["analyze", "x > -3", "--z3", "--boundary", "--format", "json"]], {"fronteiras_incluem": {"var": "x", "valores": [-3, -2]}},
     ["L43: \"`speed > 100` → 100 e 101\"", "L533: negativos"], "Por analogia literal ao exemplo inteiro: x > -3 → -3 e -2.",
     "Z3: -2 é o menor inteiro > -3 e -3 não satisfaz.", ["QE18_fronteira"], env="z3")
case("EX-19", [["analyze", "-f", "{EX}/requisitos.mcdc", "--direct", "--format", "json"], ["analyze", "-f", "{EX}/requisitos.mcdc", "--format", "json"]],
     {"cobertura_e_diagnostico_iguais": True}, ["L419: \"o modo direto dá a mesma cobertura e o mesmo diagnóstico que a tabela-verdade completa\""],
     "Direto = tabela (inclusive a condição redundante do REQ-003).", "Texto literal.", env="z3")
case("EX-20", [["analyze", "(A and B) or C", "--unique-cause", "--direct", "--format", "json"], ["analyze", "(A and B) or C", "--unique-cause", "--format", "json"]],
     {"cobertura_e_diagnostico_iguais": True}, ["L419: \"nas duas variantes\" / modo direto = tabela"], "Direto = tabela na causa única.", "Texto literal.", env="z3")
case("EX-21", [["analyze", "A and B", "--constraint", "A", "--direct", "--format", "json"], ["analyze", "A and B", "--constraint", "A", "--format", "json"]],
     {"cobertura_e_diagnostico_iguais": True}, ["L419", "L535: \"condições bloqueadas\" (Z3DirectAnalyzerTest)"],
     "Direto = tabela com restrição (A bloqueada).", "Texto literal; Z3 Q01_AN14.", env="z3")
case("EX-22", [["analyze", "speed > 100 and speed > 50", "--direct", "--format", "json"], ["analyze", "speed > 100 and speed > 50", "--z3", "--format", "json"]],
     {"cobertura_e_diagnostico_iguais": True}, ["L419", "L535"], "Direto = tabela com Z3 (condição bloqueada por impossíveis).", "Texto literal.", env="z3")
case("EX-23", [["analyze", "not A or (B and not C)", "--mutation"]], {"exit": 0},
     ["L239", L_EXIT], "Mutação não altera o código; todas as condições com par => 0.", "Z3: pares de causa única sat para A, B, C.", ["QE23_*"])
case("EX-24", [["analyze", PAR11, "--format", "json"]], {"exit": 0, "pares_max": {"condicao": "A", "max": 1000}},
     ["L587: \"até 1000 pares guardados por condição\"", L_EXIT],
     "A tem 2047 pares de causa única (>1000); no máximo 1000 guardados; condições com par => 0.",
     "Z3: contagem por enumeração de modelos não é necessária: 2^11-1 combinações de B com OR verdadeiro (aritmética).")
case("EX-25", [["analyze", "-f", "{EX}/requisitos.mcdc", "--format", "truth-csv"]], {"exit": 2, "blocos_linhas": [8, 4, 4]},
     ["L555: \"cabeçalho por decisão\"", "L279: 2ⁿ combinações", "L241: REQ-003 redundante"],
     "Três blocos com cabeçalho (8, 4 e 4 linhas: 3, 2 e 2 entradas); REQ-003 redundante => 2.", "Texto literal.")
case("EX-26", [["analyze", "--json", "{IN}/EX05_virgula_requisito.json"]], {"exit": 0}, [L_EXIT],
     "Texto de uma decisão com requisito e ações: condições com par => 0.", "flag ∧ sw: pares de causa única.")
case("EX-27", [["verify", "--json", "{IN}/EX05_virgula_requisito.json"]], {"aviso_z3": True},
     ["L83: \"verify ... (usa o Z3)\"", "L73: \"avisam quando o executável não está instalado\""], "verify sem z3 no PATH avisa.", "Texto literal.", env="sem_z3")
case("EX-28", [["analyze", "A and B", "--exact"]], {"aviso_z3": True}, ["L63: \"necessário para --z3, --exact, --direct e verify\"", "L73"],
     "--exact sem z3 avisa.", "Texto literal.", env="sem_z3")
case("EX-29", [["analyze", "A and B", "--context", "A"]], {}, ["L119: \"No `verify`\""], "--context fora do verify: não diz se é erro.", "Omissão.", status="INDETERMINADO")
case("EX-30", [["analyze", "A and B", "--exact", "--direct"]], {}, ["L111", "L113"], "--exact com --direct: combinação não descrita.", "Omissão.", status="INDETERMINADO", env="z3")
case("EX-31", [["analyze", "--json", "{EX}/vm-decisoes.json", "--direct", "--mutation"]], {}, ["L113", "L117"],
     "Mutação no modo direto: não descrito.", "Omissão.", status="INDETERMINADO", env="z3")

# ---------------- Z3 ----------------
queries = {}
tv = lambda b: "true" if b else "false"
# QE01: valores concretos
G = "(and (< x 5) (<= y 5) (> z 5) (>= w 5) (not (= v 5)) (= u 5) (not (= mode idle)))"
for name, vals, exp in tests:
    decl = "(declare-datatypes () ((Mode idle choice)))\n" + "".join(f"(define-fun {k} () Int {v})\n" for k, v in vals.items() if k != "mode")
    decl += f"(define-fun mode () Mode {vals['mode']})\n"
    queries[f"QE01_{name}"] = f"; {name}: guarda = {exp}? unsat da negação => sim\n{decl}(assert (not (= {G} {tv(exp == 'T')})))\n(check-sat)\n"


def rows_query(tag, sort, conds, decl_vars):
    for bits in itertools.product([True, False], repeat=len(conds)):
        nm = "".join("T" if b else "F" for b in bits)
        body = "".join(f"(declare-const {v} {sort})\n" for v in decl_vars)
        body += "".join(f"(assert (= {c} {tv(b)}))\n" for c, b in zip(conds, bits))
        queries[f"{tag}_{sort}_{nm}"] = f"; {tag} linha {nm} ({sort})\n{body}(check-sat)\n"


rows_query("QE13", "Int", ["(> x (- 3))", "(< x 2)"], ["x"])
rows_query("QE13", "Real", ["(> x (- 3.0))", "(< x 2.0)"], ["x"])
rows_query("QE14", "Int", ["(> x 3)", "(<= y x)", "(> y 5)"], ["x", "y"])
rows_query("QE14", "Real", ["(> x 3.0)", "(<= y x)", "(> y 5.0)"], ["x", "y"])
rows_query("QE15", "Real", ["(>= t 10.5)", "(<= t 30.0)"], ["t"])
rows_query("QE16", "Int", ["(< x (- 5))", "(> x 5)"], ["x"])
rows_query("QE17", "Real", ["(> t 0.5)", "(< t 1.0)"], ["t"])
queries["QE18_fronteira"] = "; -2 satisfaz x > -3, -3 não, e todo inteiro > -3 é >= -2: unsat da negação\n(assert (not (and (> (- 2) (- 3)) (not (> (- 3) (- 3))) (forall ((x Int)) (=> (> x (- 3)) (>= x (- 2)))))))\n(check-sat)\n"
for x in ("A", "B", "C"):
    others = [n for n in ("A", "B", "C") if n != x]
    e = lambda s: f"(or (not A{s}) (and B{s} (not C{s})))"
    q = "".join(f"(declare-const {n}{s} Bool)\n" for n in ("A", "B", "C") for s in ("1", "2"))
    q += "".join(f"(assert (= {n}1 {n}2))\n" for n in others) + f"(assert (not (= {x}1 {x}2)))\n(assert (not (= {e('1')} {e('2')})))\n(check-sat)\n"
    queries[f"QE23_par_{x}"] = f"; not A or (B and not C): par de causa única para {x}\n" + q

summary = []
for name, text in sorted(queries.items()):
    qp = os.path.join(QD, name + ".smt2")
    open(qp, "w", encoding="utf-8", newline="\n").write(text)
    r = subprocess.run([Z3, "-T:60", qp], capture_output=True, text=True)
    open(os.path.join(OD, name + ".out"), "w", encoding="utf-8", newline="\n").write(r.stdout + r.stderr)
    summary.append(f"{name}\t{r.stdout.strip()}")
open(os.path.join(OD, "_resumo.tsv"), "w", encoding="utf-8", newline="\n").write("\n".join(summary) + "\n")
print("\n".join(summary))

oracle = {"condicao": "C1", "extensao": "01", "fonte_sha256": "91981FA0181E5CC1BC5A67DAAFC965BB82D6F8EB0A6D47EB58CE291A3EF5D33B",
          "unidade_de_contagem": "um caso = um ID", "casos": cases}
json.dump(oracle, open(os.path.join(BASE, "oraculo-extensao-01.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
print(len(cases), "casos;", sum(c["status"] == "DETERMINADO" for c in cases), "determinados")
