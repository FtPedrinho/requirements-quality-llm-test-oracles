; tabela-verdade de: porta_fechada and not obstaculo
; entradas (átomos distintos): p0 = porta_fechada; p1 = obstaculo
(declare-const p0 Bool)
(declare-const p1 Bool)
(push)(assert (and (= p0 true) (= p1 true) (and p0 (not p1))))(check-sat)(pop)
(push)(assert (and (= p0 true) (= p1 false) (and p0 (not p1))))(check-sat)(pop)
(push)(assert (and (= p0 false) (= p1 true) (and p0 (not p1))))(check-sat)(pop)
(push)(assert (and (= p0 false) (= p1 false) (and p0 (not p1))))(check-sat)(pop)
