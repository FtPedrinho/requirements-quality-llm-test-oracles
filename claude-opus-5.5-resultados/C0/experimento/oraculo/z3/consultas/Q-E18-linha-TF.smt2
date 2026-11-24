(declare-const antes Bool)(declare-const agora Bool)
(assert (and (= antes false) (not (= agora true))))
(check-sat)
