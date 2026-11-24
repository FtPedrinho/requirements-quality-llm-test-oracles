; guarda de tipada.json nos testes de tipada.csv
(declare-datatypes () ((M a b c)))
(declare-const x Int)(declare-const r Real)(declare-const m M)(declare-const k Bool)
(push)(assert (and (= x 0) (= r 9) (= m b) (= k false) (or (or (and (< x 3) (>= x (- 2))) (and (<= r 1.5) (not (= m b)))) (= k true))))(check-sat)(pop) ; U1
(push)(assert (and (= x 5) (= r 9) (= m b) (= k false) (or (or (and (< x 3) (>= x (- 2))) (and (<= r 1.5) (not (= m b)))) (= k true))))(check-sat)(pop) ; U2
(push)(assert (and (= x (- 3)) (= r 1.5) (= m a) (= k false) (or (or (and (< x 3) (>= x (- 2))) (and (<= r 1.5) (not (= m b)))) (= k true))))(check-sat)(pop) ; U3
(push)(assert (and (= x (- 3)) (= r 1.5) (= m b) (= k false) (or (or (and (< x 3) (>= x (- 2))) (and (<= r 1.5) (not (= m b)))) (= k true))))(check-sat)(pop) ; U4
(push)(assert (and (= x 7) (= r 2) (= m c) (= k true) (or (or (and (< x 3) (>= x (- 2))) (and (<= r 1.5) (not (= m b)))) (= k true))))(check-sat)(pop) ; U5
