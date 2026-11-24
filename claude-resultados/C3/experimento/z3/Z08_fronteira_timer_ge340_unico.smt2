; fronteira de the_flashing_timer >= 340 (inteiros): par adjacente (v, v+1) em que a comparação muda
(declare-const v Int)
(assert (not (= (>= v 340) (>= (+ v 1) 340))))
(assert (not (= v 339)))
(check-sat)
