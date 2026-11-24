; vm1 e vm4 escrevem valores diferentes em the_system_mode (e/ou the_coffee_machine_output);
; conflito só se as guardas puderem valer juntas. Esperado pelo C1 (0 conflitos na VM): unsat

(declare-datatypes () ((Mode idle choice preparing_weak preparing_strong)))
(declare-datatypes () ((Btn released pressed)))
(declare-const the_system_mode Mode)
(declare-const the_coin_sensor Bool)
(declare-const the_coin_sensor_antes Bool)
(declare-const the_coffee_request_button Btn)
(declare-const the_coffee_request_button_antes Btn)
(declare-const the_request_timer Real)

(assert (and (= the_system_mode idle) (= the_coin_sensor_antes false) (= the_coin_sensor true)))
(assert (and (= the_system_mode preparing_weak) (>= the_request_timer 10.0) (<= the_request_timer 30.0)))
(check-sat)
