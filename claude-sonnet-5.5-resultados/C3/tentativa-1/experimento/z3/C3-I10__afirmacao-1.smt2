; Caso C3-I10 - afirmacao-1
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const gulosa Int)(declare-const exata Int)
(assert (and (= gulosa 6) (= exata 5)))
(check-sat)
(get-model)
