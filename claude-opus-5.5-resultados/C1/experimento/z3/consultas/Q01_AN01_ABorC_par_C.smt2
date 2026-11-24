; (A and B) or C; C1: 'todo par de causa única vale em mascaramento'
; condição alvo: C
(declare-const A_1 Bool)
(declare-const B_1 Bool)
(declare-const C_1 Bool)
(declare-const A_2 Bool)
(declare-const B_2 Bool)
(declare-const C_2 Bool)
(assert (= A_1 A_2))
(assert (= B_1 B_2))
(assert (not (= C_1 C_2)))
(assert (not (= (or (and A_1 B_1) C_1) (or (and A_2 B_2) C_2))))
(check-sat)
(get-model)
