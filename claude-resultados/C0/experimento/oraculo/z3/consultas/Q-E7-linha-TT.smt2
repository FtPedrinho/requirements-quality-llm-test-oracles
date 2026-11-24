(declare-const A Bool)(declare-const B Bool)(assert (and A B (or (not A) (not B))))(check-sat)
