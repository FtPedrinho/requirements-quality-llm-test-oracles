; Caso C3-I05 - conjuncao
; Resposta esperada da formula: unsat
(set-logic ALL)
(declare-const limiteDireto Int)
(assert (= limiteDireto 30))
(assert (= limiteDireto 12))
(check-sat)
