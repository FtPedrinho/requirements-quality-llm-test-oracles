; Caso C3-I05 - afirmacao-2
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const limiteDireto Int)
(assert (= limiteDireto 12))
(check-sat)
(get-model)
