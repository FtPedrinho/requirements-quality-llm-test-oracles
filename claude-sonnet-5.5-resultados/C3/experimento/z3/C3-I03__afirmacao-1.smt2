; Caso C3-I03 - afirmacao-1
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const cod0Significa Int)
(assert (= cod0Significa 0))
(check-sat)
(get-model)
