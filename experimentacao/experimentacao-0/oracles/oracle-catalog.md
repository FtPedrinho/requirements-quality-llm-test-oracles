# Catálogo de oráculos

Os oráculos desta etapa foram preparados a partir exclusivamente dos textos e guardas originais. Nenhum resultado interpretativo do Z3 foi usado como resposta esperada.

| Oracle ID | Requirement ID | Decision ID | Resultado esperado | Fonte |
|---|---|---|---|---|
| ORC-001 | REQ001 | vm#1 | verdadeiro quando a guarda é satisfeita | exemplos/vm-decisoes.json |
| ORC-002 | REQ002 | vm#2 | verdadeiro quando a guarda é satisfeita | exemplos/vm-decisoes.json |
| ORC-003 | REQ003 | vm#3 | verdadeiro quando a guarda é satisfeita | exemplos/vm-decisoes.json |
| ORC-004 | REQ004 | vm#4 | verdadeiro quando a guarda é satisfeita | exemplos/vm-decisoes.json |
| ORC-005 | REQ005 | vm#5 | verdadeiro quando a guarda é satisfeita | exemplos/vm-decisoes.json |
| ORC-006 | REQ001 | tis#1 | verdadeiro quando a guarda é satisfeita | exemplos/tis-decisoes.json |
| ORC-007 | REQ002 | tis#2 | verdadeiro quando a guarda é satisfeita | exemplos/tis-decisoes.json |
| ORC-008 | REQ003 | tis#3 | verdadeiro quando a guarda é satisfeita | exemplos/tis-decisoes.json |
| ORC-009 | REQ004 | tis#4 | verdadeiro quando a guarda é satisfeita | exemplos/tis-decisoes.json |
| ORC-010 | REQ005 | tis#5 | verdadeiro quando a guarda é satisfeita | exemplos/tis-decisoes.json |
| ORC-011 | REQ006 | tis#6 | verdadeiro quando a guarda é satisfeita | exemplos/tis-decisoes.json |
| ORC-012 | REQ007 | tis#7 | verdadeiro quando a guarda é satisfeita | exemplos/tis-decisoes.json |
| ORC-013 | REQ008 | tis#8 | verdadeiro quando a guarda é satisfeita | exemplos/tis-decisoes.json |
| ORC-014 | REQ009 | tis#9 | verdadeiro quando a guarda é satisfeita | exemplos/tis-decisoes.json |
| ORC-015 | REQ010 | tis#10 | verdadeiro quando a guarda é satisfeita | exemplos/tis-decisoes.json |
| ORC-016 | REQ011 | tis#11 | verdadeiro quando a guarda é satisfeita | exemplos/tis-decisoes.json |
| ORC-017 | REQ012 | tis#12 | verdadeiro quando a guarda é satisfeita | exemplos/tis-decisoes.json |
| ORC-018 | REQ013 | tis#13 | verdadeiro quando a guarda é satisfeita | exemplos/tis-decisoes.json |
| ORC-019 | REQ014 | tis#14 | verdadeiro quando a guarda é satisfeita | exemplos/tis-decisoes.json |
| ORC-020 | REQ015 | tis#15 | verdadeiro quando a guarda é satisfeita | exemplos/tis-decisoes.json |
| ORC-021 | REQ016 | tis#16 | verdadeiro quando a guarda é satisfeita | exemplos/tis-decisoes.json |
| ORC-022 | REQ017 | tis#17 | verdadeiro quando a guarda é satisfeita | exemplos/tis-decisoes.json |
| ORC-023 | REQ001 | npp#1 | verdadeiro quando a guarda é satisfeita | exemplos/npp-decisoes.json |
| ORC-024 | REQ002 | npp#2 | verdadeiro quando a guarda é satisfeita | exemplos/npp-decisoes.json |
| ORC-025 | REQ003 | npp#3 | verdadeiro quando a guarda é satisfeita | exemplos/npp-decisoes.json |
| ORC-026 | REQ004 | npp#4 | verdadeiro quando a guarda é satisfeita | exemplos/npp-decisoes.json |
| ORC-027 | REQ005 | npp#5 | verdadeiro quando a guarda é satisfeita | exemplos/npp-decisoes.json |
| ORC-028 | REQ006 | npp#6 | verdadeiro quando a guarda é satisfeita | exemplos/npp-decisoes.json |
| ORC-029 | REQ007 | npp#7 | verdadeiro quando a guarda é satisfeita | exemplos/npp-decisoes.json |
| ORC-030 | REQ008 | npp#8 | verdadeiro quando a guarda é satisfeita | exemplos/npp-decisoes.json |
| ORC-031 | REQ009 | npp#9 | verdadeiro quando a guarda é satisfeita | exemplos/npp-decisoes.json |
| ORC-032 | REQ010 | npp#10 | verdadeiro quando a guarda é satisfeita | exemplos/npp-decisoes.json |
| ORC-033 | REQ011 | npp#11 | verdadeiro quando a guarda é satisfeita | exemplos/npp-decisoes.json |
| ORC-034 | REQ-001 | generic-REQ-001 | verdadeiro quando a guarda é satisfeita | exemplos/requisitos.mcdc |
| ORC-035 | REQ-002 | generic-REQ-002 | verdadeiro quando a guarda é satisfeita | exemplos/requisitos.mcdc |
| ORC-036 | REQ-003 | generic-REQ-003 | verdadeiro quando a guarda é satisfeita | exemplos/requisitos.mcdc |

## Campos estruturados

### ORC-001 - vm#1
- **Preconditions:** the_system_mode = idle /\ the_coin_sensor_antes = false /\ the_coin_sensor = true
- **Initial State:** Não especificado
- **Inputs:** the_system_mode, the_coin_sensor, the_coin_sensor_antes
- **Conditions:** the_system_mode = idle /\ the_coin_sensor_antes = false /\ the_coin_sensor = true
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_request_timer := 0, the_system_mode := choice
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_request_timer recebe 0; the_system_mode recebe choice
- **Rationale:** When the system mode is idle, and the coin sensor changes to true, the coffee machine system shall: reset the request timer, assign choice to the system mode.
- **Source Reference:** exemplos/vm-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa., A semântica do estado anterior depende da transição documentada no texto original.

### ORC-002 - vm#2
- **Preconditions:** the_system_mode = choice /\ the_coin_sensor = false /\ the_coin_sensor_antes = false /\ the_coffee_request_button_antes != pressed /\ the_coffee_request_button = pressed /\ the_request_timer <= 30.0
- **Initial State:** Não especificado
- **Inputs:** the_system_mode, the_coin_sensor, the_coin_sensor_antes, the_coffee_request_button, the_coffee_request_button_antes, the_request_timer
- **Conditions:** the_system_mode = choice /\ the_coin_sensor = false /\ the_coin_sensor_antes = false /\ the_coffee_request_button_antes != pressed /\ the_coffee_request_button = pressed /\ the_request_timer <= 30.0
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_request_timer := 0, the_system_mode := preparing_weak
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_request_timer recebe 0; the_system_mode recebe preparing_weak
- **Rationale:** When the system mode is choice, and the coin sensor is false, and the coin sensor was false, and the coffee request button changes to pressed, and the request timer is lower than or equal to 30.0, the coffee machine system shall: reset the request timer, assign preparing weak coffee to the system mode.
- **Source Reference:** exemplos/vm-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa., A semântica do estado anterior depende da transição documentada no texto original.

### ORC-003 - vm#3
- **Preconditions:** the_system_mode = choice /\ the_coin_sensor = false /\ the_coin_sensor_antes = false /\ the_coffee_request_button_antes != pressed /\ the_coffee_request_button = pressed /\ the_request_timer > 30.0
- **Initial State:** Não especificado
- **Inputs:** the_system_mode, the_coin_sensor, the_coin_sensor_antes, the_coffee_request_button, the_coffee_request_button_antes, the_request_timer
- **Conditions:** the_system_mode = choice /\ the_coin_sensor = false /\ the_coin_sensor_antes = false /\ the_coffee_request_button_antes != pressed /\ the_coffee_request_button = pressed /\ the_request_timer > 30.0
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_request_timer := 0, the_system_mode := preparing_strong
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_request_timer recebe 0; the_system_mode recebe preparing_strong
- **Rationale:** When the system mode is choice, and the coin sensor is false, and the coin sensor was false, and the coffee request button changes to pressed, and the request timer is greater than 30.0, the coffee machine system shall: reset the request timer, assign preparing strong coffee to the system mode.
- **Source Reference:** exemplos/vm-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa., A semântica do estado anterior depende da transição documentada no texto original.

### ORC-004 - vm#4
- **Preconditions:** the_system_mode = preparing_weak /\ the_request_timer >= 10.0 /\ the_request_timer <= 30.0
- **Initial State:** Não especificado
- **Inputs:** the_system_mode, the_request_timer
- **Conditions:** the_system_mode = preparing_weak /\ the_request_timer >= 10.0 /\ the_request_timer <= 30.0
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_system_mode := idle, the_coffee_machine_output := weak
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_system_mode recebe idle; the_coffee_machine_output recebe weak
- **Rationale:** When the system mode is preparing weak coffee, and the request timer is greater than or equal to 10.0, and the request timer is lower than or equal to 30.0, the coffee machine system shall: assign idle to the system mode, assign weak to the coffee machine output.
- **Source Reference:** exemplos/vm-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa.

### ORC-005 - vm#5
- **Preconditions:** the_system_mode = preparing_strong /\ the_request_timer >= 30.0 /\ the_request_timer <= 50.0
- **Initial State:** Não especificado
- **Inputs:** the_system_mode, the_request_timer
- **Conditions:** the_system_mode = preparing_strong /\ the_request_timer >= 30.0 /\ the_request_timer <= 50.0
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_system_mode := idle, the_coffee_machine_output := strong
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_system_mode recebe idle; the_coffee_machine_output recebe strong
- **Rationale:** When the system mode is preparing strong coffee, and the request timer is greater than or equal to 30.0, and the request timer is lower than or equal to 50.0, the coffee machine system shall : assign idle to the system mode , assign strong to the coffee machine output.
- **Source Reference:** exemplos/vm-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa.

### ORC-006 - tis#1
- **Preconditions:** the_voltage_antes > 80 /\ the_voltage <= 80
- **Initial State:** Não especificado
- **Inputs:** the_voltage, the_voltage_antes
- **Conditions:** the_voltage_antes > 80 /\ the_voltage <= 80
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_indication_lights := off, the_flashing_timer := 0
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_indication_lights recebe off; the_flashing_timer recebe 0
- **Rationale:** When the voltage becomes lower than or equal to 80, the lights controller component shall: Assign off to the indication lights, Reset the flashing timer.
- **Source Reference:** exemplos/tis-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa., A semântica do estado anterior depende da transição documentada no texto original.

### ORC-007 - tis#2
- **Preconditions:** ((the_voltage_antes <= 80 /\ the_voltage > 80) \/ (the_flashing_mode_antes != left_flashing /\ the_flashing_mode = left_flashing)) /\ the_voltage > 80 /\ the_flashing_mode = left_flashing
- **Initial State:** Não especificado
- **Inputs:** the_voltage, the_voltage_antes, the_flashing_mode, the_flashing_mode_antes
- **Conditions:** ((the_voltage_antes <= 80 /\ the_voltage > 80) \/ (the_flashing_mode_antes != left_flashing /\ the_flashing_mode = left_flashing)) /\ the_voltage > 80 /\ the_flashing_mode = left_flashing
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_indication_lights := left_flashing, the_flashing_timer := 0
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_indication_lights recebe left_flashing; the_flashing_timer recebe 0
- **Rationale:** When the voltage becomes greater than 80 or the flashing mode becomes left flashing, and the voltage is greater than 80, and the flashing mode is left flashing, the lights controller component shall: Assign left flashing to the indication lights, Reset the flashing timer.
- **Source Reference:** exemplos/tis-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa., A semântica do estado anterior depende da transição documentada no texto original.

### ORC-008 - tis#3
- **Preconditions:** ((the_voltage_antes <= 80 /\ the_voltage > 80) \/ (the_flashing_mode_antes != right_flashing /\ the_flashing_mode = right_flashing)) /\ the_voltage > 80 /\ the_flashing_mode = right_flashing
- **Initial State:** Não especificado
- **Inputs:** the_voltage, the_voltage_antes, the_flashing_mode, the_flashing_mode_antes
- **Conditions:** ((the_voltage_antes <= 80 /\ the_voltage > 80) \/ (the_flashing_mode_antes != right_flashing /\ the_flashing_mode = right_flashing)) /\ the_voltage > 80 /\ the_flashing_mode = right_flashing
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_indication_lights := right_flashing, the_flashing_timer := 0
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_indication_lights recebe right_flashing; the_flashing_timer recebe 0
- **Rationale:** When the voltage becomes greater than 80 or the flashing mode becomes right flashing, and the voltage is greater than 80, and the flashing mode is right flashing, the lights controller component shall: Assign right flashing to the indication lights, Reset the flashing timer.
- **Source Reference:** exemplos/tis-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa., A semântica do estado anterior depende da transição documentada no texto original.

### ORC-009 - tis#4
- **Preconditions:** ((the_voltage_antes <= 80 /\ the_voltage > 80) \/ (the_flashing_mode_antes != both_flashing /\ the_flashing_mode = both_flashing)) /\ the_voltage > 80 /\ the_flashing_mode = both_flashing
- **Initial State:** Não especificado
- **Inputs:** the_voltage, the_voltage_antes, the_flashing_mode, the_flashing_mode_antes
- **Conditions:** ((the_voltage_antes <= 80 /\ the_voltage > 80) \/ (the_flashing_mode_antes != both_flashing /\ the_flashing_mode = both_flashing)) /\ the_voltage > 80 /\ the_flashing_mode = both_flashing
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_indication_lights := both_flashing, the_flashing_timer := 0
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_indication_lights recebe both_flashing; the_flashing_timer recebe 0
- **Rationale:** When the voltage becomes greater than 80 or the flashing mode becomes both flashing, and the voltage is greater than 80, and the flashing mode is both flashing, the lights controller component shall: Assign both flashing to the indication lights, Reset the flashing timer.
- **Source Reference:** exemplos/tis-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa., A semântica do estado anterior depende da transição documentada no texto original.

### ORC-010 - tis#5
- **Preconditions:** the_voltage > 80 /\ the_flashing_mode = no_flashing
- **Initial State:** Não especificado
- **Inputs:** the_voltage, the_flashing_mode
- **Conditions:** the_voltage > 80 /\ the_flashing_mode = no_flashing
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_indication_lights := off, the_flashing_timer := 0
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_indication_lights recebe off; the_flashing_timer recebe 0
- **Rationale:** When the voltage is greater than 80, and the flashing mode is no flashing, the lights controller component shall: Assign off to the indication lights, Reset the flashing timer.
- **Source Reference:** exemplos/tis-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa.

### ORC-011 - tis#6
- **Preconditions:** the_voltage > 80 /\ the_flashing_timer >= 340 /\ (the_indication_lights = left_flashing \/ the_indication_lights = right_flashing)
- **Initial State:** Não especificado
- **Inputs:** the_voltage, the_indication_lights, the_flashing_timer
- **Conditions:** the_voltage > 80 /\ the_flashing_timer >= 340 /\ (the_indication_lights = left_flashing \/ the_indication_lights = right_flashing)
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_indication_lights := off, the_flashing_timer := 0
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_indication_lights recebe off; the_flashing_timer recebe 0
- **Rationale:** When the voltage is greater than 80, and the flashing timer is greater than or equal to 340, and the indication lights are left flashing or the indication lights are right flashing, the lights controller component shall: Assign off to the indication lights, Reset the flashing timer.
- **Source Reference:** exemplos/tis-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa.

### ORC-012 - tis#7
- **Preconditions:** the_voltage > 80 /\ the_flashing_timer >= 220 /\ the_indication_lights = off /\ the_flashing_mode = left_flashing
- **Initial State:** Não especificado
- **Inputs:** the_voltage, the_flashing_mode, the_indication_lights, the_flashing_timer
- **Conditions:** the_voltage > 80 /\ the_flashing_timer >= 220 /\ the_indication_lights = off /\ the_flashing_mode = left_flashing
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_indication_lights := left_flashing, the_flashing_timer := 0
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_indication_lights recebe left_flashing; the_flashing_timer recebe 0
- **Rationale:** When the voltage is greater than 80, and the flashing timer is greater than or equal to 220, and the indication lights are off, and the flashing mode is left flashing, the lights controller component shall: Assign left flashing to the indication lights, Reset the flashing timer.
- **Source Reference:** exemplos/tis-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa.

### ORC-013 - tis#8
- **Preconditions:** the_voltage > 80 /\ the_flashing_timer >= 220 /\ the_indication_lights = off /\ the_flashing_mode = right_flashing
- **Initial State:** Não especificado
- **Inputs:** the_voltage, the_flashing_mode, the_indication_lights, the_flashing_timer
- **Conditions:** the_voltage > 80 /\ the_flashing_timer >= 220 /\ the_indication_lights = off /\ the_flashing_mode = right_flashing
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_indication_lights := right_flashing, the_flashing_timer := 0
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_indication_lights recebe right_flashing; the_flashing_timer recebe 0
- **Rationale:** When the voltage is greater than 80, and the flashing timer is greater than or equal to 220, and the indication lights are off, and the flashing mode is right flashing, the lights controller component shall: Assign right flashing to the indication lights, Reset the flashing timer.
- **Source Reference:** exemplos/tis-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa.

### ORC-014 - tis#9
- **Preconditions:** the_voltage > 80 /\ the_flashing_timer >= 220 /\ the_indication_lights = off /\ the_flashing_mode = both_flashing
- **Initial State:** Não especificado
- **Inputs:** the_voltage, the_flashing_mode, the_indication_lights, the_flashing_timer
- **Conditions:** the_voltage > 80 /\ the_flashing_timer >= 220 /\ the_indication_lights = off /\ the_flashing_mode = both_flashing
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_indication_lights := both_flashing, the_flashing_timer := 0
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_indication_lights recebe both_flashing; the_flashing_timer recebe 0
- **Rationale:** When the voltage is greater than 80, and the flashing timer is greater than or equal to 220, and the indication lights are off, and the flashing mode is both flashing, the lights controller component shall: Assign both flashing to the indication lights, Reset the flashing timer.
- **Source Reference:** exemplos/tis-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa.

### ORC-015 - tis#10
- **Preconditions:** the_turn_indicator_lever_antes != left /\ the_turn_indicator_lever = left /\ the_emergency_flashing = off
- **Initial State:** Não especificado
- **Inputs:** the_turn_indicator_lever, the_turn_indicator_lever_antes, the_emergency_flashing
- **Conditions:** the_turn_indicator_lever_antes != left /\ the_turn_indicator_lever = left /\ the_emergency_flashing = off
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_flashing_mode := left_flashing, the_flashing_timer := 0
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_flashing_mode recebe left_flashing; the_flashing_timer recebe 0
- **Rationale:** When the turn indicator lever changes to the left position, and the emergency flashing is off, the flashing mode component shall: assign left flashing to the flashing mode, Reset the flashing timer.
- **Source Reference:** exemplos/tis-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa., A semântica do estado anterior depende da transição documentada no texto original.

### ORC-016 - tis#11
- **Preconditions:** the_turn_indicator_lever_antes != right /\ the_turn_indicator_lever = right /\ the_emergency_flashing = off
- **Initial State:** Não especificado
- **Inputs:** the_turn_indicator_lever, the_turn_indicator_lever_antes, the_emergency_flashing
- **Conditions:** the_turn_indicator_lever_antes != right /\ the_turn_indicator_lever = right /\ the_emergency_flashing = off
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_flashing_mode := right_flashing, the_flashing_timer := 0
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_flashing_mode recebe right_flashing; the_flashing_timer recebe 0
- **Rationale:** When the turn indicator lever changes to the right position, and the emergency flashing is off, the flashing mode component shall: assign right flashing to the flashing mode, Reset the flashing timer.
- **Source Reference:** exemplos/tis-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa., A semântica do estado anterior depende da transição documentada no texto original.

### ORC-017 - tis#12
- **Preconditions:** the_emergency_flashing_antes != on /\ the_emergency_flashing = on
- **Initial State:** Não especificado
- **Inputs:** the_emergency_flashing, the_emergency_flashing_antes
- **Conditions:** the_emergency_flashing_antes != on /\ the_emergency_flashing = on
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_flashing_mode := both_flashing, the_flashing_timer := 0
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_flashing_mode recebe both_flashing; the_flashing_timer recebe 0
- **Rationale:** When the emergency flashing becomes on, the flashing mode component shall: assign both flashing to the flashing mode, Reset the flashing timer.
- **Source Reference:** exemplos/tis-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa., A semântica do estado anterior depende da transição documentada no texto original.

### ORC-018 - tis#13
- **Preconditions:** the_emergency_flashing = on /\ the_emergency_flashing_antes = on /\ the_turn_indicator_lever_antes != left /\ the_turn_indicator_lever = left
- **Initial State:** Não especificado
- **Inputs:** the_turn_indicator_lever, the_turn_indicator_lever_antes, the_emergency_flashing, the_emergency_flashing_antes
- **Conditions:** the_emergency_flashing = on /\ the_emergency_flashing_antes = on /\ the_turn_indicator_lever_antes != left /\ the_turn_indicator_lever = left
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_flashing_mode := left_flashing, the_flashing_timer := 0
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_flashing_mode recebe left_flashing; the_flashing_timer recebe 0
- **Rationale:** When the emergency flashing is on, and the emergency flashing was on, and the turn indicator lever changes to the left position, the flashing mode component shall: assign left flashing to the flashing mode, Reset the flashing timer.
- **Source Reference:** exemplos/tis-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa., A semântica do estado anterior depende da transição documentada no texto original.

### ORC-019 - tis#14
- **Preconditions:** the_emergency_flashing = on /\ the_emergency_flashing_antes = on /\ the_turn_indicator_lever_antes != right /\ the_turn_indicator_lever = right
- **Initial State:** Não especificado
- **Inputs:** the_turn_indicator_lever, the_turn_indicator_lever_antes, the_emergency_flashing, the_emergency_flashing_antes
- **Conditions:** the_emergency_flashing = on /\ the_emergency_flashing_antes = on /\ the_turn_indicator_lever_antes != right /\ the_turn_indicator_lever = right
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_flashing_mode := right_flashing, the_flashing_timer := 0
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_flashing_mode recebe right_flashing; the_flashing_timer recebe 0
- **Rationale:** When the emergency flashing is on, and the emergency flashing was on, and the turn indicator lever changes to the right position, the flashing mode component shall: assign right flashing to the flashing mode, Reset the flashing timer.
- **Source Reference:** exemplos/tis-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa., A semântica do estado anterior depende da transição documentada no texto original.

### ORC-020 - tis#15
- **Preconditions:** the_emergency_flashing = on /\ the_emergency_flashing_antes = on /\ the_turn_indicator_lever_antes != idle /\ the_turn_indicator_lever = idle /\ the_flashing_mode != both_flashing
- **Initial State:** Não especificado
- **Inputs:** the_flashing_mode, the_turn_indicator_lever, the_turn_indicator_lever_antes, the_emergency_flashing, the_emergency_flashing_antes
- **Conditions:** the_emergency_flashing = on /\ the_emergency_flashing_antes = on /\ the_turn_indicator_lever_antes != idle /\ the_turn_indicator_lever = idle /\ the_flashing_mode != both_flashing
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_flashing_mode := both_flashing, the_flashing_timer := 0
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_flashing_mode recebe both_flashing; the_flashing_timer recebe 0
- **Rationale:** When the emergency flashing is on, and the emergency flashing was on, and the turn indicator lever changes to the idle position, and the flashing mode is not both flashing, the flashing mode component shall: assign both flashing to the flashing mode, Reset the flashing timer.
- **Source Reference:** exemplos/tis-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa., A semântica do estado anterior depende da transição documentada no texto original.

### ORC-021 - tis#16
- **Preconditions:** the_emergency_flashing_antes != off /\ the_emergency_flashing = off /\ the_turn_indicator_lever = left /\ the_turn_indicator_lever_antes = left /\ the_flashing_mode != left_flashing
- **Initial State:** Não especificado
- **Inputs:** the_flashing_mode, the_turn_indicator_lever, the_turn_indicator_lever_antes, the_emergency_flashing, the_emergency_flashing_antes
- **Conditions:** the_emergency_flashing_antes != off /\ the_emergency_flashing = off /\ the_turn_indicator_lever = left /\ the_turn_indicator_lever_antes = left /\ the_flashing_mode != left_flashing
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_flashing_mode := left_flashing, the_flashing_timer := 0
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_flashing_mode recebe left_flashing; the_flashing_timer recebe 0
- **Rationale:** When the emergency flashing becomes off, and the turn indicator lever is on the left position, and the turn indicator lever was on the left position, and the flashing mode is not left flashing, the flashing mode component shall: assign left flashing to the flashing mode, Reset the flashing timer.
- **Source Reference:** exemplos/tis-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa., A semântica do estado anterior depende da transição documentada no texto original.

### ORC-022 - tis#17
- **Preconditions:** the_emergency_flashing_antes != off /\ the_emergency_flashing = off /\ the_turn_indicator_lever = right /\ the_turn_indicator_lever_antes = right /\ the_flashing_mode != right_flashing
- **Initial State:** Não especificado
- **Inputs:** the_flashing_mode, the_turn_indicator_lever, the_turn_indicator_lever_antes, the_emergency_flashing, the_emergency_flashing_antes
- **Conditions:** the_emergency_flashing_antes != off /\ the_emergency_flashing = off /\ the_turn_indicator_lever = right /\ the_turn_indicator_lever_antes = right /\ the_flashing_mode != right_flashing
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_flashing_mode := right_flashing, the_flashing_timer := 0
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_flashing_mode recebe right_flashing; the_flashing_timer recebe 0
- **Rationale:** When the emergency flashing becomes off, and the turn indicator lever is on the right position, and the turn indicator lever was on the right position, and the flashing mode is not right flashing, the flashing mode component shall: assign right flashing to the flashing mode, Reset the flashing timer.
- **Source Reference:** exemplos/tis-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa., A semântica do estado anterior depende da transição documentada no texto original.

### ORC-023 - npp#1
- **Preconditions:** the_water_pressure_antes < 9 /\ the_water_pressure >= 9 /\ the_pressure_mode = low
- **Initial State:** Não especificado
- **Inputs:** the_water_pressure, the_water_pressure_antes, the_pressure_mode
- **Conditions:** the_water_pressure_antes < 9 /\ the_water_pressure >= 9 /\ the_pressure_mode = low
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_pressure_mode := permitted
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_pressure_mode recebe permitted
- **Rationale:** When the water pressure becomes greater than or equal to 9, and the pressure mode is low, the Safety Injection System shall assign permitted to the pressure mode.
- **Source Reference:** exemplos/npp-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa., A semântica do estado anterior depende da transição documentada no texto original.

### ORC-024 - npp#2
- **Preconditions:** the_water_pressure_antes < 10 /\ the_water_pressure >= 10 /\ the_pressure_mode = permitted
- **Initial State:** Não especificado
- **Inputs:** the_water_pressure, the_water_pressure_antes, the_pressure_mode
- **Conditions:** the_water_pressure_antes < 10 /\ the_water_pressure >= 10 /\ the_pressure_mode = permitted
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_pressure_mode := high
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_pressure_mode recebe high
- **Rationale:** When the water pressure becomes greater than or equal to 10, and the pressure mode is permitted, the Safety Injection System shall assign high to the pressure mode.
- **Source Reference:** exemplos/npp-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa., A semântica do estado anterior depende da transição documentada no texto original.

### ORC-025 - npp#3
- **Preconditions:** the_water_pressure_antes >= 9 /\ the_water_pressure < 9 /\ the_pressure_mode = permitted
- **Initial State:** Não especificado
- **Inputs:** the_water_pressure, the_water_pressure_antes, the_pressure_mode
- **Conditions:** the_water_pressure_antes >= 9 /\ the_water_pressure < 9 /\ the_pressure_mode = permitted
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_pressure_mode := low
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_pressure_mode recebe low
- **Rationale:** When the water pressure becomes lower than 9, and the pressure mode is permitted, the Safety Injection System shall assign low to the pressure mode.
- **Source Reference:** exemplos/npp-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa., A semântica do estado anterior depende da transição documentada no texto original.

### ORC-026 - npp#4
- **Preconditions:** the_water_pressure_antes >= 10 /\ the_water_pressure < 10 /\ the_pressure_mode = high
- **Initial State:** Não especificado
- **Inputs:** the_water_pressure, the_water_pressure_antes, the_pressure_mode
- **Conditions:** the_water_pressure_antes >= 10 /\ the_water_pressure < 10 /\ the_pressure_mode = high
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_pressure_mode := permitted
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_pressure_mode recebe permitted
- **Rationale:** When the water pressure becomes lower than 10, and the pressure mode is high, the Safety Injection System shall assign permitted to the pressure mode.
- **Source Reference:** exemplos/npp-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa., A semântica do estado anterior depende da transição documentada no texto original.

### ORC-027 - npp#5
- **Preconditions:** the_blockage_button_antes != pressed /\ the_blockage_button = pressed /\ the_reset_button != pressed /\ the_pressure_mode != high
- **Initial State:** Não especificado
- **Inputs:** the_pressure_mode, the_blockage_button, the_blockage_button_antes, the_reset_button
- **Conditions:** the_blockage_button_antes != pressed /\ the_blockage_button = pressed /\ the_reset_button != pressed /\ the_pressure_mode != high
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_overridden_mode := true
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_overridden_mode recebe true
- **Rationale:** When the blockage button becomes pressed, and the reset button is not pressed, and the pressure mode is not high, the Safety Injection System shall assign true to the overridden mode.
- **Source Reference:** exemplos/npp-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa., A semântica do estado anterior depende da transição documentada no texto original.

### ORC-028 - npp#6
- **Preconditions:** the_reset_button_antes != pressed /\ the_reset_button = pressed /\ the_pressure_mode != high
- **Initial State:** Não especificado
- **Inputs:** the_pressure_mode, the_reset_button, the_reset_button_antes
- **Conditions:** the_reset_button_antes != pressed /\ the_reset_button = pressed /\ the_pressure_mode != high
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_overridden_mode := false
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_overridden_mode recebe false
- **Rationale:** When the reset button becomes pressed, and the pressure mode is not high, the Safety Injection System shall assign false to the overridden mode.
- **Source Reference:** exemplos/npp-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa., A semântica do estado anterior depende da transição documentada no texto original.

### ORC-029 - npp#7
- **Preconditions:** the_pressure_mode_antes != high /\ the_pressure_mode = high
- **Initial State:** Não especificado
- **Inputs:** the_pressure_mode, the_pressure_mode_antes
- **Conditions:** the_pressure_mode_antes != high /\ the_pressure_mode = high
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_overridden_mode := false
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_overridden_mode recebe false
- **Rationale:** When the pressure mode becomes high, the Safety Injection System shall assign false to the overridden mode.
- **Source Reference:** exemplos/npp-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa., A semântica do estado anterior depende da transição documentada no texto original.

### ORC-030 - npp#8
- **Preconditions:** the_pressure_mode_antes = high /\ the_pressure_mode != high
- **Initial State:** Não especificado
- **Inputs:** the_pressure_mode, the_pressure_mode_antes
- **Conditions:** the_pressure_mode_antes = high /\ the_pressure_mode != high
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_overridden_mode := false
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_overridden_mode recebe false
- **Rationale:** When the pressure mode becomes not high, the Safety Injection System shall assign false to the overridden mode.
- **Source Reference:** exemplos/npp-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa., A semântica do estado anterior depende da transição documentada no texto original.

### ORC-031 - npp#9
- **Preconditions:** the_pressure_mode = low /\ the_overridden_mode = true
- **Initial State:** Não especificado
- **Inputs:** the_pressure_mode, the_overridden_mode
- **Conditions:** the_pressure_mode = low /\ the_overridden_mode = true
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_safety_injection_mode := off
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_safety_injection_mode recebe off
- **Rationale:** When the pressure mode is low, and the overridden mode is true, the Safety Injection System shall assign off to the safety injection mode.
- **Source Reference:** exemplos/npp-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa.

### ORC-032 - npp#10
- **Preconditions:** the_pressure_mode = low /\ the_overridden_mode = false
- **Initial State:** Não especificado
- **Inputs:** the_pressure_mode, the_overridden_mode
- **Conditions:** the_pressure_mode = low /\ the_overridden_mode = false
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_safety_injection_mode := on
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_safety_injection_mode recebe on
- **Rationale:** When the pressure mode is low, and the overridden mode is false, the Safety Injection System shall assign on to the safety injection mode.
- **Source Reference:** exemplos/npp-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa.

### ORC-033 - npp#11
- **Preconditions:** the_pressure_mode = permitted \/ the_pressure_mode = high
- **Initial State:** Não especificado
- **Inputs:** the_pressure_mode
- **Conditions:** the_pressure_mode = permitted \/ the_pressure_mode = high
- **Trigger/Event:** When
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** the_safety_injection_mode := off
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** the_safety_injection_mode recebe off
- **Rationale:** When the pressure mode is permitted or the pressure mode is high, the Safety Injection System shall assign off to the safety injection mode.
- **Source Reference:** exemplos/npp-decisoes.json
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa.

### ORC-034 - generic-REQ-001
- **Preconditions:** (alarme_ativo and porta_aberta) or botao_emergencia
- **Initial State:** Não especificado
- **Inputs:** alarme_ativo, botao_emergencia, p, ta_aberta
- **Conditions:** (alarme_ativo and porta_aberta) or botao_emergencia
- **Trigger/Event:** (alarme_ativo and porta_aberta) or botao_emergencia
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** Nenhuma ação explicitamente documentada
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** Não especificado
- **Rationale:** (alarme_ativo and porta_aberta) or botao_emergencia
- **Source Reference:** exemplos/requisitos.mcdc
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa., Domínio das variáveis não informado no arquivo .mcdc.

### ORC-035 - generic-REQ-002
- **Preconditions:** porta_fechada and not obstaculo
- **Initial State:** Não especificado
- **Inputs:** obstaculo, p, ta_fechada
- **Conditions:** porta_fechada and not obstaculo
- **Trigger/Event:** porta_fechada and not obstaculo
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** Nenhuma ação explicitamente documentada
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** Não especificado
- **Rationale:** porta_fechada and not obstaculo
- **Source Reference:** exemplos/requisitos.mcdc
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa., Domínio das variáveis não informado no arquivo .mcdc.

### ORC-036 - generic-REQ-003
- **Preconditions:** freio_acionado or (freio_acionado and pedal_pressionado)
- **Initial State:** Não especificado
- **Inputs:** freio_acionado, pedal_pressionado
- **Conditions:** freio_acionado or (freio_acionado and pedal_pressionado)
- **Trigger/Event:** freio_acionado or (freio_acionado and pedal_pressionado)
- **Expected Decision:** verdadeiro quando a guarda é satisfeita
- **Expected Action:** Nenhuma ação explicitamente documentada
- **Expected Output:** Não especificado além das ações explícitas
- **Expected State:** Não especificado
- **Rationale:** freio_acionado or (freio_acionado and pedal_pressionado)
- **Source Reference:** exemplos/requisitos.mcdc
- **Uncertainties:** Estado inicial não especificado independentemente da guarda., Saída não especificada fora das ações explícitas., Implementação e comportamento executável não consultados nesta etapa., Domínio das variáveis não informado no arquivo .mcdc.

