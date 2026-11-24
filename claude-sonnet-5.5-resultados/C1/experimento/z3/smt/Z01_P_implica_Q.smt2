(set-logic ALL)
(declare-const x Int)
(assert (and (> x 100) (not (> x 50))))
(check-sat)
