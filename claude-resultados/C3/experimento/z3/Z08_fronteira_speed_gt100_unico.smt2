; fronteira de speed > 100 (inteiros): par adjacente (v, v+1) em que a comparação muda
(declare-const v Int)
(assert (not (= (> v 100) (> (+ v 1) 100))))
(assert (not (= v 100)))
(check-sat)
