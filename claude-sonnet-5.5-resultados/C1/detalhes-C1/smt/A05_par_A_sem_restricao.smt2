(set-logic ALL)
(declare-const x0 Bool)(declare-const x1 Bool)(declare-const y0 Bool)(declare-const y1 Bool)
(assert (= x1 y1))(assert (not (= x0 y0)))(assert (not (= (and x0 x1) (and y0 y1))))
(check-sat)
