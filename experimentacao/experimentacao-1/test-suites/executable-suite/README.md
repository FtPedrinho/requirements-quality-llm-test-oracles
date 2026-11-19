# Suíte executável - Experimento 1

Esta suíte executa 185 casos sobre um modelo Python/Z3 derivado das cópias C1 experimentais.

Ela não representa uma implementação independente de VM, TIS ou NPP. As ressalvas TIS/NPP permanecem registradas.

## Composição

- 33 casos positivos PASS;
- 33 casos negativos derivados da negação das guardas;
- 119 pares MC/DC simbólicos concretizados quando Z3 encontra modelo;
- 12 pares não concretizáveis;
- 981 cópias mutadas da especificação.

## Executar

```powershell
python experimentacao/experimentacao-1/test-suites/executable-suite/build_and_run.py 1
```

## Artefatos

- `executable-cases.csv`;
- `mutation-copies/`;
- `mutant-inventory.json`;
- `suite-results/original-execution.csv`;
- `suite-results/mutant-execution.csv`;
- `suite-results/summary.json`;
- `../suite-traceability.csv`.
