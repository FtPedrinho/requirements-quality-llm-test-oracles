; Caso C3-I09 - afirmacao-2
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const resultadoPrecisaMudar Bool)
(assert (not resultadoPrecisaMudar))
(check-sat)
(get-model)
