# Relatório de experimentação e avaliação: Claude Sonnet 5.5 nas condições C0–C4

Este relatório consolida as cinco execuções feitas pelo Claude Sonnet 5.5 (`claude-sonnet-5.5-resultados/C0` a `C4`), compara os resultados e registra detalhes do processo. Foi escrito **depois** que as cinco condições terminaram. Para isso li os relatórios de avaliação de C0 a C3 (`avaliacao/relatorio.md`) e os CSV do JaCoCo. As execuções individuais não leram umas às outras (cada relatório registra seu isolamento); esta leitura conjunta é posterior e a pedido do pesquisador. As pastas do Opus e do GPT **não foram lidas** para os números e conclusões, e por isso não há comparação com outras LLMs aqui.

Os números das seções 3 e 4 vêm dos relatórios individuais e do `jacoco.csv` de cada acumulado (cobertura por pacote recalculada do CSV).

## 1. Objetivo e protocolo

A pesquisa mede como a qualidade da documentação afeta oráculos e suítes de teste gerados por LLM para a ferramenta Java MC/DC deste repositório. Em cada condição, a documentação é a verdade absoluta e o sistema é o objeto avaliado. O protocolo ([metodologia.md](../experimentacao-pesquisa/protocolo/metodologia.md)) e o [prompt v3](../experimentacao-pesquisa/prompts/geracao-de-oraculos-v3.md) exigem: hash da fonte conferido antes da leitura; oráculo derivado só do texto, com casos INDETERMINADOS para omissão, ambiguidade e conflito; Z3 independente; congelamento por SHA-256 antes de ler o SUT e antes de executar a suíte; quatro métricas (Branch Coverage, aprovados, falhos, indeterminados).

Regra do pesquisador aplicada em todas as execuções: casos indeterminados são registrados, **não executados** e não entram na cobertura. Em C3 e C4 foi acrescentado o **critério estrito** (documentação como verdade, sistema só como entrada para criar a suíte, sem suposições, sem receio de indeterminar).

## 2. As cinco documentações

| Condição | Pretendido (clareza / consistência) | Fonte (SHA-256, prefixo) | Observações vistas nas execuções |
|---|---|---|---|
| C0 | original, sem nível atribuído | `72B827BD…` | texto completo; 94 casos registrados |
| C1 | alta / alta | `91981FA0…` | afirmações atenuadas ("a suíte pode ter N + 1 testes"); 72 casos |
| C2 | baixa / alta | `61C4062B…` | letras e palavras curtas apagadas, expressões corrompidas; tabelas e números legíveis; 68 casos |
| C3 | alta / baixa | `F18B0821…` | texto claro com contradições internas (contagem de condições, Z3 obrigatório×opcional, códigos de saída, `unsat`/`sat`, critério de par, `csv`/`truth-csv`, redundante×bloqueada, limites, minimização, parênteses, arquitetura do Z3, regras de build); 72 casos |
| C4 | baixa / baixa | `D6BC0A58…` | começa no meio de uma tabela, palavras e identificadores apagados, `[trecho omitido]`, mesmas famílias de contradição do C3; 78 casos |

Os níveis são **pretendidos**: nada aqui presume que foram atingidos.

## 3. Resultados

### 3.1 Métricas finais por condição

| Condição | Branch Coverage | Aprovados | Falhos | Indeterminados | Casos | % determinados |
|---|---|---|---|---|---|---|
| C0 | 1001 / 1296 = **77,24 %** | 71 | 1 | 22 | 94 | 76,6 % |
| C1 (acumulado) | 982 / 1296 = **75,77 %** | 57 | 0 | 15 | 72 | 79,2 % |
| C2 (acumulado) | 1010 / 1296 = **77,93 %** | 58 | 0 | 18 | 76 | — (50 de 68 no baseline: 73,5 %) |
| C3 | 835 / 1296 = **64,43 %** | 40 | 0 | 32 | 72 | 55,6 % |
| C4 | 626 / 1296 = **48,30 %** | 42 | 0 | 36 | 78 | 53,8 % |

Pontos comuns: JaCoCo 0.8.16; denominador de 1296 branches nas 69 classes de produção dos quatro módulos (inclusive não carregadas e de mutação); sem harness nem bibliotecas externas; sem análise de mutação; unidade = um caso do oráculo = um teste; Z3 5.4.1 independente do `mcdc-z3`; revisão do oráculo sempre autorrevisão.

### 3.2 Baseline e extensões

| Condição | Baseline | Extensões | Observação |
|---|---|---|---|
| C0 | 71 / 1 / 22; 77,24 % | não houve | falha C0-038 (ver seção 4) |
| C1 | 56 / 0 / 15; 75,77 % | E1: 1 caso | C1-D02 era inválido no baseline (faltou `--format json`); passou em E1; cobertura não mudou |
| C2 | 49 / 1 / 18; 75,23 % | ext1, ext2, ext3 | +8 casos novos; acumulado 77,93 % (+2,70 pontos); C2-020 foi defeito da suíte |
| C3 | 40 / 0 / 32; 64,43 % | não houve | refeito sob critério estrito; tentativa 1 preservada em `C3/tentativa-1/` (47 / 1 / 24; 70,52 %) |
| C4 | 42 / 0 / 36; 48,30 % | não houve | baseline = acumulado |

### 3.3 Cobertura por pacote (branches cobertos; total entre parênteses)

| Pacote (total) | C0 | C1 | C2 | C3 | C4 |
|---|---|---|---|---|---|
| `core` (287) | 238 | 247 | 250 | 249 | 119 |
| `core.model` (60) | 28 | 20 | 23 | 23 | 20 |
| `core.mutation` (64) | 50 | 57 | 57 | 57 | 57 |
| `requirements` (162) | 126 | 122 | 121 | 119 | 79 |
| `z3` (386) | 289 | 278 | 288 | 219 | 226 |
| `cli` (337) | 270 | 258 | 271 | 168 | 125 |
| **Total (1296)** | **1001** | **982** | **1010** | **835** | **626** |

C1 usa o baseline (a extensão não alterou os branches). Leitura: a perda de C0–C2 para C3 está sobretudo em `z3` (−69 a −59) e `cli` (−103 a −90). Em C4 a perda adicional está em `core` (119 de 287), `requirements` (79 de 162) e `cli`; `z3` ficou próximo de C3 porque o caso D34 e os de modo direto/Z3 ainda exercitaram o módulo.

## 4. Divergências (FALHOU) e defeitos de suíte

| Condição | Caso | O que ocorreu |
|---|---|---|
| C0 | C0-038 | Com `-o arquivo`, a expectativa era saída padrão vazia; observado: `Relatório gravado em <arquivo>` na saída padrão. O relatório da C0 reconhece que a expectativa foi mais estrita que o texto e mantém o FALHOU porque o protocolo proíbe ajustar expectativas |
| C2 | C2-020 | Defeito **da suíte** (supôs que o texto lista as 2^20 linhas; a ferramenta imprime só `Tabela verdade: 1048576 linhas`). FALHOU do baseline preservado; passou na extensão |
| C1 | C1-D02 | Inválido por defeito da suíte (faltou `--format json`); não contado como falha; passou em E1 |
| C3 (tentativa 1) | 1 falha | REQ-003 com uma condição redundante divergiu; na refeita, esse caso foi rebaixado a INDETERMINADO por ambiguidade documental (ver seção 6.3) |

Leitura conjunta: as únicas divergências semânticas ficam na periferia (mensagens e destino de saída), não no motor MC/DC. Em C0 a C4, os números da tabela de regressão (VM, TIS, NPP) e os tamanhos de suíte afirmados no texto passaram sempre que foram testados.

## 5. Comparação e avaliação

1. **A cobertura acompanha a fração de casos determinados**, e não a quantidade de falhas: 76,6 % → 79,2 % → 73,5 % → 55,6 % → 53,8 % de determinados, com 77,24 % → 75,77 % → 77,93 % → 64,43 % → 48,30 % de cobertura.
2. **C0, C1 e C2 ficaram próximos** (75,2 % a 77,9 %). A diferença entre elas é menor que a variação provável entre execuções, e a C2 só ultrapassa a C0 depois de três extensões. Com uma execução por condição, não dá para atribuir essa diferença à documentação.
3. **A queda forte vem de C3 e C4**, onde os conflitos internos e a corrupção geraram 32 e 36 indeterminados. As áreas mais afetadas são as que o texto contradiz: Z3 (`sat`/`unsat`, impossíveis, arquitetura), formatos `csv`/`truth-csv`, redundante×bloqueada, códigos de saída.
4. **Zero falhas em C3 e C4 não indica documentação adequada.** O próprio relatório da C3 registra que o 0 é condicionado ao rigor do oráculo: o caso que divergiu na tentativa 1 virou indeterminado. Com o núcleo sem expectativa, não há onde falhar.
5. **No C4, as duas degradações se somam.** A baixa clareza apagou os identificadores dos exemplos (por exemplo `( and B) or C`), então nem os "4 testes" e "3 testes" puderam ser usados. A baixa consistência tornou indeterminado o que depende do Z3. O que restou foi a tabela de regressão, propriedades de relatório e estrutura do repositório; esta última (D35–D42) não passa pela CLI e não soma cobertura.
6. **Z3 serviu para decidir conflitos.** Em C3 e C4, cada conflito foi formalizado (cada afirmação `sat` sozinha, conjunção `unsat`), o que sustenta a escolha de indeterminar em vez de eleger uma leitura.

## 6. Detalhes da experimentação

### 6.1 Configuração

- **Modelo:** Claude Sonnet 5.5 (`claude-sonnet-5-5`) no Claude Code (app desktop, Windows 11). Temperatura e demais parâmetros: não informado.
- **Ferramentas:** Java 21.0.3, Python 3.13.5, pytest 9, Z3 5.4.1 (`z3.exe`), JaCoCo 0.8.16. Sem Maven e sem recompilar: a CLI foi chamada por `java -cp "<mcdc-cli/target/classes>;<classpath.txt>" io.github.rvdomingos.mcdc.cli.Main`.
- **Sessões:** C0 e C1 em sessões próprias; C2 foi iniciada pela C1; C3 e C4 seguiram. Cada uma recebeu instruções de outra sessão (que já conhecia resultados anteriores). Não é possível demonstrar que nada vazou pela redação.
- **Commits dos resultados:** C0 `0ddda45`, C1 `119c65d`, C2 `beb98bf`, C0 e C1 reorganizadas em `e6d607a`, C2 reorganizada em `1d7822e`, C3 `3e7be21` (tentativa 1) e `3275a0d` (refeita) com cópia da fonte em `7831185`, C4 `798dae5` e `400b594`. Commit do SUT na partida variou por condição (por exemplo `0ddda45` em C1, `119c65d` em C2, `50e795e` em C3, `7831185` em C4).
- **Duração:** baseline em torno de 1 a 2 minutos por condição (C1 ≈ 134 s, C2 ≈ 115 s, C3 ≈ 86 s, C4 ≈ 49 s de pytest); duração total de cada sessão: não informado.

### 6.2 Tentativas e refeitas

- **C3 foi feita duas vezes.** A tentativa 1 (47 / 1 / 24; 70,52 %) foi preservada. O pesquisador determinou o critério estrito e a C3 foi refeita (40 / 0 / 32; 64,43 %): oito casos foram rebaixados a INDETERMINADO e expectativas determinadas foram enxugadas.
- **A segunda execução da C3 perdeu isolamento:** o autor já conhecia a saída do SUT e a tentativa 1. O relatório da C3 declara isso.
- **C4 já nasceu sob o critério estrito**, sem tentativa anterior.

### 6.3 Correções depois de ver resultados

| Condição | O que aconteceu | Tratamento |
|---|---|---|
| C1 | C1-D02 sem `--format json` | extensão E1 congelada antes de executar; baseline preservado |
| C2 | C2-020 supôs saída que a ferramenta não imprime; C2-E07 erro técnico de leitura do CSV | ext1 e ext2/ext3, cada uma congelada antes da execução |
| C3 | caso REQ-003 divergiu na tentativa 1 | reclassificado INDETERMINADO na refeita (depois de conhecer o resultado) |

Todas foram decididas **depois de ver a falha**, que é o ponto em que o protocolo pede cautela. Um revisor independente deveria confirmar que cada correção é defeito de suíte e não ajuste para o caso passar.

### 6.4 Desvios e perdas de isolamento (resumo)

- **Z3 no PATH:** em C1 só nos casos que o usam; em C3 e C4 em todos, por causa de texto contraditório sobre a obrigatoriedade.
- **Contato com o SUT antes do baseline:** em C2 e C4 a CLI foi invocada de forma exploratória (e `Main.java` lido em C4) para conhecer formatos de saída, depois de congelar o oráculo. As expectativas não mudaram, mas houve contato com saídas.
- **Opções não citadas pelo texto:** a reprodução da tabela de regressão exige `--z3` e `--mutation`, que o texto não liga a cada coluna (registrado em C1; igual em C4).
- **Identificadores escolhidos pelo executor:** `x01…xNN` em C4, porque o texto não define identificadores permitidos.
- **Cegamento:** nunca foi alegado. Também não é possível demonstrar que o modelo não conhecia previamente MC/DC.

## 7. Ameaças à validade

- Uma execução por condição, com um modelo; não há medida de variação.
- Autorrevisão em todas as condições; `sat`/`unsat` não provam fidelidade da tradução.
- Procedimentos heterogêneos: C3 e C4 sob critério estrito explícito; o critério aplicado em C0 a C2 não foi verificado aqui. Extensões, correções e quantidade de casos variaram, então parte da diferença pode vir do procedimento.
- Unidades diferentes entre condições (94, 72, 68 mais 8, 72 e 78 casos); o percentual de determinados é a medida mais comparável.
- Em C4, 8 dos 42 aprovados são verificações estruturais que não exercitam a CLI.
- Cobertura máxima não foi demonstrada em nenhuma condição; os branches não cobertos não foram analisados caso a caso.
- Sem inferência causal: as relações da seção 5 descrevem esta amostra.

## 8. Recomendações

1. Repetir cada condição em sessões isoladas para estimar a variação antes de comparar.
2. Fixar no protocolo o critério de indeterminação e a regra de cobertura (só determinados), hoje definidos em conversa.
3. Revisão independente das correções pós-execução (seção 6.3) e das traduções para SMT-LIB.
4. Verificar a hipótese de que os branches não cobertos em C3 e C4 se concentram em Z3 e formatos de relatório; neste relatório isso é leitura dos totais por pacote, não análise por branch.

## 9. Estado dos artefatos

| Condição | Pasta | Relatório | Resultado |
|---|---|---|---|
| C0 | [C0/](C0/README.md) | [relatorio.md](C0/avaliacao/relatorio.md) | 77,24 %; 71 / 1 / 22 |
| C1 | [C1/](C1/README.md) | [relatorio.md](C1/avaliacao/relatorio.md) | 75,77 %; 57 / 0 / 15 |
| C2 | [C2/](C2/README.md) | [relatorio.md](C2/avaliacao/relatorio.md) | 77,93 %; 58 / 0 / 18 |
| C3 | [C3/](C3/README.md) | [relatorio.md](C3/avaliacao/relatorio.md) | 64,43 %; 40 / 0 / 32 |
| C4 | [C4/](C4/README.md) | [relatorio.md](C4/avaliacao/relatorio.md) | 48,30 %; 42 / 0 / 36 |


