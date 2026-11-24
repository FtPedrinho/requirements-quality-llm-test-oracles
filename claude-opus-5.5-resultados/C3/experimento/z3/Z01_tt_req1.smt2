; tabela-verdade de: (alarme_ativo and porta_aberta) or botao_emergencia
; entradas (átomos distintos): p0 = alarme_ativo; p1 = porta_aberta; p2 = botao_emergencia
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
