; verify --context 'the_system_mode = preparing_weak': existe situação em que nenhuma guarda vale? sat => lacuna

(declare-datatypes () ((Mode idle choice preparing_weak preparing_strong)))
(declare-datatypes () ((Btn released pressed)))
(declare-const the_system_mode Mode)
(declare-const the_coin_sensor Bool)
(declare-const the_coin_sensor_antes Bool)
(declare-const the_coffee_request_button Btn)
(declare-const the_coffee_request_button_antes Btn)
(declare-const the_request_timer Real)

(assert (= the_system_mode preparing_weak))
(assert (not (or (and (= the_system_mode idle) (= the_coin_sensor_antes false) (= the_coin_sensor true)) (and (= the_system_mode choice) (= the_coin_sensor false) (= the_coin_sensor_antes false) (not (= the_coffee_request_button_antes pressed)) (= the_coffee_request_button pressed) (<= the_request_timer 30.0)) (and (= the_system_mode choice) (= the_coin_sensor false) (= the_coin_sensor_antes false) (not (= the_coffee_request_button_antes pressed)) (= the_coffee_request_button pressed) (> the_request_timer 30.0)) (and (= the_system_mode preparing_weak) (>= the_request_timer 10.0) (<= the_request_timer 30.0)) (and (= the_system_mode preparing_strong) (>= the_request_timer 30.0) (<= the_request_timer 50.0)))))
(check-sat)
(get-model)
