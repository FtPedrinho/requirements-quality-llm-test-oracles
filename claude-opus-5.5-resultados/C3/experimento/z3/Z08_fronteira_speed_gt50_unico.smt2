; fronteira de speed > 50 (inteiros): par adjacente (v, v+1) em que a comparação muda
(declare-const v Int)
(assert (not (= (> v 50) (> (+ v 1) 50))))
(assert (not (= v 50)))
(check-sat)
