; K5: csv contém a suíte (testes gerados)?
(declare-const tem_suite Bool)

(assert tem_suite)
(assert (not tem_suite))
(check-sat)
