(declare-const c Bool)(declare-const d Bool)
; contexto d=true; guardas c, not c
(assert (and d (not c) (not (not c))))
(check-sat)
