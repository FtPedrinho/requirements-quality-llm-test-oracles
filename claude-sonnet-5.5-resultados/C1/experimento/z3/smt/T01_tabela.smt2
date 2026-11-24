(set-logic ALL)
(define-fun f ((A Bool) (B Bool)) Bool (and A B))
(check-sat)
(get-value ((f true true) (f true false) (f false true) (f false false)))
