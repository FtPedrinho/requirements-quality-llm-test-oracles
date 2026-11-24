(declare-const s Int)
(assert (> s 100))
(assert (not (> s 50)))
(check-sat)
