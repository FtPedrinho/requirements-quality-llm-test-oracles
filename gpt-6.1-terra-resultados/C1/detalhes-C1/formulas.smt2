; Blocos independentes, cada bloco reinicia o contexto.
; A vetor=0 saida=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun A () Bool)
(assert
 (let (($x13 (= A false)))
(and $x13 $x13)))
(check-sat)


(reset)
; A vetor=0 saida=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun A () Bool)
(assert
 (let (($x13 (= A false)))
(and $x13 (= A true))))
(check-sat)


(reset)
; A vetor=1 saida=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun A () Bool)
(assert
 (let (($x15 (= A true)))
(and $x15 (= A false))))
(check-sat)


(reset)
; A vetor=1 saida=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun A () Bool)
(assert
 (let (($x15 (= A true)))
(and $x15 $x15)))
(check-sat)


(reset)
; not_A vetor=0 saida=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun A () Bool)
(assert
 (let (($x13 (= A false)))
(and $x13 (= (not A) false))))
(check-sat)


(reset)
; not_A vetor=0 saida=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun A () Bool)
(assert
 (let (($x13 (= A false)))
(and $x13 (= (not A) true))))
(check-sat)


(reset)
; not_A vetor=1 saida=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun A () Bool)
(assert
 (let (($x28 (= A true)))
(and $x28 (= (not A) false))))
(check-sat)


(reset)
; not_A vetor=1 saida=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun A () Bool)
(assert
 (let (($x28 (= A true)))
(and $x28 (= (not A) true))))
(check-sat)


(reset)
; A_and_B vetor=0 saida=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x25 (= B false)))
(let (($x16 (= A false)))
(and $x16 $x25 (= (and A B) false)))))
(check-sat)


(reset)
; A_and_B vetor=0 saida=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x25 (= B false)))
(let (($x16 (= A false)))
(and $x16 $x25 (= (and A B) true)))))
(check-sat)


(reset)
; A_and_B vetor=1 saida=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x25 (= B false)))
(let (($x21 (= A true)))
(and $x21 $x25 (= (and A B) false)))))
(check-sat)


(reset)
; A_and_B vetor=1 saida=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x25 (= B false)))
(let (($x21 (= A true)))
(and $x21 $x25 (= (and A B) true)))))
(check-sat)


(reset)
; A_and_B vetor=2 saida=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x17 (= B true)))
(let (($x31 (= A false)))
(and $x31 $x17 (= (and A B) false)))))
(check-sat)


(reset)
; A_and_B vetor=2 saida=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x17 (= B true)))
(let (($x31 (= A false)))
(and $x31 $x17 (= (and A B) true)))))
(check-sat)


(reset)
; A_and_B vetor=3 saida=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x17 (= B true)))
(let (($x13 (= A true)))
(and $x13 $x17 (= (and A B) false)))))
(check-sat)


(reset)
; A_and_B vetor=3 saida=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x17 (= B true)))
(let (($x13 (= A true)))
(and $x13 $x17 (= (and A B) true)))))
(check-sat)


(reset)
; A_or_B vetor=0 saida=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x14 (= B false)))
(let (($x33 (= A false)))
(and $x33 $x14 (= (or A B) false)))))
(check-sat)


(reset)
; A_or_B vetor=0 saida=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x14 (= B false)))
(let (($x33 (= A false)))
(and $x33 $x14 (= (or A B) true)))))
(check-sat)


(reset)
; A_or_B vetor=1 saida=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x14 (= B false)))
(let (($x19 (= A true)))
(and $x19 $x14 (= (or A B) false)))))
(check-sat)


(reset)
; A_or_B vetor=1 saida=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x14 (= B false)))
(let (($x19 (= A true)))
(and $x19 $x14 (= (or A B) true)))))
(check-sat)


(reset)
; A_or_B vetor=2 saida=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x23 (= B true)))
(let (($x31 (= A false)))
(and $x31 $x23 (= (or A B) false)))))
(check-sat)


(reset)
; A_or_B vetor=2 saida=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x23 (= B true)))
(let (($x31 (= A false)))
(and $x31 $x23 (= (or A B) true)))))
(check-sat)


(reset)
; A_or_B vetor=3 saida=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x23 (= B true)))
(let (($x21 (= A true)))
(and $x21 $x23 (= (or A B) false)))))
(check-sat)


(reset)
; A_or_B vetor=3 saida=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x23 (= B true)))
(let (($x21 (= A true)))
(and $x21 $x23 (= (or A B) true)))))
(check-sat)


(reset)
; A_and_B_or_C vetor=0 saida=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun C () Bool)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x22 (= C false)))
(let (($x15 (= B false)))
(let (($x26 (= A false)))
(and $x26 $x15 $x22 (= (or (and A B) C) false))))))
(check-sat)


(reset)
; A_and_B_or_C vetor=0 saida=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun C () Bool)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x22 (= C false)))
(let (($x15 (= B false)))
(let (($x26 (= A false)))
(and $x26 $x15 $x22 (= (or (and A B) C) true))))))
(check-sat)


(reset)
; A_and_B_or_C vetor=1 saida=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun C () Bool)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x22 (= C false)))
(let (($x15 (= B false)))
(let (($x20 (= A true)))
(and $x20 $x15 $x22 (= (or (and A B) C) false))))))
(check-sat)


(reset)
; A_and_B_or_C vetor=1 saida=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun C () Bool)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x22 (= C false)))
(let (($x15 (= B false)))
(let (($x20 (= A true)))
(and $x20 $x15 $x22 (= (or (and A B) C) true))))))
(check-sat)


(reset)
; A_and_B_or_C vetor=2 saida=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun C () Bool)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x22 (= C false)))
(let (($x36 (= B true)))
(let (($x24 (= A false)))
(and $x24 $x36 $x22 (= (or (and A B) C) false))))))
(check-sat)


(reset)
; A_and_B_or_C vetor=2 saida=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun C () Bool)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x22 (= C false)))
(let (($x36 (= B true)))
(let (($x24 (= A false)))
(and $x24 $x36 $x22 (= (or (and A B) C) true))))))
(check-sat)


(reset)
; A_and_B_or_C vetor=3 saida=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun C () Bool)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x22 (= C false)))
(let (($x36 (= B true)))
(let (($x28 (= A true)))
(and $x28 $x36 $x22 (= (or (and A B) C) false))))))
(check-sat)


(reset)
; A_and_B_or_C vetor=3 saida=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun C () Bool)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x22 (= C false)))
(let (($x36 (= B true)))
(let (($x28 (= A true)))
(and $x28 $x36 $x22 (= (or (and A B) C) true))))))
(check-sat)


(reset)
; A_and_B_or_C vetor=4 saida=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun C () Bool)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x21 (= C true)))
(let (($x15 (= B false)))
(let (($x29 (= A false)))
(and $x29 $x15 $x21 (= (or (and A B) C) false))))))
(check-sat)


(reset)
; A_and_B_or_C vetor=4 saida=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun C () Bool)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x21 (= C true)))
(let (($x15 (= B false)))
(let (($x29 (= A false)))
(and $x29 $x15 $x21 (= (or (and A B) C) true))))))
(check-sat)


(reset)
; A_and_B_or_C vetor=5 saida=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun C () Bool)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x21 (= C true)))
(let (($x15 (= B false)))
(let (($x14 (= A true)))
(and $x14 $x15 $x21 (= (or (and A B) C) false))))))
(check-sat)


(reset)
; A_and_B_or_C vetor=5 saida=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun C () Bool)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x21 (= C true)))
(let (($x15 (= B false)))
(let (($x14 (= A true)))
(and $x14 $x15 $x21 (= (or (and A B) C) true))))))
(check-sat)


(reset)
; A_and_B_or_C vetor=6 saida=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun C () Bool)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x21 (= C true)))
(let (($x40 (= B true)))
(let (($x27 (= A false)))
(and $x27 $x40 $x21 (= (or (and A B) C) false))))))
(check-sat)


(reset)
; A_and_B_or_C vetor=6 saida=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun C () Bool)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x21 (= C true)))
(let (($x40 (= B true)))
(let (($x27 (= A false)))
(and $x27 $x40 $x21 (= (or (and A B) C) true))))))
(check-sat)


(reset)
; A_and_B_or_C vetor=7 saida=False
; benchmark generated from python API
(set-info :status unknown)
(declare-fun C () Bool)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x21 (= C true)))
(let (($x40 (= B true)))
(let (($x19 (= A true)))
(and $x19 $x40 $x21 (= (or (and A B) C) false))))))
(check-sat)


(reset)
; A_and_B_or_C vetor=7 saida=True
; benchmark generated from python API
(set-info :status unknown)
(declare-fun C () Bool)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x21 (= C true)))
(let (($x40 (= B true)))
(let (($x19 (= A true)))
(and $x19 $x40 $x21 (= (or (and A B) C) true))))))
(check-sat)


(reset)
; B22 restricao exclui A=T B=F
; benchmark generated from python API
(set-info :status unknown)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x37 (not B)))
(and (or (not A) B) A $x37)))
(check-sat)


(reset)
; B22 restricao admite A=F B=F
; benchmark generated from python API
(set-info :status unknown)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x37 (not B)))
(let (($x9 (not A)))
(and (or $x9 B) $x9 $x37))))
(check-sat)


(reset)
; B23 impossibilidade speed>100 e nao speed>50
; benchmark generated from python API
(set-info :status unknown)
(declare-fun speed () Int)
(assert
 (let (($x13 (<= speed 50)))
(and (> speed 100) $x13)))
(check-sat)


(reset)
; B23 fronteira falsa
; benchmark generated from python API
(set-info :status unknown)
(declare-fun speed () Int)
(assert
 (= speed 100))
(check-sat)


(reset)
; B23 fronteira verdadeira
; benchmark generated from python API
(set-info :status unknown)
(declare-fun speed () Int)
(assert
 (= speed 101))
(check-sat)


(reset)
; B26 conflito
; benchmark generated from python API
(set-info :status unknown)
(declare-fun A () Bool)
(assert
 (and A true))
(check-sat)


(reset)
; B27 lacuna
; benchmark generated from python API
(set-info :status unknown)
(declare-fun A () Bool)
(assert
 (let (($x16 (not A)))
(and $x16 $x16)))
(check-sat)


(reset)
; B29 B muda decisao
; benchmark generated from python API
(set-info :status unknown)
(declare-fun B () Bool)
(declare-fun A () Bool)
(assert
 (let (($x23 (or A (and A (not B)))))
(let (($x10 (and A B)))
(let (($x20 (or A $x10)))
(xor $x20 $x23)))))
(check-sat)


(reset)
; B30 A muda entre vetores validos
; benchmark generated from python API
(set-info :status unknown)
(declare-fun A () Bool)
(assert
 (and A (not A)))
(check-sat)


(reset)
; B24 cobertura causa unica com no maximo 3 vetores
; benchmark generated from python API
(set-info :status unknown)
(declare-fun v7 () Bool)
(declare-fun v6 () Bool)
(declare-fun v5 () Bool)
(declare-fun v4 () Bool)
(declare-fun v3 () Bool)
(declare-fun v2 () Bool)
(declare-fun v1 () Bool)
(declare-fun v0 () Bool)
(assert
 (let ((?x38 (ite v7 1 0)))
(let ((?x30 (ite v6 1 0)))
(let ((?x35 (ite v5 1 0)))
(let ((?x24 (ite v4 1 0)))
(let ((?x13 (ite v3 1 0)))
(let ((?x22 (ite v2 1 0)))
(let ((?x14 (ite v1 1 0)))
(let ((?x18 (ite v0 1 0)))
(let (($x9 (and v2 v6)))
(let (($x37 (and v1 v5)))
(let (($x36 (and v0 v4)))
(let (($x23 (or $x36 $x37 $x9)))
(let (($x25 (and v1 v3)))
(let (($x32 (or $x25)))
(let (($x39 (and v2 v3)))
(let (($x34 (or $x39)))
(and $x34 $x32 $x23 (<= (+ ?x18 ?x14 ?x22 ?x13 ?x24 ?x35 ?x30 ?x38) 3)))))))))))))))))))
(check-sat)


(reset)
; B24 cobertura causa unica com no maximo 4 vetores
; benchmark generated from python API
(set-info :status unknown)
(declare-fun v7 () Bool)
(declare-fun v6 () Bool)
(declare-fun v5 () Bool)
(declare-fun v4 () Bool)
(declare-fun v3 () Bool)
(declare-fun v2 () Bool)
(declare-fun v1 () Bool)
(declare-fun v0 () Bool)
(assert
 (let ((?x38 (ite v7 1 0)))
(let ((?x30 (ite v6 1 0)))
(let ((?x35 (ite v5 1 0)))
(let ((?x24 (ite v4 1 0)))
(let ((?x13 (ite v3 1 0)))
(let ((?x22 (ite v2 1 0)))
(let ((?x14 (ite v1 1 0)))
(let ((?x18 (ite v0 1 0)))
(let (($x9 (and v2 v6)))
(let (($x37 (and v1 v5)))
(let (($x36 (and v0 v4)))
(let (($x23 (or $x36 $x37 $x9)))
(let (($x25 (and v1 v3)))
(let (($x32 (or $x25)))
(let (($x39 (and v2 v3)))
(let (($x34 (or $x39)))
(and $x34 $x32 $x23 (<= (+ ?x18 ?x14 ?x22 ?x13 ?x24 ?x35 ?x30 ?x38) 4)))))))))))))))))))
(check-sat)

