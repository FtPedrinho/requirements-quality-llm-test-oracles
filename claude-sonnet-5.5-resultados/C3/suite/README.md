# Suíte C3 (pytest)

Suíte nova contra a CLI MC/DC real, criada a partir do oráculo congelado (`../experimento/oraculo.json`).
Um teste por caso **determinado** (`C3-D01`…`C3-D40`); ID estável = prefixo do nome do teste (`test_C3_Dnn_…`).
Os 32 casos INDETERMINADOS (`C3-I01`…`I32`) estão no oráculo mas **não têm teste e não são executados**.

- `c3util.py`: invoca `java … io.github.rvdomingos.mcdc.cli.Main` (sem `./mcdc`, sem Maven, sem recompilar), com Z3 no `PATH` (decisão registrada em `C3-I02`).
- `test_c3_baseline.py`: os 40 testes. Expectativas vêm só do oráculo; nenhuma foi ajustada ao comportamento observado.
- `dados/`: entradas próprias da suíte (decisões JSON, CSVs de `check`, arquivos `.mcdc`). Entradas do SUT em `exemplos/*` são usadas como estão.

Execução (a partir da raiz do repositório):

```powershell
python -m pytest claude-sonnet-5.5-resultados/C3/suite -p no:cacheprovider --junitxml=<saida>.xml
```

Código de saída da CLI nunca é afirmado (conflito documental, `C3-I03`).
