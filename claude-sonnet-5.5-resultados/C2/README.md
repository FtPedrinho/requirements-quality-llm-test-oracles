# Experimento C2 (Claude Sonnet 5.5)

Condição C2: `experimentacao-pesquisa/experimentacao-2/documentation/tool-readme-C2.md` (SHA-256 `61C4062B…EFBE1`). Relatório completo no modelo do
protocolo: [`avaliacao/relatorio.md`](avaliacao/relatorio.md); veredito por caso: [`avaliacao/resultados-por-caso.csv`](avaliacao/resultados-por-caso.csv).

- `avaliacao/`: relatório (métricas, avaliação, limitações) e resultados por caso (acumulado).
- `experimento/`: análise documental (`analise-oraculo.md`), `oraculo.json` e `oraculo-extensao1.json`, geradores, Z3 (`z3/gerar_smt.py`, `z3/smt/`),
  congelamentos SHA-256 (`congelamento/01-oraculo`, `02-suite` — este inclui as extensões) e `README.md` do experimento.
- `resultados/`: `rodada-01-baseline/`, `rodada-02-extensoes/` (extensões 1–3) e `acumulado/` (JaCoCo acumulado).
- `suite/`: suíte pytest do baseline (`test_c2.py`) e das extensões (`test_c2_ext1/2/3.py`).
- `reorganizacao.md`: registro da reorganização de pastas.
