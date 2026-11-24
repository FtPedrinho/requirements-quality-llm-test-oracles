; pares de independência de: (A and B) or C
; condição A, critério mascaramento
(push) (declare-const x0 Bool) (declare-const x1 Bool) (declare-const x2 Bool) (declare-const y0 Bool) (declare-const y1 Bool) (declare-const y2 Bool) (assert (and (not (= x0 y0)) (not (= (or (and x0 x1) x2) (or (and y0 y1) y2))) (not (= (or (and x0 x1) x2) (or (and (not x0) x1) x2))) (not (= (or (and y0 y1) y2) (or (and (not y0) y1) y2))))) (check-sat) (pop)
; condição A, critério causa_unica
(push) (declare-const x0 Bool) (declare-const x1 Bool) (declare-const x2 Bool) (declare-const y0 Bool) (declare-const y1 Bool) (declare-const y2 Bool) (assert (and (not (= x0 y0)) (not (= (or (and x0 x1) x2) (or (and y0 y1) y2))) (= x1 y1) (= x2 y2))) (check-sat) (pop)
; condição A, critério simplificado
(push) (declare-const x0 Bool) (declare-const x1 Bool) (declare-const x2 Bool) (declare-const y0 Bool) (declare-const y1 Bool) (declare-const y2 Bool) (assert (and (not (= x0 y0)))) (check-sat) (pop)
; condição B, critério mascaramento
(push) (declare-const x0 Bool) (declare-const x1 Bool) (declare-const x2 Bool) (declare-const y0 Bool) (declare-const y1 Bool) (declare-const y2 Bool) (assert (and (not (= x1 y1)) (not (= (or (and x0 x1) x2) (or (and y0 y1) y2))) (not (= (or (and x0 x1) x2) (or (and x0 (not x1)) x2))) (not (= (or (and y0 y1) y2) (or (and y0 (not y1)) y2))))) (check-sat) (pop)
; condição B, critério causa_unica
(push) (declare-const x0 Bool) (declare-const x1 Bool) (declare-const x2 Bool) (declare-const y0 Bool) (declare-const y1 Bool) (declare-const y2 Bool) (assert (and (not (= x1 y1)) (not (= (or (and x0 x1) x2) (or (and y0 y1) y2))) (= x0 y0) (= x2 y2))) (check-sat) (pop)
; condição B, critério simplificado
(push) (declare-const x0 Bool) (declare-const x1 Bool) (declare-const x2 Bool) (declare-const y0 Bool) (declare-const y1 Bool) (declare-const y2 Bool) (assert (and (not (= x1 y1)))) (check-sat) (pop)
; condição C, critério mascaramento
(push) (declare-const x0 Bool) (declare-const x1 Bool) (declare-const x2 Bool) (declare-const y0 Bool) (declare-const y1 Bool) (declare-const y2 Bool) (assert (and (not (= x2 y2)) (not (= (or (and x0 x1) x2) (or (and y0 y1) y2))) (not (= (or (and x0 x1) x2) (or (and x0 x1) (not x2)))) (not (= (or (and y0 y1) y2) (or (and y0 y1) (not y2)))))) (check-sat) (pop)
; condição C, critério causa_unica
(push) (declare-const x0 Bool) (declare-const x1 Bool) (declare-const x2 Bool) (declare-const y0 Bool) (declare-const y1 Bool) (declare-const y2 Bool) (assert (and (not (= x2 y2)) (not (= (or (and x0 x1) x2) (or (and y0 y1) y2))) (= x0 y0) (= x1 y1))) (check-sat) (pop)
; condição C, critério simplificado
(push) (declare-const x0 Bool) (declare-const x1 Bool) (declare-const x2 Bool) (declare-const y0 Bool) (declare-const y1 Bool) (declare-const y2 Bool) (assert (and (not (= x2 y2)))) (check-sat) (pop)
