; Caso C3-D01 - min-suite-2-insat
; Resposta esperada da formula: unsat
(set-logic QF_UF)
(define-fun f ((A Bool) (B Bool)) Bool (and A (not B)))
(declare-const r0_A Bool)
(declare-const r0_B Bool)
(declare-const r1_A Bool)
(declare-const r1_B Bool)
(assert (or (and (= r0_B r1_B) (not (= r0_A r1_A)) (not (= (f r0_A r0_B) (f r1_A r1_B))))))
(assert (or (and (= r0_A r1_A) (not (= r0_B r1_B)) (not (= (f r0_A r0_B) (f r1_A r1_B))))))
(check-sat)
(get-model)
