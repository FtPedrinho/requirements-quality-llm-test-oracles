# Resultados por caso — C1

Unidade de contagem: um caso = um ID do oráculo (todas as suas asserções precisam valer para PASSOU).
`rodada-01` = baseline (preservado); `rodada-02` = mesma suíte com a correção 01 (codificação do stdout), referência do baseline corrigido; `rodada-03` = extensão 01. O veredito final é o da rodada-02 (AN/SY/CK/VF) ou da rodada-03 (EX).

| ID | Oráculo | rodada-01 | Veredito final | Códigos de saída observados | Expectativa / observação |
|---|---|---|---|---|---|
| AN-01 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"exit": 0} |
| AN-02 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"exit": 0, "testes_distintos": 4, "linhas_dados": "testes_distintos * 3"} |
| AN-03 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"exit": 0} |
| AN-04 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"exit": 0, "testes_distintos": 3} |
| AN-05 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"exit": 0} |
| AN-06 | DETERMINADO | PASSOU | **PASSOU** | 0, 0, 0 | {"exit": 0, "linhas_dados": 8, "resultado_por_linha": "(A and B) or not C"} |
| AN-07 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"exit": 0, "linhas_dados": 8, "resultado_por_linha": "A or (B and C)"} |
| AN-08 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"exit": 0} |
| AN-09 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"exit": 0} |
| AN-10 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"exit": 0, "linhas_dados": 8, "resultado_por_linha": "(A and B) or (not A and C)"} |
| AN-11 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"exit": 0, "linhas_dados": 8, "primeira_linha_toda_verdadeira": true, "resultado_por_linha": "(A and B) or C"} |
| AN-12 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"testes_distintos": 8} |
| AN-13 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"exit": 0} |
| AN-14 | DETERMINADO | PASSOU | **PASSOU** | 2 | {"exit": 2} |
| AN-15 | DETERMINADO | PASSOU | **PASSOU** | 2 | {"exit": 2} |
| AN-16 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"exit": 0} |
| AN-17 | DETERMINADO | PASSOU | **PASSOU** | 1 | {"exit": 1} |
| AN-18 | DETERMINADO | PASSOU | **PASSOU** | 1 | {"exit": 1} |
| AN-19 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"exit": 0} |
| AN-20 | DETERMINADO | PASSOU | **PASSOU** | 1 | {"exit": 1} |
| AN-21 | DETERMINADO | PASSOU | **PASSOU** | 1 | {"exit": 1} |
| AN-22 | DETERMINADO | FALHOU\* | **PASSOU** | 0, 0 | {"exit": 0, "arquivo_igual_stdout_sem_o": true, "stdout_com_o_sem_relatorio": true} |
| AN-23 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"exit": 0, "json_valido": true} |
| AN-24 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"exit": 0} |
| AN-25 | INDETERMINADO | INDETERMINADO | **INDETERMINADO** | 1 | INDETERMINADO: Omissão: o texto não diz se recusa, muda de modo ou qual código de saída. (executado só como diagnóstico) |
| AN-26 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"exit": 0} |
| AN-27 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"testes_distintos": 5} |
| AN-28 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"testes_distintos": 6} |
| AN-29 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"linhas_dados": 8, "impossiveis": "exatamente as 2 linhas com speed>100=T e speed>50=F"} |
| AN-30 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"exit": 0, "valores_realizam_guarda": true} |
| AN-31 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"valores_fronteira_speed_incluem": [100, 101, 50, 51]} |
| AN-32 | DETERMINADO | PASSOU | **PASSOU** | 1 | {"aviso_z3": true} |
| AN-33 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"exit": 0} |
| AN-34 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"exit": 0} |
| AN-35 | INDETERMINADO | INDETERMINADO | **INDETERMINADO** | 1 | INDETERMINADO: Omissão do comportamento além do limite. (executado só como diagnóstico) |
| AN-36 | INDETERMINADO | INDETERMINADO | **INDETERMINADO** | 1 | INDETERMINADO: Omissão. (executado só como diagnóstico) |
| AN-37 | INDETERMINADO | INDETERMINADO | **INDETERMINADO** | 1 | INDETERMINADO: Ambiguidade. (executado só como diagnóstico) |
| AN-38 | INDETERMINADO | INDETERMINADO | **INDETERMINADO** | 0 | INDETERMINADO: Omissão da definição de causa única para ocorrências acopladas. (executado só como diagnóstico) |
| AN-39 | INDETERMINADO | INDETERMINADO | **INDETERMINADO** | 1 | INDETERMINADO: Omissão. (executado só como diagnóstico) |
| AN-40 | INDETERMINADO | INDETERMINADO | **INDETERMINADO** | 1 | INDETERMINADO: Omissão. (executado só como diagnóstico) |
| AN-41 | DETERMINADO | PASSOU | **PASSOU** | 1 | {"exit": 1} |
| AN-42 | DETERMINADO | PASSOU | **PASSOU** | 2 | {"exit": 2} |
| AN-43 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"exit": 0} |
| AN-44 | INDETERMINADO | INDETERMINADO | **INDETERMINADO** | 1 | INDETERMINADO: Ambiguidade. (executado só como diagnóstico) |
| SY-VM-01 | DETERMINADO | PASSOU | **PASSOU** | 0, 0 | {"decisoes": 5, "condicoes": 21, "combinacoes": 152, "impossiveis": 4, "testes": 26, "testes_por_decisao_igual_condicoes_mais_1": true, "requisitos_rastreados": true} |
| SY-VM-02 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"mutantes": 152, "equivalentes": 0, "pegos": 152} |
| SY-VM-03 | DETERMINADO | PASSOU | **PASSOU** | 0, 0 | {"conflitos": 0, "exit": 0} |
| SY-VM-04 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"testes": 26} |
| SY-VM-05 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"testes": 26} |
| SY-VM-06 | DETERMINADO | PASSOU | **PASSOU** | 0, 0 | {"cobertura_e_diagnostico_iguais": true} |
| SY-TIS-01 | DETERMINADO | PASSOU | **PASSOU** | 2, 2 | {"decisoes": 17, "condicoes": 69, "combinacoes": 268, "impossiveis": 4, "testes": 80, "requisitos_rastreados": true} |
| SY-TIS-02 | DETERMINADO | PASSOU | **PASSOU** | 2 | {"mutantes": 450, "equivalentes": 21, "pegos": 428} |
| SY-TIS-03 | DETERMINADO | PASSOU | **PASSOU** | 2, 2 | {"conflitos": 3, "exit": 2} |
| SY-TIS-04 | DETERMINADO | PASSOU | **PASSOU** | 2 | {"testes": 80} |
| SY-TIS-05 | DETERMINADO | PASSOU | **PASSOU** | 2 | {"testes": 80} |
| SY-TIS-06 | DETERMINADO | PASSOU | **PASSOU** | 2, 2 | {"cobertura_e_diagnostico_iguais": true} |
| SY-NPP-01 | DETERMINADO | PASSOU | **PASSOU** | 0, 0 | {"decisoes": 11, "condicoes": 29, "combinacoes": 76, "impossiveis": 1, "testes": 40, "testes_por_decisao_igual_condicoes_mais_1": true, "requisitos_rastreados": true} |
| SY-NPP-02 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"mutantes": 146, "equivalentes": 0, "pegos": 146} |
| SY-NPP-03 | DETERMINADO | PASSOU | **PASSOU** | 2, 2 | {"conflitos": 1, "exit": 2} |
| SY-NPP-04 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"testes": 40} |
| SY-NPP-05 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"testes": 40} |
| SY-NPP-06 | DETERMINADO | PASSOU | **PASSOU** | 0, 0 | {"cobertura_e_diagnostico_iguais": true} |
| SY-VM-07 | DETERMINADO | PASSOU | **PASSOU** | 2 | {"exit": 2} |
| SY-TIS-07 | INDETERMINADO | INDETERMINADO | **INDETERMINADO** | 2 | INDETERMINADO: O texto não define 'requisito completo'; N+1 só vale para completos (Q07_TIS_nao_completos: 69+17≠80). (executado só como diagnóstico) |
| CK-01 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"exit": 0} |
| CK-02 | DETERMINADO | PASSOU | **PASSOU** | 2 | {"exit": 2} |
| CK-03 | DETERMINADO | PASSOU | **PASSOU** | 2 | {"exit": 2} |
| CK-04 | DETERMINADO | PASSOU | **PASSOU** | 1 | {"exit": 1} |
| CK-05 | DETERMINADO | PASSOU | **PASSOU** | 2 | {"exit": 2} |
| CK-06 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"json_valido": true} |
| CK-07 | DETERMINADO | PASSOU | **PASSOU** | 1 | {"exit": 1} |
| CK-08 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"exit": 0} |
| VF-01 | DETERMINADO | PASSOU | **PASSOU** | 2 | {"exit": 2} |
| VF-02 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"exit": 0} |
| VF-03 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"exit": 0} |
| VF-04 | DETERMINADO | PASSOU | **PASSOU** | 2 | {"exit": 2} |
| VF-05 | DETERMINADO | PASSOU | **PASSOU** | 0 | {"exit": 0} |
| VF-06 | DETERMINADO | PASSOU | **PASSOU** | 2 | {"json_valido": true} |
| VF-07 | DETERMINADO | PASSOU | **PASSOU** | 1 | {"exit": 1} |
| EX-01 | DETERMINADO | — | **PASSOU** | 0 | {"exit": 0} |
| EX-02 | DETERMINADO | — | **PASSOU** | 0 | {"json_valido": true} |
| EX-03 | DETERMINADO | — | **PASSOU** | 0 | {"exit": 0} |
| EX-04 | DETERMINADO | — | **PASSOU** | 1 | {"exit": 1, "stderr_contem": "3"} |
| EX-05 | DETERMINADO | — | **PASSOU** | 0 | {"exit": 0, "csv_coluna_igual": {"coluna": "requirement", "valor": "R-1, R-2"}} |
| EX-06 | DETERMINADO | — | **PASSOU** | 1 | {"exit": 1} |
| EX-07 | DETERMINADO | — | **PASSOU** | 1 | {"exit": 1} |
| EX-08 | DETERMINADO | — | **PASSOU** | 1 | {"exit": 1} |
| EX-09 | DETERMINADO | — | **PASSOU** | 1 | {"exit": 1} |
| EX-10 | DETERMINADO | — | **PASSOU** | 1 | {"exit": 1} |
| EX-11 | DETERMINADO | — | **PASSOU** | 1 | {"exit": 1} |
| EX-12 | DETERMINADO | — | **PASSOU** | 1 | {"exit": 1} |
| EX-13 | DETERMINADO | — | **PASSOU** | 0 | {"linhas_dados": 4, "impossiveis_formula": {"colunas": {"a": "> -3", "b": "< 2"}, "impossivel_sse": "(not a) and (not b)"}} |
| EX-14 | DETERMINADO | — | **PASSOU** | 2 | {"linhas_dados": 8, "impossiveis_formula": {"colunas": {"a": "x > 3", "b": "y <= x", "c": "y > 5"}, "impossivel_sse": "(not a) and b and c"}} |
| EX-15 | DETERMINADO | — | **PASSOU** | 0 | {"linhas_dados": 4, "impossiveis_formula": {"colunas": {"a": ">= 10.5", "b": "<= 30"}, "impossivel_sse": "(not a) and (not b)"}} |
| EX-16 | DETERMINADO | — | **PASSOU** | 0 | {"exit": 0, "guarda_py": "(x < -5) or (x > 5)"} |
| EX-17 | DETERMINADO | — | **PASSOU** | 0 | {"exit": 0, "guarda_py": "(t > 0.5) and (t < 1.0)"} |
| EX-18 | DETERMINADO | — | **PASSOU** | 0 | {"fronteiras_incluem": {"var": "x", "valores": [-3, -2]}} |
| EX-19 | DETERMINADO | — | **PASSOU** | 2, 2 | {"cobertura_e_diagnostico_iguais": true} |
| EX-20 | DETERMINADO | — | **PASSOU** | 0, 0 | {"cobertura_e_diagnostico_iguais": true} |
| EX-21 | DETERMINADO | — | **PASSOU** | 2, 2 | {"cobertura_e_diagnostico_iguais": true} |
| EX-22 | DETERMINADO | — | **PASSOU** | 2, 2 | {"cobertura_e_diagnostico_iguais": true} |
| EX-23 | DETERMINADO | — | **PASSOU** | 0 | {"exit": 0} |
| EX-24 | DETERMINADO | — | **PASSOU** | 0 | {"exit": 0, "pares_max": {"condicao": "A", "max": 1000}} |
| EX-25 | DETERMINADO | — | **PASSOU** | 2 | {"exit": 2, "blocos_linhas": [8, 4, 4]} |
| EX-26 | DETERMINADO | — | **PASSOU** | 0 | {"exit": 0} |
| EX-27 | DETERMINADO | — | **FALHOU** | 0 | {"aviso_z3": true} — **falhou:** saída menciona Z3 (exit 0) |
| EX-28 | DETERMINADO | — | **PASSOU** | 1 | {"aviso_z3": true} |
| EX-29 | INDETERMINADO | — | **INDETERMINADO** | 1 | INDETERMINADO: Omissão. (executado só como diagnóstico) |
| EX-30 | INDETERMINADO | — | **INDETERMINADO** | 1 | INDETERMINADO: Omissão. (executado só como diagnóstico) |
| EX-31 | INDETERMINADO | — | **INDETERMINADO** | 1 | INDETERMINADO: Omissão. (executado só como diagnóstico) |

\* AN-22 na rodada-01: FALHOU por erro técnico de medição (stdout da JVM em Cp1252 decodificado como UTF-8); reclassificado como erro técnico, ver `experimento/correcoes/correcao-01-codificacao-stdout.md`. Na rodada-02 PASSOU, sem mudança de expectativa.

Totais finais: FALHOU: 1, INDETERMINADO: 12, PASSOU: 97 (total 110).
