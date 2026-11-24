; K1: (A and B) or (not A and C): condições por ocorrência (4) x por variável (3)
(declare-const ncond Int)

(assert (= ncond 4))
(assert (= ncond 3))
(check-sat)
