; A and not B: C1 declara 3 testes; espera-se k=2 unsat e k=3 sat
; k = 3 linhas
(declare-const A_0 Bool)
(declare-const B_0 Bool)
(declare-const A_1 Bool)
(declare-const B_1 Bool)
(declare-const A_2 Bool)
(declare-const B_2 Bool)
(assert (or (and (= B_0 B_1) (not (= A_0 A_1)) (not (= (and A_0 (not B_0)) (and A_1 (not B_1))))) (and (= B_0 B_2) (not (= A_0 A_2)) (not (= (and A_0 (not B_0)) (and A_2 (not B_2))))) (and (= B_1 B_2) (not (= A_1 A_2)) (not (= (and A_1 (not B_1)) (and A_2 (not B_2)))))))  ; par para A
(assert (or (and (= A_0 A_1) (not (= B_0 B_1)) (not (= (and A_0 (not B_0)) (and A_1 (not B_1))))) (and (= A_0 A_2) (not (= B_0 B_2)) (not (= (and A_0 (not B_0)) (and A_2 (not B_2))))) (and (= A_1 A_2) (not (= B_1 B_2)) (not (= (and A_1 (not B_1)) (and A_2 (not B_2)))))))  ; par para B
(check-sat)
(get-model)
