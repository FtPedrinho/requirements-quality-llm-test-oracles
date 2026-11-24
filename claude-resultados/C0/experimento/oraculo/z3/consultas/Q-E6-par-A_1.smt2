; Q-E6-par-A_1: par mascaramento de A#1
(declare-const t1_A Bool)
(declare-const t1_B Bool)
(declare-const t2_A Bool)
(declare-const t2_B Bool)
(assert (and (distinct t1_A t2_A) (distinct (or t1_A (and t1_A t1_B)) (or t2_A (and t2_A t2_B))) (distinct (or t1_A (and t1_A t1_B)) (or (not t1_A) (and t1_A t1_B))) (distinct (or t2_A (and t2_A t2_B)) (or (not t2_A) (and t2_A t2_B)))))
(check-sat)
(get-model)
