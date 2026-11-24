# Relatório da execução C0

Segue o [modelo de relatório](../../../experimentacao-pesquisa/protocolo/modelo-relatorio.md). Não usa resultados de nenhuma outra condição: `copilot-resultados/` não foi consultado.

## Identificação e fontes

| Item | Valor |
|---|---|
| Condição | C0, documentação original, sem nível de clareza ou consistência atribuído |
| Fonte normativa | `experimentacao-pesquisa/documentacao-original/tool-readme-original.md` |
| SHA-256 da fonte | `72B827BDEE6CE859527765CFF574A473519C00A1AF9AA9F3AACCE4236A4995F8`, conferido antes da leitura |
| Prompt | `experimentacao-pesquisa/prompts/geracao-de-oraculos-v3.md` |
| Modelo | Claude Opus 5.5 (`claude-opus-5-5`) no Claude Code (app desktop); temperatura e demais parâmetros: não informado |
| Commit de referência | `03589c40c3aa07a2138d6923c96049345870a661` (main, árvore limpa) |
| Ambiente | Windows 11 (10.0.26200), JDK 21.0.3, Python 3.13.5 |
| Z3 do oráculo | Z3 5.4.1 (`z3.exe` do pacote `z3-solver`), processo independente do `mcdc-z3` |
| Z3 do SUT | o mesmo executável, posto no PATH só nos casos marcados `z3: true` |
| Cobertura | JaCoCo 0.8.16 (agente + CLI) |
| Data | 2026-11-24 |

**Isolamento.** O contexto da sessão tinha o protocolo, o prompt, o README de `experimentacao-pesquisa` e a fonte C0. O código do SUT ficou acessível no repositório o tempo todo, mas só foi aberto **depois** do congelamento do oráculo (09:42:20). Não tenho como demonstrar ausência de influência de conhecimento prévio do modelo. A especificação em PDF não foi lida. Houve uma perda de isolamento: o defeito das entradas da correção 1 foi notado pela mensagem do SUT (detalhes abaixo).

## Oráculos e Z3

- **Inventário e decisões de interpretação:** [analise.md](../experimento/oraculo/analise.md). Casos: [oraculo.json](../experimento/oraculo/oraculo.json) e [oraculo-extensao-1.json](../experimento/extensao-1/oraculo-extensao-1.json). Cada caso tem ID, argumentos, trecho literal, regra, expectativa e justificativa.
- **Z3 do baseline:** 94 consultas SMT-LIB em [z3/consultas/](../experimento/oraculo/z3/consultas/), todas conformes, com testemunhas nos `.out`.
  - As consultas cobrem a existência de par por condição (mascaramento e causa única), o tamanho mínimo da suíte ((A∧B)∨C = 4; A∧¬B = 3; exemplo do `--exact` = 5; paridade = 8; conjunção = N+1 por lemas para N=13 e N=20), as linhas impossíveis, a fronteira 100/101, os conflitos e lacunas do `verify` e as suítes dos CSV do `check`.
- **Z3 da extensão:** 42 consultas, todas conformes.
- **Erro técnico do Z3:** na rodada 1 do oráculo, a consulta `Q-E14-min-13` deu *timeout* (`-T:60`). Ela foi trocada por lemas, como registra [rodada-1-timeout.txt](../experimento/oraculo/z3/rodada-1-timeout.txt).
- **Congelamentos (SHA-256 do manifesto):**

| Congelamento | Hora | SHA-256 do manifesto |
|---|---|---|
| Oráculo (208 arquivos) | 09:42:20 | `501ac0b31c72cb21b2ac685f6240d762f8ee7ec90607d49bbcaec624ec204c8a` |
| Suíte, build do SUT e ferramentas (89 arquivos) | 09:46:37 | `66a8ce0943960e6bb3b1a5ace588456140166085a74a83cff4311c0d3fa99fe0` |
| Correção 1 (entradas) | 09:49:57 | `518b1bddcaf25613039ab6e439fee6110891336dd53c8b469b8d68056636f090` |
| Extensão 1 | 09:55:06 | `c9832a0ba1de57305443801b07d8fbce5d0494f29427b33f17779228968087ef` |

- **Revisão:** autorrevisão, sem revisor independente.

## Métricas

**Unidade de contagem:** um caso = um ID do oráculo. As várias asserções de um ID contam como um único teste. Execuções auxiliares de comparação (`same_truth_as`, `same_pairing_as`) não contam como testes.

**Escopo da cobertura:** todas as 69 classes de produção de `mcdc-core`, `mcdc-requirements`, `mcdc-z3` e `mcdc-cli`, compiladas do commit de referência, inclusive as não carregadas e as do pacote `mutation`. Ficam de fora o harness (Python), Jackson e o JDK. O denominador de 1296 desvios coincide com o total que o próprio README declara.

### Resultado final (baseline da rodada 2 + extensão 1)

| Métrica | Resultado |
|---|---|
| **Branch Coverage** | **1097 / 1296 = 84,65%** |
| **Testes aprovados** | **92** |
| **Testes falhos** | **1** (C0-X13) |
| **Testes indeterminados** | **14** |

### Por fase

| Fase | Casos | Aprovados | Falhos | Indeterminados | Inválidos / erro técnico | Branch Coverage |
|---|---|---|---|---|---|---|
| Rodada 1, baseline original | 85 | 69 | 0 semânticos | 13 | 3 inválidos (C07–C09) | 1037/1296 = 80,02% |
| Rodada 2, baseline corrigido | 85 | 72 | 0 | 13 | 0 | 1040/1296 = 80,25% |
| Extensão 1, só os casos novos | 22 | 20 | 1 | 1 | 0 | 937/1296 = 72,30% |
| **Acumulado (rodada 2 + extensão 1)** | **107** | **92** | **1** | **14** | 0 | **1097/1296 = 84,65%** |

Na rodada 1, o runner registrou C07–C09 como FALHOU porque as entradas eram JSON inválido. Eles foram reclassificados como inválidos e não entram em nenhuma contagem de falhas.

Cobertura acumulada por módulo: cli 297/337 (88,1%), core 348/411 (84,7%), requirements 138/162 (85,2%), z3 314/386 (81,3%). Não há alegação de que esse seja o máximo possível.

## Evidências

- Resultados por caso: [resultados-por-caso.md](resultados-por-caso.md). Os dados brutos estão em `../resultados/<fase>/resultados.json`, com stdout e stderr de cada caso em `saidas/<ID>/`.
- Cobertura: `../resultados/<fase>/jacoco.exec`, `jacoco.csv`, `jacoco.xml` e `jacoco-html/`.
- Como reproduzir: `python -I suite/executar_suite.py <rodada>` (a extensão usa `ORACULO=…/oraculo-extensao-1.json`) e `bash suite/cobertura.sh <rodada>`. O merge do acumulado usa `jacococli merge rodada-2/jacoco.exec extensao-1/jacoco.exec`.

### Divergência (FALHOU)

**C0-X13.** A documentação, na linha `InputEdgeCasesTest`, diz "número da linha com erro" para o CSV de testes. Com o valor `X` na linha 4 do CSV, o SUT recusou com código 1 (como esperado), mas a mensagem foi `Erro: T1: valor lógico inválido: X`: cita o teste, **não a linha**.

Ameaça à validade: a frase vem da descrição de um teste interno e pode valer só para outro tipo de erro de linha. Pelo protocolo, a expectativa sustentada pelo texto foi mantida.

### Indeterminados: observado, sem julgamento

| ID | Situação sem expectativa única | Observado |
|---|---|---|
| A15 | 21 entradas sem `--z3` | código 1 |
| A17 | 31 entradas com `--direct` | código 1 |
| B15 | comando desconhecido | código 1 + uso |
| B16 | sem argumentos | código 1 + uso |
| B17 | `x > -5` (sinal de menos) | código 0 |
| C12 | `--constraint` com `-f` | código 1 |
| D03 | `--boundary` sem `--z3` | código 1 |
| E07 | `verify` VM com `--context` do README | código 2 |
| F07 | `check` sem `--tests` | código 1 |
| F08 | `check` do exemplo do README | código 2 |
| G06 | `verify` em `.mcdc` | código 0 |
| G07 | `verify` com expressão direta | código 0 |
| G09 | causa única com aparições acopladas | código 0 |
| X22 | `verify --z3` | código 1 |

## Erros técnicos e casos inválidos (fora das métricas)

1. **Build:** o Maven 3.10.1 offline não resolveu plugins (sem rede). O SUT foi compilado com `javac --release 21` a partir de `git archive HEAD`, num diretório separado ([COMO-FOI-COMPILADO.md](../experimento/build-sut/COMO-FOI-COMPILADO.md)). As fontes e a documentação não foram tocadas.
2. **Z3 do oráculo:** o *timeout* de `Q-E14-min-13` foi substituído por lemas.
3. **Casos inválidos na rodada 1 (C07, C08, C09):** `cafe-doc.json` e `temporal.json` saíram com `/\` em vez de `/\\` (o heredoc perdeu uma barra) e eram JSON inválido. Foram corrigidos sem mudar nenhuma expectativa ([correcao-1](../experimento/correcao-1/README.md)), e a suíte foi reexecutada inteira na rodada 2. **Perda de isolamento:** o defeito foi notado pela mensagem do SUT.
4. **Harness:** o `cobertura.sh` falhava com caminho POSIX ao ler o `config.json` e foi corrigido antes de medir a rodada 1. O runner recebeu extensões aditivas para a extensão 1.

## Limitações

- **Autorrevisão.** O mesmo modelo produziu o oráculo, a suíte e o julgamento.
- **Leituras interpretativas** (detalhadas em `analise.md`): a definição de par em causa única, "guardas simples" = conjunção sem repetição, código 1 para formato não aceito, "ids repetidos" como erro, e "número da linha" (X13).
- **Saída em texto.** O formato não é documentado. Os casos em texto verificam só código de saída e menções mínimas.
- **Adaptadores JSON e CSV.** Foram escritos depois do congelamento, lendo o código, para extrair valores cujos nomes de campo o README não documenta. As expectativas não mudaram, mas a escolha do campo é minha. Exemplo: "Requisitos" foi contado como valores distintos de `requirement`; "Conflitos", como o tamanho da lista `conflicts`.
- **Mesmo binário de Z3.** O oráculo e o SUT usaram o mesmo `z3.exe`. O oráculo não usa a saída do SUT, mas um defeito do próprio Z3 afetaria os dois.
- **Fora do escopo:** o desempenho (os tempos do README são de testes internos) e as notas de mutação PIT (que o protocolo exclui).
- **Codificação:** o stdout e o stderr do SUT chegaram com acentos corrompidos, mesmo com `-Dstdout.encoding=UTF-8`, e foram decodificados com substituição. Nenhuma asserção usa texto acentuado: as verificadas são "redundante", "bloqueada", IDs, "z3", "100" e "101".
- **Hashes das ferramentas externas** (JaCoCo, Jackson, `z3.exe`) estão em `CONGELAMENTO-SUITE.sha256`.
