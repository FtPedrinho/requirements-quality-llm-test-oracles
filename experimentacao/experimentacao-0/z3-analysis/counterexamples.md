# Contraexemplos

## Incompatibilidades identificadas

Os resultados abaixo são contraexemplos formais da satisfação conjunta das guardas com ações que atribuem valores diferentes à mesma variável.

| Sistema | Requisitos | Variável | Ações conflitantes | Modelo observado |
|---|---|---|---|---|
| TIS | tis#2, tis#6 | `the_indication_lights` | `left_flashing` versus `off` | Tensão 81, timer 340, modo left |
| TIS | tis#3, tis#6 | `the_indication_lights` | `right_flashing` versus `off` | Tensão 81, timer 340, modo right |
| TIS | tis#4, tis#6 | `the_indication_lights` | `both_flashing` versus `off` | Tensão 81, timer 340, modo both |
| NPP | npp#5, npp#8 | `the_overridden_mode` | `true` versus `false` | Bloco pressionado; modo anterior high; modo atual low |

## Interpretação

Os pares são SAT dentro da formalização: as duas guardas podem ser satisfeitas simultaneamente e atribuem valores diferentes à mesma variável.

Isso exige análise humana para determinar se existe:

- incompatibilidade real;
- domínio temporal que impede a combinação;
- relação de prioridade não documentada;
- erro de tradução;
- representação incompleta da ação ou do estado.

Nenhuma dessas possibilidades foi resolvida pelo Z3.
