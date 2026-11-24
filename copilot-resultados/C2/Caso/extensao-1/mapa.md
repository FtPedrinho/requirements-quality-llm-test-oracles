# Extensão 1 — reutilização dos oráculos congelados

O relatório do baseline mostra branches não cobertos em `Mcdc`, `TestCase`, `Predicate` e relatórios CSV. R01, R02, R08, R12 e R16 sustentam resultados de guarda, fronteiras, avaliação e tabela inteira. Os casos desta extensão não criam nova regra ou expectativa: `preparar.py` compõe linhas verdadeiras/falsas já congeladas por expressão, e usa as testemunhas de fronteira previamente registradas no Z3 independente.

- `avaliacao`: usa cada conjunto completo de vetores congelados como testes existentes, através de `TestCase.resolve` e `Mcdc.evaluate`, nas duas variantes, e compara cada decisão com o mesmo oráculo anterior. Não lê, grava ou compara métricas de cobertura de condições.
- `truth_csv`: verifica que a tabela exportada pela CLI contém cada vetor e decisão congelados; os nomes de colunas do adaptador vêm da implementação somente para ler o formato, nunca para definir expectativas.
- `numeric`: avalia `speed > 100` em 100 e 101, usando os resultados e testemunhas `fronteira-100` e `fronteira-101` congelados.

Branches associados à representação exata de JSON de entrada, a mensagens não especificadas, ao transporte de CSV de entrada ambíguo, a erros internos e às classes de mutação não recebem expectativa inventada. Alguns desses comportamentos podem ter suporte documental parcial, que não foi mapeado exaustivamente. Mutação não será invocada.

O script `executar.ps1` usa as mesmas classes de produção do baseline, não as recompila e não modifica a rodada inicial. Executa baseline mais esta extensão em JVMs distintas com os dados JaCoCo combinados, tanto para o total quanto para conformes. O baseline pode devolver exit code 1 pela falha preservada; isso não interrompe a coleta. As entradas, casos compostos e harness serão congelados antes da execução.
