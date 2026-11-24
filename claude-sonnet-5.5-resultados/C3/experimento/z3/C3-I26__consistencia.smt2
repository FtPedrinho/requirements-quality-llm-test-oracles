; Caso C3-I26 - consistencia
; Resposta esperada da formula: sat
(set-logic QF_LIA)
(declare-const semPar Int)
(assert (= semPar 1))
(check-sat)
(get-model)
