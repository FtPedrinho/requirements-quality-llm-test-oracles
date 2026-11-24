; speed > 100 or (speed > 50 and rain): A=speed>100, B=speed>50, R=rain; speed inteiro
(declare-const speed Int) (declare-const rain Bool)
(assert (= (> speed 100) true))
(assert (= (> speed 50) true))
(assert (= rain true))
(check-sat)
(get-model)
