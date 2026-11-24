; Caso C3-I02 - conjuncao
; Resposta esperada da formula: unsat
(set-logic ALL)
(declare-const iniciavel Bool)
(assert iniciavel)
(assert (not iniciavel))
(check-sat)
