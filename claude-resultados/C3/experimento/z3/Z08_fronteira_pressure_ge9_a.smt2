; fronteira de the_water_pressure >= 9 (inteiros): par adjacente (v, v+1) em que a comparação muda
(declare-const v Int)
(assert (not (= (>= v 9) (>= (+ v 1) 9))))
(check-sat)
(get-value (v))
