; Caso C3-D12 - combinacao-11
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-datatypes ((Mode 0)) (((idle) (other))))
(declare-const speed Int)(declare-const mode Mode)
(assert (= (> speed 100) true))(assert (= (= mode idle) true))
(check-sat)
(get-model)
