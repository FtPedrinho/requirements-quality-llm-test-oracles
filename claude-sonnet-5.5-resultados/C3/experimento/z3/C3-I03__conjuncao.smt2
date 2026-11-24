; Caso C3-I03 - conjuncao
; Resposta esperada da formula: unsat
(set-logic ALL)
(declare-const cod0Significa Int)
(assert (= cod0Significa 0))
(assert (= cod0Significa 1))
(check-sat)
