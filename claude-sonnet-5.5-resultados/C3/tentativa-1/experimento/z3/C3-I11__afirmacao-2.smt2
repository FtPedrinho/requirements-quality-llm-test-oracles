; Caso C3-I11 - afirmacao-2
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const semParEmTodoCenarioERedundante Bool)
(assert (not semParEmTodoCenarioERedundante))
(check-sat)
(get-model)
