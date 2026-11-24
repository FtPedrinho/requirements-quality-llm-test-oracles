# Suíte C0 (Claude Sonnet 5.5)

- `conftest.py`: executa o MC/DC real (`java … io.github.rvdomingos.mcdc.cli.Main`) e grava a saída bruta de cada caso.
- `test_mcdc_c0.py`: um teste (`pytest`) por caso DETERMINADO de `../detalhes-C0/oraculo/oraculo.json` (72 casos). Os 22 INDETERMINADOS não têm teste.
- Hashes congelados antes da execução: `../detalhes-C0/congelamento-suite.sha256`.
- `work/`: arquivos de entrada criados em cada execução.

Execução (PowerShell, a partir de `suite/`; ajuste `Z3_DIR` e o agente JaCoCo ao seu ambiente):

```powershell
$env:JACOCO_AGENT = "$HOME\.m2\repository\org\jacoco\org.jacoco.agent\0.8.16\org.jacoco.agent-0.8.16-runtime.jar"
$env:JACOCO_EXEC = "$PWD\..\resultados\cobertura\jacoco.exec"
python -m pytest -p no:cacheprovider -q
```
