# Análise dos dez casos ausentes da suíte C2

## Resultado da tentativa

Foram preservados os 26 métodos originais executáveis e adicionados 10 casos em S2. Contra a implementação Java instalada, S2 teve 9 aprovações e 1 caso ignorado. A execução confirma apenas que o código observado satisfaz as asserções; a validade semântica foi avaliada separadamente contra o gabarito independente congelado.

| Caso S2 | Associação C2 | Classe | Execução | Resultado frente ao gabarito independente |
|---|---|---|---|---|
| CSV de `check` válido | B016 | Assumido | PASS | Sem unidade correspondente no catálogo independente |
| Ocorrências repetidas de entrada | B019 | Assumido | PASS | Sem unidade correspondente |
| Restrição inviável | B022 | Assumido | PASS | Sem unidade correspondente |
| Seleção padrão gulosa | B023 | Assumido | PASS | Parcial: verifica o rótulo, não os pares selecionados |
| Seleção exata | B024 | Inferido | PASS | Parcial: `tamanho(exata) <= tamanho(gulosa)` não prova minimalidade |
| Relatório interno de mutação | B027 | Assumido | PASS | Corresponde ao B027 independente quanto a relatório, score e sobreviventes |
| Sobreposição compatível | B003 | Inferido | PASS | Sem unidade correspondente |
| Resultado Z3 `UNKNOWN` | B034 | Indeterminado | SKIPPED | Sem resultado esperado ou entrada determinística justificável em C2 |
| `truth-csv` com uma linha por combinação | B032 | Assumido | PASS | Corresponde ao B018 independente quanto a 2^n linhas; cabeçalho continua sem validação independente |
| Truncamento de listas de pares | B018 | Assumido | PASS | Não corresponde ao B018 independente, que é a tabela-verdade |

As entradas, resultados esperados, trechos de origem, justificativas, lacunas, inferências e suposições por caso estão em [`assumptions-register.csv`](./assumptions-register.csv).

## Classificação

- Documentados: **0**.
- Inferidos: **2** (seleção exata; sobreposição compatível).
- Assumidos: **7**.
- Indeterminados: **1**.

O caso inferido da seleção exata traduz “procura seleçao exata” como cardinalidade não maior que a seleção padrão. Essa condição é necessária, mas não demonstra minimalidade. A sobreposição compatível interpreta a afirmação sobre valores diferentes como distinção em relação a valores iguais; a documentação não define essa regra.

Os casos assumidos incluem o esquema de CSV, sufixos `#1/#2`, marcador `INFEASIBLE`, algoritmo/rótulo `GREEDY`, opção e campos de mutação, cabeçalho de `truth-csv` e reticências. Não se alterou a documentação C2. O teste de `UNKNOWN` permanece registrado, mas desabilitado porque C2 não permite provocar esse resultado de modo determinístico nem determinar sua resposta.

## Gabarito, identificadores e regra de avaliação

O gabarito congelado em `oracle-reference/oracle-reference-catalog.csv` contém 19 comportamentos validados. O catálogo C2 gerado a partir da documentação tem 34 IDs e alguns IDs não conservam a mesma semântica do gabarito: por exemplo, o B018 gerado para C2 é limite de entradas/truncamento, enquanto o B018 independente é quantidade de linhas da tabela-verdade. A comparação foi feita pela descrição do comportamento, e não por igualdade numérica de IDs. O catálogo congelado não foi alterado.

Um caso assumido pode receber crédito **somente** quando a asserção observada coincide com um critério explícito do gabarito independente; aprovação na execução, por si só, não concede crédito. Sob essa regra:

- `truthCsvContainsOneRecordPerBooleanCombination` confirma quatro linhas de dados para duas condições, alinhadas ao B018 independente (2^n). Os nomes e a ordem das colunas permanecem suposições sem crédito separado.
- `mutationOptionReportsObservedScore` confirma os campos de relatório `score` e `survivors`, alinhados ao B027 independente.
- Os outros oito casos não identificam integralmente um comportamento independente válido: não correspondem ao catálogo, verificam apenas uma parte insuficiente do critério, ou são indeterminados.

Assim, os dois casos acima acrescentam **2 TP** à comparação de oráculos e elevam a cobertura de S3 em dois comportamentos frente a S1. Os detalhes e créditos por método estão em [`test-audit.csv`](./test-audit.csv).

## Cobertura e métricas de oráculos

O denominador de cobertura/Recall é o catálogo independente congelado, **R_t = 19**, não os 34 IDs do catálogo C2 gerado. Os comportamentos efetivamente verificados são:

- S1: 9/19 — B005, B006, B012, B013, B014, B015, B017, B028 e B029.
- S2: 2/19 — tabela-verdade 2^n (B018 independente) e relatório de mutação com score/sobreviventes (B027 independente).
- S3: 11/19 — união sem duplicar requisitos.

Para a matriz de oráculos, cada comportamento independente é contado no máximo uma vez. Assertions parciais não recebem TP; não há assertion contraditória identificada (FP=0). Os comportamentos válidos do gabarito não identificados integralmente são FN. O caso `UNKNOWN`, os oito casos S2 sem validação integral e as suposições extras de cabeçalho não são introduzidos como novas unidades positivas ou negativas; permanecem relatados separadamente. Os resultados numéricos e a divergência com métricas históricas estão em [`metrics.md`](./metrics.md).

## Eficácia operacional versus confiabilidade semântica

S2 matou 198 mutantes no PIT; isso mede capacidade operacional de distinguir versões mutadas. Pelo teste registrado como primeiro killer, 188 desses kills vieram de casos classificados como assumidos e 10 de casos inferidos. Dois casos assumidos — mutação e contagem da tabela-verdade — tiveram confirmação independente para as asserções delimitadas acima; seus 19 e 4 kills, respectivamente, somam 23. Os **165** kills restantes atribuídos a oráculos assumidos não têm confirmação correspondente no gabarito. Dos 10 kills inferidos, sete são atribuídos ao teste de seleção exata: a desigualdade de tamanho é compatível com o gabarito, mas não prova minimalidade; os três restantes vêm da sobreposição compatível, sem unidade correspondente no catálogo.

Um kill não transforma expectativa não documentada em requisito correto. A relação de killer do PIT aponta o primeiro teste detectado, não prova exclusividade causal nem confiabilidade semântica. Os mutantes, inclusive sobreviventes, estão discriminados nos CSVs completos.
