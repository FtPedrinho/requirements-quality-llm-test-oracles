; Caso C3-I06 - afirmacao-2
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const colunasObrigatorias Bool)
(assert (not colunasObrigatorias))
(check-sat)
(get-model)
