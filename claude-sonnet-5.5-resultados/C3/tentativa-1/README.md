# C3 — Claude Sonnet 5.5

Experimento da condição C3 (fonte `tool-readme-C3.md`, SHA-256 `F18B0821D79C7315486C13D5260FA2F6D6E9418EF03B86CDE58E66B91B7B87A3`), independente das demais condições.

| Métrica | Resultado |
|---|---|
| Branch Coverage | 914 / 1296 = 70,52 % (JaCoCo 0.8.16, 69 classes) |
| Aprovados | 47 |
| Falhos | 1 (`C3-D15`) |
| Indeterminados | 24 (não executados) |

- [`avaliacao/relatorio.md`](avaliacao/relatorio.md), [`avaliacao/resultados-por-caso.csv`](avaliacao/resultados-por-caso.csv)
- [`experimento/`](experimento/README.md): oráculo, análise, Z3, congelamento
- [`resultados/`](resultados/): `rodada-01-baseline/`, `acumulado/` (sem rodada de extensões)
- [`suite/`](suite/README.md): suíte pytest e entradas
