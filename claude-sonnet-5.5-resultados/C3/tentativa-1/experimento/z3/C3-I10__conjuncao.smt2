; Caso C3-I10 - conjuncao
; Resposta esperada da formula: unsat
(set-logic ALL)
(declare-const gulosa Int)(declare-const exata Int)
(assert (and (= gulosa 6) (= exata 5)))
(assert (<= gulosa exata))
(check-sat)
