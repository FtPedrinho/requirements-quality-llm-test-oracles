; Caso C3-D41 - sempre-alguma-guarda
; Resposta esperada da formula: unsat
(set-logic ALL)
(declare-datatypes ((Modo 0)) (((idle) (busy) (off))))
(declare-const mode Modo)
(declare-const coin Bool)
(assert (= mode idle))(assert (not (= mode idle)))(assert (not (= mode busy)))
(check-sat)
