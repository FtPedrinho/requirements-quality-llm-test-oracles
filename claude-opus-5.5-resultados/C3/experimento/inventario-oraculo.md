# Inventário do oráculo C3

Gerado por `casos.py` a partir de `tool-readme-C3.md` (SHA-256 F18B0821…7A3). Linhas [Lnn] referem-se à fonte.

Casos: 75 — determinados: 36, indeterminados: 39.

## C3-T01 — Tabela-verdade de (A and B) or C (DETERMINADO)

- Entrada: `mcdc analyze (A and B) or C`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L37] Gerar os testes | `mcdc analyze` | Tabela verdade, pares de independência, suíte de testes e o par que demonstra cada condição
  - [L291] tabela-verdade: para as entradas distintas da expressão, são consideradas as 2ⁿ combinações e calculado o resultado da guarda em cada uma
  - [L515] `TruthTableTest` | Uma linha por combinação; a linha 0 é tudo verdadeiro; a saída de cada linha; restrições; limite de 20 entradas
  - [L137-143] e: `and`, `&&`, `/\` | ou: `or`, `\|\|`, `\/` | não: `not`, `!` | comparação: `=`, `==`, `!=`, `<`, `<=`, `>`, `>=`
- Regra: Para n entradas distintas, 2ⁿ combinações com o resultado da guarda; a linha 0 tem todas as entradas verdadeiras.
- Expectativa: A saída apresenta a tabela-verdade com 8 combinações; em cada uma o resultado é (A∧B)∨C (Z3); a primeira linha (linha 0) é A=B=C=T. Componentes não julgados: código de saída (K3).
- Justificativa: Sem entrada repetida, sem Z3: nenhum conflito K atinge a tabela-verdade.
- Conflitos considerados: K1(não se aplica), K3
- Evidências Z3: Z01_tt_ABorC

## C3-T02 — Operadores && e || (DETERMINADO)

- Entrada: `mcdc analyze (A && B) || C`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L137-143] e: `and`, `&&`, `/\` | ou: `or`, `\|\|`, `\/` | não: `not`, `!` | comparação: `=`, `==`, `!=`, `<`, `<=`, `>`, `>=`
  - [L291] tabela-verdade: para as entradas distintas da expressão, são consideradas as 2ⁿ combinações e calculado o resultado da guarda em cada uma
- Regra: `&&` é e, `||` é ou.
- Expectativa: Tabela-verdade com 8 combinações idêntica à de (A and B) or C. Componentes não julgados: código de saída (K3).
- Justificativa: Formas aceitas listadas sem conflito.
- Conflitos considerados: K3
- Evidências Z3: Z01_tt_amp, Z02_eq_amp

## C3-T03 — Operadores DFRS e precedência (DETERMINADO)

- Entrada: `mcdc analyze A /\ B \/ C`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L137-143] e: `and`, `&&`, `/\` | ou: `or`, `\|\|`, `\/` | não: `not`, `!` | comparação: `=`, `==`, `!=`, `<`, `<=`, `>`, `>=`
  - [L545] `ExpressionParserTest` | Precedência (e antes de ou), parênteses, comparações, operadores do DFRS; expressões inválidas recusadas
  - [L291] tabela-verdade: para as entradas distintas da expressão, são consideradas as 2ⁿ combinações e calculado o resultado da guarda em cada uma
- Regra: `/\` é e, `\/` é ou; e tem precedência sobre ou.
- Expectativa: Tabela-verdade com 8 combinações igual a (A∧B)∨C. Componentes não julgados: código de saída (K3).
- Justificativa: Operadores e precedência explícitos.
- Conflitos considerados: K3
- Evidências Z3: Z01_tt_dfrs, Z02_eq_dfrs

## C3-T04 — Precedência e antes de ou (DETERMINADO)

- Entrada: `mcdc analyze A or B and C`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L545] `ExpressionParserTest` | Precedência (e antes de ou), parênteses, comparações, operadores do DFRS; expressões inválidas recusadas
  - [L291] tabela-verdade: para as entradas distintas da expressão, são consideradas as 2ⁿ combinações e calculado o resultado da guarda em cada uma
- Regra: e antes de ou: A or B and C = A ∨ (B ∧ C).
- Expectativa: Tabela-verdade com 8 combinações de A∨(B∧C). Componentes não julgados: código de saída (K3).
- Justificativa: Precedência explícita na descrição do ExpressionParserTest.
- Conflitos considerados: K3
- Evidências Z3: Z01_tt_prec, Z02_eq_prec

## C3-T05 — Negação com not (DETERMINADO)

- Entrada: `mcdc analyze not A and B`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L137-143] e: `and`, `&&`, `/\` | ou: `or`, `\|\|`, `\/` | não: `not`, `!` | comparação: `=`, `==`, `!=`, `<`, `<=`, `>`, `>=`
  - [L291] tabela-verdade: para as entradas distintas da expressão, são consideradas as 2ⁿ combinações e calculado o resultado da guarda em cada uma
- Regra: `not` é negação.
- Expectativa: Tabela-verdade com 4 combinações de ¬A∧B. Componentes não julgados: código de saída (K3).
- Justificativa: Operador listado.
- Conflitos considerados: K3
- Evidências Z3: Z01_tt_notA

## C3-T06 — Negação com ! (DETERMINADO)

- Entrada: `mcdc analyze !A and B`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L137-143] e: `and`, `&&`, `/\` | ou: `or`, `\|\|`, `\/` | não: `not`, `!` | comparação: `=`, `==`, `!=`, `<`, `<=`, `>`, `>=`
  - [L291] tabela-verdade: para as entradas distintas da expressão, são consideradas as 2ⁿ combinações e calculado o resultado da guarda em cada uma
- Regra: `!` é negação.
- Expectativa: Tabela-verdade com 4 combinações de ¬A∧B (igual a C3-T05). Componentes não julgados: código de saída (K3).
- Justificativa: Operador listado.
- Conflitos considerados: K3
- Evidências Z3: Z01_tt_bangA, Z02_eq_not

## C3-T07 — Comparações como entradas (DETERMINADO)

- Entrada: `mcdc analyze speed > 100 /\ mode = idle`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L137-143] e: `and`, `&&`, `/\` | ou: `or`, `\|\|`, `\/` | não: `not`, `!` | comparação: `=`, `==`, `!=`, `<`, `<=`, `>`, `>=`
  - [L291] tabela-verdade: para as entradas distintas da expressão, são consideradas as 2ⁿ combinações e calculado o resultado da guarda em cada uma
  - [L243] # restrição escrita à mão: A = speed > 100 implica B = speed > 50
- Regra: Cada comparação é uma entrada lógica (A = speed > 100).
- Expectativa: Tabela-verdade com 2 entradas (speed > 100, mode = idle) e 4 combinações; resultado = conjunção. Componentes não julgados: código de saída (K3).
- Justificativa: Decisão A1 da análise: comparações são entradas, conforme L243 e L41.
- Conflitos considerados: K3
- Evidências Z3: Z01_tt_cmp

## C3-T08 — Pares no mascaramento: cada condição demonstrada (DETERMINADO)

- Entrada: `mcdc analyze (A and B) or C`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L37] Gerar os testes | `mcdc analyze` | Tabela verdade, pares de independência, suíte de testes e o par que demonstra cada condição
  - [L297] pares de independência: para cada condição, são procurados dois testes possíveis nos quais essa condição muda, o resultado da decisão também muda e a condição satisfaz o critério da variante de MC/DC selecionada
  - [L299] Critério simplificado: para demonstrar MC/DC, basta que a condição mude entre dois testes; o resultado da decisão pode permanecer igual.
  - [L55] As duas variantes de MC/DC são suportadas: **mascaramento** (padrão) e **causa única** (`--unique-cause`).
- Regra: Para cada condição há um par; todo par reportado muda a condição; a suíte contém, para cada condição, dois testes em que ela muda.
- Expectativa: As 3 condições (A, B, C) aparecem como demonstradas (nenhuma sem par); em cada par reportado a condição tem valores diferentes; a suíte tem, para cada condição, dois testes em que ela difere. Componentes não julgados: código de saída (K3).
- Justificativa: K7 (critério estrito × simplificado) não altera estas propriedades: Z3 mostra par sat nos três critérios para A, B e C; todo par estrito muda a condição. A exigência de mudança do resultado fica de fora (C3-I09).
- Conflitos considerados: K7, K3
- Evidências Z3: Z03_pares_ABorC

## C3-T09 — Pares na causa única: cada condição demonstrada (DETERMINADO)

- Entrada: `mcdc analyze (A and B) or C --unique-cause`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L55] As duas variantes de MC/DC são suportadas: **mascaramento** (padrão) e **causa única** (`--unique-cause`).
  - [L297] pares de independência: para cada condição, são procurados dois testes possíveis nos quais essa condição muda, o resultado da decisão também muda e a condição satisfaz o critério da variante de MC/DC selecionada
  - [L299] Critério simplificado: para demonstrar MC/DC, basta que a condição mude entre dois testes; o resultado da decisão pode permanecer igual.
- Regra: Causa única: idem C3-T08 na variante --unique-cause.
- Expectativa: As 3 condições demonstradas; cada par reportado muda a condição; suíte alterna cada condição. Componentes não julgados: código de saída (K3).
- Justificativa: Par de causa única sat para A, B, C (Z3).
- Conflitos considerados: K7, K3
- Evidências Z3: Z03_pares_ABorC

## C3-T10 — Tabela-verdade com entrada repetida (DETERMINADO)

- Entrada: `mcdc analyze (A and B) or (not A and C)`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L291] tabela-verdade: para as entradas distintas da expressão, são consideradas as 2ⁿ combinações e calculado o resultado da guarda em cada uma
  - [L55] entrada é uma variável distinta da expressão; condição é cada ocorrência de uma entrada na expressão
- Regra: A tabela é montada sobre as entradas distintas (A, B, C).
- Expectativa: Tabela-verdade com 8 combinações e resultados de (A∧B)∨(¬A∧C). Componentes não julgados: código de saída (K3).
- Justificativa: K1 diverge só na contagem de condições; nas duas leituras há 3 entradas distintas (L55 e L57), logo 2³ combinações.
- Conflitos considerados: K1, K3
- Evidências Z3: Z01_tt_rep, K01_contagem_condicoes_juntas

## C3-T11 — Expressão inválida: parêntese aberto (DETERMINADO)

- Entrada: `mcdc analyze (A and B`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L545] `ExpressionParserTest` | Precedência (e antes de ou), parênteses, comparações, operadores do DFRS; expressões inválidas recusadas
  - [L579] `MainTest` | Os três comandos, as fontes, os formatos, o código de saída 0, 1 ou 2, entradas inválidas
- Regra: Expressões inválidas são recusadas.
- Expectativa: A ferramenta recusa a expressão: não apresenta análise (tabela/suíte) e emite mensagem de erro. Componentes não julgados: código de saída (K3).
- Justificativa: ExpressionParserTest: 'expressões inválidas recusadas'. O código (1 ou 0) é K3.
- Conflitos considerados: K3
- Evidências Z3: —

## C3-T12 — Expressão inválida: operando ausente (DETERMINADO)

- Entrada: `mcdc analyze A and`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L545] `ExpressionParserTest` | Precedência (e antes de ou), parênteses, comparações, operadores do DFRS; expressões inválidas recusadas
- Regra: Expressões inválidas são recusadas.
- Expectativa: Recusa: sem análise, com mensagem de erro. Componentes não julgados: código de saída (K3).
- Justificativa: Idem C3-T11.
- Conflitos considerados: K3
- Evidências Z3: —

## C3-T13 — Arquivo .mcdc de exemplo (DETERMINADO)

- Entrada: `mcdc analyze -f {EX}/requisitos.mcdc`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L151] **Arquivo `.mcdc`:** um requisito por linha, `ID: expressão`. Linhas com `#` são comentários.
  - [L291] tabela-verdade: para as entradas distintas da expressão, são consideradas as 2ⁿ combinações e calculado o resultado da guarda em cada uma
- Regra: Um requisito por linha `ID: expressão`; `#` é comentário.
- Expectativa: A saída analisa exatamente REQ-001, REQ-002 e REQ-003 (comentário não vira requisito); tabelas com 8, 4 e 4 combinações e resultados conforme Z3. Componentes não julgados: código de saída (K3).
- Justificativa: Formato explícito; a tabela de REQ-003 usa as 2 entradas distintas (K1 não afeta).
- Conflitos considerados: K1, K3
- Evidências Z3: Z01_tt_req1, Z01_tt_req2, Z01_tt_req3

## C3-T14 — Arquivo .mcdc com erro de sintaxe (DETERMINADO)

- Entrada: `mcdc analyze -f {ENT}/erro-sintaxe.mcdc`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L547] `RequirementsFileTest` | Arquivo `.mcdc`, comentários, linha sem identificador, erro de sintaxe com o requisito
  - [L545] `ExpressionParserTest` | Precedência (e antes de ou), parênteses, comparações, operadores do DFRS; expressões inválidas recusadas
- Regra: Erro de sintaxe é recusado e reportado com o requisito.
- Expectativa: Recusa sem análise; a mensagem de erro identifica o requisito REQ-ERRO. Componentes não julgados: código de saída (K3).
- Justificativa: RequirementsFileTest: 'erro de sintaxe com o requisito' + expressões inválidas recusadas.
- Conflitos considerados: K3
- Evidências Z3: —

## C3-T15vm — JSON NAT2TEST VM: contagens e rastreabilidade (DETERMINADO)

- Entrada: `mcdc analyze --json {EX}/vm-decisoes.json --format json`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L161] **JSON de decisões** (formato do Extractor da NAT2TEST): contém as variáveis e seus tipos, além das decisões, cada uma com sua guarda e suas ações.
  - [L213] `json` | Resultado completo de cada decisão, ligado ao requisito de origem (formato de integração)
  - [L501-507, tabela transcrita] VM: 5 requisitos, 21 condições, 152 combinações, 4 impossíveis, 26 testes, 152 mutantes, 0 equivalentes, 152 pegos, 0 conflitos | TIS: 17, 14 completos, 69, 268, 4, 80, 450, 21, 428, 3 | NPP: 11, 11, 29, 76, 1, 40, 146, 0, 146, 1
  - [L291] tabela-verdade: para as entradas distintas da expressão, são consideradas as 2ⁿ combinações e calculado o resultado da guarda em cada uma
- Regra: Resultado JSON por decisão ligado ao requisito; números da regressão independentes de K1/K6/K7.
- Expectativa: JSON com 5 decisões, cada uma ligada ao seu requisito (REQ001…REQ005); soma das combinações = 152; soma das condições = 21. Componentes não julgados: código de saída (K3).
- Justificativa: Nenhuma guarda de VM repete entrada (K1 não afeta 21); combinações = Σ2ⁿ conferida com Z3.
- Conflitos considerados: K1, K3
- Evidências Z3: Z13_combinacoes_sistemas

## C3-T15npp — JSON NAT2TEST NPP: contagens e rastreabilidade (DETERMINADO)

- Entrada: `mcdc analyze --json {EX}/npp-decisoes.json --format json`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L161] **JSON de decisões** (formato do Extractor da NAT2TEST): contém as variáveis e seus tipos, além das decisões, cada uma com sua guarda e suas ações.
  - [L213] `json` | Resultado completo de cada decisão, ligado ao requisito de origem (formato de integração)
  - [L501-507, tabela transcrita] VM: 5 requisitos, 21 condições, 152 combinações, 4 impossíveis, 26 testes, 152 mutantes, 0 equivalentes, 152 pegos, 0 conflitos | TIS: 17, 14 completos, 69, 268, 4, 80, 450, 21, 428, 3 | NPP: 11, 11, 29, 76, 1, 40, 146, 0, 146, 1
  - [L291] tabela-verdade: para as entradas distintas da expressão, são consideradas as 2ⁿ combinações e calculado o resultado da guarda em cada uma
- Regra: Resultado JSON por decisão ligado ao requisito; números da regressão independentes de K1/K6/K7.
- Expectativa: JSON com 11 decisões, cada uma ligada ao seu requisito (REQ001…REQ011); soma das combinações = 76; soma das condições = 29. Componentes não julgados: código de saída (K3).
- Justificativa: Nenhuma guarda de NPP repete entrada (K1 não afeta 29); combinações = Σ2ⁿ conferida com Z3.
- Conflitos considerados: K1, K3
- Evidências Z3: Z13_combinacoes_sistemas

## C3-T15tis — JSON NAT2TEST TIS: decisões e combinações (DETERMINADO)

- Entrada: `mcdc analyze --json {EX}/tis-decisoes.json --format json`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L161] **JSON de decisões** (formato do Extractor da NAT2TEST): contém as variáveis e seus tipos, além das decisões, cada uma com sua guarda e suas ações.
  - [L213] `json` | Resultado completo de cada decisão, ligado ao requisito de origem (formato de integração)
  - [L501-507, tabela transcrita] VM: 5 requisitos, 21 condições, 152 combinações, 4 impossíveis, 26 testes, 152 mutantes, 0 equivalentes, 152 pegos, 0 conflitos | TIS: 17, 14 completos, 69, 268, 4, 80, 450, 21, 428, 3 | NPP: 11, 11, 29, 76, 1, 40, 146, 0, 146, 1
  - [L291] tabela-verdade: para as entradas distintas da expressão, são consideradas as 2ⁿ combinações e calculado o resultado da guarda em cada uma
- Regra: Idem; condições do TIS ficam fora (K1, ver C3-I26).
- Expectativa: JSON com 17 decisões ligadas aos requisitos REQ001…REQ017; soma das combinações = 268. Componentes não julgados: código de saída (K3).
- Justificativa: Combinações dependem das entradas distintas (Σ2ⁿ = 268, Z3).
- Conflitos considerados: K1, K3
- Evidências Z3: Z13_combinacoes_sistemas

## C3-T16 — Mutação: tipos de defeito (DETERMINADO)

- Entrada: `mcdc analyze A and (B or C) --mutation`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L49] Validar a suíte | `--mutation` | Versões do requisito com um defeito cada (seis tipos) e quais os testes pegam
  - [L309] mutação (opcional): são avaliados seis tipos de defeito de Kapoor e Bowen (ORF, ENF, VNF, MVF, VRF, ASF); versões equivalentes ao requisito original não entram na contagem
- Regra: Os mutantes pertencem aos seis tipos ORF, ENF, VNF, MVF, VRF, ASF.
- Expectativa: A saída traz a análise de mutação; todo tipo de mutante citado ∈ {ORF, ENF, VNF, MVF, VRF, ASF}; há ao menos um mutante. Componentes não julgados: código de saída (K3).
- Justificativa: Lista fechada de seis tipos; detecção fica fora (K7/K14).
- Conflitos considerados: K7, K14, K3
- Evidências Z3: —

## C3-T17vm — Mutação VM: total de mutantes (DETERMINADO)

- Entrada: `mcdc analyze --json {EX}/vm-decisoes.json --mutation --format json`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L501-507, tabela transcrita] VM: 5 requisitos, 21 condições, 152 combinações, 4 impossíveis, 26 testes, 152 mutantes, 0 equivalentes, 152 pegos, 0 conflitos | TIS: 17, 14 completos, 69, 268, 4, 80, 450, 21, 428, 3 | NPP: 11, 11, 29, 76, 1, 40, 146, 0, 146, 1
  - [L309] mutação (opcional): são avaliados seis tipos de defeito de Kapoor e Bowen (ORF, ENF, VNF, MVF, VRF, ASF); versões equivalentes ao requisito original não entram na contagem
- Regra: Total de mutantes da regressão (inclui equivalentes, ver nota).
- Expectativa: Total de mutantes gerados para VM = 152. Componentes não julgados: código de saída (K3).
- Justificativa: A coluna 'Mutantes' inclui equivalentes (TIS: 450 − 21 = 429 detectáveis, 428 pegos, 1 escapou = L619). Geração sintática: não depende de K6/K7; sem repetição, K1 não afeta. Equivalentes e pegos ficam fora.
- Conflitos considerados: K1, K7, K14, K3
- Evidências Z3: —

## C3-T17npp — Mutação NPP: total de mutantes (DETERMINADO)

- Entrada: `mcdc analyze --json {EX}/npp-decisoes.json --mutation --format json`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L501-507, tabela transcrita] VM: 5 requisitos, 21 condições, 152 combinações, 4 impossíveis, 26 testes, 152 mutantes, 0 equivalentes, 152 pegos, 0 conflitos | TIS: 17, 14 completos, 69, 268, 4, 80, 450, 21, 428, 3 | NPP: 11, 11, 29, 76, 1, 40, 146, 0, 146, 1
  - [L309] mutação (opcional): são avaliados seis tipos de defeito de Kapoor e Bowen (ORF, ENF, VNF, MVF, VRF, ASF); versões equivalentes ao requisito original não entram na contagem
- Regra: Total de mutantes da regressão (inclui equivalentes, ver nota).
- Expectativa: Total de mutantes gerados para NPP = 146. Componentes não julgados: código de saída (K3).
- Justificativa: A coluna 'Mutantes' inclui equivalentes (TIS: 450 − 21 = 429 detectáveis, 428 pegos, 1 escapou = L619). Geração sintática: não depende de K6/K7; sem repetição, K1 não afeta. Equivalentes e pegos ficam fora.
- Conflitos considerados: K1, K7, K14, K3
- Evidências Z3: —

## C3-T18 — Saída em arquivo com -o (DETERMINADO)

- Entrada: `mcdc analyze (A and B) or C -o {OUT}/relatorio.txt`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L129] `-o <arquivo>` | Grava o relatório no arquivo em vez de mostrar na tela
- Regra: -o grava o relatório no arquivo em vez da tela.
- Expectativa: O arquivo existe e contém o relatório (tabela-verdade de (A and B) or C); a saída padrão não contém o relatório. Componentes não julgados: código de saída (K3).
- Justificativa: Opção explícita.
- Conflitos considerados: K3
- Evidências Z3: —

## C3-T19 — Formato json no analyze (DETERMINADO)

- Entrada: `mcdc analyze (A and B) or C --format json`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L127] `--format <formato>` | `text` (padrão), `json`, `csv` (suíte) ou `truth-csv` (tabela-verdade inteira); `check` e `verify` aceitam `text` e `json`
  - [L213] `json` | Resultado completo de cada decisão, ligado ao requisito de origem (formato de integração)
- Regra: `json` produz o resultado completo da decisão.
- Expectativa: Saída é JSON válido com o resultado da decisão (tabela de 8 combinações). Componentes não julgados: código de saída (K3).
- Justificativa: Formato json sem conflito (K5 só atinge csv/truth-csv).
- Conflitos considerados: K5, K3
- Evidências Z3: Z01_tt_ABorC

## C3-T20 — check: suíte completa (DETERMINADO)

- Entrada: `mcdc check (A and B) or C --tests {ENT}/check-completa.csv`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L51] Avaliar testes existentes | `mcdc check` | Cobertura MC/DC de um conjunto de testes, o que falta e testes com resultado esperado errado
  - [L191] cada linha associa um teste a uma entrada e ao valor atribuído a essa entrada. O valor pode ser lógico (`T`/`F`) ou concreto, conforme o tipo da variável. As colunas `decision` e `expected_outcome` são opcionais.
  - [L83-87] mcdc analyze <fonte> [opções] | mcdc check <fonte> --tests <testes.csv> | mcdc verify <fonte> [--context "<expr>"]
- Regra: check mede a cobertura MC/DC dos testes, o que falta e esperados errados.
- Expectativa: As 3 condições demonstradas (cobertura completa), nada faltando, nenhum teste com resultado esperado errado. Componentes não julgados: código de saída (K3).
- Justificativa: Os pares (T1,T2) A, (T1,T3) B, (T3,T4) C são de causa única: válidos nas duas leituras de K7. Esperados = guarda (Z3).
- Conflitos considerados: K7, K3
- Evidências Z3: Z11_check_check-completa, Z03_pares_ABorC

## C3-T21 — check: um teste só (DETERMINADO)

- Entrada: `mcdc check (A and B) or C --tests {ENT}/check-um-teste.csv`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L51] Avaliar testes existentes | `mcdc check` | Cobertura MC/DC de um conjunto de testes, o que falta e testes com resultado esperado errado
  - [L297] pares de independência: para cada condição, são procurados dois testes possíveis nos quais essa condição muda, o resultado da decisão também muda e a condição satisfaz o critério da variante de MC/DC selecionada
  - [L299] Critério simplificado: para demonstrar MC/DC, basta que a condição mude entre dois testes; o resultado da decisão pode permanecer igual.
- Regra: Um par exige dois testes.
- Expectativa: Nenhuma condição demonstrada; A, B e C apontadas como faltando; nenhum esperado errado. Componentes não julgados: código de saída (K3).
- Justificativa: Tanto o critério estrito quanto o simplificado exigem dois testes.
- Conflitos considerados: K7, K3
- Evidências Z3: Z11_check_check-um-teste

## C3-T22 — check: resultado esperado errado (DETERMINADO)

- Entrada: `mcdc check (A and B) or C --tests {ENT}/check-esperado-errado.csv`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L51] Avaliar testes existentes | `mcdc check` | Cobertura MC/DC de um conjunto de testes, o que falta e testes com resultado esperado errado
  - [L145] **Código de saída:** `0`: comando concluído sem apontar os problemas descritos para o código `2`; `1`: entrada inválida; `2`: resultado válido do processamento, mas com uma condição sem par no `analyze`, [...] um resultado esperado divergente no `check`, ou um conflito ou uma lacuna no `verify`.
- Regra: check aponta testes com resultado esperado errado.
- Expectativa: Apenas T2 apontado como resultado esperado divergente (guarda dá F, esperado T). Componentes não julgados: código de saída (K3).
- Justificativa: Avaliação da guarda pelo Z3.
- Conflitos considerados: K3
- Evidências Z3: Z11_check_check-esperado-errado

## C3-T23 — check: CSV sem coluna value (DETERMINADO)

- Entrada: `mcdc check (A and B) or C --tests {ENT}/check-sem-coluna-value.csv`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L191] cada linha associa um teste a uma entrada e ao valor atribuído a essa entrada. O valor pode ser lógico (`T`/`F`) ou concreto, conforme o tipo da variável. As colunas `decision` e `expected_outcome` são opcionais.
  - [L551] `TestCasesFileTest` | CSV de testes, com e sem a coluna de decisão; colunas faltando
- Regra: test, input e value são as colunas obrigatórias implícitas; 'colunas faltando' é erro.
- Expectativa: A ferramenta recusa o CSV (sem avaliação, com mensagem de erro). Componentes não julgados: código de saída (K3).
- Justificativa: K4 só trata de decision/expected_outcome; sem value não há valor a avaliar.
- Conflitos considerados: K4, K3
- Evidências Z3: —

## C3-T24 — check com exemplos/decisoes.json e testes.csv (DETERMINADO)

- Entrada: `mcdc check --json {EX}/decisoes.json --tests {EX}/testes.csv`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L281] ./mcdc check --json exemplos/decisoes.json --tests exemplos/testes.csv
  - [L51] Avaliar testes existentes | `mcdc check` | Cobertura MC/DC de um conjunto de testes, o que falta e testes com resultado esperado errado
  - [L191] cada linha associa um teste a uma entrada e ao valor atribuído a essa entrada. O valor pode ser lógico (`T`/`F`) ou concreto, conforme o tipo da variável. As colunas `decision` e `expected_outcome` são opcionais.
- Regra: Valores concretos avaliados pela guarda; esperado divergente apontado.
- Expectativa: Somente T4 apontado com resultado esperado errado (guarda #3 dá F). Decisão #1: the_coin_sensor = true demonstrada; the_system_mode = idle não. Decisão #3: the_coffee_request_button = true e the_coin_sensor = true não demonstradas. Componentes não julgados: código de saída (K3).
- Justificativa: T1/T2 mudam só the_coin_sensor e o resultado (par válido nas duas leituras K7); em #3 o botão e a moeda não mudam. A demonstração de the_system_mode = choice em #3 depende de K7 e do uso do esperado errado de T4: não julgada.
- Conflitos considerados: K7, K3
- Evidências Z3: Z12_decisoes_testes

## C3-T25 — check com formato json (DETERMINADO)

- Entrada: `mcdc check (A and B) or C --tests {ENT}/check-completa.csv --format json`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L127] `--format <formato>` | `text` (padrão), `json`, `csv` (suíte) ou `truth-csv` (tabela-verdade inteira); `check` e `verify` aceitam `text` e `json`
  - [L51] Avaliar testes existentes | `mcdc check` | Cobertura MC/DC de um conjunto de testes, o que falta e testes com resultado esperado errado
- Regra: check aceita json.
- Expectativa: Saída é JSON válido. Componentes não julgados: código de saída (K3).
- Justificativa: L127.
- Conflitos considerados: K3
- Evidências Z3: —

## C3-T26 — verify sem --context não aponta lacunas (DETERMINADO)

- Entrada: `mcdc verify --json {EX}/npp-decisoes.json`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L53] Revisar os requisitos entre si | `mcdc verify` | Conflitos (dois requisitos valem juntos e escrevem valores diferentes) e lacunas (nenhum requisito vale)
  - [L125] `--context "<expr>"` | No `verify`: confere se, nessa situação, sempre alguma guarda vale
  - [L567] `Z3RequirementsVerifierTest` | Conflitos, guardas que não se sobrepõem, mesmo valor sem conflito, lacunas só com contexto
- Regra: Lacunas só com contexto.
- Expectativa: Nenhuma lacuna é apontada. Componentes não julgados: código de saída (K3).
- Justificativa: Z3RequirementsVerifierTest: 'lacunas só com contexto'. A contagem de conflitos fica fora (K6).
- Conflitos considerados: K6, K3
- Evidências Z3: —

## C3-T27 — Fronteiras de speed > 100 e speed > 50 (DETERMINADO)

- Entrada: `mcdc analyze speed > 100 or (speed > 50 and rain) --z3 --boundary`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L43] Testes de fronteira | `--z3 --boundary` | Variações no limite de cada comparação (`speed > 100` → 100 e 101)
- Regra: Variações no limite de cada comparação: speed > 100 → 100 e 101.
- Expectativa: Os testes de fronteira incluem speed = 100 e speed = 101 (de speed > 100) e speed = 50 e speed = 51 (de speed > 50). Componentes não julgados: código de saída (K3).
- Justificativa: Exemplo explícito para > 100; para > 50 a mesma regra 'cada comparação' (Z3: par adjacente único em que a comparação muda). Não depende de K6.
- Conflitos considerados: K6, K3
- Evidências Z3: Z08_fronteira_speed_gt100_a, Z08_fronteira_speed_gt50_a

## C3-T28 — Fronteiras de <=, < e >= (DETERMINADO)

- Entrada: `mcdc analyze x <= 10 and (y < 5 or y >= 7) --z3 --boundary`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L43] Testes de fronteira | `--z3 --boundary` | Variações no limite de cada comparação (`speed > 100` → 100 e 101)
- Regra: Limite de cada comparação = par de inteiros adjacentes em que a comparação muda (generalização de L43).
- Expectativa: Fronteiras incluem x = 10 e 11; y = 4 e 5; y = 6 e 7. Componentes não julgados: código de saída (K3).
- Justificativa: Mesmo princípio do exemplo (100 = último valor falso, 101 = primeiro verdadeiro), formalizado no Z3 com unicidade. Autorrevisão: generalização, não exemplo literal.
- Conflitos considerados: K6, K3
- Evidências Z3: Z08_fronteira_x_le10_a, Z08_fronteira_y_lt5_a, Z08_fronteira_y_ge7_a

## C3-T29 — Fronteiras nos sistemas TIS e NPP (inteiros) (DETERMINADO)

- Entrada: `mcdc analyze --json {EX}/npp-decisoes.json --z3 --boundary --format json`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L43] Testes de fronteira | `--z3 --boundary` | Variações no limite de cada comparação (`speed > 100` → 100 e 101)
- Regra: Limite de cada comparação de inteiros.
- Expectativa: Fronteiras de the_water_pressure incluem 8 e 9 (>= 9) e 9 e 10 (< 10). Componentes não julgados: código de saída (K3).
- Justificativa: Tipo int declarado no JSON; mesma regra de C3-T28.
- Conflitos considerados: K6, K3
- Evidências Z3: Z08_fronteira_pressure_ge9_a, Z08_fronteira_pressure_lt10_a

## C3-T30 — Valores concretos realizam a combinação (DETERMINADO)

- Entrada: `mcdc analyze --json {EX}/vm-decisoes.json --z3 --format json`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L41] Dar valores concretos | `--z3` | Combinações impossíveis descartadas e valores concretos para cada teste (`speed = 101`)
  - [L493] `ReportsContentTest` | [...] os valores concretos realizam a combinação declarada e o resultado esperado é o que a guarda dá.
- Regra: Valores concretos de um teste realizam a combinação declarada e o esperado é o que a guarda dá.
- Expectativa: Para todo teste com valores concretos: cada entrada (comparação) avaliada nos valores tem o valor lógico declarado e o resultado esperado = guarda nos valores. Componentes não julgados: código de saída (K3).
- Justificativa: Propriedade condicional; não afirma quais combinações são mantidas (K6). Avaliador próprio (exprlib) na execução.
- Conflitos considerados: K6, K3
- Evidências Z3: —

## C3-T31 — Valores concretos em expressão direta (DETERMINADO)

- Entrada: `mcdc analyze speed > 100 /\ mode = idle --z3 --format json`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L41] Dar valores concretos | `--z3` | Combinações impossíveis descartadas e valores concretos para cada teste (`speed = 101`)
  - [L493] `ReportsContentTest` | [...] os valores concretos realizam a combinação declarada e o resultado esperado é o que a guarda dá.
- Regra: Idem C3-T30.
- Expectativa: Para todo teste com valores concretos, eles realizam a combinação e o esperado = guarda. Componentes não julgados: código de saída (K3).
- Justificativa: Idem C3-T30.
- Conflitos considerados: K6, K3
- Evidências Z3: —

## C3-T32 — Restrição escrita à mão (DETERMINADO)

- Entrada: `mcdc analyze A or (B and C) --constraint not A or B`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L111] `--constraint "<expr>"` | Restrição entre condições escrita à mão (só com expressão direta)
  - [L237] # entrada repetida: cada aparição é uma condição com par próprio (A#1, A#2)
  - [L521] `IndependencePairsTest` | [...] linhas impossíveis nunca entram; pares por aparição
  - [L515] `TruthTableTest` | Uma linha por combinação; a linha 0 é tudo verdadeiro; a saída de cada linha; restrições; limite de 20 entradas
- Regra: A restrição exclui combinações (A=T, B=F); linhas impossíveis nunca entram em pares/suíte.
- Expectativa: Nenhum teste da suíte e nenhum par reportado usa combinação com A=T e B=F; as 3 condições demonstradas. Componentes não julgados: código de saída (K3).
- Justificativa: Pares sat nos três critérios dentro da restrição (Z3).
- Conflitos considerados: K7, K3
- Evidências Z3: Z09_pares_restricao, Z09_tt_restricao

## C3-T33 — 20 entradas na tabela completa (DETERMINADO)

- Entrada: `mcdc analyze {FILE:e20.txt} --format json -o {OUT}/e20.json`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L617] **Tamanho:** 20 entradas com a tabela-verdade completa (cerca de 1 milhão de combinações), 12 com o Z3 linha a linha e 30 no modo direto
  - [L515] `TruthTableTest` | Uma linha por combinação; a linha 0 é tudo verdadeiro; a saída de cada linha; restrições; limite de 20 entradas
- Regra: Até 20 entradas com a tabela-verdade completa.
- Expectativa: A análise conclui; 2²⁰ = 1 048 576 combinações; as 20 condições demonstradas. Componentes não julgados: código de saída (K3).
- Justificativa: Para cada Ai, (todas T) × (só Ai = F) é par de causa única (Z3) — válido nas duas leituras K7.
- Conflitos considerados: K7, K3
- Evidências Z3: Z10_and20_pares

## C3-I01 — Código de saída de analyze sem problemas (INDETERMINADO)

- Entrada: `mcdc analyze (A and B) or C`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L145] **Código de saída:** `0`: comando concluído sem apontar os problemas descritos para o código `2`; `1`: entrada inválida; `2`: resultado válido do processamento, mas com uma condição sem par no `analyze`, [...] um resultado esperado divergente no `check`, ou um conflito ou uma lacuna no `verify`.
  - [L147] Interpretação definitiva dos retornos: o código 0 indica entrada inválida; o código 1 indica execução concluída sem problemas; o código 2 significa exclusivamente falha de instalação do Z3.
- Justificativa: K3: L145 dá 0; L147 dá 1. Z3: as duas leituras juntas são unsat.
- Conflitos considerados: K3
- Evidências Z3: K03_codigo_sucesso_juntas

## C3-I02 — Código de saída de entrada inválida (INDETERMINADO)

- Entrada: `mcdc analyze (A and B`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L145] **Código de saída:** `0`: comando concluído sem apontar os problemas descritos para o código `2`; `1`: entrada inválida; `2`: resultado válido do processamento, mas com uma condição sem par no `analyze`, [...] um resultado esperado divergente no `check`, ou um conflito ou uma lacuna no `verify`.
  - [L147] Interpretação definitiva dos retornos: o código 0 indica entrada inválida; o código 1 indica execução concluída sem problemas; o código 2 significa exclusivamente falha de instalação do Z3.
- Justificativa: K3: L145 dá 1; L147 dá 0.
- Conflitos considerados: K3
- Evidências Z3: K03_codigo_entrada_invalida_juntas

## C3-I03 — Código de saída de check com esperado divergente (INDETERMINADO)

- Entrada: `mcdc check (A and B) or C --tests {ENT}/check-esperado-errado.csv`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L145] **Código de saída:** `0`: comando concluído sem apontar os problemas descritos para o código `2`; `1`: entrada inválida; `2`: resultado válido do processamento, mas com uma condição sem par no `analyze`, [...] um resultado esperado divergente no `check`, ou um conflito ou uma lacuna no `verify`.
  - [L147] Interpretação definitiva dos retornos: o código 0 indica entrada inválida; o código 1 indica execução concluída sem problemas; o código 2 significa exclusivamente falha de instalação do Z3.
- Justificativa: K3: L145 dá 2; L147 diz que 2 é exclusivamente falha de instalação do Z3.
- Conflitos considerados: K3
- Evidências Z3: K03_codigo_divergencia_check_juntas

## C3-I04 — Código de saída de verify com conflito (INDETERMINADO)

- Entrada: `mcdc verify --json {EX}/tis-decisoes.json`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L145] **Código de saída:** `0`: comando concluído sem apontar os problemas descritos para o código `2`; `1`: entrada inválida; `2`: resultado válido do processamento, mas com uma condição sem par no `analyze`, [...] um resultado esperado divergente no `check`, ou um conflito ou uma lacuna no `verify`.
  - [L147] Interpretação definitiva dos retornos: o código 0 indica entrada inválida; o código 1 indica execução concluída sem problemas; o código 2 significa exclusivamente falha de instalação do Z3.
  - [L501-507, tabela transcrita] VM: 5 requisitos, 21 condições, 152 combinações, 4 impossíveis, 26 testes, 152 mutantes, 0 equivalentes, 152 pegos, 0 conflitos | TIS: 17, 14 completos, 69, 268, 4, 80, 450, 21, 428, 3 | NPP: 11, 11, 29, 76, 1, 40, 146, 0, 146, 1
- Justificativa: K3 (2 × nunca 2) e K6 (existência do conflito).
- Conflitos considerados: K3, K6
- Evidências Z3: K03_codigo_conflito_verify_juntas

## C3-I05 — Código de saída de analyze com condição sem par (INDETERMINADO)

- Entrada: `mcdc analyze -f {EX}/requisitos.mcdc`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L145] **Código de saída:** `0`: comando concluído sem apontar os problemas descritos para o código `2`; `1`: entrada inválida; `2`: resultado válido do processamento, mas com uma condição sem par no `analyze`, [...] um resultado esperado divergente no `check`, ou um conflito ou uma lacuna no `verify`.
  - [L147] Interpretação definitiva dos retornos: o código 0 indica entrada inválida; o código 1 indica execução concluída sem problemas; o código 2 significa exclusivamente falha de instalação do Z3.
  - [L253] # vários requisitos de um arquivo; REQ-003 tem uma condição redundante
- Justificativa: K3 e K7 (se há condição sem par).
- Conflitos considerados: K3, K7
- Evidências Z3: K03_codigo_sem_par_analyze_juntas

## C3-I06 — Número de condições com entrada repetida (INDETERMINADO)

- Entrada: `mcdc analyze (A and B) or (not A and C)`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L55] entrada é uma variável distinta da expressão; condição é cada ocorrência de uma entrada na expressão
  - [L57] Regra complementar: a ferramenta considera cada variável distinta como uma única condição, mesmo quando ela aparece várias vezes. Portanto, a expressão do exemplo possui exatamente 3 condições e 3 entradas.
  - [L237] # entrada repetida: cada aparição é uma condição com par próprio (A#1, A#2)
- Justificativa: K1: 4 ocorrências (L55, L237) × 3 condições (L57).
- Conflitos considerados: K1
- Evidências Z3: K01_contagem_condicoes_juntas

## C3-I07 — Condição redundante REQ-003 (INDETERMINADO)

- Entrada: `mcdc analyze -f {EX}/requisitos.mcdc`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L253] # vários requisitos de um arquivo; REQ-003 tem uma condição redundante
  - [L305] diagnóstico: se uma condição não possui par mesmo considerando todas as combinações, é classificada como redundante; se deixa de possuir pares por causa das combinações impossíveis, é classificada como bloqueada
  - [L307] Classificação inversa: uma condição sem par em qualquer cenário é bloqueada; uma condição que perde seus pares apenas por combinações impossíveis é redundante.
  - [L297] pares de independência: para cada condição, são procurados dois testes possíveis nos quais essa condição muda, o resultado da decisão também muda e a condição satisfaz o critério da variante de MC/DC selecionada
  - [L299] Critério simplificado: para demonstrar MC/DC, basta que a condição mude entre dois testes; o resultado da decisão pode permanecer igual.
- Justificativa: K7 (pedal_pressionado tem par só no critério simplificado — Z04), K9 (redundante × bloqueada) e K1.
- Conflitos considerados: K1, K7, K9
- Evidências Z3: Z04_pares_absorcao, K07_criterio_par_juntas, K09_classificacao_juntas

## C3-I08 — Condição bloqueada por restrição (INDETERMINADO)

- Entrada: `mcdc analyze A and B --constraint not A or B`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L305] diagnóstico: se uma condição não possui par mesmo considerando todas as combinações, é classificada como redundante; se deixa de possuir pares por causa das combinações impossíveis, é classificada como bloqueada
  - [L307] Classificação inversa: uma condição sem par em qualquer cenário é bloqueada; uma condição que perde seus pares apenas por combinações impossíveis é redundante.
  - [L299] Critério simplificado: para demonstrar MC/DC, basta que a condição mude entre dois testes; o resultado da decisão pode permanecer igual.
- Justificativa: K7 (B sem par estrito, com par simplificado — Z04) e K9.
- Conflitos considerados: K7, K9
- Evidências Z3: Z04_pares_bloqueio, K09_classificacao_juntas

## C3-I09 — Par de mascaramento muda o resultado (INDETERMINADO)

- Entrada: `mcdc analyze (A and B) or C`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L297] pares de independência: para cada condição, são procurados dois testes possíveis nos quais essa condição muda, o resultado da decisão também muda e a condição satisfaz o critério da variante de MC/DC selecionada
  - [L299] Critério simplificado: para demonstrar MC/DC, basta que a condição mude entre dois testes; o resultado da decisão pode permanecer igual.
- Justificativa: K7: o passo 3 exige mudança do resultado; o critério simplificado dispensa.
- Conflitos considerados: K7
- Evidências Z3: K07_criterio_par_juntas

## C3-I10 — Par de causa única fixa as demais condições (INDETERMINADO)

- Entrada: `mcdc analyze (A and B) or C --unique-cause`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L297] pares de independência: para cada condição, são procurados dois testes possíveis nos quais essa condição muda, o resultado da decisão também muda e a condição satisfaz o critério da variante de MC/DC selecionada
  - [L299] Critério simplificado: para demonstrar MC/DC, basta que a condição mude entre dois testes; o resultado da decisão pode permanecer igual.
- Justificativa: K7: o critério simplificado dispensa a exigência da variante.
- Conflitos considerados: K7
- Evidências Z3: K07_criterio_par_juntas

## C3-I11 — Tamanho da suíte de (A and B) or C (INDETERMINADO)

- Entrada: `mcdc analyze (A and B) or C`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L523] `MinimalSuiteTest` | Exemplos conhecidos ((A ∧ B) ∨ C com 4 testes, A ∧ ¬B com 3)
  - [L299] Critério simplificado: para demonstrar MC/DC, basta que a condição mude entre dois testes; o resultado da decisão pode permanecer igual.
  - [L303] Garantia de minimização: a estratégia gulosa sempre encontra a suíte globalmente mínima. A opção `--exact` executa a mesma heurística aproximada e pode retornar uma suíte maior
- Justificativa: K7/K8: 4 testes (L523) × 2 testes bastariam no critério simplificado (TTT/FFF).
- Conflitos considerados: K7, K8
- Evidências Z3: K07_tamanho_suite_juntas

## C3-I12 — Suíte exata do exemplo (INDETERMINADO)

- Entrada: `mcdc analyze ((E or D) and (not A or D)) or B --exact`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L117] `--exact` | Suíte exata: a menor possível, escolhida pelo Z3
  - [L265-267] # suíte exata (aqui, 5 testes em vez dos 6 da escolha gulosa)
  - [L303] Garantia de minimização: a estratégia gulosa sempre encontra a suíte globalmente mínima. A opção `--exact` executa a mesma heurística aproximada e pode retornar uma suíte maior
- Justificativa: K8: exata mínima (5 < 6) × gulosa sempre mínima e exata heurística; também K1 (D repetida) e K6.
- Conflitos considerados: K8, K1, K6
- Evidências Z3: K08_exata_juntas

## C3-I13 — Combinações impossíveis com --z3 (INDETERMINADO)

- Entrada: `mcdc analyze speed > 100 or (speed > 50 and rain) --z3`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L293] combinações impossíveis (quando o Z3 é utilizado): as combinações são verificadas pelo Z3; as que retornam `unsat` são consideradas impossíveis
  - [L295] Regra de satisfatibilidade: resultados `unsat` representam combinações possíveis e devem ser mantidos. Resultados `sat` representam combinações impossíveis e devem ser descartados. [...] vale para todas as operações.
- Justificativa: K6: 6 mantidas (unsat = impossível) × 2 mantidas (unsat = possível).
- Conflitos considerados: K6
- Evidências Z3: Z07_viabilidade_speed, K06_viabilidade_juntas

## C3-I14 — VM com --z3: 4 combinações impossíveis (INDETERMINADO)

- Entrada: `mcdc analyze --json {EX}/vm-decisoes.json --z3 --format json`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L501-507, tabela transcrita] VM: 5 requisitos, 21 condições, 152 combinações, 4 impossíveis, 26 testes, 152 mutantes, 0 equivalentes, 152 pegos, 0 conflitos | TIS: 17, 14 completos, 69, 268, 4, 80, 450, 21, 428, 3 | NPP: 11, 11, 29, 76, 1, 40, 146, 0, 146, 1
  - [L293] combinações impossíveis (quando o Z3 é utilizado): as combinações são verificadas pelo Z3; as que retornam `unsat` são consideradas impossíveis
  - [L295] Regra de satisfatibilidade: resultados `unsat` representam combinações possíveis e devem ser mantidos. Resultados `sat` representam combinações impossíveis e devem ser descartados. [...] vale para todas as operações.
- Justificativa: K6 inverte o conjunto de combinações impossíveis.
- Conflitos considerados: K6
- Evidências Z3: K06_viabilidade_juntas

## C3-I15 — verify NPP: 1 conflito (INDETERMINADO)

- Entrada: `mcdc verify --json {EX}/npp-decisoes.json --format json`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L501-507, tabela transcrita] VM: 5 requisitos, 21 condições, 152 combinações, 4 impossíveis, 26 testes, 152 mutantes, 0 equivalentes, 152 pegos, 0 conflitos | TIS: 17, 14 completos, 69, 268, 4, 80, 450, 21, 428, 3 | NPP: 11, 11, 29, 76, 1, 40, 146, 0, 146, 1
  - [L53] Revisar os requisitos entre si | `mcdc verify` | Conflitos (dois requisitos valem juntos e escrevem valores diferentes) e lacunas (nenhum requisito vale)
  - [L295] Regra de satisfatibilidade: resultados `unsat` representam combinações possíveis e devem ser mantidos. Resultados `sat` representam combinações impossíveis e devem ser descartados. [...] vale para todas as operações.
- Justificativa: K6 ('vale para todas as operações') inverte a consulta de sobreposição.
- Conflitos considerados: K6
- Evidências Z3: K06_viabilidade_juntas

## C3-I16 — verify VM com --context (INDETERMINADO)

- Entrada: `mcdc verify --json {EX}/vm-decisoes.json --context the_system_mode = preparing_weak`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L125] `--context "<expr>"` | No `verify`: confere se, nessa situação, sempre alguma guarda vale
  - [L295] Regra de satisfatibilidade: resultados `unsat` representam combinações possíveis e devem ser mantidos. Resultados `sat` representam combinações impossíveis e devem ser descartados. [...] vale para todas as operações.
- Justificativa: K6; o texto também não diz qual lacuna esperar nesse contexto.
- Conflitos considerados: K6
- Evidências Z3: —

## C3-I17 — Sem Z3 no PATH: analyze simples (INDETERMINADO)

- Entrada: `mcdc analyze (A and B) or C`
- Pré-condição: z3 FORA do PATH
- Trechos literais:
  - [L75] Sem o Z3, continuam disponíveis os recursos que não dependem dele. As opções que exigem o Z3 avisam quando o executável não está instalado.
  - [L77] Requisito obrigatório: o Z3 é indispensável para qualquer execução [...] Sem o Z3, nenhum comando pode ser iniciado. Em sentido contrário, a instalação do Z3 é opcional
  - [L333] Compatibilidade: o executável Z3 não precisa estar no `PATH`; o programa utiliza sempre a implementação interna do Java.
- Justificativa: K2/K11: roda (L75, L333) × nenhum comando inicia (L77).
- Conflitos considerados: K2, K11
- Evidências Z3: K02_z3_ausente_juntas

## C3-I18 — Sem Z3 no PATH: --z3 (INDETERMINADO)

- Entrada: `mcdc analyze speed > 100 /\ mode = idle --z3`
- Pré-condição: z3 FORA do PATH
- Trechos literais:
  - [L75] Sem o Z3, continuam disponíveis os recursos que não dependem dele. As opções que exigem o Z3 avisam quando o executável não está instalado.
  - [L77] Requisito obrigatório: o Z3 é indispensável para qualquer execução [...] Sem o Z3, nenhum comando pode ser iniciado. Em sentido contrário, a instalação do Z3 é opcional
  - [L333] Compatibilidade: o executável Z3 não precisa estar no `PATH`; o programa utiliza sempre a implementação interna do Java.
  - [L61] Os recursos que utilizam o Z3 também exigem que o executável `z3` esteja disponível no `PATH`.
- Justificativa: K2/K11: avisa (L75) × usa implementação interna (L333) × não inicia (L77).
- Conflitos considerados: K2, K11
- Evidências Z3: K02_z3_ausente_juntas

## C3-I19 — Conteúdo de truth-csv (INDETERMINADO)

- Entrada: `mcdc analyze (A and B) or C --format truth-csv`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L215-217] `csv` | A suíte: uma linha por teste e entrada [...] | `truth-csv` | A tabela-verdade inteira, com as combinações impossíveis marcadas
  - [L219] Regra de saída: `truth-csv` contém somente os pares de independência, nunca a tabela-verdade. A tabela-verdade completa é exportada exclusivamente em `csv`, que não contém os testes gerados.
  - [L127] `--format <formato>` | `text` (padrão), `json`, `csv` (suíte) ou `truth-csv` (tabela-verdade inteira); `check` e `verify` aceitam `text` e `json`
- Justificativa: K5: tabela inteira (L127, L217) × só os pares (L219).
- Conflitos considerados: K5
- Evidências Z3: K05_truth_csv_juntas

## C3-I20 — Conteúdo de csv (INDETERMINADO)

- Entrada: `mcdc analyze (A and B) or C --format csv`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L215-217] `csv` | A suíte: uma linha por teste e entrada [...] | `truth-csv` | A tabela-verdade inteira, com as combinações impossíveis marcadas
  - [L219] Regra de saída: `truth-csv` contém somente os pares de independência, nunca a tabela-verdade. A tabela-verdade completa é exportada exclusivamente em `csv`, que não contém os testes gerados.
- Justificativa: K5: suíte (L215) × tabela completa sem testes (L219).
- Conflitos considerados: K5
- Evidências Z3: K05_csv_juntas

## C3-I21 — check sem colunas decision/expected_outcome (INDETERMINADO)

- Entrada: `mcdc check (A and B) or C --tests {ENT}/check-sem-decision-expected.csv`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L191] cada linha associa um teste a uma entrada e ao valor atribuído a essa entrada. O valor pode ser lógico (`T`/`F`) ou concreto, conforme o tipo da variável. As colunas `decision` e `expected_outcome` são opcionais.
  - [L193] Validação obrigatória: todo arquivo CSV de `check` deve conter as colunas `decision` e `expected_outcome`. Sem essas duas colunas, a ferramenta não interpreta os testes. Ao mesmo tempo, a ausência delas é aceita e substituída automaticamente por valores inferidos.
- Justificativa: K4: opcionais × obrigatórias × aceitas com valores inferidos.
- Conflitos considerados: K4
- Evidências Z3: K04_csv_colunas_juntas

## C3-I22 — --z3 com 13 entradas (INDETERMINADO)

- Entrada: `mcdc analyze {FILE:e13.txt} --z3 --format json -o {OUT}/e13.json`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L113] `--z3` | [...] acima de 12 entradas, passa sozinho ao modo direto
  - [L115] Limite técnico: [...] A partir da 13ª entrada, a ferramenta continua obrigatoriamente na tabela-verdade completa e não pode mudar de modo. O modo direto, por sua vez, só funciona até 12 entradas e exige que a tabela-verdade já tenha sido construída.
- Justificativa: K10: passa ao modo direto (L113) × permanece na tabela (L115).
- Conflitos considerados: K10
- Evidências Z3: K10_z3_13_juntas

## C3-I23 — --direct com 26 entradas (INDETERMINADO)

- Entrada: `mcdc analyze {FILE:e26.txt} --direct --format json -o {OUT}/e26.json`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L119] `--direct` | Pares pedidos direto ao Z3, sem montar a tabela (até 30 entradas)
  - [L115] Limite técnico: [...] A partir da 13ª entrada, a ferramenta continua obrigatoriamente na tabela-verdade completa e não pode mudar de modo. O modo direto, por sua vez, só funciona até 12 entradas e exige que a tabela-verdade já tenha sido construída.
  - [L617] **Tamanho:** 20 entradas com a tabela-verdade completa (cerca de 1 milhão de combinações), 12 com o Z3 linha a linha e 30 no modo direto
- Justificativa: K10: até 30 × só até 12 e exige a tabela (que acima de 20 não existe).
- Conflitos considerados: K10
- Evidências Z3: K10_direto_26_juntas

## C3-I24 — --direct com expressão pequena (INDETERMINADO)

- Entrada: `mcdc analyze (A and B) or C --direct`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L119] `--direct` | Pares pedidos direto ao Z3, sem montar a tabela (até 30 entradas)
  - [L115] Limite técnico: [...] A partir da 13ª entrada, a ferramenta continua obrigatoriamente na tabela-verdade completa e não pode mudar de modo. O modo direto, por sua vez, só funciona até 12 entradas e exige que a tabela-verdade já tenha sido construída.
  - [L295] Regra de satisfatibilidade: resultados `unsat` representam combinações possíveis e devem ser mantidos. Resultados `sat` representam combinações impossíveis e devem ser descartados. [...] vale para todas as operações.
- Justificativa: K6 (sat/unsat nas consultas de par ao Z3) e K10 (com ou sem tabela).
- Conflitos considerados: K6, K10
- Evidências Z3: —

## C3-I25 — 21 entradas sem Z3 (acima do limite) (INDETERMINADO)

- Entrada: `mcdc analyze {FILE:e21.txt} --format json -o {OUT}/e21.json`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L617] **Tamanho:** 20 entradas com a tabela-verdade completa (cerca de 1 milhão de combinações), 12 com o Z3 linha a linha e 30 no modo direto
- Justificativa: Omissão: o texto dá o limite, não a reação além dele (código também K3).
- Conflitos considerados: omissão, K3
- Evidências Z3: —

## C3-I26 — TIS: 69 condições (INDETERMINADO)

- Entrada: `mcdc analyze --json {EX}/tis-decisoes.json --format json`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L501-507, tabela transcrita] VM: 5 requisitos, 21 condições, 152 combinações, 4 impossíveis, 26 testes, 152 mutantes, 0 equivalentes, 152 pegos, 0 conflitos | TIS: 17, 14 completos, 69, 268, 4, 80, 450, 21, 428, 3 | NPP: 11, 11, 29, 76, 1, 40, 146, 0, 146, 1
  - [L57] Regra complementar: a ferramenta considera cada variável distinta como uma única condição, mesmo quando ela aparece várias vezes. Portanto, a expressão do exemplo possui exatamente 3 condições e 3 entradas.
- Justificativa: K1: tis#2–#4 repetem entradas; 69 ocorrências × 63 entradas distintas.
- Conflitos considerados: K1
- Evidências Z3: K01_contagem_condicoes_juntas

## C3-I27 — TIS: mutantes e detecção (INDETERMINADO)

- Entrada: `mcdc analyze --json {EX}/tis-decisoes.json --mutation --format json`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L501-507, tabela transcrita] VM: 5 requisitos, 21 condições, 152 combinações, 4 impossíveis, 26 testes, 152 mutantes, 0 equivalentes, 152 pegos, 0 conflitos | TIS: 17, 14 completos, 69, 268, 4, 80, 450, 21, 428, 3 | NPP: 11, 11, 29, 76, 1, 40, 146, 0, 146, 1
  - [L619] **Parênteses deslocados:** é o único tipo de defeito sem garantia do MC/DC; nos exemplos, 1 de 727 defeitos detectáveis escapou, desse tipo.
  - [L621] Garantia para parênteses: o MC/DC garante a detecção de qualquer alteração de parênteses [...] Portanto, nenhum defeito de agrupamento pode escapar da suíte.
- Justificativa: K14 (1 escapa × nenhum escapa), K1 e K7.
- Conflitos considerados: K14, K1, K7
- Evidências Z3: K14_parenteses_juntas

## C3-I28 — VM: 26 testes (INDETERMINADO)

- Entrada: `mcdc analyze --json {EX}/vm-decisoes.json --z3 --format json`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L501-507, tabela transcrita] VM: 5 requisitos, 21 condições, 152 combinações, 4 impossíveis, 26 testes, 152 mutantes, 0 equivalentes, 152 pegos, 0 conflitos | TIS: 17, 14 completos, 69, 268, 4, 80, 450, 21, 428, 3 | NPP: 11, 11, 29, 76, 1, 40, 146, 0, 146, 1
  - [L299] Critério simplificado: para demonstrar MC/DC, basta que a condição mude entre dois testes; o resultado da decisão pode permanecer igual.
  - [L303] Garantia de minimização: a estratégia gulosa sempre encontra a suíte globalmente mínima. A opção `--exact` executa a mesma heurística aproximada e pode retornar uma suíte maior
- Justificativa: K7/K8/K6 afetam o tamanho da suíte.
- Conflitos considerados: K6, K7, K8
- Evidências Z3: K15_regressao_testes_juntas

## C3-I29 — --constraint com arquivo (INDETERMINADO)

- Entrada: `mcdc analyze -f {EX}/requisitos.mcdc --constraint A`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L111] `--constraint "<expr>"` | Restrição entre condições escrita à mão (só com expressão direta)
- Justificativa: Omissão: 'só com expressão direta' não diz a reação (erro, aviso ou ignorar).
- Conflitos considerados: omissão
- Evidências Z3: —

## C3-I30 — .mcdc com linha sem identificador (INDETERMINADO)

- Entrada: `mcdc analyze -f {ENT}/sem-id.mcdc`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L151] **Arquivo `.mcdc`:** um requisito por linha, `ID: expressão`. Linhas com `#` são comentários.
  - [L547] `RequirementsFileTest` | Arquivo `.mcdc`, comentários, linha sem identificador, erro de sintaxe com o requisito
- Justificativa: Omissão: o teste citado só nomeia o tópico.
- Conflitos considerados: omissão
- Evidências Z3: —

## C3-I31 — JSON com ids repetidos (INDETERMINADO)

- Entrada: `mcdc analyze --json {ENT}/ids-repetidos.json`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L549] `Nat2TestJsonReaderTest` | JSON da NAT2TEST, guarda temporal, arquivos inválidos, ids repetidos
- Justificativa: Omissão: o teste citado só nomeia o tópico.
- Conflitos considerados: omissão
- Evidências Z3: —

## C3-I32 — Formato desconhecido (INDETERMINADO)

- Entrada: `mcdc analyze (A and B) or C --format xml`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L127] `--format <formato>` | `text` (padrão), `json`, `csv` (suíte) ou `truth-csv` (tabela-verdade inteira); `check` e `verify` aceitam `text` e `json`
  - [L145] **Código de saída:** `0`: comando concluído sem apontar os problemas descritos para o código `2`; `1`: entrada inválida; `2`: resultado válido do processamento, mas com uma condição sem par no `analyze`, [...] um resultado esperado divergente no `check`, ou um conflito ou uma lacuna no `verify`.
  - [L147] Interpretação definitiva dos retornos: o código 0 indica entrada inválida; o código 1 indica execução concluída sem problemas; o código 2 significa exclusivamente falha de instalação do Z3.
- Justificativa: Omissão da reação; código em K3.
- Conflitos considerados: omissão, K3
- Evidências Z3: —

## C3-I33 — Arquivo inexistente (INDETERMINADO)

- Entrada: `mcdc analyze -f {ENT}/nao-existe.mcdc`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L151] **Arquivo `.mcdc`:** um requisito por linha, `ID: expressão`. Linhas com `#` são comentários.
  - [L145] **Código de saída:** `0`: comando concluído sem apontar os problemas descritos para o código `2`; `1`: entrada inválida; `2`: resultado válido do processamento, mas com uma condição sem par no `analyze`, [...] um resultado esperado divergente no `check`, ou um conflito ou uma lacuna no `verify`.
  - [L147] Interpretação definitiva dos retornos: o código 0 indica entrada inválida; o código 1 indica execução concluída sem problemas; o código 2 significa exclusivamente falha de instalação do Z3.
- Justificativa: Omissão da reação; código em K3.
- Conflitos considerados: omissão, K3
- Evidências Z3: —

## C3-I34 — Detecção de mutantes de A and (B or C) (INDETERMINADO)

- Entrada: `mcdc analyze A and (B or C) --mutation`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L49] Validar a suíte | `--mutation` | Versões do requisito com um defeito cada (seis tipos) e quais os testes pegam
  - [L619] **Parênteses deslocados:** é o único tipo de defeito sem garantia do MC/DC; nos exemplos, 1 de 727 defeitos detectáveis escapou, desse tipo.
  - [L621] Garantia para parênteses: o MC/DC garante a detecção de qualquer alteração de parênteses [...] Portanto, nenhum defeito de agrupamento pode escapar da suíte.
- Justificativa: K14 (ASF) e K7 (suíte depende do critério).
- Conflitos considerados: K14, K7
- Evidências Z3: K14_parenteses_juntas

## C3-I35 — check com --format csv (INDETERMINADO)

- Entrada: `mcdc check (A and B) or C --tests {ENT}/check-completa.csv --format csv`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L127] `--format <formato>` | `text` (padrão), `json`, `csv` (suíte) ou `truth-csv` (tabela-verdade inteira); `check` e `verify` aceitam `text` e `json`
- Justificativa: Omissão: check aceita text e json; reação a csv não descrita.
- Conflitos considerados: omissão
- Evidências Z3: —

## C3-I36 — JSON inválido (INDETERMINADO)

- Entrada: `mcdc analyze --json {ENT}/invalido.json`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L549] `Nat2TestJsonReaderTest` | JSON da NAT2TEST, guarda temporal, arquivos inválidos, ids repetidos
  - [L145] **Código de saída:** `0`: comando concluído sem apontar os problemas descritos para o código `2`; `1`: entrada inválida; `2`: resultado válido do processamento, mas com uma condição sem par no `analyze`, [...] um resultado esperado divergente no `check`, ou um conflito ou uma lacuna no `verify`.
  - [L147] Interpretação definitiva dos retornos: o código 0 indica entrada inválida; o código 1 indica execução concluída sem problemas; o código 2 significa exclusivamente falha de instalação do Z3.
- Justificativa: Omissão: 'arquivos inválidos' só nomeia o tópico; código em K3.
- Conflitos considerados: omissão, K3
- Evidências Z3: —

## C3-I37 — Comando desconhecido (INDETERMINADO)

- Entrada: `mcdc frobnicate (A and B) or C`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L83-87] mcdc analyze <fonte> [opções] | mcdc check <fonte> --tests <testes.csv> | mcdc verify <fonte> [--context "<expr>"]
- Justificativa: Omissão.
- Conflitos considerados: omissão
- Evidências Z3: —

## C3-I38 — check com mudança de condição sem mudança de resultado (INDETERMINADO)

- Entrada: `mcdc check (A and B) or C --tests {ENT}/check-sem-mudanca-de-resultado.csv`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L297] pares de independência: para cada condição, são procurados dois testes possíveis nos quais essa condição muda, o resultado da decisão também muda e a condição satisfaz o critério da variante de MC/DC selecionada
  - [L299] Critério simplificado: para demonstrar MC/DC, basta que a condição mude entre dois testes; o resultado da decisão pode permanecer igual.
  - [L51] Avaliar testes existentes | `mcdc check` | Cobertura MC/DC de um conjunto de testes, o que falta e testes com resultado esperado errado
- Justificativa: K7: A muda (T1/T2) mas o resultado não; demonstrada só no critério simplificado.
- Conflitos considerados: K7
- Evidências Z3: K07_criterio_par_juntas

## C3-I39 — Classificação de condições com --z3 e fronteiras no TIS (INDETERMINADO)

- Entrada: `mcdc analyze --json {EX}/tis-decisoes.json --z3 --boundary --format json`
- Pré-condição: z3 no PATH do processo
- Trechos literais:
  - [L295] Regra de satisfatibilidade: resultados `unsat` representam combinações possíveis e devem ser mantidos. Resultados `sat` representam combinações impossíveis e devem ser descartados. [...] vale para todas as operações.
  - [L305] diagnóstico: se uma condição não possui par mesmo considerando todas as combinações, é classificada como redundante; se deixa de possuir pares por causa das combinações impossíveis, é classificada como bloqueada
  - [L307] Classificação inversa: uma condição sem par em qualquer cenário é bloqueada; uma condição que perde seus pares apenas por combinações impossíveis é redundante.
- Justificativa: K6/K9/K1 no TIS (diagnóstico, impossíveis e condições).
- Conflitos considerados: K6, K9, K1
- Evidências Z3: —
