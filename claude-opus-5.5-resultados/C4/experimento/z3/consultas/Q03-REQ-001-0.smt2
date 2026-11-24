; Q03-REQ-001-0: existe par para a entrada alarme_ativo ?
(declare-const a0 Bool) ; alarme_ativo (linha 1)
(declare-const c0 Bool) ; alarme_ativo (linha 2)
(declare-const a1 Bool) ; porta_aberta (linha 1)
(declare-const c1 Bool) ; porta_aberta (linha 2)
(declare-const a2 Bool) ; botao_emergencia (linha 1)
(declare-const c2 Bool) ; botao_emergencia (linha 2)
(assert (= a1 c1))
(assert (= a2 c2))
(assert (not (= a0 c0)))
(push) ; leitura A: decisao tambem muda
(assert (not (= (or (and a0 a1) a2) (or (and c0 c1) c2))))
(check-sat)
(pop)
(push) ; leitura B: so a mudanca isolada da condicao
(check-sat)
(pop)
