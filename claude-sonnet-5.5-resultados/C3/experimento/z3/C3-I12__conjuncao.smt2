; Caso C3-I12 - conjuncao
; Resposta esperada da formula: unsat
(set-logic ALL)
(declare-const processoExterno Bool)
(assert processoExterno)
(assert (not processoExterno))
(check-sat)
