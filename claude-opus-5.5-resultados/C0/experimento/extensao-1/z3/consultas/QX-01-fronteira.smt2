(declare-const x Int)
(assert (or (and (> x 3) (< x 4)) (> 3 3) (not (> 4 3))))
(check-sat)
