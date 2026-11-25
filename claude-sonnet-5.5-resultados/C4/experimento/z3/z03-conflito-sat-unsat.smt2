; Conflito textual: significado de unsat/sat para combinacoes impossiveis (linhas 81 e 83).
(set-logic ALL)

(declare-const q_unsat Bool)
(declare-const impossivel Bool)
; S1: linha 81: as que retornam `unsat` sao consideradas impossiveis e nao participam da analise
; S2: linha 83: resultados `unsat` representam combinacoes possiveis [...] `sat` impossiveis

(assert q_unsat)

(echo "S1 isolada (consulta com resposta unsat)")
(push)
(assert (= impossivel q_unsat)) ; S1
(check-sat)
(pop)

(echo "S2 isolada (consulta com resposta unsat)")
(push)
(assert (= impossivel (not q_unsat))) ; S2
(check-sat)
(pop)

(echo "S1 e S2")
(push)
(assert (= impossivel q_unsat)) ; S1
(assert (= impossivel (not q_unsat))) ; S2
(check-sat)
(pop)
