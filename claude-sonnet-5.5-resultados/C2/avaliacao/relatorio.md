# RESULTADOS — Condição C2 (Claude Sonnet 5.5)

## Identificação e fontes

- Condição: **C2**. Fonte normativa exclusiva: `experimentacao-pesquisa/experimentacao-2/documentation/tool-readme-C2.md`,
  SHA-256 `61C4062B5FC6B4F364F40465B0E017C80E0FA0C5433412EB2E925C545F6EFBE1` (conferido **antes** da leitura; coincide).
- Prompt: `experimentacao-pesquisa/prompts/geracao-de-oraculos-v3.md`; protocolo `protocolo/metodologia.md`; modelo `protocolo/modelo-relatorio.md`.
- Modelo: Claude Sonnet 5.5 (`claude-sonnet-5-5`), sessão do Claude Code; configuração de amostragem: não informado.
- Commit de referência do SUT/repositório no início: `119c65dd7b842fa79ad60cab9727df8996d62caf` (árvore limpa; SUT e documentação não alterados).
- Ambiente: Windows 11, Git Bash/PowerShell, Java (JDK 21+), sem Maven (classes já compiladas, sem recompilar), Python 3.13.5 + pytest 9,
  Z3 5.4.1 (build 145c0c51…), JaCoCo 0.8.16 (agente + CLI).
- **Isolamento**: não foram lidas nem usadas as pastas `claude-opus-5.5-resultados`, `gpt-6.1-terra-resultados`,
  `claude-sonnet-5.5-resultados/C0` e `C1`, nem a pasta de notas compartilhadas da sessão-mãe. Só o método descrito na tarefa foi reaproveitado
  (oráculo antes do SUT, Z3, congelamento, baseline). Não é possível demonstrar ausência de influência do conhecimento prévio do modelo sobre a ferramenta.

## Oráculo e Z3 (resumo; detalhes em `../experimento/`)

- 68 casos no oráculo: **50 determinados** e **18 indeterminados** (omissão, expressão corrompida, falta de definição). Unidade de contagem:
  **um caso do oráculo = um teste** (ID estável `C2-nnn`).
- O texto-fonte está fortemente degradado (letras/palavras ausentes). Só se determinou o que o texto fixa de forma única; completar expressões
  corrompidas (p.ex. `((E or D) and (not ? or D)) or B`) seria suposição → INDETERMINADO.
- Decisão do pesquisador aplicada: indeterminados registrados, **não executados**, fora da cobertura.
- Z3 5.4.1 independente (`z3.exe` + SMT-LIB gerado por `experimento/z3/gerar_smt.py`); cerca de 45 consultas (arquivos .smt2 com respostas .out), nenhuma `unknown`/timeout. Resultados-chave: mínimos de suíte
  `(A and B) or C`=4, `A and not B`=3, `(A or B) and (C or D)`=4 (mascaramento padrão) / 5 (causa única); 2 de 8 combinações impossíveis em
  `speed > 100 or (speed > 50 and rain)`; `B` nunca altera `A or (A and B)`.
- Revisão texto→fórmula: **autorrevisão** (sem revisor independente). `sat/unsat` não provam fidelidade da tradução; a definição de mascaramento
  não existe no texto e foi usada apenas onde coincide com causa única.
- Congelamentos: `../experimento/congelamento/01-oraculo.sha256` (antes de qualquer leitura de código do SUT), `02-suite.sha256`
  (baseline e extensões, cada um antes da respectiva execução).

## Métricas

Escopo da cobertura: JaCoCo 0.8.16, **todas as 69 classes de produção** dos 4 módulos (`mcdc-core`, `mcdc-requirements`, `mcdc-z3` JARs + `mcdc-cli/target/classes`),
inclusive não carregadas e de mutação; sem harness (pytest) nem bibliotecas externas; sem análise de mutação. Branch Coverage = branches cobertos / branches totais.

| Métrica | Baseline | Acumulado (baseline + extensões) |
|---|---|---|
| **Branch Coverage** | **975 / 1296 = 75,23 %** | **1010 / 1296 = 77,93 %** |
| Testes aprovados | 49 | 58 |
| Testes falhos | 1 (C2-020, defeito da própria suíte; ver abaixo) | 0 |
| Testes indeterminados | 18 (registrados, não executados) | 18 |
| Unidade / total de casos | 68 casos | 76 casos (68 + 8 da extensão) |

- Baseline = `test_c2.py`, executado uma vez (1 falhou, 49 passaram, 18 indeterminados não executados; 114,9 s).
- Extensões (cada uma congelada antes de executar; baseline preservado): **ext1** (`test_c2_ext1.py`, 9 testes: reavaliação de C2-020 + 8 casos novos
  documentados C2-E01..E08): 7 passaram, 2 falharam por defeito de verificação da suíte; **ext2** (`test_c2_ext2.py`): C2-020 passou, C2-E07 erro
  técnico de leitura do CSV; **ext3** (`test_c2_ext3.py`): C2-E07 passou.
- Acumulado: C2-020 conta pelo resultado da extensão que corrigiu a verificação; o baseline segue registrado como FALHOU.

## Avaliação

- **Nenhuma divergência semântica foi observada**: todos os 58 casos determinados avaliados (incluindo os números de regressão VM/TIS/NPP, mutantes,
  conflitos, `--exact`, `--direct`, `--z3`, `check`, `verify`, formatos e entradas inválidas) satisfizeram a expectativa documental.
- A única falha do baseline (C2-020) foi **defeito da suíte**, não do SUT: a suíte supôs que o relatório de texto lista as 2^20 linhas; a ferramenta
  declara `Tabela verdade: 1048576 linhas` e não as imprime. A expectativa documental (20 entradas suportadas, 2^20 combinações, cobertura completa)
  foi confirmada na extensão. Preservei o FALHOU do baseline em vez de apagá-lo.
- A cobertura de 77,93 % ficou limitada por escolha de escopo: só havia casos determinados do texto; o texto não descreve mensagens de erro, caminhos
  internos do Z3 (`SmtEncoding`, `Z3Process`), e muitos ramos (`Predicate`, `VerifyReport`, `CheckReport`, `TextReport`) só seriam exercitados com
  expectativas que o texto não fixa (INDETERMINADO). Não se alega cobertura máxima global.
- O texto degradado reduziu a fração determinada (50 de 68 = 73,5 %); 18 indeterminados são lacunas ou corrupções do texto, não defeitos do SUT.

## Evidências e limitações

- Por caso: `resultados-por-caso.csv` (nesta pasta, acumulado, com histórico por rodada), `../resultados/rodada-01-baseline/resultados-por-caso-baseline.csv`, `../resultados/rodada-02-extensoes/resultados-por-caso-extensao1/2/3.csv`.
- Brutos (comando, `exit`, stdout, stderr, arquivos de entrada): `../resultados/rodada-01-baseline/bruto/` (baseline; logs pytest em `bruto/pytest-*.log`), `../resultados/rodada-02-extensoes/bruto-extensao1/2/3/`.
- JUnit: `junit-baseline.xml` (rodada-01) e `junit-extensao1/2/3.xml` (rodada-02). JaCoCo: `jacoco-baseline.{exec,csv}` + `jacoco-baseline-html/` (rodada-01, só baseline);
  `../resultados/acumulado/jacoco.{exec,csv,xml}` + `jacoco-html/` (o `.exec` acumula as 4 rodadas, `append=true`).
- Comando base: `java -Dstdout.encoding=UTF-8 -cp "mcdc-cli/target/classes;<classpath.txt>" io.github.rvdomingos.mcdc.cli.Main …` com
  `JAVA_TOOL_OPTIONS=-javaagent:…jacoco.agent-0.8.16-runtime.jar=destfile=…,append=true`; `z3.exe` no `PATH` apenas nos casos que o usam
  (nos demais é removido do `PATH`). Comandos de execução em `suite/README.md`.
- Desvios/limitações:
  1. Antes de congelar a suíte, a CLI foi invocada de forma exploratória (exemplos simples e `exemplos/vm-decisoes.json`) apenas para conhecer os formatos
     de saída; as expectativas do oráculo já estavam congeladas e não foram alteradas. Esse contato com saídas é uma perda parcial de cegamento na fase de suíte.
  2. Duas extensões extras (ext2, ext3) foram necessárias para corrigir erros de verificação da própria suíte; cada uma foi congelada antes de executar.
  3. A verificação do número de mutantes usa a soma dos campos `total`, `equivalent`, `killed` do JSON; a interpretação da tabela de regressão
     ("Mutantes/Equivalentes/Pegos") é da análise documental.
  4. Casos com leitura interpretativa (códigos de saída de VM/TIS/NPP; `verify` sem `--context`; "Completos") estão registrados em `../experimento/analise-oraculo.md`.
  5. Tempo de execução e `unknown`/timeouts do Z3: nenhum timeout; erros técnicos da CLI: nenhum. Erros técnicos da suíte: C2-E07 em ext2 (leitura de CSV).
  6. Ferramenta de cobertura mede instruções de bytecode de ramos; o total de 1296 branches coincide com o número de "desvios" que o próprio texto-fonte reporta para o projeto, mas isso não foi usado como meta.
