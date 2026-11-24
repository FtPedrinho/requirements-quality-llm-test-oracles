(declare-datatypes () ((Mode idle choice)))
(declare-const x Int)(declare-const y Int)(declare-const mode Mode)
(assert (and (> x 3) (<= y x) (not (= mode idle))))
(check-sat)
