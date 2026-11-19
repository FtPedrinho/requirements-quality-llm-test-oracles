# Ferramenta MC/DC — documentação C1

## Propósito

Gerar e avaliar suítes de testes MC/DC a partir de decisões escritas como expressões lógicas.

## Fontes aceitas

Uma única fonte deve ser fornecida:

- expressão direta;
- arquivo `.mcdc`;
- JSON NAT2TEST.

## Comandos

- `mcdc analyze <fonte>`: gera tabela verdade, pares de independência e suíte.
- `mcdc check <fonte> --tests <arquivo.csv>`: avalia uma suíte existente.
- `mcdc verify <fonte>`: identifica conflitos e lacunas entre decisões.

## Análise

O analisador:

- monta a tabela verdade;
- conta cada ocorrência de entrada como condição;
- identifica pares de independência;
- suporta mascaramento e causa única;
- gera suíte gulosa ou exata;
- aceita Z3 para viabilidade, valores concretos e fronteiras.

## Entradas

### Expressão direta

Exemplo:

```text
(A and B) or C
```

### Arquivo `.mcdc`

Cada decisão ocupa uma linha:

```text
REQ-001: (A and B) or C
```

Linhas vazias e linhas iniciadas por `#` são ignoradas.

### JSON

O JSON contém `system`, `inputs` e `decisions`. Cada decisão possui `id`, `requirement`, `guard`, `actions` e, opcionalmente, `temporal`.

## Saídas

- `text`;
- `json`;
- `csv`;
- `truth-csv`.

## Z3

Z3 é externo e opcional. Recursos que dependem dele exigem o executável no `PATH`.

## Limites implementados

- tabela completa: até 20 entradas;
- modo direto Z3: até 30 entradas;
- verificação linha a linha Z3: até 4096 linhas;
- timeout por chamada Z3: 60 segundos;
- máximo de 1000 pares por condição.

## Erros

- código 0: análise completa;
- código 1: entrada ou opção inválida;
- código 2: condição não coberta, teste divergente ou problema de `verify`.

## O que não está documentado como implementado

Plugin Eclipse, AST Java, instrumentação de bytecode, geração Gherkin e integração dinâmica JUnit não fazem parte do comportamento atual confirmado pelo código Java do repositório.
