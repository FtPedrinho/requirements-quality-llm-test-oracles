# Extensão 01 — justificativa

- Motivo: a cobertura da rodada-02 (1042/1296 branches) localizou branches não exercitados em
  `Predicate` (comparações com valores concretos), `TestCasesFile` (aspas, células vazias), `Main`
  (validação de opções), `SmtEncoding` (negativos, reais, comparação entre variáveis, modelos com
  `(- n)` e `(/ a b)`), `Z3DirectAnalyzer` (restrição, causa única, redundância/bloqueio), `CsvReport`
  (aspas), `ExpressionParser` (tokens sobrando, operador fora de lugar), `TextReport` (requisito e ações)
  e `IndependencePairs` (teto de pares).
- Regra: a cobertura só indicou ONDE procurar. Cada caso EX-xx tem trecho literal do C1 e, quando cabe,
  consulta Z3 independente (`z3/`). Sem suporte documental => INDETERMINADO (EX-29, EX-30, EX-31).
- Interpretações registradas: EX-01 usa o tipo `int`, que não aparece no texto do C1 mas aparece no
  arquivo de entrada `exemplos/decisoes.json` citado pelo C1 para o `check`; EX-18 aplica por analogia
  o exemplo literal `speed > 100 → 100 e 101` a `x > -3 → -3 e -2`; EX-13/EX-14 não dependem do tipo
  (Int ou Real dão as mesmas linhas impossíveis no Z3).
- 31 casos: 28 DETERMINADO, 3 INDETERMINADO. Oráculo: `oraculo-extensao-01.json`.
- Suíte: `suite/run_suite.py` recebeu só novos extratores (stderr_contem, csv_coluna_igual,
  impossiveis_formula, guarda_py, fronteiras_incluem, pares_max, blocos_linhas) e a opção `--entradas`;
  a versão da rodada-02 está em `suite/versoes/run_suite.rodada-02.py`. Expectativas anteriores não mudam.
- Execução: `resultados/rodada-03-extensao-01/` (só os 31 casos novos) e
  `resultados/acumulado/` (merge do jacoco.exec das rodadas 02 e 03).
