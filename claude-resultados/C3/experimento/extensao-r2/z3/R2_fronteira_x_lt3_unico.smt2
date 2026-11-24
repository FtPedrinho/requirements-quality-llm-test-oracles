; fronteira inteira de x < 3
(declare-const v Int)
(assert (not (= (< v 3) (< (+ v 1) 3))))
(assert (not (= v 2)))
(check-sat)
