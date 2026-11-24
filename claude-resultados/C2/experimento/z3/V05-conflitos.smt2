; consulta V05-conflitos -- sobreposição de guardas com ações de valores diferentes
(set-logic ALL)
(declare-const x Int)
(declare-const s Bool)
(push)
(assert (> x 5))
(assert (and (> x 3) (= s true)))
(check-sat)
(pop)
