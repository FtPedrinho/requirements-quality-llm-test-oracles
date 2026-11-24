; K7/K8: total de testes VM (26 documentado) depende do critério de par e da minimização
(declare-const n Int)(declare-const ncond Int)(assert (= ncond 21))

(assert (< n 26))
(check-sat)
