; Caso C3-I15 - afirmacao-1
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const porModulo Bool)
(assert porModulo)
(check-sat)
(get-model)
