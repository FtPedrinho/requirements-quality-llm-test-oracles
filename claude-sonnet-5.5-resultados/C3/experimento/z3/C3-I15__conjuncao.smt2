; Caso C3-I15 - conjuncao
; Resposta esperada da formula: unsat
(set-logic ALL)
(declare-const porModulo Bool)
(assert porModulo)
(assert (not porModulo))
(check-sat)
