(declare-const x Int)
(assert (or (and (>= x 5) (< x 5)) (>= 4 5) (not (>= 5 5)) (and (< x 10) (>= x 9) (not (= x 9))) (not (< 9 10)) (< 10 10)))
(check-sat)
