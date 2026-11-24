; Caso C3-D09 - linha-101
; Resposta esperada da formula: unsat
(set-logic QF_UF)
(declare-const A Bool)(declare-const B Bool)(declare-const C Bool)
(assert (= A true))(assert (= B false))(assert (= C true))
(assert (or (not A) B))
(check-sat)
