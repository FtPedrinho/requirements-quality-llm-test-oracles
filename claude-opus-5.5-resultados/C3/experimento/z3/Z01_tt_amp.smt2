; tabela-verdade de: (A && B) || C
; entradas (átomos distintos): p0 = A; p1 = B; p2 = C
(declare-const p0 Bool)
(declare-const p1 Bool)
(declare-const p2 Bool)
(push)(assert (and (= p0 true) (= p1 true) (= p2 true) (or (and p0 p1) p2)))(check-sat)(pop)
(push)(assert (and (= p0 true) (= p1 true) (= p2 false) (or (and p0 p1) p2)))(check-sat)(pop)
(push)(assert (and (= p0 true) (= p1 false) (= p2 true) (or (and p0 p1) p2)))(check-sat)(pop)
(push)(assert (and (= p0 true) (= p1 false) (= p2 false) (or (and p0 p1) p2)))(check-sat)(pop)
(push)(assert (and (= p0 false) (= p1 true) (= p2 true) (or (and p0 p1) p2)))(check-sat)(pop)
(push)(assert (and (= p0 false) (= p1 true) (= p2 false) (or (and p0 p1) p2)))(check-sat)(pop)
(push)(assert (and (= p0 false) (= p1 false) (= p2 true) (or (and p0 p1) p2)))(check-sat)(pop)
(push)(assert (and (= p0 false) (= p1 false) (= p2 false) (or (and p0 p1) p2)))(check-sat)(pop)
