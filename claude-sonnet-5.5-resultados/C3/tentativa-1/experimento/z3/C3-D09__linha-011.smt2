; Caso C3-D09 - linha-011
; Resposta esperada da formula: sat
(set-logic QF_UF)
(declare-const A Bool)(declare-const B Bool)(declare-const C Bool)
(assert (= A false))(assert (= B true))(assert (= C true))
(assert (or (not A) B))
(check-sat)
