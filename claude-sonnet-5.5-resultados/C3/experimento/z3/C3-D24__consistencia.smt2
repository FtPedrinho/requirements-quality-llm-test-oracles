; Caso C3-D24 - consistencia
; Resposta esperada da formula: sat
(set-logic QF_LIA)
(declare-const c Int)
(assert (= c 3))(assert (= (+ 0 3 1) 4))
(check-sat)
(get-model)
