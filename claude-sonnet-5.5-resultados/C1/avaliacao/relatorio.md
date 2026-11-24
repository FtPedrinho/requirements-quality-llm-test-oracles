# Resultados do experimento C1 — Claude Sonnet 5.5

## Identificação e fontes

- **Condição**: C1. **Fonte normativa exclusiva**: `experimentacao-pesquisa/experimentacao-1/documentation/tool-readme-C1.md`.
- **SHA-256 verificado antes da leitura**: `91981FA0181E5CC1BC5A67DAAFC965BB82D6F8EB0A6D47EB58CE291A3EF5D33B` (coincide).
- **Prompt**: `experimentacao-pesquisa/prompts/geracao-de-oraculos-v3.md`; protocolo e modelo de relatório da mesma pasta.
- **Modelo**: Claude Sonnet 5.5 (`claude-sonnet-5-5`), configuração de raciocínio/temperatura: não informado.
- **Commit de referência do repositório (antes deste experimento)**: `0ddda45`.
- **Isolamento**: não foram lidas as pastas `claude-opus-5.5-resultados`, `gpt-6.1-terra-resultados` nem `claude-sonnet-5.5-resultados/C0`, nem
  resultados de outras condições. O contexto recebido incluiu uma descrição da tarefa por outra sessão (que menciona a existência do
  experimento C0, sem resultados). Não se demonstra cegamento além disso. O repositório contém, no disco, as pastas de outras execuções (não abertas).
- **Ambiente**: Windows 11; Java 21.0.3; Python 3.13.5 + pytest 9.0.2; Z3 5.4.1 (`z3.exe`); JaCoCo 0.8.16 (agente e CLI).
  A CLI foi chamada por `java -cp "<mcdc-cli/target/classes>;<classpath.txt>" io.github.rvdomingos.mcdc.cli.Main` (o script `./mcdc` não serve no Windows). Sem Maven, sem recompilação.

## Oráculo e Z3

- 72 casos: **57 DETERMINADOS** e **15 INDETERMINADOS** (`../experimento/oraculo.json`, `../experimento/analise-oraculo.md`).
- Z3 independente do `mcdc-z3`: 52 consultas SMT-LIB (`../experimento/z3/smt/*.smt2` e `.out`) geradas por `experimento/z3/gerar_smt.py`
  (existência de pares de causa única, suítes mínimas, tabelas-verdade, relações entre predicados, fronteiras, enum, sobreposição/lacuna de guardas, avaliação dos testes de `check`).
  Nenhuma resposta `unknown`/timeout. Z3 não prova fidelidade texto→fórmula.
- Tensão registrada: C1-S07 (paridade de 3 entradas = 8 testes, literal do texto) × Z3 por entrada = 4; mantido o valor documental (granularidade por ocorrência).
- **Revisão: autorrevisão** (sem revisor independente). Hashes: `../experimento/congelamento/01-oraculo.sha256` (antes de ler o SUT),
  `02-suite.sha256` (antes do baseline), `03-extensao.sha256` (antes da extensão).
- Indeterminados (não executados, decisão do pesquisador): I01–I15 — ver motivos no oráculo.

## Métricas

Unidade de contagem: **um caso do oráculo = um teste**. Cobertura: JaCoCo 0.8.16, escopo = todas as classes de produção dos 4 módulos
(JARs `mcdc-core`, `mcdc-requirements`, `mcdc-z3` + `mcdc-cli/target/classes`; 69 classes, inclusive não carregadas e de mutação),
sem harness (pytest) nem bibliotecas externas (Jackson); sem análise de mutação do código.

| Métrica | Baseline | Acumulado (baseline + extensão E1) |
|---|---|---|
| **Branch Coverage** | **982 / 1296 = 75,77 %** | **982 / 1296 = 75,77 %** |
| Testes aprovados | 56 | 57 |
| Testes falhos | 0 | 0 |
| Testes indeterminados | 15 (não executados) | 15 (não executados) |

Informação operacional (fora das métricas): no baseline 1 teste foi **inválido por defeito da suíte** (C1-D02: faltou `--format json` na invocação,
a extração de métricas leu texto em vez de JSON; registrado como FALHOU no CSV bruto do baseline, mas não é divergência semântica e não entra na contagem de falhos).
A extensão E1 reexecutou o mesmo caso com a opção corrigida e a mesma expectativa (26 testes): **passou**. Erros técnicos de infraestrutura: 0.
Linhas (informativo): 1661 / 1984 em ambos. A extensão não alterou o conjunto de branches cobertos.

Cobertura por pacote (baseline, branches cobertos/total): core 247/287, core.model 20/60, core.mutation 57/64, requirements 122/162, z3 278/386, cli 258/337.

## Evidências

- Resultados por caso: `resultados-por-caso.csv` (nesta pasta, acumulado), `../resultados/rodada-01-baseline/resultados-por-caso-baseline.csv`, `../resultados/rodada-02-extensao/resultados-extensao.csv`; JUnit: `junit-baseline.xml` e `junit-extensao.xml` nas respectivas rodadas.
- Saídas brutas de cada invocação da CLI: `../resultados/rodada-01-baseline/bruto/`, `../resultados/rodada-02-extensao/bruto/`. JaCoCo: `jacoco-baseline.*` (rodada-01), `jacoco-extensao.exec` (rodada-02), `jacoco-acumulado.*` (`../resultados/acumulado/`); relatórios `*.csv` e `*-html/`.
- Comandos: ver `../experimento/README.md`.

## Avaliação

- **Todos os 56 casos determinados avaliados no baseline passaram** e o 57º (C1-D02) passou na extensão; nenhuma asserção foi ajustada. Isso diz que, para estes casos,
  o comportamento observado concorda com o texto C1 — inclusive as afirmações numéricas da tabela de regressão (VM/TIS/NPP), as 5×6 testes do exemplo `--exact`,
  os códigos de saída 0/1/2 e a paridade de 3 entradas = 8 testes.
- A suíte é majoritariamente caixa-preta e de contagens/códigos de saída: o oráculo deliberadamente não fixa campos de JSON, mensagens ou ordens que a documentação não define.
  Por isso a Branch Coverage (75,77 %) deixa de fora principalmente: ramos de erro/mensagens, ramos de `check`/`verify` além dos casos básicos,
  `core.model` (20/60) e partes do módulo z3 (limites, Z3 ausente/travado, saídas grandes) — não testáveis sem expectativa documental única (indeterminados I01–I15) ou com Z3 removido.
  Não se alega cobertura máxima.
- Os 15 indeterminados refletem lacunas reais da documentação C1: comportamento além dos limites (21/31 entradas), Z3 ausente, formatos `check/verify --format csv`,
  `_antes`, ids duplicados, colunas faltantes, mascaramento em condições repetidas, campos de formatos, `--boundary` sem `--z3`, `--constraint` com outras fontes, linha `.mcdc` sem ID,
  e a ambiguidade "lacunas só com contexto".

## Limitações e desvios

- Autorrevisão do oráculo; Z3 verifica fórmulas, não a tradução do texto.
- Definição de "causa única" adotada por leitura do termo (declarada em `oraculo.json`).
- Opções usadas para reproduzir a tabela de regressão (`--z3`; `--mutation` para mutantes) são suposição, pois o texto não as cita. Contagem de requisitos = requisitos distintos ligados às decisões (ou nº de decisões, se sem ID).
- Os arquivos `exemplos/*` (citados pela documentação, mas externos a ela) foram usados em A16, V05, V06, E01–E03, M01–M03, D01–D02.
- Defeito da suíte em C1-D02 corrigido via extensão E1 (congelada antes de executar), baseline preservado.
- Janela de execução do baseline: ~134 s, uma JVM por invocação com agente JaCoCo; classes soltas de `mcdc-core/target/classes` não foram analisadas (divergem dos JARs do classpath).
- Z3 foi colocado no `PATH` apenas nos casos que o usam. Modelo/hiperparâmetros de geração: não informado.
