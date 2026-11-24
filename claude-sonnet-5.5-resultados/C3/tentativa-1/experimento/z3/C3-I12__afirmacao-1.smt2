; Caso C3-I12 - afirmacao-1
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const processoExterno Bool)
(assert processoExterno)
(check-sat)
(get-model)
