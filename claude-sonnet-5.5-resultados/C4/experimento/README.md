# Experimento C4 — oráculo, Z3 e congelamento

Conteúdo:

* `analise-oraculo.md`: inventário do texto C4, decisões e indeterminações.
* `oraculo.json` / `oraculo-casos.csv`: 78 casos (42 DETERMINADOS D01–D42 e 36
  INDETERMINADOS I01–I36) com entrada, pré-condição, trecho literal, regra,
  expectativa ou motivo.
* `gerar_oraculo.py`, `gerar_z3.py`: geradores (o oráculo e as consultas são
  reproduzíveis: `python gerar_oraculo.py`, `python gerar_z3.py`).
* `z3/`: consultas `.smt2`, respostas `.out` e `resumo-z3.csv` (Z3 5.4.1
  standalone, independente do `mcdc-z3`; 56 verificações, nenhuma `unknown`).
* `congelamento/`: `01-oraculo.sha256` (antes de ler o SUT, autorrevisão),
  `02-suite.sha256` (antes do baseline), `03-resultados-baseline.sha256`.

## Ordem dos fatos

1. Hash da fonte C4 conferido antes de ler. 2. Leitura de protocolo e fonte.
3. Oráculo, SMT-LIB e Z3. 4. Congelamento 01 (autorrevisão). 5. Só então
inspeção do SUT (`Main.java`, amostra de saída `exemplos/saidas/vm-relatorio.json`
e execuções de sondagem da CLI) **apenas** para saber invocar e medir.
6. Suíte, congelamento 02, uma execução baseline com JaCoCo.

## Perdas de isolamento / desvios

Ver `../avaliacao/relatorio.md` (seção de limitações). Em particular: o Z3 foi
mantido no `PATH` em todos os casos (o texto C4 é contraditório sobre isso).
