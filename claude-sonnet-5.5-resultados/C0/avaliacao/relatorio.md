# Resultados e avaliação — Experimento C0 (Claude Sonnet 5.5)

Condição **C0**: documentação original (`tool-readme-original.md`, SHA-256 `72b827bd…a4995f8`, conferido antes da leitura).
Modelo: Claude Sonnet 5.5 (`claude-sonnet-5-5`). Prompt: `prompts/geracao-de-oraculos-v3.md`. Revisão do oráculo: **autorrevisão**.
Não foram lidos resultados, suítes ou oráculos de outras execuções (Opus, GPT) para produzir este experimento.

## Métricas

| Métrica | Resultado |
|---|---|
| **Branch Coverage** | **1001 / 1296 = 77,24 %** (JaCoCo 0.8.16; 69 classes de produção dos 4 módulos; baseline, sem extensões) |
| Testes aprovados (PASSOU) | **71** |
| Testes falhos (FALHOU) | **1** (C0-038) |
| Testes indeterminados | **22** (C0-I01 … C0-I22; não executados, não entram na cobertura) |

Unidade de contagem: **caso de teste** com ID estável (72 determinados + 22 indeterminados = 94 registrados).
Por decisão do pesquisador, os casos indeterminados **não foram executados** e portanto não contribuem para a cobertura.
Erros técnicos: **0**. Casos inválidos ou não avaliados: **0**.

### Cobertura por pacote (branches)

| Pacote | Cobertos / Total |
|---|---|
| core | 238 / 287 |
| core.model | 28 / 60 |
| core.mutation | 50 / 64 |
| requirements | 126 / 162 |
| z3 | 289 / 386 |
| cli | 270 / 337 |
| **Total** | **1001 / 1296** |

Denominador: todas as classes de produção dos quatro módulos (JARs de `mcdc-core`, `mcdc-requirements` e `mcdc-z3`, e `mcdc-cli/target/classes`), inclusive classes não carregadas e as de mutação; sem harness nem bibliotecas externas. Nenhuma análise de mutação foi executada.

## Resultado por grupo

| Grupo | Passou / Total |
|---|---|
| analyze/booleano | 6 / 6 |
| analyze/exato | 1 / 1 |
| analyze/diagnostico | 2 / 2 |
| analyze/restricao | 1 / 1 |
| analyze/precedencia | 2 / 2 |
| operadores | 17 / 17 |
| entrada-invalida | 4 / 4 |
| formatos | 5 / 6 |
| z3 | 8 / 8 |
| limites | 2 / 2 |
| arquivo-mcdc | 3 / 3 |
| arquivo-json | 2 / 2 |
| check | 8 / 8 |
| verify | 10 / 10 |

Detalhe por caso: `resultados-por-caso.csv` (nesta pasta); saída bruta: `../resultados/rodada-01-baseline/bruto/<ID>.json`; JaCoCo: `../resultados/rodada-01-baseline/cobertura/html/index.html`.

## Divergência preservada

**C0-038 — FALHOU.** Esperado (oráculo congelado): com `-o arquivo`, o relatório vai para o arquivo e a saída padrão fica vazia ("Grava o relatório no arquivo em vez de mostrar na tela"). Observado: o arquivo foi criado com o relatório, mas a saída padrão mostra a linha `Relatório gravado em <arquivo>`.

Avaliação: a divergência é real em relação à expectativa que adotei (stdout vazio), mas essa expectativa foi mais estrita que o texto. A documentação exige que o *relatório* não seja mostrado, e uma mensagem de confirmação não a contradiz claramente. É uma fragilidade do meu oráculo, não necessariamente um defeito do sistema. Mantive o FALHOU porque o protocolo proíbe ajustar a expectativa ao comportamento observado. Reclassificar é decisão do pesquisador.

## Avaliação qualitativa

- **Sistema vs. documentação C0:** nos 71 casos aprovados o comportamento concorda com o texto. Isso inclui os códigos de saída 0/1/2, a precedência de *e* sobre *ou*, `A#1`/`A#2`, os tamanhos de suíte (3, 4, 5 com `--exact`, 8 na paridade), o diagnóstico *redundante*/*bloqueada*, o `truth-csv` com 2ⁿ+1 linhas, os limites de 13/20/26 entradas, os conflitos dos três sistemas de exemplo e as lacunas só com `--context`. O Z3 independente confirmou separadamente os mínimos 3, 4, 5 e 8 citados na documentação.
- **Indeterminação documental:** 22 de 94 casos (23,4 %) não têm expectativa única. Concentram-se em comportamento acima dos limites (21 e 31 entradas), formato exato dos relatórios (JSON, mutação, aviso de Z3 ausente), entradas inválidas não enumeradas (fonte dupla, sem fonte, arquivo inexistente, `&`), o significado de "completo" nas tabelas dos sistemas de exemplo, causa única com entrada repetida e `--boundary` sem `--z3`.
- **Cobertura de 77,24 %:** o limite principal é o protocolo adotado (só casos determinados, só pela CLI, sem extensão), não a impossibilidade de cobrir. As maiores lacunas estão em `z3` (97 branches não cobertos), `cli` (67) e `core.model` (32). Não analisei quais branches são esses; a hipótese de que correspondem a erros do Z3, validações e formatos de relatório que a C0 não define **não foi verificada**.
- **O que não se pode afirmar:** não há prova de fidelidade texto→fórmula (autorrevisão); a cobertura não é máxima global; os resultados não permitem concluir equivalência com outros modelos ou condições.

## Limitações e desvios de execução

1. **Launcher:** o script `./mcdc` (feito para macOS/Linux, separa o classpath com `:`) não funciona no Windows. Invoquei o mesmo `Main` com o mesmo `classpath.txt` (separador `;`): `java -cp mcdc-cli/target/classes;<classpath.txt> io.github.rvdomingos.mcdc.cli.Main`. O SUT não foi alterado.
2. **Classes executadas:** core, requirements e z3 vieram dos JARs de `target/` (como no `classpath.txt`); `mcdc-cli` veio de `target/classes`. Não havia Maven e **nada foi recompilado**. As classes soltas de `mcdc-core/target/classes` diferem do JAR (JaCoCo acusou 2 classes divergentes), por isso o relatório usa os JARs. A procedência dos binários em relação ao commit `5d40d5a` não foi verificada (`não informado`).
3. **Código sem efeito na suíte congelada:** `conftest.py` tem uma expressão regular que deveria trocar JARs por `target/classes`, mas por erro de escape nunca casa. Não afetou os resultados (ver item 2) e não foi corrigida para preservar o hash congelado.
4. **Z3:** executável `z3` 5.4.1 do pacote `z3-solver`, colocado no `PATH` só para os casos `usa_z3`. Sem ele a CLI recusa `--z3` com saída 1. O módulo `mcdc-z3` chama esse mesmo executável.
5. **Isolamento:** ao listar diretórios vi os nomes das pastas de resultados de outras LLMs e, ao procurar um executável do Z3, caminhos de outras sessões. Não li nenhum conteúdo delas. Contexto recebido: conversa com o pesquisador, protocolo e documentação C0.
6. **Ambiente:** Windows 11, Java 21.0.3, Python 3.13.5, pytest 9.0.2, JaCoCo 0.8.16, Z3 5.4.1. O baseline levou 77,9 s.
7. **JaCoCo:** agente via `JAVA_TOOL_OPTIONS` com `append=true`; cada caso é uma JVM e o `.exec` acumula todas as invocações (inclusive a de referência do C0-039).
8. **Extensões:** nenhuma. O baseline é o resultado acumulado.
