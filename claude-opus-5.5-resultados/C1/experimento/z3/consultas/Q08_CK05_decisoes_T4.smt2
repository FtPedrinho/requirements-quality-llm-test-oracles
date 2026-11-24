; exemplos/decisoes.json #3: (mode = choice /\ button = true) \/ coin = true
; T4: mode=idle, button=true, coin=false, esperado T. Guarda = T? unsat => guarda é F => esperado divergente
(declare-datatypes () ((Mode idle choice preparing_strong preparing_weak)))
(declare-const mode Mode) (declare-const button Bool) (declare-const coin Bool)
(assert (= mode idle)) (assert (= button true)) (assert (= coin false))
(assert (or (and (= mode choice) (= button true)) (= coin true)))
(check-sat)
