; Conflito textual: criterio do par de independencia (linhas 85 e 87).
(set-logic ALL)

(declare-const decisao_precisa_mudar Bool)
; S1: linha 85: a condicao muda, o resultado da decisao tambem muda
; S2: linha 87: o resultado da decisao pode permanecer igual [...] mudanca isolada e suficiente


(echo "S1 isolada")
(push)
(assert decisao_precisa_mudar) ; S1
(check-sat)
(pop)

(echo "S2 isolada")
(push)
(assert (not decisao_precisa_mudar)) ; S2
(check-sat)
(pop)

(echo "S1 e S2")
(push)
(assert decisao_precisa_mudar) ; S1
(assert (not decisao_precisa_mudar)) ; S2
(check-sat)
(pop)
