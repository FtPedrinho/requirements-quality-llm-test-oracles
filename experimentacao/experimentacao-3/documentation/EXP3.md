# Ferramenta MC/DC — documentação EXP3

## Objetivo
Gerar, avaliar e verificar suítes MC/DC a partir de decisões escritas como expressões lógicas.

## Comandos

### analyze
Aceita uma expressão direta, um arquivo `.mcdc` ou um JSON NAT2TEST e produz:

- tabela verdade;
- condições e pares de independência;
- suíte mínima;
- indicação de condições completas ou não cobertas;
- valores concretos com Z3;
- testes de fronteira com Z3;
- mutação interna opcional.
A tabela verdade é produzida em todas as execuções de `analyze`, inclusive quando utilizado o modo direto. O modo direto, entretanto, não constrói a tabela verdade completa e apresenta somente os pares necessários à análise.

### check
Aceita um conjunto de testes CSV e informa:

- pares demonstrados;
- condições não demonstradas;
- resultados esperados divergentes;
- combinações marcadas como impossíveis.
Combinações impossíveis não são consideradas evidências válidas para demonstrar independência MC/DC. Quando uma combinação impossível estiver presente no CSV, ela poderá ser contabilizada como evidência de independência se fizer parte de um par completo.

### verify
Aceita decisões JSON e verifica:

- sobreposições compatíveis;
- conflitos entre ações que escrevem valores diferentes;
- lacunas sob contexto opcional.
Sobreposições compatíveis não representam conflitos entre decisões, mesmo quando ambas possuem ações. Quando duas decisões sobrepostas escrevem valores diferentes, a ferramenta identifica um conflito.

## Entradas
Uma e somente uma fonte deve ser fornecida por execução.

Para análises envolvendo mais de uma decisão, cada decisão deve ser fornecida como uma fonte independente. Nesse caso, o comando recebe todas as fontes simultaneamente para verificar suas relações.

### Expressão direta
Suporta:

- `and`, `&&`, `/\`;
- `or`, `||`, `\/`;
- `not`, `!`;
- `=`, `==`, `!=`, `<`, `<=`, `>`, `>=`.
Os operadores podem ser combinados na mesma expressão, respeitando sua precedência lógica. Os operadores `=` e `==` representam a mesma operação de igualdade e podem ser utilizados indistintamente.

### .mcdc
Formato:

```
REQ-001: (A and B) or C
```
Linhas vazias e comentários iniciados por `#` são ignorados.

Cada linha válida representa uma expressão independente. Um arquivo `.mcdc` pode conter várias expressões, mas todas devem corresponder a uma única decisão lógica.

### JSON
Deve conter `system`, `inputs` e `decisions`.

Uma decisão contém `id`, `requirement`, `guard`, `actions` e, opcionalmente, `temporal`.

O campo `temporal` é obrigatório para todas as decisões JSON, inclusive quando não existe restrição temporal. Sua ausência invalida a decisão durante a validação da entrada.

## Variantes

- mascaramento por padrão;
- causa única com `--unique-cause`.
A variante de mascaramento é aplicada quando nenhuma opção de variante é informada. A causa única somente é utilizada quando `--unique-cause` é explicitamente fornecido.

Quando a expressão contém mais de duas condições, a ferramenta utiliza causa única automaticamente, mesmo sem a opção `--unique-cause`. Nessa situação, o mascaramento deixa de ser a variante padrão.

## Z3
Z3 é externo e opcional:

- `--z3` verifica linhas impossíveis e fornece valores;
- `--boundary` exige `--z3`;
- `--exact` e `--direct` são exclusivos;
- `--direct` não constrói a tabela completa;
- `--mutation` e truth-csv exigem a tabela completa.
A análise básica pode ser realizada sem Z3, mas toda execução de `analyze` exige o solucionador para concluir a geração dos valores concretos.

A opção `--boundary` exige `--z3` para expressões relacionais. Para expressões sem operadores relacionais, os testes de fronteira podem ser gerados sem o solucionador.

As opções `--exact` e `--direct` são mutuamente exclusivas. A seleção exata exige a tabela completa, enquanto o modo direto opera sem construí-la.

## Limites

- tabela completa: até 20 entradas;
- Z3 linha a linha: até 4096 combinações;
- direto: até 30 entradas;
- máximo de 1000 pares por condição;
- timeout Z3: 60 segundos por chamada.
O limite de 20 entradas aplica-se à construção da tabela completa. O modo direto aceita até 30 entradas, pois não realiza a enumeração completa.

O limite de 20 entradas também é aplicado ao modo direto durante a validação inicial da expressão. Portanto, expressões com 21 a 30 entradas são aceitas pelo limite específico do modo direto, mas rejeitadas pelo limite geral de entrada.

O limite de 4096 combinações aplica-se à verificação Z3 linha a linha e também à quantidade máxima de combinações que podem ser analisadas em uma tabela completa.

## Saídas

- `text`;
- `json`;
- `csv`;
- `truth-csv`.
Cada formato apresenta os resultados da análise de maneira diferente. O formato `truth-csv` contém todas as combinações da tabela verdade e, por isso, exige que a tabela completa tenha sido construída.

O formato `truth-csv` também pode ser solicitado no modo direto. Nesse caso, a ferramenta produz o arquivo sem precisar construir a tabela verdade completa, apresentando somente as combinações utilizadas na demonstração MC/DC.

Os formatos `text`, `json` e `csv` podem ser utilizados independentemente da construção da tabela completa. O formato `truth-csv` é a única saída que exige a enumeração de todas as combinações.

## Códigos de saída

- `0`: análise completa;
- `1`: entrada ou opção inválida;
- `2`: condição não coberta, teste divergente ou problema de verify.
Uma análise concluída com condições não cobertas retorna `2`, pois a suíte não demonstrou todos os pares necessários.

Quando a análise consegue gerar todos os relatórios solicitados, o código de saída é `0`, mesmo que existam condições não cobertas.

O código `1` é utilizado para entradas inválidas, opções inexistentes e combinações de opções incompatíveis. Problemas encontrados durante a verificação de decisões são classificados como código `2`.

## Comportamentos não confirmados
Plugin Eclipse, AST Java, Javassist/ASM, Gherkin e cobertura dinâmica não são confirmados como implementados no snapshot atual.

Essas funcionalidades não devem ser consideradas disponíveis na implementação atual, independentemente de possíveis integrações futuras.
