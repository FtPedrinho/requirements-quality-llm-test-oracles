; Caso C3-D43 - 2-elevado-20
; Resposta esperada da formula: sat
(set-logic QF_LIA)
(declare-const c Int)
(assert (= c 1048576))(assert (= c (* 1024 1024)))
(check-sat)
