; Caso C3-I16 - afirmacao-1
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const asfGarantido Bool)
(assert asfGarantido)
(check-sat)
(get-model)
