; x = 0, x=0, resultado=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun x () Int)
(assert
 (= x 0))
(assert
 (let (($x7 (= x 0)))
(= $x7 true)))
(check-sat)

(reset)
; x = 0, x=1, resultado=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun x () Int)
(assert
 (= x 1))
(assert
 (let (($x7 (= x 0)))
(= $x7 false)))
(check-sat)

(reset)
; x == 0, x=0, resultado=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun x () Int)
(assert
 (= x 0))
(assert
 (let (($x7 (= x 0)))
(= $x7 true)))
(check-sat)

(reset)
; x == 0, x=1, resultado=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun x () Int)
(assert
 (= x 1))
(assert
 (let (($x7 (= x 0)))
(= $x7 false)))
(check-sat)

(reset)
; x != 0, x=1, resultado=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun x () Int)
(assert
 (= x 1))
(assert
 (let (($x8 (and (distinct x 0) true)))
(= $x8 true)))
(check-sat)

(reset)
; x != 0, x=0, resultado=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun x () Int)
(assert
 (= x 0))
(assert
 (let (($x8 (and (distinct x 0) true)))
(= $x8 false)))
(check-sat)

(reset)
; x < 0, x=-1, resultado=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun x () Int)
(assert
 (= x (- 1)))
(assert
 (let (($x9 (< x 0)))
(= $x9 true)))
(check-sat)

(reset)
; x < 0, x=0, resultado=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun x () Int)
(assert
 (= x 0))
(assert
 (let (($x9 (< x 0)))
(= $x9 false)))
(check-sat)

(reset)
; x <= 0, x=0, resultado=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun x () Int)
(assert
 (= x 0))
(assert
 (let (($x10 (<= x 0)))
(= $x10 true)))
(check-sat)

(reset)
; x <= 0, x=1, resultado=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun x () Int)
(assert
 (= x 1))
(assert
 (let (($x10 (<= x 0)))
(= $x10 false)))
(check-sat)

(reset)
; x > 0, x=1, resultado=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun x () Int)
(assert
 (= x 1))
(assert
 (let (($x11 (> x 0)))
(= $x11 true)))
(check-sat)

(reset)
; x > 0, x=0, resultado=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun x () Int)
(assert
 (= x 0))
(assert
 (let (($x11 (> x 0)))
(= $x11 false)))
(check-sat)

(reset)
; x >= 0, x=0, resultado=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun x () Int)
(assert
 (= x 0))
(assert
 (let (($x12 (>= x 0)))
(= $x12 true)))
(check-sat)

(reset)
; x >= 0, x=-1, resultado=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun x () Int)
(assert
 (= x (- 1)))
(assert
 (let (($x12 (>= x 0)))
(= $x12 false)))
(check-sat)
