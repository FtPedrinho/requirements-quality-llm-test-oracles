; K3: código de saída (conflito_verify) – Uso x Interpretação definitiva
(declare-const c Int)

(assert (= c 2))
(assert (not (= c 2)))
(check-sat)
