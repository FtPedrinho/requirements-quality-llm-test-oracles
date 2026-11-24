(declare-const x Int)(declare-const b Bool)
(assert (and (> x 5) (not (< x 3)) b))
(check-sat)
