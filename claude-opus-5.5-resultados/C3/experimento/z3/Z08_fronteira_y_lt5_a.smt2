; fronteira de y < 5 (inteiros): par adjacente (v, v+1) em que a comparação muda
(declare-const v Int)
(assert (not (= (< v 5) (< (+ v 1) 5))))
(check-sat)
(get-value (v))
