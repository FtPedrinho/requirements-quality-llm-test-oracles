; fronteira de speed > 100: 101 satisfaz, 100 não, e não há inteiro entre eles
(declare-const s Int)
(assert (not (and (> 101 100) (not (> 100 100)) (forall ((x Int)) (=> (> x 100) (>= x 101))))))
(check-sat)
