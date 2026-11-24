(declare-const c Bool)(declare-const d Bool)
; contexto c=false; guardas c, d; lacuna = contexto e nenhuma guarda
(assert (and (not c) (not c) (not d)))
(check-sat)
(get-model)
