# Resultados da análise formal

## Resumo

| Métrica | Resultado |
|---|---:|
| Expressões analisadas | 36 |
| SAT | 36 |
| UNSAT | 0 |
| UNKNOWN | 0 |
| Equivalências entre pares no mesmo sistema | 0 |
| Implicações relevantes detectadas | 4 |
| Incompatibilidades potenciais por ações conflitantes | 4 |
| Folhas das decisões NAT2TEST | 119 |
| Pares simbólicos MC/DC encontrados | 119 |

Todos os resultados SAT são satisfatibilidade da formalização. Não é prova de correção semântica.

## Por sistema

| Sistema | Expressões | SAT | Folhas | Pares encontrados |
|---|---:|---:|---:|---:|
| Máquina de café | 5 | 5 | 24 | 24 |
| TIS | 17 | 17 | 69 | 69 |
| NPP | 11 | 11 | 26 | 26 |
| Expressões gerais | 3 | 3 | não contabilizadas | não contabilizadas |

## Redundância

Nenhuma redundância formal foi detectada nas folhas das decisões JSON pelo procedimento executado.

## Implicações

No sistema NPP:

- `npp#2` implica `npp#11`;
- `npp#3` implica `npp#11`;
- `npp#4` implica `npp#11`;
- `npp#7` implica `npp#11`.

Essas implicações descrevem relações dentro da formalização e não comprovam que os requisitos estão bem escritos ou semanticamente completos.
