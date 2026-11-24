; -2 satisfaz x > -3, -3 não, e todo inteiro > -3 é >= -2: unsat da negação
(assert (not (and (> (- 2) (- 3)) (not (> (- 3) (- 3))) (forall ((x Int)) (=> (> x (- 3)) (>= x (- 2)))))))
(check-sat)
