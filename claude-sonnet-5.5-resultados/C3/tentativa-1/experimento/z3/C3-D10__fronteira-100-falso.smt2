; Caso C3-D10 - fronteira-100-falso
; Resposta esperada da formula: sat
(set-logic QF_LIA)
(declare-const speed Int)
(assert (= speed 100))(assert (not (> speed 100)))
(check-sat)
(get-model)
