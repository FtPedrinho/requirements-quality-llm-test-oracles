; Caso C3-D04 - agrupamento-alternativo-difere
; Resposta esperada da formula: sat
(set-logic QF_UF)
(declare-const A Bool)(declare-const B Bool)(declare-const C Bool)
(assert (not (= (or A (and B C)) (and (or A B) C))))
(check-sat)
(get-model)
