; Caso C3-I04 - afirmacao-2
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const modoDireto Bool)
(assert (not modoDireto))
(check-sat)
(get-model)
