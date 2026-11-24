; Caso C3-D09 - linha-110
; Resposta esperada da formula: sat
(set-logic QF_UF)
(declare-const A Bool)(declare-const B Bool)(declare-const C Bool)
(assert (= A true))(assert (= B true))(assert (= C false))
(assert (or (not A) B))
(check-sat)
