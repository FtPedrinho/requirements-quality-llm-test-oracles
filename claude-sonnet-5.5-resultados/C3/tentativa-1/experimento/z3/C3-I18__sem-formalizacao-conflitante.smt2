; Caso C3-I18 - sem-formalizacao-conflitante
; Resposta esperada da formula: sat
(set-logic QF_UF)
(declare-const definido Bool)
(assert (not definido))
(check-sat)
