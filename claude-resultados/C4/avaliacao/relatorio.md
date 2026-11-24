# Relatório da execução — condição C4

## Identificação e fontes

- **Condição:** C4 (clareza e consistência pretendidas baixas; o nível não foi presumido, foi observado no texto).
- **Fonte normativa exclusiva:** `experimentacao-pesquisa/experimentacao-4/tool-readme-C4.md`, SHA-256
  `D6BC0A588CD9A7DF7F1F566573944FA5CB1707BBA676B4E9854CAD2CC5440FC2` (conferido antes da leitura; `experimento/fonte.sha256`).
- **Prompt:** `experimentacao-pesquisa/prompts/geracao-de-oraculos-v3.md` (SHA-256 `c10078b5…6d6d`).
  **Protocolo:** `experimentacao-pesquisa/protocolo/metodologia.md` (SHA-256 `06f829f5…5648`).
- **Modelo/configuração:** Claude Opus 5.5 (`claude-opus-5-5`) no Claude Code (app desktop), sessão iniciada por outra
  sessão com as regras de cobertura e isolamento do pesquisador. Temperatura e demais parâmetros: não informado.
- **Commit de referência:** `ed7d2e00170e3e2c28201bf63e1b51a24a1bfe81` (o SUT compilado vem de `git archive HEAD`).
- **Ambiente:** Windows 11; Java 21.0.3; Python 3.13.5; Z3 5.4.1 independente (`z3.exe`, fora do PATH do SUT);
  JaCoCo 0.8.16 (agente e CLI); Jackson 2.17.2. Maven não usado (offline); SUT compilado com
  `javac --release 21 -encoding UTF-8 -g` (`experimento/build/build-sut.sh`).
- **Isolamento:** não foram abertos resultados de C0–C3, `copilot-resultados/`, `research/`, `relatorios/`,
  `exemplos/saidas/`, outras `experimentacao-*` nem `experimentacao-pesquisa/experimentos/`. Perda menor: dois
  arquivos de entrada não citados pela fonte (`exemplos/vm-requisitos.mcdc`, `exemplos/maquina-cafe.mcdc`) foram
  exibidos por um comando de leitura; não foram usados. Não é possível demonstrar ausência de influência do
  conhecimento prévio do modelo.

## Metodologia aplicada

1. Verificação do SHA-256 da fonte e leitura integral (423 linhas).
2. Inventário de regras, exemplos, limites e conflitos (`experimento/analise.md`).
3. Derivação dos casos só do texto. Três decisões guiaram a derivação:
   - operandos apagados dos exemplos (o `A` de `( and B) or C`) **não** foram reconstruídos; as regras em prosa
     foram exercitadas com expressões próprias (E1–E7 e uma expressão DFRS);
   - um conflito que não muda o resultado não impede a expectativa: as duas leituras foram formalizadas no Z3 e,
     quando ambas davam `sat`, o caso ficou determinado; quando divergiam, INDETERMINADO;
   - tudo que depende da classificação de combinações pelo Z3 ficou INDETERMINADO (ver discussão), por isso
     nenhuma execução usa `--z3`.
4. Formalização em SMT-LIB e execução do Z3 independente: 26 consultas (`experimento/z3/`), sem `unknown`/timeout.
5. Autorrevisão (sem revisor independente) e **congelamento** do oráculo por SHA-256 antes de ler ou executar o SUT:
   `experimento/congelamento-oraculo.sha256` (61 arquivos; o próprio manifesto tem SHA-256
   `3c682e14…a9ea`). Conferido de novo após a rodada: intacto.
6. Após o congelamento: compilação do SUT e leitura do código da CLI **só** para invocação e localização dos dados
   (`Main.java`, `JsonReport.java`, `CheckReport.java`, nome dos vetores e mensagens de problema). Resultados de
   invocação: `--te` = `--tests`; observação pelo `--format json`; erros em stderr.
7. Suíte nova (`suite/runner.py`, `suite/cobertura.sh`), congelada antes da execução
   (`suite/congelamento-suite-r1.sha256`, cópia em `suite/versoes/r1-baseline/`).
8. Rodada `r1-baseline`: 18 execuções (X01–X18), cada uma uma vez, numa JVM com agente JaCoCo; 45 casos
   determinados julgados sobre elas; 37 indeterminados registrados e **não executados**.
9. Cobertura: relatório JaCoCo com `--classfiles` dos 4 módulos compilados.

### O que mudou ao longo da execução

- Antes de executar, o runner foi ajustado (ainda antes do congelamento da suíte) para registrar exceções de
  observação como `ERRO_TECNICO` em vez de `FALHOU`; nenhuma ocorreu.
- Nenhuma correção nem extensão após a rodada: a única falha (C4-D26) é divergência documental, não erro do harness,
  e não foi encontrada situação documentada ainda não testada com expectativa única. Os branches não cobertos
  (sobretudo `mcdc-z3`, relatório de texto, CSV, `verify`) correspondem a comportamentos indeterminados no C4 ou a
  formatos não descritos; testá-los só para cobertura violaria a regra do pesquisador.
- Portanto a rodada `r1-baseline` é também a **rodada final**.

## Oráculos e Z3

- Inventário completo: `experimento/inventario-oraculo.md`; dados: `experimento/oraculo.json`.
- 82 casos: 45 DETERMINADOS (C4-D01..D45) e 37 INDETERMINADOS (C4-I01..I37).

| Consulta | Resultado | Uso |
|---|---|---|
| Q01-E1..E4 | Resultado de cada combinação (E1: 1 V de 8; E2: 1 F de 4; E3, E4: 8 linhas) | D01–D05 |
| Q02 | 2 linhas de E4 violam `not p or q` | D16–D17 |
| Q03-REQ-001/002 | Par existe nas leituras A e B (sat/sat) | D24–D25 |
| Q03-REQ-003 | pedal_pressionado: A = unsat, B = sat | justifica I18/I19 |
| Q04-T1..T4 | Guarda: T1 V, T2 F, T3 V, T4 F (esperado T) | D38–D42 |
| Q05-vm/tis/npp | 5/21/152, 17/69/268, 11/29/76 conferem; unsat 4/4/1; sat 148/264/75 | D27–D35; justifica I09 |
| Q06 | 2^20 = 1048576; pares de x01 = 524287 > 1000 | D44–D45 |
| Q07 | Par de causa única para p, q, r em `(p and q) or r` | D11–D13 |

`sat`/`unsat` dizem respeito às fórmulas; não provam a fidelidade da tradução do texto degradado.

## Hashes

| Artefato | SHA-256 |
|---|---|
| Manifesto do oráculo `experimento/congelamento-oraculo.sha256` | `3c682e1494feee4ac07583d12a9536394be9c5af70a1b44fb0ed92b63e08a9ea` |
| `experimento/oraculo.json` | `cdec152cc05f01156765e5e9da3d3fc7ea6a85e5a2dc5f0d73cf119154680cd8` |
| Manifesto da suíte `suite/congelamento-suite-r1.sha256` | `8d980ed229f39a637a3330722c57f435ff549cf73ef8abb6624a63e89b6d9563` |
| `suite/runner.py` | `7328cff17bc93316533a70b1008d677010cf084740e90c881045b47d2c09b24e` |
| `suite/cobertura.sh` | `9780babe88e3cb2330ade522d9ecc86fe8342167da284f1f8fed7d3f461d3e9a` |
| `experimento/entradas/erro-sintaxe.mcdc` | `93b2fbe1af08863fe11ef889723d7daa8f5f1ca156035519d00e388c17347015` |
| Entradas de `exemplos/` | `experimento/entradas-exemplos.sha256` |
| Classes compiladas (73 arquivos) | `experimento/build/classes.sha256` |
| Dados da rodada | `resultados/r1-baseline.sha256` |

## Métricas

Unidade de contagem: caso do oráculo (ID estável). Ferramenta: JaCoCo 0.8.16. Escopo: todas as classes de produção
de `mcdc-core`, `mcdc-requirements`, `mcdc-z3` e `mcdc-cli` (JaCoCo analisou 69 classes a partir de 73 arquivos
`.class`; o motivo da diferença não foi verificado). Excluídos: harness, Jackson, JDK. Sem análise de mutação.

### Rodada `r1-baseline` (= resultado final)

| Métrica | Resultado |
|---|---|
| Branch Coverage | **500 / 1296 = 38,58%** |
| Testes aprovados | **44** |
| Testes falhos | **1** |
| Testes indeterminados | **37** (não executados; não afetam a cobertura) |

Erros técnicos, casos inválidos e não avaliados: 0.

Cobertura por módulo (somando os pacotes):

| Módulo | Branches cobertos / total |
|---|---|
| `mcdc-core` (core, core.model, core.mutation) | 277 / 411 |
| `mcdc-requirements` | 114 / 162 |
| `mcdc-z3` | 0 / 386 |
| `mcdc-cli` | 109 / 337 |
| **Total** | **500 / 1296** |

Não se alega cobertura máxima global.

## Evidências e divergências

- Resultado por caso: `avaliacao/resultados-por-caso.md`; dados brutos: `resultados/r1-baseline/` (stdout/stderr por
  execução, `resultados.json`, `jacoco.exec`, CSV, XML, HTML).
- **Divergência (FALHOU) — C4-D26.** Fonte: "InputEdgeCasesTest: [...] núemro linha  erro" e
  "RequirementsFileTest: [...] erro  sintaxe requisito". Expectativa: recusa com erro que mencione a linha 3.
  Observado: recusa (exit 1) com `Erro: REQ-B: Faltou fechar parêntese`, que identifica o requisito, mas não o número
  da linha. A falha é preservada. Ressalva: a frase da fonte não diz a qual entrada se aplica o número da linha; o
  oráculo o aplicou a toda leitura de entradas (decisão congelada), e essa leitura do texto degradado faz parte da
  divergência.
- Os demais 44 casos determinados passaram, inclusive os números da tabela de regressão (requisitos, condições e
  combinações dos três sistemas), a detecção do T4 com esperado errado e os limites de 20 entradas e de 1000 pares
  (x01 com `pairsTruncated`).
- Códigos de saída observados (não julgados): 0 nas análises completas, 1 nas recusas, 2 em X10, X13 e X16
  (decisões sem cobertura completa).

## Como a qualidade da documentação C4 afetou o oráculo

- **Clareza baixa (degradação textual).** A fonte começa no meio de uma tabela; não tem lista de opções, descrição
  dos formatos texto/JSON nem dos códigos de saída. Palavras curtas sumiram, inclusive o identificador `A` em todos os
  exemplos e em MinimalSuiteTest. Consequências: os exemplos literais (I01–I06) e as expectativas numéricas mais
  concretas da fonte ("4 testes", "5 em vez de 6") ficaram sem entrada válida; códigos de saída (I23), precedência
  (I36), comportamento acima dos limites (I24) e resultados de leitura inválida (I26, I27) ficaram omitidos. Opções com
  grafia corrompida (`--te`, `chsseck`, `- relatorio.json`) só puderam ser invocadas depois de ler o código, e `-o`
  ficou indeterminado (I31).
- **Consistência baixa (parágrafos contraditórios).** Sete conflitos atingem o núcleo do comportamento: impossíveis
  sat x unsat (I09), critério do par (I18), minimalidade gulosa x `--exact` (I05, I16, I17, I34), redundante x
  bloqueada (I19, I20), arquitetura e limite de tempo do Z3 (I21, I22), conteúdo de `csv`/`truth-csv` (I07, I08,
  I33) e garantia de parênteses na mutação (I30). O conflito sat/unsat se declara prevalente, mas o Z3 mostrou que só
  a leitura original reproduz os números medidos da própria fonte (4/4/1 contra 148/264/75); como o texto não diz o
  que prevalece sobre esses números, todo o comportamento do Z3 (`--z3`, `--boundary`, `--direct`, `--exact`,
  `verify`) ficou sem expectativa. Esse é o principal motivo para `mcdc-z3` ter 0% de branches cobertos e para
  `mcdc-cli` ter cobertura baixa (relatório de verify, CSV e texto não exercitados).
- **O que ficou determinado.** Regras que sobreviveram ao ruído e não estavam em conflito: 2^n combinações, linha 0
  toda verdadeira, aparições como condições `#1/#2`, variante padrão, relação causa única ⊆ mascaramento, restrição
  manual, recusa de expressões inválidas, leitura de `.mcdc`/JSON NAT2TEST, números de regressão independentes do Z3,
  JSON válido e rastreável, `check` (esperado errado e pares faltando), tipos de mutação e limites de tamanho. Alguns
  casos só ficaram determinados porque o Z3 mostrou que as duas leituras de um conflito levam ao mesmo resultado
  (D12, D13, D24, D25, D40–D41).
- **Efeito na suíte.** Com 45% dos casos indeterminados e a exclusão dos indeterminados da cobertura, a suíte
  alcança só o caminho booleano sem Z3. A divergência encontrada (D26) depende de uma frase degradada, o que mostra
  que, sob baixa clareza, até expectativas determinadas trazem incerteza de interpretação.

## Limitações

- Autorrevisão; sem revisor independente.
- A tradução do texto degradado para fórmulas e expectativas é interpretação; o Z3 só verifica as fórmulas.
- Decisões de análise (não reconstruir operandos, tratar a regra sat/unsat como conflito não resolvido, aceitar
  `elos/requisitos.mcdc` como `exemplos/requisitos.mcdc`) influenciam fortemente as contagens; outra leitura
  igualmente defensável poderia mudar a proporção entre determinados e indeterminados.
- Uma única rodada; não houve repetição para medir variação do modelo.
- Perda menor de isolamento já descrita (dois arquivos de entrada não citados exibidos).
- A cobertura depende da compilação com `javac` fora do Maven (mesmas fontes do commit; recursos copiados).
