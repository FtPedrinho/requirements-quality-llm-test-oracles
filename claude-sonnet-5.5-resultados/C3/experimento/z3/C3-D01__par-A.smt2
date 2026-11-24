; Caso C3-D01 - par-A
; Resposta esperada da formula: sat
(set-logic QF_UF)
(define-fun f ((A Bool) (B Bool)) Bool (and A (not B)))
(declare-const a_A Bool)
(declare-const b_A Bool)
(declare-const a_B Bool)
(declare-const b_B Bool)
(assert (= a_B b_B))
(assert (not (= a_A b_A)))
(assert (not (= (f a_A a_B) (f b_A b_B))))
(check-sat)
(get-model)
