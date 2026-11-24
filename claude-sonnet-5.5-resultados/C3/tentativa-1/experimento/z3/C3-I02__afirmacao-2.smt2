; Caso C3-I02 - afirmacao-2
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const iniciavel Bool)
(assert (not iniciavel))
(check-sat)
(get-model)
