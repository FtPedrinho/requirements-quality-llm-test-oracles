# Extensão 1 do C0

- **Por quê:** a rodada 2 deixou sem cobertura desvios em `SmtEncoding`, `Predicate`, `Z3DirectAnalyzer`, `TestCasesFile`, `CsvReport` e `Mcdc`. Ali o README C0 documenta comportamentos que eu ainda não tinha testado: comparações numéricas e de enumeração com o Z3, o modo direto com redundância, bloqueio e causa única, `--exact` em causa única, a coluna `decision` e as aspas no CSV, e a linha do erro.
- **Regra:** a cobertura só apontou onde procurar. Cada expectativa cita o README e, quando é pertinente, tem consultas Z3 em `z3/` (42/42 conforme).
- **Casos:** 22, sendo 21 determinados e 1 indeterminado (X22: `--z3` no verify).
- **Mudanças no runner** (`suite/executar_suite.py`), todas aditivas: o arquivo de oráculo pode vir da variável `ORACULO`, há o marcador `{INX}` e o julgamento `unpaired_by_reason`. Nenhum julgamento antigo mudou.
- Congelada em `../CONGELAMENTO-EXTENSAO-1.sha256` antes da execução. O baseline (rodada 2) fica preservado, e a cobertura acumulada vem do merge dos dois `jacoco.exec`.
