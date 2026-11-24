; K6: número de combinações mantidas de speed>100 or (speed>50 and rain)
(declare-const mantidas Int)

(assert (= mantidas 6))
(assert (= mantidas 2))
(check-sat)
