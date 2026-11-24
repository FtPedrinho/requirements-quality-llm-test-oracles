; fronteira de the_water_pressure < 10 (inteiros): par adjacente (v, v+1) em que a comparação muda
(declare-const v Int)
(assert (not (= (< v 10) (< (+ v 1) 10))))
(assert (not (= v 9)))
(check-sat)
