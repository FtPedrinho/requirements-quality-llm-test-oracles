"""Suite C0 contra a ferramenta MC/DC real (caixa-preta pela CLI).

Le as expectativas do oraculo congelado (experimento/oraculo/oraculo.json), executa cada caso com
o agente JaCoCo, julga PASSOU/FALHOU (determinados) ou registra a observacao (indeterminados).
Os adaptadores abaixo so EXTRAEM valores das saidas; os valores esperados vem do oraculo.

Uso: python -I executar_suite.py <rodada>   (ex.: rodada-1)
"""
import json, os, re, shutil, subprocess, sys, time, hashlib, itertools

HERE = os.path.dirname(os.path.abspath(__file__))
C0 = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(C0))
CFG = json.load(open(os.path.join(HERE, "config.json"), encoding="utf-8"))
ORACLE_PATH = os.environ.get("ORACULO", os.path.join(C0, "experimento", "oraculo", "oraculo.json"))
IN_DIR = os.path.join(C0, "experimento", "oraculo", "entradas")
INX_DIR = os.path.join(C0, "experimento", "extensao-1", "entradas")
MAIN = "io.github.rvdomingos.mcdc.cli.Main"

# ----------------------------------------------------------------------------- avaliador proprio
TOK = re.compile(r"\s*(\(|\)|&&|\|\||/\\|\\/|!=|==|<=|>=|=|<|>|!|-?\d+(?:\.\d+)?|[A-Za-z_][A-Za-z0-9_#]*)")
CMP = {"=", "==", "!=", "<", "<=", ">", ">="}

def tokenize(s):
    pos, out = 0, []
    s = s.strip()
    while pos < len(s):
        m = TOK.match(s, pos)
        if not m: raise ValueError(f"token invalido em {s[pos:]!r}")
        out.append(m.group(1)); pos = m.end()
        while pos < len(s) and s[pos].isspace(): pos += 1
    return out

class Parser:
    def __init__(self, s): self.t = tokenize(s); self.i = 0
    def peek(self): return self.t[self.i] if self.i < len(self.t) else None
    def take(self): self.i += 1; return self.t[self.i - 1]
    def parse(self):
        e = self.or_(); assert self.peek() is None, "sobra"; return e
    def or_(self):
        xs = [self.and_()]
        while self.peek() in ("or", "||", "\\/"): self.take(); xs.append(self.and_())
        return xs[0] if len(xs) == 1 else ("or", xs)
    def and_(self):
        xs = [self.un()]
        while self.peek() in ("and", "&&", "/\\"): self.take(); xs.append(self.un())
        return xs[0] if len(xs) == 1 else ("and", xs)
    def un(self):
        p = self.peek()
        if p in ("not", "!"): self.take(); return ("not", self.un())
        if p == "(":
            self.take(); e = self.or_(); assert self.take() == ")"; return e
        a = self.take()
        if self.peek() in CMP:
            op = self.take(); b = self.take(); return ("cmp", a, op, b)
        return ("var", a)

def label_leaves(e):
    """Rotula cada aparicao: nome, ou nome#k quando a entrada aparece mais de uma vez."""
    leaves = []
    def walk(x):
        if x[0] in ("var", "cmp"): leaves.append(x)
        elif x[0] == "not": walk(x[1])
        else: [walk(y) for y in x[1]]
    walk(e)
    key = lambda l: l[1] if l[0] == "var" else f"{l[1]} {l[2]} {l[3]}"
    counts = {}
    for l in leaves: counts[key(l)] = counts.get(key(l), 0) + 1
    seen, labels = {}, {}
    for l in leaves:
        k = key(l); seen[k] = seen.get(k, 0) + 1
        labels[id(l)] = (k if counts[k] == 1 else f"{k}#{seen[k]}", k)
    return labels

def ev(e, env, labels=None, flip=None):
    t = e[0]
    if t in ("var", "cmp"):
        lab, inp = labels[id(e)] if labels else (None, None)
        v = env[inp if labels else (e[1] if t == "var" else f"{e[1]} {e[2]} {e[3]}")]
        return (not v) if (flip is not None and lab == flip) else v
    if t == "not": return not ev(e[1], env, labels, flip)
    if t == "and": return all(ev(x, env, labels, flip) for x in e[1])
    return any(ev(x, env, labels, flip) for x in e[1])

def ev_concrete(e, asg):
    t = e[0]
    if t == "var": return parse_bool(asg[e[1]])
    if t == "cmp": return compare(asg.get(e[1], e[1]), e[2], asg.get(e[3], e[3]))
    if t == "not": return not ev_concrete(e[1], asg)
    if t == "and": return all(ev_concrete(x, asg) for x in e[1])
    return any(ev_concrete(x, asg) for x in e[1])

def parse_bool(s):
    s = str(s).strip().lower()
    if s in ("true", "t"): return True
    if s in ("false", "f"): return False
    raise ValueError(f"booleano invalido {s!r}")

def num(s):
    try: return float(s)
    except Exception: return None

def compare(a, op, b):
    a, b = str(a), str(b)
    na, nb = num(a), num(b)
    if na is not None and nb is not None: a, b = na, nb
    elif a.lower() in ("true", "false") or b.lower() in ("true", "false"): a, b = a.lower(), b.lower()
    return {"=": a == b, "==": a == b, "!=": a != b, "<": a < b, "<=": a <= b, ">": a > b, ">=": a >= b}[op]

def has_valid_pairs(expr, tests, unique):
    ast = Parser(expr).parse(); labels = label_leaves(ast)
    conds = {lab: inp for lab, inp in labels.values()}
    missing = []
    for lab, inp in conds.items():
        ok = False
        for t1, t2 in itertools.combinations(tests, 2):
            if t1[inp] == t2[inp]: continue
            f1, f2 = ev(ast, t1, labels), ev(ast, t2, labels)
            if f1 == f2: continue
            if f1 == ev(ast, t1, labels, lab) or f2 == ev(ast, t2, labels, lab): continue
            if unique and any(t1[k] != t2[k] for k in t1 if k != inp): continue
            ok = True; break
        if not ok: missing.append(lab)
    return missing

# ----------------------------------------------------------------------------- execucao
def classpath():
    cls = os.path.join(CFG["sut_build"], "classes")
    return ";".join(os.path.join(cls, m) for m in CFG["modules"]) + ";" + CFG["jackson_cp"]

def run_cli(args, z3, outdir, exec_file):
    env = dict(os.environ)
    paths = [p for p in env.get("PATH", "").split(os.pathsep) if p and os.path.normcase(os.path.abspath(p)) != os.path.normcase(CFG["z3_dir"])]
    if z3: paths.insert(0, CFG["z3_dir"])
    env["PATH"] = os.pathsep.join(paths)
    args = [a.replace("{INX}", INX_DIR).replace("{IN}", IN_DIR).replace("{OUT}", outdir) for a in args]
    agent = f"-javaagent:{CFG['jacoco_agent']}=destfile={exec_file},append=true,includes=io.github.rvdomingos.mcdc.*"
    cmd = [CFG["java"], "-Dfile.encoding=UTF-8", "-Dstdout.encoding=UTF-8", "-Dstderr.encoding=UTF-8", agent, "-cp", classpath(), MAIN] + args
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=REPO, env=env, capture_output=True, timeout=CFG["timeout_s"])
        return {"args": args, "z3": z3, "exit": p.returncode, "stdout": p.stdout.decode("utf-8", "replace"),
                "stderr": p.stderr.decode("utf-8", "replace"), "secs": round(time.time() - t0, 2), "tech_error": None}
    except subprocess.TimeoutExpired:
        return {"args": args, "z3": z3, "exit": None, "stdout": "", "stderr": "", "secs": CFG["timeout_s"], "tech_error": "timeout"}

def load_json(obs):
    return json.loads(obs["stdout"])

def suite_tests(dec):
    return [dict(t["values"]) for t in dec["minimalSuite"]]

def truth_csv(text):
    blocks, cur = [], None
    for line in text.splitlines():
        if not line.strip(): cur = None; continue
        cells = next(iter(__import__("csv").reader([line])))
        if cells[:3] == ["decision", "requirement", "row"]:
            cur = {"header": cells, "rows": []}; blocks.append(cur); continue
        cur["rows"].append(dict(zip(cur["header"], cells)))
    return blocks

def truth_inputs(block):
    h = block["header"]; return h[3:h.index("outcome")]

# ----------------------------------------------------------------------------- julgamento
def judge(case, obs, aux):
    exp = case["esperado"]; checks = []
    def chk(name, ok, detail=""): checks.append({"assercao": name, "ok": bool(ok), "detalhe": detail})
    combined = obs["stdout"] + "\n" + obs["stderr"]
    if "exit" in exp: chk("exit", obs["exit"] == exp["exit"], f"esperado {exp['exit']}, obtido {obs['exit']}")
    if "exit_any_of" in exp: chk("exit_any_of", obs["exit"] in exp["exit_any_of"], f"obtido {obs['exit']}")
    if "contains" in exp:
        for s in exp["contains"]: chk(f"contains:{s}", s.lower() in combined.lower())
    if "contains_any" in exp: chk("contains_any", any(s.lower() in combined.lower() for s in exp["contains_any"]))
    if "file_written" in exp:
        path = exp["file_written"].replace("{OUT}", obs["outdir"])
        content = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
        chk("file_written", len(content.strip()) > 0 and content.strip() not in obs["stdout"], f"bytes={len(content)}")
    json_keys = {"json_valid", "tests", "pairs_valid", "conditions", "all_paired", "unpaired", "impossible",
                 "concrete_ok", "boundary_values", "mutation_types_subset", "totals", "conflicts", "n_conditions",
                 "n_decisions", "suite_feasible_under", "same_pairing_as", "unpaired_by_reason"}
    if json_keys & set(exp):
        try:
            j = load_json(obs); chk("json_valid", True)
        except Exception as ex:
            chk("json_valid", False, f"saida nao e JSON: {ex}"); return checks
        decs = j.get("decisions") if isinstance(j.get("decisions"), list) else None
        d0 = decs[0] if decs else None
        expr = case["args"][1] if len(case["args"]) > 1 and not case["args"][1].startswith("-") else None
        if "tests" in exp: chk("tests", len(d0["minimalSuite"]) == exp["tests"], f"obtido {len(d0['minimalSuite'])}")
        if "n_decisions" in exp: chk("n_decisions", len(decs) == exp["n_decisions"], f"obtido {len(decs)}")
        if "conditions" in exp:
            got = [c["label"] for c in d0["conditions"]]
            chk("conditions", sorted(got) == sorted(exp["conditions"]), f"obtido {got}")
        if "n_conditions" in exp: chk("n_conditions", len(d0["conditions"]) == exp["n_conditions"], f"obtido {len(d0['conditions'])}")
        if "all_paired" in exp:
            unc = [c for d in decs for c in d["uncoveredConditions"]]
            chk("all_paired", (not unc) == exp["all_paired"], f"sem par: {unc}")
        if "unpaired" in exp:
            got = {u["condition"]: {"REDUNDANT": "redundante", "INFEASIBLE": "bloqueada"}.get(u["reason"], u["reason"]) for u in d0["uncovered"]}
            chk("unpaired", got == exp["unpaired"], f"obtido {got}")
        if "unpaired_by_reason" in exp:
            got = {}
            for u in d0["uncovered"]:
                k = {"REDUNDANT": "redundante", "INFEASIBLE": "bloqueada"}.get(u["reason"], u["reason"]); got[k] = got.get(k, 0) + 1
            chk("unpaired_by_reason", got == exp["unpaired_by_reason"], f"obtido {got}")
        if "impossible" in exp:
            imp = sum(1 for r in d0["truthTable"] if not r["feasible"])
            chk("impossible", imp == exp["impossible"], f"obtido {imp}")
        if "pairs_valid" in exp:
            miss = has_valid_pairs(expr, suite_tests(d0), exp["pairs_valid"] == "unique")
            chk(f"pairs_valid:{exp['pairs_valid']}", not miss, f"sem par valido na suite: {miss}")
        if "suite_feasible_under" in exp:
            k = Parser(exp["suite_feasible_under"]).parse()
            bad = [t for t in suite_tests(d0) if not ev(k, t)]
            chk("suite_feasible", not bad, f"testes impossiveis na suite: {bad}")
        if "concrete_ok" in exp:
            problems = []
            for d in decs:
                g = Parser(d["guard"]).parse(); lab = label_leaves(g)
                preds = {i["name"]: i for i in d["inputs"]}
                for t in d["minimalSuite"]:
                    asg = t.get("assignment") or {}
                    if not asg: problems.append(f"{t['vector']}: sem valores concretos"); continue
                    for name, val in t["values"].items():
                        p = preds.get(name, {})
                        real = compare(asg.get(p["variable"], p["variable"]), p["operator"], asg.get(str(p["value"]), p["value"])) if "operator" in p else parse_bool(asg[name])
                        if real != val: problems.append(f"{t['vector']}: {name} declarado {val}, valores dao {real}")
                    if ev_concrete(g, asg) != t["outcome"]: problems.append(f"{t['vector']}: esperado {t['outcome']} != guarda")
            chk("concrete_ok", not problems, "; ".join(problems[:5]))
        if "boundary_values" in exp:
            for var, vals in exp["boundary_values"].items():
                got = sorted({num(b["assignment"][var]) for b in d0.get("boundaryTests", []) if var in b["assignment"]})
                chk(f"boundary:{var}", all(float(v) in got for v in vals), f"obtido {got}")
        if "mutation_types_subset" in exp:
            kinds = set(d0["mutation"]["faults"]) if d0.get("mutation") else set()
            chk("mutation_types", kinds and kinds <= set(exp["mutation_types_subset"]), f"obtido {sorted(kinds)}")
        if "totals" in exp:
            got = {"requirements": len({d["requirement"] for d in decs}),
                   "conditions": sum(len(d["conditions"]) for d in decs),
                   "combinations": sum(d["truthTableRows"] for d in decs),
                   "impossible": sum(1 for d in decs for r in d.get("truthTable", []) if not r["feasible"]),
                   "tests": sum(len(d["minimalSuite"]) for d in decs),
                   "mutants": sum(f["total"] for d in decs if d.get("mutation") for f in d["mutation"]["faults"].values()),
                   "equivalent": sum(f["equivalent"] for d in decs if d.get("mutation") for f in d["mutation"]["faults"].values()),
                   "killed": sum(f["killed"] for d in decs if d.get("mutation") for f in d["mutation"]["faults"].values())}
            for k, v in exp["totals"].items(): chk(f"totals:{k}", got[k] == v, f"esperado {v}, obtido {got[k]}")
        if "conflicts" in exp: chk("conflicts", len(j["conflicts"]) == exp["conflicts"], f"obtido {len(j['conflicts'])}")
        if "same_pairing_as" in exp:
            other = json.loads(aux["same_pairing_as"]["stdout"])
            a = {d["id"]: sorted(d["uncoveredConditions"]) for d in decs}
            b = {d["id"]: sorted(d["uncoveredConditions"]) for d in other["decisions"]}
            chk("same_pairing_as", a == b, f"direto {a} x tabela {b}")
    if "exit_same_as" in exp: chk("exit_same_as", obs["exit"] == aux["exit_same_as"]["exit"], f"{obs['exit']} x {aux['exit_same_as']['exit']}")
    if any(k in exp for k in ("truth_rows", "row0_all_true", "truth_outputs_correct", "impossible_rows", "same_truth_as")):
        blocks = truth_csv(obs["stdout"]); b = blocks[0]; ins = truth_inputs(b)
        if "truth_rows" in exp: chk("truth_rows", len(b["rows"]) == exp["truth_rows"], f"obtido {len(b['rows'])}")
        if "row0_all_true" in exp: chk("row0_all_true", all(b["rows"][0][i] == "T" for i in ins), str(b["rows"][0]))
        if "truth_outputs_correct" in exp:
            ast = Parser(case["args"][1]).parse()
            bad = [r["row"] for r in b["rows"] if ev(ast, {i: r[i] == "T" for i in ins}) != (r["outcome"] == "T")]
            chk("truth_outputs", not bad, f"linhas erradas {bad}")
        if "impossible_rows" in exp:
            got = sorted([{i: r[i] == "T" for i in ins} for r in b["rows"] if r["feasible"] == "F"], key=str)
            chk("impossible_rows", got == sorted(exp["impossible_rows"], key=str), f"obtido {got}")
        if "same_truth_as" in exp:
            ob = truth_csv(aux["same_truth_as"]["stdout"])[0]; oi = truth_inputs(ob)
            proj = lambda blk, ii: [tuple([r[i] for i in ii] + [r["outcome"], r["feasible"]]) for r in blk["rows"]]
            chk("same_truth_as", ins == oi and proj(b, ins) == proj(ob, oi), f"entradas {ins} x {oi}")
    if any(k in exp for k in ("csv_rows", "csv_outcome_correct")):
        import csv as _csv
        rows = list(_csv.DictReader(obs["stdout"].splitlines()))
        if "csv_rows" in exp: chk("csv_rows", len(rows) == exp["csv_rows"], f"obtido {len(rows)}")
        if "csv_outcome_correct" in exp:
            ast = Parser(exp["csv_outcome_correct"]).parse(); by = {}
            for r in rows: by.setdefault(r["test"], {})[r["input"]] = (r["value"] == "T", r["expected_outcome"] == "T")
            bad = [t for t, m in by.items() if ev(ast, {k: v[0] for k, v in m.items()}) != list(m.values())[0][1]]
            chk("csv_outcome", not bad, f"testes errados {bad}")
    return checks

def main():
    rodada = sys.argv[1]
    rdir = os.path.join(C0, "resultados", rodada)
    if os.path.exists(rdir): sys.exit(f"{rdir} ja existe; nao sobrescrever rodadas")
    os.makedirs(os.path.join(rdir, "saidas"))
    exec_file = os.path.join(rdir, "jacoco.exec")
    oracle = json.load(open(ORACLE_PATH, encoding="utf-8"))
    results = []
    for case in oracle["casos"]:
        outdir = os.path.join(rdir, "saidas", case["id"]); os.makedirs(outdir)
        obs = run_cli(case["args"], case["z3"], outdir, exec_file); obs["outdir"] = outdir
        aux = {}
        for k in ("same_truth_as", "exit_same_as", "same_pairing_as"):
            if k in case["esperado"]:
                key = json.dumps(case["esperado"][k])
                aux[k] = next((v for v in aux.values() if v.get("_key") == key), None) or run_cli(case["esperado"][k], case["z3"], outdir, exec_file)
                aux[k]["_key"] = key
        for name, o in [("principal", obs)] + list(aux.items()):
            with open(os.path.join(outdir, f"{name}.stdout.txt"), "w", encoding="utf-8") as f: f.write(o["stdout"])
            with open(os.path.join(outdir, f"{name}.stderr.txt"), "w", encoding="utf-8") as f: f.write(o["stderr"])
        rec = {"id": case["id"], "status_oraculo": case["status"], "args": obs["args"], "z3": case["z3"],
               "exit": obs["exit"], "segundos": obs["secs"]}
        tech = obs["tech_error"] or next((a["tech_error"] for a in aux.values() if a["tech_error"]), None)
        if tech:
            rec["resultado"] = "ERRO_TECNICO"; rec["detalhe"] = tech
        elif case["status"] == "INDETERMINADO":
            rec["resultado"] = "INDETERMINADO"
            rec["observacao"] = (obs["stdout"] + obs["stderr"]).strip()[:300]
        else:
            try:
                checks = judge(case, obs, aux)
                rec["assercoes"] = checks
                rec["resultado"] = "PASSOU" if all(c["ok"] for c in checks) else "FALHOU"
            except Exception as ex:
                rec["resultado"] = "ERRO_TECNICO"; rec["detalhe"] = f"adaptador: {type(ex).__name__}: {ex}"
        results.append(rec)
        print(f"{rec['id']:8} {rec['resultado']:13} exit={rec['exit']} {rec['segundos']}s", flush=True)
    summary = {r: sum(1 for x in results if x["resultado"] == r) for r in ("PASSOU", "FALHOU", "INDETERMINADO", "ERRO_TECNICO")}
    json.dump({"rodada": rodada, "resumo": summary, "casos": results}, open(os.path.join(rdir, "resultados.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(summary)

if __name__ == "__main__":
    main()
