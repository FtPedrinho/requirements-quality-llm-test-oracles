# Ferramenta MC/DC

Gera testes de **MC/DC** (*Modified Condition/Decision Coverage*) a partir de requisitos. Para cada requisito escrito como expressão lógica (a guarda), a ferramenta monta a tabela verdade, encontra os pares de independência de cada condição e escolhe um conjunto pequeno de testes que atinge MC/DC, dizendo qual par demonstra cada condição. Com o [Z3](https://github.com/Z3Prover/z3), também descarta as combinações impossíveis e dá valores concretos para cada teste.

Além de gerar testes, a ferramenta mede o MC/DC de testes que já existem, confere se os testes gerados pegam defeitos plantados (mutação) e verifica se os requisitos de um sistema se contradizem.

## Sumário

- [O que a ferramenta faz](#o-que-a-ferramenta-faz)
- [Instalação](#instalação)
- [Uso](#uso)
- [Formatos de entrada](#formatos-de-entrada)
- [Saídas](#saídas)
- [Exemplos](#exemplos)
- [Como funciona](#como-funciona)
- [Arquitetura](#arquitetura)
- [Qualidade e testes](#qualidade-e-testes)
- [Limites conhecidos](#limites-conhecidos)
- [Referências](#referências)

## O que a ferramenta faz

| Função | Comando | O que entrega |
|---|---|---|
| Gerar os testes | `mcdc analyze` | Tabela verdade, pares de independência, suíte de testes e o par que demonstra cada condição |
| Explicar o que não pode ser coberto | `mcdc analyze` | Para cada condição sem par: **redundante** (o requisito pode ser simplificado) ou **bloqueada** por combinações impossíveis |
| Dar valores concretos | `--z3` | Combinações impossíveis descartadas e valores reais para cada teste (`speed = 101`) |
| Testes de fronteira | `--z3 --boundary` | Variações no limite de cada comparação (`speed > 100` → 100 e 101) |
| Suíte exata | `--exact` | A menor suíte possível, escolhida pelo Z3 |
| Decisões grandes | `--direct` | Pares pedidos direto ao Z3, sem montar a tabela (até 30 entradas) |
| Validar a suíte | `--mutation` | Versões do requisito com um defeito cada (seis tipos) e quais os testes pegam |
| Avaliar testes existentes | `mcdc check` | Cobertura MC/DC de um conjunto de testes, o que falta e testes com resultado esperado errado |
| Revisar os requisitos entre si | `mcdc verify` | Conflitos (dois requisitos valem juntos e escrevem valores diferentes) e lacunas (nenhum requisito vale) |

As duas variantes de MC/DC são suportadas: **mascaramento** (padrão) e **causa única** (`--unique-cause`). Cada aparição de uma entrada na expressão conta como uma condição, como manda a DO-178C: em `(A and B) or (not A and C)` há 3 entradas e 4 condições (`A#1`, `B`, `A#2`, `C`).

## Instalação

Requer **JDK 21** ou mais novo e **Maven**. As opções com o Z3 precisam do executável `z3` no `PATH`.

```bash
brew install z3                                  # opcional: só para --z3, --exact, --direct e verify
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
mvn clean verify                                 # compila, roda os testes e gera a cobertura
./mcdc analyze "(A and B) or C"
```

O script `./mcdc` roda a ferramenta a partir das classes compiladas. Sem o Z3, tudo funciona, exceto as opções que dependem dele, que avisam quando ele não está instalado.

## Uso

```
mcdc analyze <fonte> [opções]                gera a suíte de testes MC/DC
mcdc check   <fonte> --tests <testes.csv>    mede o MC/DC de testes já existentes
mcdc verify  <fonte> [--context "<expr>"]    confere os requisitos entre si (usa o Z3)
```

**Fonte** (uma só):

| Fonte | Exemplo |
|---|---|
| Expressão direta | `"(A and B) or C"`, `'speed > 100 /\ mode = idle'` |
| Arquivo `.mcdc` | `-f exemplos/requisitos.mcdc` |
| JSON de decisões da NAT2TEST | `--json exemplos/vm-decisoes.json` |

**Opções:**

| Opção | Efeito |
|---|---|
| `--unique-cause` | Causa única em vez de mascaramento |
| `--constraint "<expr>"` | Restrição entre condições escrita à mão (só com expressão direta) |
| `--z3` | Usa o Z3 para descobrir combinações impossíveis e dar valores concretos; acima de 12 entradas, passa sozinho ao modo direto |
| `--exact` | Suíte exata: a menor possível, escolhida pelo Z3 |
| `--direct` | Pares pedidos direto ao Z3, sem montar a tabela (até 30 entradas) |
| `--boundary` | Com `--z3`, acrescenta variantes de fronteira |
| `--mutation` | Confere se a suíte pega versões do requisito com um defeito |
| `--context "<expr>"` | No `verify`: confere se, nessa situação, sempre alguma guarda vale |
| `--format <formato>` | `text` (padrão), `json`, `csv` (suíte) ou `truth-csv` (tabela verdade inteira); `check` e `verify` aceitam `text` e `json` |
| `-o <arquivo>` | Grava o relatório no arquivo em vez de mostrar na tela |

**Operadores** (use aspas simples quando a expressão tiver `\`):

| Operador | Formas aceitas |
|---|---|
| e | `and`, `&&`, `/\` |
| ou | `or`, `\|\|`, `\/` |
| não | `not`, `!` |
| comparação | `=`, `==`, `!=`, `<`, `<=`, `>`, `>=` |

**Código de saída:** `0` tudo certo; `1` entrada inválida; `2` alguma condição sem par (no `check`: alguma condição não demonstrada ou resultado esperado divergente; no `verify`: algum conflito ou lacuna).

## Formatos de entrada

**Arquivo `.mcdc`:** um requisito por linha, `ID: expressão`. Linhas com `#` são comentários.

```
REQ-001: (alarme_ativo and porta_aberta) or botao_emergencia
REQ-002: porta_fechada and not obstaculo
```

**JSON de decisões** (formato do Extractor da NAT2TEST): as variáveis com tipo e as decisões com a guarda e as ações. O valor do passo anterior é escrito com o sufixo `_antes`.

```json
{
  "system": "the_coffee_machine_system",
  "inputs": [
    { "name": "the_system_mode", "type": "enum", "values": ["idle", "choice"] },
    { "name": "the_coin_sensor", "type": "bool" }
  ],
  "decisions": [
    { "id": "vm#1", "requirement": "REQ-001",
      "guard": "the_system_mode = idle /\\ the_coin_sensor = true",
      "actions": ["the_system_mode := choice"] }
  ]
}
```

**Testes existentes** (para o `check`), em CSV: uma linha por teste e entrada, com o valor lógico (`T`/`F`) ou o valor concreto da variável. As colunas `decision` e `expected_outcome` são opcionais.

```
decision,test,input,value,expected_outcome
vm#1,T1,the_system_mode,idle,T
vm#1,T1,the_coin_sensor,true,T
```

## Saídas

| Formato | Conteúdo |
|---|---|
| `text` | Tabela verdade, pares, suíte, demonstração por condição, fronteiras, mutação e o motivo de cada problema |
| `json` | Resultado completo de cada decisão, ligado ao requisito de origem (formato de integração) |
| `csv` | A suíte: uma linha por teste e entrada, com o resultado esperado, o que o teste demonstra e os valores concretos |
| `truth-csv` | A tabela verdade inteira, com as combinações impossíveis marcadas |

Saídas já geradas para os sistemas de exemplo estão em [exemplos/saidas/](exemplos/saidas/).

## Exemplos

```bash
# mascaramento (padrão) ou causa única
./mcdc analyze "(A and B) or C"
./mcdc analyze "(A and B) or C" --unique-cause

# comparações e os operadores do DFRS
./mcdc analyze 'speed > 100 /\ mode = idle'

# entrada repetida: cada aparição é uma condição com par próprio (A#1, A#2)
./mcdc analyze "(A and B) or (not A and C)"

# restrição escrita à mão: A = speed > 100 implica B = speed > 50
./mcdc analyze "A or (B and C)" --constraint "not A or B"

# o Z3 descobre as combinações impossíveis, dá valores concretos e testes de fronteira
./mcdc analyze "speed > 100 or (speed > 50 and rain)" --z3 --boundary

# validação por mutação
./mcdc analyze "A and (B or C)" --mutation

# vários requisitos de um arquivo; REQ-003 tem uma condição redundante
./mcdc analyze -f exemplos/requisitos.mcdc

# requisitos de sistemas de exemplo da NAT2TEST: máquina de café (VM), pisca-pisca (TIS) e injeção de segurança (NPP)
./mcdc analyze --json exemplos/vm-decisoes.json --z3
./mcdc analyze --json exemplos/tis-decisoes.json --z3 --format json -o relatorio.json
./mcdc analyze --json exemplos/vm-decisoes.json --z3 --format truth-csv -o tabela.csv

# suíte exata (aqui, 5 testes em vez dos 6 da escolha gulosa)
./mcdc analyze "((E or D) and (not A or D)) or B" --exact

# modo direto: pares pedidos ao Z3 sem montar a tabela
./mcdc analyze --json exemplos/vm-decisoes.json --direct

# conflitos entre requisitos e lacunas numa situação
./mcdc verify --json exemplos/npp-decisoes.json
./mcdc verify --json exemplos/vm-decisoes.json --context 'the_system_mode = preparing_weak'

# avaliar testes que já existem
./mcdc check --json exemplos/decisoes.json --tests exemplos/testes.csv
```

## Como funciona

```
guarda do requisito
  → 1. tabela verdade: as 2ⁿ combinações das entradas e a saída de cada uma
  → 2. combinações impossíveis: cada linha vira uma consulta ao Z3 (sat / unsat); unsat sai da conta
  → 3. pares de independência: para cada condição, dois testes possíveis em que ela muda,
       a saída muda e ela decide nos dois (trocar só ela muda a saída)
  → 4. escolha da suíte: condições com menos pares primeiro; o par que acrescenta menos testes;
       no empate, causa única (ou, com --exact, a menor suíte pelo Z3)
  → 5. diagnóstico: condição sem par é redundante, se continua sem par com todas as combinações,
       ou bloqueada pelas combinações impossíveis
  → 6. mutação (opcional): seis tipos de defeito de Kapoor e Bowen (ORF, ENF, VNF, MVF, VRF, ASF);
       versões equivalentes ao original saem da conta
```

Nas guardas simples, a suíte tem **N + 1** testes, em vez das 2ᴺ combinações: nos 33 requisitos de exemplo, 146 testes no lugar de 496 combinações. O exponencial fica no cálculo da ferramenta (até 20 entradas com a tabela inteira, 12 com o Z3 linha a linha e 30 no modo direto), não no trabalho de quem executa os testes.

## Arquitetura

Projeto Maven com quatro módulos:

| Módulo | Conteúdo | Depende de |
|---|---|---|
| `mcdc-core` | Modelo da expressão e motor: tabela verdade, condições por aparição, pares, escolha da suíte, diagnóstico, avaliação de testes existentes e mutação | nada (sem bibliotecas externas) |
| `mcdc-requirements` | Leitor de expressões, arquivos `.mcdc`, JSON da NAT2TEST e CSV de testes | `mcdc-core`, Jackson |
| `mcdc-z3` | Conversa com o Z3 por SMT-LIB: viabilidade, valores concretos e de fronteira, suíte exata, modo direto e verificação entre requisitos | `mcdc-core` |
| `mcdc-cli` | Comandos `analyze`, `check` e `verify` e os relatórios em texto, JSON e CSV | os três acima |

O Z3 é chamado como processo externo, sem biblioteca nativa no build, com limite de 60 segundos por chamada.

## Qualidade e testes

### Notas atuais

Medidas em 17/11/2026 com o [JaCoCo](https://www.jacoco.org/) (cobertura de código) e o [PIT](https://pitest.org/) (mutação do código), ferramentas gratuitas que rodam pelo Maven.

| Módulo | Testes | Linhas cobertas | Desvios cobertos | Nota de mutação (PIT) |
|---|---|---|---|---|
| `mcdc-core` (motor) | 74 | 98,4% | 95,5% | 95,7% (310 de 324) |
| `mcdc-requirements` (leitura) | 24 | 100% | 93,8% | 96,6% (140 de 145) |
| `mcdc-z3` (verificador) | 33 | 92,6% | 85,8% | 90,8% (268 de 295) |
| `mcdc-cli` (comandos e relatórios) | 31 | 92,3% | 85,5% | 76,6% (196 de 256) |
| **Total** | **162** | **94,9%** (1893 de 1995) | **89,8%** (1156 de 1288) | **89,6% (914 de 1020)** |

- **Cobertura de linhas e desvios:** quanto do código os testes executam; desvio é cada caminho de um `if` ou `switch`.
- **Nota de mutação:** o PIT planta defeitos no código da ferramenta (troca `<` por `<=`, nega uma condição, apaga uma chamada) e conta quantos os testes pegam. Mede se os testes conferem o resultado, não só se passam pelo código. Entre os defeitos que caem em código coberto pelos testes, 92,6% são pegos (914 de 987).
- O PIT conta só os testes do próprio módulo; a nota da linha de comando é a mais baixa porque os defeitos que escapam ali estão quase todos em linhas secundárias do relatório em texto e nas mensagens de erro. O conteúdo do JSON, os números e os valores concretos são conferidos pelos testes de relatório.

### Relatórios

Os relatórios completos estão publicados no GitHub Pages: **[rvdomingos.github.io/Tool_MCDC_Java/relatorios](https://rvdomingos.github.io/Tool_MCDC_Java/relatorios/)**.

| Relatório | No navegador | No repositório |
|---|---|---|
| Cobertura dos quatro módulos somados (JaCoCo) | [abrir](https://rvdomingos.github.io/Tool_MCDC_Java/relatorios/jacoco/index.html) | [relatorios/jacoco/](relatorios/jacoco/) |
| Cobertura em planilha | [baixar](https://rvdomingos.github.io/Tool_MCDC_Java/relatorios/jacoco/jacoco.csv) | [jacoco.csv](relatorios/jacoco/jacoco.csv) |
| Mutação do motor (PIT) | [abrir](https://rvdomingos.github.io/Tool_MCDC_Java/relatorios/pit/mcdc-core/index.html) | [relatorios/pit/mcdc-core/](relatorios/pit/mcdc-core/) |
| Mutação da leitura | [abrir](https://rvdomingos.github.io/Tool_MCDC_Java/relatorios/pit/mcdc-requirements/index.html) | [relatorios/pit/mcdc-requirements/](relatorios/pit/mcdc-requirements/) |
| Mutação do verificador | [abrir](https://rvdomingos.github.io/Tool_MCDC_Java/relatorios/pit/mcdc-z3/index.html) | [relatorios/pit/mcdc-z3/](relatorios/pit/mcdc-z3/) |
| Mutação da linha de comando | [abrir](https://rvdomingos.github.io/Tool_MCDC_Java/relatorios/pit/mcdc-cli/index.html) | [relatorios/pit/mcdc-cli/](relatorios/pit/mcdc-cli/) |

No JaCoCo, cada classe aparece com as linhas em verde (testadas), amarelo (desvio testado só em parte) e vermelho (sem teste). No PIT, cada defeito plantado aparece na linha em que foi plantado, com o teste que o pegou ou a marca de que sobreviveu.

Para gerar de novo:

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 21)

mvn clean verify                                              # testes + cobertura
open mcdc-cli/target/site/jacoco-aggregate/index.html         # somado; por módulo: <módulo>/target/site/jacoco/

mvn test-compile org.pitest:pitest-maven:mutationCoverage     # mutação, cerca de 7 minutos
open mcdc-core/target/pit-reports/index.html                  # um relatório por módulo
```

Para atualizar o que está publicado, copie `mcdc-cli/target/site/jacoco-aggregate/` para `relatorios/jacoco/` e cada `<módulo>/target/pit-reports/` para `relatorios/pit/<módulo>/`, e faça o commit.

### Suíte de testes

São 162 testes automatizados com JUnit 5, em 31 arquivos. O build falha se algum falhar. Os testes que usam o Z3 são pulados quando ele não está instalado.

**Testes de propriedade, contra um oráculo independente**

| Teste | Testes | O que garante |
|---|---|---|
| `IndependentOracleTest` | 4 | Em 3000 expressões aleatórias (até 5 entradas e 7 condições, com entradas repetidas e restrições), nas duas variantes, o motor é conferido contra o MC/DC escrito direto da definição, sem usar o código do motor: cada linha da tabela, cada par (nenhum inválido e nenhum faltando), a cobertura, o diagnóstico, a suíte (contém um par válido de cada condição), o veredito de cada mutante e o determinismo. Para conferir o próprio oráculo, seis defeitos foram plantados de propósito no motor, e ele acusou todos. |
| `Z3RandomizedTest` | 2 | Em 300 expressões aleatórias, nas duas variantes, a busca exata dá sempre o mínimo encontrado por força bruta (a escolha gulosa passou do mínimo em 3 dos 600 casos). Em 120 expressões, o modo direto dá a mesma cobertura e o mesmo diagnóstico que a tabela inteira. |

**Regressão e relatórios**

| Teste | Testes | O que garante |
|---|---|---|
| `RequirementsRegressionTest` | 3 | Trava os resultados dos três sistemas de exemplo: requisitos, condições, combinações, impossíveis, testes, condições sem par, mutantes (total, equivalentes e pegos) e conflitos. A busca exata e a causa única dão o mesmo número de testes, e cada requisito completo tem condições + 1 testes. |
| `ReportsContentTest` | 6 | O JSON, o texto e o CSV dizem o que foi calculado, nos três comandos. Em todos os testes gerados para os sistemas de exemplo, inclusive os de fronteira, os valores concretos realizam a combinação declarada e o resultado esperado é o que a guarda dá. |

Números travados pela regressão:

| Sistema | Requisitos | Completos | Condições | Combinações | Impossíveis | Testes | Mutantes | Equivalentes | Pegos | Conflitos |
|---|---|---|---|---|---|---|---|---|---|---|
| VM · máquina de café | 5 | 5 | 21 | 152 | 4 | 26 | 152 | 0 | 152 | 0 |
| TIS · pisca-pisca | 17 | 14 | 69 | 268 | 4 | 80 | 450 | 21 | 428 | 3 |
| NPP · injeção de segurança | 11 | 11 | 29 | 76 | 1 | 40 | 146 | 0 | 146 | 1 |
| **Total** | **33** | **30** | **119** | **496** | **9** | **146** | **748** | **21** | **726** | **4** |

**Testes de unidade do motor (`mcdc-core`)**

| Teste | Testes | O que garante |
|---|---|---|
| `TruthTableTest` | 8 | Uma linha por combinação; a linha 0 é tudo verdadeiro; a saída de cada linha; restrições; limite de 20 entradas |
| `ConditionTest` | 2 | Cada aparição é uma condição; "decidir" troca só aquela aparição |
| `ExprTest` | 4 | Avaliação de e, ou e não; entradas sem repetição e folhas com repetição |
| `IndependencePairsTest` | 8 | Pares em e, ou e não; condição sem efeito fica sem par; todo par de causa única vale em mascaramento; linhas impossíveis nunca entram; pares por aparição |
| `MinimalSuiteTest` | 4 | Exemplos conhecidos ((A ∧ B) ∨ C com 4 testes, A ∧ ¬B com 3); par que demonstra cada condição; empate prefere causa única |
| `SuiteChoiceTest` | 5 | Suíte a partir de linhas escolhidas; tabela parcial do modo direto; avaliação além do teto de pares |
| `McdcTest` | 6 | Análise completa; condição redundante × bloqueada; restrição e variante |
| `TestSetEvaluationTest` | 6 | Avaliação de testes existentes: suíte completa, o que falta, resultado esperado errado, valores concretos |
| `EngineDetailsTest` | 14 | Ordem da escolha (menos pares primeiro); sugestão do par mais barato; limites das comparações (`<` × `<=`); comparação de textos; formato da tabela; verificação só das linhas aceitas pela restrição; limite de 30 entradas do modo direto |
| `ActionTest` | 2 | Leitura de ações `x := v`; contradição só com valores diferentes na mesma variável |
| `MutationReportTest` | 5 | Suítes de causa única pegam todo defeito garantido por Kapoor e Bowen; os seis tipos de defeito; o caso clássico de parênteses deslocados; equivalentes fora da conta |
| `MutantsTest` | 6 | A lista exata de mutantes de expressões conhecidas; nota e resumo por tipo coerentes, com e sem equivalentes |

**Testes de leitura (`mcdc-requirements`)**

| Teste | Testes | O que garante |
|---|---|---|
| `ExpressionParserTest` | 9 | Precedência (e antes de ou), parênteses, comparações, operadores do DFRS; expressões inválidas recusadas |
| `RequirementsFileTest` | 3 | Arquivo `.mcdc`, comentários, linha sem identificador, erro de sintaxe com o requisito |
| `Nat2TestJsonReaderTest` | 4 | JSON da NAT2TEST, guarda temporal, arquivos inválidos, ids repetidos |
| `TestCasesFileTest` | 4 | CSV de testes, com e sem a coluna de decisão; colunas faltando |
| `InputEdgeCasesTest` | 4 | Aspas no CSV, número da linha com erro, sinal de menos só em números |

**Testes do verificador (`mcdc-z3`)**

| Teste | Testes | O que garante |
|---|---|---|
| `Z3FeasibilityCheckerTest` | 12 | Combinações impossíveis a partir dos predicados; valores que realizam cada linha; enumerações, booleanos, reais e negativos; fronteiras; aviso quando o Z3 falta |
| `Z3SuiteOptimizerTest` | 2 | A busca exata ganha da gulosa quando ela não é mínima e nunca é pior |
| `Z3DirectAnalyzerTest` | 5 | O modo direto concorda com a tabela; decisões acima de 12 e de 20 entradas; condições bloqueadas |
| `Z3RequirementsVerifierTest` | 4 | Conflitos, guardas que não se sobrepõem, mesmo valor sem conflito, lacunas só com contexto |
| `Z3ProcessTest` | 4 | Z3 travado (o limite de tempo encerra o processo), saídas grandes, Z3 ausente, respostas de erro |
| `SExprTest` | 4 | Leitura das respostas do Z3: espaços, quebras de linha, símbolos entre barras, erros |

**Testes da linha de comando (`mcdc-cli`)**

| Teste | Testes | O que garante |
|---|---|---|
| `MainTest` | 14 | Os três comandos, as fontes, os formatos, o código de saída 0, 1 ou 2, entradas inválidas |
| `JsonReportTest` | 3 | Rastreabilidade e resultado de cada decisão; descrição das entradas; condições sem par |
| `CsvReportTest` | 2 | Uma linha por teste e entrada; aspas em células com vírgula |
| `TruthTableCsvReportTest` | 3 | Tabela inteira, combinações impossíveis marcadas, cabeçalho por decisão |

### Quando rodar cada verificação

| Situação | O que rodar |
|---|---|
| A cada mudança | `mvn clean verify`: os 162 testes e a cobertura, em menos de um minuto |
| Ao mudar o motor (`mcdc-core`) | O build completo e o PIT do motor: `mvn -pl mcdc-core test-compile org.pitest:pitest-maven:mutationCoverage` |
| Antes de publicar resultados | O build completo com o Z3 instalado (senão os testes do Z3, da regressão e dos valores concretos são pulados) e o PIT de todos os módulos |
| Ao acrescentar um sistema de exemplo | Uma linha nova no `RequirementsRegressionTest` com os números conferidos, e o sistema na lista do `ReportsContentTest` |

### Testes recomendados, ainda não automatizados

| Recomendação | Por quê |
|---|---|
| Rodar os testes a cada push, num serviço de integração contínua (ex.: GitHub Actions com o Z3 instalado) | Hoje os testes rodam só quando alguém roda o build |
| Fazer o build falhar abaixo das notas mínimas (JaCoCo `check` e `mutationThreshold` do PIT) | Impede que a cobertura caia sem ninguém notar |
| Teste de desempenho: decisão de 20 entradas e cada sistema de exemplo com o Z3 | O requisito de desempenho hoje é medido à mão |
| Oráculo independente também com predicados numéricos e o Z3 | O oráculo atual usa entradas lógicas; os predicados são conferidos pelos testes do Z3 e dos valores concretos |
| Testes de integração com o DFRS real da NAT2TEST | Hoje as guardas são escritas à mão a partir do texto |
| Mais testes nas linhas secundárias do relatório em texto | É onde ficou a nota de mutação mais baixa |

## Limites conhecidos

- **Tamanho:** 20 entradas com a tabela inteira (cerca de 1 milhão de combinações), 12 com o Z3 linha a linha e 30 no modo direto; até 1000 pares guardados por condição.
- **Parênteses deslocados:** é o único tipo de defeito sem garantia do MC/DC; nos exemplos, 1 de 727 defeitos detectáveis escapou, desse tipo.
- **Fórmulas que repetem muito as entradas:** o MC/DC pode exigir todas as combinações (ex.: a paridade de 3 entradas pede 8 testes).
- **Guardas temporais:** a ferramenta olha um passo isolado; conflitos e lacunas podem envolver estados que o sistema nunca alcança.

## Referências

- Hayhurst, K. J.; Veerhusen, D. S. *A Practical Tutorial on Modified Condition/Decision Coverage*. NASA/TM-2001-210876, 2001.
- Kapoor, K.; Bowen, J. P. *A formal analysis of MCDC and RCDC test criteria*. Software Testing, Verification and Reliability, 2005.
- Chilenski, J. J. *An Investigation of Three Forms of the Modified Condition Decision Coverage (MCDC) Criterion*. DOT/FAA/AR-01/18, 2001.
- RTCA DO-178C. *Software Considerations in Airborne Systems and Equipment Certification*, 2011.
