; Caso C3-I11 - afirmacao-1
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-const semParEmTodoCenarioERedundante Bool)
(assert semParEmTodoCenarioERedundante)
(check-sat)
(get-model)
