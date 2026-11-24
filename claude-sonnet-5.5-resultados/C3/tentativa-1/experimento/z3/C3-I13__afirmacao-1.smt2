; Caso C3-I13 - afirmacao-1
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const linhas Real)(declare-const desvios Real)
(assert (and (= linhas 95.5) (= desvios 90.3)))
(check-sat)
(get-model)
