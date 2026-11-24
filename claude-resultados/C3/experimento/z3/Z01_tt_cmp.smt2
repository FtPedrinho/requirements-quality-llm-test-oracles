; tabela-verdade de: speed > 100 /\ mode = idle
; entradas (átomos distintos): p0 = speed > 100; p1 = mode = idle
(declare-const p0 Bool)
(declare-const p1 Bool)
(push)(assert (and (= p0 true) (= p1 true) (and p0 p1)))(check-sat)(pop)
(push)(assert (and (= p0 true) (= p1 false) (and p0 p1)))(check-sat)(pop)
(push)(assert (and (= p0 false) (= p1 true) (and p0 p1)))(check-sat)(pop)
(push)(assert (and (= p0 false) (= p1 false) (and p0 p1)))(check-sat)(pop)
