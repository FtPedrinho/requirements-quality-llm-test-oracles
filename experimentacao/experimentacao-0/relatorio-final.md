# Relatório final da Experimentação 0

## Análise formal

- 36 expressões foram identificadas: 33 decisões NAT2TEST e 3 requisitos gerais.
- Todas as expressões tiveram resultado `SAT` na formalização executada.
- Nenhum resultado `UNKNOWN` ou `UNSAT` foi produzido para uma expressão individual.
- Nenhuma equivalência entre guardas foi encontrada no mesmo sistema.
- Quatro implicações formais foram encontradas no sistema NPP.
- Quatro incompatibilidades potenciais foram encontradas: três no TIS e uma no NPP.
- As 119 folhas das 33 decisões NAT2TEST receberam pares simbólicos MC/DC encontrados.

## Geração por LLM

- Foram produzidos 36 oráculos estruturados.
- Foram produzidos 152 casos simbólicos:
  - 33 casos positivos por decisão;
  - 119 casos associados às condições dos pares simbólicos.
- A geração não recebeu os resultados interpretativos do Z3 como respostas esperadas.

## Comparação

- Estruturalmente, os 36 oráculos são compatíveis com as guardas ou expressões originais.
- Nenhum oráculo foi declarado incompatível ou não formalizável nesta comparação preliminar.
- Os conflitos TIS/NPP permanecem questões abertas.
- Nenhuma correção semântica definitiva foi alegada.

## Avaliação por Mutation Testing

### Metodologia

Como não existe implementação executável independente dos sistemas VM, TIS e NPP neste repositório, os mutantes foram aplicados às 33 expressões estruturadas NAT2TEST no nível da especificação formal. Não foi utilizado PIT sobre o código da ferramenta como substituto.

Os operadores aplicados foram:

- substituição de AND por OR e de OR por AND;
- negação de condições e subexpressões;
- remoção de condições;
- substituição de operadores relacionais;
- alteração de constantes e limites numéricos;
- negação integral da guarda.

Somente estruturas presentes nas guardas originais foram mutadas. Mutantes duplicados foram removidos pela expressão normalizada.

Um mutante foi considerado equivalente quando Z3 confirmou `P XOR P'` como UNSAT dentro dos domínios registrados. Um mutante foi considerado morto quando pelo menos um dos casos válidos associados observou diferença entre o modelo original e o mutado.

Os 152 casos originais foram preservados. O caso positivo, os pares simbólicos MC/DC e os vetores concretizados foram considerados unidades de execução. Para métricas, porém, a unidade positiva foi agregada por mutante: não foram contadas várias execuções do mesmo mutante como múltiplos verdadeiros positivos.

### Resultados

| Item | Resultado |
|---|---:|
| Mutantes únicos | 981 |
| Equivalentes | 21 |
| Não equivalentes classificados | 936 |
| Mortos | 894 |
| Sobreviventes | 42 |
| UNKNOWN/não avaliáveis | 24 |
| Casos do modelo original | 152 |
| Casos concretos que passaram | 140 |
| Casos não concretizados | 12 |

A partição dos mutantes é completa:

\[
981 = 894 + 42 + 21 + 24
\]

Os 24 mutantes `UNKNOWN/não avaliáveis` não são mortos ou sobreviventes. O fato de não terem sido formalizados ou avaliados deve ser registrado separadamente, não convertido em positivo ou negativo.

### Métricas reproduzidas

Para mutante agregado:

- Verdadeiro positivo: mutante não equivalente morto;
- Falso negativo: mutante não equivalente sobrevivente;
- Verdadeiro negativo: mutante equivalente não morto;
- Falso positivo: mutante equivalente morto ou rejeição incorreta do comportamento original.

| Métrica | Fórmula | Resultado |
|---|---|---:|
| Mutation Score reportado | 894 / (981 - 21) | 93,125% |
| Mutation Score excluindo não avaliáveis | 894 / (981 - 21 - 24) | 95,513% |
| Precision | 894 / (894 + 0) | 1,000 |
| Recall | 894 / (894 + 42) | 0,955 |
| F1-score | 2 × (1,000 × 0,955) / (1,000 + 0,955) | 0,977 |

Os resultados foram recomputados a partir dos artefatos JSON/CSV existentes. Os 894 mutantes mortos no registro JSON correspondem aos 894 mutantes mortos identificados no CSV de execução.

**Ressalva do Mutation Score:** a primeira fórmula reproduz o resultado originalmente registrado, mas mantém os 24 mutantes não avaliáveis no denominador por não classificá-los separadamente. Como mutantes não avaliáveis não demonstram eficácia nem sobrevivência, o número mais defensável para o conjunto avaliado é **95,513%**, obtido após excluir equivalentes e não avaliáveis.

### Comportamento original e casos não concretizados

Os 152 casos preservados foram testados contra a expressão original:

- 140 passaram;
- 12 não produziram modelo concreto e ficaram não avaliáveis.
- Nenhum caso rejeitou incorretamente o comportamento original.

Os 12 casos não concretizados não foram incluídos como TP, FP, TN ou FN. Eles são registros independentes dos 24 mutantes `UNKNOWN/não avaliáveis`.

### Análise dos resultados

- Os oráculos detectaram 894 dos 936 mutantes não equivalentes e avaliáveis.
- Precision foi 1,000 porque não foram encontrados falsos positivos contra o comportamento original ou equivalentes mortos.
- Recall foi 0,955, com 42 mutantes não equivalentes sobreviventes.
- TIS REQ002-REQ004 apresentou o menor nível observado entre os oráculos desse sistema.
- VM REQ004 e REQ005 apresentaram sobreviventes relacionados a limites e operadores relacionais.
- Mutantes de AND/OR, negações e remoções amplas tiveram, em geral, maior frequência de detecção.
- Os sobreviventes concentraram-se em operadores relacionais, alterações de constantes e remoções de condições.
- A alta quantidade de casos não implica, por si só, qualidade dos oráculos: a suíte contém casos derivados das mesmas formalizações e não é uma implementação independente do domínio.

As métricas não demonstram capacidade de detectar defeitos reais em implementação. Elas medem a discriminação dos oráculos dentro das 33 expressões formalizadas e dos casos gerados pela Experimentação 0.

## Auditoria dos cálculos

A auditoria independente confirmou:

- 981 identificadores de mutante únicos;
- 4974 pares únicos mutante/caso no registro de execução;
- correspondência exata entre os mutantes mortos no JSON e no CSV;
- ausência de dupla contagem ao agregar mortes por existência de pelo menos um caso `KILL`;
- reprodutibilidade dos totais a partir dos artefatos existentes.

A auditoria completa está em [resumo da auditoria](mutation-testing/audit/audit-summary.md) e [métricas reproduzidas](mutation-testing/audit/reproduced-metrics.csv).

## Suite executável

Foi construída uma suíte Python/Z3 executável derivada das 33 decisões NAT2TEST:

- 185 casos registrados;
- 173 concretizáveis;
- 12 não concretizáveis;
- 981 cópias JSON mutadas;
- 894 mutantes mortos;
- 42 sobreviventes;
- 21 equivalentes;
- 24 não avaliáveis;
- Mutation Score corrigido: 95,5128%;
- Precision: 1,000;
- Recall: 0,9092;
- F1: 0,9524.

Esta suíte mede a especificação formal executável, não uma implementação real de VM, TIS ou NPP.

## Próxima etapa

Os avaliadores humanos deverão validar:

1. representação Z3 das expressões;
2. alcançabilidade dos contraexemplos;
3. semântica das ações conflitantes;
4. suporte documental das interpretações da LLM;
5. adequação dos vetores simbólicos;
6. informações ausentes antes do experimento fatorial.

## Avaliação da Experimentação 0

**ADEQUADA COM RESSALVAS**

Os requisitos permitiram formalizações completas em Z3, oráculos estruturados e uma execução automatizada de mutantes em nível de especificação. Os indicadores mostram boa capacidade de detecção dentro desse conjunto: 894 mutantes mortos, Precision 1,000, Recall 0,955 e F1 0,977.

Entretanto, a conclusão é limitada por:

- ausência de implementação independente dos sistemas VM, TIS e NPP;
- dependência da tradução das guardas;
- domínios numéricos e temporais parcialmente formalizados;
- 24 mutantes não avaliáveis;
- 12 pares MC/DC não concretizados;
- 42 mutantes não equivalentes sobreviventes;
- ausência de validação humana da semântica dos requisitos.

A Experimentação 0 pode ser considerada uma linha de base formal e empírica exploratória, mas não uma validação definitiva de correção semântica ou de capacidade dos oráculos de detectar defeitos reais em implementação.
