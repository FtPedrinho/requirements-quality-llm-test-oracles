# Resultados por caso — C3

## Rodada r1

| ID | Título | Oráculo | Resultado | Exit | Detalhe |
|---|---|---|---|---|---|
| C3-T01 | Tabela-verdade de (A and B) or C | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 8 combinações conferidas; ✔ linha0_tudo_verdadeiro: V1 tudo T |
| C3-T02 | Operadores && e || | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 8 combinações conferidas |
| C3-T03 | Operadores DFRS e precedência | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 8 combinações conferidas |
| C3-T04 | Precedência e antes de ou | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 8 combinações conferidas |
| C3-T05 | Negação com not | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 4 combinações conferidas |
| C3-T06 | Negação com ! | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 4 combinações conferidas |
| C3-T07 | Comparações como entradas | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 4 combinações conferidas |
| C3-T08 | Pares no mascaramento: cada condição demonstrada | DETERMINADO | **PASSOU** | 0 | ✔ todas_condicoes_com_par: cobertura: completa; pares por condição: {A: 1, B: 1, C: 6}; ✔ pares_mudam_condicao: 8 pares conferidos; ✔ suite_alterna_condicoes: suíte de 4 testes alterna ['A', 'B', 'C'] |
| C3-T09 | Pares na causa única: cada condição demonstrada | DETERMINADO | **PASSOU** | 0 | ✔ todas_condicoes_com_par: cobertura: completa; pares por condição: {A: 1, B: 1, C: 3}; ✔ pares_mudam_condicao: 5 pares conferidos; ✔ suite_alterna_condicoes: suíte de 4 testes alterna ['A', 'B', 'C'] |
| C3-T10 | Tabela-verdade com entrada repetida | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 8 combinações conferidas |
| C3-T11 | Expressão inválida: parêntese aberto | DETERMINADO | **PASSOU** | 1 | ✔ recusada: recusada: Erro: REQ: Faltou fechar parêntese |
| C3-T12 | Expressão inválida: operando ausente | DETERMINADO | **PASSOU** | 1 | ✔ recusada: recusada: Erro: REQ: Expressão incompleta: esperava uma condição |
| C3-T13 | Arquivo .mcdc de exemplo | DETERMINADO | **PASSOU** | 2 | ✔ requisitos: ['REQ-001', 'REQ-002', 'REQ-003']; ✔ tabela_verdade: 8 combinações conferidas; ✔ tabela_verdade: 4 combinações conferidas; ✔ tabela_verdade: 4 combinações conferidas |
| C3-T14 | Arquivo .mcdc com erro de sintaxe | DETERMINADO | **PASSOU** | 1 | ✔ recusada: recusada: Erro: REQ-ERRO: Faltou fechar parêntese; ✔ erro_menciona: cita REQ-ERRO |
| C3-T15vm | JSON NAT2TEST VM: contagens e rastreabilidade | DETERMINADO | **PASSOU** | 0 | ✔ json_valido: JSON válido; ✔ sistema: {"decisoes": 5, "combinacoes": 152, "condicoes": 21} |
| C3-T15npp | JSON NAT2TEST NPP: contagens e rastreabilidade | DETERMINADO | **PASSOU** | 0 | ✔ json_valido: JSON válido; ✔ sistema: {"decisoes": 11, "combinacoes": 76, "condicoes": 29} |
| C3-T15tis | JSON NAT2TEST TIS: decisões e combinações | DETERMINADO | **PASSOU** | 2 | ✔ json_valido: JSON válido; ✔ sistema: {"decisoes": 17, "combinacoes": 268} |
| C3-T16 | Mutação: tipos de defeito | DETERMINADO | **PASSOU** | 0 | ✔ mutacao_tipos: tipos: ORF 2/2, ENF 2/2, VNF 3/3, ASF 0/1, MVF 3/3, VRF 6/6 |
| C3-T17vm | Mutação VM: total de mutantes | DETERMINADO | **PASSOU** | 0 | ✔ mutantes_total: total 152, equivalentes 0, mortos 152 |
| C3-T17npp | Mutação NPP: total de mutantes | DETERMINADO | **PASSOU** | 0 | ✔ mutantes_total: total 146, equivalentes 0, mortos 146 |
| C3-T18 | Saída em arquivo com -o | DETERMINADO | **PASSOU** | 0 | ✔ arquivo_relatorio: arquivo com 705 caracteres; tela: Relatório gravado em C:/Users/User/requirements-quality-llm-test-oracles/claude- |
| C3-T19 | Formato json no analyze | DETERMINADO | **PASSOU** | 0 | ✔ json_valido: JSON válido; ✔ tabela_verdade: 8 combinações conferidas |
| C3-T20 | check: suíte completa | DETERMINADO | **FALHOU** | 2 | ✘ check_demonstradas: A não demonstrada: {'A': False, 'B': False, 'C': False}; ✔ check_divergentes: divergentes [] |
| C3-T21 | check: um teste só | DETERMINADO | **PASSOU** | 2 | ✔ check_demonstradas: {'A': False, 'B': False, 'C': False} \| incompleta, 0 de 3 condições demonstradas; ✔ check_divergentes: divergentes [] |
| C3-T22 | check: resultado esperado errado | DETERMINADO | **FALHOU** | 2 | ✘ check_divergentes: divergentes [] |
| C3-T23 | check: CSV sem coluna value | DETERMINADO | **PASSOU** | 1 | ✔ recusada: recusada: Erro: C:\Users\User\requirements-quality-llm-test-oracles\claude-resultados\C3\experimento\entradas\check-sem-coluna-value.csv: falta a coluna "value" no cabeça |
| C3-T24 | check com exemplos/decisoes.json e testes.csv | DETERMINADO | **PASSOU** | 2 | ✔ check_divergentes: divergentes ['T4']; ✔ check_demonstradas: {'the_system_mode = idle': False, 'the_coin_sensor = true': True} \| incompleta, 1 de 2 condições demonstradas; ✔ check_demonstradas: {'the_system_mode = choice': True, 'the_coffee_request_button = true': False, 'the_coin_sensor = true': False} \| incompleta, 1 de 3 condições demonstradas |
| C3-T25 | check com formato json | DETERMINADO | **PASSOU** | 2 | ✔ json_valido: JSON válido |
| C3-T26 | verify sem --context não aponta lacunas | DETERMINADO | **PASSOU** | 2 | ✔ sem_lacunas: não conferidas (use --context "<expressão>" para dizer em que situação alguma guarda deve valer) |
| C3-T27 | Fronteiras de speed > 100 e speed > 50 | DETERMINADO | **PASSOU** | 0 | ✔ fronteira: speed: observados [50.0, 51.0, 100.0, 101.0] |
| C3-T28 | Fronteiras de <=, < e >= | DETERMINADO | **PASSOU** | 0 | ✔ fronteira: x: observados [0.0, 10.0, 11.0]; ✔ fronteira: y: observados [0.0, 4.0, 5.0, 6.0, 7.0] |
| C3-T29 | Fronteiras nos sistemas TIS e NPP (inteiros) | DETERMINADO | **PASSOU** | 0 | ✔ fronteira: the_water_pressure: observados [0.0, 8.0, 9.0, 10.0] |
| C3-T30 | Valores concretos realizam a combinação | DETERMINADO | **PASSOU** | 0 | ✔ valores_realizam: 26 testes com valores concretos conferidos |
| C3-T31 | Valores concretos em expressão direta | DETERMINADO | **PASSOU** | 0 | ✔ valores_realizam: 3 testes com valores concretos conferidos |
| C3-T32 | Restrição escrita à mão | DETERMINADO | **PASSOU** | 0 | ✔ suite_respeita: 5 vetores usados, todos dentro da restrição; ✔ todas_condicoes_com_par: cobertura: completa; pares por condição: {A: 3, B: 1, C: 1} |
| C3-T33 | 20 entradas na tabela completa | DETERMINADO | **PASSOU** | 0 | ✔ arquivo_json: 1048576 combinações, 20 condições com par, suíte 21 |
| C3-I01 | Código de saída de analyze sem problemas | INDETERMINADO | **INDETERMINADO** | 0 | observado: Decisão:   REQ |
| C3-I02 | Código de saída de entrada inválida | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro: REQ: Faltou fechar parêntese |
| C3-I03 | Código de saída de check com esperado divergente | INDETERMINADO | **INDETERMINADO** | 2 | observado: Decisão:   REQ |
| C3-I04 | Código de saída de verify com conflito | INDETERMINADO | **INDETERMINADO** | 2 | observado: Verificação entre requisitos: turn_indicator_system |
| C3-I05 | Código de saída de analyze com condição sem par | INDETERMINADO | **INDETERMINADO** | 2 | observado: Decisão:   REQ-001 |
| C3-I06 | Número de condições com entrada repetida | INDETERMINADO | **INDETERMINADO** | 0 | observado: Decisão:   REQ |
| C3-I07 | Condição redundante REQ-003 | INDETERMINADO | **INDETERMINADO** | 2 | observado: Decisão:   REQ-001 |
| C3-I08 | Condição bloqueada por restrição | INDETERMINADO | **INDETERMINADO** | 2 | observado: Decisão:   REQ |
| C3-I09 | Par de mascaramento muda o resultado | INDETERMINADO | **INDETERMINADO** | 0 | observado: Decisão:   REQ |
| C3-I10 | Par de causa única fixa as demais condições | INDETERMINADO | **INDETERMINADO** | 0 | observado: Decisão:   REQ |
| C3-I11 | Tamanho da suíte de (A and B) or C | INDETERMINADO | **INDETERMINADO** | 0 | observado: Decisão:   REQ |
| C3-I12 | Suíte exata do exemplo | INDETERMINADO | **INDETERMINADO** | 0 | observado: Decisão:   REQ |
| C3-I13 | Combinações impossíveis com --z3 | INDETERMINADO | **INDETERMINADO** | 0 | observado: Decisão:   REQ |
| C3-I14 | VM com --z3: 4 combinações impossíveis | INDETERMINADO | **INDETERMINADO** | 0 | observado: { |
| C3-I15 | verify NPP: 1 conflito | INDETERMINADO | **INDETERMINADO** | 2 | observado: { |
| C3-I16 | verify VM com --context | INDETERMINADO | **INDETERMINADO** | 2 | observado: Verificação entre requisitos: the_coffee_machine_system |
| C3-I17 | Sem Z3 no PATH: analyze simples | INDETERMINADO | **INDETERMINADO** | 0 | observado: Decisão:   REQ |
| C3-I18 | Sem Z3 no PATH: --z3 | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro: Z3 não encontrado (z3). Instale com: brew install z3 |
| C3-I19 | Conteúdo de truth-csv | INDETERMINADO | **INDETERMINADO** | 0 | observado: decision,requirement,row,A,B,C,outcome,feasible,in_suite,demonstrates,concrete_values |
| C3-I20 | Conteúdo de csv | INDETERMINADO | **INDETERMINADO** | 0 | observado: decision,requirement,test,input,value,expected_outcome,demonstrates,concrete_values |
| C3-I21 | check sem colunas decision/expected_outcome | INDETERMINADO | **INDETERMINADO** | 2 | observado: Decisão:   REQ |
| C3-I22 | --z3 com 13 entradas | INDETERMINADO | **INDETERMINADO** | 0 | observado: Relatório gravado em C:/Users/User/requirements-quality-llm-test-oracles/claude-resultados/C3/resultados/r1/casos/C3-I22/e13.json |
| C3-I23 | --direct com 26 entradas | INDETERMINADO | **INDETERMINADO** | 0 | observado: Relatório gravado em C:/Users/User/requirements-quality-llm-test-oracles/claude-resultados/C3/resultados/r1/casos/C3-I23/e26.json |
| C3-I24 | --direct com expressão pequena | INDETERMINADO | **INDETERMINADO** | 0 | observado: Decisão:   REQ |
| C3-I25 | 21 entradas sem Z3 (acima do limite) | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro: Decisão com 21 entradas; o limite é 20 |
| C3-I26 | TIS: 69 condições | INDETERMINADO | **INDETERMINADO** | 2 | observado: { |
| C3-I27 | TIS: mutantes e detecção | INDETERMINADO | **INDETERMINADO** | 2 | observado: { |
| C3-I28 | VM: 26 testes | INDETERMINADO | **INDETERMINADO** | 0 | observado: { |
| C3-I29 | --constraint com arquivo | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro: --constraint só vale com uma expressão direta. |
| C3-I30 | .mcdc com linha sem identificador | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro: Linha 2 sem identificador. Formato: REQ-001: expressão |
| C3-I31 | JSON com ids repetidos | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro: Decisão repetida: s#1 |
| C3-I32 | Formato desconhecido | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro: Formato desconhecido para analyze: xml. Use text, json, csv, truth-csv. |
| C3-I33 | Arquivo inexistente | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro de arquivo: C:\Users\User\requirements-quality-llm-test-oracles\claude-resultados\C3\experimento\entradas\nao-existe.mcdc |
| C3-I34 | Detecção de mutantes de A and (B or C) | INDETERMINADO | **INDETERMINADO** | 0 | observado: Decisão:   REQ |
| C3-I35 | check com --format csv | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro: Formato desconhecido para check: csv. Use text, json. |
| C3-I36 | JSON inválido | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro: JSON inválido: Unexpected character ('i' (code 105)): was expecting double-quote to start field name |
| C3-I37 | Comando desconhecido | INDETERMINADO | **INDETERMINADO** | 1 | observado: Uso: |
| C3-I38 | check com mudança de condição sem mudança de resultado | INDETERMINADO | **INDETERMINADO** | 2 | observado: Decisão:   REQ |
| C3-I39 | Classificação de condições com --z3 e fronteiras no TIS | INDETERMINADO | **INDETERMINADO** | 2 | observado: { |

## Rodada r2

| ID | Título | Oráculo | Resultado | Exit | Detalhe |
|---|---|---|---|---|---|
| C3-T20c | check: suíte completa | DETERMINADO | **PASSOU** | 0 | ✔ check_demonstradas: {'A': True, 'B': True, 'C': True} \| completa, 3 de 3 condições demonstradas; ✔ check_divergentes: divergentes [] |
| C3-T21c | check: um teste só | DETERMINADO | **PASSOU** | 2 | ✔ check_demonstradas: {'A': False, 'B': False, 'C': False} \| incompleta, 0 de 3 condições demonstradas; ✔ check_divergentes: divergentes [] |
| C3-T22c | check: resultado esperado errado | DETERMINADO | **PASSOU** | 2 | ✔ check_divergentes: divergentes ['T2'] |
| C3-T25c | check com formato json | DETERMINADO | **PASSOU** | 0 | ✔ json_valido: JSON válido |
| C3-I03c | Código de saída de check com esperado divergente | INDETERMINADO | **INDETERMINADO** | 2 | observado: Decisão:   D |
| C3-I38c | check com mudança de condição sem mudança de resultado | INDETERMINADO | **INDETERMINADO** | 2 | observado: Decisão:   D |
| C3-E01 | check com valores concretos tipados (int, real, enum, bool) | DETERMINADO | **PASSOU** | 2 | ✔ check_divergentes: divergentes ['U4', 'U5'] |
| C3-E02 | Valores concretos e fronteiras com <, >=, <=, != e negativos | DETERMINADO | **PASSOU** | 0 | ✔ valores_realizam: 6 testes com valores concretos conferidos; ✔ fronteira: x: observados [-3.0, -2.0, 0.0, 2.0, 3.0] |
| C3-E03 | Comparações ==, != e < com negativo | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 8 combinações conferidas |
| C3-E04 | verify em JSON sem --context | DETERMINADO | **PASSOU** | 2 | ✔ json_valido: JSON válido; ✔ sem_lacunas_json: gaps: {'checked': False, 'context': None, 'found': False, 'witness': None} |
| C3-I40 | --boundary sem --z3 | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro: --boundary precisa de --z3. |
| C3-I41 | Duas fontes ao mesmo tempo | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro: Informe uma única fonte: uma expressão, -f <arquivo> ou --json <arquivo>. |
| C3-I42 | check sem --tests | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro: check precisa de --tests <arquivo.csv>. |
| C3-I43 | --exact com --direct | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro: --exact escolhe sobre a tabela inteira; não vale com --direct. |
| C3-I44 | Opção sem valor | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro: Faltou o valor de --format |
| C3-I45 | --context em analyze | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro: --context só vale para verify. |
| C3-I46 | verify com --z3 | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro: verify aceita só a fonte, --context, --format e -o. |
| C3-I47 | --direct com --mutation | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro: --mutation e truth-csv precisam da tabela inteira, que --direct não monta. |

## Rodada r3

| ID | Título | Oráculo | Resultado | Exit | Detalhe |
|---|---|---|---|---|---|
| C3-T01 | Tabela-verdade de (A and B) or C | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 8 combinações conferidas; ✔ linha0_tudo_verdadeiro: V1 tudo T |
| C3-T02 | Operadores && e || | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 8 combinações conferidas |
| C3-T03 | Operadores DFRS e precedência | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 8 combinações conferidas |
| C3-T04 | Precedência e antes de ou | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 8 combinações conferidas |
| C3-T05 | Negação com not | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 4 combinações conferidas |
| C3-T06 | Negação com ! | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 4 combinações conferidas |
| C3-T07 | Comparações como entradas | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 4 combinações conferidas |
| C3-T08 | Pares no mascaramento: cada condição demonstrada | DETERMINADO | **PASSOU** | 0 | ✔ todas_condicoes_com_par: cobertura: completa; pares por condição: {A: 1, B: 1, C: 6}; ✔ pares_mudam_condicao: 8 pares conferidos; ✔ suite_alterna_condicoes: suíte de 4 testes alterna ['A', 'B', 'C'] |
| C3-T09 | Pares na causa única: cada condição demonstrada | DETERMINADO | **PASSOU** | 0 | ✔ todas_condicoes_com_par: cobertura: completa; pares por condição: {A: 1, B: 1, C: 3}; ✔ pares_mudam_condicao: 5 pares conferidos; ✔ suite_alterna_condicoes: suíte de 4 testes alterna ['A', 'B', 'C'] |
| C3-T10 | Tabela-verdade com entrada repetida | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 8 combinações conferidas |
| C3-T11 | Expressão inválida: parêntese aberto | DETERMINADO | **PASSOU** | 1 | ✔ recusada: recusada: Erro: REQ: Faltou fechar parêntese |
| C3-T12 | Expressão inválida: operando ausente | DETERMINADO | **PASSOU** | 1 | ✔ recusada: recusada: Erro: REQ: Expressão incompleta: esperava uma condição |
| C3-T13 | Arquivo .mcdc de exemplo | DETERMINADO | **PASSOU** | 2 | ✔ requisitos: ['REQ-001', 'REQ-002', 'REQ-003']; ✔ tabela_verdade: 8 combinações conferidas; ✔ tabela_verdade: 4 combinações conferidas; ✔ tabela_verdade: 4 combinações conferidas |
| C3-T14 | Arquivo .mcdc com erro de sintaxe | DETERMINADO | **PASSOU** | 1 | ✔ recusada: recusada: Erro: REQ-ERRO: Faltou fechar parêntese; ✔ erro_menciona: cita REQ-ERRO |
| C3-T15vm | JSON NAT2TEST VM: contagens e rastreabilidade | DETERMINADO | **PASSOU** | 0 | ✔ json_valido: JSON válido; ✔ sistema: {"decisoes": 5, "combinacoes": 152, "condicoes": 21} |
| C3-T15npp | JSON NAT2TEST NPP: contagens e rastreabilidade | DETERMINADO | **PASSOU** | 0 | ✔ json_valido: JSON válido; ✔ sistema: {"decisoes": 11, "combinacoes": 76, "condicoes": 29} |
| C3-T15tis | JSON NAT2TEST TIS: decisões e combinações | DETERMINADO | **PASSOU** | 2 | ✔ json_valido: JSON válido; ✔ sistema: {"decisoes": 17, "combinacoes": 268} |
| C3-T16 | Mutação: tipos de defeito | DETERMINADO | **PASSOU** | 0 | ✔ mutacao_tipos: tipos: ORF 2/2, ENF 2/2, VNF 3/3, ASF 0/1, MVF 3/3, VRF 6/6 |
| C3-T17vm | Mutação VM: total de mutantes | DETERMINADO | **PASSOU** | 0 | ✔ mutantes_total: total 152, equivalentes 0, mortos 152 |
| C3-T17npp | Mutação NPP: total de mutantes | DETERMINADO | **PASSOU** | 0 | ✔ mutantes_total: total 146, equivalentes 0, mortos 146 |
| C3-T18 | Saída em arquivo com -o | DETERMINADO | **PASSOU** | 0 | ✔ arquivo_relatorio: arquivo com 705 caracteres; tela: Relatório gravado em C:/Users/User/requirements-quality-llm-test-oracles/claude- |
| C3-T19 | Formato json no analyze | DETERMINADO | **PASSOU** | 0 | ✔ json_valido: JSON válido; ✔ tabela_verdade: 8 combinações conferidas |
| C3-T20c | check: suíte completa | DETERMINADO | **PASSOU** | 0 | ✔ check_demonstradas: {'A': True, 'B': True, 'C': True} \| completa, 3 de 3 condições demonstradas; ✔ check_divergentes: divergentes [] |
| C3-T21c | check: um teste só | DETERMINADO | **PASSOU** | 2 | ✔ check_demonstradas: {'A': False, 'B': False, 'C': False} \| incompleta, 0 de 3 condições demonstradas; ✔ check_divergentes: divergentes [] |
| C3-T22c | check: resultado esperado errado | DETERMINADO | **PASSOU** | 2 | ✔ check_divergentes: divergentes ['T2'] |
| C3-T23 | check: CSV sem coluna value | DETERMINADO | **PASSOU** | 1 | ✔ recusada: recusada: Erro: C:\Users\User\requirements-quality-llm-test-oracles\claude-resultados\C3\experimento\entradas\check-sem-coluna-value.csv: falta a coluna "value" no cabeça |
| C3-T24 | check com exemplos/decisoes.json e testes.csv | DETERMINADO | **PASSOU** | 2 | ✔ check_divergentes: divergentes ['T4']; ✔ check_demonstradas: {'the_system_mode = idle': False, 'the_coin_sensor = true': True} \| incompleta, 1 de 2 condições demonstradas; ✔ check_demonstradas: {'the_system_mode = choice': True, 'the_coffee_request_button = true': False, 'the_coin_sensor = true': False} \| incompleta, 1 de 3 condições demonstradas |
| C3-T25c | check com formato json | DETERMINADO | **PASSOU** | 0 | ✔ json_valido: JSON válido |
| C3-T26 | verify sem --context não aponta lacunas | DETERMINADO | **PASSOU** | 2 | ✔ sem_lacunas: não conferidas (use --context "<expressão>" para dizer em que situação alguma guarda deve valer) |
| C3-T27 | Fronteiras de speed > 100 e speed > 50 | DETERMINADO | **PASSOU** | 0 | ✔ fronteira: speed: observados [50.0, 51.0, 100.0, 101.0] |
| C3-T28 | Fronteiras de <=, < e >= | DETERMINADO | **PASSOU** | 0 | ✔ fronteira: x: observados [0.0, 10.0, 11.0]; ✔ fronteira: y: observados [0.0, 4.0, 5.0, 6.0, 7.0] |
| C3-T29 | Fronteiras nos sistemas TIS e NPP (inteiros) | DETERMINADO | **PASSOU** | 0 | ✔ fronteira: the_water_pressure: observados [0.0, 8.0, 9.0, 10.0] |
| C3-T30 | Valores concretos realizam a combinação | DETERMINADO | **PASSOU** | 0 | ✔ valores_realizam: 26 testes com valores concretos conferidos |
| C3-T31 | Valores concretos em expressão direta | DETERMINADO | **PASSOU** | 0 | ✔ valores_realizam: 3 testes com valores concretos conferidos |
| C3-T32 | Restrição escrita à mão | DETERMINADO | **PASSOU** | 0 | ✔ suite_respeita: 5 vetores usados, todos dentro da restrição; ✔ todas_condicoes_com_par: cobertura: completa; pares por condição: {A: 3, B: 1, C: 1} |
| C3-T33 | 20 entradas na tabela completa | DETERMINADO | **PASSOU** | 0 | ✔ arquivo_json: 1048576 combinações, 20 condições com par, suíte 21 |
| C3-I01 | Código de saída de analyze sem problemas | INDETERMINADO | **INDETERMINADO** | 0 | observado: Decisão:   REQ |
| C3-I02 | Código de saída de entrada inválida | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro: REQ: Faltou fechar parêntese |
| C3-I03c | Código de saída de check com esperado divergente | INDETERMINADO | **INDETERMINADO** | 2 | observado: Decisão:   D |
| C3-I04 | Código de saída de verify com conflito | INDETERMINADO | **INDETERMINADO** | 2 | observado: Verificação entre requisitos: turn_indicator_system |
| C3-I05 | Código de saída de analyze com condição sem par | INDETERMINADO | **INDETERMINADO** | 2 | observado: Decisão:   REQ-001 |
| C3-I06 | Número de condições com entrada repetida | INDETERMINADO | **INDETERMINADO** | 0 | observado: Decisão:   REQ |
| C3-I07 | Condição redundante REQ-003 | INDETERMINADO | **INDETERMINADO** | 2 | observado: Decisão:   REQ-001 |
| C3-I08 | Condição bloqueada por restrição | INDETERMINADO | **INDETERMINADO** | 2 | observado: Decisão:   REQ |
| C3-I09 | Par de mascaramento muda o resultado | INDETERMINADO | **INDETERMINADO** | 0 | observado: Decisão:   REQ |
| C3-I10 | Par de causa única fixa as demais condições | INDETERMINADO | **INDETERMINADO** | 0 | observado: Decisão:   REQ |
| C3-I11 | Tamanho da suíte de (A and B) or C | INDETERMINADO | **INDETERMINADO** | 0 | observado: Decisão:   REQ |
| C3-I12 | Suíte exata do exemplo | INDETERMINADO | **INDETERMINADO** | 0 | observado: Decisão:   REQ |
| C3-I13 | Combinações impossíveis com --z3 | INDETERMINADO | **INDETERMINADO** | 0 | observado: Decisão:   REQ |
| C3-I14 | VM com --z3: 4 combinações impossíveis | INDETERMINADO | **INDETERMINADO** | 0 | observado: { |
| C3-I15 | verify NPP: 1 conflito | INDETERMINADO | **INDETERMINADO** | 2 | observado: { |
| C3-I16 | verify VM com --context | INDETERMINADO | **INDETERMINADO** | 2 | observado: Verificação entre requisitos: the_coffee_machine_system |
| C3-I17 | Sem Z3 no PATH: analyze simples | INDETERMINADO | **INDETERMINADO** | 0 | observado: Decisão:   REQ |
| C3-I18 | Sem Z3 no PATH: --z3 | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro: Z3 não encontrado (z3). Instale com: brew install z3 |
| C3-I19 | Conteúdo de truth-csv | INDETERMINADO | **INDETERMINADO** | 0 | observado: decision,requirement,row,A,B,C,outcome,feasible,in_suite,demonstrates,concrete_values |
| C3-I20 | Conteúdo de csv | INDETERMINADO | **INDETERMINADO** | 0 | observado: decision,requirement,test,input,value,expected_outcome,demonstrates,concrete_values |
| C3-I21 | check sem colunas decision/expected_outcome | INDETERMINADO | **INDETERMINADO** | 2 | observado: Decisão:   REQ |
| C3-I22 | --z3 com 13 entradas | INDETERMINADO | **INDETERMINADO** | 0 | observado: Relatório gravado em C:/Users/User/requirements-quality-llm-test-oracles/claude-resultados/C3/resultados/r3/casos/C3-I22/e13.json |
| C3-I23 | --direct com 26 entradas | INDETERMINADO | **INDETERMINADO** | 0 | observado: Relatório gravado em C:/Users/User/requirements-quality-llm-test-oracles/claude-resultados/C3/resultados/r3/casos/C3-I23/e26.json |
| C3-I24 | --direct com expressão pequena | INDETERMINADO | **INDETERMINADO** | 0 | observado: Decisão:   REQ |
| C3-I25 | 21 entradas sem Z3 (acima do limite) | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro: Decisão com 21 entradas; o limite é 20 |
| C3-I26 | TIS: 69 condições | INDETERMINADO | **INDETERMINADO** | 2 | observado: { |
| C3-I27 | TIS: mutantes e detecção | INDETERMINADO | **INDETERMINADO** | 2 | observado: { |
| C3-I28 | VM: 26 testes | INDETERMINADO | **INDETERMINADO** | 0 | observado: { |
| C3-I29 | --constraint com arquivo | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro: --constraint só vale com uma expressão direta. |
| C3-I30 | .mcdc com linha sem identificador | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro: Linha 2 sem identificador. Formato: REQ-001: expressão |
| C3-I31 | JSON com ids repetidos | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro: Decisão repetida: s#1 |
| C3-I32 | Formato desconhecido | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro: Formato desconhecido para analyze: xml. Use text, json, csv, truth-csv. |
| C3-I33 | Arquivo inexistente | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro de arquivo: C:\Users\User\requirements-quality-llm-test-oracles\claude-resultados\C3\experimento\entradas\nao-existe.mcdc |
| C3-I34 | Detecção de mutantes de A and (B or C) | INDETERMINADO | **INDETERMINADO** | 0 | observado: Decisão:   REQ |
| C3-I35 | check com --format csv | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro: Formato desconhecido para check: csv. Use text, json. |
| C3-I36 | JSON inválido | INDETERMINADO | **INDETERMINADO** | 1 | observado: Erro: JSON inválido: Unexpected character ('i' (code 105)): was expecting double-quote to start field name |
| C3-I37 | Comando desconhecido | INDETERMINADO | **INDETERMINADO** | 1 | observado: Uso: |
| C3-I38c | check com mudança de condição sem mudança de resultado | INDETERMINADO | **INDETERMINADO** | 2 | observado: Decisão:   D |
| C3-I39 | Classificação de condições com --z3 e fronteiras no TIS | INDETERMINADO | **INDETERMINADO** | 2 | observado: { |
| C3-E01 | check com valores concretos tipados (int, real, enum, bool) | DETERMINADO | **PASSOU** | 2 | ✔ check_divergentes: divergentes ['U4', 'U5'] |
| C3-E02 | Valores concretos e fronteiras com <, >=, <=, != e negativos | DETERMINADO | **PASSOU** | 0 | ✔ valores_realizam: 6 testes com valores concretos conferidos; ✔ fronteira: x: observados [-3.0, -2.0, 0.0, 2.0, 3.0] |
| C3-E03 | Comparações ==, != e < com negativo | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 8 combinações conferidas |
| C3-E04 | verify em JSON sem --context | DETERMINADO | **PASSOU** | 2 | ✔ json_valido: JSON válido; ✔ sem_lacunas_json: gaps: {'checked': False, 'context': None, 'found': False, 'witness': None} |

## Rodada r4

| ID | Título | Oráculo | Resultado | Exit | Detalhe |
|---|---|---|---|---|---|
| C3-T01 | Tabela-verdade de (A and B) or C | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 8 combinações conferidas; ✔ linha0_tudo_verdadeiro: V1 tudo T |
| C3-T02 | Operadores && e || | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 8 combinações conferidas |
| C3-T03 | Operadores DFRS e precedência | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 8 combinações conferidas |
| C3-T04 | Precedência e antes de ou | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 8 combinações conferidas |
| C3-T05 | Negação com not | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 4 combinações conferidas |
| C3-T06 | Negação com ! | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 4 combinações conferidas |
| C3-T07 | Comparações como entradas | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 4 combinações conferidas |
| C3-T08 | Pares no mascaramento: cada condição demonstrada | DETERMINADO | **PASSOU** | 0 | ✔ todas_condicoes_com_par: cobertura: completa; pares por condição: {A: 1, B: 1, C: 6}; ✔ pares_mudam_condicao: 8 pares conferidos; ✔ suite_alterna_condicoes: suíte de 4 testes alterna ['A', 'B', 'C'] |
| C3-T09 | Pares na causa única: cada condição demonstrada | DETERMINADO | **PASSOU** | 0 | ✔ todas_condicoes_com_par: cobertura: completa; pares por condição: {A: 1, B: 1, C: 3}; ✔ pares_mudam_condicao: 5 pares conferidos; ✔ suite_alterna_condicoes: suíte de 4 testes alterna ['A', 'B', 'C'] |
| C3-T10 | Tabela-verdade com entrada repetida | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 8 combinações conferidas |
| C3-T11 | Expressão inválida: parêntese aberto | DETERMINADO | **PASSOU** | 1 | ✔ recusada: recusada: Erro: REQ: Faltou fechar parêntese |
| C3-T12 | Expressão inválida: operando ausente | DETERMINADO | **PASSOU** | 1 | ✔ recusada: recusada: Erro: REQ: Expressão incompleta: esperava uma condição |
| C3-T13 | Arquivo .mcdc de exemplo | DETERMINADO | **PASSOU** | 2 | ✔ requisitos: ['REQ-001', 'REQ-002', 'REQ-003']; ✔ tabela_verdade: 8 combinações conferidas; ✔ tabela_verdade: 4 combinações conferidas; ✔ tabela_verdade: 4 combinações conferidas |
| C3-T14 | Arquivo .mcdc com erro de sintaxe | DETERMINADO | **PASSOU** | 1 | ✔ recusada: recusada: Erro: REQ-ERRO: Faltou fechar parêntese; ✔ erro_menciona: cita REQ-ERRO |
| C3-T15vm | JSON NAT2TEST VM: contagens e rastreabilidade | DETERMINADO | **PASSOU** | 0 | ✔ json_valido: JSON válido; ✔ sistema: {"decisoes": 5, "combinacoes": 152, "condicoes": 21} |
| C3-T15npp | JSON NAT2TEST NPP: contagens e rastreabilidade | DETERMINADO | **PASSOU** | 0 | ✔ json_valido: JSON válido; ✔ sistema: {"decisoes": 11, "combinacoes": 76, "condicoes": 29} |
| C3-T15tis | JSON NAT2TEST TIS: decisões e combinações | DETERMINADO | **PASSOU** | 2 | ✔ json_valido: JSON válido; ✔ sistema: {"decisoes": 17, "combinacoes": 268} |
| C3-T16 | Mutação: tipos de defeito | DETERMINADO | **PASSOU** | 0 | ✔ mutacao_tipos: tipos: ORF 2/2, ENF 2/2, VNF 3/3, ASF 0/1, MVF 3/3, VRF 6/6 |
| C3-T17vm | Mutação VM: total de mutantes | DETERMINADO | **PASSOU** | 0 | ✔ mutantes_total: total 152, equivalentes 0, mortos 152 |
| C3-T17npp | Mutação NPP: total de mutantes | DETERMINADO | **PASSOU** | 0 | ✔ mutantes_total: total 146, equivalentes 0, mortos 146 |
| C3-T18 | Saída em arquivo com -o | DETERMINADO | **PASSOU** | 0 | ✔ arquivo_relatorio: arquivo com 705 caracteres; tela: Relatório gravado em C:/Users/User/requirements-quality-llm-test-oracles/claude- |
| C3-T19 | Formato json no analyze | DETERMINADO | **PASSOU** | 0 | ✔ json_valido: JSON válido; ✔ tabela_verdade: 8 combinações conferidas |
| C3-T20c | check: suíte completa | DETERMINADO | **PASSOU** | 0 | ✔ check_demonstradas: {'A': True, 'B': True, 'C': True} \| completa, 3 de 3 condições demonstradas; ✔ check_divergentes: divergentes [] |
| C3-T21c | check: um teste só | DETERMINADO | **PASSOU** | 2 | ✔ check_demonstradas: {'A': False, 'B': False, 'C': False} \| incompleta, 0 de 3 condições demonstradas; ✔ check_divergentes: divergentes [] |
| C3-T22c | check: resultado esperado errado | DETERMINADO | **PASSOU** | 2 | ✔ check_divergentes: divergentes ['T2'] |
| C3-T23 | check: CSV sem coluna value | DETERMINADO | **PASSOU** | 1 | ✔ recusada: recusada: Erro: C:\Users\User\requirements-quality-llm-test-oracles\claude-resultados\C3\experimento\entradas\check-sem-coluna-value.csv: falta a coluna "value" no cabeça |
| C3-T24 | check com exemplos/decisoes.json e testes.csv | DETERMINADO | **PASSOU** | 2 | ✔ check_divergentes: divergentes ['T4']; ✔ check_demonstradas: {'the_system_mode = idle': False, 'the_coin_sensor = true': True} \| incompleta, 1 de 2 condições demonstradas; ✔ check_demonstradas: {'the_system_mode = choice': True, 'the_coffee_request_button = true': False, 'the_coin_sensor = true': False} \| incompleta, 1 de 3 condições demonstradas |
| C3-T25c | check com formato json | DETERMINADO | **PASSOU** | 0 | ✔ json_valido: JSON válido |
| C3-T26 | verify sem --context não aponta lacunas | DETERMINADO | **PASSOU** | 2 | ✔ sem_lacunas: não conferidas (use --context "<expressão>" para dizer em que situação alguma guarda deve valer) |
| C3-T27 | Fronteiras de speed > 100 e speed > 50 | DETERMINADO | **PASSOU** | 0 | ✔ fronteira: speed: observados [50.0, 51.0, 100.0, 101.0] |
| C3-T28 | Fronteiras de <=, < e >= | DETERMINADO | **PASSOU** | 0 | ✔ fronteira: x: observados [0.0, 10.0, 11.0]; ✔ fronteira: y: observados [0.0, 4.0, 5.0, 6.0, 7.0] |
| C3-T29 | Fronteiras nos sistemas TIS e NPP (inteiros) | DETERMINADO | **PASSOU** | 0 | ✔ fronteira: the_water_pressure: observados [0.0, 8.0, 9.0, 10.0] |
| C3-T30 | Valores concretos realizam a combinação | DETERMINADO | **PASSOU** | 0 | ✔ valores_realizam: 26 testes com valores concretos conferidos |
| C3-T31 | Valores concretos em expressão direta | DETERMINADO | **PASSOU** | 0 | ✔ valores_realizam: 3 testes com valores concretos conferidos |
| C3-T32 | Restrição escrita à mão | DETERMINADO | **PASSOU** | 0 | ✔ suite_respeita: 5 vetores usados, todos dentro da restrição; ✔ todas_condicoes_com_par: cobertura: completa; pares por condição: {A: 3, B: 1, C: 1} |
| C3-T33 | 20 entradas na tabela completa | DETERMINADO | **PASSOU** | 0 | ✔ arquivo_json: 1048576 combinações, 20 condições com par, suíte 21 |
| C3-E01 | check com valores concretos tipados (int, real, enum, bool) | DETERMINADO | **PASSOU** | 2 | ✔ check_divergentes: divergentes ['U4', 'U5'] |
| C3-E02 | Valores concretos e fronteiras com <, >=, <=, != e negativos | DETERMINADO | **PASSOU** | 0 | ✔ valores_realizam: 6 testes com valores concretos conferidos; ✔ fronteira: x: observados [-3.0, -2.0, 0.0, 2.0, 3.0] |
| C3-E03 | Comparações ==, != e < com negativo | DETERMINADO | **PASSOU** | 0 | ✔ tabela_verdade: 8 combinações conferidas |
| C3-E04 | verify em JSON sem --context | DETERMINADO | **PASSOU** | 2 | ✔ json_valido: JSON válido; ✔ sem_lacunas_json: gaps: {'checked': False, 'context': None, 'found': False, 'witness': None} |
