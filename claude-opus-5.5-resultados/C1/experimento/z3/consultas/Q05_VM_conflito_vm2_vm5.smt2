; vm2 e vm5 escrevem valores diferentes em the_system_mode (e/ou the_coffee_machine_output);
; conflito só se as guardas puderem valer juntas. Esperado pelo C1 (0 conflitos na VM): unsat

(declare-datatypes () ((Mode idle choice preparing_weak preparing_strong)))
(declare-datatypes () ((Btn released pressed)))
(declare-const the_system_mode Mode)
(declare-const the_coin_sensor Bool)
(declare-const the_coin_sensor_antes Bool)
(declare-const the_coffee_request_button Btn)
(declare-const the_coffee_request_button_antes Btn)
(declare-const the_request_timer Real)

(assert (and (= the_system_mode choice) (= the_coin_sensor false) (= the_coin_sensor_antes false) (not (= the_coffee_request_button_antes pressed)) (= the_coffee_request_button pressed) (<= the_request_timer 30.0)))
(assert (and (= the_system_mode preparing_strong) (>= the_request_timer 30.0) (<= the_request_timer 50.0)))
(check-sat)
