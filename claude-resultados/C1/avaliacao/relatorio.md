# Relatório da execução — condição C1

## Identificação e fontes

- **Condição:** C1 (clareza/consistência pretendidas: alta/alta; nível não presumido).
- **Fonte normativa exclusiva:** `experimentacao-pesquisa/experimentacao-1/documentation/tool-readme-C1.md`,
  SHA-256 `91981FA0181E5CC1BC5A67DAAFC965BB82D6F8EB0A6D47EB58CE291A3EF5D33B`, conferido em 2026-11-24T10:22:08-03:00, antes da leitura.
- **Prompt:** `experimentacao-pesquisa/prompts/geracao-de-oraculos-v3.md` (SHA-256 `c10078b5…866d6d`), seguido junto com
  `protocolo/metodologia.md` e `protocolo/modelo-relatorio.md`.
- **Modelo:** Claude Opus 5.5 (`claude-opus-5-5`), Claude Code no app desktop, sessão iniciada por outra sessão.
  Temperatura e outros parâmetros de amostragem: `não informado`.
- **Contexto e isolamento:** a sessão recebeu da sessão de origem a tarefa, as regras de isolamento e as notas de ambiente
  (caminhos de Java, Maven, Z3, JaCoCo e procedimento de build com `javac`), sem resultados de outras condições. Não foram
  abertos `claude-resultados/C0/`, `copilot-resultados/`, `research/`, `relatorios/`, `exemplos/saidas/`, as outras
  `experimentacao-*` nem `experimentos/`, nem o histórico git desses caminhos. O código do SUT (`mcdc-*/src`, via cópia
  `git archive`) só foi lido depois do congelamento do oráculo (10:29:39), e só para saber invocar a CLI e ler os formatos
  de saída (`Main`, `CsvReport`, `TruthTableCsvReport`, `JsonReport`, `VerifyReport`) e, na extensão, para localizar
  branches não cobertos. Limite: não é possível demonstrar ausência de influência do conhecimento prévio do modelo
  sobre MC/DC (literatura) nem sobre a ferramenta.
- **Commit de referência:** `92d9df8929b20b092eb8664810a829cb4933d44f` (`main`, árvore limpa).
- **Ambiente:** Windows 11 Home 10.0.26200; Java/javac 21.0.3; Python 3.13.5; Z3 5.4.1 (64 bit, build 145c0c51…);
  JaCoCo 0.8.16 (agente e CLI); Jackson 2.17.2. O Maven não foi usado (offline); o SUT foi compilado com
  `javac --release 21 -encoding UTF-8 -g` a partir de `git archive HEAD`, fora do repositório
  (`experimento/build-sut/build.sh`, log e hashes das 73 classes em `experimento/build-sut/`).

## Oráculos e Z3

- **Inventário e análise:** `experimento/analise-oraculo.md` (inventário por área, 7 decisões de interpretação,
  relação texto–fórmula, autorrevisão); `experimento/inventario-oraculo.md` (tabela por caso com trecho literal).
- **Casos:** baseline com 79 casos (70 DETERMINADO, 9 INDETERMINADO) em `experimento/oraculo.json`; extensão 01 com
  31 casos (28 DETERMINADO, 3 INDETERMINADO) em `experimento/extensao-01/oraculo-extensao-01.json`. Cada caso tem ID,
  comando(s), ambiente (com ou sem Z3 no PATH), trecho literal com linha, regra, expectativa, justificativa e consultas Z3.
- **Z3:** `z3.exe` 5.4.1 independente do SUT, `-T:60`. Baseline: 63 arquivos de consulta (`experimento/z3/`; os de viabilidade da VM têm uma
  `check-sat` por linha); extensão: 48 consultas (`experimento/extensao-01/z3/`). Nenhuma resposta `unknown`, nenhum timeout. Principais testemunhas:
  pares de causa única (`sat`) para as expressões com código 0 esperado; A sem par com `--constraint A` (`unsat`) e com
  par sem restrição (`sat`), ou seja, bloqueada; pedal de REQ-003 sem efeito (`unsat`), ou seja, redundante; das 152
  linhas da VM, 4 são impossíveis (vm4 e vm5, TFF/FFF), como diz a tabela de regressão; 0 conflitos na VM (10 `unsat`);
  lacuna da VM com `preparing_weak` (`sat`); totais da tabela de regressão consistentes (`unsat` da negação);
  tamanhos mínimos de suíte de causa única 4 e 3 (auxiliares). O Z3 não prova que a tradução do texto em fórmulas seja fiel.
- **Indeterminados (12):** AN-25 (>20 entradas), AN-35 (>30 no direto), AN-36 (`--boundary` sem `--z3`), AN-37
  (`--constraint` com arquivo), AN-38 (causa única com entrada repetida), AN-39 (comando desconhecido), AN-40 (sem
  argumentos), AN-44 (linha `.mcdc` sem identificador), SY-TIS-07 ("requisito completo" não definido), EX-29
  (`--context` no analyze), EX-30 (`--exact` com `--direct`), EX-31 (`--mutation` no direto). Todos foram executados só
  como diagnóstico, sem julgamento.
- **Congelamento (SHA-256 com data e hora, em `experimento/congelamento/`):**
  `01-oraculo.sha256` (10:29:39, antes de ler o SUT), `02-suite.sha256` (10:32:11, antes da 1ª execução; inclui o hash do
  manifesto 01), `03-correcao-01.sha256` (10:37:47), `04-extensao-01.sha256` (antes da rodada-03), `05-resultados.sha256`
  (resultados finais).
- **Revisão:** autorrevisão; não houve revisor independente.

## Métricas

Unidade de contagem: **um caso = um ID do oráculo** (um ou mais comandos da CLI; todas as asserções devem valer).
Branch Coverage: JaCoCo 0.8.16, contador BRANCH, escopo = todas as classes de produção dos 4 módulos compilados
(`--classfiles` de `mcdc-core`, `mcdc-requirements`, `mcdc-z3` e `mcdc-cli`), inclusive classes não carregadas e as
classes de mutação (`core.mutation`). Ficam de fora o harness (Python) e as bibliotecas externas (Jackson, JDK).
O JaCoCo analisou 69 das 73 classes; as outras 4 não têm código executável (as interfaces `FeasibilityChecker` e
`SuiteOptimizer`) ou são sintéticas. Não houve análise de mutação.

| Rodada | Casos | Branch Coverage | Aprovados | Falhos | Indeterminados | Erros técnicos |
|---|---|---|---|---|---|---|
| rodada-01 baseline (bruta) | 79 | 1042 / 1296 = 80,40% | 69 | 1 (AN-22)* | 9 | — |
| rodada-01 baseline (com AN-22 reclassificado) | 79 | 1042 / 1296 = 80,40% | 69 | 0 | 9 | 1 (AN-22, medição) |
| rodada-02 baseline com a correção 01 | 79 | 1042 / 1296 = 80,40% | 70 | 0 | 9 | 0 |
| rodada-03 extensão 01 (sozinha) | 31 | 910 / 1296 = 70,22% | 27 | 1 (EX-27) | 3 | 0 |
| **Acumulado (rodada-02 + rodada-03)** | **110** | **1117 / 1296 = 86,19%** | **97** | **1** | **12** | **0** |

\* A falha de AN-22 na rodada-01 veio do harness: a JVM escrevia o stdout em Cp1252 e o runner decodificava em UTF-8.
É erro técnico, não divergência semântica (`experimento/correcoes/correcao-01-codificacao-stdout.md`). O baseline foi
preservado; a rodada-02 reexecutou tudo com a correção congelada.

Linhas (informativo, não é métrica da pesquisa): acumulado 1859/2001. Por pacote (branches, acumulado): cli 292/337,
core 263/287, core.model 46/60, core.mutation 62/64, requirements 141/162, z3 313/386.

Não há demonstração de que 86,19% seja o máximo possível; os branches restantes incluem caminhos de erro do processo
Z3 (timeout e resposta inválida), símbolos especiais no SMT-LIB e combinações de opções sem suporte documental.

## Evidências e limitações

- **Divergência (FALHOU), EX-27:** `mcdc verify --json EX05_virgula_requisito.json` com o Z3 fora do PATH terminou com
  código 0, sem mencionar o Z3. A expectativa vem de L73 ("as opções que exigem o Z3 avisam quando o executável não está
  instalado") e L63/L83 (o `verify` usa o Z3). A entrada tinha uma só decisão, e a saída diz "0 pares que escrevem alguma
  variável em comum"; o motivo provável é que nenhuma consulta ao Z3 foi necessária. O texto não faz essa ressalva, por
  isso a divergência fica registrada em relação à referência adotada. Pela regra de preservação, o caso não foi refeito
  com outra entrada.
- **Erro técnico:** AN-22 na rodada-01 (acima). Nenhum outro caso ficou não avaliado, e não houve timeout.
- **Expectativas por eliminação ou interpretação** (ver `analise-oraculo.md` §2): código 1 para arquivo inexistente,
  formato inválido, `csv` no check, `-x` e opção sem valor; tipo `int` em EX-01; analogia de fronteira em EX-18;
  mascaramento usado só através de L491 e dos números literais. Todas passaram; se a interpretação estiver errada, o
  caso pode estar mal classificado como determinado.
- **Medição adaptada ao formato:** as expectativas foram congeladas antes da leitura dos formatos. Os extratores (campos
  JSON, colunas CSV, coluna `feasible`) foram escritos depois, lendo o código dos relatórios, e congelados antes da
  execução. Para contar conflitos (SY-*-03), a suíte roda também o mesmo `verify` com `--format json`.
- **Dados brutos:** `resultados/<rodada>/casos/<ID>/` (`cmdN.stdout`, `cmdN.stderr`, `resultado.json` com o código de
  saída e o tempo), `resultados.json`, `execucao.log`, `jacoco.exec`, `jacoco.csv`, `jacoco.xml` e `jacoco-html/` por rodada,
  mais `resultados/acumulado/`.
- **Comandos:** build `bash experimento/build-sut/build.sh <dir>`; suíte `python -I suite/run_suite.py --oraculo <json>
  --classpath-file <dir>/runtime.classpath --rodada <dir> [--entradas <dir>]`; cobertura
  `bash suite/coverage.sh <dir-build> <dir-rodada> [execs…]`.
- **Limitações:** compilação com `javac` em vez de Maven (as mesmas fontes e a mesma versão do Jackson, sem plugins);
  classes compiladas no scratchpad da sessão (hashes preservados em `experimento/build-sut/classes.sha256`); uma JVM por
  comando com o agente JaCoCo em `append`; o Z3 do SUT é o mesmo executável do Z3 independente (5.4.1), usado em
  processos separados; o modelo e o avaliador são o mesmo agente, com autorrevisão apenas.
