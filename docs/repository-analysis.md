# Análise técnica abrangente do repositório

Este documento descreve tecnicamente o SUT e não define a metodologia experimental. Resultados de cobertura/mutação do produto ou de suas suítes internas não são resultados das novas suítes LLM. O protocolo ativo está em [experimentacao-pesquisa/](../experimentacao-pesquisa/).

## 1. Visão geral

O projeto original chama-se **Ferramenta MC/DC**. Sua finalidade é gerar suítes de testes de MC/DC (Modified Condition/Decision Coverage) a partir de expressões lógicas ou decisões, avaliar suítes existentes e verificar conflitos entre decisões escritas como requisitos.

Os principais casos de uso descritos no [README da ferramenta](README.md) são:

- geração de tabelas verdade e pares de independência;
- seleção gulosa ou exata de uma suíte mínima;
- identificação de condições redundantes ou bloqueadas por restrições;
- geração de valores concretos e testes de fronteira com Z3;
- avaliação de testes existentes;
- detecção de conflitos e lacunas entre requisitos;
- geração interna de mutantes de expressões para validar uma suíte.

O projeto usa JDK 21, Maven, Java 21, JUnit 5, Jackson, JaCoCo, PIT, Z3 e arquivos DFRS/NAT2TEST em JSON. Os artefatos originais incluem um PDF técnico, documentos `.mcdc`, JSON e CSV, além de relatórios HTML já gerados por JaCoCo e PIT.

## 2. Tecnologias e arquitetura

O projeto é Maven multi-módulo, definido em [pom.xml](../pom.xml):

| Módulo | Responsabilidade | Dependências principais |
|---|---|---|
| `mcdc-core` | Expressões, tabela verdade, pares de independência, seleção da suíte, avaliação de testes e mutantes de expressões | Apenas JUnit no build |
| `mcdc-requirements` | Parsing de expressões, arquivos `.mcdc`, JSON NAT2TEST e CSV de testes | `mcdc-core`, Jackson |
| `mcdc-z3` | Viabilidade, valores concretos, fronteiras, otimização exata e verificação de requisitos | `mcdc-core`, executável externo Z3 |
| `mcdc-cli` | Comandos `analyze`, `check` e `verify`, relatórios text/JSON/CSV | Os três módulos acima |

A entrada percorre `Nat2TestJsonReader` ou `RequirementsFile`, torna-se um `DecisionSet` e é convertida em expressões do núcleo. `Mcdc.analyze` monta a tabela verdade e os pares de independência em [Mcdc.java](../mcdc-core/src/main/java/io/github/rvdomingos/mcdc/core/Mcdc.java). `Z3RequirementsVerifier` usa uma chamada ao processo Z3 para comparar decisões e detectar conflitos em [Z3RequirementsVerifier.java](../mcdc-z3/src/main/java/io/github/rvdomingos/mcdc/z3/Z3RequirementsVerifier.java).

A configuração exige JDK 21 ou superior, Maven e, apenas para recursos específicos, o executável `z3` no `PATH`. O script [mcdc](../mcdc) usa os artefatos compilados e espera que o Maven tenha criado `mcdc-cli/target/classpath.txt`.

Arquivos relevantes:

- [setup.sh](../setup.sh): esqueleto histórico de criação do projeto; não deve ser executado sobre o repositório atual, pois termina com erro se módulos já existirem.
- [.gitignore](../.gitignore): exclui `target/`, IDEs e requisitos locais em `exemplos/pc-*`.
- [relatorios/](../relatorios/): relatórios HTML/XML/CSV já gerados.

## 3. Documentação de requisitos

### 3.1 Fontes examinadas

Existem quatro categorias de documentação funcional relevante:

1. Expressões manuais em [exemplos/requisitos.mcdc](../exemplos/requisitos.mcdc): 3 requisitos.
2. Decisões da máquina de café em [exemplos/decisoes.json](../exemplos/decisoes.json): 4 decisões.
3. Decisões da máquina de café em [exemplos/vm-decisoes.json](../exemplos/vm-decisoes.json): 5 requisitos e em [exemplos/vm-requisitos.mcdc](../exemplos/vm-requisitos.mcdc): a mesma área em formato textual.
4. Sistemas NAT2TEST em [exemplos/tis-decisoes.json](../exemplos/tis-decisoes.json) e [exemplos/npp-decisoes.json](../exemplos/npp-decisoes.json): 17 e 11 decisões, respectivamente.

Ao todo, os quatro JSON principais contêm 37 decisões; os arquivos `.mcdc` apresentam também versões derivadas ou simplificadas. O [README da ferramenta](README.md) menciona 33 requisitos de exemplo, mas os JSON atuais somam 37 decisões distintas entre os três sistemas, além do conjunto auxiliar em `decisoes.json`. A diferença não foi encontrada explicada por outra fonte e deve ser tratada como divergência documental, não corrigida.

Há ainda “Especificação Técnica - Ferramenta Dupla MC_DC (Requisitos e Código Java).pdf”. Não foi possível confirmar automaticamente seu conteúdo porque a extração de PDF não está disponível nas ferramentas desta análise. O arquivo foi registrado como fonte potencial não examinada.

### 3.2 Convenções e estilo

Os arquivos `.mcdc` usam `ID: expressão`; linhas iniciadas por `#` são comentários. Os identificadores são `REQ-001`, `REQ-002`, etc. ou `REQ001` nos arquivos da máquina de café.

Os JSON NAT2TEST registram:

- `system`;
- `inputs`, com `name`, `type` e possíveis `values`;
- `decisions`, com `id`, `requirement`, `text`, `guard`, `actions` e, em um caso auxiliar, `temporal`.

As ações são atribuições como `the_system_mode := choice`. Isso fornece pré-condições implícitas na guarda, eventos por variáveis `_antes`, ações esperadas e relações de estado.

### 3.3 Exemplos e candidatos à análise de qualidade

- **VM REQ002 e REQ003**, em [vm-decisoes.json](../exemplos/vm-decisoes.json), diferem apenas no limite do temporizador: `<= 30.0` implica `preparando fraco`; `> 30.0` implica `preparando forte`. A fronteira é clara, mas a semântica de arredondamento e valores intermediários não está explicitada.
- **TIS REQ002 a REQ004**, em [tis-decisoes.json](../exemplos/tis-decisoes.json), descrevem modos left, right e both com guardas semelhantes. São bons candidatos para variantes controladas de clareza.
- **NPP REQ009 a REQ011**, em [npp-decisoes.json](../exemplos/npp-decisoes.json), cobrem modos low, permitted e high e a variável `safety_injection_mode`. Potencialmente permitem investigar cobertura de estados e consistência.
- **REQ003** em [exemplos/requisitos.mcdc](../exemplos/requisitos.mcdc) possui `freio_acionado or (freio_acionado and pedal_pressionado)`, uma condição redundante observável na expressão. Isso é redundância lógica, não necessariamente uma inconsistência com outro requisito.

O texto de [vm-decisoes.json](../exemplos/vm-decisoes.json) usa nomes em inglês e termos como “weak/strong coffee”. O modelo é suficientemente detalhado para algumas guardas, mas não constitui um documento funcional único da aplicação original. Os três JSON representam exemplos importados ou derivados de sistemas NAT2TEST, não uma implementação de aplicação reunida no repositório.

## 4. Análise da implementação

A implementação não é uma aplicação de domínio separada. Ela implementa o analisador MC/DC: parsing, modelo de expressão, cálculo de verdade, diagnóstico, verificação com Z3 e interface de linha de comando.

Os módulos principais são:

- modelo lógico em `mcdc-core/src/main/java/io/github/rvdomingos/mcdc/core/model`;
- tabela verdade e condições em `TruthTable`, `Condition` e `DecisionAnalysis`;
- pares de independência em `IndependencePairs`;
- seleção de suíte em `MinimalSuite`;
- avaliação de suíte existente em `TestSetEvaluation`;
- mutantes de expressão em `core/mutation`;
- leitores em `mcdc-requirements`;
- integração Z3 em `mcdc-z3`;
- comandos e relatórios em `mcdc-cli`.

Regras relevantes observadas:

- cada ocorrência de uma entrada na expressão é contabilizada como condição distinta;
- são suportadas as variantes mascaramento e causa única;
- o motor pode recusar combinações impossíveis fornecidas pelo Z3;
- decisões acima de 12 entradas passam ao modo direto em `--z3`;
- o modo direto limita-se a 30 entradas;
- o Z3 é chamado como processo externo;
- o timeout por chamada é registrado no código como 60 segundos;
- o verificador detecta conflitos entre ações que escrevem a mesma variável com valores diferentes;
- o contexto opcional permite identificar situações sem nenhuma guarda ativa.

Não foi encontrada uma implementação de máquina de café, TIS ou NPP correspondente aos sistemas descritos nos JSON. Os JSON são entradas analíticas da ferramenta, não especificações ligadas a um módulo de negócio implementado no repositório.

## 5. Suíte de testes existente

A suíte usa JUnit 5 com Surefire e tem aproximadamente 167 métodos anotados com `@Test`, `@ParameterizedTest`, `@RepeatedTest` ou `@TestFactory`. O README registra 171 testes, uma diferença que não foi validada pela execução nesta etapa. A contagem documentada é de cobertura/relatórios históricos e não foi reproduzida por uma execução.

Os testes cobrem:

- parsing de expressões;
- arquivos `.mcdc`;
- leitura JSON NAT2TEST;
- leitura CSV;
- casos de fronteira;
- tabela verdade;
- pares de independência;
- escolha gulosa e exata;
- avaliação de suítes existentes;
- mutantes internos;
- integração Z3;
- comandos e formatos de relatório.

O relatório [exemplos/testes.csv](../exemplos/testes.csv) é um exemplo de teste externo à suíte JUnit. O CSV contém colunas `decision`, `test`, `input`, `value` e `expected_outcome`. O próprio comentário do arquivo declara que `T4` tem resultado esperado errado para demonstrar a detecção de divergência.

## 6. Rastreabilidade

Relacionamentos confirmados:

- requisito do JSON → `Decision` criada pelo leitor → guarda analisada pelo motor → casos gerados em saída CSV/JSON;
- arquivo `.mcdc` → `RequirementsFile` → `DecisionSet` → motor MC/DC;
- requisito do CSV → `TestCasesFile` → `TestSetEvaluation` → diagnóstico de cobertura;
- decisão com ações → `Z3RequirementsVerifier` → conflito entre ações.

Relacionamentos não confirmados:

- não existe evidência de implementação funcional dos sistemas VM, TIS e NPP;
- os requisitos de exemplo não estão ligados a classes de domínio homônimas;
- não foi encontrada uma matriz original requisito-teste;
- o PDF técnico não pôde ser associado a requisitos específicos nesta inspeção.

A matriz antiga de rastreabilidade dos exemplos de domínio foi arquivada e não é uma referência comportamental da metodologia atual. Consulte os [documentos e modelos de coleta](../experimentacao-pesquisa/).
