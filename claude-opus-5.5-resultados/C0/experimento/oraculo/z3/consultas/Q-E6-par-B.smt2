; Q-E6-par-B: par mascaramento de B
(declare-const t1_A Bool)
(declare-const t1_B Bool)
(declare-const t2_A Bool)
(declare-const t2_B Bool)
(assert (and (distinct t1_B t2_B) (distinct (or t1_A (and t1_A t1_B)) (or t2_A (and t2_A t2_B))) (distinct (or t1_A (and t1_A t1_B)) (or t1_A (and t1_A (not t1_B)))) (distinct (or t2_A (and t2_A t2_B)) (or t2_A (and t2_A (not t2_B))))))
(check-sat)
