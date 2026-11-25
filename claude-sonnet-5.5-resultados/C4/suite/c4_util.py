# -*- coding: utf-8 -*-
"""Utilitarios da suite C4: invocacao da CLI mcdc (sem Maven), captura de brutos."""
import json
import os
import subprocess
from functools import lru_cache
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
Z3_DIR = r"C:\Users\User\AppData\Roaming\Python\bin"
RAW = Path(os.environ.get("C4_RAW_DIR", str(RAIZ / "claude-sonnet-5.5-resultados" / "C4" / "resultados" / "_tmp-brutos")))
_contador = [0]


@lru_cache(maxsize=1)
def classpath():
    cp = (RAIZ / "mcdc-cli" / "target" / "classpath.txt").read_text(encoding="utf-8").strip()
    return str(RAIZ / "mcdc-cli" / "target" / "classes") + ";" + cp


def executar(*args, timeout=900):
    """Roda a CLI com Z3 no PATH. Retorna dict(args, rc, out, err). Grava brutos."""
    chave = tuple(args)
    return _executar(chave, timeout)


@lru_cache(maxsize=None)
def _executar(args, timeout):
    env = dict(os.environ)
    env["PATH"] = Z3_DIR + os.pathsep + env.get("PATH", "")
    cmd = ["java", "-Dstdout.encoding=UTF-8", "-Dstderr.encoding=UTF-8", "-Xmx3g", "-cp", classpath(),
           "io.github.rvdomingos.mcdc.cli.Main", *args]
    r = subprocess.run(cmd, cwd=RAIZ, env=env, capture_output=True, timeout=timeout)
    out = r.stdout.decode("utf-8", errors="replace")
    err = r.stderr.decode("utf-8", errors="replace")
    _contador[0] += 1
    RAW.mkdir(parents=True, exist_ok=True)
    base = RAW / f"exec-{_contador[0]:03d}"
    resumo = {"args": [a if len(a) < 400 else a[:400] + "..." for a in args], "returncode": r.returncode}
    base.with_suffix(".meta.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=1), encoding="utf-8")
    if len(out) < 2_000_000:
        base.with_suffix(".out.txt").write_text(out, encoding="utf-8")
    else:
        base.with_suffix(".out.txt").write_text(out[:2_000_000] + "\n[truncado no bruto: saida maior que 2 MB]\n", encoding="utf-8")
    base.with_suffix(".err.txt").write_text(err, encoding="utf-8")
    return {"args": args, "rc": r.returncode, "out": out, "err": err}


def json_da(*args):
    r = executar(*args)
    try:
        return json.loads(r["out"])
    except json.JSONDecodeError as e:
        raise AssertionError(f"saida nao e JSON valido ({e}); rc={r['rc']}; stderr={r['err'][:300]!r}")


def nomes(n, prefixo="x"):
    return [f"{prefixo}{i:02d}" for i in range(1, n + 1)]
