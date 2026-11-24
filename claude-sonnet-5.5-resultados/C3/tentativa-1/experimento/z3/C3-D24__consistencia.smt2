; Caso C3-D24 - consistencia
; Resposta esperada da formula: sat
(set-logic QF_LIA)
(declare-const t Int)
(assert (= t 40))
(check-sat)
(get-model)
