; equivalência: (A && B) || C  ==  (A and B) or C
(declare-const p0 Bool)
(declare-const p1 Bool)
(declare-const p2 Bool)
(assert (not (= (or (and p0 p1) p2) (or (and p0 p1) p2))))(check-sat)
