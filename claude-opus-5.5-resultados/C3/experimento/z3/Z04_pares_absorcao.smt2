; pares de independência de: A or (A and B)
; condição A, critério mascaramento
(push) (declare-const x0 Bool) (declare-const x1 Bool) (declare-const y0 Bool) (declare-const y1 Bool) (assert (and (not (= x0 y0)) (not (= (or x0 (and x0 x1)) (or y0 (and y0 y1)))) (not (= (or x0 (and x0 x1)) (or (not x0) (and (not x0) x1)))) (not (= (or y0 (and y0 y1)) (or (not y0) (and (not y0) y1)))))) (check-sat) (pop)
; condição A, critério causa_unica
(push) (declare-const x0 Bool) (declare-const x1 Bool) (declare-const y0 Bool) (declare-const y1 Bool) (assert (and (not (= x0 y0)) (not (= (or x0 (and x0 x1)) (or y0 (and y0 y1)))) (= x1 y1))) (check-sat) (pop)
; condição A, critério simplificado
(push) (declare-const x0 Bool) (declare-const x1 Bool) (declare-const y0 Bool) (declare-const y1 Bool) (assert (and (not (= x0 y0)))) (check-sat) (pop)
; condição B, critério mascaramento
(push) (declare-const x0 Bool) (declare-const x1 Bool) (declare-const y0 Bool) (declare-const y1 Bool) (assert (and (not (= x1 y1)) (not (= (or x0 (and x0 x1)) (or y0 (and y0 y1)))) (not (= (or x0 (and x0 x1)) (or x0 (and x0 (not x1))))) (not (= (or y0 (and y0 y1)) (or y0 (and y0 (not y1))))))) (check-sat) (pop)
; condição B, critério causa_unica
(push) (declare-const x0 Bool) (declare-const x1 Bool) (declare-const y0 Bool) (declare-const y1 Bool) (assert (and (not (= x1 y1)) (not (= (or x0 (and x0 x1)) (or y0 (and y0 y1)))) (= x0 y0))) (check-sat) (pop)
; condição B, critério simplificado
(push) (declare-const x0 Bool) (declare-const x1 Bool) (declare-const y0 Bool) (declare-const y1 Bool) (assert (and (not (= x1 y1)))) (check-sat) (pop)
