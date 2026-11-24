(declare-const antes Bool)(declare-const agora Bool)
(assert (and (not (= antes false)) (not (= agora true))))
(check-sat)
