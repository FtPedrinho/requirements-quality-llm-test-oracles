; Caso C3-D37 - guardas-simultaneas
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-datatypes ((Modo 0)) (((idle) (busy) (off))))
(declare-const mode Modo)
(declare-const coin Bool)
(assert (= mode idle))(assert (and (= mode idle) coin))
(check-sat)
(get-model)
