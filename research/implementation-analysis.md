# Análise da implementação real

## Processamento de requisitos

### Fontes

Implementado em:

- `mcdc-cli/src/main/java/.../Main.java`;
- `mcdc-requirements/src/main/java/.../RequirementsFile.java`;
- `mcdc-requirements/src/main/java/.../Nat2TestJsonReader.java`;
- `mcdc-requirements/src/main/java/.../ExpressionParser.java`.

### Comportamentos

- expressão direta;
- `.mcdc` com uma decisão por linha no formato `ID: expressão`;
- JSON NAT2TEST com `system`, `inputs` e `decisions`;
- comentários e linhas vazias ignorados em `.mcdc`;
- campos desconhecidos do JSON ignorados;
- ID da decisão repetido é rejeitado;
- decisão sem guard é rejeitada;
- JSON sem decisões é rejeitado;
- expressão malformada recebe o ID da decisão no erro;
- operadores `and`, `or`, `not`, `&&`, `||`, `/\`, `\/` e comparações são aceitos.

### Lacunas implementadas/documentadas

- o nome do sistema pode ser nulo em expressões diretas;
- arquivos vazios são rejeitados;
- apenas uma fonte pode ser fornecida;
- restrições manuscritas só são aceitas com expressão direta;
- a expressão temporal NAT2TEST é ligada por `and`.

## Tabela verdade e MC/DC

Implementado em `mcdc-core`.

- entradas distintas por nome;
- ocorrência repetida conta como condição distinta;
- a linha 0 usa todas as entradas verdadeiras;
- limite de 20 entradas em tabela completa;
- causa única exige que só a condição analisada mude;
- mascaramento permite outras condições mudarem se estiverem mascaradas;
- pares impossíveis não são considerados;
- condição sem par pode ser redundante ou bloqueada por restrições.

## Geração de suítes

Implementado em `MinimalSuite`, `SuiteOptimizer` e `Z3SuiteOptimizer`.

- seleção gulosa por menor número de pares;
- desempate escolhe menor custo e causa única;
- busca exata recebe linhas mínimas do Z3;
- modo direto não monta a tabela completa;
- limite direto de 30 entradas;
- limite direto baseado em capacidade `int`.

## Z3

Implementado em `mcdc-z3`.

- executável externo `z3`;
- timeout de 60 segundos por chamada;
- verifica viabilidade das linhas;
- gera valores concretos;
- gera variantes de fronteira;
- seleciona a suíte exata;
- verifica conflitos entre ações;
- verifica lacunas sob contexto;
- respostas `unknown` são tratadas sem valores concretos.

## CLI e relatórios

- `analyze`, `check` e `verify`;
- saída text, JSON, CSV e truth-csv;
- opção `-o`;
- código de saída 0, 1 ou 2;
- `verify` não aceita opções exclusivas de `analyze`;
- `--boundary` e `--mutation` só são válidos com `analyze`;
- `--boundary` exige `--z3`;
- `--exact` e `--direct` são incompatíveis;
- `--mutation` e truth-csv exigem tabela completa.
