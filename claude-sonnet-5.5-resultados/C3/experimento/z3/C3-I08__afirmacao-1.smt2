; Caso C3-I08 - afirmacao-1
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const unsatImpossivel Bool)
(assert unsatImpossivel)
(check-sat)
(get-model)
