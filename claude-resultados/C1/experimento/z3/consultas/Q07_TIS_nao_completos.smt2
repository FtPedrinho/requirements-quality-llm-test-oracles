; TIS: 69 condições, 17 requisitos, 14 completos, 80 testes. Se todos fossem N+1 dariam 86.
; Existe distribuição em que os 14 completos têm N+1 e os 3 restantes totalizam 80-? Apenas mostra que
; N+1 não vale para os 17 (86 != 80); o texto não define 'completo'.
(assert (not (= (+ 69 17) 80)))
(check-sat)
