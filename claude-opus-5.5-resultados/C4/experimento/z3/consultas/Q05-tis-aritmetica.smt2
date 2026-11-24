; Q05-tis-aritmetica: numeros da tabela de regressao x regra 2^n
(declare-const combinacoes Int)
(declare-const condicoes Int)
(declare-const requisitos Int)
(assert (= combinacoes (+ 4 16 16 16 4 16 16 16 16 8 8 4 16 16 32 32 32)))
(assert (= condicoes (+ 2 6 6 6 2 4 4 4 4 3 3 2 4 4 5 5 5)))
(assert (= requisitos 17))
(push)
(assert (and (= combinacoes 268) (= condicoes 69) (= requisitos 17)))
(check-sat)
(pop)
(push) ; leitura substituta: impossiveis = combinacoes sat; tabela diz 4
(assert (= 264 4))
(check-sat)
(pop)
(push) ; leitura original: impossiveis = combinacoes unsat; tabela diz 4
(assert (= 4 4))
(check-sat)
(pop)
