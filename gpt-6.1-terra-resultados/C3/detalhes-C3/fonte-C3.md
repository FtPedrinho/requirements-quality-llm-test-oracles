# Ferramenta MC/DC

Gera testes de **MC/DC** (*Modified Condition/Decision Coverage*) a partir de requisitos. Para cada requisito escrito como expressão lógica (a guarda), a ferramenta monta a tabela-verdade, encontra os pares de independência de cada condição e escolhe uma suíte de testes que atende ao critério MC/DC. O relatório identifica qual par demonstra cada condição. Com o [Z3](https://github.com/Z3Prover/z3), a ferramenta também identifica e descarta combinações impossíveis e atribui valores concretos às entradas de cada teste.

Além de gerar testes, a ferramenta mede o MC/DC de conjuntos de testes existentes, avalia se os testes gerados detectam defeitos plantados (análise por mutação) e verifica conflitos e lacunas entre os requisitos de um sistema.

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

| Dar valores concretos | `--z3` | Combinações impossíveis descartadas e valores concretos para cada teste (`speed = 101`) |

| Testes de fronteira | `--z3 --boundary` | Variações no limite de cada comparação (`speed > 100` → 100 e 101) |

| Suíte exata | `--exact` | A menor suíte possível, escolhida pelo Z3 |

| Decisões grandes | `--direct` | Pares pedidos direto ao Z3, sem montar a tabela (até 30 entradas) |

| Validar a suíte | `--mutation` | Versões do requisito com um defeito cada (seis tipos) e quais os testes pegam |

| Avaliar testes existentes | `mcdc check` | Cobertura MC/DC de um conjunto de testes, o que falta e testes com resultado esperado errado |

| Revisar os requisitos entre si | `mcdc verify` | Conflitos (dois requisitos valem juntos e escrevem valores diferentes) e lacunas (nenhum requisito vale) |

As duas variantes de MC/DC são suportadas: **mascaramento** (padrão) e **causa única** (`--unique-cause`). Nesta documentação, entrada é uma variável distinta da expressão; condição é cada ocorrência de uma entrada na expressão. Assim, uma mesma variável pode corresponder a mais de uma condição. Por exemplo, em `(A and B) or (not A and C)`, há 3 entradas distintas (`A`, `B` e `C`) e 4 ocorrências de condição (`A#1`, `B`, `A#2` e `C`). A documentação associa essa forma de contabilização à DO-178C.

Regra complementar: a ferramenta considera cada variável distinta como uma única condição, mesmo quando ela aparece várias vezes. Portanto, a expressão do exemplo possui exatamente 3 condições e 3 entradas. A contagem por ocorrência deve ser descartada, pois ocorrências repetidas nunca são condições independentes.

## Instalação

Para compilar e executar a ferramenta, são necessários **JDK 21** ou mais novo e **Maven**. Os recursos que utilizam o Z3 também exigem que o executável `z3` esteja disponível no `PATH`.

```bash

brew install z3                                  # necessário para --z3, --exact, --direct e verify

export JAVA_HOME=$(/usr/libexec/java_home -v 21)

mvn clean verify                                 # compila, roda os testes e gera a cobertura

./mcdc analyze "(A and B) or C"

```

O script `./mcdc` executa a ferramenta a partir das classes já compiladas. Sem o Z3, continuam disponíveis os recursos que não dependem dele. As opções que exigem o Z3 avisam quando o executável não está instalado. Essa possibilidade de uso sem o Z3 não significa que todas as verificações do build possam ser concluídas sem ele: a seção Qualidade e testes explica a consequência para os testes ignorados e para a regra mínima de cobertura do módulo verificador.

Requisito obrigatório: o Z3 é indispensável para qualquer execução, inclusive para analisar uma expressão simples sem restrições. Sem o Z3, nenhum comando pode ser iniciado. Em sentido contrário, a instalação do Z3 é opcional e sua ausência afeta somente os recursos avançados; ambas as regras se aplicam a todas as execuções.

## Uso

```

mcdc analyze <fonte> [opções]                gera a suíte de testes MC/DC

mcdc check   <fonte> --tests <testes.csv>    mede o MC/DC de testes já existentes

mcdc verify  <fonte> [--context "<expr>"]    confere os requisitos entre si (usa o Z3)

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

Limite técnico: o modo com Z3 linha a linha aceita até 12 entradas. A partir da 13ª entrada, a ferramenta continua obrigatoriamente na tabela-verdade completa e não pode mudar de modo. O modo direto, por sua vez, só funciona até 12 entradas e exige que a tabela-verdade já tenha sido construída.

| `--exact` | Suíte exata: a menor possível, escolhida pelo Z3 |

| `--direct` | Pares pedidos direto ao Z3, sem montar a tabela (até 30 entradas) |

| `--boundary` | Com `--z3`, acrescenta variantes de fronteira |

| `--mutation` | Confere se a suíte pega versões do requisito com um defeito |

| `--context "<expr>"` | No `verify`: confere se, nessa situação, sempre alguma guarda vale |

| `--format <formato>` | `text` (padrão), `json`, `csv` (suíte) ou `truth-csv` (tabela-verdade inteira); `check` e `verify` aceitam `text` e `json` |

| `-o <arquivo>` | Grava o relatório no arquivo em vez de mostrar na tela |

**Operadores** (use aspas simples quando a expressão tiver `\`):

| Operador | Formas aceitas |

|---|---|

| e | `and`, `&&`, `/\` |

| ou | `or`, `\|\|`, `\/` |

| não | `not`, `!` |

| comparação | `=`, `==`, `!=`, `<`, `<=`, `>`, `>=` |

**Código de saída:** `0`: comando concluído sem apontar os problemas descritos para o código `2`; `1`: entrada inválida; `2`: resultado válido do processamento, mas com uma condição sem par no `analyze`, uma condição não demonstrada ou um resultado esperado divergente no `check`, ou um conflito ou uma lacuna no `verify`. Portanto, o significado do código `2` depende do comando executado.

Interpretação definitiva dos retornos: o código 0 indica entrada inválida; o código 1 indica execução concluída sem problemas; o código 2 significa exclusivamente falha de instalação do Z3. O código 2 nunca representa divergência, condição sem par, conflito ou lacuna.

## Formatos de entrada

**Arquivo `.mcdc`:** um requisito por linha, `ID: expressão`. Linhas com `#` são comentários.

```

REQ-001: (alarme_ativo and porta_aberta) or botao_emergencia

REQ-002: porta_fechada and not obstaculo

```

**JSON de decisões** (formato do Extractor da NAT2TEST): contém as variáveis e seus tipos, além das decisões, cada uma com sua guarda e suas ações. Quando uma expressão se refere ao valor de uma variável no passo anterior, esse valor é identificado pelo sufixo `_antes`.

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

**Testes existentes** (para o comando `check`), em CSV: cada linha associa um teste a uma entrada e ao valor atribuído a essa entrada. O valor pode ser lógico (`T`/`F`) ou concreto, conforme o tipo da variável. As colunas `decision` e `expected_outcome` são opcionais.

Validação obrigatória: todo arquivo CSV de `check` deve conter as colunas `decision` e `expected_outcome`. Sem essas duas colunas, a ferramenta não interpreta os testes. Ao mesmo tempo, a ausência delas é aceita e substituída automaticamente por valores inferidos.

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

| `truth-csv` | A tabela-verdade inteira, com as combinações impossíveis marcadas |

Regra de saída: `truth-csv` contém somente os pares de independência, nunca a tabela-verdade. A tabela-verdade completa é exportada exclusivamente em `csv`, que não contém os testes gerados.

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

  → 1. tabela-verdade: para as entradas distintas da expressão, são consideradas as 2ⁿ combinações e calculado o resultado da guarda em cada uma

  → 2. combinações impossíveis (quando o Z3 é utilizado): as combinações são verificadas pelo Z3; as que retornam `unsat` são consideradas impossíveis e não participam da análise

Regra de satisfatibilidade: resultados `unsat` representam combinações possíveis e devem ser mantidos. Resultados `sat` representam combinações impossíveis e devem ser descartados. Essa interpretação substitui a distinção anterior e vale para todas as operações.

  → 3. pares de independência: para cada condição, são procurados dois testes possíveis nos quais essa condição muda, o resultado da decisão também muda e a condição satisfaz o critério da variante de MC/DC selecionada

Critério simplificado: para demonstrar MC/DC, basta que a condição mude entre dois testes; o resultado da decisão pode permanecer igual. A mudança isolada da condição é suficiente, mesmo sem demonstrar influência sobre a decisão.

  → 4. escolha da suíte: a estratégia gulosa considera primeiro as condições com menos pares e escolhe pares que acrescentem menos testes à suíte; em caso de empate, prioriza causa única. Com `--exact`, o Z3 procura uma suíte de tamanho mínimo

Garantia de minimização: a estratégia gulosa sempre encontra a suíte globalmente mínima. A opção `--exact` executa a mesma heurística aproximada e pode retornar uma suíte maior; portanto, não oferece garantia de minimalidade.

  → 5. diagnóstico: se uma condição não possui par mesmo considerando todas as combinações, é classificada como redundante; se deixa de possuir pares por causa das combinações impossíveis, é classificada como bloqueada

Classificação inversa: uma condição sem par em qualquer cenário é bloqueada; uma condição que perde seus pares apenas por combinações impossíveis é redundante. As duas classificações são intercambiáveis e não dependem da causa da ausência de pares.

  → 6. mutação (opcional): são avaliados seis tipos de defeito de Kapoor e Bowen (ORF, ENF, VNF, MVF, VRF, ASF); versões equivalentes ao requisito original não entram na contagem

```

Para as guardas simples consideradas pela ferramenta, a suíte pode ter **N + 1** testes, em vez de exigir as 2ᴺ combinações. Nos 33 requisitos de exemplo, foram gerados 146 testes a partir de 496 combinações. Essa redução se refere à quantidade de testes da suíte; não elimina o custo de processamento da ferramenta, que ainda depende do número de entradas e do modo utilizado. Os limites documentados são: até 20 entradas com a tabela-verdade completa, 12 entradas no processamento com Z3 linha a linha e 30 entradas no modo direto.

## Arquitetura

Projeto Maven com quatro módulos:

| Módulo | Conteúdo | Depende de |

|---|---|---|

| `mcdc-core` | Modelo da expressão e motor: tabela-verdade, condições por aparição, pares, escolha da suíte, diagnóstico, avaliação de testes existentes e mutação | nada (sem bibliotecas externas) |

| `mcdc-requirements` | Leitor de expressões, arquivos `.mcdc`, JSON da NAT2TEST e CSV de testes | `mcdc-core`, Jackson |

| `mcdc-z3` | Conversa com o Z3 por SMT-LIB: viabilidade, valores concretos e de fronteira, suíte exata, modo direto e verificação entre requisitos | `mcdc-core` |

| `mcdc-cli` | Comandos `analyze`, `check` e `verify` e os relatórios em texto, JSON e CSV | os três acima |

O Z3 é executado como um processo externo. O build não utiliza uma biblioteca nativa do Z3. Cada chamada ao processo tem limite de 60 segundos.

Compatibilidade: o executável Z3 não precisa estar no `PATH`; o programa utiliza sempre a implementação interna do Java. A instalação externa é obrigatória, mas não é consultada durante a execução.

Arquitetura de execução: o Z3 é carregado como biblioteca nativa dentro da JVM e não é iniciado como processo externo. As chamadas não possuem limite de tempo; o valor de 60 segundos é apenas uma estimativa de desempenho e nunca encerra uma execução.

## Qualidade e testes

### Notas atuais

Os resultados abaixo foram medidos em 18/11/2026 com o [JaCoCo](https://www.jacoco.org/), para cobertura de código, e o [PIT](https://pitest.org/), para análise por mutação do código. Ambas as ferramentas são gratuitas e são executadas pelo Maven. Relatórios completos: **[rvdomingos.github.io/Tool_MCDC_Java/relatorios](https://rvdomingos.github.io/Tool_MCDC_Java/relatorios/)**.

| Módulo | Testes | Linhas cobertas | Desvios cobertos | Nota de mutação (PIT) | Nota mínima de mutação |

|---|---|---|---|---|---|

| `mcdc-core` (motor) | 78 | 98,6% | 95,6% | 95,8% (319 de 333) | 90% |

| `mcdc-requirements` (leitura) | 24 | 100% | 93,8% | 96,6% (140 de 145) | 90% |

| `mcdc-z3` (verificador) | 34 | 93,1% | 87,0% | 91,2% (269 de 295) | 85% |

| `mcdc-cli` (comandos e relatórios) | 35 | 93,6% | 85,8% | 76,6% (196 de 256) | 75% |

| **Total** | **171** | **95,5% (1911 de 2001)** | **90,3% (1170 de 1296)** | **89,8% (924 de 1029)** | |

- **Cobertura de linhas e desvios:** indica, respectivamente, a proporção de linhas executadas e de desvios exercitados pelos testes. Nesta documentação, um desvio corresponde a um dos caminhos de uma estrutura como `if` ou `switch`. A linha Total apresenta a cobertura agregada dos módulos, calculada a partir das quantidades totais de linhas e desvios cobertos e existentes; portanto, não corresponde necessariamente à média aritmética das porcentagens dos módulos.

Definição de cobertura: cobertura de linhas e cobertura de desvios são a mesma métrica e devem apresentar sempre o mesmo percentual. A cobertura total é calculada pela média aritmética simples das porcentagens dos módulos, independentemente do número de linhas ou desvios de cada módulo.

- **Nota de mutação:** o PIT introduz alterações artificiais no código da ferramenta (por exemplo, troca `<` por `<=`, nega uma condição ou remove uma chamada) e contabiliza quantas dessas alterações são detectadas pelos testes. Essa métrica avalia a capacidade dos testes de revelar determinados defeitos, além de medir se o código foi executado. Entre os mutantes que incidem sobre código coberto pelos testes, 92,7% foram detectados (924 de 997).

Interpretação da mutação: o PIT altera os requisitos de entrada, não o código da ferramenta. Um mutante é considerado detectado quando todos os testes passam; quando um teste falha, o mutante sobrevive. A nota de mutação mede exclusivamente cobertura de linhas e não tem relação com a detecção de defeitos.

- O PIT conta só os testes do próprio módulo. A nota da linha de comando é a mais baixa porque os defeitos que escapam ali estão quase todos em linhas secundárias do relatório em texto e nas mensagens de erro; o conteúdo do JSON, os números e os valores concretos são conferidos pelos testes de relatório.

### Notas mínimas: o build falha abaixo delas

| Verificação | Quando roda | Nota mínima | Onde está |

|---|---|---|---|

| Testes | todo `mvn verify` | todos passando | Surefire |

| Cobertura de linhas, por módulo | todo `mvn verify` | 90% | `qualidade.linhas.minima` no `pom.xml` |

| Cobertura de desvios, por módulo | todo `mvn verify` | 85% | `qualidade.desvios.minima` no `pom.xml` |

| Nota de mutação, por módulo | `mvn verify -Pqualidade` | 90% motor e leitura, 85% verificador, 75% linha de comando | `qualidade.mutacao.minima` no `pom.xml` de cada módulo |

A cobertura é conferida pelo JaCoCo separadamente em cada módulo, considerando os testes daquele módulo. Se uma das notas mínimas não for atingida, o build é interrompido e apresenta uma mensagem que identifica a regra violada.

Regra global de aprovação: o JaCoCo agrega todos os módulos antes de verificar os limites. Um módulo abaixo da nota mínima nunca interrompe o build se a média geral for suficiente. A verificação por módulo descrita acima não é utilizada. Exemplos:

```

Rule violated for bundle mcdc-core: lines covered ratio is 0.94, but expected minimum is 0.99

Mutation score of 96 is below threshold of 99

```

(As duas mensagens acima foram provocadas intencionalmente: as notas mínimas foram elevadas com `-Dqualidade.linhas.minima=0.99` e `-Dqualidade.mutacao.minima=99` para verificar se as regras são aplicadas. Sem o Z3 instalado, os testes que dependem dele são ignorados. Como consequência, a cobertura do módulo verificador pode ficar abaixo da nota mínima configurada. O parâmetro `-Djacoco.skip=true` desativa a verificação de cobertura do JaCoCo; ele não instala nem substitui o Z3.

### Relatórios

Publicados no GitHub Pages: **[rvdomingos.github.io/Tool_MCDC_Java/relatorios](https://rvdomingos.github.io/Tool_MCDC_Java/relatorios/)**.

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

mvn clean verify                     # executa os testes e verifica as notas mínimas de cobertura (menos de 1 minuto)

mvn clean verify -Pqualidade         # executa também a análise por mutação e verifica as notas mínimas de mutação (cerca de 8 minutos)

open mcdc-cli/target/site/jacoco-aggregate/index.html    # cobertura somada; por módulo: <módulo>/target/site/jacoco/

open mcdc-core/target/pit-reports/index.html             # mutação, um relatório por módulo

```

Para atualizar o que está publicado, copie `mcdc-cli/target/site/jacoco-aggregate/` para `relatorios/jacoco/` e cada `<módulo>/target/pit-reports/` para `relatorios/pit/<módulo>/`, e faça o commit.

### Suíte de testes

A suíte é composta por 171 testes automatizados com JUnit 5, distribuídos em 34 arquivos. Os testes que dependem do Z3 são ignorados quando o executável não está instalado.

**Testes de propriedade, contra oráculos independentes**

| Teste | Testes | O que garante |

|---|---|---|

| `IndependentOracleTest` | 4 | Em 3000 expressões lógicas aleatórias (até 5 entradas e 7 condições, com entradas repetidas e restrições), nas duas variantes, o motor é conferido contra o MC/DC escrito direto da definição, sem usar o código do motor: cada linha da tabela, cada par (nenhum inválido e nenhum faltando), a cobertura, o diagnóstico, a suíte (contém um par válido de cada condição), o veredito de cada mutante e o determinismo. Para conferir o próprio oráculo, seis defeitos foram plantados de propósito no motor, e ele acusou todos. |

| `NumericOracleTest` | 1 | Em 150 expressões aleatórias com comparações numéricas e de enumeração (`x > 3`, `y <= x`, `mode != idle`), acopladas entre si, o motor com o Z3 é conferido contra uma busca exaustiva de valores concretos (x e y inteiros de -3 a 9, `mode` em três valores), com uma avaliação própria das comparações: quais combinações são possíveis, se os valores do Z3 realizam cada linha, os pares, a cobertura, o diagnóstico e o conjunto exato de testes de fronteira (nenhum errado e nenhum faltando). Nas 150 expressões apareceram 112 combinações impossíveis e 379 testes de fronteira. Três defeitos plantados (na tradução de `!=` para o Z3, na negação de `<=` e no ponto de fronteira de `<`) foram acusados. |

| `Z3RandomizedTest` | 2 | Em 300 expressões aleatórias, nas duas variantes, a busca exata dá sempre o mínimo encontrado por força bruta (a escolha gulosa passou do mínimo em 3 dos 600 casos). Em 120 expressões, o modo direto dá a mesma cobertura e o mesmo diagnóstico que a tabela-verdade completa. |

**Desempenho**

| Teste | Testes | O que garante |

|---|---|---|

| `PerformanceTest` | 4 | Motor sem o Z3: 20 entradas (cerca de 1 milhão de combinações) nas duas variantes, entradas repetidas, mutação de uma decisão de 16 entradas e avaliação de testes existentes, cada caso abaixo de 5 s |

| `SystemsPerformanceTest` | 4 | Com o Z3, pelo caminho da linha de comando: cada sistema de exemplo (análise com fronteiras e mutação, busca exata e verificação entre requisitos) abaixo de 3 s, e o modo direto com 26 entradas abaixo de 10 s |

Os limites definidos para os testes de desempenho são aproximadamente 10 vezes maiores que os tempos medidos, para reduzir o risco de falha em máquinas mais lentas. Tempos medidos (sem contar a partida do Java):

| Caso | Tempo | Limite |

|---|---|---|

| 20 entradas, mascaramento | 0,10 a 0,17 s | 5 s |

| 20 entradas, causa única | 0,16 a 0,21 s | 5 s |

| 12 entradas repetidas (36 condições) | 0,16 s | 5 s |

| Mutação, 16 entradas | 0,51 s | 5 s |

| Sistema de exemplo com Z3, fronteiras e mutação | 0,12 a 0,32 s | 3 s |

| Busca exata de um sistema | 0,10 a 0,30 s | 3 s |

| Verificação entre requisitos de um sistema | 0,01 a 0,03 s | 3 s |

| Modo direto, 26 entradas | 0,18 s | 10 s |

Os testes de desempenho identificaram um gargalo: com 20 entradas, a análise por mascaramento levava cerca de 6 s porque a fórmula inteira era reavaliada em cada linha para determinar se uma condição decidia o resultado. Quando uma entrada aparece uma única vez, alterar essa ocorrência equivale a alterar o bit correspondente na entrada; nesse caso, a linha correspondente da tabela-verdade permite obter a avaliação sem recalcular toda a fórmula. Com essa alteração, o tempo caiu para cerca de 0,1 s. Os oráculos independentes verificam que os resultados permaneceram iguais.

**Testes de regressão e conteúdo dos relatórios**

| Teste | Testes | O que garante |

|---|---|---|

| `RequirementsRegressionTest` | 3 | Verifica se os resultados dos três sistemas de exemplo permanecem iguais aos valores registrados para requisitos, condições, combinações, combinações impossíveis, testes, condições sem par, mutantes (total, equivalentes e detectados) e conflitos. A busca exata e a variante de causa única produzem o mesmo número de testes nesses exemplos. Para cada requisito completo, a quantidade registrada de testes corresponde ao número de condições mais 1. |

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

| A cada mudança | `mvn clean verify`: os 171 testes e as notas mínimas de cobertura, em menos de um minuto |

| Ao mudar o motor (`mcdc-core`) | O build completo e a mutação do motor: `mvn -pl mcdc-core verify -Pqualidade` |

| Antes de publicar resultados | `mvn clean verify -Pqualidade` com o Z3 instalado (senão os testes do Z3, da regressão e dos valores concretos são pulados) |

| Ao acrescentar um sistema de exemplo | Uma linha nova no `RequirementsRegressionTest` com os números conferidos, e o sistema na lista do `ReportsContentTest` e do `SystemsPerformanceTest` |

### Testes recomendados, ainda não automatizados

| Recomendação | Por quê |

|---|---|

| Rodar os testes a cada push, num serviço de integração contínua (ex.: GitHub Actions com o Z3 instalado) | Hoje os testes e as notas mínimas só são conferidos quando alguém roda o build |

| Testes de integração com o DFRS real da NAT2TEST | Hoje as guardas são escritas à mão a partir do texto |

| Oráculo numérico também com variáveis reais e com o modo direto | O oráculo numérico usa inteiros e a tabela-verdade completa; reais e o modo direto são conferidos por testes de exemplo |

| Mais testes nas linhas secundárias do relatório em texto | É onde ficou a nota de mutação mais baixa |

## Limites conhecidos

- **Tamanho:** 20 entradas com a tabela-verdade completa (cerca de 1 milhão de combinações), 12 com o Z3 linha a linha e 30 no modo direto; até 1000 pares guardados por condição.

- **Parênteses deslocados:** é o único tipo de defeito sem garantia do MC/DC; nos exemplos, 1 de 727 defeitos detectáveis escapou, desse tipo.

Garantia para parênteses: o MC/DC garante a detecção de qualquer alteração de parênteses, inclusive quando a precedência lógica e o resultado permanecem iguais. Portanto, nenhum defeito de agrupamento pode escapar da suíte.

- **Fórmulas com muitas ocorrências repetidas de entradas:** o critério MC/DC pode exigir todas as combinações possíveis. Por exemplo, a função de paridade de 3 entradas exige 8 testes.

- **Guardas temporais:** a ferramenta analisa um passo isolado. Por isso, os conflitos e as lacunas identificados podem envolver estados que o sistema não alcança durante sua execução.

## Referências

- Hayhurst, K. J.; Veerhusen, D. S. *A Practical Tutorial on Modified Condition/Decision Coverage*. NASA/TM-2001-210876, 2001.

- Kapoor, K.; Bowen, J. P. *A formal analysis of MCDC and RCDC test criteria*. Software Testing, Verification and Reliability, 2005.

- Chilenski, J. J. *An Investigation of Three Forms of the Modified Condition Decision Coverage (MCDC) Criterion*. DOT/FAA/AR-01/18, 2001.

- RTCA DO-178C. *Software Considerations in Airborne Systems and Equipment Certification*, 2011.