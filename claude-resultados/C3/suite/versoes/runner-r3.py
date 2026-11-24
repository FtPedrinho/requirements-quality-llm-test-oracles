"""Suíte C3: executa os casos do oráculo congelado contra a CLI real do MC/DC, com JaCoCo.

Uso: python -I runner.py <rodada> <sut_dir> [ids...]
  <sut_dir>: saída de experimento/build/build.sh (classes/, classpath.txt)
As expectativas vêm de experimento/oraculo.json (congelado). Este arquivo só sabe
COMO observar a saída (formato aprendido do código após o congelamento).
"""
import json
import os
import re
import subprocess
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
C3 = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(C3))
EXP = os.path.join(C3, "experimento")
sys.path.insert(0, EXP)
import exprlib as X  # noqa: E402

RODADA, SUT = sys.argv[1], sys.argv[2]
ONLY = set(sys.argv[3:])
ORACLE_FILE = os.environ.get("C3_ORACULO", os.path.join(EXP, "oraculo.json"))
OUTDIR = os.path.join(C3, "resultados", RODADA)
if os.path.exists(os.path.join(OUTDIR, "resultados.json")):
    raise SystemExit(f"rodada {RODADA} já existe; não sobrescrever")
os.makedirs(OUTDIR, exist_ok=True)

Z3DIR = "C:/Users/User/AppData/Roaming/Python/bin"
HOME = os.path.expanduser("~").replace("\\", "/")
AGENT = f"{HOME}/.m2/repository/org/jacoco/org.jacoco.agent/0.8.16/org.jacoco.agent-0.8.16-runtime.jar"
EXEC = os.path.join(OUTDIR, "jacoco.exec").replace("\\", "/")
CP = open(os.path.join(SUT, "classpath.txt"), encoding="utf-8").read().strip()
EXDIR = os.path.join(ROOT, "exemplos").replace("\\", "/")
ENTDIR = os.path.join(EXP, "entradas").replace("\\", "/")
ENT2DIR = os.path.join(EXP, "extensao-r2", "entradas").replace("\\", "/")
TIPOS = {s: {i["name"]: i["type"] for i in json.load(open(f"{EXDIR}/{s}-decisoes.json", encoding="utf-8"))["inputs"]}
         for s in ("vm", "tis", "npp")}


def base_path():
    parts = [p for p in os.environ["PATH"].split(os.pathsep) if "Python\\bin" not in p and "Python/bin" not in p]
    return parts


def run_case(case):
    cdir = os.path.join(OUTDIR, "casos", case["id"])
    os.makedirs(cdir, exist_ok=True)
    args = []
    for a in case["args"]:
        a = a.replace("{ENT2}", ENT2DIR).replace("{EX}", EXDIR).replace("{ENT}", ENTDIR).replace("{OUT}", cdir.replace("\\", "/"))
        m = re.fullmatch(r"\{FILE:(.+)\}", a)
        if m:
            a = open(os.path.join(EXP, "entradas", m.group(1)), encoding="utf-8").read().strip()
        args.append(a)
    env = dict(os.environ)
    path = base_path()
    if "FORA" not in case["precondicao"]:
        path = [Z3DIR.replace("/", "\\")] + path
    env["PATH"] = os.pathsep.join(path)
    cmd = ["java", f"-javaagent:{AGENT}=destfile={EXEC},append=true,includes=io.github.rvdomingos.*",
           "-Dstdout.encoding=UTF-8", "-Dstderr.encoding=UTF-8", "-cp", CP,
           "io.github.rvdomingos.mcdc.cli.Main", *args]
    r = subprocess.run(cmd, capture_output=True, env=env, timeout=600)
    out, err = r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")
    for n, v in [("stdout.txt", out), ("stderr.txt", err), ("exit.txt", str(r.returncode))]:
        open(os.path.join(cdir, n), "w", encoding="utf-8", newline="\n").write(v)
    open(os.path.join(cdir, "comando.json"), "w", encoding="utf-8").write(json.dumps(args, ensure_ascii=False))
    return out, err, r.returncode, cdir


# ------------------------------------------------------------ leitura do texto
def blocks(out):
    """Divide o relatório em texto por decisão."""
    parts = re.split(r"(?m)^(?=Decisão:   )", out)
    return [p for p in parts if p.startswith("Decisão:")]


def block_for(out, dec):
    for b in blocks(out):
        head = b.split("\n", 3)
        ids = [ln.split(":", 1)[1].strip() for ln in head[:2] if ln.startswith(("Decisão:", "Requisito:"))]
        if dec is None or dec in ids:
            return b
    raise AssertionError(f"decisão {dec} ausente na saída")


def norm(s):
    return re.sub(r"\s+", "", s).replace("==", "=")


def text_table(b):
    lines = b.splitlines()
    i = next(k for k, ln in enumerate(lines) if ln.startswith("Vetor "))
    names = [n for n in re.split(r"\s{3,}", lines[i][6:].split("| D")[0].strip()) if n]
    rows = []
    for ln in lines[i + 1:]:
        if not re.match(r"^V\d+\s", ln):
            break
        left, right = ln.split("|", 1)
        vals = left.split()[1:]
        rows.append({"nome": left.split()[0], "valores": dict(zip(names, [v == "T" for v in vals])),
                     "saida": right.strip().startswith("T"), "impossivel": "impossível" in right})
    return names, rows


def text_pairs(b):
    sec = b.split("Pares de independência:\n", 1)[1].split("\n\n", 1)[0]
    res = {}
    for ln in sec.splitlines():
        cond, rest = ln.strip().split(": ", 1)
        res[cond] = re.findall(r"\((V\d+), (V\d+)\)", rest)
    return res


def text_suite(b):
    m = re.search(r"\((\d+) testes\):\n((?:  V\d+ .*\n)*)", b)
    return [{"nome": ln.split()[0], "bits": ln.split()[1], "linha": ln} for ln in m.group(2).splitlines()]


def text_coverage(b):
    return re.search(r"Cobertura MC/DC: (.*)", b).group(1)


def map_names(tool_names, expected_atoms):
    m = {}
    for a in expected_atoms:
        hit = [t for t in tool_names if norm(t) == norm(a)]
        if len(hit) != 1:
            raise AssertionError(f"entrada {a!r} não identificada entre {tool_names}")
        m[a] = hit[0]
    return m


# ------------------------------------------------------------------ verificações
def chk_tabela(v, out, js, cdir):
    exp = v["linhas"]
    atoms = list(exp[0]["entradas"].keys())
    if js is not None:
        decs = js["decisions"]
        d = decs[0] if "decisao" not in v else next(x for x in decs if v["decisao"] in (x["id"], x["requirement"]))
        tool_names = [i["name"] for i in d["inputs"]]
        rows = [{"valores": r["values"], "saida": r["outcome"]} for r in d["truthTable"]]
        n = d["truthTableRows"]
    else:
        b = block_for(out, v.get("decisao"))
        tool_names, rows = text_table(b)
        n = len(rows)
    nm = map_names(tool_names, atoms)
    assert n == v["combinacoes"] and len(rows) == v["combinacoes"], f"combinações {n}/{len(rows)} ≠ {v['combinacoes']}"
    got = {tuple(r["valores"][nm[a]] for a in atoms): r["saida"] for r in rows}
    want = {tuple(r["entradas"][a] for a in atoms): r["saida"] for r in exp}
    assert got == want, f"tabela diverge: {[k for k in want if got.get(k) != want[k]]}"
    return f"{n} combinações conferidas"


def chk_linha0(v, out, js, cdir):
    _, rows = text_table(block_for(out, None))
    assert all(rows[0]["valores"].values()), f"primeira linha {rows[0]}"
    return f"{rows[0]['nome']} tudo T"


def chk_condicoes_com_par(v, out, js, cdir):
    b = block_for(out, None)
    pairs = text_pairs(b)
    cov = text_coverage(b)
    missing = [c for c in v["condicoes"] if not pairs.get(c)]
    assert not missing and cov.startswith("completa"), f"sem par: {missing}; cobertura: {cov}"
    return f"cobertura: {cov}; pares por condição: {{{', '.join(f'{c}: {len(pairs[c])}' for c in v['condicoes'])}}}"


def chk_pares_mudam(v, out, js, cdir):
    b = block_for(out, None)
    _, rows = text_table(b)
    byname = {r["nome"]: r for r in rows}
    n = 0
    for cond, ps in text_pairs(b).items():
        for p, q in ps:
            assert byname[p]["valores"][cond] != byname[q]["valores"][cond], f"par {p},{q} não muda {cond}"
            n += 1
    return f"{n} pares conferidos"


def chk_suite_alterna(v, out, js, cdir):
    b = block_for(out, None)
    names, rows = text_table(b)
    byname = {r["nome"]: r for r in rows}
    suite = [byname[t["nome"]] for t in text_suite(b)]
    for c in v["condicoes"]:
        assert len({r["valores"][c] for r in suite}) == 2, f"suíte não alterna {c}"
    return f"suíte de {len(suite)} testes alterna {v['condicoes']}"


def chk_recusada(v, out, js, cdir):
    assert "Decisão:" not in out and "Vetor" not in out and not out.strip().startswith("{"), "houve relatório"
    assert err_text(cdir).strip(), "sem mensagem de erro"
    return "recusada: " + err_text(cdir).strip().splitlines()[0][:160]


def err_text(cdir):
    return open(os.path.join(cdir, "stderr.txt"), encoding="utf-8").read()


def chk_erro_menciona(v, out, js, cdir):
    assert v["texto"] in err_text(cdir) + out, f"mensagem não cita {v['texto']}"
    return f"cita {v['texto']}"


def chk_requisitos(v, out, js, cdir):
    ids = [b.split("\n", 1)[0].split(":", 1)[1].strip() for b in blocks(out)]
    assert ids == v["ids"], f"requisitos {ids}"
    return f"{ids}"


def chk_json_valido(v, out, js, cdir):
    assert js is not None, "saída não é JSON"
    return "JSON válido"


def chk_sistema(v, out, js, cdir):
    d = js["decisions"]
    got = {"decisoes": len(d), "combinacoes": sum(x["truthTableRows"] for x in d),
           "requisitos": [x["requirement"] for x in d]}
    if "condicoes" in v:
        got["condicoes"] = sum(len(x["conditions"]) for x in d)
    want = {k: v[k] for k in got}
    assert got == want, f"obtido {got}"
    return json.dumps({k: got[k] for k in got if k != "requisitos"})


def chk_mut_tipos(v, out, js, cdir):
    sec = out.split("Validação por mutação", 1)[1].split("\n\n", 1)[0]
    types = re.findall(r"\(([A-Z]{3})\): (\d+) de (\d+)", sec)
    assert types, "sem tipos de mutante"
    bad = [t for t, *_ in types if t not in v["permitidos"]]
    assert not bad, f"tipos fora da lista: {bad}"
    return "tipos: " + ", ".join(f"{t} {k}/{n}" for t, k, n in types)


def chk_mut_total(v, out, js, cdir):
    tot = sum(f["total"] for d in js["decisions"] for f in d["mutation"]["faults"].values())
    eq = sum(f["equivalent"] for d in js["decisions"] for f in d["mutation"]["faults"].values())
    kil = sum(f["killed"] for d in js["decisions"] for f in d["mutation"]["faults"].values())
    assert tot == v["total"], f"total {tot} (equivalentes {eq}, mortos {kil})"
    return f"total {tot}, equivalentes {eq}, mortos {kil}"


def chk_arquivo_rel(v, out, js, cdir):
    p = os.path.join(cdir, v["arquivo"])
    assert os.path.exists(p), "arquivo não criado"
    txt = open(p, encoding="utf-8").read()
    assert "Vetor" in txt and "Decisão:" in txt, "arquivo sem relatório"
    assert "Vetor" not in out and "Decisão:" not in out, "relatório também na tela"
    return f"arquivo com {len(txt)} caracteres; tela: {out.strip()[:80]}"


def check_blocks(out):
    res = {}
    for b in blocks(out):
        dec = b.split("\n", 1)[0].split(":", 1)[1].strip()
        sec = b.split("\nCondições:\n", 1)[1].split("\n\n", 1)[0]
        conds = {}
        for ln in sec.splitlines():
            c, rest = ln.strip().split(": ", 1)
            conds[c] = rest.startswith("demonstrada")
        probs = []
        if "\nProblemas:\n" in b:
            probs = [ln.strip() for ln in b.split("\nProblemas:\n", 1)[1].split("\n\n", 1)[0].splitlines()]
        res[dec] = {"conds": conds, "problemas": probs, "cobertura": re.search(r"Cobertura MC/DC: (.*)", b).group(1)}
    return res


def chk_check_dem(v, out, js, cdir):
    res = check_blocks(out)
    r = res[v["decisao"]] if "decisao" in v else next(iter(res.values()))
    for c in v["demonstradas"]:
        assert r["conds"].get(c) is True, f"{c} não demonstrada: {r['conds']}"
    for c in v["nao_demonstradas"]:
        assert r["conds"].get(c) is False, f"{c} não deveria estar demonstrada: {r['conds']}"
    if not v.get("parcial"):
        assert set(r["conds"]) == set(v["demonstradas"]) | set(v["nao_demonstradas"]), f"condições {list(r['conds'])}"
    return f"{r['conds']} | {r['cobertura']}"


def chk_check_div(v, out, js, cdir):
    res = check_blocks(out)
    div = sorted(p.split(":")[0] for r in res.values() for p in r["problemas"] if "resultado esperado" in p)
    assert div == sorted(v["testes"]), f"divergentes {div}"
    return f"divergentes {div}"


def chk_sem_lacunas(v, out, js, cdir):
    ln = re.search(r"Lacunas: (.*)", out).group(1)
    assert not ln.startswith("encontrada"), ln
    return ln


def chk_sem_lacunas_json(v, out, js, cdir):
    assert not js["gaps"]["found"], f"lacuna: {js['gaps']}"
    return f"gaps: {js['gaps']}"


def boundary_values(out, js, var):
    vals = []
    if js is not None:
        for d in js["decisions"]:
            for b in d.get("boundaryTests", []):
                if var in b["assignment"]:
                    vals.append(b["assignment"][var])
    else:
        sec = out.split("Testes de fronteira", 1)[1].split("\n\n", 1)[0]
        for m in re.finditer(r"\[(.*)\]", sec):
            for kv in m.group(1).split(", "):
                k, val = kv.split(" = ", 1)
                if k == var:
                    vals.append(val)
    return sorted({float(x) for x in vals})


def chk_fronteira(v, out, js, cdir):
    got = boundary_values(out, js, v["variavel"])
    miss = [x for x in v["valores"] if float(x) not in got]
    assert not miss, f"faltam {miss}; observados {got}"
    return f"{v['variavel']}: observados {got}"


def chk_valores(v, out, js, cdir):
    sysname = None
    for s in ("vm", "tis", "npp"):
        if js.get("system") and s in ("vm",) and "coffee" in js["system"]:
            sysname = "vm"
    types = v.get("tipos") or TIPOS.get(sysname, {})
    n = 0
    for d in js["decisions"]:
        e = X.parse(d["guard"])
        for t in d["minimalSuite"]:
            a = t.get("assignment")
            if not a:
                continue
            for atom in X.atoms(e):
                got = X.eval_atom_concrete(atom, a, types)
                assert got == t["values"][atom], f"{d['id']} {t['vector']}: {atom} = {got} ≠ {t['values'][atom]} ({a})"
            val = {atom: X.eval_atom_concrete(atom, a, types) for atom in X.atoms(e)}
            assert X.ev(e, val) == t["outcome"], f"{d['id']} {t['vector']}: guarda ≠ esperado"
            n += 1
    return f"{n} testes com valores concretos conferidos"


def chk_respeita(v, out, js, cdir):
    b = block_for(out, None)
    names, rows = text_table(b)
    byname = {r["nome"]: r for r in rows}
    cons = X.parse(v["restricao"])
    used = [t["nome"] for t in text_suite(b)] + [x for ps in text_pairs(b).values() for p in ps for x in p]
    bad = sorted({u for u in used if not X.ev(cons, byname[u]["valores"])})
    assert not bad, f"usa combinações fora da restrição: {bad}"
    return f"{len(set(used))} vetores usados, todos dentro da restrição"


def chk_arquivo_json(v, out, js, cdir):
    d = json.load(open(os.path.join(cdir, v["arquivo"]), encoding="utf-8"))["decisions"][0]
    withpair = sum(1 for c, ps in d["independencePairs"].items() if ps)
    assert d["truthTableRows"] == v["combinacoes"], f"combinações {d['truthTableRows']}"
    assert withpair == v["condicoes_com_par"] and not d["uncoveredConditions"], f"com par {withpair}"
    return f"{d['truthTableRows']} combinações, {withpair} condições com par, suíte {len(d['minimalSuite'])}"


CHECKS = {"tabela_verdade": chk_tabela, "linha0_tudo_verdadeiro": chk_linha0,
          "todas_condicoes_com_par": chk_condicoes_com_par, "pares_mudam_condicao": chk_pares_mudam,
          "suite_alterna_condicoes": chk_suite_alterna, "recusada": chk_recusada, "erro_menciona": chk_erro_menciona,
          "requisitos": chk_requisitos, "json_valido": chk_json_valido, "sistema": chk_sistema,
          "mutacao_tipos": chk_mut_tipos, "mutantes_total": chk_mut_total, "arquivo_relatorio": chk_arquivo_rel,
          "check_demonstradas": chk_check_dem, "check_divergentes": chk_check_div, "sem_lacunas": chk_sem_lacunas,
          "fronteira": chk_fronteira, "valores_realizam": chk_valores, "suite_respeita": chk_respeita,
          "arquivo_json": chk_arquivo_json, "sem_lacunas_json": chk_sem_lacunas_json}


def main():
    oracle = json.load(open(ORACLE_FILE, encoding="utf-8"))
    results = []
    seen = {}  # mesmo comando e mesma pré-condição: uma execução só, observada por vários casos
    for case in oracle["casos"]:
        if ONLY and case["id"] not in ONLY:
            continue
        key = (tuple(case["args"]), case["precondicao"])
        if key in seen:
            out, err, code, cdir, src = seen[key]
            mine = os.path.join(OUTDIR, "casos", case["id"])
            os.makedirs(mine, exist_ok=True)
            open(os.path.join(mine, "reutiliza.txt"), "w", encoding="utf-8").write(
                f"Mesma execução de {src} (comando e pré-condição idênticos); ver casos/{src}/\n")
        else:
            out, err, code, cdir = run_case(case)
            seen[key] = (out, err, code, cdir, case["id"])
        try:
            js = json.loads(out)
        except ValueError:
            js = None
        rec = {"id": case["id"], "titulo": case["titulo"], "status_oraculo": case["status"], "exit": code,
               "stderr_1a_linha": (err.strip().splitlines() or [""])[0][:200], "verificacoes": []}
        if case["status"] == "INDETERMINADO":
            rec["resultado"] = "INDETERMINADO"
            rec["observacao"] = (out.strip().splitlines() or [""])[0][:200]
        else:
            verdict = "PASSOU"
            for v in case["verificacoes"]:
                try:
                    detail = CHECKS[v["tipo"]](v, out, js, cdir)
                    rec["verificacoes"].append({"tipo": v["tipo"], "ok": True, "detalhe": detail})
                except AssertionError as e:
                    rec["verificacoes"].append({"tipo": v["tipo"], "ok": False, "detalhe": str(e)[:600]})
                    verdict = "FALHOU"
                except Exception:  # noqa: BLE001 — erro do harness, não falha semântica
                    rec["verificacoes"].append({"tipo": v["tipo"], "ok": None,
                                                "detalhe": "ERRO DO HARNESS: " + traceback.format_exc()[-600:]})
                    if verdict == "PASSOU":
                        verdict = "ERRO_TECNICO"
            rec["resultado"] = verdict
        results.append(rec)
        print(f"{rec['id']:12} {rec['resultado']:13} exit={code}", flush=True)
    json.dump(results, open(os.path.join(OUTDIR, "resultados.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    cnt = {}
    for r in results:
        cnt[r["resultado"]] = cnt.get(r["resultado"], 0) + 1
    print(cnt)


main()
