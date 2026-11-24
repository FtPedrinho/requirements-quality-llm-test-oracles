; Q-E7-par-B-livre: par mascaramento de B
(declare-const t1_A Bool)
(declare-const t1_B Bool)
(declare-const t2_A Bool)
(declare-const t2_B Bool)
(assert (and (distinct t1_B t2_B) (distinct (and t1_A t1_B) (and t2_A t2_B)) (distinct (and t1_A t1_B) (and t1_A (not t1_B))) (distinct (and t2_A t2_B) (and t2_A (not t2_B)))))
(check-sat)
(get-model)
