; Caso C3-D39 - disjuntas
; Resposta esperada da formula: unsat
(set-logic ALL)
(declare-datatypes ((Modo 0)) (((idle) (busy) (off))))
(declare-const mode Modo)
(declare-const coin Bool)
(assert (= mode idle))(assert (= mode busy))
(check-sat)
