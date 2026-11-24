; Caso C3-I05 - afirmacao-1
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const limiteDireto Int)
(assert (= limiteDireto 30))
(check-sat)
(get-model)
