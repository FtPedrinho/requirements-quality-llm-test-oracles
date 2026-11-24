(declare-const antes Bool)(declare-const agora Bool)
(assert (and (not (= antes false)) (= agora true)))
(check-sat)
