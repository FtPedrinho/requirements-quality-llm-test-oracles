(declare-const x Int)(declare-const z Int)
(assert (and (>= x 5) (< x 10) (not (= z 3))))
(check-sat)
