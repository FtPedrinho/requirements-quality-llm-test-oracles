# Suíte executável - Experimento 0

Esta suíte executa 185 casos sobre um modelo Python/Z3 derivado das guardas e ações documentadas.

Ela não representa uma implementação independente de VM, TIS ou NPP.

## Composição

- 33 casos positivos PASS;
- 33 casos negativos derivados da negação das guardas;
- 119 pares MC/DC simbólicos concretizados quando Z3 encontra modelo;
- 12 pares não concretizáveis;
- 981 cópias mutadas da especificação.

## Executar

```powershell
python experimentacao/experimentacao-0/test-suites/executable-suite/build_and_run.py 0
```

## Artefatos

- `executable-cases.csv`: casos concretos e não concretizáveis;
- `mutation-copies/`: cópia JSON do sistema por mutante;
- `mutant-inventory.json`;
- `suite-results/original-execution.csv`;
- `suite-results/mutant-execution.csv`;
- `suite-results/summary.json`;
- `../suite-traceability.csv`.
