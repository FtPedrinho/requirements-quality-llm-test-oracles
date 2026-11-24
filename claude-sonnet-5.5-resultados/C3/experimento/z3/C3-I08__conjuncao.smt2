; Caso C3-I08 - conjuncao
; Resposta esperada da formula: unsat
(set-logic ALL)
(declare-const unsatImpossivel Bool)
(assert unsatImpossivel)
(assert (not unsatImpossivel))
(check-sat)
