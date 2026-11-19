# Relatório final — Experimento C4

## Resultado resumido

C4 avalia a documentação de baixa clareza e baixa consistência fornecida em [documentacao-c4.md](documentacao-c4.md). A suíte foi construída e executada contra a implementação Java original, sem alterar o código de produção nem ajustar expectativas após observar os resultados.

| Execução | Casos | Aprovados | Falhas | Erros | Desabilitados |
|---|---:|---:|---:|---:|---:|
| C4 | 40 | 23 | 11 | 0 | 6 |

As aprovações demonstram somente compatibilidade operacional. As falhas incluem expectativas concorrentes extraídas de frases contraditórias e expectativas baseadas em interpretações; não são, por si sós, prova de que a expectativa esteja semanticamente errada.

## Integridade e reprodutibilidade

- Documentação C4 congelada: SHA-256 `01A899182C6799805B192F9FC36CF64210A270797B157DB339AC6423CA2C7FB0`.
- Catálogo de oráculos, congelado antes da consulta à implementação e ao gabarito: 38 registros; SHA-256 `29188FC427D052A1CF9DBEFE966848761DFDAC09937D6AE9DFC27ACB5C3B5BBE`.
- Implementação: commit `20288f1f2e40dcd4ca3e9412f772b72a5489b188`.
- Referência independente copiada após a execução, sem alterações: [frozen-reference-catalog.csv](evidencias/referencia-independente/frozen-reference-catalog.csv), SHA-256 `EF725BCD1A36D663356A1505B77B0756201F35A58430563AABFD270450ED8118`.
- Comando: `mvn -Djacoco.skip=true test`, executado em `suite-testes/`; Java 21; Maven 3.9.11; Z3 4.15.4.
- Evidências: [test-audit.csv](evidencias/execucoes/test-audit.csv), [s2-maven-test.log](evidencias/execucoes/s2-maven-test.log), [s2-surefire-report.xml](evidencias/execucoes/s2-surefire-report.xml) e [assumptions-register.csv](evidencias/assumptions-register.csv).

Os hashes validam os arquivos locais registrados; como a documentação C4 foi transcrita manualmente da mensagem, eles não constituem prova criptográfica de identidade byte a byte com a mensagem original.

## Classificação, falhas e informações ausentes

O catálogo tem 30 oráculos documentados, 4 inferidos, 1 assumido e 3 indeterminados. Contando métodos de teste, incluindo casos repetidos para rastreabilidade, são 31 documentados, 5 inferidos, 1 assumido e 3 indeterminados. Dos 40 casos, 6 foram desabilitados: três limites/documentos sem consequência executável definida, dois casos indeterminados e um recurso que a própria documentação não confirma. O caso de Z3 sem opção permaneceu ativo apenas para registrar uma das leituras conflitantes; não recebe crédito semântico.

As 11 falhas observadas foram:

1. Tabela verdade em modo direto: a expectativa de tabela completa falhou; outra cláusula diz que modo direto não constrói a tabela completa.
2. Combinação impossível em par completo: a expectativa de contagem falhou; o outro teste que exclui a combinação passou.
3. Código de saída para relatório com condição descoberta: a expectativa de `0` falhou; a cláusula que exige código `2` passou.
4. Campo `temporal`: a expectativa de obrigatoriedade falhou; a expectativa contrária de opcionalidade passou.
5. Campos JSON literalmente corrompidos: a expectativa assumida de aceitação falhou.
6. Limite de entradas no modo direto: a expectativa de rejeitar 21 entradas falhou; a expectativa oposta de aceitá-las passou.
7. Linhas `.mcdc`: a expectativa de uma decisão para duas linhas falhou; a expectativa de duas decisões passou.
8. `truth-csv` no modo direto: a expectativa de saída parcial falhou por incompatibilidade de opção.
9. Múltiplas fontes: a expectativa de aceitar dois arquivos falhou; o comando rejeitou a cardinalidade.
10. Variante automática: a expectativa de causa única para mais de duas condições falhou; a implementação reportou mascaramento.
11. Opção grafada `--boudary`: a expectativa inferida de aceitação falhou; o parser rejeitou a opção.

Cinco métodos de teste dependeram de inferências (quatro registros do catálogo); um método/registro exigiu suposição; três métodos/registros permaneceram indeterminados. As principais informações ausentes ou incompatíveis são: nomes corretos de campos JSON; esquema e cabeçalho CSV; aridade de fontes para várias decisões; agregação de linhas `.mcdc`; critério para impossibilidades em pares completos; significado de “tabela” no modo direto; grafias canônicas das opções; obrigatoriedade do Z3; limites `20`, `30`, `096` e `46`; ação ao exceder limites de pares; formato parcialmente chamado de “quivo”; efeito do timeout; e prioridade dos códigos de saída.

## Avaliação pelas cinco métricas

A unidade de contagem é o comportamento independente no catálogo congelado de referência: 19 comportamentos. Casos duplicados contam no máximo uma vez. Assertions parciais, ambíguas, indeterminadas ou sem correspondência não recebem crédito; não são convertidas em falso positivo ou verdadeiro positivo apenas por passarem na implementação. O registro de auditoria contém a decisão por teste.

| Métrica | Cálculo C4 | Resultado |
|---|---|---:|
| Cobertura de requisitos | `9 / 19 × 100` | **47,37%** |
| Mutation Score | Suíte integral: não avaliável; subconjunto aprovado exploratório: `131 / (333 - 0)` | **39,34% exploratório** |
| Precision | `9 / (9 + 4)` | **69,23%** |
| Recall | `9 / (9 + 10)` | **47,37%** |
| F1-score | `2 × (9/13) × (9/19) / ((9/13) + (9/19))` | **56,25%** |

Os nove comportamentos de referência cobertos são B005, B006, B012, B020, B021, B025, B026, B028 e B029. As quatro expectativas contraditórias em relação ao gabarito são: tabela completa no modo direto (B025), aceitação de várias fontes (B005), aceitação de campos JSON corrompidos (B015) e seleção automática de causa única (B020). Os dez comportamentos não identificados por uma assertion válida são B004, B011, B013, B014, B015, B017, B018, B023, B024 e B027.

Para a classificação, somente correspondências únicas e suficientemente verificadas contam como TP. A expectativa incorreta conta como FP mesmo quando seu teste passa; comportamentos apenas parciais, ambíguos ou não descritos pelo gabarito ficam separados. Duplicatas não aumentam TP. Assim, resultados de execução não substituem a avaliação semântica independente.

## Mutation Testing

A linha de base original teve 11 falhas, portanto o PIT **não foi executado sobre a suíte integral** e o Mutation Score da suíte integral continua não avaliável. Para responder ao pedido posterior de executar PIT, foi feita uma execução exploratória em cópia isolada da suíte: os 11 métodos que falhavam foram desabilitados apenas nessa cópia, sem mudar os testes originais, o código de produção ou os resultados esperados. Os 23 testes restantes passaram na linha de base filtrada; os seis casos previamente desabilitados foram mantidos.

| Classificação | Quantidade |
|---|---:|
| Mutantes gerados | 333 |
| Killed | 131 |
| Survived | 82 |
| No coverage | 120 |
| Equivalent identificado | 0 |
| Timed out | 0 |
| Non-viable / Error | 0 |

O Mutation Score exploratório é `131 / (333 - 0) × 100 = 39,34%`. Mutantes `No coverage` permanecem no denominador da fórmula solicitada. O PIT não identificou equivalentes, mas não houve adjudicação semântica manual; portanto, zero identificados não prova que não existam equivalentes.

Os resultados por mutante, com o killer registrado pelo PIT, estão em [mutation-results-passing-subset.csv](evidencias/mutation-testing/exploratory/mutation-results-passing-subset.csv); o [relatório detalhado](evidencias/mutation-testing/exploratory/pit-approved-subset-report.md), XML bruto, exclusões, cópias filtradas e logs também estão em `evidencias/mutation-testing/`. O XML registra o teste detector reportado pelo PIT, não uma lista exaustiva de todos os testes que poderiam matar cada mutante. Este score mede detecção operacional somente no subconjunto aprovado; não valida a correção semântica dos oráculos nem apaga as 11 falhas da suíte original. O conjunto limpo contém 333 mutantes, diferente do conjunto histórico de 456 usado em C2/C3, e não é diretamente comparável a ele.

## Comparação descritiva

| Métrica | C1 | C2 (S3) | C3 (S3) | C4 |
|---|---:|---:|---:|---:|
| Cobertura de requisitos | Não disponível | 11/19 = 57,89% | 13/19 = 68,42% | 9/19 = **47,37%** |
| Mutation Score | Não disponível | 218/456 = 47,81% | Suíte integral: não avaliável; subconjunto aprovado exploratório: 118/333 = 35,44% | Suíte integral: não avaliável; subconjunto aprovado exploratório: **131/333 = 39,34%** |
| Precision | Não disponível | 100,00% | 86,67% | **69,23%** |
| Recall | Não disponível | 57,89% | 68,42% | **47,37%** |
| F1-score | Não disponível | 73,33% | 76,47% | **56,25%** |

C1 não tem geração/avaliação de oráculos comparável registrada. C2/C3/C4 usam a referência de 19 comportamentos, mas não têm exatamente o mesmo desenho de suíte ou execução. Descritivamente, C4 tem a menor cobertura, Recall e F1 entre C2–C4; também tem quatro FPs independentes e a menor Precision. Isso é compatível com a hipótese de que baixa clareza combinada com contradições dificulte identificar expectativas confiáveis, mas não estabelece causalidade. Os scores exploratórios C3/C4 usam o mesmo conjunto de 333 mutantes e os subconjuntos aprovados; não são scores das suítes integrais nem diretamente comparáveis ao C2 de 456 mutantes.

## Conclusão e limitações

A documentação permitiu construir 40 casos, mas as contradições produziram expectativas mutuamente incompatíveis e o gabarito independente identificou quatro expectativas incorretas. O processo encontrou nove comportamentos válidos, deixando dez sem cobertura válida. Ainda que 23 casos tenham passado e o subconjunto aprovado tenha matado 131 mutantes, isso não elimina a baixa confiabilidade semântica: aprovação operacional e kills não validam o oráculo. A linha de base vermelha impede um score válido da suíte integral.

Os resultados são descritivos de um sistema, uma documentação e uma geração de suíte. O gabarito contém 19 comportamentos e pode não representar todas as regras possíveis; casos fora dele foram mantidos como ambíguos ou não comparáveis, em vez de forçados para TP/FP/FN.
