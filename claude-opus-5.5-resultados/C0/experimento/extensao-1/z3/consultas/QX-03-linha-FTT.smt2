(declare-const x Int)(declare-const b Bool)
(assert (and (not (> x 5)) (< x 3) b))
(check-sat)
