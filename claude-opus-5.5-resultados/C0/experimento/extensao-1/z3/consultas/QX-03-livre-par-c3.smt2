(declare-const t1_x1 Bool)(declare-const t1_x2 Bool)(declare-const t1_b Bool)
(declare-const t2_x1 Bool)(declare-const t2_x2 Bool)(declare-const t2_b Bool)
(assert (and (distinct t1_b t2_b) (distinct (or (and t1_x1 t1_x2) t1_b) (or (and t2_x1 t2_x2) t2_b)) (distinct (or (and t1_x1 t1_x2) t1_b) (or (and t1_x1 t1_x2) (not t1_b))) (distinct (or (and t2_x1 t2_x2) t2_b) (or (and t2_x1 t2_x2) (not t2_b)))))
(check-sat)
