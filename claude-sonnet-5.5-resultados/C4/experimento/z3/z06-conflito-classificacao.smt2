; Conflito textual: redundante x bloqueada (linhas 93 e 95).
(set-logic ALL)

(declare-datatypes ((Rot 0)) (((redundante) (bloqueada))))
(declare-const rot_sem_par_em_todas Rot)
(declare-const rot_perde_par_por_impossiveis Rot)
; R1: linha 93: sem par mesmo considerando todas as combinacoes -> redundante; perde par por impossiveis -> bloqueada
; R2: linha 95: sem par em qualquer cenario -> bloqueada; perde par so por impossiveis -> redundante
; R3: linha 95: as duas classificacoes sao intercambiaveis e nao dependem do caso de ausencia de par


(echo "R1 isolada")
(push)
(assert (and (= rot_sem_par_em_todas redundante) (= rot_perde_par_por_impossiveis bloqueada))) ; R1
(check-sat)
(pop)

(echo "R2 isolada")
(push)
(assert (and (= rot_sem_par_em_todas bloqueada) (= rot_perde_par_por_impossiveis redundante))) ; R2
(check-sat)
(pop)

(echo "R3 isolada")
(push)
(assert (= rot_sem_par_em_todas rot_perde_par_por_impossiveis)) ; R3
(check-sat)
(pop)

(echo "R1 e R2")
(push)
(assert (and (= rot_sem_par_em_todas redundante) (= rot_perde_par_por_impossiveis bloqueada))) ; R1
(assert (and (= rot_sem_par_em_todas bloqueada) (= rot_perde_par_por_impossiveis redundante))) ; R2
(check-sat)
(pop)

(echo "R1 e R3")
(push)
(assert (and (= rot_sem_par_em_todas redundante) (= rot_perde_par_por_impossiveis bloqueada))) ; R1
(assert (= rot_sem_par_em_todas rot_perde_par_por_impossiveis)) ; R3
(check-sat)
(pop)

(echo "R1, R2 e R3")
(push)
(assert (and (= rot_sem_par_em_todas redundante) (= rot_perde_par_por_impossiveis bloqueada))) ; R1
(assert (and (= rot_sem_par_em_todas bloqueada) (= rot_perde_par_por_impossiveis redundante))) ; R2
(assert (= rot_sem_par_em_todas rot_perde_par_por_impossiveis)) ; R3
(check-sat)
(pop)
