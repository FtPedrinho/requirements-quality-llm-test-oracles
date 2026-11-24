; Caso C3-I07 - afirmacao-2
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const csvTemSuite Bool)
(assert (not csvTemSuite))
(check-sat)
(get-model)
