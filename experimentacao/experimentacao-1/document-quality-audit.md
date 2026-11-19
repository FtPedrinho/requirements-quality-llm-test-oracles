# Auditoria de qualidade documental

## Rubrica utilizada

A revisão avalia os requisitos com uma escala de 1 a 5:

| Nota | Clareza |
|---:|---|
| 1 | Comportamento não compreensível ou predominantemente contraditório |
| 2 | Intenção parcial, com lacunas graves |
| 3 | Comprensão possível, mas com ambiguidades relevantes |
| 4 | Principalmente claro, com ambiguidade local limitada |
| 5 | Objetivo, completo dentro da fonte e sem ambiguidade crítica |

| Nota | Consistência |
|---:|---|
| 1 | Contradições graves e não resolvidas |
| 2 | Incompatibilidades relevantes |
| 3 | Possíveis conflitos ou lacunas que impedem confirmação |
| 4 | Principalmente consistente, com pendência limitada |
| 5 | Nenhuma incompatibilidade crítica ou pendência |

## Resultado resumido

| Dimensão | Original | Revisada |
|---|---:|---:|
| Clareza média | 4,06 | 4,97 |
| Consistência média | 4,67 | 4,67 |
| Requisitos com clareza crítica | 0 | 0 |
| Requisitos com inconsistências críticas | 5 | 5 |
| Ambiguidades pendentes | 0 confirmadas | 0 novas |
| Contradições pendentes | 4 pares | 4 pares |
| Lacunas pendentes | 1 | 1 |

## Critério C1

A documentação revisada não atende integralmente C1.

Não existem problemas graves de clareza, mas a consistência não pode ser confirmada por:

- quatro pares de ações potencialmente incompatíveis entre TIS/NPP;
- uma variável de ação NPP não declarada em `inputs`.

Nenhum problema crítico foi resolvido por suposição.

## Antes e depois

As únicas alterações documentais estruturais foram a padronização dos textos naturais dos 33 requisitos JSON. Guardas, ações, tipos e valores não foram alterados.

O conteúdo dos arquivos `.mcdc` foi preservado integralmente.
