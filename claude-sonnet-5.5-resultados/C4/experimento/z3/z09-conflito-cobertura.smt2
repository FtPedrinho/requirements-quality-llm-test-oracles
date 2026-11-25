; Conflito textual: cobertura de linhas x desvios sao a mesma metrica (linha 147) x tabela (linha 143).
(set-logic ALL)

(declare-const linhas Real)
(declare-const desvios Real)
; C1: linha 143: linhas 95,5% (1911 de 2001); desvios 90,3% (1170 de 1296)
; C2: linha 147: cobertura de linhas e de desvios sao a mesma metrica [...] sempre o mesmo percentual


(echo "C1 isolada")
(push)
(assert (and (= linhas (/ 1911.0 2001.0)) (= desvios (/ 1170.0 1296.0)))) ; C1
(check-sat)
(pop)

(echo "C2 isolada")
(push)
(assert (= linhas desvios)) ; C2
(check-sat)
(pop)

(echo "C1 e C2")
(push)
(assert (and (= linhas (/ 1911.0 2001.0)) (= desvios (/ 1170.0 1296.0)))) ; C1
(assert (= linhas desvios)) ; C2
(check-sat)
(pop)
