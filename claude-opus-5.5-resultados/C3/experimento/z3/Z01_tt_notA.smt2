; tabela-verdade de: not A and B
; entradas (átomos distintos): p0 = A; p1 = B
(declare-const p0 Bool)
(declare-const p1 Bool)
(push)(assert (and (= p0 true) (= p1 true) (and (not p0) p1)))(check-sat)(pop)
(push)(assert (and (= p0 true) (= p1 false) (and (not p0) p1)))(check-sat)(pop)
(push)(assert (and (= p0 false) (= p1 true) (and (not p0) p1)))(check-sat)(pop)
(push)(assert (and (= p0 false) (= p1 false) (and (not p0) p1)))(check-sat)(pop)
