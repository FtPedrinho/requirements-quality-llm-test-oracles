"""Consultas SMT-LIB da extensao-1 do C0 (Z3 independente, sem usar o SUT)."""
import itertools, json, os, subprocess
Z3 = os.path.expanduser(r"~\AppData\Roaming\Python\bin\z3.exe")
HERE = os.path.dirname(os.path.abspath(__file__)); Q = os.path.join(HERE, "consultas"); os.makedirs(Q, exist_ok=True)
R = []

def run(qid, txt, expect, note):
    p = os.path.join(Q, qid + ".smt2"); open(p, "w").write(txt)
    out = subprocess.run([Z3, "-smt2", "-T:60", p], capture_output=True, text=True).stdout.strip()
    open(os.path.join(Q, qid + ".out"), "w").write(out + "\n")
    R.append({"id": qid, "esperado": expect, "obtido": out.splitlines()[0], "ok": out.splitlines()[0] == expect, "nota": note})

def rows(prefix, decl, atoms, imp, note):
    for bits in itertools.product([True, False], repeat=len(atoms)):
        tag = "".join("T" if b else "F" for b in bits)
        lits = " ".join(a if b else f"(not {a})" for a, b in zip(atoms, bits))
        exp = "unsat" if imp(bits) else "sat"
        run(f"{prefix}-linha-{tag}", f"{decl}(assert (and {lits}))\n(check-sat)\n", exp, note)

def pairs(prefix, decl_fn, atoms_fn, f, note, expect):
    """par de mascaramento por condicao i: t1,t2 viaveis, ci difere, f difere, ci decide em t1 e t2."""
    for i, exp in enumerate(expect):
        a1, a2 = atoms_fn("t1"), atoms_fn("t2")
        def fl(a, k): return [f"(not {x})" if j == k else x for j, x in enumerate(a)]
        body = (f"(and (distinct {a1[i]} {a2[i]}) (distinct {f(a1)} {f(a2)}) "
                f"(distinct {f(a1)} {f(fl(a1, i))}) (distinct {f(a2)} {f(fl(a2, i))}))")
        run(f"{prefix}-par-c{i+1}", decl_fn("t1") + decl_fn("t2") + f"(assert {body})\n(check-sat)\n", exp, note)

# QX-01: x > 3 or (y <= x and mode != idle); x,y inteiros; mode enum {idle, other}
D = "(declare-datatypes () ((Mode idle choice)))\n"
decl1 = D + "(declare-const x Int)(declare-const y Int)(declare-const mode Mode)\n"
rows("QX-01", decl1, ["(> x 3)", "(<= y x)", "(not (= mode idle))"], lambda b: False, "C0-X01: 0 impossiveis")
dfn = lambda p: f"(declare-const {p}_x Int)(declare-const {p}_y Int)(declare-const {p}_mode Mode)\n"
pairs("QX-01", lambda p: (D if p == "t1" else "") + dfn(p), lambda p: [f"(> {p}_x 3)", f"(<= {p}_y {p}_x)", f"(not (= {p}_mode idle))"],
      lambda a: f"(or {a[0]} (and {a[1]} {a[2]}))", "C0-X01: todas com par", ["sat"] * 3)
run("QX-01-fronteira", "(declare-const x Int)\n(assert (or (and (> x 3) (< x 4)) (> 3 3) (not (> 4 3))))\n(check-sat)\n", "unsat", "C0-X01: 3/4")

# QX-02: (x >= 5 and x < 10) or z == 3
decl2 = "(declare-const x Int)(declare-const z Int)\n"
rows("QX-02", decl2, ["(>= x 5)", "(< x 10)", "(= z 3)"], lambda b: (not b[0]) and (not b[1]), "C0-X02: 2 impossiveis")
pairs("QX-02", lambda p: f"(declare-const {p}_x Int)(declare-const {p}_z Int)\n", lambda p: [f"(>= {p}_x 5)", f"(< {p}_x 10)", f"(= {p}_z 3)"],
      lambda a: f"(or (and {a[0]} {a[1]}) {a[2]})", "C0-X02: todas com par", ["sat"] * 3)
run("QX-02-fronteira", "(declare-const x Int)\n(assert (or (and (>= x 5) (< x 5)) (>= 4 5) (not (>= 5 5)) (and (< x 10) (>= x 9) (not (= x 9))) (not (< 9 10)) (< 10 10)))\n(check-sat)\n", "unsat", "C0-X02: 4/5 e 9/10")

# QX-03: (x > 5 and x < 3) or b
decl3 = "(declare-const x Int)(declare-const b Bool)\n"
rows("QX-03", decl3, ["(> x 5)", "(< x 3)", "b"], lambda bb: bb[0] and bb[1], "C0-X03: impossiveis")
pairs("QX-03", lambda p: f"(declare-const {p}_x Int)(declare-const {p}_b Bool)\n", lambda p: [f"(> {p}_x 5)", f"(< {p}_x 3)", f"{p}_b"],
      lambda a: f"(or (and {a[0]} {a[1]}) {a[2]})", "C0-X03: c1,c2 sem par viavel; b com par", ["unsat", "unsat", "sat"])
pairs("QX-03-livre", lambda p: f"(declare-const {p}_x1 Bool)(declare-const {p}_x2 Bool)(declare-const {p}_b Bool)\n", lambda p: [f"{p}_x1", f"{p}_x2", f"{p}_b"],
      lambda a: f"(or (and {a[0]} {a[1]}) {a[2]})", "C0-X03: com todas as combinacoes ha par => bloqueadas", ["sat", "sat", "sat"])

# QX-11: suites do check por decisao
def fixed(f, tests, nvars):
    names = [f"t{i}" for i in range(len(tests))]; txt = ""
    for n, vals in zip(names, tests):
        txt += "".join(f"(define-fun {n}_v{k} () Bool {'true' if v else 'false'})" for k, v in enumerate(vals)) + "\n"
    out = []
    for k in range(nvars):
        opts = []
        for x, y in itertools.combinations(names, 2):
            ax = [f"{x}_v{j}" for j in range(nvars)]; ay = [f"{y}_v{j}" for j in range(nvars)]
            fl = lambda a: [f"(not {v})" if j == k else v for j, v in enumerate(a)]
            opts.append(f"(and (distinct {ax[k]} {ay[k]}) (distinct {f(ax)} {f(ay)}) (distinct {f(ax)} {f(fl(ax))}) (distinct {f(ay)} {f(fl(ay))}))")
        out.append(txt + f"(assert (or {' '.join(opts)}))\n(check-sat)\n")
    return out
for k, t in enumerate(fixed(lambda a: f"(and {a[0]} {a[1]})", [(1, 1), (0, 1), (1, 0)], 2)):
    run(f"QX-11-d1-c{k+1}", t, "sat", "C0-X11 d#1")
for k, t in enumerate(fixed(lambda a: f"(or {a[0]} {a[1]})", [(0, 0), (1, 0), (0, 1)], 2)):
    run(f"QX-11-d2-c{k+1}", t, "sat", "C0-X11 d#2")

ver = subprocess.run([Z3, "--version"], capture_output=True, text=True).stdout.strip()
json.dump({"z3": ver, "total": len(R), "conforme": sum(r["ok"] for r in R), "divergentes": [r["id"] for r in R if not r["ok"]], "consultas": R},
          open(os.path.join(HERE, "resultados-z3.json"), "w"), indent=1)
print(ver, f"{sum(r['ok'] for r in R)}/{len(R)}", [r["id"] for r in R if not r["ok"]])
