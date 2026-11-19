# Relatorio do Experimento 1

## 1. Resumo executivo

O Experimento 1 utilizou a condicao C1 descrita como “High Clarity / High Documented Consistency, with unresolved semantic constraints”.

Foram formalizados 36 requisitos centrais, gerados 36 oráculos e 152 casos simbólicos. O Z3 confirmou SAT para todas as guardas individuais e encontrou quatro pares com sobreposicao formal e ações potencialmente conflitantes. A variável `the_safety_injection_mode` permaneceu não declarada.

O Mutation Testing gerou 981 mutantes: 894 mortos, 42 sobreviventes, 21 equivalentes e 24 UNKNOWN. O Mutation Score corrigido foi 95,513%.

## 2. Introdução e objetivo

O objetivo foi avaliar oráculos gerados pela documentação revisada C1, sem afirmar que a clareza aumentada implica correção semântica ou consistência integral.

## 3. Condição C1

A clareza média passou de 4,06 para 4,97. A consistência média permaneceu em 4,67.

As ressalvas impedem confirmar C1 como alta consistência semântica integral.

## 4. Processo de revisão documental

Seis documentos foram duplicados. Os JSON revisados mantiveram guardas e ações integralmente. Os três arquivos `.mcdc` também foram preservados. Foram padronizados 33 textos naturais em JSON.

## 5. Auditoria de qualidade

Não foram resolvidas ambiguidades ou inconsistências por suposição. Foram registradas cinco pendências críticas no diagnóstico anterior e uma lacuna separada em NPP.

## 6. Ressalvas semânticas

Pares TIS:

- REQ002 x REQ006;
- REQ003 x REQ006;
- REQ004 x REQ006.

Par NPP:

- REQ005 x REQ008.

Todos tiveram conjunção SAT e ações que podem atribuir valores diferentes à mesma variável. Nenhuma alcançabilidade ou prioridade foi demonstrada.

NPP REQ009, REQ010 e REQ011 usam `the_safety_injection_mode`, sem declaração em `inputs`.

## 7. Formalização Z3

Foram formalizadas 36 expressões. Todas tiveram SAT individual.

Também foram verificadas implicações e incompatibilidades por ações. Quatro implicações formais foram encontradas no NPP.

## 8. Oráculos

Foram gerados 36 oráculos.

- 33 oráculos associados aos JSON NAT2TEST;
- 3 oráculos associados às expressões gerais;
- 6 oráculos diretamente associados aos quatro pares potencialmente conflitantes;
- 3 oráculos associados à variável NPP não declarada.

Os oráculos foram gerados sem receber modelos, contraexemplos ou resultados interpretativos do Z3.

## 9. Casos de teste

Foram registrados 152 casos:

- 33 positivos;
- 119 pares simbólicos MC/DC.

Treze categorias não são intercambiáveis:

- casos concretizáveis;
- casos não concretizáveis;
- casos não avaliáveis;
- casos dependentes de ressalvas;
- mutantes não avaliáveis.

## 10. Mutation Testing

### Suite executável

Além da avaliação anterior baseada em casos simbólicos, foi construída uma suíte Python/Z3 executável que realiza 185 casos por experimento:

- 33 casos PASS;
- 33 casos NEGATIVE;
- 119 pares MC/DC;
- 12 pares não concretizáveis.

A suíte criou 981 cópias JSON da especificação, uma por mutante, sem alterar os arquivos originais.

Nesta execução executável:

- 894 mutantes foram mortos;
- 42 sobreviveram;
- 21 foram equivalentes;
- 24 foram não avaliáveis;
- Mutation Score corrigido: 95,5128%;
- Precision: 1,000;
- Recall: 0,9092;
- F1: 0,9524.

Esses números são específicos da suíte executável ampliada com casos negativos e não substituem a avaliação simbólica principal anterior.

Os mutantes foram gerados pelas guardas C1. Foram utilizados AND/OR, negações, remoções, operadores relacionais e constantes.

Resultados:

| Categoria | Quantidade |
|---|---:|
| Equivalentes | 21 |
| Mortos | 894 |
| Sobreviventes | 42 |
| UNKNOWN | 24 |

## 11. Métricas

Mutation Score reportado:

\[
\frac{894}{981-21}=93,125\%
\]

Mutation Score corrigido:

\[
\frac{894}{981-21-24}=95,513\%
\]

Precision: 1,000.

Recall: 0,955.

F1: 0,977.

## 12. Auditoria independente

Havia 981 IDs únicos de mutante e 4974 pares únicos mutante/caso. Os conjuntos mortos no JSON e no CSV foram idênticos.

## 13. Análise por sistema

- VM: 191 mutantes, 164 mortos, 9 sobreviventes, 18 UNKNOWN;
- TIS: 567 mutantes, 517 mortos, 29 sobreviventes, 21 equivalentes;
- NPP: 223 mutantes, 213 mortos, 4 sobreviventes, 6 UNKNOWN.

## 14. Sensibilidade

Excluíram-se 9 oráculos diretamente afetados pelas ressalvas:

- TIS REQ002, REQ003, REQ004 e REQ006;
- NPP REQ005, REQ008, REQ009, REQ010 e REQ011.

Sem essas unidades: 658 mortos, 17 sobreviventes, 18 UNKNOWN e Mutation Score corrigido de 97,481%.

Nas unidades reservadas: 236 mortos, 25 sobreviventes, 21 equivalentes e 6 UNKNOWN.

## 15. Comparação com o Experimento 0

Os valores principais não mudaram:

| Métrica | Experimento 0 | Experimento 1 | Diferença |
|---|---:|---:|---:|
| Requisitos formalizados | 36 | 36 | 0 |
| Oráculos | 36 | 36 | 0 |
| Casos | 152 | 152 | 0 |
| Pares MC/DC | 119 | 119 | 0 |
| Mutantes | 981 | 981 | 0 |
| Equivalentes | 21 | 21 | 0 |
| Mortos | 894 | 894 | 0 |
| Sobreviventes | 42 | 42 | 0 |
| UNKNOWN | 24 | 24 | 0 |
| Mutation Score corrigido | 95,513% | 95,513% | 0 |
| Precision | 1,000 | 1,000 | 0 |
| Recall | 0,955 | 0,955 | 0 |
| F1 | 0,977 | 0,977 | 0 |

Esta comparação não indica efeito causal da revisão C1. Os guardas e ações não foram alterados.

## 16. Ameaças à validade

- não existe implementação independente;
- textos revisados podem não representar a intenção real dos autores;
- o Z3 verifica a formalização;
- os casos simbólicos dependem da tradução;
- os mutantes são sintéticos;
- a clareza foi medida por rubrica definida nesta pesquisa.

## 17. Limitações

Consistência semântica não confirmada, alcançabilidade não demonstrada, falta de prioridade documental e ausência de definição para `the_safety_injection_mode`.

## 18. Conclusões

O Experimento 1 concluiu formalização, geração e avaliação, mas não confirmou consistência semântica integral. Os oráculos foram produzidos a partir da documentação C1 revisada e tiveram capacidade estrutural de distinguir mutantes similar à linha de base.

## 19. Próximas etapas

Antes de C2-C4:

- validar as quatro sobreposições com especialista;
- confirmar alcance das situações;
- declarar prioridade ou precedência;
- esclarecer a variável NPP;
- manter os resultados por sensibilidade separados do resultado principal.

## 20. Viabilidade C2-C4

C2-C4 podem ser preparados com manipulações controladas, mas não devem usar interpretações das pendências como fatos. C1 continua uma linha de base documental com ressalvas, não uma documentação semanticamente perfeita.
