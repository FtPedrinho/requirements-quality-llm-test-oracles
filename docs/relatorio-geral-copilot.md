# Relatório geral dos experimentos assistidos pelo Copilot — C0 a C4

**Data de consolidação:** 18/11/2026  
**Escopo:** resultados disponíveis para os cinco experimentos, diferenças entre clareza e consistência documental e limitações de comparabilidade.

## 1. Síntese executiva

A pesquisa investiga se documentação técnica e requisitos podem apoiar a geração de oráculos de teste por LLMs e como clareza e consistência afetam a completude e a confiabilidade desses oráculos. C0 é exploratório; C1–C4 representam, de forma pretendida, as quatro combinações de clareza e consistência.

Os resultados principais, comparáveis sobre o gabarito de 19 comportamentos, são:

| Condição | Clareza / consistência | Cobertura | Mutation Score | Precision | Recall | F1 |
|---|---|---:|---:|---:|---:|---:|
| C0 | Linha de base exploratória | Não avaliável nessa referência | Ver seção 4; alvos distintos | Não avaliável | Não comparável | Não comparável |
| C1 | Clareza alta; consistência alta pretendida, não confirmada | Não avaliável nessa referência | Ver seção 4; alvos distintos | Não avaliável | Não comparável | Não comparável |
| C2 | Clareza baixa; consistência preservada | **11/19 — 57,89%** | **218/456 — 47,81%** no alvo core | **100,00%** | **57,89%** | **73,33%** |
| C3 | Clareza alta; consistência baixa | **13/19 — 68,42%** | Suíte integral: **não avaliável**; subconjunto aprovado exploratório: **118/333 — 35,44%** | **86,67%** | **68,42%** | **76,47%** |
| C4 | Clareza baixa; consistência baixa | **9/19 — 47,37%** | Suíte integral: **não avaliável**; subconjunto aprovado exploratório: **131/333 — 39,34%** | **69,23%** | **47,37%** | **56,25%** |

C2, C3 e C4 sugerem padrões distintos: baixa clareza com consistência preservada coincidiu com omissões; contradições em texto legível coincidiram com mais comportamentos encontrados, mas também com oráculos incorretos e falhas na execução-base; a combinação de baixa clareza e baixa consistência apresentou os menores valores de cobertura, Precision, Recall e F1. Isso é evidência descritiva, **não demonstra causalidade**.

O Mutation Score não mede sozinho a correção semântica do oráculo. Em C2, por exemplo, a suíte complementar matou mutantes, mas grande parte desses kills foi atribuída a testes assumidos ou inferidos. Um teste pode detectar uma alteração e ainda ter uma expectativa sem sustentação documental.

Os scores C3/C4 de 333 mutantes são execuções exploratórias em subconjuntos que passaram na linha de base filtrada. Não substituem os scores das suítes integrais, que permanecem não avaliáveis, e não são diretamente comparáveis ao conjunto histórico de 456 mutantes de C2/C3. C3 e C4 usaram o mesmo conjunto exploratório de mutantes; o desenho e o tamanho dos subconjuntos diferem.

## 2. Contexto, condições e proveniência

| Experimento | Condição pretendida | Descrição da documentação e do processo |
|---|---|---|
| C0 | Linha de base | Documentação original, sem manipulação controlada. Inclui uma trilha formal VM/TIS/NPP e uma trilha separada de testes da ferramenta MC/DC. |
| C1 | Alta clareza / alta consistência | Documentação reorganizada e mais clara; guardas e ações preservadas. A consistência alta foi uma intenção, não uma propriedade integralmente confirmada. |
| C2 | Baixa clareza / alta consistência | Texto degradado linguisticamente, mas com consistência terminológica e lógica declarada como preservada. Foram mantidos 26 testes originais e tentados 10 complementares. |
| C3 | Alta clareza / baixa consistência | Texto legível com contradições/tensões registradas antes da execução. A análise documental identificou 10 contradições/tensões e 4 regras aparentemente compatíveis. |
| C4 | Baixa clareza / baixa consistência | Texto com erros, frases incompletas, ambiguidades, omissões e afirmações incompatíveis. A suíte contém 40 casos ligados a 38 registros do catálogo. |

O registro de proveniência de C0 e C1 é inconsistente: alguns artefatos atribuem oráculos ao Copilot, outros não documentam uma geração independente ou deixam a atribuição ambígua. C2 registra que os complementos foram produzidos pelo agente Copilot; C3 e C4 também registram geração pelo Copilot. Modelo, versão e parâmetros não estão suficientemente harmonizados para atribuir todos os resultados a uma única versão do Copilot.

## 3. Clareza e consistência observadas

### C0 e C1: efeito da revisão de clareza

A avaliação documental de C0 e C1 mediu clareza e consistência em escala de 1 a 5:

| Medida | C0/original | C1 | Variação |
|---|---:|---:|---:|
| Clareza média | 4,06 | 4,97 | +0,91 |
| Consistência média | 4,67 | 4,67 | 0,00 |

A organização e a clareza melhoraram, mas permaneceram quatro pares de ações potencialmente incompatíveis e uma variável de saída NPP não declarada. As guardas e ações formalizadas não mudaram; por isso, resultados iguais na trilha formal C0/C1 não demonstram que a melhoria textual tenha aumentado a qualidade dos oráculos.

### C2: pouca clareza sem contradições deliberadas

A comparação documental C1–C2 classificou C2 como de ambiguidade lexical máxima controlada, especificidade muito baixa e condições/sintaxe indiretas e fragmentadas, mantendo alta a consistência terminológica e lógica. Nos resultados, a Precision de 100% não impediu que oito dos 19 comportamentos do gabarito ficassem sem cobertura válida na suíte combinada. O padrão é compatível com uma documentação que não leva necessariamente a oráculos falsos, mas dificulta identificar todas as expectativas.

### C3: texto claro com contradições

C3 mostra que legibilidade não resolve inconsistência: 13/19 comportamentos foram cobertos, mas a Precision da suíte combinada caiu para 86,67%, com duas expectativas contraditórias com o gabarito. As dez contradições/tensões são rastreadas em [contradictions.csv](../experimentacao/experimentacao-3/contradictions.csv). As sete falhas da linha de base refletem expectativas concorrentes mantidas deliberadamente, não uma autorização para escolher retrospectivamente a que faria o teste passar.

### C4: combinação de baixa clareza e baixa consistência

C4 teve 9/19 comportamentos cobertos, quatro falsos positivos e dez falsos negativos segundo a avaliação registrada. A suíte-base apresentou 11 falhas; por isso, o Mutation Score integral continua não avaliável. Em execução exploratória posterior, os 11 métodos que falhavam foram desabilitados somente em cópias isoladas; os 23 restantes passaram e o PIT matou 131/333 mutantes (39,34%). A documentação exigiu inferências, suposições e manutenção explícita de casos indeterminados. Os resultados são compatíveis com prejuízo simultâneo à completude e à confiabilidade semântica, mas C4 não é uma replicação controlada dos demais experimentos.

## 4. Resultados e métricas por experimento

### 4.1 C0 — linha de base exploratória

**Trilha formal VM/TIS/NPP**

- 36 expressões/requisitos: 33 decisões NAT2TEST e 3 expressões gerais.
- 36 oráculos, 152 casos simbólicos e 119 pares MC/DC.
- 185 casos na versão executável do modelo: 173 concretizáveis e 12 não concretizados.
- 981 mutantes de especificação: 894 mortos, 42 sobreviventes, 21 equivalentes e 24 não avaliáveis.
- Mutation Score arquivado: 93,125% excluindo equivalentes do denominador, mas mantendo não avaliáveis; recalculado excluindo também os 24 não avaliáveis: 95,513%.
- Uma [auditoria reproduzida](../experimentacao/experimentacao-0/mutation-testing/audit/reproduced-metrics.csv) registra Precision 100%, Recall 95,513% e F1 97,705% para mutantes. Outros relatórios históricos apresentam Recall/F1 de 90,92%/95,24%; sem unidade/agregação harmonizada, não se escolhe um par como métrica única.

**Trilha da ferramenta Java**

- 25 testes JUnit aprovados.
- O resumo histórico reporta 320 mutantes PIT mortos de 333 (96,096%).
- Esse PIT avalia a suíte de regressão da ferramenta MC/DC, não a correção de oráculos VM/TIS/NPP nem uma avaliação contra o gabarito de 19 comportamentos.

C0 não tem Cobertura, Precision, Recall e F1 comparáveis ao gabarito independente usado em C2–C4.

### 4.2 C1 — alta clareza e consistência pretendida

- Clareza média: 4,06 → 4,97; consistência média: 4,67 → 4,67.
- 36 requisitos, 36 oráculos, 152 casos simbólicos, 119 pares MC/DC e 185 casos executáveis foram mantidos na trilha formal.
- Os resultados formais da série de 981 mutantes são iguais aos de C0: 894 mortos, 42 sobreviventes, 21 equivalentes e 24 não avaliáveis; MS arquivado de 93,125% ou 95,513% com a exclusão adicional dos não avaliáveis.
- A execução da ferramenta registra 25/25 testes aprovados e o mesmo resultado histórico de 320/333 mutantes PIT (96,096%).
- Não há avaliação de oráculos C1 por uma geração independente e anotação contra o gabarito de 19 comportamentos.

O [arquivo de resultados C1](../experimentacao/experimentacao-1/results-summary.csv) também apresenta uma quebra por sistema na trilha formal:

| Sistema | Killed / total | Survived | Equivalent | Unknown | MS corrigido | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Safety injection | 213/223 | 4 | 0 | 6 | 98,16% | 100% | 98,16% | 99,07% |
| Coffee machine | 164/191 | 9 | 0 | 18 | 94,80% | 100% | 94,80% | 97,33% |
| Turn indicator/TIS | 517/567 | 29 | 21 | 0 | 94,69% | 100% | 94,69% | 97,27% |

Esses valores são métricas da trilha formal de mutantes; não devem ser misturados às métricas de qualidade dos oráculos em C2–C4.

### 4.3 C2 — baixa clareza, consistência preservada

**Execução**

| Suíte | Testes | Aprovados | Falhas | Ignorados |
|---|---:|---:|---:|---:|
| S1 — originais | 26 | 26 | 0 | 0 |
| S2 — complementares | 10 | 9 | 0 | 1 |
| S3 — combinada | 36 | 35 | 0 | 1 |

Na S2, foram registrados 2 casos inferidos, 7 assumidos e 1 indeterminado. O caso indeterminado foi atribuído a `Z3 UNKNOWN`.

**Cinco métricas contra o gabarito independente de 19 comportamentos**

| Métrica | S1 | S2 | S3 |
|---|---:|---:|---:|
| Cobertura | 9/19 = 47,37% | 2/19 = 10,53% | 11/19 = 57,89% |
| Mutation Score — core, 456 mutantes | 152/456 = 33,33% | 198/456 = 43,42% | 218/456 = 47,81% |
| Precision | 100,00% | 100,00% | 100,00% |
| Recall | 47,37% | 10,53% | 57,89% |
| F1 | 64,29% | 19,05% | 73,33% |

Na S3 do alvo core, 218 mutantes foram mortos, 162 sobreviveram, 71 ficaram sem cobertura, 5 tiveram timeout e nenhum equivalente foi identificado. Dos 198 kills associados à S2, 188 tiveram como primeiro killer testes assumidos e 10 inferidos; somente 23 kills tinham correspondência corroborada pelo gabarito. Portanto, o score operacional não certifica a confiabilidade semântica.

Há também uma série separada para a CLI com 256 registros por suíte: S1 teve 72 kills, 109 sobreviventes, 69 sem cobertura e 6 timeouts; S2 teve 97, 81, 73 e 5; S3 teve 110, 100, 38 e 8, respectivamente. Sem equivalentes registrados, os quocientes K/256 são 28,13%, 37,89% e 42,97%. Esses valores são de outro alvo e não substituem o MS core de 456 mutantes.

**Registros históricos não reconciliados em C2:** [oracle-metrics.csv](../experimentacao/experimentacao-2/metrics/oracle-metrics.csv) usa 34 comportamentos (18 TP, 0 FP, 16 FN), enquanto o relatório final usa o gabarito de 19 comportamentos (11 TP, 0 FP, 8 FN). [mutation-metrics.csv](../experimentacao/experimentacao-2/metrics/mutation-metrics.csv) reporta 320/333 = 96,096%, mas seus estados listados somam 334 e o caminho de origem cita `mcdc-core`, diferindo dos arquivos de cenário [core (456 mutantes)](../experimentacao/experimentacao-2/mutation-testing/mutation-results-combined.csv) e [CLI (256 mutantes)](../experimentacao/experimentacao-2/mutation-testing/mutation-results-cli-combined.csv). O relatório principal desta consolidação mantém como resultados comparáveis os números registrados em [results.md](../experimentacao/experimentacao-2/results.md) para o gabarito de 19 comportamentos e a série core de 456; os outros registros ficam sinalizados, não apagados nem combinados.

### 4.4 C3 — alta clareza, baixa consistência

**Execução**

| Suíte | Testes | Aprovados | Falhas | Ignorados |
|---|---:|---:|---:|---:|
| S1 — documental | 49 | 37 | 7 | 5 |
| S2 — complementar | 5 | 1 | 0 | 4 |
| S3 — combinada | 54 | 38 | 7 | 9 |

**Cinco métricas**

| Métrica | S1 | S2 | S3 |
|---|---:|---:|---:|
| Cobertura | 12/19 = 63,16% | 1/19 = 5,26% | 13/19 = 68,42% |
| Mutation Score da suíte integral | Não avaliável | 0/456 = 0,00%* | Não avaliável |
| Precision | 85,71% | 100,00% | 86,67% |
| Recall | 63,16% | 5,26% | 68,42% |
| F1 | 72,73% | 10,00% | 76,47% |

\* Na execução histórica, o S2 teve todos os 456 mutantes em `NO_COVERAGE`; 0% não significa que houve cobertura e todos os mutantes sobreviveram. As execuções integrais de S1/S3 foram bloqueadas pelas sete falhas da linha de base. Em execução posterior e exploratória, 38 testes aprovados do subconjunto S3 detectaram 118/333 mutantes (35,44%); 110 sobreviveram, 105 ficaram sem cobertura, nenhum equivalente foi identificado e não houve timeout ou erro. Os sete casos que falhavam foram desabilitados somente em cópias isoladas. O conjunto 333 não é o conjunto histórico 456 e não substitui o resultado da suíte integral. A suíte combinada teve duas expectativas contra o gabarito.

### 4.5 C4 — baixa clareza e baixa consistência

**Execução:** 40 casos, 23 aprovados, 11 falhas, nenhum erro de teste e 6 desabilitados. O catálogo contém 30 oráculos documentados, 4 inferidos, 1 assumido e 3 indeterminados. A suíte integral continua sem Mutation Score avaliável por causa das 11 falhas. Em uma execução exploratória posterior, os 11 métodos que falhavam foram desabilitados somente em cópia isolada; os 23 restantes passaram e o PIT matou 131/333 mutantes (39,34%), com 82 sobreviventes, 120 sem cobertura e nenhum equivalente identificado, timeout ou erro.

| Métrica | Resultado |
|---|---:|
| Cobertura | 9/19 = 47,37% |
| Mutation Score | Suíte integral: não avaliável; subconjunto aprovado exploratório: 131/333 = 39,34% |
| Precision | 9/(9+4) = 69,23% |
| Recall | 9/(9+10) = 47,37% |
| F1 | 56,25% |

As falhas preservadas incluem interpretações opostas para tabela no modo direto, combinações impossíveis, código de saída, campo `temporal`, limite do modo direto, múltiplas linhas `.mcdc` e variante MC/DC. Quatro expectativas foram classificadas como falsos positivos contra a referência; dez comportamentos do gabarito não tiveram oráculo válido correspondente. A auditoria por caso está em [test-audit.csv](../experimentacao/experimentacao-4/evidencias/execucoes/test-audit.csv).

## 5. Comparação dos fatores e interpretação

### Clareza

1. **Efeito observado em C0→C1:** a avaliação da documentação registra aumento de 4,06 para 4,97 na clareza, sem mudança da média de consistência (4,67). Isso demonstra melhora na rubrica documental, mas não permite concluir que a clareza sozinha elevou a correção dos oráculos, pois não há avaliação C1 independente no gabarito de 19 comportamentos e as regras formais foram preservadas.
2. **C2:** texto de baixa clareza com consistência preservada obteve Precision de 100%, mas Recall de 57,89%. No conjunto medido, o problema aparece mais como omissão/completude insuficiente do que como expectativas falsas.
3. **C4:** com baixa clareza e baixa consistência, tanto Precision (69,23%) quanto Recall (47,37%) ficaram menores que em C2/C3. Isso é compatível com a dificuldade adicional de interpretar trechos e escolher entre afirmações concorrentes.

### Consistência

1. **C3 versus C2:** C3, apesar das contradições, teve maior cobertura e Recall (68,42%) que C2 (57,89%), mas menor Precision (86,67% versus 100%) e sete falhas na linha de base. A clareza pode ter ajudado a extrair mais comportamentos, enquanto as contradições prejudicaram a escolha de expectativas corretas.
2. **C4:** a presença simultânea de baixa clareza e inconsistência coincidiu com queda de Precision, Recall e F1. Os testes passaram ou falharam operacionalmente diante da implementação, mas o gabarito foi necessário para avaliar quais expectativas eram semanticamente defensáveis.
3. **Mutation Score:** C2 demonstra que uma suíte pode matar mutantes usando oráculos assumidos. Os subconjuntos aprovados C3/C4 também mataram mutantes, mas seus resultados não certificam a semântica dos oráculos. Na execução exploratória, C4 teve 13 kills a mais e MS 3,90 pontos percentuais maior que C3 (39,34% versus 35,44%) sobre as mesmas 333 mutações; como quantidade e composição dos testes diferem, isso não demonstra efeito causal da clareza ou consistência.

## 6. Limitações para conclusão causal

- C0 é exploratório e C1 tem proveniência de geração não reconciliada; não são comparáveis às métricas de oráculo C2–C4.
- As notas numéricas de clareza/consistência só estão disponíveis de forma consistente para C0/C1. C2–C4 são classificados qualitativamente, não por uma mesma rubrica aplicada e validada.
- C2/C3/C4 usam o gabarito de 19 comportamentos, mas a quantidade e estrutura das suítes diferem; C4 não tem o mesmo arranjo S1/S2/S3.
- Alvos PIT e denominadores variam entre trilha formal de especificação, regressão da ferramenta, core e CLI. Resultados desses alvos não são somáveis.
- Há artefatos históricos C2 com denominadores conflitantes; foram preservados como divergências, não usados para alterar os resultados principais.
- A versão exata do Copilot e os parâmetros de geração não estão registrados de modo uniforme.
- C4 contém uma transcrição manual da documentação recebida; o hash identifica o arquivo local, não prova identidade byte a byte com a mensagem original.

## 7. Conclusão geral

Os dados disponíveis sugerem que **clareza e consistência afetam aspectos diferentes** da geração de oráculos. A clareza favorece a identificação e decomposição dos comportamentos; quando baixa, aumenta omissões, inferências e dependência de suposições. A consistência reduz a competição entre expectativas; quando baixa, permite que um texto individualmente legível produza oráculos mutuamente incompatíveis e reduza Precision, além de impedir uma linha de base verde.

C2 reforça que consistência não garante completude. C3 reforça que clareza não resolve contradições. C4 sugere que a combinação pode prejudicar tanto completude quanto confiabilidade semântica. Como as condições históricas não foram executadas sob um protocolo fatorial inteiramente uniforme, esses achados devem ser tratados como **tendências observadas**, não como prova causal nem como avaliação universal do Copilot.

## 8. Relatórios e evidências por experimento

- [C0 — resultados](../experimentacao/experimentacao-0/results.md)
- [C1 — resultados](../experimentacao/experimentacao-1/results.md)
- [C2 — resultados](../experimentacao/experimentacao-2/results.md)
- [C3 — resultados](../experimentacao/experimentacao-3/results.md)
- [C4 — relatório final](../experimentacao/experimentacao-4/relatorio-final.md)
- [README geral da pesquisa](../README.md)
