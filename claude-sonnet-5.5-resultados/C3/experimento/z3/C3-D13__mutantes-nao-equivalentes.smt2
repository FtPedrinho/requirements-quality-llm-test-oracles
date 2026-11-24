; Caso C3-D13 - mutantes-nao-equivalentes
; Resposta esperada da formula: sat
(set-logic QF_UF)
(declare-const A Bool)(declare-const B Bool)(declare-const C Bool)
(assert (not (= (and A (or B C)) (and A (and B C)))))
(check-sat)
(get-model)
