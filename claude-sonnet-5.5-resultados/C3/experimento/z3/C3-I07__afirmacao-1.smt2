; Caso C3-I07 - afirmacao-1
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const csvTemSuite Bool)
(assert csvTemSuite)
(check-sat)
(get-model)
