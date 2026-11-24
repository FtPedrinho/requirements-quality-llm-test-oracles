; Caso C3-I16 - afirmacao-2
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const asfGarantido Bool)
(assert (not asfGarantido))
(check-sat)
(get-model)
