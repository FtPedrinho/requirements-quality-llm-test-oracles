(declare-datatypes () ((Mode a b c)))
(declare-const mode Mode) (declare-const flag Bool) (declare-const sw Bool)

; VF-04: arquivo do VF-01 com --context 'flag = false': nenhuma guarda vale? sat => lacuna
(assert (= flag false)) (assert (not (or (= flag true) (= sw true))))
(check-sat) (get-model)
