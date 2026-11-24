; Caso C3-I14 - afirmacao-2
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const pitAlteraCodigo Bool)
(assert (not pitAlteraCodigo))
(check-sat)
(get-model)
