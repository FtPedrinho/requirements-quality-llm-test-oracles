; Caso C3-I06 - conjuncao
; Resposta esperada da formula: unsat
(set-logic ALL)
(declare-const colunasObrigatorias Bool)
(assert colunasObrigatorias)
(assert (not colunasObrigatorias))
(check-sat)
