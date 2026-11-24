; Q-E2-min-2: existe suite de 2 testes com par mascaramento de cada condicao
(declare-const s0_A Bool)
(declare-const s0_B Bool)
(declare-const s1_A Bool)
(declare-const s1_B Bool)
(assert (or (and (distinct s0_A s1_A) (distinct (and s0_A (not s0_B)) (and s1_A (not s1_B))) (distinct (and s0_A (not s0_B)) (and (not s0_A) (not s0_B))) (distinct (and s1_A (not s1_B)) (and (not s1_A) (not s1_B))))))
(assert (or (and (distinct s0_B s1_B) (distinct (and s0_A (not s0_B)) (and s1_A (not s1_B))) (distinct (and s0_A (not s0_B)) (and s0_A (not (not s0_B)))) (distinct (and s1_A (not s1_B)) (and s1_A (not (not s1_B)))))))
(check-sat)
