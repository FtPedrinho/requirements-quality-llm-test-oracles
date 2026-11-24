; Q-E16-REQ002-porta_fechada: par mascaramento de porta_fechada
(declare-const t1_obstaculo Bool)
(declare-const t1_porta_fechada Bool)
(declare-const t2_obstaculo Bool)
(declare-const t2_porta_fechada Bool)
(assert (and (distinct t1_porta_fechada t2_porta_fechada) (distinct (and t1_porta_fechada (not t1_obstaculo)) (and t2_porta_fechada (not t2_obstaculo))) (distinct (and t1_porta_fechada (not t1_obstaculo)) (and (not t1_porta_fechada) (not t1_obstaculo))) (distinct (and t2_porta_fechada (not t2_obstaculo)) (and (not t2_porta_fechada) (not t2_obstaculo)))))
(check-sat)
(get-model)
