; Caso C3-D03 - comparacoes-sat-e-falsificaveis
; Resposta esperada da formula: sat
(set-logic QF_LIA)
(declare-const x Int)
(push)
(assert (> x 100))
(check-sat)
(pop)
(push)
(assert (not (> x 100)))
(check-sat)
(pop)
