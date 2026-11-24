; equivalência: !A and B  ==  not A and B
(declare-const p0 Bool)
(declare-const p1 Bool)
(assert (not (= (and (not p0) p1) (and (not p0) p1))))(check-sat)
