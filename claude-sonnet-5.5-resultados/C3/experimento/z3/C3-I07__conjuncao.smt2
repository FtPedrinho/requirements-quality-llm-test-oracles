; Caso C3-I07 - conjuncao
; Resposta esperada da formula: unsat
(set-logic ALL)
(declare-const csvTemSuite Bool)
(assert csvTemSuite)
(assert (not csvTemSuite))
(check-sat)
