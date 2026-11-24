; Q-E16-REQ002-obstaculo: par mascaramento de obstaculo
(declare-const t1_obstaculo Bool)
(declare-const t1_porta_fechada Bool)
(declare-const t2_obstaculo Bool)
(declare-const t2_porta_fechada Bool)
(assert (and (distinct t1_obstaculo t2_obstaculo) (distinct (and t1_porta_fechada (not t1_obstaculo)) (and t2_porta_fechada (not t2_obstaculo))) (distinct (and t1_porta_fechada (not t1_obstaculo)) (and t1_porta_fechada (not (not t1_obstaculo)))) (distinct (and t2_porta_fechada (not t2_obstaculo)) (and t2_porta_fechada (not (not t2_obstaculo))))))
(check-sat)
(get-model)
