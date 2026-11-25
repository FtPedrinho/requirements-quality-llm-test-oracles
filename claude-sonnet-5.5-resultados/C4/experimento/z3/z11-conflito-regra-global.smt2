; Conflito textual: verificacao por modulo x agregada (linhas 165, 169 e 171).
(set-logic ALL)

(declare-const verificacao_por_modulo Bool)
(declare-const modulo_abaixo_interrompe_build Bool)
; V1: linha 169: a cobertura e conferida pelo JaCoCo separadamente em cada modulo; abaixo da nota minima o build e interrompido
; V2: linha 171: um modulo abaixo da nota minima nunca interrompe o build se a media geral for suficiente

(assert (= modulo_abaixo_interrompe_build verificacao_por_modulo))

(echo "V1 isolada")
(push)
(assert modulo_abaixo_interrompe_build) ; V1
(check-sat)
(pop)

(echo "V2 isolada")
(push)
(assert (not modulo_abaixo_interrompe_build)) ; V2
(check-sat)
(pop)

(echo "V1 e V2")
(push)
(assert modulo_abaixo_interrompe_build) ; V1
(assert (not modulo_abaixo_interrompe_build)) ; V2
(check-sat)
(pop)
