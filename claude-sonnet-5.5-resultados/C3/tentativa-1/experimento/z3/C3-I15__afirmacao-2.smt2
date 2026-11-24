; Caso C3-I15 - afirmacao-2
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const porModulo Bool)
(assert (not porModulo))
(check-sat)
(get-model)
