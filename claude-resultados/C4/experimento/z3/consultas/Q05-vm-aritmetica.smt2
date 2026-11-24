; Q05-vm-aritmetica: numeros da tabela de regressao x regra 2^n
(declare-const combinacoes Int)
(declare-const condicoes Int)
(declare-const requisitos Int)
(assert (= combinacoes (+ 8 64 64 8 8)))
(assert (= condicoes (+ 3 6 6 3 3)))
(assert (= requisitos 5))
(push)
(assert (and (= combinacoes 152) (= condicoes 21) (= requisitos 5)))
(check-sat)
(pop)
(push) ; leitura substituta: impossiveis = combinacoes sat; tabela diz 4
(assert (= 148 4))
(check-sat)
(pop)
(push) ; leitura original: impossiveis = combinacoes unsat; tabela diz 4
(assert (= 4 4))
(check-sat)
(pop)
