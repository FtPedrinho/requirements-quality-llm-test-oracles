; Q03-REQ-002-0: existe par para a entrada porta_fechada ?
(declare-const a0 Bool) ; porta_fechada (linha 1)
(declare-const c0 Bool) ; porta_fechada (linha 2)
(declare-const a1 Bool) ; obstaculo (linha 1)
(declare-const c1 Bool) ; obstaculo (linha 2)
(assert (= a1 c1))
(assert (not (= a0 c0)))
(push) ; leitura A: decisao tambem muda
(assert (not (= (and a0 (not a1)) (and c0 (not c1)))))
(check-sat)
(pop)
(push) ; leitura B: so a mudanca isolada da condicao
(check-sat)
(pop)
