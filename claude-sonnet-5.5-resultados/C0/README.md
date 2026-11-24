# Experimento C0 (Claude Sonnet 5.5)

Condição C0: documentação original (`experimentacao-pesquisa/documentacao-original/tool-readme-original.md`). Relatório completo no
modelo do protocolo: [`avaliacao/relatorio.md`](avaliacao/relatorio.md); veredito por caso: [`avaliacao/resultados-por-caso.csv`](avaliacao/resultados-por-caso.csv).

- `avaliacao/`: relatório (métricas, avaliação, limitações) e resultados por caso.
- `experimento/`: análise documental (`analise-oraculo.md`), `oraculo.json`, geradores, consultas SMT-LIB e respostas Z3 (`z3/`),
  congelamentos SHA-256 (`congelamento/01-oraculo`, `02-suite`) e `README.md` do experimento.
- `resultados/rodada-01-baseline/`: saídas brutas (`bruto/`), JUnit e cobertura JaCoCo (`cobertura/`).
- `suite/`: suíte pytest (um teste por caso determinado) e dados de trabalho.
- `reorganizacao.md`: registro da reorganização de pastas (layout alinhado às demais LLMs).
