# Metodologia experimental comum — C0-C4

## 1. Objetivo e desenho

Investigar como diferentes níveis de clareza e consistência da documentação técnica influenciam LLMs ao gerar oráculos e suítes de testes para a ferramenta Java MC/DC. Para esta pesquisa, a documentação congelada de cada condição é a referência normativa do oráculo, mesmo quando divergir do comportamento real do SUT. O objetivo inclui cobertura estrutural, executabilidade, resultados de execução, conformidade documental dos oráculos e eficiência operacional.

**Objetivo de geração:** buscar a maior quantidade possível de testes significativos aprovados e a maior Branch Coverage possível, contemplando requisitos e comportamentos documentados com oráculos sustentados exclusivamente pela documentação técnica e de requisitos. Exercitar cenários, entradas e fronteiras distintos, sem inflar a quantidade com duplicatas sem contribuição. A aprovação é um resultado observado, não garantia nem critério para excluir testes: manter testes que falhem diante de divergências do SUT. Nunca sacrificar comportamento documentado, conformidade ou validade do oráculo por quantidade, aprovação, velocidade ou cobertura.

| C | Clareza | Consistência | Tratamento |
|---|---|---|---|
| C0 | Documentação original; caracterizar, sem rotular por suposição | Documentação original; caracterizar, sem rotular por suposição | Condição natural; análise separada |
| C1 | Alta pretendida | Alta pretendida | Fatorial |
| C2 | Baixa pretendida | Alta pretendida | Fatorial |
| C3 | Alta pretendida | Baixa pretendida | Fatorial |
| C4 | Baixa pretendida | Baixa pretendida | Fatorial |

As categorias pretendidas precisam ser caracterizadas antes da geração; não são evidência de que a manipulação atingiu o nível. As documentações de requisitos originais e experimentais são fontes congeladas e não devem ser modificadas durante esta pesquisa.

### Fontes normativas para o reinício

Usar somente a fonte correspondente à condição, verificando seu hash antes da geração. As execuções e oráculos anteriores com Copilot foram descartados da análise atual e não devem orientar a nova geração.

| Condição | Fonte | SHA-256 |
|---|---|---|
| C0 | [tool-readme-original.md](../documentacao-original/tool-readme-original.md) | `72B827BDEE6CE859527765CFF574A473519C00A1AF9AA9F3AACCE4236A4995F8` |
| C1 | [tool-readme-C1.md](../../experimentacao/experimentacao-1/documentation/tool-readme-C1.md) | `91981FA0181E5CC1BC5A67DAAFC965BB82D6F8EB0A6D47EB58CE291A3EF5D33B` |
| C2 | [tool-readme-C2.md](../../experimentacao/experimentacao-2/documentation/tool-readme-C2.md) | `61C4062B5FC6B4F364F40465B0E017C80E0FA0C5433412EB2E925C545F6EFBE1` |
| C3 | [tool-readme-C3.md](../../experimentacao/experimentacao-3/documentation/tool-readme-C3.md) | `F18B0821D79C7315486C13D5260FA2F6D6E9418EF03B86CDE58E66B91B7B87A3` |
| C4 | [tool-readme-C4.md](../../experimentacao/experimentacao-4/tool-readme-C4.md) | `D6BC0A588CD9A7DF7F1F566573944FA5CB1707BBA676B4E9854CAD2CC5440FC2` |

A fonte de C1 foi atualizada para `tool-readme-C1.md` por decisão do pesquisador, em substituição à referência anterior `tool-readme-C2.md` (SHA-256 `141C693DB506B2025D5EAD924C4C628660FEF7C163EC54BB7437C21FAA5C4856`). Não renomear nem alterar os documentos durante a geração. Os antigos arquivos `documentacao-Cx.md`, seus manifestos e os guias experimentais anteriores não definem as fontes deste reinício.

## 2. Procedimento padronizado

Em cada condição C0-C4, seguir esta ordem: **analisar a documentação → criar e congelar o oráculo → ler o SUT e criar os casos visando Branch Coverage → executar e registrar métricas**. Preparar o ambiente e registrar sua proveniência não autoriza consultar o código ou o comportamento do SUT antes do congelamento do oráculo. As etapas abaixo detalham esse fluxo.

### Etapa 1 — Preparação documental

- Identificar todos os arquivos entregues ao modelo, versão, origem e SHA-256.
- Preservar a documentação original e cópias C0-C4 sem edição.
- Para novas gerações, usar o [prompt atualizado](../prompts/geracao-de-oraculos-v2.md) e registrar sua versão e hash. Preservar o prompt anterior e os hashes históricos; não tratar a nova versão como se tivesse sido usada nos baselines. O hash atual do prompt anterior corresponde a C0-R2, C1 e C2, mas não ao hash registrado para C0-R1; não afirmar que ele reproduz o prompt dessa rodada. Diferenças entre versões devem ser consideradas na comparação dos resultados.
- Registrar a condição do experimento; não misturar arquivos de condições diferentes.
- Caracterizar C0 diretamente, sem atribuir nível alto/baixo de clareza ou consistência sem evidência.

### Etapa 2 — Preparação do ambiente

Registrar o commit do SUT; sistema operacional e arquitetura; Java, Maven, Z3 e ferramentas de cobertura com versões; dependências; máquina/recursos relevantes; harness e comando. Usar o mesmo SUT e ambiente em todas as condições sempre que possível.

Registrar também nome e versão do LLM, endpoint/plataforma se disponível, parâmetros, prompt, contexto fornecido, número de chamadas, repetições, datas e tokens/custo reportados. Ausências são `não informado`; não estimar.

### Etapa 3 — Oráculo documental com apoio de Z3

Antes de consultar o código, a LLM lê a documentação da condição e deriva dela o oráculo. A documentação é assumida como fielmente verdadeira para fins do experimento: uma divergência do SUT não autoriza corrigir o oráculo. Para cada expectativa, registrar a citação literal, a regra formalizada, entradas, saída esperada e a justificativa que liga o texto à formalização.

Formalizar as restrições derivadas do texto em SMT-LIB e usar um solver Z3 independente do SUT para verificar satisfatibilidade/viabilidade e obter entradas concretas e casos de fronteira quando aplicável. Registrar fórmula, versão do solver, resultado (`sat`, `unsat`, `unknown`), testemunhas e limites. `unknown`, timeout ou indisponibilidade do solver são falhas técnicas da formalização/geração, não evidência de ambiguidade documental. Não usar a saída do módulo `mcdc-z3` ou da CLI sob teste para decidir o resultado esperado: isso criaria circularidade. Z3 verifica a fórmula fornecida; não prova que a tradução da linguagem natural foi fiel nem substitui a documentação como fonte normativa.

Faça um inventário rastreável de requisitos, comportamentos, entradas, saídas, opções, formatos, fronteiras e erros explicitamente documentados. Planeje casos para maximizar a cobertura desse inventário e os resultados true/false das condições para os quais a documentação permita uma expectativa única. Use Z3 para procurar testemunhas e, quando viável, conjuntos menores de vetores que cubram o mesmo inventário; registre objetivo, restrições, critério de parada e resultado da busca. Não usar código, relatório de cobertura do SUT ou seus resultados para criar ou desempatar expectativas nesta etapa.

Se duas afirmações documentais conflitarem para a mesma situação, não escolher uma nem combiná-las silenciosamente. Registrar as alternativas e classificar o oráculo como `INDETERMINADO — CONFLITO DOCUMENTAL`, salvo se o próprio texto resolver o conflito. O mesmo vale para omissões ou ambiguidades que impeçam uma expectativa única. Se a documentação não especificar o resultado de um comportamento, registrá-lo como `INDETERMINADO — OMISSÃO`, sem escolher o resultado observado no SUT como expectativa. Não inventar regras para tornar a fórmula satisfatível.

Congele a análise, formalização e oráculos com hash antes de inspecionar o código.

### Etapa 4 — Inspeção do SUT e geração da suíte

Depois de congelar os oráculos, inspecionar o código e a CLI do repositório para mapear cada regra formalizada aos pontos de entrada e criar a suíte contra o sistema MC/DC real. Usar a implementação para entender como invocar o SUT e medir branches/condições; não a usar para corrigir, substituir ou desempatar expectativas documentais.

Depois de executar o baseline congelado, use o relatório de cobertura para localizar branches não exercitados e mapear cada um de volta ao inventário documental. Uma asserção semântica adicional só pode ser criada se a documentação determinar sua expectativa. Se o branch depender de comportamento não documentado, registrar um caso indeterminado com ID e motivo da lacuna; pode-se executá-lo como diagnóstico, sem inventar um oráculo ou julgar o resultado. Identificar cada extensão como nova rodada `coverage-informed`, preservar o baseline, congelar seus próprios casos e expectativas antes de executá-los e reportar os resultados por rodada. Cobertura observada pode orientar a escolha da entrada, nunca a semântica esperada.

Quando um oráculo documental determinado e conforme divergir do SUT, criar e manter a asserção correspondente para que ela falhe. Preservar o oráculo original e registrar a discrepância como não conformidade do SUT em relação à referência documental adotada, sem ajustar a expectativa ou excluir o teste para fazê-lo passar. Isso não prova, por si só, a intenção original ou qual fonte está objetivamente correta.

Cada caso gerado inclui, quando aplicável:

- ID estável e objetivo;
- referência documental literal;
- regra formalizada e evidência da correspondência com o texto;
- entrada concreta, pré-condições e dados de execução; registrar testemunhas/resultado Z3;
- resultado esperado e justificativa documental, ou estado `INDETERMINADO`;
- classificação do oráculo: `CONFORME À DOCUMENTAÇÃO`, `INCORRETO/SEM SUPORTE`, `INVÁLIDO` ou `INDETERMINADO`;
- módulos, branches e condições que se pretende exercitar;
- instruções para executar e artefato de evidência.

Para otimização, incluir também os requisitos/comportamentos documentados cobertos, branches/condições que se pretende exercitar após o mapeamento do SUT, redundâncias removidas e comportamentos documentados ainda sem teste. Declarar a meta como “melhor cobertura documentada alcançada”, não como cobertura máxima global, salvo se a busca exaustiva e seu universo forem demonstrados.

Qualquer expectativa dependente de regra não documentada é `INCORRETO/SEM SUPORTE` (subtipo `ASSUMIDO`), mesmo se a suposição estiver declarada; divulgá-la não a torna conforme. `INVÁLIDO` identifica saída/formalização/caso malformado que não pode ser avaliado como oráculo. `INDETERMINADO` identifica ambiguidade, omissão ou contradição documental sem resultado único. Congele prompt, resposta, formalizações, oráculos e suíte por hash antes da execução.

### Etapa 5 — Execução

Executar sem alterar o SUT, a documentação de requisitos ou os oráculos congelados. Para cada caso, registrar entrada, estado do oráculo, resultado esperado, resultado observado, status, mensagem de erro e evidência. Contabilizar testes gerados, executados, aprovados, falhos, indeterminados e inválidos, bem como erros técnicos, sem ocultar resultados para elevar aprovação. Casos indeterminados não recebem aprovação/reprovação semântica; podem ser executados apenas como observação diagnóstica, identificados separadamente.

Uma saída não explicitada ou sem expectativa determinada pela documentação não é, por si só, falha do SUT: registrar `INDETERMINADO — OMISSÃO` e `SEM JULGAMENTO`. Se um requisito documentado for contrariado, registrar a falha da asserção conforme como divergência. Identificar separadamente casos indeterminados descobertos durante a inspeção do SUT, sem modificar o baseline; manter uma unidade de contagem por caso/oráculo, evitando duplicar a mesma ocorrência.

Registrar separadamente a classificação do oráculo e o resultado de execução:

- `PASSOU`: a observação do SUT satisfez a asserção congelada;
- `FALHOU`: a observação do SUT não satisfez a asserção. Só classificar como `DIVERGÊNCIA DOCUMENTAÇÃO/SUT` quando o oráculo for conforme; se for incorreto/sem suporte, registrar que a falha veio de uma expectativa não conforme;
- `SEM JULGAMENTO`: oráculo indeterminado, sem aprovação/reprovação semântica;
- `NÃO EXECUTADO — INVÁLIDO`: caso/formalização malformado, sem execução ou avaliação válida;
- `ERRO DE EXECUÇÃO`: falha técnica ou de infraestrutura impediu concluir a execução.

Não confundir erro de geração, oráculo incorreto, divergência do SUT e indisponibilidade de infraestrutura. Uma falha do teste só é evidência de divergência documentação–SUT quando seu oráculo foi classificado como conforme à documentação.

### Etapa 6 — Cobertura, avaliação e consolidação

Executar a suíte com instrumentação sobre escopo congelado do SUT, coletar Branch Coverage e manter os relatórios brutos. Reportar cobertura da suíte total e, separadamente, do subconjunto com oráculos conformes, estruturalmente válidos e executáveis; não ocultar testes inválidos ou indeterminados das contagens. Avaliar conformidade documental segundo as classificações e regras da seção 4. Esses resultados medem fidelidade à documentação, não a verdade objetiva da documentação nem a correção geral do SUT.

Se a cobertura ficar aquém da meta, fazer uma nova rodada somente após relacionar branches não cobertos a comportamentos documentados. Preservar os resultados e hashes anteriores; não substituir, apagar ou reclassificar o baseline. Reportar separadamente ganhos da nova rodada, novos casos, branches sem suporte documental e alterações no tamanho/tempo da suíte. Não usar cobertura de código como justificativa para alterar expectativas já congeladas.

## 3. Métricas operacionais

Para qualquer taxa, se o denominador for zero, registrar as contagens e `não calculável (denominador zero)`; não substituir por 0% ou 100%. Se a instrumentação necessária não estiver disponível, registrar `não coletado` e a razão.

Branch Coverage é a única métrica de cobertura da pesquisa. Condition Coverage e Mutation Score não fazem parte das métricas desta pesquisa e não devem ser coletadas ou comparadas nas próximas rodadas. Contagens e taxas de execução, aprovação, falha, indeterminação e qualidade do oráculo continuam sendo registradas. Registros e executores históricos são preservados; campos legados que indiquem essas métricas como não coletadas não integram a avaliação atual. Novos executores não devem incluir esses campos.

### 3.1 Branch Coverage

`Branch Coverage = branches executados / total de branches × 100`.

É a proporção dos desvios de controle instrumentados que a suíte executou. Reportar os números absolutos, percentual, versão da ferramenta, módulos/classes incluídos e exclusões. Usar o mesmo commit e escopo C0-C4.

JaCoCo reporta cobertura de branches, mas seus relatórios históricos de regressão não representam cobertura das suítes LLM. A coleta atual deve ser feita com os testes gerados e o SUT instrumentado.

### 3.2 Taxa de executabilidade

`Taxa de executabilidade = testes executáveis / total de testes gerados × 100`.

Um caso conta como **estruturalmente válido** quando tem ID, entrada/pré-condição, instruções e resultado esperado ou status indeterminado em forma que o harness possa interpretar. Isso não valida a semântica do oráculo. Um caso conta como **executável** quando o harness aceita/invoca esse caso no ambiente predefinido. Registrar separadamente falhas de geração/formato, incompatibilidade técnica de biblioteca/runtime e bloqueio de infraestrutura; elas não são falhas funcionais do SUT.

### 3.3 Taxa de aprovação

`Taxa de aprovação bruta = asserções satisfeitas / asserções avaliadas com oráculo determinado × 100`.

Incluir oráculos `CONFORME À DOCUMENTAÇÃO` e `INCORRETO/SEM SUPORTE`, discriminando as taxas e contagens por classificação. Excluir casos `INVÁLIDOS`, `INDETERMINADOS` e erros técnicos que impeçam avaliar uma asserção, reportando-os separadamente. A taxa bruta mede apenas se o SUT satisfez as expectativas codificadas; não comprova conformidade documental. Um oráculo incorreto que passe continua incorreto.

### 3.4 Taxa de indeterminação

`Taxa de indeterminação = oráculos indeterminados / total de oráculos gerados × 100`.

Classificar todos os oráculos gerados, inclusive os casos malformados. Registrar motivo documental: omissão, ambiguidade ou conflito. Falha técnica de formalização/geração, timeout ou `unknown` do Z3 fica na contagem de erros técnicos, não na taxa de indeterminação documental.

Incluir cada caso registrado sem expectativa determinada, inclusive os identificados após a inspeção do SUT, no total de oráculos gerados e no numerador de indeterminação da respectiva rodada. Sua execução diagnóstica, quando ocorrer, também conta entre os testes executados e contribui para a Branch Coverage da suíte total; apresentá-la separadamente da cobertura do subconjunto conforme. Não incluí-lo como aprovação, falha semântica ou divergência documentação–SUT.

### 3.5 Conformidade documental e divergência do SUT

`Conformidade documental = oráculos CONFORME À DOCUMENTAÇÃO / (oráculos CONFORME À DOCUMENTAÇÃO + oráculos INCORRETOS/SEM SUPORTE) × 100`.

`Taxa de oráculos incorretos/sem suporte = oráculos INCORRETOS/SEM SUPORTE / total de oráculos gerados × 100`.

`Taxa de oráculos inválidos = oráculos INVÁLIDOS / total de oráculos gerados × 100`.

`Divergência documentação–SUT = casos com oráculo conforme que falharam por resultado divergente / casos com oráculo conforme executados com resultado conclusivo × 100`.

Oráculos `INVÁLIDOS` e `INDETERMINADOS` ficam fora do denominador de conformidade documental, mas suas quantidades e taxas sobre o total gerado devem ser reportadas separadamente. A divergência mede apenas a comparação entre expectativas documentais classificadas como conformes e o comportamento observado do SUT; não decide, por si só, qual fonte está correta.

### 3.6 Quantidades e custo

Por condição e repetição, registrar testes/oráculos gerados; estruturalmente válidos; executáveis; executados; asserções satisfeitas/não satisfeitas; conformes à documentação; incorretos/sem suporte; inválidos; indeterminados; divergências documentação–SUT; erros técnicos de formalização/Z3/geração; e erros de execução. Registrar tokens de entrada/saída ou total conforme reportado pela plataforma, duração de geração, chamadas, custos financeiros e quantidade de testes. Valores ausentes ficam `não informado`.

As contagens e custos são variáveis descritivas exigidas para interpretar as taxas, não um índice composto.

## 4. Análise qualitativa dos oráculos

Usar a documentação experimental congelada como referência normativa para avaliar se cada oráculo é fiel ao que foi especificado. Não presumir que a documentação seja uma verdade objetiva sobre o produto: as métricas medem conformidade documental. Não criar um gabarito comportamental alternativo, nem calcular Precision, Recall ou F1. Para cada caso, registrar uma única classificação primária:

- `CONFORME À DOCUMENTAÇÃO`: expectativa explicitamente declarada ou unicamente implicada pelo trecho citado, com formalização rastreável e sem conflito documental aplicável;
- `INCORRETO/SEM SUPORTE`: expectativa contradiz a documentação ou apresenta suposição/regra não implicada pelo texto como fato;
- `INVÁLIDO`: saída, formalização ou teste malformado que não permite avaliação válida; indisponibilidade/`unknown` do Z3, por si só, é erro técnico e não invalida a lógica;
- `INDETERMINADO`: ambiguidade, omissão ou contradição documental impede expectativa única.

Congele essa classificação antes da execução. Idealmente, um revisor que não gerou o oráculo classifica sua conformidade usando apenas documentação, formalização e caso congelados, sem ver código nem resultado do SUT; registrar divergências entre avaliadores e a forma de adjudicação. Se não houver revisor independente, identificar a autoavaliação da IA como limitação.

Registrar também subtipos (p.ex., contradição, entrada não suportada, limite, tradução Z3) e evidências. `sat` não valida a tradução; `unsat` não prova que a documentação está errada: verificar se o conjunto de afirmações documentais é conflitante ou se houve erro de formalização. Em caso de divergência do SUT, manter a expectativa documental conforme e registrar falha da asserção, sem corrigir o oráculo. A implementação é evidência do comportamento observado, não critério para reclassificar a documentação.

## 5. Comparação

- C0 × C1: documentação original versus tratamento de clareza/consistência elevadas;
- C1 × C2: redução pretendida da clareza com consistência elevada;
- C1 × C3: redução pretendida da consistência com clareza elevada;
- C2 × C4: redução pretendida da consistência sob baixa clareza;
- C3 × C4: redução pretendida da clareza sob baixa consistência.

C2 × C4 e C3 × C4, em conjunto com os efeitos simples nos níveis altos, permitem examinar interação dos fatores. C0 é natural e reportado separadamente; não atribuir níveis artificiais. Comparar apenas execuções com modelos, prompts, configuração, SUT, ambiente, harness e denominadores compatíveis. Se não forem controlados, descrever diferenças sem atribuição causal.

## 6. Ameaças à validade

| Ameaça | Efeito possível | Tratamento/registro |
|---|---|---|
| Modelo, versão ou configuração diferentes | Mudanças podem vir do modelo e não do documento | Registrar metadados; manter constantes quando possível |
| Prompts e contexto diferentes | O estímulo de geração pode confundir o efeito documental | Congelar estrutura do prompt e inventariar todo contexto |
| Variação entre chamadas | Uma execução pode não representar a condição | Registrar repetições; quantidade ainda requer decisão prévia |
| Ambiente, dependências ou recursos distintos | Pode afetar executabilidade e latência | Fixar ambiente e registrar falhas infra/técnicas |
| Ferramenta/escopo de cobertura | Diferenças no escopo podem comprometer comparações de branches | Congelar escopo, versão e exclusões |
| Oráculos inadequados ou não fundamentados | Teste pode passar sem refletir requisito ou falhar por expectation defeituosa | Auditoria qualitativa rastreável; não usar aprovação como verdade |
| Ambiguidade e contradições | Múltiplas interpretações plausíveis | Registrar alternativas e indeterminações sem escolher pelo código |
| Divergência documentação–implementação | Não é possível inferir automaticamente qual representa intenção | Preservar oráculo documental claro e registrar discrepância |
| Comparabilidade incompleta | Não permite atribuir diferenças aos fatores | Reportar condições e limitações; evitar causalidade |
| Documentação assumida normativa, mas possivelmente incorreta sobre o produto | Conformidade documental não equivale a verdade funcional do SUT | Reportar conformidade ao texto e divergência documentação–SUT como medidas distintas |
| Tradução de texto natural para Z3 | Erro de formalização pode parecer contradição ou gerar entrada inválida | Preservar citação, fórmula, testemunhas e revisão da correspondência texto–fórmula |
| Circularidade ao usar Z3 integrado ao SUT para definir o oráculo | Defeito no próprio SUT pode contaminar a expectativa | Usar solver independente e não consultar a saída esperada da CLI/módulo sob teste |
| C0 não é uma célula manipulada | Confunde comparações se rotulada alto/baixo | Descrever a documentação natural; analisá-la separadamente |

## 7. Decisões a registrar antes da coleta

1. Modelo, versão, parâmetros e número de repetições por condição.
2. Commit e versão do SUT, sistema operacional e recursos do ambiente.
3. Escopo de módulos/classes e branches para cobertura.
4. Harness e critério operacional de caso estruturalmente válido/executável.
5. Fonte e unidade dos dados de tokens, tempo e custos, caso a plataforma não os reporte.
6. Versão do Z3 independente e procedimento/revisor para conferir a correspondência entre trechos documentais e fórmulas SMT.

Essas decisões permanecem pendentes; não foram preenchidas por suposição nesta revisão.
