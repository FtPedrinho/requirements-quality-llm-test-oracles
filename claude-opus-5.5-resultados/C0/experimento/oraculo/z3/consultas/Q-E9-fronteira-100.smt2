; nao ha inteiro entre 100 e 101; 100 falso e 101 verdadeiro para speed > 100
(declare-const speed Int)
(assert (or (and (> speed 100) (< speed 101)) (> 100 100) (not (> 101 100))))
(check-sat)
