"""Gera avaliacao/resultados-por-caso.md a partir dos oráculos congelados e dos resultados das rodadas.
Uso (na pasta claude-resultados/C1): python -I avaliacao/gerar_resultados_por_caso.py"""
import json


def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


o1 = json.load(open("experimento/oraculo.json", encoding="utf-8"))["casos"]
o2 = json.load(open("experimento/extensao-01/oraculo-extensao-01.json", encoding="utf-8"))["casos"]
load = lambda p: {r["id"]: r for r in json.load(open(p, encoding="utf-8"))}
r1 = load("resultados/rodada-01-baseline/resultados.json")
r2 = load("resultados/rodada-02-correcao/resultados.json")
r3 = load("resultados/rodada-03-extensao-01/resultados.json")
L = ["# Resultados por caso — C1", "",
     "Unidade de contagem: um caso = um ID do oráculo (todas as suas asserções precisam valer para PASSOU).",
     "`rodada-01` = baseline (preservado); `rodada-02` = mesma suíte com a correção 01 (codificação do stdout), "
     "referência do baseline corrigido; `rodada-03` = extensão 01. O veredito final é o da rodada-02 (AN/SY/CK/VF) "
     "ou da rodada-03 (EX).", "",
     "| ID | Oráculo | rodada-01 | Veredito final | Códigos de saída observados | Expectativa / observação |",
     "|---|---|---|---|---|---|"]
cnt = {}
for c in o1 + o2:
    fin = r2.get(c["id"]) or r3.get(c["id"])
    base = r1.get(c["id"], {}).get("veredito", "—")
    if c["id"] == "AN-22":
        base = "FALHOU\\*"
    v = fin["veredito"]
    cnt[v] = cnt.get(v, 0) + 1
    exits = ", ".join(str(x["exit"]) for x in fin["comandos"])
    if c["status"] == "INDETERMINADO":
        det = "INDETERMINADO: " + c["justificativa"] + " (executado só como diagnóstico)"
    else:
        det = json.dumps(c["expectativa"], ensure_ascii=False)
        bad = [x["verificacao"] for x in fin["verificacoes"] if not x["ok"]]
        if bad:
            det += " — **falhou:** " + "; ".join(bad)
    L.append(f"| {c['id']} | {c['status']} | {base} | **{v}** | {exits} | {esc(det)} |")
L += ["", "\\* AN-22 na rodada-01: FALHOU por erro técnico de medição (stdout da JVM em Cp1252 decodificado como "
      "UTF-8); reclassificado como erro técnico, ver `experimento/correcoes/correcao-01-codificacao-stdout.md`. "
      "Na rodada-02 PASSOU, sem mudança de expectativa.", "",
      "Totais finais: " + ", ".join(f"{k}: {v}" for k, v in sorted(cnt.items())) + f" (total {sum(cnt.values())})."]
open("avaliacao/resultados-por-caso.md", "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print(cnt)
