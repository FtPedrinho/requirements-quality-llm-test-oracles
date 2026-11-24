; tabela-verdade de: freio_acionado or (freio_acionado and pedal_pressionado)
; entradas (átomos distintos): p0 = freio_acionado; p1 = pedal_pressionado
(declare-const p0 Bool)
(declare-const p1 Bool)
(push)(assert (and (= p0 true) (= p1 true) (or p0 (and p0 p1))))(check-sat)(pop)
(push)(assert (and (= p0 true) (= p1 false) (or p0 (and p0 p1))))(check-sat)(pop)
(push)(assert (and (= p0 false) (= p1 true) (or p0 (and p0 p1))))(check-sat)(pop)
(push)(assert (and (= p0 false) (= p1 false) (or p0 (and p0 p1))))(check-sat)(pop)
