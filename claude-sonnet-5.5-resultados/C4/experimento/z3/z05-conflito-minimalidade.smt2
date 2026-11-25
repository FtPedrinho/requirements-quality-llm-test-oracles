; Conflito textual: guloso x exato (linhas 53, 89 e 91; Z3RandomizedTest).
(set-logic ALL)

(declare-const minimo Int)
(declare-const exato Int)
(declare-const guloso Int)
; G: linha 91: a estrategia gulosa sempre encontra a suite globalmente minima
; X: linha 53: (aqui, 5 testes em vez de 6 da escolha gulosa)
; E: linha 89: com `--exact`, o Z3 procura suite de tamanho minimo
; M: linha 91: --exact [...] pode retornar uma suite maior

(assert (<= minimo exato))
(assert (<= exato guloso))

(echo "G isolada")
(push)
(assert (= guloso minimo)) ; G
(check-sat)
(pop)

(echo "X isolada")
(push)
(assert (and (= exato 5) (= guloso 6))) ; X
(check-sat)
(pop)

(echo "E isolada")
(push)
(assert (= exato minimo)) ; E
(check-sat)
(pop)

(echo "M isolada")
(push)
(assert (> exato minimo)) ; M
(check-sat)
(pop)

(echo "G e X")
(push)
(assert (= guloso minimo)) ; G
(assert (and (= exato 5) (= guloso 6))) ; X
(check-sat)
(pop)

(echo "E e M")
(push)
(assert (= exato minimo)) ; E
(assert (> exato minimo)) ; M
(check-sat)
(pop)

(echo "G, X, E e M")
(push)
(assert (= guloso minimo)) ; G
(assert (and (= exato 5) (= guloso 6))) ; X
(assert (= exato minimo)) ; E
(assert (> exato minimo)) ; M
(check-sat)
(pop)
