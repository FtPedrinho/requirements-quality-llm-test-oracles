# Relatório da execução — condição C3

## Identificação e fontes

- **Condição:** C3 (clareza alta / consistência baixa pretendidas; o nível não é presumido).
- **Fonte normativa exclusiva:** `experimentacao-pesquisa/experimentacao-3/documentation/tool-readme-C3.md`,
  SHA-256 `F18B0821D79C7315486C13D5260FA2F6D6E9418EF03B86CDE58E66B91B7B87A3` (conferido antes da leitura: confere).
- **Prompt:** `experimentacao-pesquisa/prompts/geracao-de-oraculos-v3.md`, com o protocolo `protocolo/metodologia.md`.
- **Modelo:** Claude Opus 5.5 (`claude-opus-5-5`), no Claude Code (app desktop), em uma sessão iniciada por outra
  sessão. Temperatura e outros parâmetros: `não informado`.
- **Contexto e isolamento:** a sessão recebeu da sessão de origem uma descrição da pesquisa e as regras de
  isolamento. Não abri nem listei `claude-resultados/C0,C1,C2,C4`, `copilot-resultados/`, `research/`,
  `relatorios/`, `exemplos/saidas/` nem as outras fontes Cx. O `git status` inicial, anexado automaticamente,
  mostrava o nome da pasta `claude-resultados/C2/` como não rastreada (só o nome, sem conteúdo). Antes do
  congelamento, além do protocolo e da fonte, li os arquivos de entrada de `exemplos/` citados pela fonte e vi o
  script de lançamento `./mcdc` (raiz do repositório; revela o nome da classe principal, sem comportamento).
  Não afirmo que não houve influência de conhecimento prévio do modelo.
- **Commit de referência do SUT:** `ed7d2e00170e3e2c28201bf63e1b51a24a1bfe81` (HEAD, via `git archive`).
- **Ambiente:** Windows 11; Java 21.0.3 (`javac --release 21 -g`); Jackson 2.17.2; Z3 5.4.1 independente
  (`C:/Users/User/AppData/Roaming/Python/bin/z3.exe`); JaCoCo 0.8.16 (agente + CLI); Python 3.13.5.

## Metodologia aplicada e o que mudou ao longo da execução

1. Conferi o hash e li a fonte inteira. Inventariei comportamentos e catalogei **15 conflitos internos** (K1–K15,
   `experimento/analise.md`), 12 deles com efeito observável pela CLI.
2. **Política para conflitos:** uma passagem que se declara "definitiva", "complementar" ou "substitui a
   anterior" é uma das partes do conflito, não uma regra de precedência da documentação. Por isso não desempata.
   O observável atingido fica INDETERMINADO. Quando todas as leituras levam ao mesmo resultado (ex.: contagem de
   condições sem entrada repetida), a expectativa fica DETERMINADA. Componentes atingidos dentro de casos
   determinados (sobretudo o código de saída, K3) ficam registrados como "não julgados".
3. **Z3 independente:** 106 consultas na base, mais 6 na extensão (`experimento/z3`, `experimento/extensao-r2/z3`).
   As consultas cobrem tabelas-verdade, equivalências, existência de pares em três critérios, viabilidade,
   fronteiras com prova de unicidade, avaliação dos CSVs e somas da regressão. Para cada conflito, cada leitura
   isolada é `sat` e as duas juntas são `unsat`, o que mostra que o conflito afeta o observável. Nenhum `unknown`
   ou timeout.
4. **Congelamento:** `experimento/congelamento-oraculo.sha256` (233 arquivos; o próprio manifesto tem
   `8c384e50…`; `oraculo.json` = `e8a602f5…`), gravado antes de ler o código ou executar o SUT.
5. **Build:** `experimento/build/build.sh`, fora do repositório, ordem core → requirements → z3 → cli. Os hashes
   das 73 classes estão em `experimento/build/classes.sha256` (`e0d960f3…`).
6. **Suíte:** depois do congelamento, li só a CLI (`Main`, relatórios) para saber como invocar e onde estão os
   dados. Escrevi `suite/runner.py`, que roda cada caso com os argumentos congelados, com o agente JaCoCo, e lê o
   texto ou o JSON. Congelei a suíte em `congelamento-suite-r1.sha256` antes da r1.
7. **Rodada r1** (75 casos). Duas asserções falharam (T20, T22). Ao revisar, constatei que o **harness** estava
   errado: os CSVs de `check` usavam `decision = D`, mas a fonte não define o identificador de uma decisão
   escrita como expressão direta (a CLI usa `REQ`), então nenhum teste foi associado. T20, T21 e T22 da r1 viram
   **casos inválidos**: a precondição "os testes pertencem à decisão" não se cumpriu. Não são falhas semânticas
   nem aprovações. T21 havia passado só por vacuidade. Os resultados brutos da r1 estão preservados.
8. **Rodada r2, correção e extensão** (`experimento/extensao-r2/`, congelada em `congelamento-r2.sha256` antes
   de rodar). A correção usa a mesma decisão vinda de `abc.mcdc` (`D: (A and B) or C`; o ID é definido pelo
   formato `.mcdc`, L151) e os mesmos CSVs: T20c, T21c, T22c, T25c, I03c, I38c. A extensão foi guiada pelos
   branches não cobertos na r1, com expectativas tiradas só do texto: E01 (check com valores concretos int/real/
   enum/bool), E02 (valores concretos e fronteiras com negativos), E03 (`==`, `!=`, `<` com negativo), E04
   (verify em JSON) e 8 diagnósticos indeterminados (I40–I47: combinações de opções cuja reação o texto omite).
9. **Acumulado r1+r2 (substituído):** cada ID estável contava uma vez, e a cobertura somava os dois
   `jacoco.exec`. Resultado: 1068/1296, 40/0/47. Esse número **não é mais o resultado final** (ver o passo 10).
10. **Suíte refeita (r3, resultado final).** Na revisão, constatei que os diagnósticos I40–I47 da r2 tinham sido
    criados só para alcançar branches de validação de opções. Nenhum trecho da fonte descreve essas situações ou
    o resultado delas. Eram testes desnecessários e inflavam a cobertura. A r3 refaz a suíte do zero
    (`experimento/r3/selecao.py`, congelada em `congelamento-r3.sha256`), **sem nenhuma expectativa nova**:
    - os 75 casos congelados da base, com T20/T21/T22/T25/I03/I38 trocados pelas versões corrigidas;
    - E01–E04 (situações descritas pela documentação, com expectativa);
    - **sem** I40–I47.
    O runner r3 executa cada comando distinto uma vez (64 execuções) e julga sobre essa mesma observação os
    casos que compartilham comando e pré-condição (ex.: T01, T08, I01, I09, I11). Assim, não há execução
    duplicada. O código que só os casos removidos alcançavam fica sem cobertura.
11. **Cobertura sem os indeterminados (r4, resultado final).** Por decisão do pesquisador, um registro
    INDETERMINADO não cumpre o papel de teste: não tem expectativa e, portanto, não verifica nada. Por isso não
    afeta a cobertura. A r4 executa apenas os 40 casos determinados da r3, com o mesmo
    oráculo e o mesmo runner e um `jacoco.exec` novo. A lista de IDs está em `experimento/r4/ids-determinados.txt`,
    congelada em `congelamento-r4.sha256`. Os 39 indeterminados continuam registrados e contados como
    indeterminados, mas não são executados nem contribuem para a cobertura. As observações diagnósticas deles
    ficam na r3.

## Métricas

Regra adotada: indeterminados são registros do oráculo, não testes. Entram só na contagem de indeterminados e
não são executados para a cobertura. Unidade de contagem: caso com ID estável (C3-Txx/Exx determinado, C3-Ixx indeterminado). Ferramenta JaCoCo
0.8.16, contador BRANCH. Escopo de produção: as 69 classes analisadas dos quatro módulos (`--classfiles` de
`mcdc-core`, `mcdc-requirements`, `mcdc-z3` e `mcdc-cli`), inclusive as não carregadas e as de mutação. Exclusões:
harness, Jackson e JDK. Não rodei análise de mutação de código.

| Rodada | Branch Coverage | Aprovados | Falhos | Indeterminados | Fora da contagem |
|---|---|---|---|---|---|
| **r4: final, cobertura só dos 40 determinados** | **859 / 1296 = 66,28%** | **40** | **0** | **39** (registrados, não executados) | — |
| r3: suíte refeita, indeterminados executados como diagnóstico (histórico) | 1056 / 1296 = 81,48% | 40 | 0 | 39 | — |
| r1 (bruto, histórico) | 1016 / 1296 = 78,40% | 34 | 2 | 39 | — |
| r1 (revisado, histórico) | 1016 / 1296 = 78,40% | 33 | 0 | 39 | 3 inválidos (T20, T21, T22) |
| r2 (correção + extensão, histórico) | 697 / 1296 = 53,78% | 8 | 0 | 10 | — |
| acumulado r1+r2 (substituído pela r3) | 1068 / 1296 = 82,41% | 40 | 0 | 47 | incluía I40–I47, removidos |

Resultado final: a r4, com 79 casos (40 determinados executados e julgados, 39 indeterminados só registrados).
Cobertura de branches por módulo na r4: core 327/411, requirements 123/162, z3 204/386, cli 205/337. Os
principais trechos sem cobertura são `Z3DirectAnalyzer` (80 branches: modo direto, todo indeterminado por K6/K10),
`Main` (45), `SmtEncoding` (41), `Z3SuiteOptimizer` (28: `--exact`, K8), `TruthTableCsvReport` e `CsvReport`
(26 cada: K5), `MinimalSuite` (20), `TestCasesFile` (20), `Predicate` (13) e `VerifyReport` (13). Ficam sem
cobertura porque nenhum caso com expectativa documental determinada os alcança. A queda de 81,48% para 66,28%
(197 branches) mede o código que só foi executado sem julgamento. Não afirmo que esta seja a cobertura máxima possível.

## Resultados, divergências e observações

- **Nenhuma divergência semântica (r3 e r4).** Todos os 40 casos determinados passaram: tabelas-verdade (operadores e
  precedência), pares que mudam a condição, cobertura completa de `(A and B) or C` nas duas variantes, recusa de
  expressões inválidas, `.mcdc`, contagens da regressão de VM/NPP/TIS que não dependem dos conflitos, total de
  mutantes, `-o`, JSON, `check`, fronteiras, valores concretos e restrição.
- **Casos inválidos (r1):** T20, T21 e T22, por erro de entrada meu (erro do harness, não do SUT). Estão em
  `resultados/r1/casos/C3-T2{0,1,2}` e foram corrigidos na r2/r3. Na r3 não houve erro técnico nem do harness.
- **Errata do oráculo congelado (não alterado):** o título de C3-T29 diz "TIS e NPP", mas o caso só executa e
  julga o NPP (`the_water_pressure`). As fronteiras do TIS calculadas no Z3 não foram usadas por nenhum caso.
- **Observações dos indeterminados** (só diagnóstico, sem julgamento): os códigos de saída seguiram a L145
  (0 = ok, 1 = inválida, 2 = problema), não a L147. As condições foram contadas por ocorrência (`A#1, B, A#2, C`).
  Combinações `unsat` foram marcadas impossíveis (L293). `pedal_pressionado` e `freio_acionado#2` foram
  rotulados "redundante" (L305). Sem z3 no PATH, a análise simples rodou e `--z3` deu "Z3 não encontrado" com
  código 1. `--z3` com 13 entradas e `--direct` com 26 usaram o modo direto. 21 entradas foram recusadas.
  `truth-csv` trouxe a tabela inteira. `--exact` deu 5 testes. `verify` do TIS apontou 3 conflitos.
  Esses comportamentos ficam do mesmo lado de uma das partes de cada conflito, mas pela política adotada isso
  **não** os converte em aprovação.

Resultados por caso: `avaliacao/resultados-por-caso.md`. Dados brutos: `resultados/<rodada>/casos/<ID>/`
(stdout, stderr, exit e comando; na r3, `reutiliza.txt` aponta a execução compartilhada) e `resultados.json`.

## Como a qualidade da documentação do C3 afetou o oráculo

- **Clareza alta:** o texto é direto e tem exemplos concretos (operadores, `speed > 100 → 100 e 101`,
  formato `.mcdc`, números da regressão). Isso deixou os aspectos não atingidos por contradição **bem
  determinados e verificáveis**: tabela-verdade, sintaxe, formatos de entrada, fronteiras, valores concretos e
  contagens da regressão. Nesses pontos o oráculo foi forte e nada divergiu.
- **Consistência baixa:** a fonte põe, ao lado da regra original, uma regra contrária com aparência de
  autoridade: códigos de saída, contagem de condições, critério de par, sat/unsat, gulosa × exata,
  redundante × bloqueada, csv × truth-csv, colunas do CSV, dependência do Z3 e limites de modo. Os pontos
  atingidos são justamente o **núcleo semântico do MC/DC** e o principal canal de asserção de uma CLI (o código
  de saída). Por isso **39 de 79 casos (49%) ficaram indeterminados**, e muitos casos determinados tiveram de
  restringir-se a propriedades fracas, comuns a todas as leituras. Exemplo: "o par muda a condição", e não "o par
  muda a condição e o resultado".
- **Sem divergências:** como as asserções fortes caíram em conflito, o oráculo não pôde afirmar nada nos pontos
  em que o comportamento da ferramenta escolhe uma das leituras. Inconsistência na documentação aparece aqui como
  **perda de poder de detecção**, não como falhas. Um defeito real em pares ou códigos de saída não seria
  detectado por este oráculo.
- **Cobertura:** 66,28% de branches na r4, só com casos determinados. Com os indeterminados executados como
  diagnóstico, a cobertura chegava a 81,48% (r3). A diferença é o efeito direto da inconsistência: as áreas
  que concentram as contradições (modo direto, suíte exata, csv/truth-csv, sat/unsat) ficam sem cobertura julgada. A
  cobertura alta não significa que o comportamento coberto foi julgado: boa parte dos branches de `mcdc-z3`, dos
  pares e do diagnóstico só foi exercitada por casos sem expectativa.
- **Conflitos não observáveis pela CLI** (K12, K13, K15: métricas, PIT e regras de build) não afetaram o oráculo.

## Limitações

- Autorrevisão: não houve revisor independente da tradução texto → fórmula. `sat`/`unsat` não provam fidelidade.
- A política para conflitos é uma escolha metodológica. Outra política (ex.: dar precedência a passagens que se
  declaram "definitivas") produziria expectativas determinadas e, possivelmente, falhas.
- Generalizações registradas: comparações são entradas (A1) e fronteiras de `<`, `<=` e `>=` (A4).
- A forma de ler a saída (parsers do runner) foi aprendida do código depois do congelamento. Um erro de parser
  apareceria como erro do harness, e nenhum ocorreu.
- O SUT foi compilado com `javac`, não com Maven. A cobertura é da suíte desta execução, não da suíte do projeto.
