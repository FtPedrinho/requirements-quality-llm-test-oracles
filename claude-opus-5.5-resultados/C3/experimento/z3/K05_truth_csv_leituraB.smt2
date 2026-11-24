; K5: truth-csv contém a tabela-verdade inteira?
(declare-const tabela_inteira Bool)

(assert (not tabela_inteira))
(check-sat)
