; A and not B: C1 declara 3 testes; espera-se k=2 unsat e k=3 sat
; k = 2 linhas
(declare-const A_0 Bool)
(declare-const B_0 Bool)
(declare-const A_1 Bool)
(declare-const B_1 Bool)
(assert (or (and (= B_0 B_1) (not (= A_0 A_1)) (not (= (and A_0 (not B_0)) (and A_1 (not B_1)))))))  ; par para A
(assert (or (and (= A_0 A_1) (not (= B_0 B_1)) (not (= (and A_0 (not B_0)) (and A_1 (not B_1)))))))  ; par para B
(check-sat)
(get-model)
