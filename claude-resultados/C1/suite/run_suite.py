"""Suíte C1: executa os casos do oráculo congelado contra a CLI MC/DC real, com o agente JaCoCo.

As expectativas vêm de experimento/oraculo.json (congelado); este arquivo só define COMO medir.
Uso:
  python -I run_suite.py --oraculo <oraculo.json> --classpath-file <runtime.classpath>
                         --rodada <dir> [--casos ID,ID,...]
Veredito por caso: PASSOU / FALHOU / INDETERMINADO / NAO_AVALIADO (erro técnico ou de medição).
"""
import argparse, csv, io, json, os, re, subprocess, sys, time

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
C1 = os.path.join(REPO, "claude-resultados", "C1")
EX = os.path.join(REPO, "exemplos").replace("\\", "/")
IN = os.path.join(C1, "experimento", "entradas").replace("\\", "/")
Z3_DIR = "C:/Users/User/AppData/Roaming/Python/bin"
AGENT = os.path.expanduser("~/.m2/repository/org/jacoco/org.jacoco.agent/0.8.16/org.jacoco.agent-0.8.16-runtime.jar").replace("\\", "/")
MAIN = "io.github.rvdomingos.mcdc.cli.Main"
TIMEOUT = 600


class Medicao(Exception):
    """A medida não pôde ser extraída de forma única (não é falha semântica)."""


def env_for(kind):
    env = dict(os.environ)
    parts = [p for p in env.get("PATH", "").split(os.pathsep) if "z3" not in p.lower() and p.replace("\\", "/").rstrip("/") != Z3_DIR]
    if kind in ("padrao", "z3"):
        parts.insert(0, Z3_DIR.replace("/", "\\"))
    env["PATH"] = os.pathsep.join(parts)
    return env


def run_cmd(args, env_kind, cp, rodada, outdir, idx):
    exec_file = os.path.join(rodada, "jacoco.exec").replace("\\", "/")
    # Correção 01 (rodada-02): stdout/stderr da JVM em UTF-8, como os arquivos gravados com -o;
    # no baseline a JVM usava Cp1252 no console e o runner decodificava como UTF-8 (perda em acentos).
    full = ["java", "-Dstdout.encoding=UTF-8", "-Dstderr.encoding=UTF-8",
            f"-javaagent:{AGENT}=destfile={exec_file},append=true", "-cp", cp, MAIN] + args
    t0 = time.time()
    try:
        p = subprocess.run(full, capture_output=True, env=env_for(env_kind), timeout=TIMEOUT)
        out, err, code = p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace"), p.returncode
    except subprocess.TimeoutExpired:
        out, err, code = "", f"TIMEOUT {TIMEOUT}s", None
    dt = time.time() - t0
    for ext, data in (("stdout", out), ("stderr", err)):
        with open(os.path.join(outdir, f"cmd{idx}.{ext}"), "w", encoding="utf-8", newline="\n") as f:
            f.write(data)
    return {"args": args, "exit": code, "stdout": out, "stderr": err, "segundos": round(dt, 2)}


def expand(args, outdir):
    return [a.replace("{EX}", EX).replace("{IN}", IN).replace("{OUT}", outdir.replace("\\", "/")) for a in args]


# ---------------- extratores ----------------
def csv_rows(text):
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        raise Medicao("CSV vazio")
    return rows


def truth_blocks(text):
    blocks = [b for b in text.strip().split("\n\n") if b.strip()]
    if not blocks:
        raise Medicao("truth-csv vazio")
    return [list(csv.DictReader(io.StringIO(b))) for b in blocks]


def suite_tests(text):
    rows = csv_rows(text)
    return rows, sorted({(r["decision"], r["test"]) for r in rows if " (" not in r["test"]})


def ev_bool(expr, values):
    # as fórmulas do oráculo usam and/or/not/parênteses, válidos em Python
    return bool(eval(expr, {"__builtins__": {}}, values))


def loads(text):
    try:
        return json.loads(text)
    except Exception as e:
        raise Medicao(f"JSON inválido: {e}")


def check(cond, msg, checks):
    checks.append({"ok": bool(cond), "verificacao": msg})


# ---------------- avaliação por caso ----------------
def avaliar(case, res, outdir):
    e = case["expectativa"]
    c = []
    first = res[0]
    if "exit" in e:
        for r in res if case["id"] in ("AN-06",) else [first]:
            check(r["exit"] == e["exit"], f"exit esperado {e['exit']}, observado {r['exit']} ({' '.join(r['args'][:2])})", c)
    if "testes_distintos" in e:
        _, tests = suite_tests(first["stdout"])
        check(len(tests) == e["testes_distintos"], f"testes distintos esperados {e['testes_distintos']}, observados {len(tests)}", c)
        if e.get("linhas_dados") == "testes_distintos * 3":
            rows = csv_rows(first["stdout"])
            check(len(rows) == len(tests) * 3, f"linhas de dados {len(rows)} = testes({len(tests)}) x 3", c)
    if "resultado_por_linha" in e or isinstance(e.get("linhas_dados"), int):
        for r in res:
            blocks = truth_blocks(r["stdout"])
            if len(blocks) != 1:
                raise Medicao("esperado 1 bloco de tabela")
            rows = blocks[0]
            if isinstance(e.get("linhas_dados"), int):
                check(len(rows) == e["linhas_dados"], f"linhas da tabela esperadas {e['linhas_dados']}, observadas {len(rows)}", c)
            if "resultado_por_linha" in e:
                bad = [row["row"] for row in rows
                       if ev_bool(e["resultado_por_linha"], {k: row[k] == "T" for k in ("A", "B", "C")}) != (row["outcome"] == "T")]
                check(not bad, f"resultado de cada linha = {e['resultado_por_linha']} (divergentes: {bad})", c)
            if e.get("primeira_linha_toda_verdadeira"):
                check(all(rows[0][k] == "T" for k in ("A", "B", "C")), f"primeira linha ({rows[0]['row']}) toda verdadeira", c)
            if "impossiveis" in e:
                cols = [k for k in rows[0] if k not in ("decision", "requirement", "row", "outcome", "feasible", "in_suite", "demonstrates", "concrete_values")]
                c100 = [k for k in cols if "100" in k]
                c50 = [k for k in cols if "50" in k and "100" not in k]
                if len(c100) != 1 or len(c50) != 1:
                    raise Medicao(f"colunas de comparação não identificadas: {cols}")
                imp = [row for row in rows if row["feasible"] == "F"]
                okset = all(row[c100[0]] == "T" and row[c50[0]] == "F" for row in imp)
                check(len(imp) == 2 and okset, f"impossíveis = 2 linhas com {c100[0]}=T e {c50[0]}=F (observadas {len(imp)}: {[r['row'] for r in imp]})", c)
    if e.get("json_valido"):
        try:
            json.loads(first["stdout"]); ok = True
        except Exception:
            ok = False
        check(ok, "stdout é JSON válido", c)
    if e.get("arquivo_igual_stdout_sem_o"):
        path = os.path.join(outdir, "AN-22.txt")
        content = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        check(content is not None and content.strip() != "", "arquivo -o criado e não vazio", c)
        check(content is not None and content == res[1]["stdout"], "conteúdo do arquivo = stdout sem -o", c)
        check(res[1]["stdout"].strip() not in first["stdout"] or not res[1]["stdout"].strip(), "relatório não mostrado na tela com -o", c)
    if e.get("valores_realizam_guarda"):
        rows = csv_rows(first["stdout"])
        bad, n = [], 0
        for r in rows:
            vals = dict(kv.split(" = ", 1) for kv in r["concrete_values"].split("; ") if kv)
            if "speed" not in vals or "rain" not in vals:
                raise Medicao(f"valores concretos incompletos: {r['concrete_values']!r}")
            s, rain = float(vals["speed"]), vals["rain"].strip().lower() in ("true", "t")
            g = (s > 100) or (s > 50 and rain)
            n += 1
            if g != (r["expected_outcome"] == "T"):
                bad.append((r["test"], r["concrete_values"], r["expected_outcome"]))
        check(n > 0 and not bad, f"guarda nos valores concretos = esperado ({n} linhas; divergentes {bad})", c)
    if "valores_fronteira_speed_incluem" in e:
        j = loads(first["stdout"])
        vals = set()
        for d in j["decisions"]:
            for b in d.get("boundaryTests", []):
                if "speed" in b["assignment"]:
                    vals.add(float(b["assignment"]["speed"]))
        want = set(float(x) for x in e["valores_fronteira_speed_incluem"])
        check(want <= vals, f"fronteiras de speed incluem {sorted(want)} (observadas {sorted(vals)})", c)
    if e.get("aviso_z3"):
        txt = (first["stdout"] + first["stderr"]).lower()
        check("z3" in txt, f"saída menciona Z3 (exit {first['exit']})", c)
    # ---- sistemas ----
    if "decisoes" in e:
        j = loads(first["stdout"])
        ds = j["decisions"]
        check(len(ds) == e["decisoes"], f"decisões {len(ds)} = {e['decisoes']}", c)
        nc = sum(len(d["conditions"]) for d in ds)
        check(nc == e["condicoes"], f"condições {nc} = {e['condicoes']}", c)
        comb = sum(d["truthTableRows"] for d in ds)
        check(comb == e["combinacoes"], f"combinações {comb} = {e['combinacoes']}", c)
        if not all("truthTable" in d for d in ds):
            raise Medicao("truthTable ausente no JSON")
        imp = sum(1 for d in ds for r in d["truthTable"] if not r["feasible"])
        check(imp == e["impossiveis"], f"impossíveis (JSON) {imp} = {e['impossiveis']}", c)
        blocks = truth_blocks(res[1]["stdout"])
        imp2 = sum(1 for b in blocks for r in b if r["feasible"] == "F")
        check(imp2 == e["impossiveis"], f"impossíveis marcadas (truth-csv) {imp2} = {e['impossiveis']}", c)
        nt = sum(len(d["minimalSuite"]) for d in ds)
        check(nt == e["testes"], f"testes {nt} = {e['testes']}", c)
        if e.get("testes_por_decisao_igual_condicoes_mais_1"):
            bad = [(d["id"], len(d["minimalSuite"]), len(d["conditions"])) for d in ds if len(d["minimalSuite"]) != len(d["conditions"]) + 1]
            check(not bad, f"testes = condições + 1 em cada decisão (divergentes {bad})", c)
        if e.get("requisitos_rastreados"):
            src = [a for a in first["args"] if a.endswith(".json")][0]
            orig = {d["id"]: d["requirement"] for d in json.load(open(src, encoding="utf-8"))["decisions"]}
            bad = [d["id"] for d in ds if orig.get(d["id"]) != d["requirement"]]
            check(not bad and len(orig) == len(ds), f"cada decisão ligada ao requisito de origem (divergentes {bad})", c)
    if "mutantes" in e:
        j = loads(first["stdout"])
        tot = eq = kill = 0
        for d in j["decisions"]:
            if "mutation" not in d:
                raise Medicao(f"{d['id']} sem bloco mutation")
            for f in d["mutation"]["faults"].values():
                tot += f["total"]; eq += f["equivalent"]; kill += f["killed"]
        check(tot == e["mutantes"], f"mutantes {tot} = {e['mutantes']}", c)
        check(eq == e["equivalentes"], f"equivalentes {eq} = {e['equivalentes']}", c)
        check(kill == e["pegos"], f"pegos {kill} = {e['pegos']}", c)
    if "conflitos" in e:
        j = loads(res[-1]["stdout"])
        n = len(j["conflicts"])
        check(n == e["conflitos"], f"conflitos {n} = {e['conflitos']}", c)
    if "testes" in e and "decisoes" not in e:
        j = loads(first["stdout"])
        nt = sum(len(d["minimalSuite"]) for d in j["decisions"])
        check(nt == e["testes"], f"testes {nt} = {e['testes']}", c)
    if e.get("cobertura_e_diagnostico_iguais"):
        a, b = loads(res[0]["stdout"]), loads(res[1]["stdout"])
        def diag(j):
            return {d["id"]: (d["complete"], sorted(d["uncoveredConditions"]), sorted((u["condition"], u["reason"]) for u in d["uncovered"])) for d in j["decisions"]}
        da, db = diag(a), diag(b)
        diff = {k: (da.get(k), db.get(k)) for k in set(da) | set(db) if da.get(k) != db.get(k)}
        check(not diff, f"direto = tabela completa em cobertura/diagnóstico (diferenças {diff})", c)
    # ---- medições acrescentadas para a extensão 01 ----
    if "stderr_contem" in e:
        check(e["stderr_contem"] in first["stderr"], f"stderr contém {e['stderr_contem']!r}: {first['stderr'].strip()[:200]!r}", c)
    if "csv_coluna_igual" in e:
        rows = csv_rows(first["stdout"])
        col, val = e["csv_coluna_igual"]["coluna"], e["csv_coluna_igual"]["valor"]
        bad = [r[col] for r in rows if r[col] != val]
        check(not bad, f"coluna {col} = {val!r} em todas as {len(rows)} linhas (divergentes {bad[:3]})", c)
    if "impossiveis_formula" in e:
        rows = truth_blocks(first["stdout"])[0]
        meta = ("decision", "requirement", "row", "outcome", "feasible", "in_suite", "demonstrates", "concrete_values")
        cols = [k for k in rows[0] if k not in meta]
        alias = {}
        for a_, sub in e["impossiveis_formula"]["colunas"].items():
            m = [k for k in cols if sub in k]
            if len(m) != 1:
                raise Medicao(f"coluna para {sub!r} não identificada em {cols}")
            alias[a_] = m[0]
        f = e["impossiveis_formula"]["impossivel_sse"]
        bad = [r["row"] for r in rows if ev_bool(f, {a_: r[k] == "T" for a_, k in alias.items()}) != (r["feasible"] == "F")]
        check(not bad, f"linha impossível sse {f} com {alias} (divergentes {bad}; impossíveis observadas {[r['row'] for r in rows if r['feasible'] == 'F']})", c)
    if "guarda_py" in e:
        rows = csv_rows(first["stdout"])
        bad = []
        for r in rows:
            vals = {}
            for kv in [x for x in r["concrete_values"].split("; ") if x]:
                k, v = kv.split(" = ", 1)
                vals[k] = (v.lower() == "true") if v.lower() in ("true", "false") else float(v)
            if not vals:
                raise Medicao(f"linha sem valores concretos: {r}")
            if ev_bool(e["guarda_py"], vals) != (r["expected_outcome"] == "T"):
                bad.append((r["test"], r["concrete_values"], r["expected_outcome"]))
        check(not bad, f"guarda {e['guarda_py']} nos valores concretos = esperado em {len(rows)} linhas (divergentes {bad})", c)
    if "fronteiras_incluem" in e:
        j = loads(first["stdout"])
        var = e["fronteiras_incluem"]["var"]
        vals = {float(b["assignment"][var]) for d in j["decisions"] for b in d.get("boundaryTests", []) if var in b["assignment"]}
        want = {float(x) for x in e["fronteiras_incluem"]["valores"]}
        check(want <= vals, f"fronteiras de {var} incluem {sorted(want)} (observadas {sorted(vals)})", c)
    if "pares_max" in e:
        j = loads(first["stdout"])
        cond, mx = e["pares_max"]["condicao"], e["pares_max"]["max"]
        n = len(j["decisions"][0]["independencePairs"][cond])
        check(0 < n <= mx, f"pares guardados para {cond}: {n} (0 < n <= {mx})", c)
    if "blocos_linhas" in e:
        blocks = truth_blocks(first["stdout"])
        check([len(b) for b in blocks] == e["blocos_linhas"], f"blocos com cabeçalho e linhas {e['blocos_linhas']} (observados {[len(b) for b in blocks]})", c)
    if not c:
        raise Medicao("nenhuma verificação definida para a expectativa")
    return c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--oraculo", required=True)
    ap.add_argument("--classpath-file", required=True)
    ap.add_argument("--rodada", required=True)
    ap.add_argument("--casos", default="")
    ap.add_argument("--entradas", default="", help="pasta de entradas montadas ({IN}); padrão: experimento/entradas")
    a = ap.parse_args()
    global IN
    if a.entradas:
        IN = os.path.abspath(a.entradas).replace("\\", "/")
    cp = open(a.classpath_file, encoding="utf-8").read().strip()
    oracle = json.load(open(a.oraculo, encoding="utf-8"))
    os.makedirs(a.rodada, exist_ok=True)
    only = set(x for x in a.casos.split(",") if x)
    summary = []
    for case in oracle["casos"]:
        if only and case["id"] not in only:
            continue
        outdir = os.path.join(a.rodada, "casos", case["id"])
        os.makedirs(outdir, exist_ok=True)
        cmds = [expand(x, outdir) for x in case["comandos"]]
        # medição adicional (não altera a expectativa): verify em JSON para contar conflitos
        if "conflitos" in case["expectativa"]:
            cmds.append(cmds[0] + ["--format", "json"])
        res = [run_cmd(x, case["ambiente"], cp, a.rodada, outdir, i + 1) for i, x in enumerate(cmds)]
        tech = [r for r in res if r["exit"] is None]
        checks, nota = [], ""
        if case["status"] == "INDETERMINADO":
            veredito = "INDETERMINADO"
            nota = "diagnóstico sem expectativa: " + "; ".join(f"exit={r['exit']}" for r in res)
        elif tech:
            veredito, nota = "NAO_AVALIADO", "timeout"
        else:
            try:
                checks = avaliar(case, res, outdir)
                veredito = "PASSOU" if all(x["ok"] for x in checks) else "FALHOU"
            except (Medicao, KeyError, IndexError, ValueError, TypeError) as ex:
                veredito, nota = "NAO_AVALIADO", f"medição: {type(ex).__name__}: {ex}"
        rec = {"id": case["id"], "veredito": veredito, "nota": nota, "verificacoes": checks,
               "comandos": [{"args": r["args"], "exit": r["exit"], "segundos": r["segundos"]} for r in res]}
        with open(os.path.join(outdir, "resultado.json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(rec, f, ensure_ascii=False, indent=2)
        summary.append(rec)
        print(f"{case['id']}\t{veredito}\t{nota}\t" + " | ".join(x["verificacao"] for x in checks if not x["ok"]), flush=True)
    with open(os.path.join(a.rodada, "resultados.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    counts = {}
    for r in summary:
        counts[r["veredito"]] = counts.get(r["veredito"], 0) + 1
    print("TOTAL", counts)


if __name__ == "__main__":
    main()
