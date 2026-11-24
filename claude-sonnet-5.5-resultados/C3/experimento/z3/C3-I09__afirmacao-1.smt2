; Caso C3-I09 - afirmacao-1
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const resultadoPrecisaMudar Bool)
(assert resultadoPrecisaMudar)
(check-sat)
(get-model)
