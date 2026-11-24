# C0 — Resultados por caso

Rodada 1 = baseline original (3 casos com entrada inválida). Rodada 2 = baseline com as entradas corrigidas, que é o **resultado da suíte**. Extensão 1 = casos novos congelados à parte.

| ID | Comando | Oráculo | Rodada 1 | Rodada 2 / Extensão | Código | Detalhe |
|---|---|---|---|---|---|---|
| C0-A01 | `analyze "(A and B) or C"` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-A02 | `analyze "(A and B) or C" --format json` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-A03 | `analyze "(A and B) or C" --unique-cause --format json` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-A04 | `analyze "A and not B" --format json` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-A05 | `analyze "(A and B) or (not A and C)" --format json` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-A06 | `analyze "A or (A and B)" --format json` | DETERMINADO | PASSOU | **PASSOU** | 2 |  |
| C0-A07 | `analyze "A or (A and B)"` | DETERMINADO | PASSOU | **PASSOU** | 2 |  |
| C0-A08 | `analyze "A and B" --constraint "not A or not B" --format json` | DETERMINADO | PASSOU | **PASSOU** | 2 |  |
| C0-A09 | `analyze "A and B" --constraint "not A or not B"` | DETERMINADO | PASSOU | **PASSOU** | 2 |  |
| C0-A10 | `analyze "A or (B and C)" --constraint "not A or B" --format json` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-A11 | `analyze "((E or D) and (not A or D)) or B" --format json` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-A12 | `analyze "((E or D) and (not A or D)) or B" --exact --format json` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-A13 | `analyze "(A and B and C) or (A and not B and not C) or (not A and B and not C) or (not A a` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-A14 | `analyze "A1 and A2 and A3 and A4 and A5 and A6 and A7 and A8 and A9 and A10 and A11 and A1` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-A15 | `analyze "A1 and A2 and A3 and A4 and A5 and A6 and A7 and A8 and A9 and A10 and A11 and A1` | INDETERMINADO | INDETERMINADO | **INDETERMINADO** | 1 | observado (sem julgamento): Erro: Decisão com 21 entradas; o limite é 20 |
| C0-A16 | `analyze "A1 and A2 and A3 and A4 and A5 and A6 and A7 and A8 and A9 and A10 and A11 and A1` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-A17 | `analyze "A1 and A2 and A3 and A4 and A5 and A6 and A7 and A8 and A9 and A10 and A11 and A1` | INDETERMINADO | INDETERMINADO | **INDETERMINADO** | 1 | observado (sem julgamento): Erro: Decisão com 31 entradas; o limite do modo direto é 30 |
| C0-A18 | `analyze "A1 and A2 and A3 and A4 and A5 and A6 and A7 and A8 and A9 and A10 and A11 and A1` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-B01 | `analyze "A && B" --format truth-csv` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-B02 | `analyze "A /\ B" --format truth-csv` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-B03 | `analyze "A \|\| B" --format truth-csv` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-B04 | `analyze "A \/ B" --format truth-csv` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-B05 | `analyze "!A and B" --format truth-csv` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-B06 | `analyze "A or B and C" --format truth-csv` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-B07 | `analyze "(A and B) or C" --format truth-csv` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-B08 | `analyze "A or (B and C)" --constraint "not A or B" --format truth-csv` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-B09 | `analyze "speed > 100 /\ mode = idle"` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-B10 | `analyze "a == 1 or b != 2 or c < 3 or d <= 4 or e >= 5" --format json` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-B11 | `analyze "(A and B"` | DETERMINADO | PASSOU | **PASSOU** | 1 |  |
| C0-B12 | `analyze "A and or B"` | DETERMINADO | PASSOU | **PASSOU** | 1 |  |
| C0-B13 | `analyze ` | DETERMINADO | PASSOU | **PASSOU** | 1 |  |
| C0-B14 | `analyze "A and B" --format xml` | DETERMINADO | PASSOU | **PASSOU** | 1 |  |
| C0-B15 | `frobnicate A` | INDETERMINADO | INDETERMINADO | **INDETERMINADO** | 1 | observado (sem julgamento): Uso:   mcdc analyze <fonte> [opções]                gera a suíte mínima de testes MC/DC   mcdc check   <fonte> --tests < |
| C0-B16 | `` | INDETERMINADO | INDETERMINADO | **INDETERMINADO** | 1 | observado (sem julgamento): Uso:   mcdc analyze <fonte> [opções]                gera a suíte mínima de testes MC/DC   mcdc check   <fonte> --tests < |
| C0-B17 | `analyze "x > -5 and y < 3" --format json` | INDETERMINADO | INDETERMINADO | **INDETERMINADO** | 0 | observado (sem julgamento): {   "tool" : "mcdc",   "system" : null,   "variant" : "MASKING",   "constraint" : null,   "complete" : true,   "de |
| C0-C01 | `analyze "(A and B) or C" --format csv` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-C02 | `analyze "(A and B) or C" -o {OUT}/rel.txt` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-C03 | `analyze -f {IN}/requisitos-doc.mcdc --format json` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-C04 | `analyze -f {IN}/requisitos-erro.mcdc` | DETERMINADO | PASSOU | **PASSOU** | 1 |  |
| C0-C05 | `analyze -f {IN}/nao-existe.mcdc` | DETERMINADO | PASSOU | **PASSOU** | 1 |  |
| C0-C06 | `analyze -f exemplos/requisitos.mcdc` | DETERMINADO | PASSOU | **PASSOU** | 2 |  |
| C0-C07 | `analyze --json {IN}/cafe-doc.json --format json` | DETERMINADO | INVÁLIDO (entrada malformada; ver correcao-1) | **PASSOU** | 0 |  |
| C0-C08 | `analyze --json {IN}/cafe-doc.json --z3 --format json` | DETERMINADO | INVÁLIDO (entrada malformada; ver correcao-1) | **PASSOU** | 0 |  |
| C0-C09 | `analyze --json {IN}/temporal.json --z3` | DETERMINADO | INVÁLIDO (entrada malformada; ver correcao-1) | **PASSOU** | 0 |  |
| C0-C10 | `analyze --json {IN}/json-invalido.json` | DETERMINADO | PASSOU | **PASSOU** | 1 |  |
| C0-C11 | `analyze --json {IN}/ids-repetidos.json` | DETERMINADO | PASSOU | **PASSOU** | 1 |  |
| C0-C12 | `analyze -f {IN}/requisitos-doc.mcdc --constraint "not alarme_ativo"` | INDETERMINADO | INDETERMINADO | **INDETERMINADO** | 1 | observado (sem julgamento): Erro: --constraint só vale com uma expressão direta. |
| C0-D01 | `analyze "speed > 100 or (speed > 50 and rain)" --z3 --boundary --format json` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-D02 | `analyze "speed > 100 or (speed > 50 and rain)" --z3 --boundary` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-D03 | `analyze "speed > 100 or (speed > 50 and rain)" --boundary --format json` | INDETERMINADO | INDETERMINADO | **INDETERMINADO** | 1 | observado (sem julgamento): Erro: --boundary precisa de --z3. |
| C0-D04 | `analyze "speed > 100 or (speed > 50 and rain)" --z3` | DETERMINADO | PASSOU | **PASSOU** | 1 |  |
| C0-D05 | `verify --json {IN}/v-conflito.json` | DETERMINADO | PASSOU | **PASSOU** | 1 |  |
| C0-D06 | `analyze --json exemplos/vm-decisoes.json --direct --format json` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-D07 | `analyze "A and (B or C)" --mutation --format json` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-D08 | `analyze "A and (B or C)" --mutation` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-E01 | `analyze --json exemplos/vm-decisoes.json --z3 --mutation --format json` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-E02 | `analyze --json exemplos/tis-decisoes.json --z3 --mutation --format json` | DETERMINADO | PASSOU | **PASSOU** | 2 |  |
| C0-E03 | `analyze --json exemplos/npp-decisoes.json --z3 --mutation --format json` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-E04 | `verify --json exemplos/vm-decisoes.json --format json` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-E05 | `verify --json exemplos/tis-decisoes.json --format json` | DETERMINADO | PASSOU | **PASSOU** | 2 |  |
| C0-E06 | `verify --json exemplos/npp-decisoes.json` | DETERMINADO | PASSOU | **PASSOU** | 2 |  |
| C0-E07 | `verify --json exemplos/vm-decisoes.json --context "the_system_mode = preparing_weak"` | INDETERMINADO | INDETERMINADO | **INDETERMINADO** | 2 | observado (sem julgamento): Verificação entre requisitos: the_coffee_machine_system 5 decisões, 10 pares que escrevem alguma variável em comum  Conf |
| C0-E08 | `analyze --json exemplos/vm-decisoes.json --z3 --exact --format json` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-E09 | `analyze --json exemplos/npp-decisoes.json --z3 --unique-cause --format json` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-E10 | `analyze --json exemplos/tis-decisoes.json --z3 --format truth-csv -o {OUT}/tabela.csv` | DETERMINADO | PASSOU | **PASSOU** | 2 |  |
| C0-F01 | `check "(A and B) or C" --tests {IN}/testes-completos.csv` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-F02 | `check "(A and B) or C" --tests {IN}/testes-incompletos.csv --format json` | DETERMINADO | PASSOU | **PASSOU** | 2 |  |
| C0-F03 | `check "(A and B) or C" --tests {IN}/testes-esperado-errado.csv` | DETERMINADO | PASSOU | **PASSOU** | 2 |  |
| C0-F04 | `check "speed > 100 and rain" --tests {IN}/testes-concretos.csv` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-F05 | `check "(A and B) or C" --tests {IN}/testes-colunas-faltando.csv` | DETERMINADO | PASSOU | **PASSOU** | 1 |  |
| C0-F06 | `check "(A and B) or C" --tests {IN}/testes-completos.csv --format csv` | DETERMINADO | PASSOU | **PASSOU** | 1 |  |
| C0-F07 | `check "(A and B) or C"` | INDETERMINADO | INDETERMINADO | **INDETERMINADO** | 1 | observado (sem julgamento): Erro: check precisa de --tests <arquivo.csv>. |
| C0-F08 | `check --json exemplos/decisoes.json --tests exemplos/testes.csv` | INDETERMINADO | INDETERMINADO | **INDETERMINADO** | 2 | observado (sem julgamento): Decisão:   the_coffee_machine_system#1 Requisito: REQ-001 Guarda:    the_system_mode = idle /\ the_coin_sensor = true Te |
| C0-F09 | `check "(A and B) or C" --tests {IN}/testes-completos.csv --format json` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-F10 | `check "(A and B) or C" --tests {IN}/testes-incompletos.csv --unique-cause` | DETERMINADO | PASSOU | **PASSOU** | 2 |  |
| C0-G01 | `verify --json {IN}/v-conflito.json --format json` | DETERMINADO | PASSOU | **PASSOU** | 2 |  |
| C0-G02 | `verify --json {IN}/v-mesmo-valor.json` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-G03 | `verify --json {IN}/v-disjuntas.json` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-G04 | `verify --json {IN}/v-mesmo-valor.json --context "c = false"` | DETERMINADO | PASSOU | **PASSOU** | 2 |  |
| C0-G05 | `verify --json {IN}/v-disjuntas.json --context "d = true" --format json` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-G06 | `verify -f {IN}/requisitos-doc.mcdc` | INDETERMINADO | INDETERMINADO | **INDETERMINADO** | 0 | observado (sem julgamento): Verificação entre requisitos 2 decisões, 0 pares que escrevem alguma variável em comum  Conflitos: nenhum  Sobreposições |
| C0-G07 | `verify "A and B"` | INDETERMINADO | INDETERMINADO | **INDETERMINADO** | 0 | observado (sem julgamento): Verificação entre requisitos 1 decisões, 0 pares que escrevem alguma variável em comum  Conflitos: nenhum  Sobreposições |
| C0-G08 | `verify --json {IN}/v-conflito.json` | DETERMINADO | PASSOU | **PASSOU** | 2 |  |
| C0-G09 | `analyze "(A and B) or (not A and C)" --unique-cause --format json` | INDETERMINADO | INDETERMINADO | **INDETERMINADO** | 0 | observado (sem julgamento): {   "tool" : "mcdc",   "system" : null,   "variant" : "UNIQUE_CAUSE",   "constraint" : null,   "complete" : true,  |
| C0-G10 | `analyze "(A and B) or C" --mutation --unique-cause --format json` | DETERMINADO | PASSOU | **PASSOU** | 0 |  |
| C0-X01 | `analyze "x > 3 or (y <= x and mode != idle)" --z3 --boundary --format json` | DETERMINADO | — | **PASSOU** | 0 |  |
| C0-X02 | `analyze "x >= 5 and x < 10 or z == 3" --z3 --boundary --format json` | DETERMINADO | — | **PASSOU** | 0 |  |
| C0-X03 | `analyze "x > 5 and x < 3 or b" --z3 --format json` | DETERMINADO | — | **PASSOU** | 2 |  |
| C0-X04 | `analyze "x > 5 and x < 3 or b" --direct --format json` | DETERMINADO | — | **PASSOU** | 2 |  |
| C0-X05 | `analyze "A or (A and B)" --direct --format json` | DETERMINADO | — | **PASSOU** | 2 |  |
| C0-X06 | `analyze "(A and B) or C" --direct --unique-cause --format json` | DETERMINADO | — | **PASSOU** | 0 |  |
| C0-X07 | `analyze "speed > 100 or (speed > 50 and rain)" --direct --format json` | DETERMINADO | — | **PASSOU** | 0 |  |
| C0-X08 | `analyze "(A and B) or C" --exact --unique-cause --format json` | DETERMINADO | — | **PASSOU** | 0 |  |
| C0-X09 | `analyze "(A and B) or C" --exact --format json` | DETERMINADO | — | **PASSOU** | 0 |  |
| C0-X10 | `analyze "speed > 100 or (speed > 50 and rain)" --z3 --boundary --format csv` | DETERMINADO | — | **PASSOU** | 0 |  |
| C0-X11 | `check --json {INX}/dois-requisitos.json --tests {INX}/testes-com-decisao.csv` | DETERMINADO | — | **PASSOU** | 0 |  |
| C0-X12 | `check "(A and B) or C" --tests {INX}/testes-aspas.csv` | DETERMINADO | — | **PASSOU** | 0 |  |
| C0-X13 | `check "(A and B) or C" --tests {INX}/testes-valor-invalido.csv` | DETERMINADO | — | **FALHOU** | 1 | contains:4:  |
| C0-X14 | `check "(A and B) or C" --tests {IN}/testes-esperado-errado.csv --format json` | DETERMINADO | — | **PASSOU** | 2 |  |
| C0-X15 | `verify --json {IN}/v-mesmo-valor.json --context "c = false" --format json` | DETERMINADO | — | **PASSOU** | 2 |  |
| C0-X16 | `analyze "not (A and B) or C" --mutation --format json` | DETERMINADO | — | **PASSOU** | 0 |  |
| C0-X17 | `analyze "(A and B) or C" --unique-cause` | DETERMINADO | — | **PASSOU** | 0 |  |
| C0-X18 | `analyze "A or (B and C)" --constraint "not A or B"` | DETERMINADO | — | **PASSOU** | 0 |  |
| C0-X19 | `analyze --json {INX}/sem-guarda.json` | DETERMINADO | — | **PASSOU** | 1 |  |
| C0-X20 | `analyze --json {IN}/cafe-doc.json --z3 --boundary --format csv` | DETERMINADO | — | **PASSOU** | 0 |  |
| C0-X21 | `analyze "(A and B) or C" --format truth-csv -o {OUT}/t.csv` | DETERMINADO | — | **PASSOU** | 0 |  |
| C0-X22 | `verify --json {IN}/v-conflito.json --z3` | INDETERMINADO | — | **INDETERMINADO** | 1 | observado (sem julgamento): Erro: verify aceita só a fonte, --context, --format e -o. |
