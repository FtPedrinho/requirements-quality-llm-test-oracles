; I07: exemplo speed > 100 or (speed > 50 and rain).
; I12: o tratamento de sat/unsat é registrado separadamente, em casos.json.
(set-logic QF_LIA)
(declare-const speed Int)
(declare-const rain Bool)
(declare-const p Bool)
(declare-const q Bool)
(assert (= p (> speed 100)))
(assert (= q (> speed 50)))
