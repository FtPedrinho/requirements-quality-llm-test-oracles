(declare-const antes Bool)(declare-const agora Bool)
(assert (and (= antes false) (= agora true)))
(check-sat)
