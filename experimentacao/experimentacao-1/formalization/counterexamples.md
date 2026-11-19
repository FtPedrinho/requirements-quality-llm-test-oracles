# Contraexemplos da formalizacao C1

## TIS

- **tis#2 x tis#6:** tensao 81, timer 340, modo left, indicacao left; acoes left_flashing e off.
- **tis#3 x tis#6:** tensao 81, timer 340, modo right, indicacao left; acoes right_flashing e off.
- **tis#4 x tis#6:** tensao 81, timer 340, modo both, indicacao left; acoes both_flashing e off.

## NPP

- **npp#5 x npp#8:** blockage released -> pressed, reset released, modo anterior high e atual low; acoes true e false em `the_overridden_mode`.

Os modelos demonstram satisfatibilidade formal das conjuncoes. Informacao sobre ordem de execucao, prioridade, alcance temporal e maquina de estados nao esta disponível na fonte consultada.
