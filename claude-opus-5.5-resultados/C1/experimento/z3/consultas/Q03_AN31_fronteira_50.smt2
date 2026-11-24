; fronteira de speed > 50: 51 satisfaz, 50 não, e não há inteiro entre eles
(declare-const s Int)
(assert (not (and (> 51 50) (not (> 50 50)) (forall ((x Int)) (=> (> x 50) (>= x 51))))))
(check-sat)
