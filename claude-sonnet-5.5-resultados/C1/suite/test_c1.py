"""Suite pytest C1 - testa a ferramenta MC/DC real contra o oraculo congelado.

Cada caso DETERMINADO de detalhes-C1/oraculo.json vira exatamente um teste
(unidade de contagem = caso). As expectativas vem so do oraculo; nenhuma foi
ajustada ao comportamento observado. Casos INDETERMINADOS nao sao executados.

Variaveis de ambiente:
  MCDC_ROOT   raiz do repositorio (padrao: ancestral que contem mcdc-cli)
  C1_BRUTO    pasta para a saida bruta de cada invocacao
  Z3_DIR      pasta do z3.exe, adicionada ao PATH so nos casos que usam Z3
"""
import csv
import io
import json
import os
import subprocess
import tempfile

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ORACULO = os.path.join(HERE, "..", "detalhes-C1", "oraculo.json")


def _root():
    r = os.environ.get("MCDC_ROOT")
    if r:
        return r
    d = HERE
    while True:
        if os.path.isdir(os.path.join(d, "mcdc-cli")):
            return d
        p = os.path.dirname(d)
        if p == d:
            raise RuntimeError("raiz do repositorio nao encontrada")
        d = p


ROOT = _root()
Z3_DIR = os.environ.get("Z3_DIR", r"C:\Users\User\AppData\Roaming\Python\bin")
BRUTO = os.environ.get("C1_BRUTO", os.path.join(HERE, "..", "resultados", "bruto"))

with open(ORACULO, encoding="utf-8") as fh:
    ORA = json.load(fh)
CASOS = [c for c in ORA["casos"] if c["status"] == "DETERMINADO"]
FIXTURES = ORA["fixtures"]


class ErroTecnico(Exception):
    """Falha de infraestrutura (JVM, timeout, solver): nao e falha semantica."""


def _classpath():
    with open(os.path.join(ROOT, "mcdc-cli", "target", "classpath.txt"), encoding="utf-8") as fh:
        deps = fh.read().strip()
    return os.path.join(ROOT, "mcdc-cli", "target", "classes") + ";" + deps


CP = _classpath()


def _usa_z3(args):
    return args[0] == "verify" or any(a in ("--z3", "--exact", "--direct") for a in args)


def invocar(args, tag):
    env = dict(os.environ)
    if _usa_z3(args):
        env["PATH"] = Z3_DIR + os.pathsep + env.get("PATH", "")
    cmd = ["java", "-Dstdout.encoding=UTF-8", "-Dstderr.encoding=UTF-8", "-cp", CP,
           "io.github.rvdomingos.mcdc.cli.Main"] + args
    try:
        p = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, timeout=180)
    except (subprocess.TimeoutExpired, OSError) as e:
        raise ErroTecnico(f"{type(e).__name__}: {e}")
    out = p.stdout.decode("utf-8", "replace")
    err = p.stderr.decode("utf-8", "replace")
    os.makedirs(BRUTO, exist_ok=True)
    with open(os.path.join(BRUTO, tag + ".txt"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("$ mcdc " + " ".join(args) + f"\n[exit {p.returncode}]\n--- stdout ---\n{out}\n--- stderr ---\n{err}\n")
    return p.returncode, out, err


def _resolve(args, tmp):
    res = []
    for a in args:
        if a.startswith("fx:"):
            name = a[3:]
            path = os.path.join(tmp, name)
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(FIXTURES[name])
            res.append(path)
        else:
            res.append(a.replace("{tmp}", tmp))
    return res


def _csv_rows(text):
    return list(csv.DictReader(io.StringIO(text)))


def _metricas(out):
    d = json.loads(out)
    ds = d["decisions"]
    reqs = {x.get("requirement") for x in ds if x.get("requirement")}
    m = {
        "requisitos": len(reqs) if reqs else len(ds),
        "condicoes": sum(len(x.get("conditions", [])) for x in ds),
        "combinacoes": sum(x.get("truthTableRows", 0) for x in ds),
        "impossiveis": sum(1 for x in ds for r in x.get("truthTable", []) if r.get("feasible") is False),
        "testes": sum(len(x.get("minimalSuite", [])) for x in ds),
    }
    mutantes = eq = 0
    for x in ds:
        for f in (x.get("mutation") or {}).get("faults", {}).values():
            mutantes += f.get("total", 0)
            eq += f.get("equivalent", 0)
    m["mutantes"] = mutantes
    m["equivalentes"] = eq
    return m


def _args_do_caso(caso, variante):
    cli = list(caso["cli"])
    if "expr" in caso:
        cli = [caso["expr"] if a.startswith("<") and a.endswith("entradas>") else a for a in cli]
    if variante is not None:
        cli = [a.replace("<grafia>", variante).replace("<op>", variante) for a in cli]
    return cli


def _variantes(caso):
    if "variantes" not in caso:
        return [None]
    return caso["variantes"]


def _expr_com_variante(caso, v):
    cli = list(caso["cli"])
    if "expr" in caso:
        cli = [caso["expr"] if (a.startswith("<") and "entradas" in a) else a for a in cli]
    if v is not None:
        if any("<grafia>" in a for a in cli):
            cli = [a.replace("<grafia>", v) for a in cli]
        else:  # A12: operador de comparacao
            cli = [a.replace("speed <op> 100", v) for a in cli]
    return cli


def _checa(caso, args, rc, out, err, tmp, falhas):
    e = caso["expectativa"]
    comb = (out + "\n" + err).lower()
    if "exit" in e and rc != e["exit"]:
        falhas.append(f"exit esperado {e['exit']}, observado {rc}")
    if "exit_em" in e and rc not in e["exit_em"]:
        falhas.append(f"exit esperado em {e['exit_em']}, observado {rc}")
    for t in e.get("contem", []):
        if t.lower() not in comb:
            falhas.append(f"saida nao contem {t!r}")
    for t in e.get("nao_contem", []):
        if t.lower() in comb:
            falhas.append(f"saida contem {t!r} indevidamente")
    if "n_testes" in e:
        try:
            n = len({r["test"] for r in _csv_rows(out)})
        except Exception as ex:
            n = f"csv ilegivel ({ex})"
        if n != e["n_testes"]:
            falhas.append(f"n_testes esperado {e['n_testes']}, observado {n}")
    if "n_linhas_csv" in e:
        n = len([l for l in out.splitlines() if l.strip()])
        if n not in e["n_linhas_csv"]:
            falhas.append(f"linhas csv esperadas em {e['n_linhas_csv']}, observado {n}")
    if any(k in e for k in ("n_linhas_verdade", "n_resultado_verdadeiro", "linha0_todo_verdadeiro")):
        try:
            rows = _csv_rows(out)
            cols = list(rows[0].keys())
            ins = cols[cols.index("row") + 1: cols.index("outcome")]
            if "n_linhas_verdade" in e and len(rows) != e["n_linhas_verdade"]:
                falhas.append(f"linhas da tabela esperadas {e['n_linhas_verdade']}, observado {len(rows)}")
            if "n_resultado_verdadeiro" in e:
                nv = sum(1 for r in rows if r["outcome"] == "T")
                if nv != e["n_resultado_verdadeiro"]:
                    falhas.append(f"resultados verdadeiros esperados {e['n_resultado_verdadeiro']}, observado {nv}")
            if e.get("linha0_todo_verdadeiro") and not all(rows[0][c] == "T" for c in ins):
                falhas.append("linha 0 nao e toda verdadeira")
        except Exception as ex:
            falhas.append(f"tabela-verdade ilegivel: {type(ex).__name__}: {ex}")
    if e.get("json_valido"):
        try:
            json.loads(out)
        except Exception as ex:
            falhas.append(f"JSON invalido: {ex}")
    if "arquivo_nao_vazio" in e:
        p = e["arquivo_nao_vazio"].replace("{tmp}", tmp)
        if not os.path.exists(p) or os.path.getsize(p) == 0:
            falhas.append("arquivo de saida ausente ou vazio")
        elif e.get("tela_sem_relatorio"):
            with open(p, encoding="utf-8", errors="replace") as fh:
                conteudo = fh.read().strip()
            if conteudo and conteudo in out:
                falhas.append("relatorio tambem foi mostrado na tela")
    if "metricas_sistema" in e:
        try:
            m = _metricas(out)
            for k, v in e["metricas_sistema"].items():
                if m[k] != v:
                    falhas.append(f"{k} esperado {v}, observado {m[k]}")
        except Exception as ex:
            falhas.append(f"metricas ilegiveis: {type(ex).__name__}: {ex}")


@pytest.mark.parametrize("caso", CASOS, ids=[c["id"] for c in CASOS])
def test_caso(caso):
    falhas = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, v in enumerate(_variantes(caso)):
            args = _resolve(_expr_com_variante(caso, v), tmp)
            rc, out, err = invocar(args, f"{caso['id']}-{i}")
            sub = []
            _checa(caso, args, rc, out, err, tmp, sub)
            falhas += [(f"[{v}] " if v is not None else "") + s for s in sub]
    assert not falhas, "; ".join(falhas)
