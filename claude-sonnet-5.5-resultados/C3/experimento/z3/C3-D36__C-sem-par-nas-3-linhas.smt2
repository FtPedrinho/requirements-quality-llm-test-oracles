; Caso C3-D36 - C-sem-par-nas-3-linhas
; Resposta esperada da formula: unsat
(set-logic QF_UF)
(define-fun f ((A Bool)(B Bool)(C Bool)) Bool (or (and A B) C))
(assert (or (and (= false true) (= true true) (not (= false false)) (not (= (f false true false) (f true true false)))) (and (= false true) (= true false) (not (= false false)) (not (= (f false true false) (f true false false)))) (and (= true true) (= false true) (not (= false false)) (not (= (f true false false) (f true true false))))))
(check-sat)
