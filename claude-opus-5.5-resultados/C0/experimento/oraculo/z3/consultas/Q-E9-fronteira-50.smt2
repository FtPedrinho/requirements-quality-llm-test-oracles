; nao ha inteiro entre 50 e 51; 50 falso e 51 verdadeiro para speed > 50
(declare-const speed Int)
(assert (or (and (> speed 50) (< speed 51)) (> 50 50) (not (> 51 50))))
(check-sat)
