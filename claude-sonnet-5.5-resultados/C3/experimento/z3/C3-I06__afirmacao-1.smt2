; Caso C3-I06 - afirmacao-1
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const colunasObrigatorias Bool)
(assert colunasObrigatorias)
(check-sat)
(get-model)
