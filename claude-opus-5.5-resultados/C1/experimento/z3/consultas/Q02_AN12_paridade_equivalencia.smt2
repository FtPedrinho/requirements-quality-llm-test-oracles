; a expressão do AN-12 é a paridade (ímpar) de 3 entradas? unsat => equivalente
(declare-const A Bool) (declare-const B Bool) (declare-const C Bool)
(define-fun e () Bool (or (and A (not B) (not C)) (and (not A) B (not C)) (and (not A) (not B) C) (and A B C)))
(assert (not (= e (xor A (xor B C)))))
(check-sat)
