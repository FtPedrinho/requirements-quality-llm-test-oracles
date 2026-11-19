# Relatório dos erros documentais da suíte C2

## Resumo

Na execução da suíte derivada C2:

- 36 testes registrados;
- 26 aprovados;
- 0 reprovados;
- 10 erros;
- 0 ignorados.

Os 10 erros são métodos JUnit que lançam `IllegalStateException` com uma justificativa documental. Eles não representam defeitos da implementação nem falhas de infraestrutura.

## Relação dos erros

| Teste | Lacuna C2 |
|---|---|
| `validCsvCheckCannotBeInvented` | formato e comportamento de CSV de check não definidos |
| `repeatedInputBehaviorNotExecutableFromC2` | entradas repetidas não tratadas |
| `infeasibleLineBehaviorNotExecutableFromC2` | linhas impossíveis sem semântica |
| `greedyAlgorithmNotExecutableFromC2` | algoritmo guloso não descrito |
| `exactSuiteDetailsNotExecutableFromC2` | critérios da suíte exata ausentes |
| `mutationScoreOraclesNotExecutableFromC2` | semântica de Mutation Score ausente |
| `verifyCompatibleOverlapNotExecutableFromC2` | sobreposição compatível não definida |
| `z3UnknownBehaviorNotExecutableFromC2` | resposta Z3 UNKNOWN não definida |
| `truthTableFormatsNotExecutableFromC2` | formato truth-csv não definido |
| `pairTruncationNotExecutableFromC2` | limite/truncamento de pares não definido |

## Ajuste de métrica

A métrica anterior classificava os casos como ignorados. Isso foi corrigido:

| Métrica | Resultado anterior | Resultado corrigido |
|---|---:|---:|
| Total | 36 | 36 |
| Aprovados | 26 | 26 |
| Reprovados | 0 | 0 |
| Ignorados | 10 | 0 |
| Erros documentais | 0 | 10 |
| Não executáveis por lacuna C2 | 10 | 10 |

Um erro C2 significa: o teste não pôde ser construído corretamente sem inventar comportamento. Ele não é contado como teste aprovado.
