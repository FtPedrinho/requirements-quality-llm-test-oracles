"""Gera os oraculos 'so determinados' do C0 a partir dos oraculos congelados, sem alterar nenhum caso."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); E = os.path.dirname(H)
for src, dst in (("oraculo/oraculo.json", "oraculo-determinados.json"), ("extensao-1/oraculo-extensao-1.json", "oraculo-extensao-1-determinados.json")):
    d = json.load(open(os.path.join(E, src), encoding="utf-8"))
    det = [c for c in d["casos"] if c["status"] == "DETERMINADO"]
    d["casos"] = det; d["filtro"] = f"somente DETERMINADO de {src} (casos copiados sem alteracao)"
    json.dump(d, open(os.path.join(H, dst), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    print(dst, len(det))
