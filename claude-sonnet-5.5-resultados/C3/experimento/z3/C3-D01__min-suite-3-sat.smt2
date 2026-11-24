; Caso C3-D01 - min-suite-3-sat
; Resposta esperada da formula: sat
(set-logic QF_UF)
(define-fun f ((A Bool) (B Bool)) Bool (and A (not B)))
(declare-const r0_A Bool)
(declare-const r0_B Bool)
(declare-const r1_A Bool)
(declare-const r1_B Bool)
(declare-const r2_A Bool)
(declare-const r2_B Bool)
(assert (or (and (= r0_B r1_B) (not (= r0_A r1_A)) (not (= (f r0_A r0_B) (f r1_A r1_B)))) (and (= r0_B r2_B) (not (= r0_A r2_A)) (not (= (f r0_A r0_B) (f r2_A r2_B)))) (and (= r1_B r2_B) (not (= r1_A r2_A)) (not (= (f r1_A r1_B) (f r2_A r2_B))))))
(assert (or (and (= r0_A r1_A) (not (= r0_B r1_B)) (not (= (f r0_A r0_B) (f r1_A r1_B)))) (and (= r0_A r2_A) (not (= r0_B r2_B)) (not (= (f r0_A r0_B) (f r2_A r2_B)))) (and (= r1_A r2_A) (not (= r1_B r2_B)) (not (= (f r1_A r1_B) (f r2_A r2_B))))))
(check-sat)
(get-model)
