; Caso C3-D40 - nenhuma-guarda-vale
; Resposta esperada da formula: sat
(set-logic ALL)
(declare-datatypes ((Modo 0)) (((idle) (busy) (off))))
(declare-const mode Modo)
(declare-const coin Bool)
(assert (= mode off))(assert (not (= mode idle)))(assert (not (= mode busy)))
(check-sat)
(get-model)
