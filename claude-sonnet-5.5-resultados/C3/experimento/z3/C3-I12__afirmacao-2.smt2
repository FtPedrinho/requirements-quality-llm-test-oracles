; Caso C3-I12 - afirmacao-2
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const processoExterno Bool)
(assert (not processoExterno))
(check-sat)
(get-model)
