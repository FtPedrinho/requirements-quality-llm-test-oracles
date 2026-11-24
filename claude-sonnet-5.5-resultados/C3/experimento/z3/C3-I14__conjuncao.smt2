; Caso C3-I14 - conjuncao
; Resposta esperada da formula: unsat
(set-logic ALL)
(declare-const pitAlteraCodigo Bool)
(assert pitAlteraCodigo)
(assert (not pitAlteraCodigo))
(check-sat)
