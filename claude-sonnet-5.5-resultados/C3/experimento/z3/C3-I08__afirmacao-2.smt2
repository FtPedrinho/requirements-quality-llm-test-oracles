; Caso C3-I08 - afirmacao-2
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const unsatImpossivel Bool)
(assert (not unsatImpossivel))
(check-sat)
(get-model)
