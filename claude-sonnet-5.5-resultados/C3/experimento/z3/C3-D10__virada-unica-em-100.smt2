; Caso C3-D10 - virada-unica-em-100
; Resposta esperada da formula: unsat
(set-logic QF_LIA)
(declare-const speed Int)
(assert (not (> speed 100)))(assert (> (+ speed 1) 100))(assert (not (= speed 100)))
(check-sat)
