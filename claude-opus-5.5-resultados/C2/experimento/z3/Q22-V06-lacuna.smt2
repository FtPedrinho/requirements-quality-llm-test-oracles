; consulta Q22-V06-lacuna -- V06: lacuna no contexto
(set-logic ALL)
(declare-datatypes () ((E_mode mode__idle mode__busy)))
(declare-const mode E_mode)
(declare-const s Bool)
(assert (= mode mode__idle))
(assert (not (or (and (= mode mode__idle) (= s true)) (= mode mode__idle))))
(check-sat)
(get-model)
