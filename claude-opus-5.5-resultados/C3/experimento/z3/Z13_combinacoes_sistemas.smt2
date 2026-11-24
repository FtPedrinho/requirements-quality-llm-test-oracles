; somas da tabela de regressão x contagens calculadas das entradas
(declare-const vm Int)(declare-const tis Int)(declare-const npp Int)
(assert (= vm 152))(assert (= tis 268))(assert (= npp 76))
(push)(assert (not (and (= vm 152) (= tis 268) (= npp 76) (= (+ vm tis npp) 496))))(check-sat)(pop)
