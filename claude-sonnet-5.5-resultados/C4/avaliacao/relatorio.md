# Relatório C4 — Claude Sonnet 5.5

## Identificação e fontes

* Condição: C4. Fonte normativa: `experimentacao-pesquisa/experimentacao-4/tool-readme-C4.md`, SHA-256 `D6BC0A588CD9A7DF7F1F566573944FA5CB1707BBA676B4E9854CAD2CC5440FC2` (conferido integralmente antes da leitura; cópia em `documentacao/`).
* Prompt: `experimentacao-pesquisa/prompts/geracao-de-oraculos-v3.md`; protocolo: `protocolo/metodologia.md`, `protocolo/modelo-relatorio.md`. Critério estrito adotado por decisão do pesquisador.
* Modelo: Claude Sonnet 5.5 (configuração de esforço: não informado). Sessão iniciada por outra sessão do mesmo pesquisador.
* Commit de referência do SUT: `78311854f869b8c01524ccbfb8308de67c5a78b6` (HEAD de `main` no início).
* Ambiente: Windows 11; Java 21.0.3; Python 3.13.5; pytest 9.0.2; Z3 5.4.1 (standalone); JaCoCo 0.8.16. Sem Maven, sem recompilação (classes pré-compiladas em `target/`).

## Oráculos e Z3

* 78 casos: **42 DETERMINADOS** (D01–D42) e **36 INDETERMINADOS** (I01–I36) em `experimento/oraculo.json`; análise em `experimento/analise-oraculo.md`.
* Texto muito degradado (letras/palavras/identificadores suprimidos, início truncado) e com conflitos explícitos (truth-csv, sat/unsat, critério de par, guloso×exato, redundante×bloqueada, parênteses, Z3 externo×biblioteca, cobertura, nota de mutação, regra global de build). Nenhum foi resolvido por suposição.
* Z3 5.4.1 independente: 12 arquivos `.smt2`, 56 verificações, todas conforme o esperado pelo autor; nenhuma `unknown`/timeout. Cada conflito: afirmações `sat` isoladas, `unsat` na conjunção. `sat`/`unsat` não provam fidelidade da tradução.
* Hashes: `experimento/congelamento/01-oraculo.sha256` (antes de ler o SUT), `02-suite.sha256`, `03-resultados-baseline.sha256`. **Revisão: autorrevisão**, sem revisor independente.

## Métricas (baseline = acumulado; não houve extensão)

| Métrica | Resultado |
|---|---|
| Branch Coverage | **626 / 1296 = 48,30 %** |
| Testes aprovados | **42** |
| Testes falhos | **0** |
| Testes indeterminados | **36** (registrados, não executados) |

Unidade de contagem: um caso do oráculo = um teste. Ferramenta: JaCoCo 0.8.16 (agente com `includes=io.github.rvdomingos.*`, `append=true`), relatório sobre os JARs de `mcdc-core`, `mcdc-requirements`, `mcdc-z3` e `mcdc-cli/target/classes`; **69 classes** de produção analisadas (inclui classes não carregadas e de mutação); sem harness nem bibliotecas externas; sem análise de mutação. Os casos INDETERMINADOS não entram na cobertura.

## Evidências

* Resultados por caso: `resultados-por-caso.csv`. JUnit, JaCoCo (`.exec`, csv, xml, html) e saídas brutas da CLI em `../resultados/rodada-01-baseline/`.
* Execução: uma única vez (≈ 49 s de pytest), a partir da raiz, `-p no:cacheprovider`, `PYTHONDONTWRITEBYTECODE=1`, `JAVA_TOOL_OPTIONS` com o agente JaCoCo. Z3 no `PATH`.
* Nenhuma falha de infraestrutura, caso inválido ou erro técnico no baseline.

## Desvios, limitações e perdas de isolamento

* **Todos os 42 determinados passaram**; isso mede aderência a um conjunto de expectativas conservadoras, não qualidade geral da documentação. A cobertura baixa (48,3 %) reflete que o texto C4 só sustentou verificações numéricas/estruturais; o restante foi indeterminado pelo critério estrito.
* Sondagem prévia: antes de congelar a suíte (mas depois do congelamento do oráculo) executei a CLI algumas vezes (expressão de 20 entradas, `vm-decisoes.json` com `--mutation`, expressão `speed...`, expressão inválida) e li `Main.java` e o início de `exemplos/saidas/vm-relatorio.json`/`npp-verificacao.json` para saber invocar e mapear campos JSON. Essas observações não alteraram nenhuma expectativa, mas houve contato com saídas do SUT antes do baseline.
* O Z3 ficou no `PATH` em todos os casos, desvio frente ao texto contraditório (I08).
* Casos D35–D42 verificam estrutura do repositório (módulos, `pom.xml`, caminhos), não comportamento da CLI; D35–D42 e D22–D34 usam medições (campos JSON) escolhidas após inspeção, e identificadores `x01…xNN` escolhidos por mim, pois o texto não define identificadores.
* Antes da suíte, expressões com um token suprimido não foram completadas (I13–I17), o que reduz o escopo de teste das funcionalidades mais centrais (mascaramento, causa única, `--exact`, `--constraint`).
* Não declaro cegamento: o modelo conhece a existência da ferramenta e do repositório; as pastas C0–C3 e outras LLMs não foram lidas. Revisão do oráculo é própria. Não afirmo cobertura máxima.
