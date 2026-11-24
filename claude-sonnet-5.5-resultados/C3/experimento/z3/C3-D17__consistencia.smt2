; Caso C3-D17 - consistencia
; Resposta esperada da formula: sat
(set-logic QF_LIA)
(declare-const t Int)(declare-const d Int)
(assert (= (+ 152 450 146) 748))(assert (= (+ 0 21 0) 21))(assert (= (+ 152 428 146) 726))(assert (= (- 748 21) 727))
(check-sat)
(get-model)
