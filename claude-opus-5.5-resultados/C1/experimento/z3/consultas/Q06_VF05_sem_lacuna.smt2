(declare-datatypes () ((Mode a b c)))
(declare-const mode Mode) (declare-const flag Bool) (declare-const sw Bool)

; VF-05: arquivo do VF-03 com --context 'mode = a': nenhuma guarda vale? unsat => sem lacuna
(assert (= mode a)) (assert (not (or (= flag true) (= flag false))))
(check-sat)
