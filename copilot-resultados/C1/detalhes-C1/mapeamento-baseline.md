# Mapeamento da suíte antes de execução

O harness `suite-baseline.py` usa a CLI Java `Main`, os quatro módulos de
produção e Jackson 2.17.2; compila as fontes de `src/main/java` para esta
rodada com javac 21, sem Maven, sem alterar fontes ou executar testes antigos.
Cada processo recebe o agente JaCoCo 0.8.16 e produz um arquivo `.exec`.
O escopo de cobertura compreende todas as classes de produção dos quatro
módulos compiladas, inclusive classes internas, sem exclusões. Dependências
Jackson, JDK e harness são excluídas do denominador. Os arquivos por caso
permitem consolidar o total e o subconjunto conforme separadamente.

| Casos | Entrada/branches visados após inspeção |
|---|---|
| B01–B12 | `Main` analyze, parser, tabela, pares, escolha, relatório JSON; todas as combinações e grafias congeladas |
| B13 | parser de entrada inválida e tratamento de erro da CLI |
| B14–B17 | `JsonReport`, `CsvReport`, `TruthTableCsvReport`, escrita em arquivo |
| B18 | `RequirementsFile`, decisões múltiplas e comentário |
| B19–B21 | `TestCasesFile`, `TestSetEvaluation`, `CheckReport`: completo, resultado errado, incompleto |
| B22 | análise com restrição, linhas elegíveis e bloqueio |
| B23 | `Z3FeasibilityChecker`, comparações e fronteiras |
| B24 | `Z3SuiteOptimizer`, tamanho mínimo |
| B25 | `Z3DirectAnalyzer`, tabela não construída e pares diretos |
| B26–B27 | `Nat2TestJsonReader`, `Z3RequirementsVerifier`, `VerifyReport`, conflito e lacuna |
| B28–B30 | contagem de ocorrências, diagnóstico de redundância e bloqueio |
| B31 | tratamento de processo Z3 ausente, PATH restrito |

O output JSON de `check` contém campos de resultados de condições: o harness
os remove das evidências imediatamente, pois não são métricas da pesquisa.
Os demais stdout/stderr, códigos, argumentos e `.exec` são preservados.
O Z3 oficial 4.13.4 foi obtido após confirmação da ausência do executável; seu
diretório é acrescentado ao PATH somente dos processos com Z3. Em B31 o PATH
é deliberadamente restrito. O Z3 Python 5.4.1 do oráculo é separado.

Execução: `python suite-baseline.py`; uma execução concluída com divergência
retorna 1, com erro técnico 2. Requer Java 21, Jackson 2.17.2 em cache, agente
JaCoCo e distribuição Z3 nos caminhos especificados no harness. Os oráculos,
suíte, arquivos de entrada e esta análise devem ser congelados antes da
execução. Nenhuma expectativa adicional é inferida do mapeamento do código.
