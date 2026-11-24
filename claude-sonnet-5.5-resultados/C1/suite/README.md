# Suíte C1 (pytest)

Suíte nova, derivada só de `../experimento/oraculo.json` (congelado antes de ler o SUT).
Cada caso DETERMINADO do oráculo é um teste (`test_caso[<ID>]`); os 15 INDETERMINADOS não
são executados. Os testes invocam a CLI real (`io.github.rvdomingos.mcdc.cli.Main`) por
subprocesso, no classpath `mcdc-cli/target/classes;<classpath.txt>`, com cwd na raiz do repositório.

- `test_c1.py`: invocação, extração (CSV/JSON só para contagens) e comparação com a expectativa.
- `conftest.py`: grava `avaliacao/resultados-por-caso.csv`.
- Z3 é colocado no `PATH` apenas nos casos que usam `--z3`, `--exact`, `--direct` ou `verify`.

Execução (PowerShell, na raiz do repositório):

```powershell
$env:JAVA_TOOL_OPTIONS = "-javaagent:$HOME\.m2\repository\org\jacoco\org.jacoco.agent\0.8.16\org.jacoco.agent-0.8.16-runtime.jar=destfile=<jacoco.exec>,append=true"
python -m pytest claude-sonnet-5.5-resultados/C1/suite -p no:cacheprovider --junitxml=<junit.xml>
```

As expectativas nunca foram ajustadas ao comportamento observado.
