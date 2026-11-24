; Caso C3-D44 - consistencia
; Resposta esperada da formula: sat
(set-logic QF_LIA)
(declare-const n Int)
(assert (= n 21))(assert (> n 20))
(check-sat)
(get-model)
