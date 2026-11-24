; Caso C3-I13 - conjuncao
; Resposta esperada da formula: unsat
(set-logic ALL)
(declare-const linhas Real)(declare-const desvios Real)
(assert (and (= linhas 95.5) (= desvios 90.3)))
(assert (= linhas desvios))
(check-sat)
