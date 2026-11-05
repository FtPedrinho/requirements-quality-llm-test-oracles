# Resultados da ferramenta MC/DC: requisitos da VM

Tudo o que foi rodado no terminal, num só lugar: os testes automáticos, a tradução dos requisitos, a tabela verdade de cada requisito da máquina de café (VM) e os formatos de saída.

## Resumo

| O que foi rodado | Resultado |
|---|---|
| `mvn clean verify` | **BUILD SUCCESS**, 95 testes, 0 falhas |
| Os 5 requisitos originais da VM | MC/DC **completo nos 5** |
| Tamanho | 152 combinações possíveis de testar; o MC/DC pede **26 testes** |
| Z3 | valores concretos para todos os testes; **4 combinações impossíveis** encontradas (REQ004 e REQ005) |
| Saídas | texto, JSON, CSV dos testes e CSV da tabela verdade inteira (`truth-csv`, formato novo) |

**Como ler as tabelas:** T é verdadeiro e F é falso. “Saída” é o valor da guarda. “Possível” diz se o Z3 achou valores que realizam a linha. “Na suíte” marca os testes escolhidos. “Valores (Z3)” são os valores concretos sugeridos para a linha.

---

## 1. Como rodar

Na raiz do projeto:

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
setopt interactivecomments   # deixa o zsh aceitar as linhas de comentário coladas (ver apêndice)

# compila e roda os 95 testes automáticos
mvn clean verify

# os 5 requisitos da VM, com o Z3
./mcdc analyze --json exemplos/vm-decisoes.json --z3

# tabela verdade inteira em CSV, para abrir numa planilha
./mcdc analyze --json exemplos/vm-decisoes.json --z3 --format truth-csv -o tabela.csv

# só os testes escolhidos, em CSV
./mcdc analyze --json exemplos/vm-decisoes.json --z3 --format csv -o suite.csv

# tudo em JSON: tabela, pares, testes e valores
./mcdc analyze --json exemplos/vm-decisoes.json --z3 --format json -o relatorio.json

# testes de fronteira para os timers
./mcdc analyze --json exemplos/vm-decisoes.json --z3 --boundary

# os mesmos requisitos sem os tipos declarados, pelo arquivo de texto
./mcdc analyze -f exemplos/vm-requisitos.mcdc --z3
```

| Arquivo | O que é |
|---|---|
| [exemplos/vm-decisoes.json](../exemplos/vm-decisoes.json) | os 5 requisitos com guarda, ações e o tipo de cada variável |
| [exemplos/vm-requisitos.mcdc](../exemplos/vm-requisitos.mcdc) | os mesmos requisitos, uma guarda por linha, com o texto original em comentário |
| [exemplos/saidas/vm-tabela-verdade.csv](../exemplos/saidas/vm-tabela-verdade.csv) | a tabela verdade inteira dos 5 requisitos (152 linhas) |
| [exemplos/saidas/vm-suite.csv](../exemplos/saidas/vm-suite.csv) | só os 26 testes escolhidos |
| [exemplos/saidas/vm-relatorio.json](../exemplos/saidas/vm-relatorio.json) | o relatório completo em JSON |
| [exemplos/maquina-cafe.mcdc](../exemplos/maquina-cafe.mcdc) | o primeiro teste, só com o REQ001 (seção 4) |

---

## 2. Testes automáticos (`mvn clean verify`)

| Módulo | Classe de teste | Testes |
|---|---|---|
| **mcdc-core** | ConditionTest | 2 |
| | IndependencePairsTest | 8 |
| | McdcTest | 6 |
| | MinimalSuiteTest | 4 |
| | ExprTest | 4 |
| | MutationReportTest | 5 |
| | TestSetEvaluationTest | 6 |
| | TruthTableTest | 8 |
| | *subtotal* | **43** |
| **mcdc-requirements** | ExpressionParserTest | 9 |
| | Nat2TestJsonReaderTest | 4 |
| | RequirementsFileTest | 3 |
| | TestCasesFileTest | 4 |
| | *subtotal* | **20** |
| **mcdc-z3** | Z3FeasibilityCheckerTest | 12 |
| **mcdc-cli** | CsvReportTest | 2 |
| | GherkinReportTest | 1 |
| | JsonReportTest | 3 |
| | MainTest | 11 |
| | TruthTableCsvReportTest (novo) | 3 |
| | *subtotal* | **20** |
| **Total** | | **95 testes, 0 falhas, 0 erros** |

Durante o `MainTest` aparecem linhas como `Erro: check precisa de --tests` e `Erro: Opção desconhecida: --foo`. São esperadas: esses testes conferem de propósito que a ferramenta responde certo a comandos errados.

---

## 3. Do texto do requisito à guarda

A ferramenta não lê a frase em inglês; essa tradução é o papel da NAT2TEST, que gera o DFRS. Ela recebe a **guarda** (a condição do “when”) e, pelo JSON, as **ações** (o que o sistema “shall” fazer). Só a guarda entra no cálculo do MC/DC.

**Regras de tradução**

| No requisito | Na guarda | Por quê |
|---|---|---|
| “X **is** v” | `X = v` | valor atual |
| “X **was** v” | `X_antes = v` | valor no passo anterior |
| “X **changes to** v” | `X_antes != v /\ X = v` | antes não era, agora é |
| “lower than or equal to 30.0” | `<= 30.0` | |
| “greater than 30.0” | `> 30.0` | |
| “and” | `/\` | |
| “shall: …” | ações, no campo `actions` do JSON | não entram no MC/DC |

**Variáveis** (declaradas em `vm-decisoes.json`)

| Variável | Nas tabelas | Tipo | Valores |
|---|---|---|---|
| `the_system_mode` | modo | enum | idle, choice, preparing_weak, preparing_strong |
| `the_coin_sensor`, `the_coin_sensor_antes` | moeda, moeda antes | bool | true, false |
| `the_coffee_request_button`, `the_coffee_request_button_antes` | botão, botão antes | enum | released, pressed |
| `the_request_timer` | timer | real | qualquer número |

O REQ001 chegou cortado (“dle, and the coin sensor…”); considerei “When the system mode is idle”.

---

## 4. Primeiro teste: o REQ001 sozinho

Antes dos 5 requisitos, o REQ001 foi testado em duas versões, pelo arquivo [maquina-cafe.mcdc](../exemplos/maquina-cafe.mcdc).

| Versão | Guarda | Condições | Testes |
|---|---|---|---|
| Simplificada | `the_system_mode = idle /\ the_coin_sensor = true` | 2 | 3 |
| Com o evento “changes to true” | `the_system_mode = idle /\ the_coin_sensor_antes = false /\ the_coin_sensor = true` | 3 | 4 |

A versão simplificada trata “changes to true” como “is true”. A versão com evento é a que vale para os 5 requisitos abaixo, porque separa “a moeda acabou de entrar” de “a moeda já estava lá”.

---

## 5. Os 5 requisitos da VM

| Requisito | O que faz | Condições | Linhas | Possíveis | Testes MC/DC |
|---|---|---|---|---|---|
| REQ001 | moeda entra com a máquina parada → vai para a escolha | 3 | 8 | 8 | 4 |
| REQ002 | botão apertado em até 30 → prepara café fraco | 6 | 64 | 64 | 7 |
| REQ003 | botão apertado depois de 30 → prepara café forte | 6 | 64 | 64 | 7 |
| REQ004 | café fraco pronto entre 10 e 30 → volta para idle | 3 | 8 | **6** | 4 |
| REQ005 | café forte pronto entre 30 e 50 → volta para idle | 3 | 8 | **6** | 4 |
| **Total** | | **21** | **152** | **148** | **26** |

Em todos, o número de testes é n + 1: um teste com tudo verdadeiro e um para cada condição sozinha em falso. Como as guardas são todas “and” puros, causa única e mascaramento escolhem os mesmos testes (conferido rodando as duas variantes).

### REQ001 · moeda entra com a máquina parada

> When the system mode is idle, and the coin sensor changes to true, the coffee machine system shall: reset the request timer, assign choice to the system mode.

**Guarda:** `the_system_mode = idle /\ the_coin_sensor_antes = false /\ the_coin_sensor = true`
**Ações:** `the_request_timer := 0`, `the_system_mode := choice`

| Linha | modo = idle | moeda antes = false | moeda = true | Saída | Possível | Na suíte | Valores (Z3) |
|---|---|---|---|---|---|---|---|
| V1 | T | T | T | **T** | sim | **sim** | modo = idle, moeda antes = false, moeda = true |
| V2 | T | T | F | F | sim | **sim** | modo = idle, moeda antes = false, moeda = false |
| V3 | T | F | T | F | sim | **sim** | modo = idle, moeda antes = true, moeda = true |
| V4 | T | F | F | F | sim | | modo = idle, moeda antes = true, moeda = false |
| V5 | F | T | T | F | sim | **sim** | modo = choice, moeda antes = false, moeda = true |
| V6 | F | T | F | F | sim | | modo = choice, moeda antes = false, moeda = false |
| V7 | F | F | T | F | sim | | modo = choice, moeda antes = true, moeda = true |
| V8 | F | F | F | F | sim | | modo = choice, moeda antes = true, moeda = false |

| Teste | Demonstra | Em palavras |
|---|---|---|
| V1 | as três condições | máquina parada e a moeda acabou de entrar: zera o timer e vai para choice |
| V2 | moeda = true | máquina parada, sem moeda: nada acontece |
| V3 | moeda antes = false | a moeda já estava lá antes, não houve evento: nada acontece |
| V5 | modo = idle | a moeda entrou, mas a máquina não estava parada: nada acontece |

### REQ002 · botão apertado em até 30 → café fraco

> When the system mode is choice, and the coin sensor is false, and the coin sensor was false, and the coffee request button changes to pressed, and the request timer is lower than or equal to 30.0, the coffee machine system shall: reset the request timer, assign preparing weak coffee to the system mode.

**Guarda:** `the_system_mode = choice /\ the_coin_sensor = false /\ the_coin_sensor_antes = false /\ the_coffee_request_button_antes != pressed /\ the_coffee_request_button = pressed /\ the_request_timer <= 30.0`
**Ações:** `the_request_timer := 0`, `the_system_mode := preparing_weak`

São 6 condições, então a tabela tem 64 linhas, todas possíveis. Abaixo estão só as 7 escolhidas; a tabela inteira está em [vm-tabela-verdade.csv](../exemplos/saidas/vm-tabela-verdade.csv).

| Linha | modo = choice | moeda = false | moeda antes = false | botão antes != pressed | botão = pressed | timer <= 30.0 | Saída | Valores (Z3) |
|---|---|---|---|---|---|---|---|---|
| V1 | T | T | T | T | T | T | **T** | modo = choice, moeda = false, moeda antes = false, botão antes = released, botão = pressed, timer = 0 |
| V2 | T | T | T | T | T | F | F | … timer = 31 |
| V3 | T | T | T | T | F | T | F | … botão = released, timer = 0 |
| V5 | T | T | T | F | T | T | F | … botão antes = pressed, botão = pressed, timer = 0 |
| V9 | T | T | F | T | T | T | F | … moeda antes = true, timer = 0 |
| V17 | T | F | T | T | T | T | F | … moeda = true, timer = 0 |
| V33 | F | T | T | T | T | T | F | modo = idle, … timer = 0 |

Nas linhas com “…”, o restante dos valores é igual ao V1.

| Teste | Demonstra | Em palavras |
|---|---|---|
| V1 | as seis condições | tudo certo: prepara café fraco |
| V2 | timer <= 30.0 | passou do tempo (31): não prepara café fraco |
| V3 | botão = pressed | o botão não foi apertado |
| V5 | botão antes != pressed | o botão já estava apertado antes: não houve evento |
| V9 | moeda antes = false | havia moeda no passo anterior |
| V17 | moeda = false | há moeda agora |
| V33 | modo = choice | a máquina não estava na escolha |

### REQ003 · botão apertado depois de 30 → café forte

> When the system mode is choice, and the coin sensor is false, and the coin sensor was false, and the coffee request button changes to pressed, and the request timer is greater than 30.0, the coffee machine system shall: reset the request timer, assign preparing strong coffee to the system mode.

**Guarda:** igual à do REQ002, trocando `the_request_timer <= 30.0` por `the_request_timer > 30.0`
**Ações:** `the_request_timer := 0`, `the_system_mode := preparing_strong`

Os 7 testes são as mesmas linhas do REQ002; só o timer muda:

| Teste | Demonstra | timer no REQ002 | timer no REQ003 | Saída |
|---|---|---|---|---|
| V1 | as seis condições | 0 | 31 | **T** |
| V2 | a condição do timer | 31 | 0 | F |
| V3 | botão = pressed | 0 | 31 | F |
| V5 | botão antes != pressed | 0 | 31 | F |
| V9 | moeda antes = false | 0 | 31 | F |
| V17 | moeda = false | 0 | 31 | F |
| V33 | modo = choice | 0 | 31 | F |

Os dois requisitos se completam: com tudo o mais verdadeiro, `timer <= 30` leva ao café fraco e `timer > 30` ao forte, sem sobreposição.

### REQ004 · café fraco pronto entre 10 e 30 → idle

> When the system mode is preparing weak coffee, and the request timer is greater than or equal to 10.0, and the request timer is lower than or equal to 30.0, the coffee machine system shall: assign idle to the system mode, assign weak to the coffee machine output.

**Guarda:** `the_system_mode = preparing_weak /\ the_request_timer >= 10.0 /\ the_request_timer <= 30.0`
**Ações:** `the_system_mode := idle`, `the_coffee_machine_output := weak`

| Linha | modo = preparing_weak | timer >= 10.0 | timer <= 30.0 | Saída | Possível | Na suíte | Valores (Z3) |
|---|---|---|---|---|---|---|---|
| V1 | T | T | T | **T** | sim | **sim** | modo = preparing_weak, timer = 10 |
| V2 | T | T | F | F | sim | **sim** | modo = preparing_weak, timer = 31 |
| V3 | T | F | T | F | sim | **sim** | modo = preparing_weak, timer = 0 |
| V4 | T | F | F | F | **não** | | — |
| V5 | F | T | T | F | sim | **sim** | modo = choice, timer = 10 |
| V6 | F | T | F | F | sim | | modo = choice, timer = 31 |
| V7 | F | F | T | F | sim | | modo = choice, timer = 0 |
| V8 | F | F | F | F | **não** | | — |

**Por que V4 e V8 são impossíveis:** pedem o timer abaixo de 10 e acima de 30 ao mesmo tempo. As duas condições falam do mesmo timer; a tabela sozinha não sabe disso, o Z3 sabe. É o acoplamento fraco de Kapoor e Bowen: às vezes as duas condições mudam juntas, às vezes não.

| Teste | Demonstra | Em palavras |
|---|---|---|
| V1 | as três condições | café fraco com timer 10: termina e volta para idle |
| V2 | timer <= 30.0 | timer 31: passou do intervalo |
| V3 | timer >= 10.0 | timer 0: ainda não deu o tempo |
| V5 | modo = preparing_weak | timer 10, mas a máquina não está preparando café fraco |

### REQ005 · café forte pronto entre 30 e 50 → idle

> When the system mode is preparing strong coffee, and the request timer is greater than or equal to 30.0, and the request timer is lower than or equal to 50.0, the coffee machine system shall: assign idle to the system mode, assign strong to the coffee machine output.

**Guarda:** `the_system_mode = preparing_strong /\ the_request_timer >= 30.0 /\ the_request_timer <= 50.0`
**Ações:** `the_system_mode := idle`, `the_coffee_machine_output := strong`

| Linha | modo = preparing_strong | timer >= 30.0 | timer <= 50.0 | Saída | Possível | Na suíte | Valores (Z3) |
|---|---|---|---|---|---|---|---|
| V1 | T | T | T | **T** | sim | **sim** | modo = preparing_strong, timer = 30 |
| V2 | T | T | F | F | sim | **sim** | modo = preparing_strong, timer = 51 |
| V3 | T | F | T | F | sim | **sim** | modo = preparing_strong, timer = 0 |
| V4 | T | F | F | F | **não** | | — |
| V5 | F | T | T | F | sim | **sim** | modo = preparing_weak, timer = 30 |
| V6 | F | T | F | F | sim | | modo = preparing_weak, timer = 51 |
| V7 | F | F | T | F | sim | | modo = preparing_weak, timer = 0 |
| V8 | F | F | F | F | **não** | | — |

Mesma situação do REQ004: o timer não pode estar abaixo de 30 e acima de 50 ao mesmo tempo.

---

## 6. Testes de fronteira

O Z3 escolheu valores inteiros (31, 51), que já tornam as condições falsas. Para testar exatamente nas bordas de um timer real, use `--boundary`. No REQ004:

| Teste de origem | Fronteira | Valores |
|---|---|---|
| V1 | timer = 10.0 | modo = preparing_weak, timer = 10 |
| V1 | timer = 30.0 | modo = preparing_weak, timer = 30 |
| V2 | timer = 30.01 | modo = preparing_weak, timer = 30.01 |
| V3 | timer = 9.99 | modo = preparing_weak, timer = 9.99 |
| V5 | timer = 10.0 | modo = choice, timer = 10 |
| V5 | timer = 30.0 | modo = choice, timer = 30 |

O intervalo [10, 30] fica testado nas duas bordas, por dentro (10 e 30) e por fora (9,99 e 30,01).

---

## 7. Observações sobre os requisitos

| Observação | Requisitos |
|---|---|
| Os cinco têm cobertura MC/DC completa, sem condição redundante | todos |
| REQ002 e REQ003 se completam pelo timer: até 30 é fraco, depois de 30 é forte | REQ002, REQ003 |
| REQ004 e REQ005 compartilham o timer 30, mas não conflitam, porque o modo é diferente | REQ004, REQ005 |
| Intervalos de timer geram combinações impossíveis, que só o Z3 descobre | REQ004, REQ005 |
| As guardas são “and” puros: causa única e mascaramento dão os mesmos testes | todos |

---

## 8. Formatos de saída

| | JSON | CSV (`csv`) | CSV da tabela (`truth-csv`) |
|---|---|---|---|
| Tabela verdade inteira | sim (`truthTable`) | não | **sim** |
| Linhas impossíveis marcadas | sim (`feasible`) | não | sim (`feasible`) |
| Pares de independência | todos, e o escolhido | não | não |
| Testes escolhidos | sim (`minimalSuite`) | sim | sim (`in_suite`) |
| Valores do Z3 | sim (`assignment`, por linha) | sim (`concrete_values`, só nos testes) | sim (`concrete_values`, por linha) |
| Melhor para | o visualizador e outros programas | lista de testes numa planilha | ver a tabela verdade numa planilha |

### JSON

Cada decisão traz:

| Campo | O que traz |
|---|---|
| `id`, `requirement`, `guard`, `actions` | identificação da decisão |
| `inputs` | cada condição separada em variável, operador e valor |
| `conditions` | as condições, com o número da aparição |
| `truthTableRows` | quantas linhas tem a tabela |
| `truthTable` | todas as linhas: valores, saída, se é possível e, com `--z3`, os valores concretos |
| `independencePairs` | todos os pares de cada condição |
| `minimalSuite` | os testes escolhidos e o que cada um demonstra |
| `chosenPairs` | o par usado para cada condição, e se é de causa única |
| `complete`, `uncoveredConditions` | se a cobertura fechou e o que faltou |

Uma linha da tabela, com `--z3`:

```json
{
  "vector" : "V3",
  "values" : { "the_system_mode = idle" : false, "the_coin_sensor = true" : true },
  "outcome" : false,
  "assignment" : { "the_system_mode" : "choice", "the_coin_sensor" : "true" },
  "feasible" : true
}
```

### CSV dos testes (`--format csv`)

Uma linha por teste e por condição:

```
decision,requirement,test,input,value,expected_outcome,demonstrates,concrete_values
vm#4,REQ004,V1,the_system_mode = preparing_weak,T,T,the_system_mode = preparing_weak; ...,the_system_mode = preparing_weak; the_request_timer = 10
```

### CSV da tabela verdade (`--format truth-csv`)

Uma linha por combinação e uma coluna por condição. Cada requisito tem o seu cabeçalho, porque as condições mudam de um para outro, e os requisitos ficam separados por uma linha em branco.

```
decision,requirement,row,the_system_mode = preparing_weak,the_request_timer >= 10.0,the_request_timer <= 30.0,outcome,feasible,in_suite,demonstrates,concrete_values
vm#4,REQ004,V1,T,T,T,T,T,T,the_system_mode = preparing_weak; the_request_timer >= 10.0; the_request_timer <= 30.0,the_system_mode = preparing_weak; the_request_timer = 10
vm#4,REQ004,V4,T,F,F,F,F,F,,
```

| Coluna | O que é |
|---|---|
| `decision`, `requirement` | a decisão e o requisito |
| `row` | a linha da tabela (V1, V2, …) |
| uma coluna por condição | T ou F |
| `outcome` | a saída da guarda |
| `feasible` | F quando a linha é impossível |
| `in_suite` | T quando a linha é um dos testes escolhidos |
| `demonstrates` | as condições que o teste demonstra |
| `concrete_values` | os valores do Z3; vazio sem `--z3` ou em linha impossível |

Tabelas com mais de 4096 linhas (13 condições ou mais) não cabem no `truth-csv`; para elas, use JSON ou o CSV dos testes.

---

## Apêndice: avisos do zsh

Ao colar um bloco de comandos com linhas de comentário, o terminal mostra `zsh: command not found: #`. Não é erro da ferramenta: o zsh, por padrão, não aceita comentários digitados, e tenta rodar cada linha `#` como comando. Os comandos de verdade rodam normalmente. Para evitar o aviso:

```bash
setopt interactivecomments
```

Para valer sempre, acrescente essa linha ao `~/.zshrc`.
