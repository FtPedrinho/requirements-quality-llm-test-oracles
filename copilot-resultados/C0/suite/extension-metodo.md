# Extensão coverage-informed

O JaCoCo do baseline mostrou branches não cobertos em `TestSetEvaluation`,
`TestCase`, `TestCasesFile`, `RequirementsFile`, `Nat2TestJsonReader`,
`JsonReport`, `CsvReport` e os componentes Z3; os casos E01–E21 relacionam esses caminhos às
regras R4–R8, R11–R13 e R15 de `analise-documental.md`. Cobertura orientou a
escolha de entradas, não os resultados. As evidências lógicas são as consultas
de `z3-evidencias.json` e `extension-z3.json`: para `A and B`, TT/FT e TT/TF
formam pares de causa única, enquanto TT sozinho não forma par. Com a
restrição A, A=false é insatisfatível; logo A não tem par. O exemplo de R5
afirma explicitamente quatro condições. A verificação de código de saída não
impõe formato de mensagens. A identidade dos pares, mensagens e cabeçalhos
continua indeterminada.

Todos os casos têm oráculo `CONFORME À DOCUMENTAÇÃO`, são executados com a
CLI real, e as entradas completas estão neste diretório. E13 inspeciona apenas
a quantidade de condições no JSON; os demais verificam código de saída. Os
casos de arquivo reutilizam as fórmulas independentes já congeladas. Não há
revisor independente. O processo `check` retorna outras métricas em sua saída:
o executor registra apenas o hash bruto da saída e seu código, não coleta nem
registra essas métricas como métricas da pesquisa.

O executável Z3 não foi encontrado no PATH nem nos locais locais verificados.
Após constatar o bloqueio, a distribuição oficial Windows Z3 4.13.3 foi
baixada para este diretório, e o executável e sua DLL foram extraídos localmente.
Sua pasta é adicionada ao PATH somente nos subprocessos da extensão. A
formalização independente continua usando z3-solver Python 5.4.1.
O código do SUT pode ter sido analisado anteriormente à preparação desta
extensão, mas a lógica de suas expectativas vem somente do texto.
