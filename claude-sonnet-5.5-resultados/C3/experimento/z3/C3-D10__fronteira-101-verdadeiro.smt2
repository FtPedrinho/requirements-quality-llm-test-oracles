; Caso C3-D10 - fronteira-101-verdadeiro
; Resposta esperada da formula: sat
(set-logic QF_LIA)
(declare-const speed Int)
(assert (= speed 101))(assert (> speed 100))
(check-sat)
(get-model)
