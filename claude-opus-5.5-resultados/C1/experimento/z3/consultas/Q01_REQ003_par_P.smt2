; REQ-003 freio or (freio and pedal): pedal sem efeito (unsat) => redundante
; condição alvo: P
(declare-const F_1 Bool)
(declare-const P_1 Bool)
(declare-const F_2 Bool)
(declare-const P_2 Bool)
(assert (= F_1 F_2))
(assert (not (= P_1 P_2)))
(assert (not (= (or F_1 (and F_1 P_1)) (or F_2 (and F_2 P_2)))))
(check-sat)
(get-model)
