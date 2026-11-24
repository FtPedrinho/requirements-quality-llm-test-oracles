; Caso C3-D21 - consistencia
; Resposta esperada da formula: sat
(set-logic QF_LIA)
(declare-const t Int)
(assert (= t 80))
(check-sat)
(get-model)
