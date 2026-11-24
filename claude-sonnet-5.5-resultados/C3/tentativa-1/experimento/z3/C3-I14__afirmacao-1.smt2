; Caso C3-I14 - afirmacao-1
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const pitAlteraCodigo Bool)
(assert pitAlteraCodigo)
(check-sat)
(get-model)
