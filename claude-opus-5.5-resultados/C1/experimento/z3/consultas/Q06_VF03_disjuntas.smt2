(declare-datatypes () ((Mode a b c)))
(declare-const mode Mode) (declare-const flag Bool) (declare-const sw Bool)

; VF-03: d1 'flag = true', d2 'flag = false'. Podem valer juntas? unsat => sem conflito
(assert (= flag true)) (assert (= flag false))
(check-sat)
