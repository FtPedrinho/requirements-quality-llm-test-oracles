; Caso C3-I25 - fronteira-50-unica
; Resposta esperada da formula: unsat
(set-logic QF_LIA)
(declare-const x Int)
(assert (not (> x 50)))(assert (> (+ x 1) 50))(assert (not (= x 50)))
(check-sat)
