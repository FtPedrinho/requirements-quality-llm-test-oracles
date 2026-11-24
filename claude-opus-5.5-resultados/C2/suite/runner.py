# -*- coding: utf-8 -*-
"""Suíte C2: executa os casos do oráculo congelado contra a CLI MC/DC real, com JaCoCo.

Uso: python runner.py <rodada> [--casos ID,ID,...] [--oraculo caminho] [--classpath arquivo]

- Lê experimento/oraculo.json e confere o hash contra experimento/congelamento/oraculo.sha256.
- Para cada caso roda a invocação do oráculo (observação primária: código de saída, stdout,
  stderr). Quando uma asserção precisa de dados estruturados e a saída primária não é JSON,
  roda uma observação auxiliar com a MESMA fonte e opções e '--format json' (sem '-o').
- Não altera expectativas: cada asserção do oráculo é avaliada como está.
- Resultado por caso: PASSOU, FALHOU, INDETERMINADO (sem expectativa; só diagnóstico) ou
  ERRO_TECNICO (falha de infraestrutura: JVM não iniciou, timeout).
"""
import argparse
import csv
import datetime
import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys

SUITE = os.path.dirname(os.path.abspath(__file__))
C2 = os.path.dirname(SUITE)
REPO = os.path.abspath(os.path.join(C2, "..", ".."))
EXP = os.path.join(C2, "experimento")
ENT = os.path.join(EXP, "entradas")
EXEMPLOS = os.path.join(REPO, "exemplos")
Z3_DIR = "C:/Users/User/AppData/Roaming/Python/bin"
M2 = os.path.expanduser("~/.m2/repository")
JACOCO_AGENT = os.path.join(M2, "org/jacoco/org.jacoco.agent/0.8.16/org.jacoco.agent-0.8.16-runtime.jar")
MAIN = "io.github.rvdomingos.mcdc.cli.Main"
TIMEOUT = 600

# parser/avaliador próprio, congelado junto com o oráculo
_spec = importlib.util.spec_from_file_location("gz3", os.path.join(EXP, "scripts", "gerar_z3.py"))
gz3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gz3)


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def check_freeze(oraculo_path=None, man=None, chave="oraculo.json"):
    man = man or os.path.join(EXP, "congelamento", "oraculo.sha256")
    exp = {}
    for line in open(man, encoding="utf-8"):
        if line.startswith("#") or not line.strip():
            continue
        h, p = line.strip().split(" ", 1)
        exp[p.lstrip("*")] = h
    real = sha256(oraculo_path or os.path.join(EXP, "oraculo.json"))
    if exp.get(chave) != real:
        sys.exit("%s difere do congelado" % chave)
    return real


# ------------------------------------------------------------------ execução
def env_for(z3):
    env = dict(os.environ)
    parts = [p for p in env.get("PATH", "").split(os.pathsep)
             if p and not os.path.exists(os.path.join(p, "z3.exe")) and not os.path.exists(os.path.join(p, "z3"))]
    if z3:
        parts.insert(0, Z3_DIR.replace("/", "\\"))
    env["PATH"] = os.pathsep.join(parts)
    return env


ENT_CASO = ENT


def subst(a, outdir, G):
    a = a.replace("{ENT_BASE}", ENT.replace("\\", "/"))
    a = a.replace("{ENT}", ENT_CASO.replace("\\", "/"))
    a = a.replace("{EX}", EXEMPLOS.replace("\\", "/")).replace("{ENT}", ENT.replace("\\", "/"))
    a = a.replace("{OUT}", outdir.replace("\\", "/"))
    m = re.fullmatch(r"\{G:(\w+)\}", a)
    return G[m.group(1)] if m else a


def run_cli(args, classpath, execfile, z3, cwd):
    cmd = ["java", "-javaagent:%s=destfile=%s,append=true,includes=io.github.rvdomingos.mcdc.*" % (
        JACOCO_AGENT.replace("\\", "/"), execfile.replace("\\", "/")),
        "-Dstdout.encoding=UTF-8", "-Dstderr.encoding=UTF-8", "-Dfile.encoding=UTF-8",
        "-cp", classpath, MAIN] + args
    t0 = datetime.datetime.now()
    try:
        r = subprocess.run(cmd, capture_output=True, env=env_for(z3), cwd=cwd, timeout=TIMEOUT)
        out = r.stdout.decode("utf-8", "replace")
        err = r.stderr.decode("utf-8", "replace")
        rc = r.returncode
        tech = None
    except subprocess.TimeoutExpired:
        out, err, rc, tech = "", "", None, "timeout de %ds" % TIMEOUT
    dt = (datetime.datetime.now() - t0).total_seconds()
    return {"cmd": cmd, "args": args, "exit": rc, "stdout": out, "stderr": err, "segundos": dt, "erro_tecnico": tech}


def aux_args(args):
    out, skip = [], False
    for i, a in enumerate(args):
        if skip:
            skip = False
            continue
        if a in ("--format", "-o"):
            skip = True
            continue
        out.append(a)
    return out + ["--format", "json"]


def fmt_of(args):
    return args[args.index("--format") + 1] if "--format" in args else "text"


# ------------------------------------------------------------------ avaliador próprio
def is_num(s):
    return re.fullmatch(r"-?\d+(\.\d+)?", str(s).strip()) is not None


def atom_value(atom, assign):
    l, op, r = atom[2]
    lv = assign.get(l)
    if lv is None:
        raise KeyError("sem valor para %s" % l)
    if op is None:
        return str(lv).strip().lower() in ("true", "t")
    rv = assign.get(r, r)
    if is_num(lv) and is_num(rv):
        a, b = float(lv), float(rv)
        return {"=": a == b, "!=": a != b, "<": a < b, "<=": a <= b, ">": a > b, ">=": a >= b}[op]
    a, b = str(lv).strip().lower(), str(rv).strip().lower()
    if op == "=":
        return a == b
    if op == "!=":
        return a != b
    raise ValueError("comparação de ordem com texto: %s" % (atom[1],))


def guard_eval_concrete(guard, assign):
    e = gz3.P(guard).parse()
    vals = {}
    for a in gz3.atoms_of(e, []):
        vals[a[1]] = atom_value(a, assign)
    return gz3.eval_bool(e, vals)


def key_of(name):
    """Chave de átomo do parser próprio para o nome de entrada do relatório."""
    try:
        e = gz3.P(name).parse()
        return e[1] if e[0] == "atom" else name
    except Exception:
        return name


def guard_eval_rows(guard, values):
    e = gz3.P(guard).parse()
    vals = {key_of(k): bool(v) for k, v in values.items()}
    return gz3.eval_bool(e, vals)


def concrete_check(report, guards):
    problemas, n = [], 0
    for d in report["decisions"]:
        guard = d["guard"]
        preds = {i["name"]: i for i in d["inputs"]}
        suite = {t["vector"]: t for t in d["minimalSuite"]}
        items = [(t["vector"], t["values"], t["outcome"], t.get("assignment") or {}) for t in d["minimalSuite"]]
        for b in d.get("boundaryTests", []):
            base = suite[b["base"]]
            items.append(("%s(%s)" % (b["base"], b["boundary"]), base["values"], base["outcome"], b["assignment"] or {}))
        for name, values, outcome, assign in items:
            n += 1
            if not assign:
                problemas.append("%s %s: sem valores concretos" % (d["id"], name))
                continue
            for inp, v in values.items():
                p = preds.get(inp, {"name": inp})
                atom = ("atom", inp, (p.get("variable", inp), p.get("operator"), p.get("value"))) \
                    if p.get("variable") else ("atom", inp, (inp, None, None))
                try:
                    got = atom_value(atom, assign)
                except Exception as ex:
                    problemas.append("%s %s: %s" % (d["id"], name, ex))
                    continue
                if got != v:
                    problemas.append("%s %s: %s deveria ser %s com %s" % (d["id"], name, inp, v, assign))
            try:
                g = guard_eval_concrete(guard, assign)
                if g != outcome:
                    problemas.append("%s %s: guarda dá %s, esperado declarado %s" % (d["id"], name, g, outcome))
            except Exception as ex:
                problemas.append("%s %s: guarda não avaliada: %s" % (d["id"], name, ex))
    return n, problemas


def truth_tables(text):
    """Lista de tabelas (cabeçalho, linhas) de um truth-csv."""
    tabs, cur = [], None
    for row in csv.reader(io.StringIO(text)):
        if not row:
            continue
        if row[:3] == ["decision", "requirement", "row"]:
            cur = {"header": row, "rows": []}
            tabs.append(cur)
        elif cur is not None:
            cur["rows"].append(dict(zip(cur["header"], row)))
    return tabs


def tt_conditions(header):
    return header[3:header.index("outcome")]


# ------------------------------------------------------------------ asserções
class Ctx:
    def __init__(self, case, prim, aux, outdir):
        self.case, self.prim, self.aux, self.outdir = case, prim, aux, outdir
        self._pj = None

    def primary_json(self):
        return json.loads(self.prim["stdout"])

    def data(self):
        """Relatório estruturado: o primário se for JSON, senão o auxiliar."""
        if fmt_of(self.prim["args"]) == "json" and "-o" not in self.prim["args"]:
            return json.loads(self.prim["stdout"])
        if self.aux is None:
            raise RuntimeError("sem observação estruturada")
        if self.aux["exit"] not in (0, 2):
            raise RuntimeError("observação JSON auxiliar terminou com código %s: %s" % (
                self.aux["exit"], (self.aux["stderr"] or self.aux["stdout"]).strip()[:300]))
        return json.loads(self.aux["stdout"])


def path_out(s, outdir):
    return s.replace("{OUT}", outdir.replace("\\", "/"))


def assert_one(k, v, c):
    """Devolve (ok, observado)."""
    if k == "exit":
        return c.prim["exit"] == v, c.prim["exit"]
    if k == "aviso_z3":
        txt = (c.prim["stdout"] + c.prim["stderr"]).lower()
        return ("z3" in txt) == v, (c.prim["stderr"] or c.prim["stdout"]).strip()[:300]
    if k == "json_valido":
        try:
            json.loads(c.prim["stdout"])
            return v, True
        except Exception as ex:
            return not v, "JSON inválido: %s" % ex
    if k == "arquivo_gerado":
        p = path_out(v, c.outdir)
        ok = os.path.isfile(p) and os.path.getsize(p) > 0
        return ok, "existe, %d bytes" % os.path.getsize(p) if os.path.isfile(p) else "ausente"
    if k == "stdout_sem_relatorio":
        p = [x for x in c.case["comando"] if "{OUT}" in x][0]
        p = path_out(p, c.outdir)
        body = open(p, encoding="utf-8").read() if os.path.isfile(p) else ""
        first = [l for l in body.splitlines() if l.strip()][:3]
        leak = any(l in c.prim["stdout"] for l in first)
        return (not leak) == v, c.prim["stdout"].strip()[:200]
    if k in ("csv_linhas_dados", "csv_resultado_esperado_correto"):
        rows = list(csv.DictReader(io.StringIO(c.prim["stdout"])))
        if k == "csv_linhas_dados":
            return len(rows) == v, len(rows)
        guard = c.data()["decisions"][0]["guard"]
        tests = {}
        for r in rows:
            tests.setdefault(r["test"], {"vals": {}, "exp": r["expected_outcome"]})["vals"][r["input"]] = r["value"] == "T"
        bad = [t for t, x in tests.items() if guard_eval_rows(guard, x["vals"]) != (x["exp"] == "T")]
        return (not bad) == v, {"testes": len(tests), "divergentes": bad}
    if k.startswith("truth_"):
        if k.endswith("_arquivo"):
            p = [x for x in c.case["comando"] if "{OUT}" in x][0]
            text = open(path_out(p, c.outdir), encoding="utf-8").read()
        else:
            text = c.prim["stdout"]
        tabs = truth_tables(text)
        rows = [r for t in tabs for r in t["rows"]]
        if k.startswith("truth_linhas"):
            return len(rows) == v, len(rows)
        if k.startswith("truth_impossiveis_marcadas"):
            n = sum(1 for r in rows if r.get("feasible") == "F")
            return n == v, n
        if k == "truth_primeira_tudo_verdadeiro":
            t = tabs[0]
            first = t["rows"][0]
            ok = all(first[cn] == "T" for cn in tt_conditions(t["header"]))
            return ok == v, {cn: first[cn] for cn in tt_conditions(t["header"])}
        if k == "truth_resultado_correto":
            guard = c.data()["decisions"][0]["guard"]
            bad = []
            for t in tabs:
                for r in t["rows"]:
                    vals = {cn: r[cn] == "T" for cn in tt_conditions(t["header"])}
                    if guard_eval_rows(guard, vals) != (r["outcome"] == "T"):
                        bad.append(r["row"])
            return (not bad) == v, {"linhas_divergentes": bad}
    if k == "json_valido_arquivo":
        p = [x for x in c.case["comando"] if "{OUT}" in x][0]
        try:
            json.load(open(path_out(p, c.outdir), encoding="utf-8"))
            return v, True
        except Exception as ex:
            return not v, str(ex)
    if k == "rastreabilidade_arquivo_qtd":
        p = [x for x in c.case["comando"] if "{OUT}" in x][0]
        r = json.load(open(path_out(p, c.outdir), encoding="utf-8"))
        n = sum(1 for d in r["decisions"] if d.get("requirement"))
        return n == v, n

    R = c.data()
    decs = R.get("decisions", [])
    cmdname = c.case["comando"][0]
    if cmdname == "verify":
        if k == "conflitos":
            return len(R["conflicts"]) == v, len(R["conflicts"])
        if k == "lacuna":
            return R["gaps"]["found"] == v, R["gaps"]
    if cmdname == "check":
        if k == "check_divergentes":
            probs = [p for d in decs for p in d["problems"]]
            names = sorted(set(re.findall(r"\bT\d+\b", " ".join(probs))))
            return names == sorted(v), {"problemas": probs}
        if k == "check_nao_demonstrada":
            n = [(d["id"], d["conditionsDemonstrated"], d["conditionsTotal"]) for d in decs]
            got = any(a < b for _, a, b in n)
            return got == v, n
        if k == "check_completo":
            got = R["complete"] and all(d["conditionsDemonstrated"] == d["conditionsTotal"] for d in decs)
            return got == v, {"complete": R["complete"], "problemas": [p for d in decs for p in d["problems"]]}
    if k == "tamanho_suite":
        n = sum(len(d["minimalSuite"]) for d in decs)
        return n == v, n
    if k == "tamanho_suite_por_requisito":
        got = {d.get("requirement") or d["id"]: len(d["minimalSuite"]) for d in decs}
        return all(got.get(r) == n for r, n in v.items()), got
    if k == "todas_condicoes_com_par":
        unc = {d["id"]: d["uncoveredConditions"] for d in decs if d["uncoveredConditions"]}
        return (not unc) == v, unc or "nenhuma condição sem par"
    if k == "requisitos_com_todas_com_par":
        got = {d.get("requirement") or d["id"]: d["uncoveredConditions"] for d in decs}
        return all(got.get(r) == [] for r in v), got
    if k == "condicoes":
        n = sum(len(d["conditions"]) for d in decs)
        return n == v, n
    if k == "entradas":
        n = sum(len(d["inputs"]) for d in decs)
        return n == v, n
    if k == "combinacoes":
        n = sum(d["truthTableRows"] for d in decs)
        return n == v, n
    if k == "impossiveis":
        if not all("truthTable" in d for d in decs):
            return False, "tabela ausente no JSON"
        n = sum(1 for d in decs for r in d["truthTable"] if not r["feasible"])
        return n == v, n
    if k == "requisitos":
        return len(decs) == v, len(decs)
    if k == "mutantes":
        if not all("mutation" in d for d in decs):
            return False, "sem seção de mutação"
        tot = {"total": 0, "equivalentes": 0, "detectados": 0}
        for d in decs:
            for f in d["mutation"]["faults"].values():
                tot["total"] += f["total"]
                tot["equivalentes"] += f["equivalent"]
                tot["detectados"] += f["killed"]
        return tot == v, tot
    if k == "condicao_classificada":
        got = {u["condition"]: u["reason"] for d in decs for u in d["uncovered"]}
        mp = {"REDUNDANT": "redundante", "INFEASIBLE": "bloqueada"}
        return all(mp.get(got.get(cn)) == cl for cn, cl in v.items()), got
    if k == "condicao_com_par":
        labels = {cc["label"] for d in decs for cc in d["conditions"]}
        unc = {x for d in decs for x in d["uncoveredConditions"]}
        return all(cn in labels and cn not in unc for cn in v), {"rotulos": sorted(labels), "sem_par": sorted(unc)}
    if k == "requisito_tem_classe":
        mp = {"REDUNDANT": "redundante", "INFEASIBLE": "bloqueada"}
        got = {(d.get("requirement") or d["id"]): [mp.get(u["reason"]) for u in d["uncovered"]] for d in decs}
        return all(cl in got.get(r, []) for r, cl in v.items()), got
    if k == "rotulos_condicoes_contem":
        labels = [cc["label"] for d in decs for cc in d["conditions"]]
        return all(x in labels for x in v), labels
    if k == "suite_sem_combinacao":
        bad = [t["vector"] for d in decs for t in d["minimalSuite"]
               if all(t["values"].get(n) == b for n, b in v.items())]
        return not bad, {"testes_que_violam": bad, "suite": [(t["vector"], t["values"]) for d in decs for t in d["minimalSuite"]]}
    if k == "fronteira_contem":
        got = {}
        for d in decs:
            for b in d.get("boundaryTests", []):
                var = gz3.P(b["condition"]).parse()[2][0]
                got.setdefault(b["condition"], set()).add(str(b["assignment"].get(var)))
        ok = all(set(vals) <= got.get(cn, set()) for cn, vals in v.items())
        return ok, {cn: sorted(s) for cn, s in got.items()}
    if k == "concretos_realizam":
        n, probs = concrete_check(R, None)
        return (n > 0 and not probs) == v, {"testes_conferidos": n, "problemas": probs[:20], "qtd_problemas": len(probs)}
    if k == "rastreabilidade":
        got = {d["id"]: d.get("requirement") for d in decs}
        return all(got.get(i) == r for i, r in v.items()), got
    if k == "equivalente_a":
        return None, "comparado após a rodada"
    raise KeyError("asserção desconhecida: %s" % k)


NEEDS_STRUCT = {"tamanho_suite", "tamanho_suite_por_requisito", "todas_condicoes_com_par", "requisitos_com_todas_com_par",
                "condicoes", "entradas", "combinacoes", "impossiveis", "requisitos", "mutantes", "condicao_classificada",
                "condicao_com_par", "requisito_tem_classe", "rotulos_condicoes_contem", "suite_sem_combinacao",
                "fronteira_contem", "concretos_realizam", "rastreabilidade", "conflitos", "lacuna", "check_divergentes",
                "check_nao_demonstrada", "check_completo", "csv_resultado_esperado_correto", "truth_resultado_correto",
                "equivalente_a"}


def structural_signature(c):
    """Para equivalente_a: tamanho da suíte e resultado por linha da tabela (renomeando entradas por posição)."""
    R = c.data()
    d = R["decisions"][0]
    names = [i["name"] for i in d["inputs"]]
    tt = [(tuple(r["values"][n] for n in names), r["outcome"]) for r in d.get("truthTable", [])]
    return {"suite": len(d["minimalSuite"]), "tabela": tt, "sem_par": d["uncoveredConditions"]}


# ------------------------------------------------------------------ principal
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rodada")
    ap.add_argument("--casos")
    ap.add_argument("--classpath", default=os.path.join(EXP, "build", "classpath.txt"))
    ap.add_argument("--oraculo", help="oráculo de extensão (padrão: experimento/oraculo.json)")
    ap.add_argument("--manifesto", help="manifesto sha256 que congela o oráculo de extensão")
    ap.add_argument("--entradas", help="pasta usada para {ENT} (padrão: experimento/entradas)")
    a = ap.parse_args()
    global ENT_CASO
    if a.entradas:
        ENT_CASO = os.path.abspath(a.entradas)
    if a.oraculo:
        orahash = check_freeze(os.path.abspath(a.oraculo), os.path.abspath(a.manifesto), os.path.basename(a.oraculo))
        oraculo = json.load(open(a.oraculo, encoding="utf-8"))
    else:
        orahash = check_freeze()
        oraculo = json.load(open(os.path.join(EXP, "oraculo.json"), encoding="utf-8"))
    G = json.load(open(os.path.join(ENT, "expressoes-geradas.json"), encoding="utf-8"))
    classpath = open(a.classpath, encoding="utf-8").read().strip()
    rd = os.path.join(C2, "resultados", a.rodada)
    if os.path.exists(rd):
        sys.exit("rodada já existe; não sobrescrever: %s" % rd)
    os.makedirs(os.path.join(rd, "casos"))
    outdir = os.path.join(rd, "arquivos-o")
    os.makedirs(outdir)
    execfile = os.path.join(rd, "jacoco.exec")
    casos = oraculo["casos"]
    if a.casos:
        sel = set(a.casos.split(","))
        casos = [x for x in casos if x["id"] in sel]
    inicio = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    resultados, ctxs = [], {}
    for case in casos:
        args = [subst(x, outdir, G) for x in case["comando"]]
        z3 = case["pre_condicoes"]["z3_no_PATH_do_SUT"]
        prim = run_cli(args, classpath, execfile, z3, REPO)
        if case["id"] == "A34":
            pass  # diagnóstico com a letra A escolhida (registrado no oráculo)
        exp = case["expectativa"] or {}
        aux = None
        fmt = fmt_of(args)
        need = any(k in NEEDS_STRUCT for k in exp) or (case["status"] == "INDETERMINADO" and args[0] in ("analyze", "check", "verify") and fmt != "json")
        if need and (fmt != "json" or "-o" in args) and args[0] in ("analyze", "check", "verify") and prim["erro_tecnico"] is None:
            aux = run_cli(aux_args(args), classpath, execfile, z3, REPO)
        cdir = os.path.join(rd, "casos", case["id"])
        os.makedirs(cdir)
        for nm, obs in (("primaria", prim), ("auxiliar-json", aux)):
            if obs is None:
                continue
            open(os.path.join(cdir, nm + ".stdout.txt"), "w", encoding="utf-8", newline="\n").write(obs["stdout"])
            open(os.path.join(cdir, nm + ".stderr.txt"), "w", encoding="utf-8", newline="\n").write(obs["stderr"])
        c = Ctx(case, prim, aux, outdir)
        ctxs[case["id"]] = c
        res = {"id": case["id"], "status_oraculo": case["status"], "comando": args, "exit": prim["exit"],
               "exit_auxiliar": aux["exit"] if aux else None, "segundos": round(prim["segundos"], 2),
               "assercoes": [], "erro_tecnico": prim["erro_tecnico"] or (aux or {}).get("erro_tecnico")}
        if res["erro_tecnico"]:
            res["resultado"] = "ERRO_TECNICO"
        elif case["status"] == "INDETERMINADO":
            res["resultado"] = "INDETERMINADO"
            try:
                R = c.data() if aux or fmt == "json" else None
                res["diagnostico"] = {"suite": sum(len(d.get("minimalSuite", [])) for d in R.get("decisions", [])) if R and "decisions" in R and args[0] == "analyze" else None}
            except Exception as ex:
                res["diagnostico"] = {"observacao": str(ex)[:300]}
            res["diagnostico_saida"] = (prim["stderr"] or prim["stdout"]).strip()[:400]
        else:
            for k, v in exp.items():
                try:
                    ok, obs = assert_one(k, v, c)
                except Exception as ex:
                    ok, obs = False, "não observável: %s: %s" % (type(ex).__name__, str(ex)[:300])
                res["assercoes"].append({"assercao": k, "esperado": v, "observado": obs, "ok": ok})
        resultados.append(res)
        print(case["id"], res.get("resultado", ""), prim["exit"], flush=True)
    # equivalente_a (comparação estrutural entre casos)
    for res in resultados:
        for asr in res["assercoes"]:
            if asr["assercao"] == "equivalente_a":
                try:
                    s1 = structural_signature(ctxs[res["id"]])
                    s2 = structural_signature(ctxs[asr["esperado"]])
                    asr["ok"] = s1 == s2
                    asr["observado"] = {"este": {"suite": s1["suite"], "linhas": len(s1["tabela"])},
                                        "referencia": {"suite": s2["suite"], "linhas": len(s2["tabela"])}, "iguais": s1 == s2}
                except Exception as ex:
                    asr["ok"] = False
                    asr["observado"] = "não observável: %s" % ex
        if "resultado" not in res:
            res["resultado"] = "PASSOU" if all(x["ok"] for x in res["assercoes"]) else "FALHOU"
    fim = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    cont = {}
    for r in resultados:
        cont[r["resultado"]] = cont.get(r["resultado"], 0) + 1
    meta = {"rodada": a.rodada, "inicio": inicio, "fim": fim, "oraculo_sha256": orahash,
            "runner_sha256": sha256(os.path.abspath(__file__)), "classpath": classpath,
            "jacoco_agent": JACOCO_AGENT, "z3_dir": Z3_DIR, "contagem": cont}
    json.dump({"meta": meta, "casos": resultados}, open(os.path.join(rd, "resultados.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, default=str)
    print(json.dumps(cont))


if __name__ == "__main__":
    main()
