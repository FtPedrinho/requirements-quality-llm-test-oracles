; CK-01: A and B com T1=(T,T)->T, T2=(F,T)->F, T3=(T,F)->F. Algum esperado diverge da guarda? unsat => não
(define-fun g ((a Bool) (b Bool)) Bool (and a b))
(assert (or (not (= (g true true) true)) (not (= (g false true) false)) (not (= (g true false) false))))
(check-sat)
