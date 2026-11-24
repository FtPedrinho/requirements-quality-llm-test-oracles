; Tabela 'Números travados pela regressão' do C1. Consistência interna: totais, N+1, mutantes.
(declare-const vR Int) (declare-const tR Int) (declare-const nR Int)
(assert (and (= vR 5) (= tR 17) (= nR 11)))
(define-fun ok () Bool (and
  (= (+ 5 17 11) 33) (= (+ 5 14 11) 30) (= (+ 21 69 29) 119) (= (+ 152 268 76) 496)
  (= (+ 4 4 1) 9) (= (+ 26 80 40) 146) (= (+ 152 450 146) 748) (= (+ 0 21 0) 21)
  (= (+ 152 428 146) 726) (= (+ 0 3 1) 4)
  ; VM e NPP: todos completos => testes = condições + requisitos
  (= (+ 21 5) 26) (= (+ 29 11) 40)
  ; detectáveis = mutantes - equivalentes; 727 detectáveis e 1 escapou (Limites conhecidos)
  (= (- 748 21) 727) (= (- 727 726) 1)
  ; VM: combinações = soma de 2^condições (3,6,6,3,3) do arquivo de entrada
  (= (+ 8 64 64 8 8) 152)
  ; VM: testes = soma (condições+1) = 4+7+7+4+4
  (= (+ 4 7 7 4 4) 26)))
(assert (not ok))
(check-sat)
