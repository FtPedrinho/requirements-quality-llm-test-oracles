# Relatório C3 — Claude Sonnet 5.5

## Identificação e fontes

- Condição **C3**; fonte normativa exclusiva `experimentacao-pesquisa/experimentacao-3/documentation/tool-readme-C3.md`, SHA-256 `F18B0821D79C7315486C13D5260FA2F6D6E9418EF03B86CDE58E66B91B7B87A3` (conferido antes da leitura).
- Prompt: `experimentacao-pesquisa/prompts/geracao-de-oraculos-v3.md`. Modelo: Claude Sonnet 5.5 (configuração além disso: não informado).
- Contexto/isolamento: a sessão recebeu do orquestrador a descrição da tarefa, as regras e o ambiente (sem resultados de outras condições). Não foram lidos `claude-opus-5.5-resultados`, `gpt-6.1-terra-resultados`, `C0`/`C1`/`C2`, notas compartilhadas, `contradictions.csv` nem o README de `experimentacao-3`. Perda de isolamento: nenhuma conhecida; cegamento não é alegado.
- Commit de referência do SUT: `50e795ea66e6f51b96548040e2bff38ec9fcc795`. Ambiente: Windows 11, Java 21.0.3, Python 3.13.5, pytest 9.0.2, Z3 5.4.1, JaCoCo 0.8.16. Sem Maven; sem recompilação (classes já existentes em `target/`).

## Oráculos e Z3

- 72 casos: **48 determinados** (`C3-D01…D48`) e **24 indeterminados** (`C3-I01…I24`). Detalhes em `../experimento/oraculo.json` e `../experimento/analise-oraculo.md`.
- O texto C3 contém contradições internas (condições por ocorrência × variável; Z3 obrigatório × opcional; códigos de saída; `unsat`/`sat`; critério de par; csv × truth-csv; redundante × bloqueada; limites de entradas; garantias de minimização e de parênteses; arquitetura do Z3; regras do build). Cada uma virou caso INDETERMINADO, sem desempate por código.
- Z3 independente 5.4.1: 122 consultas SMT-LIB (`../experimento/z3/`), todas com a resposta esperada da fórmula; nenhum `unknown`/timeout. Cada conflito textual foi formalizado (afirmações isoladas `sat`, conjunção `unsat`). O Z3 não prova a fidelidade da tradução.
- Revisão: **autorrevisão**. Hashes: `../experimento/congelamento/01-oraculo.sha256` (oráculo, análise, geradores, SMT/saídas Z3, congelados antes de ler o SUT), `02-suite.sha256` (suíte e entradas, antes de executar), `03-resultados-baseline.sha256`.

## Métricas

Unidade: um caso do oráculo = um teste (ID estável). Ferramenta de cobertura: JaCoCo 0.8.16 (agente na CLI real). Escopo: as 69 classes de produção dos 4 módulos (`mcdc-core`, `mcdc-requirements`, `mcdc-z3` via JARs; `mcdc-cli/target/classes`), incluindo classes não carregadas e de mutação; sem harness nem bibliotecas externas; sem análise de mutação do projeto.

| Métrica | Baseline | Extensões | Acumulado |
|---|---|---|---|
| Branch Coverage | 914 / 1296 = **70,52 %** | não houve | 914 / 1296 = 70,52 % |
| Testes aprovados | **47** | — | 47 |
| Testes falhos | **1** (`C3-D15`) | — | 1 |
| Testes indeterminados | **24** (registrados, não executados, fora da cobertura) | — | 24 |

Não houve rodada de extensão: nenhum defeito da suíte foi percebido antes da execução, e as demais situações documentadas já estavam cobertas por casos do baseline. Não se alega cobertura máxima.

## Falha preservada

- **C3-D15** — o texto diz (exemplo de `analyze -f exemplos/requisitos.mcdc`) “REQ-003 tem uma condição redundante”; o oráculo fixou **exatamente 1** condição sem par. O SUT reporta 2 (`freio_acionado#2` e `pedal_pressionado`). A leitura de “uma” como “exatamente uma” é uma escolha do oráculo (autorrevisão) e a expectativa não foi alterada. Divergência em relação à referência adotada.

## Evidências, desvios e limitações

- Resultados por caso: `resultados-por-caso.csv`. Brutos: `../resultados/rodada-01-baseline/` (`pytest-bruto.txt`, `junit.xml`, `jacoco.exec`, `jacoco.csv/xml`, `jacoco-html/`). Execução única, ~107 s.
- **Desvio** da orientação do orquestrador: o Z3 ficou no `PATH` em **todos** os casos (não só nos que o usam), porque o texto é contraditório sobre sua obrigatoriedade (`C3-I02`); só assim a expectativa dos casos determinados é única. Consequência: o comportamento sem Z3 não foi avaliado.
- Código de saída da CLI nunca foi afirmado (`C3-I03`). Formatos `csv`/`truth-csv` e o rótulo redundante/bloqueada não foram avaliados (`C3-I07`, `I11`).
- Regressões numéricas (VM/TIS/NPP) usam os valores da tabela do texto; o número de condições não foi afirmado (`C3-I01`). Todos coincidiram com o SUT.
- Alguns casos usam expectativas aplicadas por analogia (ex.: fronteira 50/51 de `speed > 50`), ou entradas próprias da suíte (`../suite/dados`).
- Comandos: `python -m pytest claude-sonnet-5.5-resultados/C3/suite -p no:cacheprovider -v --junitxml=…` com `JAVA_TOOL_OPTIONS=-javaagent:…jacocoagent…=destfile=…,append=true,includes=io.github.rvdomingos.*`; relatório com `org.jacoco.cli-0.8.16-nodeps.jar report --classfiles …`.
- O número de classes analisadas (69) e o total de branches (1296) coincidem com a tabela do texto C3 (desvios: 1296).
