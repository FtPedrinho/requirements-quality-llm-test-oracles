; Q-E10-min-2: existe suite de 2 testes com par mascaramento de cada condicao
(declare-const s0_M Bool)
(declare-const s0_S Bool)
(declare-const s1_M Bool)
(declare-const s1_S Bool)
(assert (or (and (distinct s0_M s1_M) (distinct (and s0_M s0_S) (and s1_M s1_S)) (distinct (and s0_M s0_S) (and (not s0_M) s0_S)) (distinct (and s1_M s1_S) (and (not s1_M) s1_S)))))
(assert (or (and (distinct s0_S s1_S) (distinct (and s0_M s0_S) (and s1_M s1_S)) (distinct (and s0_M s0_S) (and s0_M (not s0_S))) (distinct (and s1_M s1_S) (and s1_M (not s1_S))))))
(check-sat)
