; Caso C3-I03 - afirmacao-2
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const cod0Significa Int)
(assert (= cod0Significa 1))
(check-sat)
(get-model)
