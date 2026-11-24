; Caso C3-I04 - afirmacao-1
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const modoDireto Bool)
(assert modoDireto)
(check-sat)
(get-model)
