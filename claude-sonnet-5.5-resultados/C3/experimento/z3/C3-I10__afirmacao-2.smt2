; Caso C3-I10 - afirmacao-2
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const gulosa Int)(declare-const exata Int)
(assert (<= gulosa exata))
(check-sat)
(get-model)
