; Conflito textual: Z3 como processo externo x biblioteca na JVM; timeout (linhas 119, 121, 123).
(set-logic ALL)

(declare-const z3_processo_externo Bool)
(declare-const timeout_encerra_execucao Bool)
; A1: linha 119: O Z3 e executado como processo externo [...] limite de 60 segundos
; A2: linha 123: Z3 e carregado como biblioteca dentro da JVM e nao e iniciado processo externo
; T1: linha 119 e Z3ProcessTest: Z3 travado no limite de tempo encerra o processo
; T2: linha 123: o valor de 60 segundos [...] nunca encerra a execucao


(echo "A1 isolada")
(push)
(assert z3_processo_externo) ; A1
(check-sat)
(pop)

(echo "A2 isolada")
(push)
(assert (not z3_processo_externo)) ; A2
(check-sat)
(pop)

(echo "A1 e A2")
(push)
(assert z3_processo_externo) ; A1
(assert (not z3_processo_externo)) ; A2
(check-sat)
(pop)

(echo "T1 isolada")
(push)
(assert timeout_encerra_execucao) ; T1
(check-sat)
(pop)

(echo "T2 isolada")
(push)
(assert (not timeout_encerra_execucao)) ; T2
(check-sat)
(pop)

(echo "T1 e T2")
(push)
(assert timeout_encerra_execucao) ; T1
(assert (not timeout_encerra_execucao)) ; T2
(check-sat)
(pop)
