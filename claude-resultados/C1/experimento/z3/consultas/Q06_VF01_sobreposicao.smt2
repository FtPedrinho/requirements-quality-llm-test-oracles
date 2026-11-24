(declare-datatypes () ((Mode a b c)))
(declare-const mode Mode) (declare-const flag Bool) (declare-const sw Bool)

; VF-01: d1 'flag = true' escreve mode := a; d2 'sw = true' escreve mode := b. Podem valer juntas? sat => conflito
(assert (= flag true)) (assert (= sw true))
(check-sat) (get-model)
