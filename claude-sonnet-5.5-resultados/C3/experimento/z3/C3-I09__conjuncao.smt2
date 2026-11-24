; Caso C3-I09 - conjuncao
; Resposta esperada da formula: unsat
(set-logic ALL)
(declare-const resultadoPrecisaMudar Bool)
(assert resultadoPrecisaMudar)
(assert (not resultadoPrecisaMudar))
(check-sat)
