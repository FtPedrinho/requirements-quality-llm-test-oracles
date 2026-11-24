; Caso C3-I11 - conjuncao
; Resposta esperada da formula: unsat
(set-logic ALL)
(declare-const semParEmTodoCenarioERedundante Bool)
(assert semParEmTodoCenarioERedundante)
(assert (not semParEmTodoCenarioERedundante))
(check-sat)
