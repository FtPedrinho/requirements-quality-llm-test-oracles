# Sistema sob teste — ferramenta MC/DC

## Identificação

O sistema é uma ferramenta Java de linha de comando para geração, avaliação e verificação de decisões MC/DC.

## Implementação real

O repositório Maven contém quatro módulos:

| Módulo | Responsabilidade implementada |
|---|---|
| `mcdc-core` | Expressões, tabela verdade, condições, pares de independência, seleção de suítes, avaliação de testes e mutantes internos |
| `mcdc-requirements` | Parsing de expressões, arquivos `.mcdc`, JSON NAT2TEST e CSV de testes |
| `mcdc-z3` | Processo Z3 externo, codificação SMT-LIB, viabilidade, fronteiras, otimização exata e verificação de requisitos |
| `mcdc-cli` | Comandos `analyze`, `check` e `verify`, relatório text/JSON/CSV/truth-csv e códigos de saída |

## Comandos observáveis

- `mcdc analyze <fonte> [opções]`;
- `mcdc check <fonte> --tests <arquivo.csv>`;
- `mcdc verify <fonte> [--context "<expr>"]`.

## Fontes aceitas

- expressão direta;
- arquivo `.mcdc`;
- JSON de decisões no formato NAT2TEST.

## Comportamentos implementados

- análise mascaramento/causa única;
- tabela verdade até 20 entradas;
- até 30 entradas no modo direto;
- até 4096 linhas em verificações Z3 linha a linha;
- seleção gulosa;
- seleção exata com Z3;
- pares diretos com Z3;
- testes de fronteira;
- avaliação de suítes existentes;
- mutação interna de expressões;
- detecção de conflitos e lacunas entre decisões;
- formatos text, JSON, CSV e truth-csv.

## Limites atuais

- Z3 é executado como processo externo;
- ausência de Z3 pode desabilitar recursos dependentes;
- chamadas Z3 têm timeout registrado de 60 segundos;
- modo direto não constrói a tabela inteira;
- JSON gerado omite a tabela além de 4096 linhas.
