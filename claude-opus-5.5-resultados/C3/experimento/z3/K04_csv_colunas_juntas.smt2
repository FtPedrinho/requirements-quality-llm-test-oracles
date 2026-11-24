; K4: CSV de check sem decision/expected_outcome é aceito?
(declare-const aceito Bool)

(assert aceito)
(assert (not aceito))
(check-sat)
