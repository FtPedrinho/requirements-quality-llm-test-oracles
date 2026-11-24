; speed > 100 /\ mode = idle, sem Z3: S=speed>100, M=mode=idle tratadas como condições
; condição alvo: S
(declare-const S_1 Bool)
(declare-const M_1 Bool)
(declare-const S_2 Bool)
(declare-const M_2 Bool)
(assert (= M_1 M_2))
(assert (not (= S_1 S_2)))
(assert (not (= (and S_1 M_1) (and S_2 M_2))))
(check-sat)
(get-model)
