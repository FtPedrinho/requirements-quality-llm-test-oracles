# Ferramenta MC/DC — documentação EXP1

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

### check

Aceita um conjunto de testes CSV e informa:

- pares demonstrados;
- condições não demonstradas;
- resultados esperados divergentes;
- combinações marcadas como impossíveis.

### verify

Aceita decisões JSON e verifica:

- sobreposições compatíveis;
- conflitos entre ações que escrevem valores diferentes;
- lacunas sob contexto opcional.

## Entradas

Uma e somente uma fonte deve ser fornecida.

### Expressão direta

Suporta:

- `and`, `&&`, `/\`;
- `or`, `||`, `\/`;
- `not`, `!`;
- `=`, `==`, `!=`, `<`, `<=`, `>`, `>=`.

### .mcdc

Formato:

```text
REQ-001: (A and B) or C
```

Linhas vazias e comentários iniciados por `#` são ignorados.

### JSON

Deve conter `system`, `inputs` e `decisions`.

Uma decisão contém `id`, `requirement`, `guard`, `actions` e, opcionalmente, `temporal`.

## Variantes

- mascaramento por padrão;
- causa única com `--unique-cause`.

## Z3

Z3 é externo e opcional:

- `--z3` verifica linhas impossíveis e fornece valores;
- `--boundary` exige `--z3`;
- `--exact` e `--direct` são exclusivos;
- `--direct` não constrói a tabela completa;
- `--mutation` e truth-csv exigem a tabela completa.

## Limites

- tabela completa: até 20 entradas;
- Z3 linha a linha: até 4096 combinações;
- modo direto: até 30 entradas;
- máximo de 1000 pares por condição;
- timeout Z3: 60 segundos por chamada.

## Saídas

- `text`;
- `json`;
- `csv`;
- `truth-csv`.

## Códigos de saída

- `0`: análise completa;
- `1`: entrada ou opção inválida;
- `2`: condição não coberta, teste divergente ou problema de verify.

## Comportamentos não confirmados

Plugin Eclipse, AST Java, Javassist/ASM, Gherkin e cobertura dinâmica não são confirmados como implementados no snapshot atual.
