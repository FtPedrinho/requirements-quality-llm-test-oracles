; consulta Q22-V07-lacuna -- V07: lacuna no contexto
(set-logic ALL)
(declare-datatypes () ((E_mode mode__idle mode__busy)))
(declare-const mode E_mode)
(declare-const s Bool)
(assert (= mode mode__idle))
(assert (not (or (and (= mode mode__idle) (= s true)) (and (= mode mode__idle) (= s false)))))
(check-sat)
(get-model)
