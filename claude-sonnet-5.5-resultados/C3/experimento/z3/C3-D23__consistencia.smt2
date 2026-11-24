; Caso C3-D23 - consistencia
; Resposta esperada da formula: sat
(set-logic QF_LIA)
(declare-const c Int)
(assert (= c 0))(assert (= (+ 0 3 1) 4))
(check-sat)
(get-model)
