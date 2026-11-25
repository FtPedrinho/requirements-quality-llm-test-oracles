# C4 — Claude Sonnet 5.5

Experimento independente da condição C4 (documentação degradada e com conflitos), critério estrito: documentação como verdade, indeterminado quando não há expectativa única.

## Resultado do baseline (acumulado = baseline; sem extensões)

| Métrica | Resultado |
|---|---|
| Branch Coverage | 626 / 1296 = 48,30 % (JaCoCo 0.8.16, 69 classes) |
| Testes aprovados | 42 |
| Testes falhos | 0 |
| Testes indeterminados | 36 (registrados, não executados) |

Unidade: um caso do oráculo = um teste. Revisão do oráculo: autorrevisão.

## Documentação normativa usada

* [documentacao/tool-readme-C4.md](documentacao/tool-readme-C4.md): cópia da fonte C4, idêntica à de `experimentacao-pesquisa/experimentacao-4/`.
* [documentacao/SHA256.txt](documentacao/SHA256.txt): `D6BC0A588CD9A7DF7F1F566573944FA5CB1707BBA676B4E9854CAD2CC5440FC2` (conferido antes da leitura).

## Suíte de testes

* [suite/](suite/): suíte pytest (`test_c4_oraculo.py`, 42 testes `test_C4_Dnn_...`), utilitário de invocação da CLI, dados de entrada e [README](suite/README.md).
* Hash congelado antes da execução: [experimento/congelamento/02-suite.sha256](experimento/congelamento/02-suite.sha256).

## Oráculo, Z3 e detalhes

* [experimento/analise-oraculo.md](experimento/analise-oraculo.md): inventário do texto, decisões e indeterminações.
* [experimento/oraculo.json](experimento/oraculo.json) e `oraculo-casos.csv`: 42 determinados (D01–D42) e 36 indeterminados (I01–I36), com trecho literal, regra, expectativa ou motivo.
* [experimento/z3/](experimento/z3/): consultas SMT-LIB, respostas do Z3 5.4.1 e `resumo-z3.csv` (56 verificações, nenhuma `unknown`).
* [experimento/README.md](experimento/README.md) e `congelamento/` (hashes 01, 02, 03); geradores `gerar_oraculo.py` e `gerar_z3.py`.

## Resultados e avaliação

* [avaliacao/relatorio.md](avaliacao/relatorio.md): relatório no modelo do protocolo (fontes, Z3, métricas, evidências, desvios, limitações, perdas de isolamento).
* [avaliacao/resultados-por-caso.csv](avaliacao/resultados-por-caso.csv): PASSOU/FALHOU/INDETERMINADO por caso.
* [resultados/rodada-01-baseline/](resultados/rodada-01-baseline/): saídas brutas da CLI, JUnit, `jacoco.exec`, CSV/XML/HTML do JaCoCo, saída do pytest; [resultados/acumulado/](resultados/acumulado/).
