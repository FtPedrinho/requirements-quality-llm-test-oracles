; Caso C3-D17 - consistencia
; Resposta esperada da formula: sat
(set-logic QF_LIA)
(declare-const tot Int)
(assert (= tot (+ 26 80 40)))(assert (= tot 146))(assert (= (+ 152 268 76) 496))(assert (= (+ 4 4 1) 9))(assert (= (+ 5 17 11) 33))
(check-sat)
(get-model)
