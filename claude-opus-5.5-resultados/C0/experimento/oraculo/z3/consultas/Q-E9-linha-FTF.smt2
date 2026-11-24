(declare-const speed Int)(declare-const rain Bool)
(assert (and (not (> speed 100)) (> speed 50) (not rain)))
(check-sat)
(get-model)
