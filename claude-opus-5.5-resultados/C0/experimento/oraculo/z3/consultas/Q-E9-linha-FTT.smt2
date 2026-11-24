(declare-const speed Int)(declare-const rain Bool)
(assert (and (not (> speed 100)) (> speed 50) rain))
(check-sat)
(get-model)
