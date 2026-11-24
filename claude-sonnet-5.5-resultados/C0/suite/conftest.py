"""Infra da suíte C0: execução do MC/DC real e registro bruto de cada caso."""
import json, os, re, shutil, subprocess, time
import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))           # raiz do repositório
ORACULO = os.path.join(AQUI, "..", "experimento", "oraculo.json")
WORK = os.path.join(AQUI, "work")
REL_WORK = os.path.relpath(WORK, RAIZ).replace("\\", "/")
Z3_DIR = os.environ.get("Z3_DIR", r"C:\Users\User\AppData\Roaming\Python\bin")
JACOCO_AGENT = os.environ.get("JACOCO_AGENT")           # caminho do agente (opcional)
JACOCO_EXEC = os.environ.get("JACOCO_EXEC")             # arquivo .exec de destino
RAW = os.environ.get("MCDC_RAW_DIR", os.path.join(AQUI, "..", "resultados", "rodada-01-baseline", "bruto"))
TIMEOUT = 180


def classpath():
    """Mesmo classpath de mcdc-cli/target/classpath.txt, com os JARs dos módulos
    trocados pelos diretórios target/classes (mesmas classes; permite relatório JaCoCo exato)."""
    cp = open(os.path.join(RAIZ, "mcdc-cli", "target", "classpath.txt"), encoding="utf-8").read().strip()
    partes = [os.path.join(RAIZ, "mcdc-cli", "target", "classes")]
    for p in cp.split(";"):
        m = re.search(r"(mcdc-[a-z0-9]+)[\/]target[\/]mcdc-[a-z0-9]+-0\.1\.0-SNAPSHOT\.jar$", p)
        partes.append(os.path.join(RAIZ, m.group(1), "target", "classes") if m else p)
    return ";".join(partes)


def executar(args, usa_z3, extra_env=None):
    env = dict(os.environ)
    path = env.get("PATH", "")
    if usa_z3:
        path = Z3_DIR + os.pathsep + path
    env["PATH"] = path
    if JACOCO_AGENT and JACOCO_EXEC:
        env["JAVA_TOOL_OPTIONS"] = "-javaagent:%s=destfile=%s,append=true,output=file" % (
            JACOCO_AGENT.replace("\\", "/"), JACOCO_EXEC.replace("\\", "/"))
    cmd = ["java", "-cp", classpath(), "io.github.rvdomingos.mcdc.cli.Main"] + list(args)
    t0 = time.time()
    r = subprocess.run(cmd, cwd=RAIZ, env=env, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=TIMEOUT)
    return {"cmd": cmd[4:], "exit": r.returncode, "stdout": r.stdout, "stderr": r.stderr,
            "segundos": round(time.time() - t0, 3)}


def carregar_casos():
    return json.load(open(ORACULO, encoding="utf-8"))["casos"]


def preparar(caso):
    d = os.path.join(WORK, caso["id"])
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    for nome, conteudo in (caso.get("files") or {}).items():
        with open(os.path.join(d, nome), "w", encoding="utf-8", newline="\n") as f:
            f.write(conteudo)
    rel = REL_WORK + "/" + caso["id"]
    resolve = lambda a: a.replace("@F/", rel + "/").replace("@OUT/", rel + "/")
    return [resolve(a) for a in caso["args"]], d


def salvar_bruto(caso_id, obs):
    os.makedirs(RAW, exist_ok=True)
    with open(os.path.join(RAW, caso_id + ".json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(obs, f, ensure_ascii=False, indent=2)
