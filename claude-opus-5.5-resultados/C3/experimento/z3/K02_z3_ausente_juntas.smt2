; K2/K11: sem z3 no PATH, analyze simples roda?
(declare-const roda Bool)

(assert roda)
(assert (not roda))
(check-sat)
