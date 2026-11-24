(declare-const c Bool)(declare-const d Bool)
; R1: c -> m:=choice ; R2: d -> m:=weak ; valores diferentes
(assert (and c d (distinct 1 2)))
(check-sat)
(get-model)
