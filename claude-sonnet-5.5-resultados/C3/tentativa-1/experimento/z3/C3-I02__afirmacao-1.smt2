; Caso C3-I02 - afirmacao-1
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const iniciavel Bool)
(assert iniciavel)
(check-sat)
(get-model)
