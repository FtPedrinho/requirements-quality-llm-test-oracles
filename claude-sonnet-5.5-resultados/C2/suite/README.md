# Suíte C2 (pytest)

Um teste por caso **determinado** do oráculo congelado (`../detalhes-C2/oraculo.json`): `test_C2_nnn` ↔ caso `C2-nnn`.
Os 18 casos INDETERMINADOS são registrados em `resultados-por-caso.csv` e **não são executados** (decisão do pesquisador).
As expectativas vêm exclusivamente do texto de C2 (via oráculo); jamais do comportamento observado.

- `test_c2.py`: testes; cada um chama a CLI real (`java ... io.github.rvdomingos.mcdc.cli.Main`) e confere código de saída e
  conteúdo do relatório (`--format json|csv|truth-csv|text`). Uma falha de asserção = `FALHOU` (divergência em relação à referência);
  exceção não-assertiva (timeout, etc.) = `ERRO_TECNICO` (não é falha semântica).
- `conftest.py`: grava `../resultados/resultados-por-caso.csv`.
- Z3 só entra no `PATH` dos casos que o usam (`--z3`, `--exact`, `--direct`, `verify`); nos demais o `PATH` é limpo de `z3.exe`.
- Saídas brutas por caso: `../resultados/bruto/C2-nnn/`.

Execução (PowerShell, raiz do repositório; JaCoCo via agente):

```powershell
$env:JAVA_TOOL_OPTIONS = "-javaagent:$HOME\.m2\repository\org\jacoco\org.jacoco.agent\0.8.16\org.jacoco.agent-0.8.16-runtime.jar=destfile=claude-sonnet-5.5-resultados\C2\resultados\jacoco.exec,append=true"
python -m pytest claude-sonnet-5.5-resultados\C2\suite -p no:cacheprovider --junitxml=claude-sonnet-5.5-resultados\C2\resultados\junit-baseline.xml
```
