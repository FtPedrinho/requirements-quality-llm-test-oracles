; Q05-npp-aritmetica: numeros da tabela de regressao x regra 2^n
(declare-const combinacoes Int)
(declare-const condicoes Int)
(declare-const requisitos Int)
(assert (= combinacoes (+ 8 8 8 8 16 8 4 4 4 4 4)))
(assert (= condicoes (+ 3 3 3 3 4 3 2 2 2 2 2)))
(assert (= requisitos 11))
(push)
(assert (and (= combinacoes 76) (= condicoes 29) (= requisitos 11)))
(check-sat)
(pop)
(push) ; leitura substituta: impossiveis = combinacoes sat; tabela diz 1
(assert (= 75 1))
(check-sat)
(pop)
(push) ; leitura original: impossiveis = combinacoes unsat; tabela diz 1
(assert (= 1 1))
(check-sat)
(pop)
