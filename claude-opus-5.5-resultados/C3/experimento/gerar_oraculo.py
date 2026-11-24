"""Gera entradas, consultas SMT-LIB, executa o Z3 independente e monta o oráculo C3.

Executado ANTES de qualquer leitura de código ou execução do SUT.
Uso: python -I gerar_oraculo.py <caminho do z3.exe>
"""
import itertools
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import exprlib as X  # noqa: E402

Z3 = sys.argv[1]
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EX = os.path.join(ROOT, "exemplos")
ENT = os.path.join(HERE, "entradas")
ZD = os.path.join(HERE, "z3")
os.makedirs(ENT, exist_ok=True)
os.makedirs(ZD, exist_ok=True)

z3log = []


def run_z3(qid, text, expect):
    """Grava a consulta, roda o Z3, guarda a saída e confere a sequência esperada."""
    p = os.path.join(ZD, f"{qid}.smt2")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    r = subprocess.run([Z3, "-T:60", p], capture_output=True, text=True)
    out = r.stdout
    with open(os.path.join(ZD, f"{qid}.out"), "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    answers = [ln.strip() for ln in out.splitlines() if ln.strip() in ("sat", "unsat", "unknown")]
    if "unknown" in answers or r.returncode not in (0, 1) or "error" in out:
        raise SystemExit(f"ERRO TÉCNICO Z3 em {qid}: {out}")
    if expect is not None and answers != expect:
        raise SystemExit(f"{qid}: esperado {expect}, Z3 deu {answers}")
    z3log.append({"id": qid, "arquivo": f"z3/{qid}.smt2", "saida": f"z3/{qid}.out",
                  "respostas": answers})
    return answers, out


# ---------------------------------------------------------------- tabelas-verdade
def truth_table(qid, expr):
    e = X.parse(expr)
    ats = X.atoms(e)
    names = {a: f"p{i}" for i, a in enumerate(ats)}
    lines = [f"; tabela-verdade de: {expr}", "; entradas (átomos distintos): " +
             "; ".join(f"{names[a]} = {a}" for a in ats)]
    lines += [f"(declare-const {names[a]} Bool)" for a in ats]
    combos = list(itertools.product([True, False], repeat=len(ats)))
    for c in combos:
        assign = " ".join(f"(= {names[a]} {'true' if v else 'false'})" for a, v in zip(ats, c))
        lines.append(f"(push)(assert (and {assign} {X.smt(e, names)}))(check-sat)(pop)")
    ans, _ = run_z3(qid, "\n".join(lines) + "\n", None)
    rows = []
    for c, a in zip(combos, ans):
        val = dict(zip(ats, c))
        out = a == "sat"
        assert out == X.ev(e, val), (expr, c)  # avaliador próprio concorda com o Z3
        rows.append({"entradas": {k: v for k, v in val.items()}, "saida": out})
    return {"expressao": expr, "entradas": ats, "combinacoes": len(combos), "linhas": rows}


def equivalence(qid, e1, e2):
    a, b = X.parse(e1), X.parse(e2)
    ats = X.atoms(a)
    assert set(ats) == set(X.atoms(b))
    names = {x: f"p{i}" for i, x in enumerate(ats)}
    t = [f"; equivalência: {e1}  ==  {e2}"] + [f"(declare-const {names[x]} Bool)" for x in ats]
    t.append(f"(assert (not (= {X.smt(a, names)} {X.smt(b, names)})))(check-sat)")
    run_z3(qid, "\n".join(t) + "\n", ["unsat"])


# --------------------------------------------------------------- pares (K7)
def pair_queries(qid, expr, constraint=None):
    """Para cada condição (expressão sem entrada repetida): existe par estrito
    de mascaramento, de causa única e par 'simplificado' (só a condição muda)?"""
    e = X.parse(expr)
    ats = X.atoms(e)
    assert len(ats) == len(X.atoms_occ(e)) or constraint == "allow-rep"
    lines = [f"; pares de independência de: {expr}" + (f" | restrição: {constraint}" if constraint and constraint != 'allow-rep' else "")]
    res = {}
    cons = X.parse(constraint) if constraint and constraint != "allow-rep" else None
    for cond in ats:
        for crit in ("mascaramento", "causa_unica", "simplificado"):
            nx = {a: f"x{i}" for i, a in enumerate(ats)}
            ny = {a: f"y{i}" for i, a in enumerate(ats)}
            nxf = dict(nx); nxf[cond] = f"(not {nx[cond]})"
            nyf = dict(ny); nyf[cond] = f"(not {ny[cond]})"
            decl = " ".join(f"(declare-const {v} Bool)" for v in list(nx.values()) + list(ny.values()))
            body = [f"(not (= {nx[cond]} {ny[cond]}))"]
            if cons is not None:
                body += [X.smt(cons, nx), X.smt(cons, ny)]
            gx, gy = X.smt(e, nx), X.smt(e, ny)
            if crit != "simplificado":
                body.append(f"(not (= {gx} {gy}))")
            if crit == "causa_unica":
                body += [f"(= {nx[a]} {ny[a]})" for a in ats if a != cond]
            if crit == "mascaramento":
                # a condição decide o resultado em cada linha do par
                body += [f"(not (= {gx} {X.smt(e, nxf)}))", f"(not (= {gy} {X.smt(e, nyf)}))"]
            lines.append(f"; condição {cond}, critério {crit}")
            lines.append(f"(push) {decl} (assert (and {' '.join(body)})) (check-sat) (pop)")
            res[(cond, crit)] = None
    ans, _ = run_z3(qid, "\n".join(lines) + "\n", None)
    out = {}
    for (k, a) in zip(res.keys(), ans):
        out.setdefault(k[0], {})[k[1]] = a
    return out


# ------------------------------------------------------------- fronteiras
def boundary(qid, var, op, k):
    p = lambda v: f"({op} {v} {k})"  # noqa: E731
    t = [f"; fronteira de {var} {op} {k} (inteiros): par adjacente (v, v+1) em que a comparação muda",
         "(declare-const v Int)", f"(assert (not (= {p('v')} {p('(+ v 1)')})))",
         "(check-sat)", "(get-value (v))"]
    ans, out = run_z3(qid + "_a", "\n".join(t) + "\n", ["sat"])
    v = int(out.split("(v ")[1].split(")")[0].replace("(- ", "-").strip())
    t2 = t[:3] + [f"(assert (not (= v {v})))", "(check-sat)"]
    run_z3(qid + "_unico", "\n".join(t2) + "\n", ["unsat"])
    return [v, v + 1]


# -------------------------------------------------------------- conflitos
def conflict(qid, comment, decls, reading_a, reading_b, extra=""):
    """Cada leitura isolada é sat; as duas juntas são unsat -> conflito relevante."""
    base = f"; {comment}\n{decls}\n{extra}\n"
    run_z3(qid + "_leituraA", base + f"(assert {reading_a})\n(check-sat)\n", ["sat"])
    run_z3(qid + "_leituraB", base + f"(assert {reading_b})\n(check-sat)\n", ["sat"])
    run_z3(qid + "_juntas", base + f"(assert {reading_a})\n(assert {reading_b})\n(check-sat)\n", ["unsat"])


def agree(qid, comment, decls, reading_a, reading_b, claim):
    """Leituras A e B juntas são satisfatíveis e ambas implicam a mesma expectativa."""
    base = f"; {comment}\n{decls}\n"
    run_z3(qid + "_juntas", base + f"(assert {reading_a})\n(assert {reading_b})\n(check-sat)\n", ["sat"])
    run_z3(qid + "_negacao", base + f"(assert {reading_a})\n(assert {reading_b})\n(assert (not {claim}))\n(check-sat)\n", ["unsat"])


# ================================================================= ENTRADAS
def wcsv(name, rows):
    p = os.path.join(ENT, name)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(rows) + "\n")


# check: suíte estrita completa de (A and B) or C
wcsv("check-completa.csv", ["decision,test,input,value,expected_outcome",
     *[f"D,{t},{i},{v},{o}" for t, vals, o in [("T1", "TTF", "T"), ("T2", "FTF", "F"), ("T3", "TFF", "F"), ("T4", "TFT", "T")]
       for i, v in zip("ABC", vals)]])
wcsv("check-um-teste.csv", ["decision,test,input,value,expected_outcome",
     "D,T1,A,T,T", "D,T1,B,T,T", "D,T1,C,F,T"])
wcsv("check-esperado-errado.csv", ["decision,test,input,value,expected_outcome",
     *[f"D,{t},{i},{v},{o}" for t, vals, o in [("T1", "TTF", "T"), ("T2", "FTF", "T"), ("T3", "TFF", "F"), ("T4", "TFT", "T")]
       for i, v in zip("ABC", vals)]])
wcsv("check-sem-coluna-value.csv", ["decision,test,input,expected_outcome", "D,T1,A,T", "D,T1,B,T", "D,T1,C,T"])
wcsv("check-sem-decision-expected.csv", ["test,input,value", "T1,A,T", "T1,B,T", "T1,C,F", "T2,A,F", "T2,B,T", "T2,C,F"])
wcsv("check-sem-mudanca-de-resultado.csv", ["decision,test,input,value,expected_outcome",
     "D,T1,A,T,T", "D,T1,B,F,T", "D,T1,C,T,T", "D,T2,A,F,T", "D,T2,B,F,T", "D,T2,C,T,T"])
# .mcdc
wcsv("erro-sintaxe.mcdc", ["# requisito com erro de sintaxe", "REQ-OK: A and B", "REQ-ERRO: (A and B"])
wcsv("sem-id.mcdc", ["REQ-001: A and B", "A or C"])
# JSON
with open(os.path.join(ENT, "invalido.json"), "w", encoding="utf-8") as f:
    f.write("{ isto não é json")
dup = {"system": "s", "inputs": [{"name": "a", "type": "bool"}, {"name": "b", "type": "bool"}],
       "decisions": [{"id": "s#1", "requirement": "R1", "guard": "a = true /\\ b = true", "actions": ["x := 1"]},
                     {"id": "s#1", "requirement": "R2", "guard": "a = true \\/ b = true", "actions": ["x := 2"]}]}
with open(os.path.join(ENT, "ids-repetidos.json"), "w", encoding="utf-8") as f:
    json.dump(dup, f, indent=2)

E20 = " and ".join(f"A{i}" for i in range(1, 21))
E21 = " and ".join(f"A{i}" for i in range(1, 22))
E13 = " and ".join(f"A{i}" for i in range(1, 14))
E26 = " or ".join(f"(A{i} and B{i})" for i in range(1, 14))
for n, e in [("e20.txt", E20), ("e21.txt", E21), ("e13.txt", E13), ("e26.txt", E26)]:
    with open(os.path.join(ENT, n), "w", encoding="utf-8", newline="\n") as f:
        f.write(e + "\n")

# ================================================================= Z3
TT = {}
for qid, e in [("Z01_tt_ABorC", "(A and B) or C"), ("Z01_tt_amp", "(A && B) || C"),
               ("Z01_tt_dfrs", "A /\\ B \\/ C"), ("Z01_tt_prec", "A or B and C"),
               ("Z01_tt_notA", "not A and B"), ("Z01_tt_bangA", "!A and B"),
               ("Z01_tt_cmp", "speed > 100 /\\ mode = idle"),
               ("Z01_tt_rep", "(A and B) or (not A and C)"),
               ("Z01_tt_req1", "(alarme_ativo and porta_aberta) or botao_emergencia"),
               ("Z01_tt_req2", "porta_fechada and not obstaculo"),
               ("Z01_tt_req3", "freio_acionado or (freio_acionado and pedal_pressionado)"),
               ("Z01_tt_mut", "A and (B or C)")]:
    TT[qid] = truth_table(qid, e)

equivalence("Z02_eq_amp", "(A && B) || C", "(A and B) or C")
equivalence("Z02_eq_dfrs", "A /\\ B \\/ C", "(A and B) or C")
equivalence("Z02_eq_prec", "A or B and C", "A or (B and C)")
equivalence("Z02_eq_not", "!A and B", "not A and B")

P_ABC = pair_queries("Z03_pares_ABorC", "(A and B) or C")
for c, d in P_ABC.items():
    assert d == {"mascaramento": "sat", "causa_unica": "sat", "simplificado": "sat"}, d
P_RED = pair_queries("Z04_pares_absorcao", "A or (A and B)", "allow-rep")
assert P_RED["B"]["mascaramento"] == "unsat" and P_RED["B"]["simplificado"] == "sat"
P_BLK = pair_queries("Z04_pares_bloqueio", "A and B", "not A or B")
assert P_BLK["B"]["mascaramento"] == "unsat" and P_BLK["B"]["simplificado"] == "sat"
P_CON = pair_queries("Z09_pares_restricao", "A or (B and C)", "not A or B")
P_20 = None  # 20 entradas: verificado por argumento (cadeia de "and"), ver Z10

# pares para "and" de n entradas: em A1 and ... and An, linha tudo-T e linha com Ai=F
# formam par de causa única (logo de mascaramento) para cada Ai.
t = ["; A1 and ... and A20: para cada i, (todas T) x (só Ai = F) é par de causa única"]
names = [f"A{i}" for i in range(1, 21)]
t += [f"(declare-const {n} Bool)" for n in names]
g = "(and " + " ".join(names) + ")"
for i, n in enumerate(names):
    allT = " ".join(f"(= {m} true)" for m in names)
    oneF = " ".join(f"(= {m} {'false' if m == n else 'true'})" for m in names)
    t.append(f"(push)(assert (and {allT} {g}))(check-sat)(pop)(push)(assert (and {oneF} (not {g})))(check-sat)(pop)")
run_z3("Z10_and20_pares", "\n".join(t) + "\n", ["sat"] * 40)

# restrição: linhas de A or (B and C) que satisfazem not A or B
TT_CONS = truth_table("Z09_tt_restricao", "(not A or B)")

# K6: combinações possíveis de speed > 100 or (speed > 50 and rain) (semântica usual de Int)
t = ["; viabilidade das combinações de (speed > 100, speed > 50, rain)", "(declare-const speed Int)", "(declare-const rain Bool)"]
feas = []
for c in itertools.product([True, False], repeat=3):
    a = " ".join([f"{'' if c[0] else '(not '}(> speed 100){'' if c[0] else ')'}",
                  f"{'' if c[1] else '(not '}(> speed 50){'' if c[1] else ')'}",
                  f"(= rain {'true' if c[2] else 'false'})"])
    t.append(f"(push)(assert (and {a}))(check-sat)(pop)")
    feas.append(c)
ans, _ = run_z3("Z07_viabilidade_speed", "\n".join(t) + "\n", None)
FEAS = [{"speed>100": c[0], "speed>50": c[1], "rain": c[2], "z3": a} for c, a in zip(feas, ans)]
assert sum(a == "unsat" for a in ans) == 2

# fronteiras
BND = {
    "speed>100": boundary("Z08_fronteira_speed_gt100", "speed", ">", 100),
    "speed>50": boundary("Z08_fronteira_speed_gt50", "speed", ">", 50),
    "x<=10": boundary("Z08_fronteira_x_le10", "x", "<=", 10),
    "y<5": boundary("Z08_fronteira_y_lt5", "y", "<", 5),
    "y>=7": boundary("Z08_fronteira_y_ge7", "y", ">=", 7),
    "the_voltage>80": boundary("Z08_fronteira_voltage_gt80", "the_voltage", ">", 80),
    "the_flashing_timer>=340": boundary("Z08_fronteira_timer_ge340", "the_flashing_timer", ">=", 340),
    "the_water_pressure>=9": boundary("Z08_fronteira_pressure_ge9", "the_water_pressure", ">=", 9),
    "the_water_pressure<10": boundary("Z08_fronteira_pressure_lt10", "the_water_pressure", "<", 10),
}
assert BND["speed>100"] == [100, 101] and BND["speed>50"] == [50, 51]

# check: avaliação das linhas dos CSVs
CHECK = {}
for name in ["check-completa", "check-um-teste", "check-esperado-errado", "check-sem-mudanca-de-resultado"]:
    rows = [r.split(",") for r in open(os.path.join(ENT, name + ".csv"), encoding="utf-8").read().split("\n")[1:] if r]
    tests = {}
    for d_, tt, i, v, o in rows:
        tests.setdefault(tt, {"val": {}, "esp": o})["val"][i] = v == "T"
    t = [f"; resultado da guarda (A and B) or C para cada teste de {name}.csv",
         "(declare-const A Bool)(declare-const B Bool)(declare-const C Bool)"]
    for tt, d_ in tests.items():
        a = " ".join(f"(= {k} {'true' if v else 'false'})" for k, v in d_["val"].items())
        t.append(f"(push)(assert (and {a} (or (and A B) C)))(check-sat)(pop)")
    ans, _ = run_z3(f"Z11_check_{name}", "\n".join(t) + "\n", None)
    CHECK[name] = {tt: {"valores": d_["val"], "esperado": d_["esp"] == "T", "guarda": a == "sat"}
                   for (tt, d_), a in zip(tests.items(), ans)}
assert [k for k, v in CHECK["check-esperado-errado"].items() if v["esperado"] != v["guarda"]] == ["T2"]
assert all(v["esperado"] == v["guarda"] for v in CHECK["check-completa"].values())

# exemplos/decisoes.json + testes.csv (entradas da fonte)
dec = json.load(open(os.path.join(EX, "decisoes.json"), encoding="utf-8"))
types = {i["name"]: i["type"] for i in dec["inputs"]}
g = {d["id"]: X.parse(d["guard"]) for d in dec["decisions"]}
tests = {}
for ln in open(os.path.join(EX, "testes.csv"), encoding="utf-8").read().splitlines():
    if not ln or ln.startswith("#") or ln.startswith("decision,"):
        continue
    d_, tt, i, v, o = ln.split(",")
    tests.setdefault((d_, tt), {"val": {}, "esp": o})["val"][i] = v
t = ["; guardas de exemplos/decisoes.json avaliadas nos testes de exemplos/testes.csv",
     "(declare-datatypes () ((Mode idle choice preparing_strong preparing_weak)))",
     "(declare-const the_system_mode Mode)(declare-const the_coin_sensor Bool)(declare-const the_coffee_request_button Bool)"]
G = {"the_coffee_machine_system#1": "(and (= the_system_mode idle) (= the_coin_sensor true))",
     "the_coffee_machine_system#3": "(or (and (= the_system_mode choice) (= the_coffee_request_button true)) (= the_coin_sensor true))"}
for (d_, tt), v in tests.items():
    a = " ".join(f"(= {k} {val})" for k, val in v["val"].items())
    t.append(f"(push)(assert (and {a} {G[d_]}))(check-sat)(pop) ; {d_} {tt}")
ans, _ = run_z3("Z12_decisoes_testes", "\n".join(t) + "\n", None)
DEC_TESTS = {}
for ((d_, tt), v), a in zip(tests.items(), ans):
    concrete = {k: X.eval_atom_concrete(at, v["val"], types) for k, at in [(x, x) for x in []]}
    py = X.ev(g[d_], {at: X.eval_atom_concrete(at, v["val"], types) for at in X.atoms(g[d_]) if at.split()[0] in v["val"]}) \
        if all(at.split()[0] in v["val"] for at in X.atoms(g[d_])) else None
    assert py is None or py == (a == "sat")
    DEC_TESTS[tt] = {"decisao": d_, "valores": v["val"], "esperado": v["esp"] == "T", "guarda": a == "sat"}
assert [k for k, v in DEC_TESTS.items() if v["esperado"] != v["guarda"]] == ["T4"]

# contagens dos sistemas de exemplo (entradas distintas = átomos distintos)
SYS = {}
for s in ["vm", "tis", "npp"]:
    d = json.load(open(os.path.join(EX, f"{s}-decisoes.json"), encoding="utf-8"))
    per = []
    for x in d["decisions"]:
        e = X.parse(x["guard"])
        per.append({"id": x["id"], "requisito": x.get("requirement"), "entradas": len(X.atoms(e)),
                    "ocorrencias": len(X.atoms_occ(e))})
    SYS[s] = {"decisoes": len(per), "combinacoes": sum(2 ** p["entradas"] for p in per),
              "entradas_distintas": sum(p["entradas"] for p in per),
              "ocorrencias": sum(p["ocorrencias"] for p in per),
              "com_repeticao": [p["id"] for p in per if p["ocorrencias"] != p["entradas"]], "por_decisao": per}
# Z3 confere as somas declaradas na regressão
t = ["; somas da tabela de regressão x contagens calculadas das entradas",
     "(declare-const vm Int)(declare-const tis Int)(declare-const npp Int)",
     f"(assert (= vm {SYS['vm']['combinacoes']}))(assert (= tis {SYS['tis']['combinacoes']}))(assert (= npp {SYS['npp']['combinacoes']}))",
     "(push)(assert (not (and (= vm 152) (= tis 268) (= npp 76) (= (+ vm tis npp) 496))))(check-sat)(pop)"]
run_z3("Z13_combinacoes_sistemas", "\n".join(t) + "\n", ["unsat"])
assert SYS["vm"]["com_repeticao"] == [] and SYS["npp"]["com_repeticao"] == [] and SYS["tis"]["com_repeticao"]
assert SYS["vm"]["entradas_distintas"] == 21 and SYS["npp"]["entradas_distintas"] == 29

# ---------------------------------------------------------- conflitos K1..K14
conflict("K01_contagem_condicoes", "K1: (A and B) or (not A and C): condições por ocorrência (4) x por variável (3)",
         "(declare-const ncond Int)", "(= ncond 4)", "(= ncond 3)")
agree("K01_sem_repeticao", "K1 sem repetição: (A and B) or C tem 3 ocorrências e 3 variáveis",
      "(declare-const ncond Int)(declare-const nocc Int)(declare-const nvar Int)(assert (= nocc 3))(assert (= nvar 3))",
      "(= ncond nocc)", "(= ncond nvar)", "(= ncond 3)")
conflict("K02_z3_ausente", "K2/K11: sem z3 no PATH, analyze simples roda?",
         "(declare-const roda Bool)", "roda", "(not roda)")
for nome, a, b in [("sucesso", "(= c 0)", "(= c 1)"), ("entrada_invalida", "(= c 1)", "(= c 0)"),
                   ("divergencia_check", "(= c 2)", "(not (= c 2))"), ("conflito_verify", "(= c 2)", "(not (= c 2))"),
                   ("sem_par_analyze", "(= c 2)", "(not (= c 2))")]:
    conflict(f"K03_codigo_{nome}", f"K3: código de saída ({nome}) – Uso x Interpretação definitiva",
             "(declare-const c Int)", a, b)
conflict("K04_csv_colunas", "K4: CSV de check sem decision/expected_outcome é aceito?",
         "(declare-const aceito Bool)", "aceito", "(not aceito)")
conflict("K05_truth_csv", "K5: truth-csv contém a tabela-verdade inteira?",
         "(declare-const tabela_inteira Bool)", "tabela_inteira", "(not tabela_inteira)")
conflict("K05_csv", "K5: csv contém a suíte (testes gerados)?",
         "(declare-const tem_suite Bool)", "tem_suite", "(not tem_suite)")
# K6: conjunto mantido = combinações sat (leitura A) x unsat (leitura B) no exemplo speed
nsat = sum(1 for f in FEAS if f["z3"] == "sat")
conflict("K06_viabilidade", "K6: número de combinações mantidas de speed>100 or (speed>50 and rain)",
         "(declare-const mantidas Int)", f"(= mantidas {nsat})", f"(= mantidas {8 - nsat})")
conflict("K07_criterio_par", "K7: B em A or (A and B) tem par? (estrito: unsat no Z04; simplificado: sat)",
         "(declare-const tem_par Bool)", "(not tem_par)", "tem_par")
conflict("K07_tamanho_suite", "K7/K8: tamanho da suíte de (A and B) or C (exemplo 4 x simplificado 2: TTT/FFF alterna todas)",
         "(declare-const n Int)", "(= n 4)", "(= n 2)")
conflict("K08_exata", "K8: exata (5) x gulosa (6) e 'gulosa sempre mínima'",
         "(declare-const g Int)(declare-const e Int)(declare-const m Int)(assert (<= m g))(assert (<= m e))",
         "(and (= e m) (= e 5) (= g 6))", "(= g m)")
conflict("K09_classificacao", "K9: condição sem par em qualquer cenário: redundante (1) x bloqueada (2)",
         "(declare-const rotulo Int)", "(= rotulo 1)", "(= rotulo 2)")
conflict("K10_z3_13", "K10: --z3 com 13 entradas: passa ao modo direto (1) x permanece na tabela (0)",
         "(declare-const modo Int)", "(= modo 1)", "(= modo 0)")
conflict("K10_direto_26", "K10: --direct com 26 entradas é aceito (limite 30) x só até 12",
         "(declare-const aceito Bool)", "aceito", "(not aceito)")
conflict("K14_parenteses", "K14: TIS: defeitos detectáveis que escapam (1 documentado x nenhum garantido)",
         "(declare-const escapam Int)", "(= escapam 1)", "(= escapam 0)")
conflict("K15_regressao_testes", "K7/K8: total de testes VM (26 documentado) depende do critério de par e da minimização",
         "(declare-const n Int)(declare-const ncond Int)(assert (= ncond 21))", "(= n 26)", "(< n 26)")

with open(os.path.join(HERE, "z3-evidencias.json"), "w", encoding="utf-8") as f:
    json.dump({"z3": subprocess.run([Z3, "--version"], capture_output=True, text=True).stdout.strip(),
               "consultas": z3log, "tabelas": TT, "tabela_restricao": TT_CONS,
               "pares": {"(A and B) or C": P_ABC, "A or (A and B)": P_RED,
                         "A and B | not A or B": P_BLK, "A or (B and C) | not A or B": P_CON},
               "viabilidade_speed": FEAS, "fronteiras": BND, "check": CHECK,
               "decisoes_testes": DEC_TESTS, "sistemas": SYS}, f, ensure_ascii=False, indent=1)
print("consultas Z3:", len(z3log))
