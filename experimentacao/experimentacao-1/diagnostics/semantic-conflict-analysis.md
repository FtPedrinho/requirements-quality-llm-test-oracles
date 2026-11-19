# Diagnostico de consistencia semantica

## Metodo

Esta analise utilizou exclusivamente os JSON experimentais e originais de VM, TIS e NPP. O Z3 verificou a satisfatibilidade da conjuncao das duas guardas de cada par.

Foram mantidas:

- as variaveis do JSON;
- os tipos e valores dos enums;
- as guardas originais;
- as acoes originais.

Nao foram consultados codigo-fonte, testes JUnit, implementacoes de dominio ou relatorios. Portanto, SAT demonstra somente que existe uma atribuicao sob a formalizacao recebida. Nao demonstra, por si, alcance real do estado do sistema.

## TIS

### REQ002 x REQ006

- **Guarda REQ002:** `((the_voltage_antes <= 80 /\ the_voltage > 80) \/ (the_flashing_mode_antes != left_flashing /\ the_flashing_mode = left_flashing)) /\ the_voltage > 80 /\ the_flashing_mode = left_flashing`
- **Guarda REQ006:** `the_voltage > 80 /\ the_flashing_timer >= 340 /\ (the_indication_lights = left_flashing \/ the_indication_lights = right_flashing)`
- **Acao REQ002:** `the_indication_lights := left_flashing`; `the_flashing_timer := 0`
- **Acao REQ006:** `the_indication_lights := off`; `the_flashing_timer := 0`
- **Z3:** SAT.
- **Modelo:** tensao atual 81; tensao anterior 81; modo anterior no_flashing; modo atual left_flashing; timer 340; indicacao left.
- **Conflito de acao:** REQ002 atribui `left_flashing` e REQ006 atribui `off` a `the_indication_lights`.
- **Evidencia documental:** os textos descrevem um evento de modo/tensao e uma condicao temporal com luzes acionadas. Nenhum documento estabelece que ambos nao podem ocorrer juntos.
- **Interpretacao:** existe sobreposicao formal, mas nao foi demonstrado que o modelo representa uma transicao alcancavel sem uma maquina de estados completa.
- **Classificacao:** **Conflito potencial dependente de informacao ausente**.

### REQ003 x REQ006

- **Guarda REQ003:** `((the_voltage_antes <= 80 /\ the_voltage > 80) \/ (the_flashing_mode_antes != right_flashing /\ the_flashing_mode = right_flashing)) /\ the_voltage > 80 /\ the_flashing_mode = right_flashing`
- **Guarda REQ006:** igual a descrita acima.
- **Acao REQ003:** `the_indication_lights := right_flashing`; timer 0.
- **Acao REQ006:** `the_indication_lights := off`; timer 0.
- **Z3:** SAT.
- **Modelo:** tensao 81; modo anterior no_flashing; modo atual right_flashing; timer 340; indicacao left.
- **Conflito de acao:** atribuicoes `right_flashing` e `off`.
- **Evidencia documental:** nao existe regra de exclusividade ou prioridade.
- **Classificacao:** **Conflito potencial dependente de informacao ausente**.

### REQ004 x REQ006

- **Guarda REQ004:** `((the_voltage_antes <= 80 /\ the_voltage > 80) \/ (the_flashing_mode_antes != both_flashing /\ the_flashing_mode = both_flashing)) /\ the_voltage > 80 /\ the_flashing_mode = both_flashing`
- **Guarda REQ006:** igual a descrita acima.
- **Acao REQ004:** `the_indication_lights := both_flashing`; timer 0.
- **Acao REQ006:** `the_indication_lights := off`; timer 0.
- **Z3:** SAT.
- **Modelo:** tensao 81; modo anterior no_flashing; modo atual both_flashing; timer 340; indicacao left.
- **Conflito de acao:** atribuicoes `both_flashing` e `off`.
- **Evidencia documental:** nao existe regra de exclusividade ou prioridade.
- **Classificacao:** **Conflito potencial dependente de informacao ausente**.

## NPP

### REQ005 x REQ008

- **Guarda REQ005:** `the_blockage_button_antes != pressed /\ the_blockage_button = pressed /\ the_reset_button != pressed /\ the_pressure_mode != high`
- **Guarda REQ008:** `the_pressure_mode_antes = high /\ the_pressure_mode != high`
- **Acao REQ005:** `the_overridden_mode := true`
- **Acao REQ008:** `the_overridden_mode := false`
- **Z3:** SAT.
- **Modelo:** blockage anterior released, atual pressed; reset released; modo anterior high, atual low.
- **Evidencia documental:** os requisitos descrevem transicoes distintas. O JSON nao declara prioridade nem precedencia.
- **Interpretacao:** a sobreposicao pode representar eventos simultaneos ou estados consecutivos. O documento nao prova nem exclui a simultaneidade.
- **Classificacao:** **Conflito potencial dependente de informacao ausente**.

## Resultado por categoria

| Categoria | Quantidade |
|---|---:|
| Conflito semantico confirmado | 0 |
| Sobreposicao formal sem conflito demonstrado | 0 |
| Conflito potencial dependente de informacao ausente | 4 |
| Nao avaliavel | 0 |

## Conclusao

1. **Conflitos semanticos efetivamente confirmados:** 0. O Z3 confirmou SAT e conflito de atribuicoes, mas nao confirmou alcance no sistema nem a existencia de processamento simultaneo.
2. **Sobreposicoes formais:** 4 pares apresentam sobreposicao formal das guardas e atribuicoes conflitantes.
3. **Dependentes de informacao ausente:** 4 pares.
4. **Nao avaliaveis:** 0 pares desta amostra.
5. **Problemas resolvidos sem alterar semantica:** nenhum dos conflitos e confirmado como resolvivel apenas por revisao textual. Padronizacao documental nao resolve a falta de prioridade/alcançabilidade.
6. **Decisoes que exigem especialista humano:** prioridade ou exclusividade dos quatro pares; alcance temporal TIS; precedencia NPP; declaracao da variable NPP.
7. **Alta consistencia:** nao pode ser confirmada nesta fase. Os pares permanecem pendentes e a variable NPP mantem uma lacuna declarativa.
