; fronteira inteira de x < 3
(declare-const v Int)
(assert (not (= (< v 3) (< (+ v 1) 3))))
(check-sat)
(get-value (v))
