; Caso C3-I01 - afirmacao-2
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const n Int)
(assert (= n 3))
(check-sat)
(get-model)
