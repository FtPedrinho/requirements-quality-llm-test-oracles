; Caso C3-I16 - conjuncao
; Resposta esperada da formula: unsat
(set-logic ALL)
(declare-const asfGarantido Bool)
(assert asfGarantido)
(assert (not asfGarantido))
(check-sat)
