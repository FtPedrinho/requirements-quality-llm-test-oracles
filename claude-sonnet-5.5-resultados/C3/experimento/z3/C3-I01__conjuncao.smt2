; Caso C3-I01 - conjuncao
; Resposta esperada da formula: unsat
(set-logic ALL)
(declare-const n Int)
(assert (= n 4))
(assert (= n 3))
(check-sat)
