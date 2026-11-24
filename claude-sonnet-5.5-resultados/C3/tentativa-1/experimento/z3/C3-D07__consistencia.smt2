; Caso C3-D07 - consistencia
; Resposta esperada da formula: sat
(set-logic QF_LIA)
(declare-const n Int)(declare-const c Int)
(assert (= n 3))(assert (= c 8))(assert (= c (* 2 2 2)))
(check-sat)
(get-model)
