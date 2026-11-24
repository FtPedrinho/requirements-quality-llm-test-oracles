(set-logic ALL)
(declare-const A Bool)
(assert (not (or A (not A))))
(check-sat)
