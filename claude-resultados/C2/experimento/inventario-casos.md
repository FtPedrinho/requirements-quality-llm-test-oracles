# Inventário de casos do oráculo C2

Gerado de `oraculo.json` (congelado antes da leitura do SUT).

caso = uma invocação da CLI com ID estável; PASSOU se todas as asserções da expectativa são satisfeitas, FALHOU se alguma é contrariada; INDETERMINADO quando não há expectativa única.

| ID | Categoria | Status | Comando | Linhas | Expectativa / motivo | Z3 |
|---|---|---|---|---|---|---|
| A01 | analyze | DETERMINADO | `analyze '(A and B) or C'` | L493, L55, L139, L491 | {"exit": 0, "tamanho_suite": 4, "todas_condicoes_com_par": true, "condicoes": 3} | Q01-AB-or-C-pares, Q15-exata-AB-or-C |
| A02 | analyze | DETERMINADO | `analyze '(A and B) or C' --unique-cause` | L55, L139, L283 | {"exit": 0, "todas_condicoes_com_par": true} | Q01-AB-or-C-pares |
| A03 | analyze | DETERMINADO | `analyze 'A and not B'` | L493, L139 | {"exit": 0, "tamanho_suite": 3, "todas_condicoes_com_par": true} | Q02-A-and-notB-pares, Q18-exata-A-and-notB |
| A04 | operadores | DETERMINADO | `analyze '(A && B) \|\| C'` | L127-L137, L493 | {"exit": 0, "tamanho_suite": 4, "todas_condicoes_com_par": true, "equivalente_a": "A01"} | Q01-AB-or-C-pares |
| A05 | operadores | DETERMINADO | `analyze '(A /\ B) \/ C'` | L127-L137, L493 | {"exit": 0, "tamanho_suite": 4, "todas_condicoes_com_par": true, "equivalente_a": "A01"} | Q01-AB-or-C-pares |
| A06 | operadores | DETERMINADO | `analyze 'A and !B'` | L127-L137, L493 | {"exit": 0, "tamanho_suite": 3, "equivalente_a": "A03"} | Q02-A-and-notB-pares |
| A07 | operadores | DETERMINADO | `analyze 'speed > 100 /\ mode = idle'` | L127-L137, L221-L223, L139 | {"exit": 0, "condicoes": 2, "todas_condicoes_com_par": true} | Q03-speed-mode-pares |
| A08 | operadores | DETERMINADO | `analyze '(x == 5) and (y != 3)'` | L127-L137, L139 | {"exit": 0, "condicoes": 2, "todas_condicoes_com_par": true} | Q04-eq-ne-pares |
| A09 | operadores | DETERMINADO | `analyze '(a < 1) or ((b <= 2) and (c >= 3))'` | L127-L137, L139 | {"exit": 0, "condicoes": 3, "todas_condicoes_com_par": true} | Q05-lt-le-ge-pares |
| A10 | entrada-repetida | DETERMINADO | `analyze '(A and B) or (not A and C)'` | L55, L225-L227, L279 | {"exit": 0, "entradas": 3, "condicoes": 4, "combinacoes": 8, "rotulos_condicoes_contem": ["A#1", "A#2"], "todas_condicoes_com_par": true} | Q06-repetida-tabela |
| A11 | precedencia | INDETERMINADO | `analyze 'A or B and C'` | L515 | INDETERMINADO: L515 'Precedênca ( ates de )': os operadores foram apagados; a fonte não diz se and precede or ou o contrário, nem se a mistura é recusada. |  |
| A12 | entrada-invalida | DETERMINADO | `analyze '(A and B'` | L139, L515 | {"exit": 1} |  |
| A13 | entrada-invalida | DETERMINADO | `analyze 'A and'` | L139, L515 | {"exit": 1} |  |
| A14 | operadores | DETERMINADO | `analyze 'x > -3'` | L523, L139 | {"exit": 0, "condicoes": 1, "todas_condicoes_com_par": true} |  |
| A15 | operadores | INDETERMINADO | `analyze 'x > -y'` | L523 | INDETERMINADO: L523 só nomeia o tema 'sinal de menos só em números' numa lista de testes; não diz o que ocorre com '-y' (recusa com código 1, outra mensagem ou outra interpretação). |  |
| A16 | paridade | DETERMINADO | `analyze {G:paridade3}` | L591 | {"tamanho_suite": 8, "combinacoes": 8} | Q07-paridade-tabela |
| A17 | limites | DETERMINADO | `analyze {G:e20}` | L293/L587, L139 | {"exit": 0, "entradas": 20, "todas_condicoes_com_par": true} | Q08-e20-pares |
| A18 | limites | INDETERMINADO | `analyze {G:e21}` | L293/L587 | INDETERMINADO: A fonte fixa o limite de 20 entradas, mas não diz o que ocorre acima dele (erro, código 1, troca de modo). |  |
| A19 | modo-direto | DETERMINADO | `analyze {G:e13} --z3` | L109, L139 | {"exit": 0, "entradas": 13, "todas_condicoes_com_par": true} | Q08-e13-pares |
| A20 | modo-direto | DETERMINADO | `analyze {G:e26} --direct` | L113/L419, L293/L587, L429 | {"exit": 0, "entradas": 26, "todas_condicoes_com_par": true} | Q08-e26-pares |
| A21 | modo-direto | INDETERMINADO | `analyze {G:e31} --direct` | L293/L587 | INDETERMINADO: Acima de 30 entradas o comportamento não é descrito. |  |
| A22 | diagnostico | DETERMINADO | `analyze 'x > 5 and x > 3' --z3 --unique-cause` | L287, L281, L139 | {"exit": 2, "condicao_classificada": {"x > 3": "bloqueada"}, "condicao_com_par": ["x > 5"], "impossiveis": 1} | Q09-bloqueio-viavel, Q09-bloqueio-livre, Q09-bloqueio-tabela |
| A23 | modo-direto | DETERMINADO | `analyze 'x > 5 and x > 3' --direct --unique-cause` | L113/L419, L287, L139 | {"exit": 2, "condicao_classificada": {"x > 3": "bloqueada"}} | Q09-bloqueio-viavel, Q09-bloqueio-livre |
| A24 | diagnostico | DETERMINADO | `analyze 'A or (A and B)' --unique-cause` | L287, L139 | {"exit": 2, "condicao_classificada": {"B": "redundante"}} | Q10-redundante-livre |
| A25 | restricao | DETERMINADO | `analyze 'A or (B and C)' --constraint 'not A or B'` | L107/L231, L139, L491 | {"exit": 0, "suite_sem_combinacao": {"A": true, "B": false}, "todas_condicoes_com_par": true} | Q11-restricao-pares |
| A26 | restricao | DETERMINADO | `analyze 'A and B' --constraint 'not A or B' --unique-cause` | L107/L231, L287, L139 | {"exit": 2, "condicao_classificada": {"B": "bloqueada"}} | Q12-restricao-bloqueio, Q12-restricao-bloqueio-livre |
| A27 | z3 | DETERMINADO | `analyze 'speed > 100 or (speed > 50 and rain)' --z3 --boundary` | L109, L281, L139, L233-L235 | {"exit": 0, "combinacoes": 8, "impossiveis": 2, "todas_condicoes_com_par": true} | Q13-speed-rain-tabela, Q13-speed-rain-pares |
| A28 | fronteira | DETERMINADO | `analyze 'speed > 100 or (speed > 50 and rain)' --z3 --boundary` | L43 | {"fronteira_contem": {"speed > 100": ["100", "101"], "speed > 50": ["50", "51"]}} | Q14-fronteira-gt100, Q14-fronteira-gt50 |
| A29 | z3 | DETERMINADO | `analyze 'speed > 100 or (speed > 50 and rain)' --z3 --boundary` | L463, L41 | {"concretos_realizam": true} | Q13-speed-rain-tabela |
| A30 | z3 | DETERMINADO | `analyze 'speed > 100 /\ mode = idle' --z3` | L463, L109 | {"exit": 0, "concretos_realizam": true} | Q03-speed-mode-pares |
| A31 | exata | DETERMINADO | `analyze '(A and B) or C' --exact --unique-cause` | L111, L285 | {"exit": 0, "tamanho_suite": 4} | Q15-exata-AB-or-C |
| A32 | exata | DETERMINADO | `analyze '(A or B) and (C or D)' --exact --unique-cause` | L111 | {"exit": 0, "tamanho_suite": 5} | Q16-exata-AorB-and-CorD |
| A33 | exata | DETERMINADO | `analyze 'A and (B or C)' --exact --unique-cause` | L111 | {"exit": 0, "tamanho_suite": 4} | Q17-exata-A-and-BorC |
| A34 | exata | INDETERMINADO | `analyze '((E or D) and (not A or D)) or B' --exact` | L253-L255 | INDETERMINADO: A variável negada foi apagada ('(not  or D)'); a expressão do exemplo não é única. O caso roda como diagnóstico com uma letra escolhida (A), sem expectativa. Além disso o mínimo no mascaramento depende da definição de mascaramento, que a fonte não dá. |  |
| A35 | mutacao | DETERMINADO | `analyze 'A and (B or C)' --mutation` | L289/L117, L139 | {"exit": 0, "todas_condicoes_com_par": true} | Q19-mutacao-pares |
| A36 | mutacao | INDETERMINADO | `analyze 'A and (B or C)' --mutation --format json` | L289/L117 | INDETERMINADO: A fonte só nomeia os seis tipos (ORF, ENF, VNF, MVF, VRF, ASF) sem definir como cada mutante é construído; o número de mutantes, equivalentes e detectados desta expressão não é derivável. |  |
| A37 | gulosa | INDETERMINADO | `analyze '(A and B) or C' --format json` | L285 | INDETERMINADO: 'considera primeiro as condições   pars' tem a qualificação apagada (menos/mais pares); quais pares são escolhidos não é derivável. |  |
| F01 | formatos | DETERMINADO | `analyze '(A and B) or C' --format json` | L121, L201-L207, L493 | {"exit": 0, "json_valido": true, "tamanho_suite": 4} |  |
| F02 | formatos | DETERMINADO | `analyze '(A and B) or C' --format csv` | L121, L201-L207, L493 | {"exit": 0, "csv_linhas_dados": 12, "csv_resultado_esperado_correto": true} |  |
| F03 | formatos | DETERMINADO | `analyze '(A and B) or C' --format truth-csv` | L121, L201-L207, L485, L279 | {"exit": 0, "truth_linhas": 8, "truth_primeira_tudo_verdadeiro": true, "truth_resultado_correto": true} |  |
| F04 | formatos | DETERMINADO | `analyze 'speed > 100 or (speed > 50 and rain)' --z3 --format truth-csv` | L201-L207, L281 | {"exit": 0, "truth_linhas": 8, "truth_impossiveis_marcadas": 2} | Q13-speed-rain-tabela |
| F05 | formatos | DETERMINADO | `analyze '(A and B) or C' -o {OUT}/F05-relatorio.txt` | L123 | {"exit": 0, "arquivo_gerado": "{OUT}/F05-relatorio.txt", "stdout_sem_relatorio": true} |  |
| F06 | formatos | DETERMINADO | `analyze --json {EX}/vm-decisoes.json --format json` | L201-L207 | {"json_valido": true, "rastreabilidade": {"vm#1": "REQ001", "vm#2": "REQ002", "vm#3": "REQ003", "vm#4": "REQ004", "vm#5": "REQ005"}} |  |
| F07 | formatos | INDETERMINADO | `check '(A and B)' --tests {ENT}/c02-completo.csv --format csv` | L121 | INDETERMINADO: L121 diz que check aceita text e json, mas não diz o que ocorre com outro formato (código 1, ignorar, outro). |  |
| M01 | mcdc-arquivo | DETERMINADO | `analyze -f {EX}/requisitos.mcdc` | L241-L243, L287, L139 | {"exit": 2, "requisitos": 3, "requisito_tem_classe": {"REQ-003": "redundante"}} |  |
| M02 | mcdc-arquivo | DETERMINADO | `analyze -f {EX}/requisitos.mcdc` | L493, L491 | {"tamanho_suite_por_requisito": {"REQ-001": 4, "REQ-002": 3}, "requisitos_com_todas_com_par": ["REQ-001", "REQ-002"]} | Q01-AB-or-C-pares, Q02-A-and-notB-pares |
| M03 | mcdc-arquivo | DETERMINADO | `analyze -f {ENT}/m03-comentarios.mcdc` | L143, L139 | {"exit": 0, "requisitos": 1} | Q25-check-AandB-pares |
| M04 | mcdc-arquivo | DETERMINADO | `analyze -f {ENT}/m04-erro-sintaxe.mcdc` | L517, L139 | {"exit": 1} |  |
| M05 | mcdc-arquivo | INDETERMINADO | `analyze -f {ENT}/m05-sem-id.mcdc` | L517, L143 | INDETERMINADO: L517 só nomeia o tema 'linha sem identificador'; não diz se é erro, se é ignorada ou se recebe id automático. |  |
| JVM1 | sistemas | DETERMINADO | `analyze --json {EX}/vm-decisoes.json --z3 --mutation --format json` | L467-L477, L461, L289/L117, L139 | {"requisitos": 5, "condicoes": 21, "combinacoes": 152, "impossiveis": 4, "tamanho_suite": 26, "mutantes": {"total": 152, "equivalentes": 0, "detectados": 152}, "exit": 0, "todas_condicoes_com_par": true} | VM-totais |
| JVM2 | sistemas | DETERMINADO | `analyze --json {EX}/vm-decisoes.json --exact --format json` | L461, L467-L477, L111 | {"tamanho_suite": 26} |  |
| JVM3 | sistemas | DETERMINADO | `analyze --json {EX}/vm-decisoes.json --z3 --unique-cause --format json` | L461, L467-L477 | {"tamanho_suite": 26} |  |
| JVM4 | sistemas | DETERMINADO | `analyze --json {EX}/vm-decisoes.json --z3 --boundary --format json` | L463, L43 | {"concretos_realizam": true} |  |
| JTIS1 | sistemas | DETERMINADO | `analyze --json {EX}/tis-decisoes.json --z3 --mutation --format json` | L467-L477, L461, L289/L117, L139 | {"requisitos": 17, "condicoes": 69, "combinacoes": 268, "impossiveis": 4, "tamanho_suite": 80, "mutantes": {"total": 450, "equivalentes": 21, "detectados": 428}} | TIS-totais |
| JTIS2 | sistemas | DETERMINADO | `analyze --json {EX}/tis-decisoes.json --exact --format json` | L461, L467-L477, L111 | {"tamanho_suite": 80} |  |
| JTIS3 | sistemas | DETERMINADO | `analyze --json {EX}/tis-decisoes.json --z3 --unique-cause --format json` | L461, L467-L477 | {"tamanho_suite": 80} |  |
| JTIS4 | sistemas | DETERMINADO | `analyze --json {EX}/tis-decisoes.json --z3 --boundary --format json` | L463, L43 | {"concretos_realizam": true} |  |
| JNPP1 | sistemas | DETERMINADO | `analyze --json {EX}/npp-decisoes.json --z3 --mutation --format json` | L467-L477, L461, L289/L117, L139 | {"requisitos": 11, "condicoes": 29, "combinacoes": 76, "impossiveis": 1, "tamanho_suite": 40, "mutantes": {"total": 146, "equivalentes": 0, "detectados": 146}, "exit": 0, "todas_condicoes_com_par": true} | NPP-totais |
| JNPP2 | sistemas | DETERMINADO | `analyze --json {EX}/npp-decisoes.json --exact --format json` | L461, L467-L477, L111 | {"tamanho_suite": 40} |  |
| JNPP3 | sistemas | DETERMINADO | `analyze --json {EX}/npp-decisoes.json --z3 --unique-cause --format json` | L461, L467-L477 | {"tamanho_suite": 40} |  |
| JNPP4 | sistemas | DETERMINADO | `analyze --json {EX}/npp-decisoes.json --z3 --boundary --format json` | L463, L43 | {"concretos_realizam": true} |  |
| J01 | sistemas | INDETERMINADO | `analyze --json {EX}/tis-decisoes.json --z3 --format json` | L467-L477, L461 | INDETERMINADO: A fonte não define 'requisito completo' (L461 só diz que nele testes = condições + 1); o critério de contagem não é único. Também o código de saída do TIS depende disso e não é derivável. |  |
| J02 | modo-direto | DETERMINADO | `analyze --json {EX}/vm-decisoes.json --direct --format json` | L113/L419, L139 | {"exit": 0, "todas_condicoes_com_par": true} | VM-totais |
| J03 | json | DETERMINADO | `analyze --json {ENT}/j15-enum.json --z3 --format json` | L153, L281 | {"exit": 0, "combinacoes": 4, "impossiveis": 1, "todas_condicoes_com_par": true} | Q21-enum-tabela, Q21-enum-pares |
| J04 | entrada-invalida | DETERMINADO | `analyze --json {ENT}/j16-invalido.json` | L519, L139 | {"exit": 1} |  |
| J05 | json | INDETERMINADO | `analyze --json {ENT}/j17-ids-repetidos.json` | L519 | INDETERMINADO: L519 só nomeia o tema 'ids repetidos'; não diz se é recusa (código 1) nem outra consequência. |  |
| J06 | formatos | DETERMINADO | `analyze --json {EX}/vm-decisoes.json --z3 --format truth-csv -o {OUT}/J06-tabela.csv` | L201-L207, L123, L467-L477, L251 | {"exit": 0, "arquivo_gerado": "{OUT}/J06-tabela.csv", "truth_linhas_arquivo": 152, "truth_impossiveis_marcadas_arquivo": 4} | VM-totais |
| J07 | formatos | DETERMINADO | `analyze --json {EX}/tis-decisoes.json --z3 --format json -o {OUT}/J07-relatorio.json` | L201-L207, L123, L249 | {"arquivo_gerado": "{OUT}/J07-relatorio.json", "json_valido_arquivo": true, "rastreabilidade_arquivo_qtd": 17} |  |
| Z01 | sem-z3 | DETERMINADO | `analyze --json {EX}/vm-decisoes.json --z3` | L73 | {"aviso_z3": true} |  |
| Z02 | sem-z3 | DETERMINADO | `analyze '(A and B) or C'` | L73, L493 | {"exit": 0, "tamanho_suite": 4} |  |
| Z03 | sem-z3 | DETERMINADO | `verify --json {EX}/npp-decisoes.json` | L73, L83 | {"aviso_z3": true} |  |
| Z04 | sem-z3 | INDETERMINADO | `analyze 'speed > 100' --boundary` | L43, L115 | INDETERMINADO: L115 tem a preposição apagada ('  `--z3`'); não se sabe se --boundary exige --z3, o implica ou é ignorado sem ele. |  |
| K01 | check | DETERMINADO | `check --json {EX}/decisoes.json --tests {EX}/testes.csv` | L51, L183, L139 | {"exit": 2, "check_divergentes": ["T4"], "check_nao_demonstrada": true} | Q23-check-exemplo |
| K02 | check | DETERMINADO | `check 'A and B' --tests {ENT}/c02-completo.csv` | L51, L183, L139, L491 | {"exit": 0, "check_completo": true} | Q25-check-AandB-pares |
| K03 | check | DETERMINADO | `check 'A and B' --tests {ENT}/c03-incompleto.csv` | L51, L139 | {"exit": 2, "check_nao_demonstrada": true} |  |
| K04 | check | DETERMINADO | `check 'A and B' --tests {ENT}/c04-esperado-errado.csv` | L51, L139 | {"exit": 2, "check_divergentes": ["T3"]} |  |
| K05 | check | DETERMINADO | `check 'A and B' --tests {ENT}/c02-completo.csv --format json` | L121, L51 | {"exit": 0, "json_valido": true} |  |
| K06 | check | DETERMINADO | `check --json {ENT}/c06-concretos.json --tests {ENT}/c06-concretos.csv` | L183, L51, L139 | {"exit": 0, "check_completo": true} | Q24-check-concretos |
| K07 | check | DETERMINADO | `check 'A and B' --tests {ENT}/c07-coluna-faltando.csv` | L183, L521, L139 | {"exit": 1} |  |
| V01 | verify | DETERMINADO | `verify --json {EX}/npp-decisoes.json` | L53/L119, L467-L477, L139 | {"exit": 2, "conflitos": 1} | NPP-conflitos |
| V02 | verify | DETERMINADO | `verify --json {EX}/tis-decisoes.json` | L53/L119, L467-L477, L139 | {"exit": 2, "conflitos": 3} | TIS-conflitos |
| V03 | verify | DETERMINADO | `verify --json {EX}/vm-decisoes.json --format json` | L53/L119, L467-L477 | {"json_valido": true, "conflitos": 0} | VM-conflitos |
| V04 | verify | DETERMINADO | `verify --json {EX}/vm-decisoes.json --context 'the_system_mode = preparing_weak'` | L53/L119, L265, L139 | {"exit": 2, "lacuna": true, "conflitos": 0} | Q20-VM-lacuna-preparing_weak, VM-conflitos |
| V05 | verify | DETERMINADO | `verify --json {ENT}/v05-conflito.json` | L53/L119, L503, L139 | {"exit": 2, "conflitos": 1} | V05-conflitos |
| V06 | verify | DETERMINADO | `verify --json {ENT}/v06-mesmo-valor.json --context 'mode = idle'` | L53/L119, L503, L139 | {"exit": 0, "conflitos": 0, "lacuna": false} | V06-conflitos, Q22-V06-lacuna |
| V07 | verify | DETERMINADO | `verify --json {ENT}/v07-disjuntos.json --context 'mode = idle'` | L53/L119, L139 | {"exit": 0, "conflitos": 0, "lacuna": false} | V07-conflitos, Q22-V07-lacuna |
| V08 | verify | DETERMINADO | `verify --json {EX}/vm-decisoes.json --context 'the_system_mode = preparing_weak' --format json` | L121, L53/L119 | {"exit": 2, "json_valido": true, "lacuna": true} | Q20-VM-lacuna-preparing_weak |
| V09 | verify | INDETERMINADO | `verify --json {EX}/vm-decisoes.json` | L53/L119 | INDETERMINADO: A fonte não diz se, sem --context, verify procura lacunas em todo o espaço de estados; o código de saída do VM sem contexto não é único. |  |
| E01 | entrada-invalida | INDETERMINADO | `check 'A and B' --tests {ENT}/nao-existe.csv` | L139 | INDETERMINADO: A fonte não diz se arquivo ausente é 'entrada inválida' (código 1) ou outro erro. |  |
| E02 | entrada-invalida | INDETERMINADO | `comando-inexistente A` | L139 | INDETERMINADO: Não descrito. |  |

Trechos literais, regra e justificativa completos de cada caso estão em `oraculo.json`.
