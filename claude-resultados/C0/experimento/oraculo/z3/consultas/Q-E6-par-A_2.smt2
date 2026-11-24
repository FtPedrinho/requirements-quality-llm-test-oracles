; Q-E6-par-A_2: par mascaramento de A#2
(declare-const t1_A Bool)
(declare-const t1_B Bool)
(declare-const t2_A Bool)
(declare-const t2_B Bool)
(assert (and (distinct t1_A t2_A) (distinct (or t1_A (and t1_A t1_B)) (or t2_A (and t2_A t2_B))) (distinct (or t1_A (and t1_A t1_B)) (or t1_A (and (not t1_A) t1_B))) (distinct (or t2_A (and t2_A t2_B)) (or t2_A (and (not t2_A) t2_B)))))
(check-sat)
