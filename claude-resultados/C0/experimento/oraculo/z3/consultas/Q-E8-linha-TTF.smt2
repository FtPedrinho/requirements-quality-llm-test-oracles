(declare-const A Bool)(declare-const B Bool)(declare-const C Bool)
(assert (and A B (not C) (or (not A) B)))
(check-sat)
