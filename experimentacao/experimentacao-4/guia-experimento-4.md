# Guia do Experimento C4

## Objetivo e motivação

Investigar como requisitos técnicos com baixa clareza e baixa consistência afetam a geração de oráculos e de uma suíte executável por Copilot. O objetivo é observar a interpretação da especificação, a completude e confiabilidade semântica dos oráculos e, se a execução-base permitir, a capacidade da suíte de detectar mutações no sistema MC/DC.

## Pergunta de pesquisa

Como a combinação de baixa clareza e baixa consistência documental afeta a correção semântica, a cobertura e a executabilidade dos oráculos gerados por IA?

## Condição C4

C4 representa **baixa clareza e baixa consistência**. A entrada é a cópia literal em [documentacao-c4.md](documentacao-c4.md), fornecida pelo usuário. Erros ortográficos, frases incompletas, ambiguidades, contradições e omissões são parte do tratamento; não devem ser corrigidos para facilitar a geração.

SHA-256 da cópia congelada: `01A899182C6799805B192F9FC36CF64210A270797B157DB339AC6423CA2C7FB0`.

## Procedimento

1. Congelar a documentação de entrada e registrar seu hash.
2. Analisar somente esse documento, registrando trechos, ambiguidades, contradições, omissões e alternativas interpretativas.
3. Concluir e congelar o catálogo de oráculos em `suite-testes/oracle-catalog.csv`, sem consultar código-fonte, documentação de outros experimentos ou o gabarito independente.
4. Só então inspecionar a interface executável para construir os testes; essa inspeção pode orientar formato de entrada e execução, mas não pode decidir o comportamento esperado.
5. Executar a suíte na implementação original, sem alterar código de produção. Registrar por teste entrada, expectativa, resultado, estado e explicação.
6. Depois de congelados os oráculos, copiar e verificar o sistema em área isolada, registrar commit/hash e estabelecer a linha de base. Executar PIT na cópia somente se a suíte passar sem mutação. Uma linha de base falha impede um Mutation Score válido.
7. Só depois da geração e execução, localizar a referência independente já existente, preservá-la e avaliar correspondências semânticas. Não modificar nem usar a referência durante a geração dos oráculos.
8. Calcular as cinco métricas e registrar limitações e evidências em `evidencias/`.

## Classificação dos oráculos

- **Documentado:** expectativa explicitamente declarada no documento.
- **Inferido:** interpretação plausível derivada de trechos existentes.
- **Assumido:** hipótese inventada para viabilizar um cenário testável, sem suporte documental suficiente.
- **Indeterminado:** não há expectativa confiável ou a documentação contém conflito que impede escolher uma.

Expectativas concorrentes devem permanecer identificadas como alternativas e não ser silenciosamente resolvidas. A classificação documental não confere crédito de correção. Teste aprovado não prova que o oráculo está semanticamente certo; teste falho não prova que o oráculo está errado.

## Referência independente

O catálogo de referência dos experimentos anteriores será localizado somente após o congelamento do catálogo C4. A comparação será semântica, não baseada apenas em identificadores. Um comportamento sem correspondência defensável será registrado como ambíguo/não avaliável, e não contado automaticamente como FP ou FN. Oráculos assumidos não recebem crédito automático.

## Métricas principais

Usar somente:

1. **Cobertura de requisitos:** `R_c / R_t × 100`, em que `R_c` é o número de comportamentos independentes efetivamente verificados por assertions válidas e `R_t` é o total de comportamentos no gabarito.
2. **Mutation Score:** `K / (M - E) × 100`, em que `K` é o número de mutantes mortos, `M` o total gerado e `E` os equivalentes identificados. Timeout, erro, não cobertura e não avaliável permanecem discriminados; não são kills.
3. **Precision:** `TP / (TP + FP)`.
4. **Recall:** `TP / (TP + FN)`.
5. **F1-score:** `2 × Precision × Recall / (Precision + Recall)`.

TP exige correspondência independente e assertion suficiente; FP exige contradição com o gabarito; FN é comportamento de referência sem oráculo válido correspondente. Casos sem critério independente suficiente são separados e não forçados para TP/FP/FN. Se o denominador não permitir o cálculo, relatar como não avaliável.

## Controles e reprodutibilidade

- A única fonte normativa para gerar expectativas é `documentacao-c4.md`.
- Não consultar código, documentação externa, resultados anteriores ou gabarito durante a geração.
- Não modificar implementação, gabarito, testes depois de observar os resultados, ou a documentação recebida.
- Preservar cada teste e seu oráculo em catálogo rastreável.
- Registrar hash do documento, commit/hash do sistema, versões de Java/Maven/Z3/PIT, comandos e logs.
- Colocar todos os artefatos do C4 sob esta pasta: suíte em `suite-testes/` e evidências em `evidencias/`.
- Se uma etapa for bloqueada, documentar o motivo e não inventar o resultado.

O catálogo inicial gerado somente da documentação tem 38 registros. SHA-256: `29188FC427D052A1CF9DBEFE966848761DFDAC09937D6AE9DFC27ACB5C3B5BBE`. Qualquer alteração posterior será registrada como nova versão, sem sobrescrever a entrada congelada.

## Estado e evidências da execução

A suíte complementar contém 40 casos associados aos 38 registros do catálogo. No snapshot `20288f1f2e40dcd4ca3e9412f772b72a5489b188`, a execução produziu 23 aprovações, 11 falhas, nenhum erro de teste e 6 casos desabilitados. As falhas contraditórias permaneceram intactas; aprovação indica apenas compatibilidade operacional, não correção semântica.

A referência independente foi copiada após a geração e execução para `evidencias/referencia-independente/frozen-reference-catalog.csv`; SHA-256: `EF725BCD1A36D663356A1505B77B0756201F35A58430563AABFD270450ED8118`. A auditoria por caso está em `evidencias/execucoes/test-audit.csv`, e o log do Maven e o relatório Surefire estão no mesmo diretório.

O PIT não foi executado sobre a suíte integral porque a linha de base tem falhas; o Mutation Score integral C4 permanece **não avaliável**, e não zero. Após solicitação posterior, foi realizada uma execução exploratória em subconjunto aprovado, desabilitando apenas cópias dos testes que falhavam. O subconjunto não substitui o protocolo original nem o score integral; seus detalhes e métricas estão em `relatorio-final.md` e `evidencias/mutation-testing/mutation-status.md`.

## Limitações previstas

A especificação pode não permitir construir expectativas confiáveis para parte dos comportamentos. Contradições podem produzir uma suíte-base vermelha, impedindo PIT. Mesmo quando um teste passa ou mata um mutante, isso mede compatibilidade operacional, não validade semântica; a avaliação contra a referência é uma etapa independente posterior.
