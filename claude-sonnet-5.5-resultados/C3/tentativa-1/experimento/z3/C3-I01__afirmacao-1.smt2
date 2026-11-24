; Caso C3-I01 - afirmacao-1
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const n Int)
(assert (= n 4))
(check-sat)
(get-model)
