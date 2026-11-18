# Preparação para validação humana

Cada item apresentado ao avaliador deve conter:

1. requisito original;
2. guarda formal utilizada;
3. resultado Z3 da satisfatibilidade;
4. resultados de redundância e implicação;
5. contraexemplo, quando houver;
6. oráculo produzido pelo Copilot;
7. resultado da comparação com Z3;
8. casos de teste derivados;
9. incertezas registradas.

## Questões para avaliadores

- A formalização representa corretamente o requisito original?
- A formalização omite estados ou restrições temporais?
- Os contraexemplos representam combinações alcançáveis?
- Existem prioridades ou efeitos de execução não documentados?
- O oráculo interpreta corretamente os resultados esperados?
- Há comportamento adicional assumido pelo oráculo?
- Os casos simbólicos são adequados ao critério MC/DC?
- Informações ausentes foram corretamente marcadas como não especificadas?
- Os conflitos TIS/NPP são reais, derivados de formalização ou impossíveis no domínio?

Os avaliadores devem validar formalização e semântica separadamente. O Z3 não substitui essa revisão.
