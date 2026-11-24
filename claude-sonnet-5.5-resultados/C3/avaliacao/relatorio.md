# Relatório C3 — Claude Sonnet 5.5 (segunda tentativa)

## Identificação e fontes

- Condição **C3**; fonte `experimentacao-pesquisa/experimentacao-3/documentation/tool-readme-C3.md`, SHA-256 `F18B0821D79C7315486C13D5260FA2F6D6E9418EF03B86CDE58E66B91B7B87A3` (conferido).
- Prompt `geracao-de-oraculos-v3.md`; modelo Claude Sonnet 5.5 (demais configurações: não informado).
- Commit de referência do SUT: `50e795ea66e6f51b96548040e2bff38ec9fcc795`. Windows 11, Java 21.0.3, Python 3.13.5, pytest 9.0.2, Z3 5.4.1, JaCoCo 0.8.16; sem Maven, sem recompilação.
- **Perda de isolamento:** esta é a segunda execução na mesma sessão; o autor já conhecia a saída do SUT e os resultados da tentativa 1 (preservada em `../tentativa-1/`, incluindo uma falha). Nenhuma outra condição/LLM foi lida (`C0`–`C2`, Opus, GPT, notas, `contradictions.csv`). Cegamento não é alegado.
- Por que refeita: o pesquisador determinou adotar a documentação como verdade, usar o sistema só como entrada para criar a suíte, não assumir ideias e registrar INDETERMINADO sem receio.

## Oráculos e Z3

- 72 casos: **40 determinados** (`C3-D01…D40`) e **32 indeterminados** (`C3-I01…I32`). Em relação à tentativa 1, oito casos foram rebaixados (I25–I32) e expectativas determinadas foram enxugadas (ver `../experimento/analise-oraculo.md`).
- Contradições internas do texto C3 (contagem de condições, Z3 obrigatório×opcional, códigos de saída, `unsat`/`sat`, critério de par, `csv`/`truth-csv`, redundante×bloqueada, limites de entradas, garantias de minimização e de parênteses, arquitetura do Z3, regras de build) geraram casos INDETERMINADOS, sem desempate pelo código.
- Z3 5.4.1 independente: 122 consultas SMT-LIB, todas com a resposta esperada; nenhum `unknown`/timeout. Revisão: **autorrevisão**.
- Hashes: `../experimento/congelamento/01-oraculo.sha256` (antes de ler o SUT na tentativa 1; nesta, o oráculo foi congelado antes de criar a suíte), `02-suite.sha256` (antes de executar), `03-resultados-baseline.sha256`.

## Métricas

Unidade: um caso do oráculo = um teste (ID estável). Cobertura: JaCoCo 0.8.16 sobre a execução da suíte com o agente na CLI real; escopo: 69 classes de produção dos 4 módulos (incluindo não carregadas e de mutação), sem harness nem bibliotecas externas; sem análise de mutação do projeto.

| Métrica | Baseline | Extensões | Acumulado |
|---|---|---|---|
| Branch Coverage | 835 / 1296 = **64,43 %** | não houve | 835 / 1296 = 64,43 % |
| Testes aprovados | **40** | — | 40 |
| Testes falhos | **0** | — | 0 |
| Testes indeterminados | **32** (não executados, fora da cobertura) | — | 32 |

Não houve rodada de extensão. Não se alega cobertura máxima; a cobertura menor que na tentativa 1 (70,52 %) reflete o oráculo mais estrito (menos casos executáveis), não melhora ou piora do SUT.

## Evidências, desvios e limitações

- Por caso: `resultados-por-caso.csv`. Brutos: `../resultados/rodada-01-baseline/` (`pytest-bruto.txt`, `junit.xml`, `jacoco.exec/csv/xml/html`). Execução única, ~86 s.
- **Resultado 0 falhas é condicionado ao rigor do oráculo**: casos que poderiam falhar (p. ex. REQ-003 com uma condição redundante, que na tentativa 1 divergiu do SUT) foram classificados INDETERMINADO por ambiguidade documental; esse rebaixamento ocorreu depois de conhecer o resultado da tentativa 1.
- Z3 no `PATH` em todos os casos (não só nos que o usam) porque o texto é contraditório sobre sua obrigatoriedade (I02); o comportamento sem Z3 não foi avaliado.
- Código de saída nunca afirmado (I03); `csv`/`truth-csv`, rótulos redundante/bloqueada, modo direto, mensagens de erro e limites além de 20 entradas não foram avaliados.
- Valores de regressão (VM/TIS/NPP) vêm da tabela do texto; o número de condições não é afirmado (I01).
- Comandos: `python -m pytest claude-sonnet-5.5-resultados/C3/suite -p no:cacheprovider -v --junitxml=…` com `JAVA_TOOL_OPTIONS=-javaagent:…jacocoagent…=destfile=…,append=true,includes=io.github.rvdomingos.*`; relatório com `org.jacoco.cli-0.8.16-nodeps.jar report --classfiles …`.
