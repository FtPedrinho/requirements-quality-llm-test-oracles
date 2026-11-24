# Relatório da execução — condição C2

Segue `experimentacao-pesquisa/protocolo/modelo-relatorio.md`. Não usa resultados de
outras condições.

## Identificação e fontes

- **Condição:** C2 (pretendido pelo protocolo: clareza baixa, consistência alta; não se
  presume que o nível foi atingido).
- **Fonte normativa exclusiva:** `experimentacao-pesquisa/experimentacao-2/documentation/tool-readme-C2.md`,
  SHA-256 `61C4062B5FC6B4F364F40465B0E017C80E0FA0C5433412EB2E925C545F6EFBE1`, conferido antes da leitura.
- **Prompt:** `experimentacao-pesquisa/prompts/geracao-de-oraculos-v3.md`
  (SHA-256 `c10078b5…866d6d`, valor completo em `experimento/congelamento/oraculo.sha256`).
- **Modelo:** Claude Opus 5.5 (`claude-opus-5-5`), no Claude Code (app desktop), sessão
  iniciada por outra sessão com a tarefa da condição C2. Temperatura e demais parâmetros
  de amostragem: não informado.
- **Contexto e isolamento:** foram lidos apenas o README e os documentos de protocolo,
  o prompt, a fonte C2, os arquivos de entrada de `exemplos/` (como entrada) e, após o
  congelamento, o código do SUT. Não foram abertos `claude-opus-5.5-resultados/C0/`, `C1/`,
  `gpt-6.1-terra-resultados/`, `research/`, `relatorios/`, `exemplos/saidas/`, as outras
  `experimentacao-*`, `experimentacao-pesquisa/experimentos/`, nem o histórico git
  desses caminhos. A pasta de notas da sessão-mãe contém um arquivo `C1-execucao.md`;
  apenas o nome apareceu numa listagem e o arquivo **não foi lido**. A tarefa recebida
  mencionava, como notas de ambiente, ferramentas e caminhos (Java, Z3, JaCoCo, Jackson,
  codificação do stdout) sem resultados. Isso não demonstra ausência de influência: o
  modelo pode ter conhecimento prévio genérico sobre MC/DC e sobre ferramentas parecidas.
- **Commit de referência:** `ed7d2e00170e3e2c28201bf63e1b51a24a1bfe81` (árvore limpa).
- **Ambiente:** Windows 11; Java 21.0.3 (javac e JVM); Python 3.13.5 (harness);
  Z3 5.4.1 independente (`C:/Users/User/AppData/Roaming/Python/bin/z3.exe`);
  JaCoCo 0.8.16 (agente e CLI). Maven não usado (offline); build por `javac`
  (`experimento/build/build.md`).

## Oráculos e Z3

- **Inventário:** 25 requisitos extraídos (R1–R25) com linhas da fonte, em
  `experimento/analise-oraculo.md`; casos com trecho literal, regra, expectativa,
  justificativa e consultas Z3 em `experimento/oraculo.json` e
  `experimento/inventario-casos.md`.
- **Baseline:** 90 casos, 75 determinados e 15 indeterminados. **Extensão r2:** 12 casos
  determinados (`experimento/extensao-r2/oraculo-extensao.json`).
- **Leitura da fonte degradada:** lacunas reconstruídas só quando outro trecho legível
  da própria fonte fixa a palavra (ex.: L139 "condição  par" → "sem par" por L39/L461);
  quando não, INDETERMINADO. Variante causa única entendida pelo nome (só a condição
  muda) e L491 (par de causa única vale no mascaramento). A ausência de par no
  mascaramento nunca foi derivada, porque a fonte não define o mascaramento.
- **Z3:** 5.4.1, consultas SMT-LIB geradas por parser próprio (`experimento/scripts/gerar_z3.py`),
  118 consultas `.smt2` (com as saídas `.out`) no baseline e 6 na extensão; nenhuma resposta `unknown`.
  Formalizado: viabilidade de cada combinação, pares de causa única (com e sem
  domínio/restrição), mínimo de suíte de causa única (`(<= soma k)` sat em k e unsat em
  k−1), fronteiras inteiras (101/100 e 51/50, únicas), valor das guardas nos testes do
  `check`, conflitos e lacunas. Testemunhas nas saídas `.out` (`get-value`, `get-model`).
  O Z3 reproduziu os números da fonte para VM (5/21/152/4, 0 conflitos), TIS
  (17/69/268/4, 3 conflitos) e NPP (11/29/76/1, 1 conflito). Limite: `sat`/`unsat`
  valem para as fórmulas e não provam fidelidade da tradução.
- **Hashes e datas:** oráculo, análise, entradas, scripts e evidências Z3 congelados em
  `experimento/congelamento/oraculo.sha256` (2026-11-24 11:07:01 -0300, antes de ler ou
  executar o SUT); `oraculo.json` = `fdd8670a…00e9e138`. Suíte r1 congelada em
  `suite-r1-baseline.sha256` (11:11:00), extensão em `extensao-r2.sha256` (11:17:14).
  Os próprios manifestos têm hash em `*.sha256.sha256`.
- **Revisão:** autorrevisão do texto–fórmula, sem revisor independente.

## Métricas

Unidade de contagem: **caso** = uma invocação da CLI com ID estável (com, quando
necessário, uma observação auxiliar `--format json` da mesma fonte e opções, que não conta
como outro caso). PASSOU = todas as asserções da expectativa satisfeitas; FALHOU = alguma
contrariada; INDETERMINADO = sem expectativa documental única (executado só como
diagnóstico).

Branch Coverage: JaCoCo 0.8.16, agente na JVM de cada invocação; denominador = todas as
classes de produção dos 4 módulos (`--classfiles` de `mcdc-core`, `mcdc-requirements`,
`mcdc-z3` e `mcdc-cli` compilados, 73 arquivos `.class`, 69 classes com código no
relatório; incluídas as classes de mutação e as não carregadas). Excluídos: harness
Python e bibliotecas (Jackson, JDK).

**Regra de cobertura:** só a execução dos casos determinados conta para a Branch
Coverage; a execução diagnóstica dos casos indeterminados fica fora. Como r1 e r2
gravaram todos os casos num único `jacoco.exec`, as rodadas `r3-determinados-baseline`
(75 casos) e `r4-determinados-extensao` (12 casos) reexecutaram só os casos
determinados, com o mesmo runner, oráculos e entradas (manifesto
`experimento/congelamento/rodadas-r3-r4-determinados.sha256`). Os resultados por caso de
r3/r4 são idênticos aos de r1/r2.

| Métrica | Baseline (r3) | Extensão (r4) | Acumulado (r3+r4) |
|---|---|---|---|
| Branch Coverage (só determinados) | 1068 / 1296 = **82,41%** | 901 / 1296 = 69,52% | 1091 / 1296 = **84,18%** |
| Testes aprovados | **75** | 12 | **87** |
| Testes falhos | **0** | 0 | **0** |
| Testes indeterminados | **15** | 0 | **15** |

Registro preservado, não oficial: r1 e r2 com os indeterminados executados mediram
1076/1296 (83,02%) e, no acumulado r1+r2, 1099/1296 (84,80%). Os indeterminados
acrescentavam 8 branches ao baseline e ao acumulado.

Outras informações operacionais (não são métricas): erros técnicos 0; casos inválidos 0;
casos não avaliados 0. Cobertura de linhas no acumulado oficial: 1858/2001.

Branches por pacote no acumulado oficial (cobertos/total): cli 298/337; core 260/287;
core.model 28/60; core.mutation 57/64; requirements 127/162; z3 321/386.
Não se alega cobertura máxima global: a extensão cobriu áreas documentadas localizadas
pela cobertura, sem busca exaustiva.

## Metodologia aplicada e o que mudou ao longo da execução

Sequência: fonte → inventário → Z3 → oráculo congelado → build e leitura da CLI → suíte
congelada → baseline → extensão congelada → execução → acumulado.

- **Antes do congelamento do oráculo:** uma consulta Z3 de fronteira (Q14) tinha erro de
  ordem; foi corrigida e todas as consultas foram regeradas. Durante a análise, itens
  que pareciam afirmáveis foram rebaixados a INDETERMINADO por falta de texto que os
  fixasse: mínimo de suíte no mascaramento, contagem de mutantes de uma expressão,
  código de saída do TIS e lacunas sem `--context`.
- **Depois do congelamento (sem mudar expectativas):** a leitura da CLI definiu a
  observação auxiliar com `--format json` e a correspondência entre campos JSON e
  termos da fonte (`INFEASIBLE` = bloqueada, `REDUNDANT` = redundante, `minimalSuite` =
  suíte). Isso é interpretação com o código à vista e está registrado como limitação.
- **Extensão r2:** o runner ganhou apenas as opções `--oraculo`, `--manifesto` e
  `--entradas`; a lógica das asserções é a do r1 (versões em `suite/versoes/`).
- **Regra de cobertura definida pelo pesquisador após as rodadas:** a cobertura gerada
  por casos indeterminados não conta. Foram feitas as rodadas r3/r4 só com os casos
  determinados; as rodadas r1/r2 ficaram preservadas.
- **Depois das rodadas:** para alinhar a documentação deste registro ao padrão das
  execuções anteriores, foram consultados apenas os nomes de arquivos e os títulos de
  seção dos READMEs e relatórios de `claude-opus-5.5-resultados/C0` e `C1`, sem ler o conteúdo.
  O oráculo, a suíte e os resultados do C2 já estavam concluídos.

## Discussão: efeito da baixa clareza sobre o oráculo

O resultado sem falhas não indica que a documentação de baixa clareza foi suficiente:

- **Efeito de seleção.** As lacunas do texto atingiram sobretudo a prosa; tabelas,
  números, opções e exemplos de código ficaram quase legíveis. O que ficou ilegível virou
  INDETERMINADO (15 de 90 no baseline, cerca de 17%). Os casos aprovados medem a parte que
  sobreviveu à degradação, justamente a mais estável (números de regressão que os testes
  da própria ferramenta travam).
- **Reconstrução pelo leitor.** Parte das expectativas dependeu de preencher lacunas
  com outro trecho do texto ("condição  par" = sem par; causa única pelo nome;
  `--constraint` como exclusão de combinações; inteiros em expressão direta). Outro
  leitor, humano ou LLM, pode reconstruir de outra forma, e conhecimento prévio sobre
  MC/DC pode ter ajudado a acertar; a ausência dessa influência não pode ser demonstrada.
- **Comportamentos sem oráculo revelados pelos diagnósticos:** `verify` sem `--context`
  não confere lacunas e termina com 0 (risco de falsa segurança); `A or B and C` é
  aceito sem aviso, com a precedência apagada no texto; `x > -y`, mais de 20 entradas sem
  Z3, mais de 30 no modo direto, `--boundary` sem `--z3`, ids repetidos e linha sem
  identificador terminam com código 1 sem que a fonte permita prever isso.
- **Consequência prática:** a baixa clareza não gerou divergências nesta execução, mas
  reduziu a parte verificável e deslocou o custo para interpretação e justificativa.
  Em contexto de certificação (DO-178C, citado pela fonte), a dependência da leitura de
  quem interpreta compromete a rastreabilidade entre requisito e teste.

## Evidências e limitações

- **Resultados por caso:** `avaliacao/resultados-por-caso.md`; detalhes completos
  (asserção, esperado, observado, comando) em `resultados/<rodada>/resultados.json`;
  stdout e stderr por caso em `resultados/<rodada>/casos/<ID>/`; arquivos gravados com
  `-o` em `resultados/<rodada>/arquivos-o/`; JaCoCo (`jacoco.exec`, CSV, XML, HTML) em
  cada rodada e no `acumulado/`.
- **Divergências:** nenhuma. Todas as expectativas determinadas foram satisfeitas pelo
  sistema, inclusive os números de regressão de VM/TIS/NPP, a suíte exata mínima,
  fronteiras, valores concretos (159 testes conferidos no TIS, 72 no NPP), REQ-003
  redundante, divergência de T4 no `check`, conflitos e lacuna do `verify`.
- **Indeterminados executados como diagnóstico** (sem julgamento): A11 precedência
  (aceita `A or B and C`, código 0); A15 `x > -y` (código 1); A18 21 entradas (código 1,
  limite 20); A21 31 entradas no modo direto (código 1); A34 exemplo `--exact` com
  `not A` (5 testes, código 0); A36 e A37 (código 0); F07 `check --format csv` (código 1);
  M05 linha sem id (código 1); J01 TIS "Completos" (código 2); J05 ids repetidos
  (código 1); Z04 `--boundary` sem `--z3` (código 1); V09 `verify` VM sem contexto
  (código 0); E01 arquivo ausente (código 1); E02 comando inexistente (código 1). Esses
  comportamentos não viraram expectativa.
- **Limitações:**
  - Interpretação da fonte degradada é do próprio modelo; algumas leituras (código 2 =
    "sem par"; restrição como exclusão de combinações; causa única pelo nome; tipos
    inteiros em expressão direta) são escolhas documentadas, não fatos do texto.
  - Asserções sobre conteúdo usam a saída JSON da CLI; a correspondência entre campos
    JSON e conceitos da fonte (ex.: `INFEASIBLE` → bloqueada, `REDUNDANT` → redundante,
    `minimalSuite` → suíte) foi estabelecida lendo o código da CLI depois do
    congelamento, só para saber onde está cada dado.
  - O avaliador de valores concretos e de resultado das guardas é o parser próprio
    congelado (recusa mistura de and/or sem parênteses).
  - Desempenho (tempos da fonte) não foi avaliado.
  - Revisão sem avaliador independente; sem repetição de rodadas para estimar variação.
  - Não houve análise de mutação (conforme protocolo); `--mutation` foi usado só como
    funcionalidade da ferramenta.
- **Comandos:** `suite/runner.py <rodada>` (r1) e `suite/runner.py r2-extensao --oraculo
  ../experimento/extensao-r2/oraculo-extensao.json --manifesto
  ../experimento/congelamento/extensao-r2.sha256 --entradas
  ../experimento/extensao-r2/entradas`; cobertura com `suite/cobertura.py`
  (acumulado: merge dos dois `jacoco.exec`). Cada invocação do SUT:
  `java -javaagent:org.jacoco.agent-0.8.16-runtime.jar=destfile=…,append=true,includes=io.github.rvdomingos.mcdc.* -Dstdout.encoding=UTF-8 -Dstderr.encoding=UTF-8 -cp <classpath.txt> io.github.rvdomingos.mcdc.cli.Main …`,
  com o Z3 no PATH só do processo quando a pré-condição do caso pede.
