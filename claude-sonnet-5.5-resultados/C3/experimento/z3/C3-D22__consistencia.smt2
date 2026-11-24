; Caso C3-D22 - consistencia
; Resposta esperada da formula: sat
(set-logic QF_LIA)
(declare-const t Int)
(assert (= t 26))
(check-sat)
(get-model)
