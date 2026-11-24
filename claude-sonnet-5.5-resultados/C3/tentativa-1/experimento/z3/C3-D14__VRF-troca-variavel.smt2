; Caso C3-D14 - VRF-troca-variavel
; Resposta esperada da formula: unsat
(set-logic QF_UF)
(define-fun f ((A Bool)(B Bool)(C Bool)) Bool (and A (or B C)))
(define-fun m ((A Bool)(B Bool)(C Bool)) Bool (and A (or B A)))
(assert (not (or (not (= (f true true false) (m true true false))) (not (= (f false true false) (m false true false))) (not (= (f true false false) (m true false false))) (not (= (f true false true) (m true false true))))))
(check-sat)
