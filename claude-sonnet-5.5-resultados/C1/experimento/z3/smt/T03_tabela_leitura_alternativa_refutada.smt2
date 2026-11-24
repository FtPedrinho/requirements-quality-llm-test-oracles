(set-logic ALL)
(define-fun f ((A Bool) (B Bool) (C Bool)) Bool (and (or A B) C))
(check-sat)
(get-value ((f true true true) (f true true false) (f true false true) (f true false false) (f false true true) (f false true false) (f false false true) (f false false false)))
