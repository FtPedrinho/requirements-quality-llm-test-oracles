; Caso C3-D11 - combinacao-00
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-datatypes ((Mode 0)) (((idle) (other))))
(declare-const speed Int)(declare-const mode Mode)
(assert (= (> speed 100) false))(assert (= (= mode idle) false))
(check-sat)
(get-model)
