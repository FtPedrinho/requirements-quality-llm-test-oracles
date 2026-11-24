# Experimento C1 (Claude Sonnet 5.5)

Condição C1: `experimentacao-pesquisa/experimentacao-1/documentation/tool-readme-C1.md`. Relatório completo no modelo do protocolo:
[`avaliacao/relatorio.md`](avaliacao/relatorio.md); veredito por caso: [`avaliacao/resultados-por-caso.csv`](avaliacao/resultados-por-caso.csv).

- `avaliacao/`: relatório (métricas, avaliação, limitações) e resultados por caso (acumulado).
- `experimento/`: análise documental (`analise-oraculo.md`), `oraculo.json`, Z3 (`z3/gerar_smt.py`, `z3/smt/`),
  congelamentos SHA-256 (`congelamento/01-oraculo`, `02-suite`, `03-extensao`) e `README.md` do experimento.
- `resultados/`: `rodada-01-baseline/`, `rodada-02-extensao/` e `acumulado/` (brutos, JUnit, JaCoCo).
- `suite/`: suíte pytest do baseline e da extensão.
- `reorganizacao.md`: registro da reorganização de pastas (layout alinhado às demais LLMs).
