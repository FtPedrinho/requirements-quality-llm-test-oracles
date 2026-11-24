; fronteira de the_voltage > 80 (inteiros): par adjacente (v, v+1) em que a comparação muda
(declare-const v Int)
(assert (not (= (> v 80) (> (+ v 1) 80))))
(assert (not (= v 80)))
(check-sat)
