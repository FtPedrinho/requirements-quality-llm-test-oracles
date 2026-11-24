; guardas de exemplos/decisoes.json avaliadas nos testes de exemplos/testes.csv
(declare-datatypes () ((Mode idle choice preparing_strong preparing_weak)))
(declare-const the_system_mode Mode)(declare-const the_coin_sensor Bool)(declare-const the_coffee_request_button Bool)
(push)(assert (and (= the_system_mode idle) (= the_coin_sensor true) (and (= the_system_mode idle) (= the_coin_sensor true))))(check-sat)(pop) ; the_coffee_machine_system#1 T1
(push)(assert (and (= the_system_mode idle) (= the_coin_sensor false) (and (= the_system_mode idle) (= the_coin_sensor true))))(check-sat)(pop) ; the_coffee_machine_system#1 T2
(push)(assert (and (= the_system_mode choice) (= the_coffee_request_button true) (= the_coin_sensor false) (or (and (= the_system_mode choice) (= the_coffee_request_button true)) (= the_coin_sensor true))))(check-sat)(pop) ; the_coffee_machine_system#3 T3
(push)(assert (and (= the_system_mode idle) (= the_coffee_request_button true) (= the_coin_sensor false) (or (and (= the_system_mode choice) (= the_coffee_request_button true)) (= the_coin_sensor true))))(check-sat)(pop) ; the_coffee_machine_system#3 T4
