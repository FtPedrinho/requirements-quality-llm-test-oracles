; K7: B em A or (A and B) tem par? (estrito: unsat no Z04; simplificado: sat)
(declare-const tem_par Bool)

(assert (not tem_par))
(assert tem_par)
(check-sat)
