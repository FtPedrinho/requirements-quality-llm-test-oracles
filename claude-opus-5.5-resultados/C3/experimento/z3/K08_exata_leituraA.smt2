; K8: exata (5) x gulosa (6) e 'gulosa sempre mínima'
(declare-const g Int)(declare-const e Int)(declare-const m Int)(assert (<= m g))(assert (<= m e))

(assert (and (= e m) (= e 5) (= g 6)))
(check-sat)
