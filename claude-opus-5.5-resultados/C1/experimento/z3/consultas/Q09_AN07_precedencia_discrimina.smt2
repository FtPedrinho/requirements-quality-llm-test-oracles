; A or (B and C) difere de (A or B) and C? sat => o teste de precedência discrimina
(declare-const A Bool) (declare-const B Bool) (declare-const C Bool)
(assert (not (= (or A (and B C)) (and (or A B) C))))
(check-sat) (get-model)
