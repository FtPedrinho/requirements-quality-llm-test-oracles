(declare-const A Bool)(declare-const B Bool)(declare-const C Bool)
(assert (and (not A) B C (or (not A) B)))
(check-sat)
