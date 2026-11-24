; Q03-REQ-003-0: existe par para a entrada freio_acionado ?
(declare-const a0 Bool) ; freio_acionado (linha 1)
(declare-const c0 Bool) ; freio_acionado (linha 2)
(declare-const a1 Bool) ; pedal_pressionado (linha 1)
(declare-const c1 Bool) ; pedal_pressionado (linha 2)
(assert (= a1 c1))
(assert (not (= a0 c0)))
(push) ; leitura A: decisao tambem muda
(assert (not (= (or a0 (and a0 a1)) (or c0 (and c0 c1)))))
(check-sat)
(pop)
(push) ; leitura B: so a mudanca isolada da condicao
(check-sat)
(pop)
