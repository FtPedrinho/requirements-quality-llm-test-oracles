; Caso C3-I13 - afirmacao-2
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const linhas Real)(declare-const desvios Real)
(assert (= linhas desvios))
(check-sat)
(get-model)
