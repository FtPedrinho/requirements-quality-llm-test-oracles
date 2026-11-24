; ((E or D) and (not A or D)) or B, causa única POR ENTRADA (aproximação; D se repete). Só evidência auxiliar: o C1 declara 5 testes para --exact (mascaramento por ocorrência).
; k = 4 linhas
(declare-const E_0 Bool)
(declare-const D_0 Bool)
(declare-const A_0 Bool)
(declare-const B_0 Bool)
(declare-const E_1 Bool)
(declare-const D_1 Bool)
(declare-const A_1 Bool)
(declare-const B_1 Bool)
(declare-const E_2 Bool)
(declare-const D_2 Bool)
(declare-const A_2 Bool)
(declare-const B_2 Bool)
(declare-const E_3 Bool)
(declare-const D_3 Bool)
(declare-const A_3 Bool)
(declare-const B_3 Bool)
(assert (or (and (= D_0 D_1) (= A_0 A_1) (= B_0 B_1) (not (= E_0 E_1)) (not (= (or (and (or E_0 D_0) (or (not A_0) D_0)) B_0) (or (and (or E_1 D_1) (or (not A_1) D_1)) B_1)))) (and (= D_0 D_2) (= A_0 A_2) (= B_0 B_2) (not (= E_0 E_2)) (not (= (or (and (or E_0 D_0) (or (not A_0) D_0)) B_0) (or (and (or E_2 D_2) (or (not A_2) D_2)) B_2)))) (and (= D_0 D_3) (= A_0 A_3) (= B_0 B_3) (not (= E_0 E_3)) (not (= (or (and (or E_0 D_0) (or (not A_0) D_0)) B_0) (or (and (or E_3 D_3) (or (not A_3) D_3)) B_3)))) (and (= D_1 D_2) (= A_1 A_2) (= B_1 B_2) (not (= E_1 E_2)) (not (= (or (and (or E_1 D_1) (or (not A_1) D_1)) B_1) (or (and (or E_2 D_2) (or (not A_2) D_2)) B_2)))) (and (= D_1 D_3) (= A_1 A_3) (= B_1 B_3) (not (= E_1 E_3)) (not (= (or (and (or E_1 D_1) (or (not A_1) D_1)) B_1) (or (and (or E_3 D_3) (or (not A_3) D_3)) B_3)))) (and (= D_2 D_3) (= A_2 A_3) (= B_2 B_3) (not (= E_2 E_3)) (not (= (or (and (or E_2 D_2) (or (not A_2) D_2)) B_2) (or (and (or E_3 D_3) (or (not A_3) D_3)) B_3))))))  ; par para E
(assert (or (and (= E_0 E_1) (= A_0 A_1) (= B_0 B_1) (not (= D_0 D_1)) (not (= (or (and (or E_0 D_0) (or (not A_0) D_0)) B_0) (or (and (or E_1 D_1) (or (not A_1) D_1)) B_1)))) (and (= E_0 E_2) (= A_0 A_2) (= B_0 B_2) (not (= D_0 D_2)) (not (= (or (and (or E_0 D_0) (or (not A_0) D_0)) B_0) (or (and (or E_2 D_2) (or (not A_2) D_2)) B_2)))) (and (= E_0 E_3) (= A_0 A_3) (= B_0 B_3) (not (= D_0 D_3)) (not (= (or (and (or E_0 D_0) (or (not A_0) D_0)) B_0) (or (and (or E_3 D_3) (or (not A_3) D_3)) B_3)))) (and (= E_1 E_2) (= A_1 A_2) (= B_1 B_2) (not (= D_1 D_2)) (not (= (or (and (or E_1 D_1) (or (not A_1) D_1)) B_1) (or (and (or E_2 D_2) (or (not A_2) D_2)) B_2)))) (and (= E_1 E_3) (= A_1 A_3) (= B_1 B_3) (not (= D_1 D_3)) (not (= (or (and (or E_1 D_1) (or (not A_1) D_1)) B_1) (or (and (or E_3 D_3) (or (not A_3) D_3)) B_3)))) (and (= E_2 E_3) (= A_2 A_3) (= B_2 B_3) (not (= D_2 D_3)) (not (= (or (and (or E_2 D_2) (or (not A_2) D_2)) B_2) (or (and (or E_3 D_3) (or (not A_3) D_3)) B_3))))))  ; par para D
(assert (or (and (= E_0 E_1) (= D_0 D_1) (= B_0 B_1) (not (= A_0 A_1)) (not (= (or (and (or E_0 D_0) (or (not A_0) D_0)) B_0) (or (and (or E_1 D_1) (or (not A_1) D_1)) B_1)))) (and (= E_0 E_2) (= D_0 D_2) (= B_0 B_2) (not (= A_0 A_2)) (not (= (or (and (or E_0 D_0) (or (not A_0) D_0)) B_0) (or (and (or E_2 D_2) (or (not A_2) D_2)) B_2)))) (and (= E_0 E_3) (= D_0 D_3) (= B_0 B_3) (not (= A_0 A_3)) (not (= (or (and (or E_0 D_0) (or (not A_0) D_0)) B_0) (or (and (or E_3 D_3) (or (not A_3) D_3)) B_3)))) (and (= E_1 E_2) (= D_1 D_2) (= B_1 B_2) (not (= A_1 A_2)) (not (= (or (and (or E_1 D_1) (or (not A_1) D_1)) B_1) (or (and (or E_2 D_2) (or (not A_2) D_2)) B_2)))) (and (= E_1 E_3) (= D_1 D_3) (= B_1 B_3) (not (= A_1 A_3)) (not (= (or (and (or E_1 D_1) (or (not A_1) D_1)) B_1) (or (and (or E_3 D_3) (or (not A_3) D_3)) B_3)))) (and (= E_2 E_3) (= D_2 D_3) (= B_2 B_3) (not (= A_2 A_3)) (not (= (or (and (or E_2 D_2) (or (not A_2) D_2)) B_2) (or (and (or E_3 D_3) (or (not A_3) D_3)) B_3))))))  ; par para A
(assert (or (and (= E_0 E_1) (= D_0 D_1) (= A_0 A_1) (not (= B_0 B_1)) (not (= (or (and (or E_0 D_0) (or (not A_0) D_0)) B_0) (or (and (or E_1 D_1) (or (not A_1) D_1)) B_1)))) (and (= E_0 E_2) (= D_0 D_2) (= A_0 A_2) (not (= B_0 B_2)) (not (= (or (and (or E_0 D_0) (or (not A_0) D_0)) B_0) (or (and (or E_2 D_2) (or (not A_2) D_2)) B_2)))) (and (= E_0 E_3) (= D_0 D_3) (= A_0 A_3) (not (= B_0 B_3)) (not (= (or (and (or E_0 D_0) (or (not A_0) D_0)) B_0) (or (and (or E_3 D_3) (or (not A_3) D_3)) B_3)))) (and (= E_1 E_2) (= D_1 D_2) (= A_1 A_2) (not (= B_1 B_2)) (not (= (or (and (or E_1 D_1) (or (not A_1) D_1)) B_1) (or (and (or E_2 D_2) (or (not A_2) D_2)) B_2)))) (and (= E_1 E_3) (= D_1 D_3) (= A_1 A_3) (not (= B_1 B_3)) (not (= (or (and (or E_1 D_1) (or (not A_1) D_1)) B_1) (or (and (or E_3 D_3) (or (not A_3) D_3)) B_3)))) (and (= E_2 E_3) (= D_2 D_3) (= A_2 A_3) (not (= B_2 B_3)) (not (= (or (and (or E_2 D_2) (or (not A_2) D_2)) B_2) (or (and (or E_3 D_3) (or (not A_3) D_3)) B_3))))))  ; par para B
(check-sat)
(get-model)
