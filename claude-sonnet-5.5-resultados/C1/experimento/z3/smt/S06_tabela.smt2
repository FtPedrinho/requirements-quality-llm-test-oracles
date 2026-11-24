(set-logic ALL)
(define-fun f ((E Bool) (D Bool) (A Bool) (B Bool)) Bool (or (and (or E D) (or (not A) D)) B))
(check-sat)
(get-value ((f true true true true) (f true true true false) (f true true false true) (f true true false false) (f true false true true) (f true false true false) (f true false false true) (f true false false false) (f false true true true) (f false true true false) (f false true false true) (f false true false false) (f false false true true) (f false false true false) (f false false false true) (f false false false false)))
