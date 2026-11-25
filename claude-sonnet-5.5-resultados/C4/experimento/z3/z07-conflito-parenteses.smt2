; Conflito textual: defeitos de parenteses (linhas 407 e 409) e coluna Pegos da tabela (linha 291).
(set-logic ALL)

(declare-const escapam_agrupamento Int)
(declare-const tis_nao_equivalentes Int)
(declare-const tis_pegos Int)
; P1: linha 407: unico tipo de defeito sem garantia MC/DC; nos exemplos, 1 de 727 detectaveis escapou, desse tipo
; P2: linha 409: nenhum defeito de agrupamento pode escapar da suite

(assert (= tis_nao_equivalentes 429))
(assert (= tis_pegos 428))
(assert (= escapam_agrupamento (- tis_nao_equivalentes tis_pegos)))

(echo "P1 isolada (coerente com a tabela: 428 de 429)")
(push)
(assert (= escapam_agrupamento 1)) ; P1
(check-sat)
(pop)

(echo "P2 isolada")
(push)
(assert (= escapam_agrupamento 0)) ; P2
(check-sat)
(pop)

(echo "P1 e P2")
(push)
(assert (= escapam_agrupamento 1)) ; P1
(assert (= escapam_agrupamento 0)) ; P2
(check-sat)
(pop)
