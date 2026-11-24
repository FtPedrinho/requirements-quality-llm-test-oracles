; K10: --z3 com 13 entradas: passa ao modo direto (1) x permanece na tabela (0)
(declare-const modo Int)

(assert (= modo 0))
(check-sat)
