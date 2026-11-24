# -*- coding: utf-8 -*-
"""Suíte C4: executa o MC/DC real (CLI) sob o agente JaCoCo e julga os casos do oráculo congelado.

Uso: python -I runner.py <repo> <classpath.txt> <jacoco-agent.jar> <dir-da-rodada>

- Cada execução Xnn roda uma única vez (JVM própria, agente JaCoCo com append no mesmo jacoco.exec).
- Casos INDETERMINADOS do oráculo não são executados (decisão do pesquisador) e são só registrados.
- As expectativas vêm de experimento/oraculo.json (congelado); este arquivo só traduz cada expectativa
  em verificação sobre a saída observada. Nenhuma expectativa é ajustada ao sistema.
- Códigos de saída são registrados, mas nenhum caso os exige (significado não documentado, C4-I23).
"""
import json
import os
import re
import subprocess
import sys

REPO, CPFILE, AGENT, OUT = sys.argv[1:5]
AQUI = os.path.dirname(os.path.abspath(__file__))
C4 = os.path.dirname(AQUI)
ORACULO = json.load(open(os.path.join(C4, "experimento", "oraculo.json"), encoding="utf-8"))
E = ORACULO["expressoes_proprias"]
os.makedirs(OUT, exist_ok=True)
EXEC_DIR = os.path.join(OUT, "execucoes")
os.makedirs(EXEC_DIR, exist_ok=True)
CP = open(CPFILE, encoding="utf-8").read().strip()
JACOCO_EXEC = os.path.join(OUT, "jacoco.exec").replace("\\", "/")
ERRO_MCDC = "claude-resultados/C4/experimento/entradas/erro-sintaxe.mcdc"

# Invocação real de cada execução do oráculo (nomes de opção confirmados no código após o congelamento:
# '--te' -> '--tests'; observação em --format json; erros vão para stderr).
ARGS = {
    "X01": ["analyze", E["E1"], "--format", "json"],
    "X02": ["analyze", E["E2"], "--format", "json"],
    "X03": ["analyze", E["E3"], "--format", "json"],
    "X04": ["analyze", E["E6"], "--format", "json"],
    "X05": ["analyze", E["E6"], "--unique-cause", "--format", "json"],
    "X06": ["analyze", E["DFRS"], "--format", "json"],
    "X07": ["analyze", E["E4"], "--constraint", "not p or q", "--format", "json"],
    "X08": ["analyze", "p and (q or r", "--format", "json"],
    "X09": ["analyze", "p and or q", "--format", "json"],
    "X10": ["analyze", "-f", "exemplos/requisitos.mcdc", "--format", "json"],
    "X11": ["analyze", "-f", ERRO_MCDC, "--format", "json"],
    "X12": ["analyze", "--json", "exemplos/vm-decisoes.json", "--format", "json"],
    "X13": ["analyze", "--json", "exemplos/tis-decisoes.json", "--format", "json"],
    "X14": ["analyze", "--json", "exemplos/npp-decisoes.json", "--format", "json"],
    "X15": ["analyze", "--json", "exemplos/decisoes.json", "--format", "json"],
    "X16": ["check", "--json", "exemplos/decisoes.json", "--tests", "exemplos/testes.csv", "--format", "json"],
    "X17": ["analyze", E["E7"], "--mutation", "--format", "json"],
    "X18": ["analyze", E["E5"], "--format", "json"],
}
SO_EXECUTAR = os.environ.get("C4_EXECUCOES")  # rodadas de extensão podem restringir execuções
if SO_EXECUTAR:
    ARGS = {k: v for k, v in ARGS.items() if k in SO_EXECUTAR.split(",")}

obs = {}
for x, args in ARGS.items():
    cmd = ["java", "-Dstdout.encoding=UTF-8", "-Dstderr.encoding=UTF-8",
           "-javaagent:%s=destfile=%s,append=true" % (AGENT, JACOCO_EXEC),
           "-cp", CP, "io.github.rvdomingos.mcdc.cli.Main"] + args
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, timeout=600)
    so, se = r.stdout.decode("utf-8"), r.stderr.decode("utf-8")
    with open(os.path.join(EXEC_DIR, x + ".stdout.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(so)
    with open(os.path.join(EXEC_DIR, x + ".stderr.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(se)
    try:
        js = json.loads(so)
    except ValueError:
        js = None
    obs[x] = {"args": args, "exit": r.returncode, "stdout": so, "stderr": se, "json": js}
    print(x, "exit", r.returncode, "json" if js is not None else "sem-json", flush=True)


# ----------------------------------------------------------------- utilidades de observação
def dec(x, i=0):
    return obs[x]["json"]["decisions"][i]


def dec_by(x, chave):
    for d in obs[x]["json"]["decisions"]:
        if d.get("id") == chave or d.get("requirement") == chave:
            return d
    raise KeyError(chave)


def labels(d):
    return [c["label"] for c in d["conditions"]]


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def recusa(x):
    o = obs[x]
    sem_relatorio = o["json"] is None and "decisions" not in o["stdout"]
    return sem_relatorio and "erro" in o["stderr"].lower(), "stdout=%r stderr=%r exit=%s" % (
        o["stdout"][:200], o["stderr"].strip()[:300], o["exit"])


def pares(d):
    return {k: {tuple(p) for p in v} for k, v in d["independencePairs"].items()}


# ----------------------------------------------------------------- verificações por caso
def v_D01():
    d = dec("X01"); return d["truthTableRows"] == 8 and len(d["truthTable"]) == 8, "truthTableRows=%s linhas=%d" % (d["truthTableRows"], len(d["truthTable"]))
def v_D02():
    r0 = dec("X01")["truthTable"][0]; return all(r0["values"].values()) and r0["outcome"] is True, "linha0=%s" % r0
def v_D03():
    t = dec("X01")["truthTable"]; n = sum(1 for r in t if r["outcome"]); return n == 1 and len(t) - n == 7, "verdadeiras=%d falsas=%d" % (n, len(t) - n)
def v_D04():
    t = dec("X02")["truthTable"]; f = [r for r in t if not r["outcome"]]
    return len(t) == 4 and len(f) == 1 and not any(f[0]["values"].values()), "linhas=%d falsas=%s" % (len(t), f)
def v_D05():
    d = dec("X03"); return d["truthTableRows"] == 8, "truthTableRows=%s" % d["truthTableRows"]
def v_D06():
    d = dec("X03"); return len(d["conditions"]) == 4, "condicoes=%s" % labels(d)
def v_D07():
    ls = labels(dec("X03")); return "p#1" in ls and "p#2" in ls, "labels=%s" % ls
def v_D08():
    ks = list(dec("X03")["independencePairs"].keys()); return "p#1" in ks and "p#2" in ks, "chaves de pares=%s" % ks
def v_D09():
    v = obs["X04"]["json"]["variant"]; return v == "MASKING", "variant=%s" % v
def v_D10():
    v = obs["X05"]["json"]["variant"]; return v == "UNIQUE_CAUSE", "variant=%s" % v
def v_D11():
    m, u = pares(dec("X04")), pares(dec("X05"))
    falta = {k: sorted(v - m.get(k, set())) for k, v in u.items() if v - m.get(k, set())}
    return not falta and bool(u), "causa_unica=%s mascaramento=%s fora=%s" % ({k: sorted(v) for k, v in u.items()}, {k: sorted(v) for k, v in m.items()}, falta)
def _sem_diag(d):
    return not d["uncovered"] and not d["uncoveredConditions"], "uncovered=%s uncoveredConditions=%s" % (d["uncovered"], d["uncoveredConditions"])
def v_D12():
    return _sem_diag(dec("X04"))
def v_D13():
    return _sem_diag(dec("X05"))
def v_D14():
    o = obs["X06"]
    if o["json"] is None:
        return False, "recusada: %s" % o["stderr"][:300]
    d = dec("X06")
    ins = {(i.get("variable"), i.get("operator"), str(i.get("value"))) for i in d["inputs"]}
    return len(d["conditions"]) == 2 and ins == {("speed", ">", "100"), ("mode", "=", "idle")}, "condicoes=%s inputs=%s" % (labels(d), d["inputs"])
def v_D15():
    o = obs["X06"]
    if o["json"] is None:
        return False, "recusada"
    d = dec("X06"); return d["truthTableRows"] == 4, "truthTableRows=%s" % d["truthTableRows"]
def v_D16():
    t = dec("X07")["truthTable"]; imp = [r["values"] for r in t if not r["feasible"]]
    alvo = all(v["p"] and not v["q"] for v in imp)
    return len(t) == 8 and len(imp) == 2 and alvo, "impossiveis=%s" % imp
def v_D17():
    d = dec("X07"); imp = {r["vector"] for r in d["truthTable"] if not r["feasible"]}
    usados = {v for ps in d["independencePairs"].values() for p in ps for v in p}
    return not (imp & usados), "impossiveis=%s usados_em_pares=%s" % (sorted(imp), sorted(usados))
def v_D18():
    return recusa("X08")
def v_D19():
    return recusa("X09")
def v_D20():
    ds = obs["X10"]["json"]["decisions"]; ids = [d.get("id") for d in ds]
    return ids == ["REQ-001", "REQ-002", "REQ-003"], "ids=%s" % ids
def _cc(chave, nc, nr):
    d = dec_by("X10", chave); return len(d["conditions"]) == nc and d["truthTableRows"] == nr, "condicoes=%s truthTableRows=%s" % (labels(d), d["truthTableRows"])
def v_D21():
    return _cc("REQ-001", 3, 8)
def v_D22():
    return _cc("REQ-002", 2, 4)
def v_D23():
    return _cc("REQ-003", 3, 4)
def v_D24():
    return _sem_diag(dec_by("X10", "REQ-001"))
def v_D25():
    return _sem_diag(dec_by("X10", "REQ-002"))
def v_D26():
    o = obs["X11"]; ok, det = recusa("X11")
    linha = re.search(r"(linha|line)\s*:?\s*3\b|:3\b", o["stderr"], re.I) is not None
    return ok and linha, det
def _sist(x, campo, esperado):
    ds = obs[x]["json"]["decisions"]
    val = {"req": len(ds), "cond": sum(len(d["conditions"]) for d in ds), "comb": sum(d["truthTableRows"] for d in ds)}[campo]
    return val == esperado, "%s=%s" % (campo, val)
def v_D27(): return _sist("X12", "req", 5)
def v_D28(): return _sist("X12", "cond", 21)
def v_D29(): return _sist("X12", "comb", 152)
def v_D30(): return _sist("X13", "req", 17)
def v_D31(): return _sist("X13", "cond", 69)
def v_D32(): return _sist("X13", "comb", 268)
def v_D33(): return _sist("X14", "req", 11)
def v_D34(): return _sist("X14", "cond", 29)
def v_D35(): return _sist("X14", "comb", 76)
def v_D36():
    return obs["X15"]["json"] is not None, "json_valido=%s" % (obs["X15"]["json"] is not None)
def v_D37():
    ds = obs["X15"]["json"]["decisions"]
    ids = {d.get("id") for d in ds}; reqs = {d.get("requirement") for d in ds}
    alvo_ids = {"the_coffee_machine_system#%d" % i for i in range(1, 5)}
    alvo_req = {"REQ-00%d" % i for i in range(1, 5)}
    return len(ds) == 4 and (ids == alvo_ids or reqs == alvo_req), "ids=%s requirements=%s" % (sorted(map(str, ids)), sorted(map(str, reqs)))
def _chk(did):
    for d in obs["X16"]["json"]["decisions"]:
        if d["id"] == did:
            return d
    raise KeyError(did)
def v_D38():
    pr = _chk("the_coffee_machine_system#3")["problems"]; return any(p.startswith("T4") for p in pr), "problems=%s" % pr
def v_D39():
    pr = [p for d in obs["X16"]["json"]["decisions"] for p in d["problems"]]
    return not any(re.match(r"T[123]\b", p) for p in pr), "problems=%s" % pr
def _cond_dem(d, *trechos):
    out = {}
    for c in d["conditions"]:
        lab = norm(c["condition"])
        for t in trechos:
            if all(w in lab for w in t.split()):
                out[t] = c["demonstrated"]
    return out
def v_D40():
    d = _chk("the_coffee_machine_system#1"); dm = _cond_dem(d, "the_system_mode idle")
    return d["complete"] is False and dm.get("the_system_mode idle") is False, "complete=%s demonstrada=%s" % (d["complete"], dm)
def v_D41():
    d = _chk("the_coffee_machine_system#3"); dm = _cond_dem(d, "the_coffee_request_button", "the_coin_sensor")
    return d["complete"] is False and dm.get("the_coffee_request_button") is False and dm.get("the_coin_sensor") is False, "complete=%s demonstradas=%s" % (d["complete"], dm)
def v_D42():
    a, b = _chk("the_coffee_machine_system#2"), _chk("the_coffee_machine_system#4")
    return a["complete"] is False and b["complete"] is False, "#2 complete=%s testes=%d; #4 complete=%s testes=%d" % (a["complete"], len(a["tests"]), b["complete"], len(b["tests"]))
def v_D43():
    o = obs["X17"]
    if o["json"] is None:
        return False, "sem relatório: %s" % o["stderr"][:300]
    m = dec("X17").get("mutation")
    tipos = set((m or {}).get("faults", {}).keys())
    seis = {"ORF", "ENF", "VNF", "MVF", "VRF", "ASF"}
    return seis <= tipos, "tipos=%s faltando=%s" % (sorted(tipos), sorted(seis - tipos))
def v_D44():
    o = obs["X18"]
    if o["json"] is None:
        return False, "sem relatório: %s" % o["stderr"][:300]
    d = dec("X18"); return d["truthTableRows"] == 1048576, "truthTableRows=%s" % d["truthTableRows"]
def v_D45():
    o = obs["X18"]
    if o["json"] is None:
        return False, "sem relatório"
    d = dec("X18")
    lab = [c["label"] for c in d["conditions"] if c["input"] == "x01"][0]
    n = len(d["independencePairs"].get(lab, []))
    return n <= 1000, "pares_guardados(%s)=%d pairsTruncated=%s" % (lab, n, d.get("pairsTruncated"))


resultados = []
for c in ORACULO["casos"]:
    item = {"id": c["id"], "status_oraculo": c["status"], "execucao": c["execucao"], "expectativa": c["expectativa"]}
    if c["status"] == "INDETERMINADO":
        item.update({"resultado": "INDETERMINADO", "observado": "não executado (sem expectativa documental única)"})
    else:
        xs = c["execucao"].split("+")
        if not all(x in obs for x in xs):
            item.update({"resultado": "NAO_EXECUTADO_NESTA_RODADA", "observado": "-"})
        else:
            fn = globals()["v_" + c["id"].split("-")[1]]
            try:
                ok, det = fn()
                item.update({"resultado": "PASSOU" if ok else "FALHOU", "observado": det})
            except Exception as ex:  # erro do harness/observação: operacional, não é falha semântica
                item.update({"resultado": "ERRO_TECNICO", "observado": "erro ao observar: %r" % ex})
        item["exit_codes"] = {x: obs[x]["exit"] for x in xs if x in obs}
    resultados.append(item)

cont = {}
for r in resultados:
    cont[r["resultado"]] = cont.get(r["resultado"], 0) + 1
with open(os.path.join(OUT, "resultados.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump({"contagem": cont, "execucoes": {x: {"args": o["args"], "exit": o["exit"]} for x, o in obs.items()},
               "casos": resultados}, f, ensure_ascii=False, indent=1)
print(json.dumps(cont, ensure_ascii=False))
