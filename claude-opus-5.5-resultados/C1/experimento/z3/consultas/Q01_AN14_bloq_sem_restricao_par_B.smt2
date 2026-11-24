; A and B sem restrição: A tem par (sat) => falta de par vem da restrição => bloqueada
; condição alvo: B
(declare-const A_1 Bool)
(declare-const B_1 Bool)
(declare-const A_2 Bool)
(declare-const B_2 Bool)
(assert (= A_1 A_2))
(assert (not (= B_1 B_2)))
(assert (not (= (and A_1 B_1) (and A_2 B_2))))
(check-sat)
(get-model)
