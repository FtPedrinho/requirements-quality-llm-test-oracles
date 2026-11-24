; (A and B) or C: C1 declara 4 testes; espera-se k=3 unsat e k=4 sat
; k = 4 linhas
(declare-const A_0 Bool)
(declare-const B_0 Bool)
(declare-const C_0 Bool)
(declare-const A_1 Bool)
(declare-const B_1 Bool)
(declare-const C_1 Bool)
(declare-const A_2 Bool)
(declare-const B_2 Bool)
(declare-const C_2 Bool)
(declare-const A_3 Bool)
(declare-const B_3 Bool)
(declare-const C_3 Bool)
(assert (or (and (= B_0 B_1) (= C_0 C_1) (not (= A_0 A_1)) (not (= (or (and A_0 B_0) C_0) (or (and A_1 B_1) C_1)))) (and (= B_0 B_2) (= C_0 C_2) (not (= A_0 A_2)) (not (= (or (and A_0 B_0) C_0) (or (and A_2 B_2) C_2)))) (and (= B_0 B_3) (= C_0 C_3) (not (= A_0 A_3)) (not (= (or (and A_0 B_0) C_0) (or (and A_3 B_3) C_3)))) (and (= B_1 B_2) (= C_1 C_2) (not (= A_1 A_2)) (not (= (or (and A_1 B_1) C_1) (or (and A_2 B_2) C_2)))) (and (= B_1 B_3) (= C_1 C_3) (not (= A_1 A_3)) (not (= (or (and A_1 B_1) C_1) (or (and A_3 B_3) C_3)))) (and (= B_2 B_3) (= C_2 C_3) (not (= A_2 A_3)) (not (= (or (and A_2 B_2) C_2) (or (and A_3 B_3) C_3))))))  ; par para A
(assert (or (and (= A_0 A_1) (= C_0 C_1) (not (= B_0 B_1)) (not (= (or (and A_0 B_0) C_0) (or (and A_1 B_1) C_1)))) (and (= A_0 A_2) (= C_0 C_2) (not (= B_0 B_2)) (not (= (or (and A_0 B_0) C_0) (or (and A_2 B_2) C_2)))) (and (= A_0 A_3) (= C_0 C_3) (not (= B_0 B_3)) (not (= (or (and A_0 B_0) C_0) (or (and A_3 B_3) C_3)))) (and (= A_1 A_2) (= C_1 C_2) (not (= B_1 B_2)) (not (= (or (and A_1 B_1) C_1) (or (and A_2 B_2) C_2)))) (and (= A_1 A_3) (= C_1 C_3) (not (= B_1 B_3)) (not (= (or (and A_1 B_1) C_1) (or (and A_3 B_3) C_3)))) (and (= A_2 A_3) (= C_2 C_3) (not (= B_2 B_3)) (not (= (or (and A_2 B_2) C_2) (or (and A_3 B_3) C_3))))))  ; par para B
(assert (or (and (= A_0 A_1) (= B_0 B_1) (not (= C_0 C_1)) (not (= (or (and A_0 B_0) C_0) (or (and A_1 B_1) C_1)))) (and (= A_0 A_2) (= B_0 B_2) (not (= C_0 C_2)) (not (= (or (and A_0 B_0) C_0) (or (and A_2 B_2) C_2)))) (and (= A_0 A_3) (= B_0 B_3) (not (= C_0 C_3)) (not (= (or (and A_0 B_0) C_0) (or (and A_3 B_3) C_3)))) (and (= A_1 A_2) (= B_1 B_2) (not (= C_1 C_2)) (not (= (or (and A_1 B_1) C_1) (or (and A_2 B_2) C_2)))) (and (= A_1 A_3) (= B_1 B_3) (not (= C_1 C_3)) (not (= (or (and A_1 B_1) C_1) (or (and A_3 B_3) C_3)))) (and (= A_2 A_3) (= B_2 B_3) (not (= C_2 C_3)) (not (= (or (and A_2 B_2) C_2) (or (and A_3 B_3) C_3))))))  ; par para C
(check-sat)
(get-model)
