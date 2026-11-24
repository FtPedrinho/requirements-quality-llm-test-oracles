# Resultados por caso — C4 (rodada `r1-baseline`, final)

Gerado por `avaliacao/gerar_resultados_por_caso.py` a partir de `experimento/oraculo.json` e `resultados/r1-baseline/resultados.json`.

Contagem: FALHOU = 1, INDETERMINADO = 37, PASSOU = 44

Unidade de contagem: caso do oráculo (ID estável). Códigos de saída são registrados, mas nenhum caso os exige.

## Casos determinados

| ID | Execução | Expectativa | Resultado | Observado | Exit |
|---|---|---|---|---|---|
| C4-D01 | X01 | A tabela-verdade analisada tem exatamente 8 combinações (3 entradas distintas). | **PASSOU** | truthTableRows=8 linhas=8 | {'X01': 0} |
| C4-D02 | X01 | A primeira linha (linha 0) tem x=y=z=verdadeiro e a decisão nela é verdadeira. | **PASSOU** | linha0={'vector': 'V1', 'values': {'x': True, 'y': True, 'z': True}, 'outcome': True, 'feasible': True} | {'X01': 0} |
| C4-D03 | X01 | Exatamente 1 das 8 combinações tem decisão verdadeira (x=y=z=V); as outras 7 têm decisão falsa. | **PASSOU** | verdadeiras=1 falsas=7 | {'X01': 0} |
| C4-D04 | X02 | 4 combinações; exatamente 1 com decisão falsa (x=F, y=F) e 3 verdadeiras. | **PASSOU** | linhas=4 falsas=[{'vector': 'V4', 'values': {'x': False, 'y': False}, 'outcome': False, 'feasible': True}] | {'X02': 0} |
| C4-D05 | X03 | 8 combinações (3 entradas distintas p, q, r). | **PASSOU** | truthTableRows=8 | {'X03': 0} |
| C4-D06 | X03 | A decisão tem 4 condições (p, q, p, r). | **PASSOU** | condicoes=['p#1', 'q', 'p#2', 'r'] | {'X03': 0} |
| C4-D07 | X03 | As duas aparições de p aparecem como condições distintas identificadas com os sufixos #1 e #2 (p#1, p#2). | **PASSOU** | labels=['p#1', 'q', 'p#2', 'r'] | {'X03': 0} |
| C4-D08 | X03 | A informação de par de independência é relatada separadamente para p#1 e para p#2 (uma entrada de par por aparição). | **PASSOU** | chaves de pares=['p#1', 'q', 'p#2', 'r'] | {'X03': 0} |
| C4-D09 | X04 | A análise é feita na variante mascaramento (MC/DC de mascaramento). | **PASSOU** | variant=MASKING | {'X04': 0} |
| C4-D10 | X05 | A análise é feita na variante causa única. | **PASSOU** | variant=UNIQUE_CAUSE | {'X05': 0} |
| C4-D11 | X04+X05 | Todo par de independência relatado na variante causa única (X05) também é par válido relatado na variante mascaramento (X04) para a mesma condição. | **PASSOU** | causa_unica={'p': [('V2', 'V6')], 'q': [('V2', 'V4')], 'r': [('V3', 'V4'), ('V5', 'V6'), ('V7', 'V8')]} mascaramento={'p': [('V2', 'V6')], 'q': [('V2', 'V4')], 'r': [('V3', 'V4'), ('V3', 'V6'), ('V3', 'V8'), ('V5', 'V4'), ('V5', 'V6'), ('V5', 'V8'), ('V7', 'V4'), ('V7', 'V6'), ('V7', 'V8')]} fora={} | {'X04': 0, 'X05': 0} |
| C4-D12 | X04 | Nenhuma condição de (p and q) or r é diagnosticada como redundante ou bloqueada; todas têm par. | **PASSOU** | uncovered=[] uncoveredConditions=[] | {'X04': 0} |
| C4-D13 | X05 | Nenhuma condição é diagnosticada como redundante ou bloqueada; todas têm par de causa única. | **PASSOU** | uncovered=[] uncoveredConditions=[] | {'X05': 0} |
| C4-D14 | X06 | A expressão é aceita (analisada, não recusada) com 2 condições: speed > 100 e mode = idle. | **PASSOU** | condicoes=['speed > 100', 'mode = idle'] inputs=[{'name': 'speed > 100', 'variable': 'speed', 'operator': '>', 'value': '100'}, {'name': 'mode = idle', 'variable': 'mode', 'operator': '=', 'value': 'idle'}] | {'X06': 0} |
| C4-D15 | X06 | 4 combinações. | **PASSOU** | truthTableRows=4 | {'X06': 0} |
| C4-D16 | X07 | Das 8 combinações, exatamente 2 são tratadas como impossíveis/excluídas (p=V,q=F,r=V e p=V,q=F,r=F) e 6 são aceitas. | **PASSOU** | impossiveis=[{'p': True, 'q': False, 'r': True}, {'p': True, 'q': False, 'r': False}] | {'X07': 0} |
| C4-D17 | X07 | Nenhum par de independência relatado usa uma combinação com p=V e q=F. | **PASSOU** | impossiveis=['V3', 'V4'] usados_em_pares=['V2', 'V5', 'V6', 'V7', 'V8'] | {'X07': 0} |
| C4-D18 | X08 | A expressão é recusada: nenhuma análise (tabela, pares, suíte) é produzida e a ferramenta sinaliza erro. | **PASSOU** | stdout='' stderr='Erro: REQ: Faltou fechar parêntese' exit=1 | {'X08': 1} |
| C4-D19 | X09 | A expressão é recusada: nenhuma análise é produzida e a ferramenta sinaliza erro. | **PASSOU** | stdout='' stderr='Erro: REQ: Esperava uma condição, encontrei: or' exit=1 | {'X09': 1} |
| C4-D20 | X10 | São analisados exatamente 3 requisitos, identificados REQ-001, REQ-002 e REQ-003; a linha de comentário não vira requisito. | **PASSOU** | ids=['REQ-001', 'REQ-002', 'REQ-003'] | {'X10': 2} |
| C4-D21 | X10 | REQ-001: 3 condições e 8 combinações. | **PASSOU** | condicoes=['alarme_ativo', 'porta_aberta', 'botao_emergencia'] truthTableRows=8 | {'X10': 2} |
| C4-D22 | X10 | REQ-002: 2 condições e 4 combinações. | **PASSOU** | condicoes=['porta_fechada', 'obstaculo'] truthTableRows=4 | {'X10': 2} |
| C4-D23 | X10 | REQ-003: 3 condições (freio_acionado#1, freio_acionado#2, pedal_pressionado) e 4 combinações. | **PASSOU** | condicoes=['freio_acionado#1', 'freio_acionado#2', 'pedal_pressionado'] truthTableRows=4 | {'X10': 2} |
| C4-D24 | X10 | Nenhuma condição de REQ-001 é diagnosticada como redundante ou bloqueada. | **PASSOU** | uncovered=[] uncoveredConditions=[] | {'X10': 2} |
| C4-D25 | X10 | Nenhuma condição de REQ-002 é diagnosticada como redundante ou bloqueada. | **PASSOU** | uncovered=[] uncoveredConditions=[] | {'X10': 2} |
| C4-D26 | X11 | O arquivo é recusado com erro que menciona a linha 3. | **FALHOU** | stdout='' stderr='Erro: REQ-B: Faltou fechar parêntese' exit=1 | {'X11': 1} |
| C4-D27 | X12 | 5 requisitos (decisões) analisados. | **PASSOU** | req=5 | {'X12': 0} |
| C4-D28 | X12 | 21 condições no total. | **PASSOU** | cond=21 | {'X12': 0} |
| C4-D29 | X12 | 152 combinações no total. | **PASSOU** | comb=152 | {'X12': 0} |
| C4-D30 | X13 | 17 requisitos (decisões) analisados. | **PASSOU** | req=17 | {'X13': 2} |
| C4-D31 | X13 | 69 condições no total. | **PASSOU** | cond=69 | {'X13': 2} |
| C4-D32 | X13 | 268 combinações no total. | **PASSOU** | comb=268 | {'X13': 2} |
| C4-D33 | X14 | 11 requisitos (decisões) analisados. | **PASSOU** | req=11 | {'X14': 0} |
| C4-D34 | X14 | 29 condições no total. | **PASSOU** | cond=29 | {'X14': 0} |
| C4-D35 | X14 | 76 combinações no total. | **PASSOU** | comb=76 | {'X14': 0} |
| C4-D36 | X15 | A saída do relatório é JSON válido (analisável). | **PASSOU** | json_valido=True | {'X15': 0} |
| C4-D37 | X15 | O JSON contém um resultado para cada uma das 4 decisões do arquivo, identificado pela decisão (id the_coffee_machine_system#1..#4 ou requisito REQ-001..REQ-004). | **PASSOU** | ids=['the_coffee_machine_system#1', 'the_coffee_machine_system#2', 'the_coffee_machine_system#3', 'the_coffee_machine_system#4'] requirements=['REQ-001', 'REQ-002', 'REQ-003', 'REQ-004'] | {'X15': 0} |
| C4-D38 | X16 | T4 é apontado como teste com resultado esperado errado (a guarda vale F nesses valores, o CSV diz T). | **PASSOU** | problems=['T4: resultado esperado T, mas a guarda dá F para esses valores'] | {'X16': 2} |
| C4-D39 | X16 | T1, T2 e T3 não são apontados como resultado esperado errado. | **PASSOU** | problems=['T4: resultado esperado T, mas a guarda dá F para esses valores'] | {'X16': 2} |
| C4-D40 | X16 | A decisão the_coffee_machine_system#1 não é dada como coberta: falta par para a condição the_system_mode = idle. | **PASSOU** | complete=False demonstrada={'the_system_mode idle': False} | {'X16': 2} |
| C4-D41 | X16 | A decisão the_coffee_machine_system#3 não é dada como coberta: faltam pares para the_coffee_request_button = true e the_coin_sensor = true. | **PASSOU** | complete=False demonstradas={'the_coffee_request_button': False, 'the_coin_sensor': False} | {'X16': 2} |
| C4-D42 | X16 | As decisões the_coffee_machine_system#2 e #4 não são dadas como cobertas (nenhum teste). | **PASSOU** | #2 complete=False testes=0; #4 complete=False testes=0 | {'X16': 2} |
| C4-D43 | X17 | O relatório de mutação cobre os seis tipos ORF, ENF, VNF, MVF, VRF e ASF (cada tipo aparece no relatório). | **PASSOU** | tipos=['ASF', 'ENF', 'MVF', 'ORF', 'VNF', 'VRF'] faltando=[] | {'X17': 0} |
| C4-D44 | X18 | A expressão é aceita e analisada com 1048576 combinações. | **PASSOU** | truthTableRows=1048576 | {'X18': 0} |
| C4-D45 | X18 | Para a condição x01 são guardados/relatados no máximo 1000 pares, embora existam mais de 1000 candidatos. | **PASSOU** | pares_guardados(x01)=1000 pairsTruncated=['x01'] | {'X18': 0} |

## Casos indeterminados (não executados)

| ID | Entrada/tema | Motivo |
|---|---|---|
| C4-I01 | ( and B) or C [--unique-cause] | Omissão: a expressão literal '( and B) or C' tem operando ausente e nenhum resultado é declarado; reconstruir o identificador seria acrescentar semântica. |
| C4-I02 | ( and B) or (not  and C) | Omissão: '( and B) or (not  and C)' com operandos ausentes; nenhum resultado declarado. |
| C4-I03 | " or (B and C)" --constraint "not  or B" | Omissão: expressão ' or (B and C)' e restrição 'not  or B' com operandos ausentes. |
| C4-I04 | " and (B or C)" --mutation | Omissão: expressão ' and (B or C)' com operando ausente; resultados de mutação não declarados. |
| C4-I05 | (( or D) and (not  or D)) or B --exact | Omissão (operandos ausentes) e conflito: o exemplo diz 5 testes com --exact contra 6 da gulosa, mas a 'Garantia de minimização' diz que a gulosa sempre é mínima e --exact usa a mesma heurística e pode retornar suíte maior. |
| C4-I06 | ( ∧ B) ∨ C ; ∧ ¬B | Omissão: exemplos '( ∧ B) ∨ C' e ' ∧ ¬B' com operando ausente. |
| C4-I07 | --format truth-csv | Conflito: truth-csv é descrito como tabela-verdade inteira e, na 'Regra de saída', como 'somente [...] independência, nunca tabela-verdade'. O texto não resolve. |
| C4-I08 | --format csv | Conflito: csv é a suíte (uma linha por teste) e, na 'Regra de saída', o único formato com a tabela-verdade completa. |
| C4-I09 | --z3 (qualquer entrada) | Conflito: o passo 2 diz unsat = impossível; a 'Regra de satisfatibilidade' inverte (sat = impossível) e se declara prevalente para todas as operações, mas a tabela de regressão (4/4/1 impossíveis) só é compatível com a leitura original (Q05: unsat = 4/4/1; sat = 148/264/75). O texto não diz qual afirmação prevalece sobre os números medidos. |
| C4-I10 | vm/tis/npp | Conflito/omissão: 'Testes' 26/80/40/146 dependem das combinações excluídas pelo Z3 (I09) e as opções usadas para medi-los não são informadas. |
| C4-I11 | vm/tis/npp --mutation | Omissão/conflito: Mutantes/Equivalentes/Pegos dependem da suíte gerada com Z3 (I09) e das opções não informadas; não está definido se o total inclui equivalentes (TIS: 428+21 != 450). |
| C4-I12 | verify --json exemplos/npp-decisoes.json (e vm/tis) | Conflito: 'Conflitos' (0/3/1) do verify dependem de satisfatibilidade, e a regra invertida 'vale [para] todas as operações'; além disso, a arquitetura do Z3 é contraditória. |
| C4-I13 | verify --context | Conflito I09/I21 sobre o uso do Z3 e nenhum resultado declarado para a lacuna. |
| C4-I14 | --z3 --boundary | Omissão: a regra de valores de fronteira não é definida; conflito I09. |
| C4-I15 | --direct | Conflito I09/I21: o modo direto depende do Z3; a comparação com a tabela (com ou sem impossíveis) não é especificada. |
| C4-I16 | --exact | Conflito sobre --exact (mínimo pelo Z3 x mesma heurística sem garantia). |
| C4-I17 | tamanho da suíte | Conflito sobre minimalidade da gulosa e omissão: o tamanho da suíte para expressões próprias não é declarado ('pode ter N+1'). |
| C4-I18 | pares de condições sem efeito | Conflito: passo 3 exige que a decisão mude; o 'critério simplificado' admite decisão igual; 'condição sem efeito fica sem par' contradiz o simplificado. Q03-REQ-003 mostra que as leituras divergem (pedal_pressionado: A=unsat, B=sat). |
| C4-I19 | REQ-003 de exemplos/requisitos.mcdc | Conflito: 'REQ-003 tem [uma] condição redundante' x critério simplificado (Q03: pedal_pressionado tem mudança isolada) x 'classificação inversa' (rótulos intercambiáveis). |
| C4-I20 | rótulo de diagnóstico | Conflito: redundante e bloqueada têm definições opostas e são declaradas intercambiáveis. |
| C4-I21 | --z3 sem z3 no PATH | Conflito: Z3 como processo externo no PATH x implementação interna Java x biblioteca nativa na JVM; comportamento sem Z3 no PATH não determinado. |
| C4-I22 | Z3 lento | Conflito: limite de 60 s encerra o processo x 'apenas estimativa [...] nunca encerra'. |
| C4-I23 | códigos de saída | Omissão: o significado dos códigos de saída 0, 1 e 2 não é documentado. |
| C4-I24 | 21 entradas | Omissão: o comportamento acima dos limites (21 entradas na tabela, >12 Z3 linha a linha, >30 modo direto) não é descrito. |
| C4-I25 | coluna Completos | Omissão: 'Completos' (14 de 17 no TIS) não é definido. |
| C4-I26 | JSON NAT2TEST inválido / ids repetidos | Omissão: o resultado para arquivo inválido e ids repetidos não é declarado. |
| C4-I27 | CSV de testes malformado | Omissão/ambiguidade: '[com/sem] coluna decisão' perdeu a palavra; resultado para colunas faltando não declarado. |
| C4-I28 | guarda temporal | Omissão: tratamento do campo temporal (decisoes.json #2) não é descrito. |
| C4-I29 | mutantes equivalentes | Omissão: os operadores de mutação não são definidos; não há como saber quais mutantes são equivalentes para conferir a exclusão da contagem. |
| C4-I30 | --mutation --unique-cause | Conflito e omissão: parênteses deslocados é 'único tipo sem garantia' x 'MC/DC garante [...] qualquer alteração de parênteses'; o texto não associa 'parênteses deslocados' a um dos seis códigos. |
| C4-I31 | saída em arquivo | Omissão: '- relatorio.json' está degradado; não se sabe se é opção de arquivo de saída. |
| C4-I32 | tempo de execução | Ambiguidade ('Tempos medidos [com/sem] contar partida Java') e dependência do ambiente/instrumentação. |
| C4-I33 | aspas no CSV | Omissão: quais células podem conter vírgula não é dito; e o conteúdo do csv está em conflito (I08). |
| C4-I34 | ordem/desempate da gulosa | Conflito: composição da suíte depende do critério de par (I18) e da garantia de minimização (I16). |
| C4-I35 | ordem das linhas | Omissão: só a linha 0 é definida; a ordem das demais linhas não é descrita. |
| C4-I36 | p or q and r | Omissão: 'Prcedência  )' perdeu o conteúdo; a precedência entre and/or não é declarada (ex.: 'p or q and r'). |
| C4-I37 | reais negativos | Omissão: resultado esperado para reais negativos não é declarado (e depende de Z3, I09). |

## Execuções

| Execução | Argumentos | Exit |
|---|---|---|
| X01 | `analyze x and y and z --format json` | 0 |
| X02 | `analyze x or y --format json` | 0 |
| X03 | `analyze (p and q) or (not p and r) --format json` | 0 |
| X04 | `analyze (p and q) or r --format json` | 0 |
| X05 | `analyze (p and q) or r --unique-cause --format json` | 0 |
| X06 | `analyze speed > 100 /\ mode = idle --format json` | 0 |
| X07 | `analyze p or (q and r) --constraint not p or q --format json` | 0 |
| X08 | `analyze p and (q or r --format json` | 1 |
| X09 | `analyze p and or q --format json` | 1 |
| X10 | `analyze -f exemplos/requisitos.mcdc --format json` | 2 |
| X11 | `analyze -f claude-resultados/C4/experimento/entradas/erro-sintaxe.mcdc --format json` | 1 |
| X12 | `analyze --json exemplos/vm-decisoes.json --format json` | 0 |
| X13 | `analyze --json exemplos/tis-decisoes.json --format json` | 2 |
| X14 | `analyze --json exemplos/npp-decisoes.json --format json` | 0 |
| X15 | `analyze --json exemplos/decisoes.json --format json` | 0 |
| X16 | `check --json exemplos/decisoes.json --tests exemplos/testes.csv --format json` | 2 |
| X17 | `analyze p and (q or r) --mutation --format json` | 0 |
| X18 | `analyze x01 and (x02 or x03 or x04 or x05 or x06 or x07 or x08 or x09 or x10 or x11 or x12 or x13 or x14 or x15 or x16 or x17 or x18 or x19 or x20) --format json` | 0 |
