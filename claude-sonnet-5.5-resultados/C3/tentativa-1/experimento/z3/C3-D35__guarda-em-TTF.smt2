; Caso C3-D35 - guarda-em-TTF
; Resposta esperada da formula: unsat
(set-logic QF_UF)
(assert (not (or (and true true) false)))
(check-sat)
