(declare-const t1_x Int)(declare-const t1_b Bool)
(declare-const t2_x Int)(declare-const t2_b Bool)
(assert (and (distinct (< t1_x 3) (< t2_x 3)) (distinct (or (and (> t1_x 5) (< t1_x 3)) t1_b) (or (and (> t2_x 5) (< t2_x 3)) t2_b)) (distinct (or (and (> t1_x 5) (< t1_x 3)) t1_b) (or (and (> t1_x 5) (not (< t1_x 3))) t1_b)) (distinct (or (and (> t2_x 5) (< t2_x 3)) t2_b) (or (and (> t2_x 5) (not (< t2_x 3))) t2_b))))
(check-sat)
