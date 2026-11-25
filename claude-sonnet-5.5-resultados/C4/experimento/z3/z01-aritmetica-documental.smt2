; Consistencia aritmetica dos numeros declarados no texto C4 (nao prova fidelidade).
(set-logic ALL)
(declare-const vm_req Int)
(declare-const vm_comp Int)
(declare-const vm_cond Int)
(declare-const vm_comb Int)
(declare-const vm_imp Int)
(declare-const vm_tst Int)
(declare-const vm_mut Int)
(declare-const vm_eq Int)
(declare-const vm_peg Int)
(declare-const vm_conf Int)
(declare-const tis_req Int)
(declare-const tis_comp Int)
(declare-const tis_cond Int)
(declare-const tis_comb Int)
(declare-const tis_imp Int)
(declare-const tis_tst Int)
(declare-const tis_mut Int)
(declare-const tis_eq Int)
(declare-const tis_peg Int)
(declare-const tis_conf Int)
(declare-const npp_req Int)
(declare-const npp_comp Int)
(declare-const npp_cond Int)
(declare-const npp_comb Int)
(declare-const npp_imp Int)
(declare-const npp_tst Int)
(declare-const npp_mut Int)
(declare-const npp_eq Int)
(declare-const npp_peg Int)
(declare-const npp_conf Int)
(declare-const tot_req Int)
(declare-const tot_comp Int)
(declare-const tot_cond Int)
(declare-const tot_comb Int)
(declare-const tot_imp Int)
(declare-const tot_tst Int)
(declare-const tot_mut Int)
(declare-const tot_eq Int)
(declare-const tot_peg Int)
(declare-const tot_conf Int)
(declare-const escapou Int)

(assert (= vm_req 5)) ; linha vm, coluna req
(assert (= vm_comp 5)) ; linha vm, coluna comp
(assert (= vm_cond 21)) ; linha vm, coluna cond
(assert (= vm_comb 152)) ; linha vm, coluna comb
(assert (= vm_imp 4)) ; linha vm, coluna imp
(assert (= vm_tst 26)) ; linha vm, coluna tst
(assert (= vm_mut 152)) ; linha vm, coluna mut
(assert (= vm_eq 0)) ; linha vm, coluna eq
(assert (= vm_peg 152)) ; linha vm, coluna peg
(assert (= vm_conf 0)) ; linha vm, coluna conf
(assert (= tis_req 17)) ; linha tis, coluna req
(assert (= tis_comp 14)) ; linha tis, coluna comp
(assert (= tis_cond 69)) ; linha tis, coluna cond
(assert (= tis_comb 268)) ; linha tis, coluna comb
(assert (= tis_imp 4)) ; linha tis, coluna imp
(assert (= tis_tst 80)) ; linha tis, coluna tst
(assert (= tis_mut 450)) ; linha tis, coluna mut
(assert (= tis_eq 21)) ; linha tis, coluna eq
(assert (= tis_peg 428)) ; linha tis, coluna peg
(assert (= tis_conf 3)) ; linha tis, coluna conf
(assert (= npp_req 11)) ; linha npp, coluna req
(assert (= npp_comp 11)) ; linha npp, coluna comp
(assert (= npp_cond 29)) ; linha npp, coluna cond
(assert (= npp_comb 76)) ; linha npp, coluna comb
(assert (= npp_imp 1)) ; linha npp, coluna imp
(assert (= npp_tst 40)) ; linha npp, coluna tst
(assert (= npp_mut 146)) ; linha npp, coluna mut
(assert (= npp_eq 0)) ; linha npp, coluna eq
(assert (= npp_peg 146)) ; linha npp, coluna peg
(assert (= npp_conf 1)) ; linha npp, coluna conf
(assert (= tot_req 33)) ; linha tot, coluna req
(assert (= tot_comp 30)) ; linha tot, coluna comp
(assert (= tot_cond 119)) ; linha tot, coluna cond
(assert (= tot_comb 496)) ; linha tot, coluna comb
(assert (= tot_imp 9)) ; linha tot, coluna imp
(assert (= tot_tst 146)) ; linha tot, coluna tst
(assert (= tot_mut 748)) ; linha tot, coluna mut
(assert (= tot_eq 21)) ; linha tot, coluna eq
(assert (= tot_peg 726)) ; linha tot, coluna peg
(assert (= tot_conf 4)) ; linha tot, coluna conf

(echo "A01 linha Total = soma das tres linhas (todas as colunas)")
(push)
(assert (= tot_req (+ vm_req tis_req npp_req)))
(assert (= tot_comp (+ vm_comp tis_comp npp_comp)))
(assert (= tot_cond (+ vm_cond tis_cond npp_cond)))
(assert (= tot_comb (+ vm_comb tis_comb npp_comb)))
(assert (= tot_imp (+ vm_imp tis_imp npp_imp)))
(assert (= tot_tst (+ vm_tst tis_tst npp_tst)))
(assert (= tot_mut (+ vm_mut tis_mut npp_mut)))
(assert (= tot_eq (+ vm_eq tis_eq npp_eq)))
(assert (= tot_peg (+ vm_peg tis_peg npp_peg)))
(assert (= tot_conf (+ vm_conf tis_conf npp_conf)))
(check-sat)
(pop)

(echo "A02 requisito completo: testes = condicoes + 1 (VM e NPP, todos os requisitos completos)")
(push)
(assert (= vm_comp vm_req))
(assert (= vm_tst (+ vm_cond vm_comp)))
(assert (= npp_comp npp_req))
(assert (= npp_tst (+ npp_cond npp_comp)))
(check-sat)
(pop)

(echo "A03 TIS: detectados + equivalentes + escapou = total de mutantes, escapou = 1 (linha 407)")
(push)
(assert (= escapou 1))
(assert (= tis_mut (+ tis_peg tis_eq escapou)))
(assert (= (- tot_mut tot_eq) 727))
(assert (= (- tot_mut tot_eq tot_peg) escapou))
(check-sat)
(pop)

(echo "A04 TIS: com escapou = 0 (linha 409) a soma nao fecha (unsat esperado)")
(push)
(assert (= escapou 0))
(assert (= tis_mut (+ tis_peg tis_eq escapou)))
(check-sat)
(pop)

(echo "A05 soma dos testes por classe listados = 171 e 34 arquivos")
(push)
(assert (= (+ 4 1 2  4 4  3 6  8 2 4 8 4 5 6 6 14 2 5 6  9 3 4 4 4  12 2 5 4 4 4  14 3 2 3) 171))
(check-sat)
(pop)

(echo "A06 testes por modulo 78+24+34+35 = 171")
(push)
(assert (= (+ 78 24 34 35) 171))
(check-sat)
(pop)

(echo "A07 arquivos de teste: 12 core + 7 transversais + 5 requisitos + 6 z3 + 4 cli = 34")
(push)
(assert (= (+ 12 7 5 6 4) 34))
(check-sat)
(pop)

(echo "A08 mutacao por modulo: numeradores 319+140+269+196 = 924 e denominadores 333+145+295+256 = 1029")
(push)
(assert (= (+ 319 140 269 196) 924))
(assert (= (+ 333 145 295 256) 1029))
(check-sat)
(pop)

(echo "A09 percentuais 95,5% (1911/2001), 90,3% (1170/1296), 89,8% (924/1029), 92,7% (924/997)")
(push)
(assert (> (/ 1911.0 2001.0) 0.9545))
(assert (< (/ 1911.0 2001.0) 0.9555))
(assert (> (/ 1170.0 1296.0) 0.9025))
(assert (< (/ 1170.0 1296.0) 0.9035))
(assert (> (/ 924.0 1029.0) 0.8975))
(assert (< (/ 924.0 1029.0) 0.8985))
(assert (> (/ 924.0 997.0) 0.9265))
(assert (< (/ 924.0 997.0) 0.9275))
(check-sat)
(pop)

(echo "A10 limites: 2^20 = 1048576 ~ 1 milhao; 12 (Z3 linha a linha) < 20 (tabela) < 30 (direto)")
(push)
(assert (= (* 1024 1024) 1048576))
(assert (< 12 20))
(assert (< 20 30))
(check-sat)
(pop)
