(set-logic ALL)
(declare-const A Bool)(declare-const B Bool)
(assert (not (= (or A (and A B)) A)))
(check-sat)
