# Relatório de experimentação e avaliação: Claude nas condições C0–C4

Este relatório consolida as cinco execuções da pesquisa feitas pelo Claude (`claude-resultados/C0` a `C4`), compara os resultados e registra detalhes do processo que os relatórios individuais não mostram juntos. Foi escrito **depois** que as cinco condições terminaram. Para isso, li as cinco fontes documentais, o protocolo, os relatórios de cada condição e os dados brutos.

Os números das seções 3 e 4 foram recalculados a partir de `jacoco.csv` e `resultados.json` de cada rodada, não copiados dos READMEs. `copilot-resultados/` não foi lido: não há comparação com o Copilot.

## 1. Objetivo e protocolo

A pesquisa mede como a **qualidade da documentação** afeta oráculos e suítes de teste gerados por LLM para a ferramenta Java MC/DC deste repositório. Em cada condição, a documentação é a verdade absoluta, e o sistema é o objeto avaliado.

O protocolo comum ([metodologia.md](../experimentacao-pesquisa/protocolo/metodologia.md)) e o [prompt v3](../experimentacao-pesquisa/prompts/geracao-de-oraculos-v3.md) exigem:
- conferir o hash da fonte;
- montar um oráculo só a partir do texto, com casos INDETERMINADOS para omissões, ambiguidades e conflitos;
- usar o Z3 independente;
- congelar por SHA-256 antes de ler o SUT;
- criar uma suíte nova, também congelada antes da execução;
- reportar quatro métricas: Branch Coverage, aprovados, falhos e indeterminados.

## 2. As cinco documentações

| Condição | Clareza / consistência pretendidas | Fonte (SHA-256, prefixo) | Linhas / palavras | Natureza da alteração |
|---|---|---|---|---|
| C0 | original, sem nível atribuído | `72B827BD…` | 404 / 4281 | README original da ferramenta |
| C1 | alta / alta | `91981FA0…` | 602 / 4739 | Reescrita mais explícita: define entrada × condição, detalha os códigos de saída e explica as consequências do build sem Z3. Atenua uma afirmação ("a suíte **pode ter** N + 1 testes") |
| C2 | baixa / alta | `61C4062B…` | 602 / 3920 | Mesmo conteúdo do C1 com letras e palavras curtas apagadas, sobretudo na prosa ("pares  independência:   condição,  procurds dois tests…"). Tabelas, números e opções ficaram quase legíveis |
| C3 | alta / baixa | `F18B0821…` | 634 / 5365 | Texto claro com parágrafos contraditórios inseridos, vários declarando "substituir" a regra anterior. Exemplos: códigos de saída, sat × unsat, critério do par, gulosa × exata, csv × truth-csv |
| C4 | baixa / baixa | `D6BC0A58…` | 422 / 2861 | Texto curto, começa no meio de uma tabela, com palavras apagadas (inclusive o operando `A` dos exemplos), `[trecho omitido]` e as mesmas famílias de contradição do C3 |

Os níveis são **pretendidos**: nada aqui presume que foram atingidos.

### Achado sobre o material: o catálogo de contradições do C3 não corresponde à fonte

`experimentacao-pesquisa/experimentacao-3/contradictions.csv` lista 14 itens (6 contradições explícitas, 3 contextuais, 1 ambiguidade e 4 "regras aparentemente compatíveis"). Conferi frases características de cada item na fonte congelada `tool-readme-C3.md` e **nenhuma aparece**: "solucionador", "evidência", "simultaneamente", "4096", "inclusive no modo direto", "Sobreposições compatíveis", "sem operadores relacionais", "relatórios são gerados", "Condição não coberta retorna", "mutuamente exclusiv" retornam 0 ocorrências.

Os conflitos que estão de fato na fonte são os que a execução C3 catalogou de forma independente (K1–K15, em [C3/experimento/analise.md](C3/experimento/analise.md)). Alguns tocam os mesmos temas do catálogo (Z3 obrigatório, códigos de saída, modo direto), mas com outros enunciados.

**Consequência:** o catálogo não serve como gabarito para medir quantas contradições "plantadas" o modelo detectou. Pela aparência, descreve outra versão da fonte. A execução C3 não leu o catálogo (seu relatório registra que não abriu outras pastas além da fonte). Recomendo que o pesquisador confira qual versão do C3 o catálogo descreve.

## 3. Resultados

### 3.1 Métricas finais por condição (cobertura só com determinados)

| Condição | Rodadas de cobertura | Branch Coverage | Aprovados | Falhos | Indeterminados | Casos | % indet. |
|---|---|---|---|---|---|---|---|
| C0 | rodada 3 + extensão 1, só determinados | 1077 / 1296 = **83,10%** | 92 | 1 | 14 | 107 | 13,1% |
| C1 | rodadas 04 + 05, só determinados | 1107 / 1296 = **85,42%** | 97 | 1 | 12 | 110 | 10,9% |
| C2 | r3 + r4, só determinados | 1091 / 1296 = **84,18%** | 87 | 0 | 15 | 102 | 14,7% |
| C3 | r4, só determinados | 859 / 1296 = **66,28%** | 40 | 0 | 39 | 79 | 49,4% |
| C4 | r1-baseline, só determinados | 500 / 1296 = **38,58%** | 44 | 1 | 37 | 82 | 45,1% |

Nas cinco condições, a cobertura agora segue a mesma regra (seção 3.2). As rodadas só com determinados de C0 e C1 foram executadas depois da primeira versão deste relatório, a pedido do pesquisador, com o mesmo runner, as mesmas entradas e o mesmo build congelados. Os vereditos foram idênticos caso a caso.

Pontos comuns às cinco execuções:
- **Denominador:** as 69 classes que o JaCoCo 0.8.16 analisa nos quatro módulos de produção, com 1296 desvios. É o mesmo total que o README original declara.
- **Unidade de contagem:** um caso do oráculo, com ID estável.
- **SUT:** o mesmo código em todas as condições. C0 usou o commit `03589c4`, C1 `92d9df8` e C2–C4 `ed7d2e0`, e o `git diff` entre eles nos quatro módulos é vazio.

### 3.2 A cobertura não é homogênea: duas regras diferentes

Durante a execução do C3, o pesquisador definiu que **um caso indeterminado não é teste**: ele não é executado e não entra na cobertura. A regra passou ao C4. C0, C1 e C2 terminaram antes e executaram os indeterminados como diagnóstico, como o protocolo original permite. Depois, os três receberam rodadas novas só com os determinados, e as originais foram preservadas.

| Condição | Com indeterminados executados (histórico) | Só determinados (oficial) | Desvios que só os diagnósticos alcançavam |
|---|---|---|---|
| C0 | 84,65% (1097) | 83,10% (1077) | 20 |
| C1 | 86,19% (1117) | 85,42% (1107) | 10 |
| C2 | 84,80% (1099) | 84,18% (1091) | 8 |
| C3 | 81,48% (1056, r3) | 66,28% (859, r4) | 197 |
| C4 | — (não executados) | 38,58% (500) | — |

Com a regra unificada, as cinco coberturas são comparáveis. O efeito da regra depende da condição. Onde os indeterminados são poucos (C0–C2), eles alcançavam de 8 a 20 desvios. No C3, onde são quase metade, alcançavam 197: lá, os diagnósticos sustentavam boa parte da cobertura.

**Observação:** o `relatorio-comparativo-C0-C4.md`, escrito pela sessão do C4, é anterior às rodadas só com determinados de C0, C1 e C2. Ele usa as coberturas antigas dessas três condições e diz que a medição não existe.

### 3.3 Cobertura por módulo (só determinados)

| Módulo (desvios) | C0 | C1 | C2 | C3 | C4 |
|---|---|---|---|---|---|
| `mcdc-core` (411) | 345 | 370 | 345 | 327 | 277 |
| `mcdc-requirements` (162) | 132 | 140 | 127 | 123 | 114 |
| `mcdc-z3` (386) | 311 | 312 | 321 | 204 | **0** |
| `mcdc-cli` (337) | 289 | 285 | 298 | 205 | 109 |
| **Total (1296)** | **1077** | **1107** | **1091** | **859** | **500** |

O módulo `mcdc-z3` é o termômetro da consistência. No C3 e no C4, as contradições atingiram justamente as regras do Z3 (sat × unsat, impossíveis, `--exact`, `--direct`). Sem expectativa, esse código ficou sem teste julgado. No C4, nenhum caso usa o Z3.

### 3.4 Baseline e fases

| Condição | Baseline | Correções | Extensões |
|---|---|---|---|
| C0 | 85 casos; r1 80,02% (69 / 3 inválidos / 13); r2 80,25% (72 / 0 / 13) | entradas JSON malformadas (C07–C09) | 22 casos: 20 / 1 / 1 |
| C1 | 79 casos; 80,40% (70 / 0 / 9 após a correção) | decodificação do stdout no harness (AN-22) | 31 casos: 27 / 1 / 3 |
| C2 | 90 casos; 83,02% (75 / 0 / 15) | nenhuma | 12 casos: 12 / 0 / 0 |
| C3 | 75 casos; r1 78,40% (34 / 2 / 39 brutos; T20–T22 depois inválidos) | IDs de decisão nos CSVs (T20–T22); remoção dos diagnósticos I40–I47; suíte refeita (r3) | r2 (18 casos: 6 corrigidos, E01–E04 e 8 diagnósticos I40–I47, depois removidos): 8 / 0 / 10 |
| C4 | 82 casos; 38,58% (44 / 1 / 37) | nenhuma | nenhuma |

## 4. Divergências encontradas (FALHOU)

| Condição | Caso | Texto da fonte | Observado |
|---|---|---|---|
| C0 | C0-X13 | "InputEdgeCasesTest: … número da linha com erro" | CSV de testes com `X` na linha 4: código 1 com `Erro: T1: valor lógico inválido: X` (cita o teste, não a linha) |
| C1 | EX-27 | Opções que exigem o Z3 avisam quando ele falta; `verify` "usa o Z3" | `verify` com uma única decisão e sem Z3 no PATH: código 0, sem aviso |
| C4 | C4-D26 | "InputEdgeCasesTest: … núemro linha  erro" (degradado) | `.mcdc` com erro na linha 3: `Erro: REQ-B: Faltou fechar parêntese` (cita o requisito, não a linha) |

Leitura conjunta:
- **As três divergências estão na periferia** (mensagens de erro e avisos), nunca no motor MC/DC. Todos os números da tabela de regressão (VM, TIS, NPP), suítes mínimas, pares, diagnósticos, impossíveis, fronteiras e valores concretos que chegaram a ser afirmados passaram em todas as condições.
- **A divergência do "número da linha"** apareceu duas vezes, em execuções independentes, a partir de textos diferentes: no C0 para o CSV e no C4 para o `.mcdc`. A frase vem da descrição de um teste interno e não diz a que entrada se aplica. É uma divergência real em relação à documentação adotada, mas a expectativa depende de leitura.
- **EX-27 (C1)** mostra que o aviso de Z3 ausente aparece só quando o Z3 é de fato chamado. Com uma única decisão, o `verify` não tem pares para consultar. No C0, o caso equivalente (C0-D05, duas decisões) recebeu o aviso. É um exemplo de como a escolha da entrada decide se uma afirmação genérica do texto é confirmada ou refutada.
- **C2 e C3 não tiveram falhas.** Isso não indica documentação adequada: com a parte verificável reduzida, as asserções mais finas (mensagens, avisos) foram as primeiras a virar indeterminadas.

## 5. Comparação e avaliação

1. **A consistência pesou mais que a clareza.** A proporção de indeterminados passa de 11–15% (C0, C1, C2) para 45–49% (C3, C4). Na cobertura só de determinados, agora comparável nas cinco, as condições de consistência alta ficam juntas (C0 83,10%, C2 84,18%, C1 85,42%), e as de consistência baixa caem para 66,28% (C3) e 38,58% (C4). A clareza baixa sozinha (C2) não se separou das documentações claras.
2. **Clareza baixa transfere o custo para a interpretação.** No C2, tabelas, números e opções sobreviveram, e o que se perdeu foi prosa. O relatório do C2 registra que parte das expectativas dependeu de reconstruir palavras apagadas a partir de outros trechos. Outro leitor pode reconstruir de outro jeito, e o conhecimento prévio de MC/DC do modelo pode ter ajudado, sem que isso possa ser demonstrado.
3. **Consistência baixa tira poder de detecção, não gera falhas.** Com contradições, o oráculo só afirma o que vale em todas as leituras. C3 e C4 adotaram a mesma política: verificar no Z3 se as leituras de um conflito levam ao mesmo resultado; se sim, o caso fica determinado; se não, indeterminado. Nenhum dos dois achou falhas no núcleo, porque o núcleo ficou sem expectativa. O C3 registra que uma política que escolhesse a regra "prevalente" geraria mais expectativas e, possivelmente, falhas.
4. **No C4, as duas degradações se somam.** A baixa clareza apagou os exemplos que dariam expectativas numéricas ("4 testes", "5 em vez de 6"), porque o operando `A` sumiu. A baixa consistência tornou indeterminado todo o comportamento do Z3. O Z3 independente mostrou ainda que a regra "prevalente" (`sat` = impossível) contradiz os números medidos da própria fonte: a leitura original reproduz 4/4/1 impossíveis, e a invertida dá 148/264/75.
5. **Documentação forte gera asserções finas.** C0 e C1 produziram expectativas sobre mensagens, avisos, formatos e números. As falhas apareceram justamente aí. A clareza aumenta o poder de detecção, não só a cobertura.
6. **C0, C1 e C2 ficaram próximos.** As diferenças de cobertura (83,10%, 85,42%, 84,18%) são menores que a variação esperada entre execuções e entre procedimentos. A principal mudança do texto C1 (N+1 como possibilidade) eliminou expectativas numéricas que o C0 tinha. Com uma execução por condição, não dá para atribuir a diferença à documentação.

## 6. Detalhes da experimentação com o Claude

### 6.1 Configuração e organização das sessões

- **Modelo e ferramentas:** Claude Opus 5.5 (`claude-opus-5-5`) no Claude Code (app desktop, Windows 11). Temperatura e demais parâmetros: não informado. Ferramentas: Java 21.0.3, Python 3.13.5, Z3 5.4.1 (`z3.exe` do pacote `z3-solver`), JaCoCo 0.8.16 e Jackson 2.17.2.
- **Sessões:** o C0 rodou na sessão principal. O C1 foi tentado ali, descartado e refeito numa sessão nova. Cada sessão seguinte foi iniciada pela anterior: C1 → C2 → C3 → C4.
- **Instruções em cadeia:** cada sessão recebeu um texto de instruções escrito pela sessão que a iniciou, com as regras de isolamento e notas de ambiente. A sessão que escrevia já conhecia os próprios resultados. As instruções que pude conferir (a do C1) não trazem resultados, mas não dá para demonstrar que nenhuma informação vazou pela redação.
- **Build:** o Maven offline não resolve plugins nesta máquina. Todas as condições compilaram o SUT com `javac --release 21` a partir de `git archive`, fora das fontes.
- **Ordem no dia 2026-11-24:** C0 (oráculo congelado às 09:42), C1 isolado (10:29), C2 (11:07), C3 (11:38) e C4 (12:24). A rodada retroativa só com determinados do C2 é da tarde, depois do C4. Os horários vêm dos manifestos e dos arquivos. Não registrei a duração de cada condição: não informado.

### 6.2 A tentativa de C1 que foi descartada

A primeira execução do C1 aconteceu na mesma sessão do C0. O executor já conhecia o SUT, as saídas e os resultados do C0. O oráculo foi reescrito do texto C1, mas a **escolha das situações** herdou o C0, inclusive os casos que no C0 vieram da extensão guiada por cobertura. O resultado ficou quase idêntico ao acumulado do C0: 84,65% → 84,72% e a mesma falha do "número da linha".

O pesquisador mandou apagar essa tentativa e refazer o C1 isolado. A versão isolada chegou a outro conjunto de casos (79 + 31), a outra falha (EX-27, em vez do número da linha, que nem foi testado) e a 86,19%.

**Lição:** a contaminação não aparece nas expectativas, que eram textuais, e sim na **seleção do que testar**, e a seleção domina a cobertura. O isolamento por sessão é necessário para comparar condições.

### 6.3 Correções depois de ver resultados

Três das cinco execuções invalidaram casos depois de observar falhas brutas:

| Condição | O que falhou | Causa declarada | Como foi tratado |
|---|---|---|---|
| C0 | C07–C09 | o heredoc do shell perdeu uma barra em `/\\` e o JSON ficou inválido | entradas corrigidas sem mudar expectativas; rodada 2 completa |
| C1 | AN-22 | o runner decodificava em UTF-8 o stdout que a JVM gravava em Cp1252 | runner corrigido e congelado; rodada 02 completa |
| C3 | T20, T22 (T21 passou só por vacuidade) | os CSVs usavam `decision = D`, mas a CLI chama de `REQ` a decisão de uma expressão direta, que a fonte não nomeia | marcados como inválidos; versões corrigidas (via `.mcdc`) na r2/r3 |

As três correções são plausíveis e documentadas, e os resultados brutos foram preservados. Mesmo assim, **as três foram decididas depois de ver a falha**, que é exatamente a situação em que o protocolo pede cautela. No C3, a correção exigiu um conhecimento do SUT (o ID `REQ`) obtido depois do congelamento. Um revisor independente deveria confirmar que cada uma é um defeito do harness e não um ajuste para fazer o caso passar.

O C3 também removeu depois os diagnósticos I40–I47, criados na extensão "só para alcançar código", e refez a suíte (r3). A decisão é coerente com a regra do pesquisador, mas mudou a métrica final.

### 6.4 Desvios de protocolo e de regra

- **Regra dos indeterminados (seção 3.2):** foi definida durante o experimento. C0, C1 e C2 só foram alinhados a ela depois, com rodadas novas. O protocolo publicado permite executar indeterminados "como diagnóstico" e não os exclui da instrumentação. A regra nova não está no `metodologia.md`.
- **Unidade de execução:** C0, C1 e C2 rodam uma invocação por caso. C3 e C4 julgam vários casos sobre a mesma execução. A contagem de testes por ID é comparável, mas o número de execuções não.
- **Observação das saídas:** os formatos JSON e CSV não são documentados em nenhuma fonte. Todas as execuções leram o código depois do congelamento para escrever os adaptadores (por exemplo, `INFEASIBLE` = bloqueada, `minimalSuite` = suíte). As expectativas não mudaram, mas a escolha dos campos é do executor.

### 6.5 Atritos técnicos recorrentes

- **Quebras de linha:** com `core.autocrlf=true`, o checkout converteu os arquivos do C0 para CRLF, e os manifestos `CONGELAMENTO-*.sha256` deixaram de conferir neste checkout. O conteúdo não mudou. Um `.gitattributes` com `claude-resultados/** -text` evitaria isso. Ainda não foi aplicado.
- **Codificação:** a saída do SUT chega em Cp1252, com acentos corrompidos. Isso causou o erro técnico do C1, e as outras execuções evitaram asserções com acentos.
- **Git Bash (MSYS):** a conversão automática de caminhos quebrou classpaths e argfiles do `javac` até usar `MSYS_NO_PATHCONV=1` e caminhos Windows.
- **Z3:** uma consulta de minimalidade com 13 slots deu *timeout* no C0 e foi trocada por lemas. No C2, uma consulta de fronteira tinha erro de ordem e foi corrigida antes do congelamento.

### 6.6 Como o Claude tratou a documentação

- **INDETERMINADO foi aplicado de forma conservadora.** Quando o texto atenuava uma afirmação ("pode ter N + 1"), o caso perdia a expectativa numérica. Quando o texto não definia um conceito usado (o critério de causa única), as execuções usaram a definição das referências citadas e registraram isso como interpretação.
- **O Z3 serviu para mais que verificar.** Além de confirmar mínimos e impossíveis, foi usado para decidir se um conflito importa (C3, C4) e para mostrar que uma regra declarada prevalente contradiz os próprios números da fonte (C4).
- **As leituras interpretativas foram registradas por caso.** Exemplos: código 1 para formato não aceito, restrição manual como "combinação impossível", "limite" de `<=` como vizinhos inteiros.

## 7. Ameaças à validade

- **Uma execução por condição**, com um único modelo. Não há medida de variação, e diferenças de poucos pontos não devem ser interpretadas.
- **Autorrevisão em todas as condições.** A tradução texto → fórmula não teve revisor independente, e `sat`/`unsat` não provam fidelidade.
- **Procedimentos heterogêneos:** número de extensões, correções, regra de cobertura, unidade de execução e políticas de interpretação variaram. Parte das diferenças pode vir do procedimento, não da documentação.
- **Isolamento:** nenhuma execução pode demonstrar ausência de conhecimento prévio do modelo sobre MC/DC. Houve perdas pontuais, registradas em cada relatório: nome de pasta no `git status`, arquivos de entrada exibidos e o defeito de entrada do C0 notado pela mensagem do SUT.
- **Material de referência:** o catálogo de contradições do C3 não corresponde à fonte (seção 2).
- **Sem inferência causal:** as relações da seção 5 descrevem esta amostra, como o protocolo pede.

## 8. Recomendações para a continuidade

1. **Registrar a regra de cobertura no `metodologia.md`.** As cinco condições já foram medidas só com determinados.
2. **Repetir cada condição** (pelo menos 3 sessões isoladas por condição) para estimar a variação antes de comparar médias.
3. **Fixar a unidade de execução e a política de conflitos** no protocolo, para que a diferença entre condições venha da documentação.
4. **Revisão independente** das correções pós-execução (C0, C1, C3) e das traduções para SMT-LIB.
5. **Conferir o `contradictions.csv`** contra a fonte C3 e, se for o caso, regenerar o catálogo a partir da versão congelada.
6. **Adicionar o `.gitattributes`** (`claude-resultados/** -text`) para preservar os bytes congelados.

## 9. Estado dos artefatos

| Condição | Pasta | Relatório | Commit |
|---|---|---|---|
| C0 | [C0/](C0/README.md) | [relatorio.md](C0/avaliacao/relatorio.md) | `92d9df8` (no `main` e no `origin`); rodadas só com determinados sem commit |
| C1 | [C1/](C1/README.md) | [relatorio.md](C1/avaliacao/relatorio.md) | `ed7d2e0` (no `main` e no `origin`); rodadas só com determinados sem commit |
| C2 | [C2/](C2/README.md) | [relatorio.md](C2/avaliacao/relatorio.md) | sem commit |
| C3 | [C3/](C3/README.md) | [relatorio.md](C3/avaliacao/relatorio.md) | sem commit |
| C4 | [C4/](C4/README.md) | [relatorio.md](C4/avaliacao/relatorio.md) | sem commit |

Também sem commit: [relatorio-comparativo-C0-C4.md](relatorio-comparativo-C0-C4.md), escrito pela sessão do C4 antes da rodada retroativa do C2, e este relatório.
