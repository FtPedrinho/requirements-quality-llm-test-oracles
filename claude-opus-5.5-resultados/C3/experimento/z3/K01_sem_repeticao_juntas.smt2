; K1 sem repetição: (A and B) or C tem 3 ocorrências e 3 variáveis
(declare-const ncond Int)(declare-const nocc Int)(declare-const nvar Int)(assert (= nocc 3))(assert (= nvar 3))
(assert (= ncond nocc))
(assert (= ncond nvar))
(check-sat)
