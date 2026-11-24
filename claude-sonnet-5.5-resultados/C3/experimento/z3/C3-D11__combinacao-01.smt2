; Caso C3-D11 - combinacao-01
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-datatypes ((Mode 0)) (((idle) (other))))
(declare-const speed Int)(declare-const mode Mode)
(assert (= (> speed 100) false))(assert (= (= mode idle) true))
(check-sat)
(get-model)
