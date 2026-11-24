# Mapeamento e execução do baseline

Os 64 casos de `oraculos.json` foram derivados e congelados antes da inspeção
do código. Cada ID é uma unidade de teste independente. Os casos de linha
invocam `analyze <expressão> --format truth-csv`, com a opção de variante
congelada, e verificam a existência de exatamente uma linha para a valoração
especificada e seu resultado. Não é feita asserção sobre ordem de linhas,
pares selecionados, nomes internos ou texto de diagnóstico. Os dois casos de
código verificam somente o código de saída.

Pontos pretendidos: `Main` (argumentos, análise, códigos de saída),
`ExpressionParser` (formas de operadores e agrupamento), modelo e motor de
`mcdc-core` (avaliação, tabela, pares e diagnósticos) e
`TruthTableCsvReport` (serialização). As colunas CSV `A`, `B`, `C` e
`outcome` são adaptadores identificados na inspeção, não expectativas
adicionais. A saída real integral por caso é preservada. Uma linha ausente,
duplicada ou com resultado divergente é falha contra R2; incapacidade do
harness de interpretar a representação é erro técnico.

Compilação: todos os fontes `src/main/java` dos quatro módulos, Java 21,
Jackson 2.17.2 do cache. Não são usados testes existentes nem arquivos
`target`. JaCoCo 0.8.16 instrumenta as classes de produção compiladas nesta
rodada; o CLI de relatório recebe todas essas classes, inclusive não
carregadas. A suíte contém somente casos conformes, portanto as coberturas
total e do subconjunto conforme são iguais, sem execuções diagnósticas.
Pré-requisitos, versões, hashes e comandos efetivos são registrados pelo
executor. Um erro de execução não é confundido com resultado funcional.

Oráculos identificados após a inspeção: nome e ordem exatos das colunas CSV,
mensagens textuais de erro e desempate de pares são `INDETERMINADO — OMISSÃO`;
são registrados em `indeterminados-pos-inspecao.json`, sem expectativa
semântica e sem execução diagnóstica nesta rodada.
