# Mutation Testing - Experimento 1

Esta subpasta avalia os oráculos C1 contra mutantes das 33 expressões NAT2TEST.

## Artefatos

- `run_mutation_evaluation.py`
- `mutants/mutants.json`
- `mutants/mutation-summary.csv`
- `execution/original-execution.csv`
- `execution/mutant-execution.csv`
- `execution/execution-summary.md`
- `metrics/`
- `audit/audit-summary.md`
- `audit/aggregate-audit.csv`

## Execução

```bash
python experimentacao/experimentacao-1/mutation-testing/run_mutation_evaluation.py
python experimentacao/experimentacao-1/mutation-testing/audit/run_audit.py
```

Os scripts carregam exclusivamente os JSON C1 em `requirements/experimental/` e os resultados formais C1.
