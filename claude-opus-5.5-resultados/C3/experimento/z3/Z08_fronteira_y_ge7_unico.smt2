; fronteira de y >= 7 (inteiros): par adjacente (v, v+1) em que a comparação muda
(declare-const v Int)
(assert (not (= (>= v 7) (>= (+ v 1) 7))))
(assert (not (= v 6)))
(check-sat)
