(declare-const c Bool)
(assert (and c (not c)))
(check-sat)
