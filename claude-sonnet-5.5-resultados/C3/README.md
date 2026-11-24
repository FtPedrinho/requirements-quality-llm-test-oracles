# C3 — Claude Sonnet 5.5 (segunda tentativa, critério estrito)

Condição C3 (fonte `tool-readme-C3.md`, SHA-256 `F18B0821D79C7315486C13D5260FA2F6D6E9418EF03B86CDE58E66B91B7B87A3`).
A primeira tentativa (oráculo mais permissivo: 48 determinados, 47 passaram, 1 falhou, 70,52 %) está preservada em [`tentativa-1/`](tentativa-1/README.md). Esta segunda foi refeita a pedido do pesquisador, com critério estrito, e é a que vale como resultado de C3.

| Métrica | Resultado |
|---|---|
| Branch Coverage | 835 / 1296 = 64,43 % (JaCoCo 0.8.16, 69 classes) |
| Aprovados | 40 |
| Falhos | 0 |
| Indeterminados | 32 (registrados, não executados) |

- [`avaliacao/relatorio.md`](avaliacao/relatorio.md), [`avaliacao/resultados-por-caso.csv`](avaliacao/resultados-por-caso.csv)
- [`experimento/`](experimento/README.md), [`resultados/`](resultados/), [`suite/`](suite/README.md)
