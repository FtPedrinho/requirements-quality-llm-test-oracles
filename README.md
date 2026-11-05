# Ferramenta MC/DC

Gera, a partir de um requisito escrito como expressão lógica, a tabela verdade, os pares de independência de cada condição e a suíte mínima de testes que atinge MC/DC, dizendo qual par demonstra cada condição. Também mede o MC/DC de testes já existentes. Lê requisitos avulsos, arquivos `.mcdc` e o JSON de decisões extraído da NAT2TEST, e devolve o relatório em texto, JSON, CSV (testes ou tabela verdade inteira) ou Gherkin.

Fase 1: motor e modo requisitos. Arquitetura em [docs/arquitetura-fase1.md](docs/arquitetura-fase1.md); estado atual em [docs/implementacao-fase1.md](docs/implementacao-fase1.md).

## Rodar

Requer JDK 21 ou mais novo e Maven. A opção `--z3` precisa do Z3 instalado (`brew install z3`).

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
mvn clean verify      # compila e roda os testes
./mcdc analyze "(A and B) or C"
```

## Exemplos

```bash
# mascaramento (padrão) ou causa única
./mcdc analyze "(A and B) or C"
./mcdc analyze "(A and B) or C" --unique-cause

# comparações e os operadores do DFRS
./mcdc analyze 'speed > 100 /\ mode = idle'
./mcdc analyze '(A = x /\ B = y) \/ C'

# entrada repetida: cada ocorrência é uma condição com par próprio (A#1, A#2)
./mcdc analyze "(A and B) or (not A and C)"

# restrição entre condições escrita à mão: A = speed > 100 implica B = speed > 50
./mcdc analyze "A or (B and C)" --constraint "not A or B"

# o Z3 descobre as linhas impossíveis sozinho e dá valores concretos a cada teste
./mcdc analyze "speed > 100 or (speed > 50 and rain)" --z3

# ... e acrescenta variantes de fronteira (speed > 100 verdadeira -> speed = 101)
./mcdc analyze "speed > 100 or (speed > 50 and rain)" --z3 --boundary

# validação por mutação: a suíte detecta versões do requisito com uma falha?
./mcdc analyze "A and (B or C)" --mutation

# vários requisitos de um arquivo; REQ-003 tem condições redundantes
./mcdc analyze -f exemplos/requisitos.mcdc

# decisões no formato que o Extractor gera a partir do DFRS da NAT2TEST
./mcdc analyze --json exemplos/decisoes.json
./mcdc analyze --json exemplos/decisoes.json --z3

# os 5 requisitos originais da VM; resultados em docs/resultados.md
./mcdc analyze --json exemplos/vm-decisoes.json --z3

# relatório em JSON (o que volta para o Viewer), CSV ou Gherkin
./mcdc analyze --json exemplos/decisoes.json --format json | jq .
./mcdc analyze --json exemplos/decisoes.json --format csv -o suite.csv
./mcdc analyze --json exemplos/vm-decisoes.json --z3 --format truth-csv -o tabela.csv   # tabela verdade inteira
./mcdc analyze --json exemplos/decisoes.json --z3 --format gherkin -o suite.feature

# modo avaliação: quanto de MC/DC testes já existentes atingem e o que falta
./mcdc check --json exemplos/decisoes.json --tests exemplos/testes.csv
./mcdc check "(A and B) or C" --tests suite.csv
```

Use aspas simples quando a expressão tiver `\`, como em `/\` e `\/`.

| Operador | Formas aceitas |
|---|---|
| e | `and`, `&&`, `/\` |
| ou | `or`, `\|\|`, `\/` |
| não | `not`, `!` |
| comparação | `=`, `==`, `!=`, `<`, `<=`, `>`, `>=` |

Código de saída: `0` cobertura completa, `1` entrada inválida, `2` alguma condição sem par de independência (no `check`: alguma condição não demonstrada ou resultado esperado divergente).

## Módulos

| Módulo | Conteúdo |
|---|---|
| `mcdc-core` | Modelo da expressão e motor: tabela verdade, condições por ocorrência, pares, suíte mínima com rastreabilidade, diagnóstico de condição sem par, modo avaliação e validação por mutação. Sem dependências externas. |
| `mcdc-requirements` | Parser de expressões, leitura de arquivos `.mcdc`, do JSON da NAT2TEST e de testes existentes em CSV |
| `mcdc-z3` | Viabilidade das linhas, valores concretos e valores de fronteira com o Z3, por SMT-LIB |
| `mcdc-cli` | Comandos `mcdc analyze` e `mcdc check`; relatórios em texto, JSON, CSV dos testes, CSV da tabela verdade e Gherkin |
