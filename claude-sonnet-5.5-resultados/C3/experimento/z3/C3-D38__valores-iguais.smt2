; Caso C3-D38 - valores-iguais
; Resposta esperada da formula: unsat
(set-logic QF_LIA)
(declare-const a Int)(declare-const b Int)
(assert (= a b))(assert (not (= a b)))
(check-sat)
