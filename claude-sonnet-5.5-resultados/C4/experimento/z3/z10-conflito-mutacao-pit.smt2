; Conflito textual: o que a nota de mutacao mede (linhas 149 e 151).
(set-logic ALL)

(declare-const mede_deteccao_de_defeitos Bool)
; M1: linha 149: mede se os testes revelam determinados defeitos, alem de medir se o codigo foi executado
; M2: linha 151: a nota de mutacao mede exclusivamente cobertura de linhas e nao tem relacao com deteccao de defeitos


(echo "M1 isolada")
(push)
(assert mede_deteccao_de_defeitos) ; M1
(check-sat)
(pop)

(echo "M2 isolada")
(push)
(assert (not mede_deteccao_de_defeitos)) ; M2
(check-sat)
(pop)

(echo "M1 e M2")
(push)
(assert mede_deteccao_de_defeitos) ; M1
(assert (not mede_deteccao_de_defeitos)) ; M2
(check-sat)
(pop)
