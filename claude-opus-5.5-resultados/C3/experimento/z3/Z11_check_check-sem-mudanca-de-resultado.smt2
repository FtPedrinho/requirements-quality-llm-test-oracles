; resultado da guarda (A and B) or C para cada teste de check-sem-mudanca-de-resultado.csv
(declare-const A Bool)(declare-const B Bool)(declare-const C Bool)
(push)(assert (and (= A true) (= B false) (= C true) (or (and A B) C)))(check-sat)(pop)
(push)(assert (and (= A false) (= B false) (= C true) (or (and A B) C)))(check-sat)(pop)
