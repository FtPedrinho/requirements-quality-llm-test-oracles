(declare-const t1_x Int)(declare-const t1_z Int)
(declare-const t2_x Int)(declare-const t2_z Int)
(assert (and (distinct (>= t1_x 5) (>= t2_x 5)) (distinct (or (and (>= t1_x 5) (< t1_x 10)) (= t1_z 3)) (or (and (>= t2_x 5) (< t2_x 10)) (= t2_z 3))) (distinct (or (and (>= t1_x 5) (< t1_x 10)) (= t1_z 3)) (or (and (not (>= t1_x 5)) (< t1_x 10)) (= t1_z 3))) (distinct (or (and (>= t2_x 5) (< t2_x 10)) (= t2_z 3)) (or (and (not (>= t2_x 5)) (< t2_x 10)) (= t2_z 3)))))
(check-sat)
