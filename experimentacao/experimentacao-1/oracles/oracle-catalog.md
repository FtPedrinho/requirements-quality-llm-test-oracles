# Catalogo de oráculos - Experimento 1

Os oraculos foram gerados exclusivamente a partir de `requirements/experimental/`. Nenhum resultado Z3 foi usado para induzir expectativas.

| Oracle ID | Sistema | Requirement ID | Decision ID | Condição de execução | Confiança | Ressalva |
|---|---|---|---|---|---|---|
| E1-ORC-001 | the_coffee_machine_system | REQ001 | vm#1 | the_system_mode = idle /\ the_coin_sensor_antes = false /\ the_coin_sensor = true | documentado | Nenhuma |
| E1-ORC-002 | the_coffee_machine_system | REQ002 | vm#2 | the_system_mode = choice /\ the_coin_sensor = false /\ the_coin_sensor_antes = false /\ the_coffee_request_button_antes != pressed /\ the_coffee_request_button = pressed /\ the_request_timer <= 30.0 | documentado | Nenhuma |
| E1-ORC-003 | the_coffee_machine_system | REQ003 | vm#3 | the_system_mode = choice /\ the_coin_sensor = false /\ the_coin_sensor_antes = false /\ the_coffee_request_button_antes != pressed /\ the_coffee_request_button = pressed /\ the_request_timer > 30.0 | documentado | Nenhuma |
| E1-ORC-004 | the_coffee_machine_system | REQ004 | vm#4 | the_system_mode = preparing_weak /\ the_request_timer >= 10.0 /\ the_request_timer <= 30.0 | documentado | Nenhuma |
| E1-ORC-005 | the_coffee_machine_system | REQ005 | vm#5 | the_system_mode = preparing_strong /\ the_request_timer >= 30.0 /\ the_request_timer <= 50.0 | documentado | Nenhuma |
| E1-ORC-006 | turn_indicator_system | REQ001 | tis#1 | the_voltage_antes > 80 /\ the_voltage <= 80 | documentado | Nenhuma |
| E1-ORC-007 | turn_indicator_system | REQ002 | tis#2 | ((the_voltage_antes <= 80 /\ the_voltage > 80) \/ (the_flashing_mode_antes != left_flashing /\ the_flashing_mode = left_flashing)) /\ the_voltage > 80 /\ the_flashing_mode = left_flashing | documentado-com-ressalva | RESSALVA-TIS-NPP |
| E1-ORC-008 | turn_indicator_system | REQ003 | tis#3 | ((the_voltage_antes <= 80 /\ the_voltage > 80) \/ (the_flashing_mode_antes != right_flashing /\ the_flashing_mode = right_flashing)) /\ the_voltage > 80 /\ the_flashing_mode = right_flashing | documentado-com-ressalva | RESSALVA-TIS-NPP |
| E1-ORC-009 | turn_indicator_system | REQ004 | tis#4 | ((the_voltage_antes <= 80 /\ the_voltage > 80) \/ (the_flashing_mode_antes != both_flashing /\ the_flashing_mode = both_flashing)) /\ the_voltage > 80 /\ the_flashing_mode = both_flashing | documentado-com-ressalva | RESSALVA-TIS-NPP |
| E1-ORC-010 | turn_indicator_system | REQ005 | tis#5 | the_voltage > 80 /\ the_flashing_mode = no_flashing | documentado | Nenhuma |
| E1-ORC-011 | turn_indicator_system | REQ006 | tis#6 | the_voltage > 80 /\ the_flashing_timer >= 340 /\ (the_indication_lights = left_flashing \/ the_indication_lights = right_flashing) | documentado-com-ressalva | RESSALVA-TIS-NPP |
| E1-ORC-012 | turn_indicator_system | REQ007 | tis#7 | the_voltage > 80 /\ the_flashing_timer >= 220 /\ the_indication_lights = off /\ the_flashing_mode = left_flashing | documentado | Nenhuma |
| E1-ORC-013 | turn_indicator_system | REQ008 | tis#8 | the_voltage > 80 /\ the_flashing_timer >= 220 /\ the_indication_lights = off /\ the_flashing_mode = right_flashing | documentado | Nenhuma |
| E1-ORC-014 | turn_indicator_system | REQ009 | tis#9 | the_voltage > 80 /\ the_flashing_timer >= 220 /\ the_indication_lights = off /\ the_flashing_mode = both_flashing | documentado | Nenhuma |
| E1-ORC-015 | turn_indicator_system | REQ010 | tis#10 | the_turn_indicator_lever_antes != left /\ the_turn_indicator_lever = left /\ the_emergency_flashing = off | documentado | Nenhuma |
| E1-ORC-016 | turn_indicator_system | REQ011 | tis#11 | the_turn_indicator_lever_antes != right /\ the_turn_indicator_lever = right /\ the_emergency_flashing = off | documentado | Nenhuma |
| E1-ORC-017 | turn_indicator_system | REQ012 | tis#12 | the_emergency_flashing_antes != on /\ the_emergency_flashing = on | documentado | Nenhuma |
| E1-ORC-018 | turn_indicator_system | REQ013 | tis#13 | the_emergency_flashing = on /\ the_emergency_flashing_antes = on /\ the_turn_indicator_lever_antes != left /\ the_turn_indicator_lever = left | documentado | Nenhuma |
| E1-ORC-019 | turn_indicator_system | REQ014 | tis#14 | the_emergency_flashing = on /\ the_emergency_flashing_antes = on /\ the_turn_indicator_lever_antes != right /\ the_turn_indicator_lever = right | documentado | Nenhuma |
| E1-ORC-020 | turn_indicator_system | REQ015 | tis#15 | the_emergency_flashing = on /\ the_emergency_flashing_antes = on /\ the_turn_indicator_lever_antes != idle /\ the_turn_indicator_lever = idle /\ the_flashing_mode != both_flashing | documentado | Nenhuma |
| E1-ORC-021 | turn_indicator_system | REQ016 | tis#16 | the_emergency_flashing_antes != off /\ the_emergency_flashing = off /\ the_turn_indicator_lever = left /\ the_turn_indicator_lever_antes = left /\ the_flashing_mode != left_flashing | documentado | Nenhuma |
| E1-ORC-022 | turn_indicator_system | REQ017 | tis#17 | the_emergency_flashing_antes != off /\ the_emergency_flashing = off /\ the_turn_indicator_lever = right /\ the_turn_indicator_lever_antes = right /\ the_flashing_mode != right_flashing | documentado | Nenhuma |
| E1-ORC-023 | safety_injection_system | REQ001 | npp#1 | the_water_pressure_antes < 9 /\ the_water_pressure >= 9 /\ the_pressure_mode = low | documentado | Nenhuma |
| E1-ORC-024 | safety_injection_system | REQ002 | npp#2 | the_water_pressure_antes < 10 /\ the_water_pressure >= 10 /\ the_pressure_mode = permitted | documentado | Nenhuma |
| E1-ORC-025 | safety_injection_system | REQ003 | npp#3 | the_water_pressure_antes >= 9 /\ the_water_pressure < 9 /\ the_pressure_mode = permitted | documentado | Nenhuma |
| E1-ORC-026 | safety_injection_system | REQ004 | npp#4 | the_water_pressure_antes >= 10 /\ the_water_pressure < 10 /\ the_pressure_mode = high | documentado | Nenhuma |
| E1-ORC-027 | safety_injection_system | REQ005 | npp#5 | the_blockage_button_antes != pressed /\ the_blockage_button = pressed /\ the_reset_button != pressed /\ the_pressure_mode != high | documentado-com-ressalva | RESSALVA-TIS-NPP |
| E1-ORC-028 | safety_injection_system | REQ006 | npp#6 | the_reset_button_antes != pressed /\ the_reset_button = pressed /\ the_pressure_mode != high | documentado | Nenhuma |
| E1-ORC-029 | safety_injection_system | REQ007 | npp#7 | the_pressure_mode_antes != high /\ the_pressure_mode = high | documentado | Nenhuma |
| E1-ORC-030 | safety_injection_system | REQ008 | npp#8 | the_pressure_mode_antes = high /\ the_pressure_mode != high | documentado-com-ressalva | RESSALVA-TIS-NPP |
| E1-ORC-031 | safety_injection_system | REQ009 | npp#9 | the_pressure_mode = low /\ the_overridden_mode = true | parcialmente-especificado | RESSALVA-NPP-OUTPUT |
| E1-ORC-032 | safety_injection_system | REQ010 | npp#10 | the_pressure_mode = low /\ the_overridden_mode = false | parcialmente-especificado | RESSALVA-NPP-OUTPUT |
| E1-ORC-033 | safety_injection_system | REQ011 | npp#11 | the_pressure_mode = permitted \/ the_pressure_mode = high | parcialmente-especificado | RESSALVA-NPP-OUTPUT |
| E1-ORC-034 | generic | REQ-001 | REQ-001 | (alarme_ativo and porta_aberta) or botao_emergencia | documentado | Nenhuma |
| E1-ORC-035 | generic | REQ-002 | REQ-002 | porta_fechada and not obstaculo | documentado | Nenhuma |
| E1-ORC-036 | generic | REQ-003 | REQ-003 | freio_acionado or (freio_acionado and pedal_pressionado) | documentado | Nenhuma |

## Detalhes

### E1-ORC-001 - vm#1
- **System:** the_coffee_machine_system
- **Requirement ID:** REQ001
- **Source:** experimentacao/experimentacao-1/requirements/experimental/vm-decisoes.json
- **Execution Condition:** the_system_mode = idle /\ the_coin_sensor_antes = false /\ the_coin_sensor = true
- **Initial State:** Nao especificado
- **Inputs:** the_system_mode, the_coin_sensor, the_coin_sensor_antes
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_request_timer := 0, the_system_mode := choice
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the system mode is idle, and the coin sensor changes to true, the coffee machine system shall reset the request timer, assign choice to the system mode.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

### E1-ORC-002 - vm#2
- **System:** the_coffee_machine_system
- **Requirement ID:** REQ002
- **Source:** experimentacao/experimentacao-1/requirements/experimental/vm-decisoes.json
- **Execution Condition:** the_system_mode = choice /\ the_coin_sensor = false /\ the_coin_sensor_antes = false /\ the_coffee_request_button_antes != pressed /\ the_coffee_request_button = pressed /\ the_request_timer <= 30.0
- **Initial State:** Nao especificado
- **Inputs:** the_system_mode, the_coin_sensor, the_coin_sensor_antes, the_coffee_request_button, the_coffee_request_button_antes, the_request_timer
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_request_timer := 0, the_system_mode := preparing_weak
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the system mode is choice, and the coin sensor is false, and the coin sensor was false, and the coffee request button changes to pressed, and the request timer is lower than or equal to 30.0, the coffee machine system shall reset the request timer, assign preparing weak coffee to the system mode.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

### E1-ORC-003 - vm#3
- **System:** the_coffee_machine_system
- **Requirement ID:** REQ003
- **Source:** experimentacao/experimentacao-1/requirements/experimental/vm-decisoes.json
- **Execution Condition:** the_system_mode = choice /\ the_coin_sensor = false /\ the_coin_sensor_antes = false /\ the_coffee_request_button_antes != pressed /\ the_coffee_request_button = pressed /\ the_request_timer > 30.0
- **Initial State:** Nao especificado
- **Inputs:** the_system_mode, the_coin_sensor, the_coin_sensor_antes, the_coffee_request_button, the_coffee_request_button_antes, the_request_timer
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_request_timer := 0, the_system_mode := preparing_strong
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the system mode is choice, and the coin sensor is false, and the coin sensor was false, and the coffee request button changes to pressed, and the request timer is greater than 30.0, the coffee machine system shall reset the request timer, assign preparing strong coffee to the system mode.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

### E1-ORC-004 - vm#4
- **System:** the_coffee_machine_system
- **Requirement ID:** REQ004
- **Source:** experimentacao/experimentacao-1/requirements/experimental/vm-decisoes.json
- **Execution Condition:** the_system_mode = preparing_weak /\ the_request_timer >= 10.0 /\ the_request_timer <= 30.0
- **Initial State:** Nao especificado
- **Inputs:** the_system_mode, the_request_timer
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_system_mode := idle, the_coffee_machine_output := weak
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the system mode is preparing weak coffee, and the request timer is greater than or equal to 10.0, and the request timer is lower than or equal to 30.0, the coffee machine system shall assign idle to the system mode, assign weak to the coffee machine output.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

### E1-ORC-005 - vm#5
- **System:** the_coffee_machine_system
- **Requirement ID:** REQ005
- **Source:** experimentacao/experimentacao-1/requirements/experimental/vm-decisoes.json
- **Execution Condition:** the_system_mode = preparing_strong /\ the_request_timer >= 30.0 /\ the_request_timer <= 50.0
- **Initial State:** Nao especificado
- **Inputs:** the_system_mode, the_request_timer
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_system_mode := idle, the_coffee_machine_output := strong
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the system mode is preparing strong coffee, and the request timer is greater than or equal to 30.0, and the request timer is lower than or equal to 50.0, the coffee machine system shall assign idle to the system mode , assign strong to the coffee machine output.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

### E1-ORC-006 - tis#1
- **System:** turn_indicator_system
- **Requirement ID:** REQ001
- **Source:** experimentacao/experimentacao-1/requirements/experimental/tis-decisoes.json
- **Execution Condition:** the_voltage_antes > 80 /\ the_voltage <= 80
- **Initial State:** Nao especificado
- **Inputs:** the_voltage, the_voltage_antes
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_indication_lights := off, the_flashing_timer := 0
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the voltage becomes lower than or equal to 80, the lights controller component shall Assign off to the indication lights, reset the flashing timer.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

### E1-ORC-007 - tis#2
- **System:** turn_indicator_system
- **Requirement ID:** REQ002
- **Source:** experimentacao/experimentacao-1/requirements/experimental/tis-decisoes.json
- **Execution Condition:** ((the_voltage_antes <= 80 /\ the_voltage > 80) \/ (the_flashing_mode_antes != left_flashing /\ the_flashing_mode = left_flashing)) /\ the_voltage > 80 /\ the_flashing_mode = left_flashing
- **Initial State:** Nao especificado
- **Inputs:** the_voltage, the_voltage_antes, the_flashing_mode, the_flashing_mode_antes
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_indication_lights := left_flashing, the_flashing_timer := 0
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the voltage becomes greater than 80 or the flashing mode becomes left flashing, and the voltage is greater than 80, and the flashing mode is left flashing, the lights controller component shall Assign left flashing to the indication lights, reset the flashing timer.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos., O requisito participa de uma sobreposicao formal com acoes potencialmente conflitantes; alcançabilidade e prioridade nao foram confirmadas.
- **Confidence:** documentado-com-ressalva
- **Reserve:** RESSALVA-TIS-NPP

### E1-ORC-008 - tis#3
- **System:** turn_indicator_system
- **Requirement ID:** REQ003
- **Source:** experimentacao/experimentacao-1/requirements/experimental/tis-decisoes.json
- **Execution Condition:** ((the_voltage_antes <= 80 /\ the_voltage > 80) \/ (the_flashing_mode_antes != right_flashing /\ the_flashing_mode = right_flashing)) /\ the_voltage > 80 /\ the_flashing_mode = right_flashing
- **Initial State:** Nao especificado
- **Inputs:** the_voltage, the_voltage_antes, the_flashing_mode, the_flashing_mode_antes
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_indication_lights := right_flashing, the_flashing_timer := 0
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the voltage becomes greater than 80 or the flashing mode becomes right flashing, and the voltage is greater than 80, and the flashing mode is right flashing, the lights controller component shall Assign right flashing to the indication lights, reset the flashing timer.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos., O requisito participa de uma sobreposicao formal com acoes potencialmente conflitantes; alcançabilidade e prioridade nao foram confirmadas.
- **Confidence:** documentado-com-ressalva
- **Reserve:** RESSALVA-TIS-NPP

### E1-ORC-009 - tis#4
- **System:** turn_indicator_system
- **Requirement ID:** REQ004
- **Source:** experimentacao/experimentacao-1/requirements/experimental/tis-decisoes.json
- **Execution Condition:** ((the_voltage_antes <= 80 /\ the_voltage > 80) \/ (the_flashing_mode_antes != both_flashing /\ the_flashing_mode = both_flashing)) /\ the_voltage > 80 /\ the_flashing_mode = both_flashing
- **Initial State:** Nao especificado
- **Inputs:** the_voltage, the_voltage_antes, the_flashing_mode, the_flashing_mode_antes
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_indication_lights := both_flashing, the_flashing_timer := 0
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the voltage becomes greater than 80 or the flashing mode becomes both flashing, and the voltage is greater than 80, and the flashing mode is both flashing, the lights controller component shall Assign both flashing to the indication lights, reset the flashing timer.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos., O requisito participa de uma sobreposicao formal com acoes potencialmente conflitantes; alcançabilidade e prioridade nao foram confirmadas.
- **Confidence:** documentado-com-ressalva
- **Reserve:** RESSALVA-TIS-NPP

### E1-ORC-010 - tis#5
- **System:** turn_indicator_system
- **Requirement ID:** REQ005
- **Source:** experimentacao/experimentacao-1/requirements/experimental/tis-decisoes.json
- **Execution Condition:** the_voltage > 80 /\ the_flashing_mode = no_flashing
- **Initial State:** Nao especificado
- **Inputs:** the_voltage, the_flashing_mode
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_indication_lights := off, the_flashing_timer := 0
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the voltage is greater than 80, and the flashing mode is no flashing, the lights controller component shall Assign off to the indication lights, reset the flashing timer.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

### E1-ORC-011 - tis#6
- **System:** turn_indicator_system
- **Requirement ID:** REQ006
- **Source:** experimentacao/experimentacao-1/requirements/experimental/tis-decisoes.json
- **Execution Condition:** the_voltage > 80 /\ the_flashing_timer >= 340 /\ (the_indication_lights = left_flashing \/ the_indication_lights = right_flashing)
- **Initial State:** Nao especificado
- **Inputs:** the_voltage, the_indication_lights, the_flashing_timer
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_indication_lights := off, the_flashing_timer := 0
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the voltage is greater than 80, and the flashing timer is greater than or equal to 340, and the indication lights are left flashing or the indication lights are right flashing, the lights controller component shall Assign off to the indication lights, reset the flashing timer.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos., O requisito participa de uma sobreposicao formal com acoes potencialmente conflitantes; alcançabilidade e prioridade nao foram confirmadas.
- **Confidence:** documentado-com-ressalva
- **Reserve:** RESSALVA-TIS-NPP

### E1-ORC-012 - tis#7
- **System:** turn_indicator_system
- **Requirement ID:** REQ007
- **Source:** experimentacao/experimentacao-1/requirements/experimental/tis-decisoes.json
- **Execution Condition:** the_voltage > 80 /\ the_flashing_timer >= 220 /\ the_indication_lights = off /\ the_flashing_mode = left_flashing
- **Initial State:** Nao especificado
- **Inputs:** the_voltage, the_flashing_mode, the_indication_lights, the_flashing_timer
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_indication_lights := left_flashing, the_flashing_timer := 0
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the voltage is greater than 80, and the flashing timer is greater than or equal to 220, and the indication lights are off, and the flashing mode is left flashing, the lights controller component shall Assign left flashing to the indication lights, reset the flashing timer.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

### E1-ORC-013 - tis#8
- **System:** turn_indicator_system
- **Requirement ID:** REQ008
- **Source:** experimentacao/experimentacao-1/requirements/experimental/tis-decisoes.json
- **Execution Condition:** the_voltage > 80 /\ the_flashing_timer >= 220 /\ the_indication_lights = off /\ the_flashing_mode = right_flashing
- **Initial State:** Nao especificado
- **Inputs:** the_voltage, the_flashing_mode, the_indication_lights, the_flashing_timer
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_indication_lights := right_flashing, the_flashing_timer := 0
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the voltage is greater than 80, and the flashing timer is greater than or equal to 220, and the indication lights are off, and the flashing mode is right flashing, the lights controller component shall Assign right flashing to the indication lights, reset the flashing timer.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

### E1-ORC-014 - tis#9
- **System:** turn_indicator_system
- **Requirement ID:** REQ009
- **Source:** experimentacao/experimentacao-1/requirements/experimental/tis-decisoes.json
- **Execution Condition:** the_voltage > 80 /\ the_flashing_timer >= 220 /\ the_indication_lights = off /\ the_flashing_mode = both_flashing
- **Initial State:** Nao especificado
- **Inputs:** the_voltage, the_flashing_mode, the_indication_lights, the_flashing_timer
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_indication_lights := both_flashing, the_flashing_timer := 0
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the voltage is greater than 80, and the flashing timer is greater than or equal to 220, and the indication lights are off, and the flashing mode is both flashing, the lights controller component shall Assign both flashing to the indication lights, reset the flashing timer.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

### E1-ORC-015 - tis#10
- **System:** turn_indicator_system
- **Requirement ID:** REQ010
- **Source:** experimentacao/experimentacao-1/requirements/experimental/tis-decisoes.json
- **Execution Condition:** the_turn_indicator_lever_antes != left /\ the_turn_indicator_lever = left /\ the_emergency_flashing = off
- **Initial State:** Nao especificado
- **Inputs:** the_turn_indicator_lever, the_turn_indicator_lever_antes, the_emergency_flashing
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_flashing_mode := left_flashing, the_flashing_timer := 0
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the turn indicator lever changes to the left position, and the emergency flashing is off, the flashing mode component shall assign left flashing to the flashing mode, reset the flashing timer.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

### E1-ORC-016 - tis#11
- **System:** turn_indicator_system
- **Requirement ID:** REQ011
- **Source:** experimentacao/experimentacao-1/requirements/experimental/tis-decisoes.json
- **Execution Condition:** the_turn_indicator_lever_antes != right /\ the_turn_indicator_lever = right /\ the_emergency_flashing = off
- **Initial State:** Nao especificado
- **Inputs:** the_turn_indicator_lever, the_turn_indicator_lever_antes, the_emergency_flashing
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_flashing_mode := right_flashing, the_flashing_timer := 0
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the turn indicator lever changes to the right position, and the emergency flashing is off, the flashing mode component shall assign right flashing to the flashing mode, reset the flashing timer.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

### E1-ORC-017 - tis#12
- **System:** turn_indicator_system
- **Requirement ID:** REQ012
- **Source:** experimentacao/experimentacao-1/requirements/experimental/tis-decisoes.json
- **Execution Condition:** the_emergency_flashing_antes != on /\ the_emergency_flashing = on
- **Initial State:** Nao especificado
- **Inputs:** the_emergency_flashing, the_emergency_flashing_antes
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_flashing_mode := both_flashing, the_flashing_timer := 0
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the emergency flashing becomes on, the flashing mode component shall assign both flashing to the flashing mode, reset the flashing timer.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

### E1-ORC-018 - tis#13
- **System:** turn_indicator_system
- **Requirement ID:** REQ013
- **Source:** experimentacao/experimentacao-1/requirements/experimental/tis-decisoes.json
- **Execution Condition:** the_emergency_flashing = on /\ the_emergency_flashing_antes = on /\ the_turn_indicator_lever_antes != left /\ the_turn_indicator_lever = left
- **Initial State:** Nao especificado
- **Inputs:** the_turn_indicator_lever, the_turn_indicator_lever_antes, the_emergency_flashing, the_emergency_flashing_antes
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_flashing_mode := left_flashing, the_flashing_timer := 0
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the emergency flashing is on, and the emergency flashing was on, and the turn indicator lever changes to the left position, the flashing mode component shall assign left flashing to the flashing mode, reset the flashing timer.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

### E1-ORC-019 - tis#14
- **System:** turn_indicator_system
- **Requirement ID:** REQ014
- **Source:** experimentacao/experimentacao-1/requirements/experimental/tis-decisoes.json
- **Execution Condition:** the_emergency_flashing = on /\ the_emergency_flashing_antes = on /\ the_turn_indicator_lever_antes != right /\ the_turn_indicator_lever = right
- **Initial State:** Nao especificado
- **Inputs:** the_turn_indicator_lever, the_turn_indicator_lever_antes, the_emergency_flashing, the_emergency_flashing_antes
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_flashing_mode := right_flashing, the_flashing_timer := 0
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the emergency flashing is on, and the emergency flashing was on, and the turn indicator lever changes to the right position, the flashing mode component shall assign right flashing to the flashing mode, reset the flashing timer.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

### E1-ORC-020 - tis#15
- **System:** turn_indicator_system
- **Requirement ID:** REQ015
- **Source:** experimentacao/experimentacao-1/requirements/experimental/tis-decisoes.json
- **Execution Condition:** the_emergency_flashing = on /\ the_emergency_flashing_antes = on /\ the_turn_indicator_lever_antes != idle /\ the_turn_indicator_lever = idle /\ the_flashing_mode != both_flashing
- **Initial State:** Nao especificado
- **Inputs:** the_flashing_mode, the_turn_indicator_lever, the_turn_indicator_lever_antes, the_emergency_flashing, the_emergency_flashing_antes
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_flashing_mode := both_flashing, the_flashing_timer := 0
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the emergency flashing is on, and the emergency flashing was on, and the turn indicator lever changes to the idle position, and the flashing mode is not both flashing, the flashing mode component shall assign both flashing to the flashing mode, reset the flashing timer.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

### E1-ORC-021 - tis#16
- **System:** turn_indicator_system
- **Requirement ID:** REQ016
- **Source:** experimentacao/experimentacao-1/requirements/experimental/tis-decisoes.json
- **Execution Condition:** the_emergency_flashing_antes != off /\ the_emergency_flashing = off /\ the_turn_indicator_lever = left /\ the_turn_indicator_lever_antes = left /\ the_flashing_mode != left_flashing
- **Initial State:** Nao especificado
- **Inputs:** the_flashing_mode, the_turn_indicator_lever, the_turn_indicator_lever_antes, the_emergency_flashing, the_emergency_flashing_antes
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_flashing_mode := left_flashing, the_flashing_timer := 0
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the emergency flashing becomes off, and the turn indicator lever is on the left position, and the turn indicator lever was on the left position, and the flashing mode is not left flashing, the flashing mode component shall assign left flashing to the flashing mode, reset the flashing timer.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

### E1-ORC-022 - tis#17
- **System:** turn_indicator_system
- **Requirement ID:** REQ017
- **Source:** experimentacao/experimentacao-1/requirements/experimental/tis-decisoes.json
- **Execution Condition:** the_emergency_flashing_antes != off /\ the_emergency_flashing = off /\ the_turn_indicator_lever = right /\ the_turn_indicator_lever_antes = right /\ the_flashing_mode != right_flashing
- **Initial State:** Nao especificado
- **Inputs:** the_flashing_mode, the_turn_indicator_lever, the_turn_indicator_lever_antes, the_emergency_flashing, the_emergency_flashing_antes
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_flashing_mode := right_flashing, the_flashing_timer := 0
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the emergency flashing becomes off, and the turn indicator lever is on the right position, and the turn indicator lever was on the right position, and the flashing mode is not right flashing, the flashing mode component shall assign right flashing to the flashing mode, reset the flashing timer.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

### E1-ORC-023 - npp#1
- **System:** safety_injection_system
- **Requirement ID:** REQ001
- **Source:** experimentacao/experimentacao-1/requirements/experimental/npp-decisoes.json
- **Execution Condition:** the_water_pressure_antes < 9 /\ the_water_pressure >= 9 /\ the_pressure_mode = low
- **Initial State:** Nao especificado
- **Inputs:** the_water_pressure, the_water_pressure_antes, the_pressure_mode
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_pressure_mode := permitted
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the water pressure becomes greater than or equal to 9, and the pressure mode is low, the Safety Injection System shall assign permitted to the pressure mode.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

### E1-ORC-024 - npp#2
- **System:** safety_injection_system
- **Requirement ID:** REQ002
- **Source:** experimentacao/experimentacao-1/requirements/experimental/npp-decisoes.json
- **Execution Condition:** the_water_pressure_antes < 10 /\ the_water_pressure >= 10 /\ the_pressure_mode = permitted
- **Initial State:** Nao especificado
- **Inputs:** the_water_pressure, the_water_pressure_antes, the_pressure_mode
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_pressure_mode := high
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the water pressure becomes greater than or equal to 10, and the pressure mode is permitted, the Safety Injection System shall assign high to the pressure mode.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

### E1-ORC-025 - npp#3
- **System:** safety_injection_system
- **Requirement ID:** REQ003
- **Source:** experimentacao/experimentacao-1/requirements/experimental/npp-decisoes.json
- **Execution Condition:** the_water_pressure_antes >= 9 /\ the_water_pressure < 9 /\ the_pressure_mode = permitted
- **Initial State:** Nao especificado
- **Inputs:** the_water_pressure, the_water_pressure_antes, the_pressure_mode
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_pressure_mode := low
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the water pressure becomes lower than 9, and the pressure mode is permitted, the Safety Injection System shall assign low to the pressure mode.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

### E1-ORC-026 - npp#4
- **System:** safety_injection_system
- **Requirement ID:** REQ004
- **Source:** experimentacao/experimentacao-1/requirements/experimental/npp-decisoes.json
- **Execution Condition:** the_water_pressure_antes >= 10 /\ the_water_pressure < 10 /\ the_pressure_mode = high
- **Initial State:** Nao especificado
- **Inputs:** the_water_pressure, the_water_pressure_antes, the_pressure_mode
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_pressure_mode := permitted
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the water pressure becomes lower than 10, and the pressure mode is high, the Safety Injection System shall assign permitted to the pressure mode.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

### E1-ORC-027 - npp#5
- **System:** safety_injection_system
- **Requirement ID:** REQ005
- **Source:** experimentacao/experimentacao-1/requirements/experimental/npp-decisoes.json
- **Execution Condition:** the_blockage_button_antes != pressed /\ the_blockage_button = pressed /\ the_reset_button != pressed /\ the_pressure_mode != high
- **Initial State:** Nao especificado
- **Inputs:** the_pressure_mode, the_blockage_button, the_blockage_button_antes, the_reset_button
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_overridden_mode := true
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the blockage button becomes pressed, and the reset button is not pressed, and the pressure mode is not high, the Safety Injection System shall assign true to the overridden mode.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos., O requisito participa de uma sobreposicao formal com acoes potencialmente conflitantes; alcançabilidade e prioridade nao foram confirmadas.
- **Confidence:** documentado-com-ressalva
- **Reserve:** RESSALVA-TIS-NPP

### E1-ORC-028 - npp#6
- **System:** safety_injection_system
- **Requirement ID:** REQ006
- **Source:** experimentacao/experimentacao-1/requirements/experimental/npp-decisoes.json
- **Execution Condition:** the_reset_button_antes != pressed /\ the_reset_button = pressed /\ the_pressure_mode != high
- **Initial State:** Nao especificado
- **Inputs:** the_pressure_mode, the_reset_button, the_reset_button_antes
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_overridden_mode := false
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the reset button becomes pressed, and the pressure mode is not high, the Safety Injection System shall assign false to the overridden mode.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

### E1-ORC-029 - npp#7
- **System:** safety_injection_system
- **Requirement ID:** REQ007
- **Source:** experimentacao/experimentacao-1/requirements/experimental/npp-decisoes.json
- **Execution Condition:** the_pressure_mode_antes != high /\ the_pressure_mode = high
- **Initial State:** Nao especificado
- **Inputs:** the_pressure_mode, the_pressure_mode_antes
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_overridden_mode := false
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the pressure mode becomes high, the Safety Injection System shall assign false to the overridden mode.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

### E1-ORC-030 - npp#8
- **System:** safety_injection_system
- **Requirement ID:** REQ008
- **Source:** experimentacao/experimentacao-1/requirements/experimental/npp-decisoes.json
- **Execution Condition:** the_pressure_mode_antes = high /\ the_pressure_mode != high
- **Initial State:** Nao especificado
- **Inputs:** the_pressure_mode, the_pressure_mode_antes
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_overridden_mode := false
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the pressure mode becomes not high, the Safety Injection System shall assign false to the overridden mode.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos., O requisito participa de uma sobreposicao formal com acoes potencialmente conflitantes; alcançabilidade e prioridade nao foram confirmadas.
- **Confidence:** documentado-com-ressalva
- **Reserve:** RESSALVA-TIS-NPP

### E1-ORC-031 - npp#9
- **System:** safety_injection_system
- **Requirement ID:** REQ009
- **Source:** experimentacao/experimentacao-1/requirements/experimental/npp-decisoes.json
- **Execution Condition:** the_pressure_mode = low /\ the_overridden_mode = true
- **Initial State:** Nao especificado
- **Inputs:** the_pressure_mode, the_overridden_mode
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_safety_injection_mode := off
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the pressure mode is low, and the overridden mode is true, the Safety Injection System shall assign off to the safety injection mode.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos., the_safety_injection_mode aparece em acoes, mas nao esta declarado em inputs com tipo ou dominio; nenhuma hipotese foi usada como fato.
- **Confidence:** parcialmente-especificado
- **Reserve:** RESSALVA-NPP-OUTPUT

### E1-ORC-032 - npp#10
- **System:** safety_injection_system
- **Requirement ID:** REQ010
- **Source:** experimentacao/experimentacao-1/requirements/experimental/npp-decisoes.json
- **Execution Condition:** the_pressure_mode = low /\ the_overridden_mode = false
- **Initial State:** Nao especificado
- **Inputs:** the_pressure_mode, the_overridden_mode
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_safety_injection_mode := on
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the pressure mode is low, and the overridden mode is false, the Safety Injection System shall assign on to the safety injection mode.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos., the_safety_injection_mode aparece em acoes, mas nao esta declarado em inputs com tipo ou dominio; nenhuma hipotese foi usada como fato.
- **Confidence:** parcialmente-especificado
- **Reserve:** RESSALVA-NPP-OUTPUT

### E1-ORC-033 - npp#11
- **System:** safety_injection_system
- **Requirement ID:** REQ011
- **Source:** experimentacao/experimentacao-1/requirements/experimental/npp-decisoes.json
- **Execution Condition:** the_pressure_mode = permitted \/ the_pressure_mode = high
- **Initial State:** Nao especificado
- **Inputs:** the_pressure_mode
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** the_safety_injection_mode := off
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** When the pressure mode is permitted or the pressure mode is high, the Safety Injection System shall assign off to the safety injection mode.
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos., the_safety_injection_mode aparece em acoes, mas nao esta declarado em inputs com tipo ou dominio; nenhuma hipotese foi usada como fato.
- **Confidence:** parcialmente-especificado
- **Reserve:** RESSALVA-NPP-OUTPUT

### E1-ORC-034 - REQ-001
- **System:** generic
- **Requirement ID:** REQ-001
- **Source:** experimentacao/experimentacao-1/requirements/experimental/requisitos.mcdc
- **Execution Condition:** (alarme_ativo and porta_aberta) or botao_emergencia
- **Initial State:** Nao especificado
- **Inputs:** alarme_ativo, botao_emergencia, p, ta_aberta
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** Nenhuma acao explicitamente documentada
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** (alarme_ativo and porta_aberta) or botao_emergencia
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

### E1-ORC-035 - REQ-002
- **System:** generic
- **Requirement ID:** REQ-002
- **Source:** experimentacao/experimentacao-1/requirements/experimental/requisitos.mcdc
- **Execution Condition:** porta_fechada and not obstaculo
- **Initial State:** Nao especificado
- **Inputs:** obstaculo, p, ta_fechada
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** Nenhuma acao explicitamente documentada
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** porta_fechada and not obstaculo
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

### E1-ORC-036 - REQ-003
- **System:** generic
- **Requirement ID:** REQ-003
- **Source:** experimentacao/experimentacao-1/requirements/experimental/requisitos.mcdc
- **Execution Condition:** freio_acionado or (freio_acionado and pedal_pressionado)
- **Initial State:** Nao especificado
- **Inputs:** freio_acionado, pedal_pressionado
- **Expected Decision:** verdadeiro quando a guarda e satisfeita
- **Expected Action:** Nenhuma acao explicitamente documentada
- **Expected Output:** Nao especificado além das acoes explicitas
- **Rationale:** freio_acionado or (freio_acionado and pedal_pressionado)
- **Uncertainties:** Estado inicial nao especificado independentemente da guarda., Comportamentos fora das acoes explicitas nao foram inferidos.
- **Confidence:** documentado
- **Reserve:** 

