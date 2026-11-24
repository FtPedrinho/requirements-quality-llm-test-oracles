; Caso C3-I25 - fronteira-50-51
; Resposta esperada da formula: sat
(set-logic QF_LIA)
(declare-const x Int)
(assert (not (> x 50)))(assert (> (+ x 1) 50))
(check-sat)
(get-model)
