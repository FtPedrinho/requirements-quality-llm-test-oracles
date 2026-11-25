; Conflito textual: conteudo do formato truth-csv (linhas 5 e 7 da fonte C4).
(set-logic ALL)

(declare-const truthcsv_tem_tabela_completa Bool)
; S1: linha 5: `truth-csv` | tabela-verdade inteira, combinacoes impossiveis marcadas
; S2: linha 7: Regra de saida: truth-csv contem somente [...] independencia, nunca tabela-verdade


(echo "S1 isolada")
(push)
(assert truthcsv_tem_tabela_completa) ; S1
(check-sat)
(pop)

(echo "S2 isolada")
(push)
(assert (not truthcsv_tem_tabela_completa)) ; S2
(check-sat)
(pop)

(echo "S1 e S2")
(push)
(assert truthcsv_tem_tabela_completa) ; S1
(assert (not truthcsv_tem_tabela_completa)) ; S2
(check-sat)
(pop)
