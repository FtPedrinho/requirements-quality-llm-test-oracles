; Caso C3-I04 - conjuncao
; Resposta esperada da formula: unsat
(set-logic ALL)
(declare-const modoDireto Bool)
(assert modoDireto)
(assert (not modoDireto))
(check-sat)
