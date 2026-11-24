(declare-const speed Int)(declare-const rain Bool)
(assert (and (> speed 100) (not (> speed 50)) (not rain)))
(check-sat)
