; Caso C3-I31 - consistencia
; Resposta esperada da formula: sat
(set-logic QF_LIA)
(declare-const n Int)
(assert (= n 21))(assert (> n 20))
(check-sat)
(get-model)
