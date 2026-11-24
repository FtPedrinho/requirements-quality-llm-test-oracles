# Segunda extensão coverage-informed

Após a primeira extensão, `Predicate` tinha 0/30 branches e a codificação
numérica Z3 apresentava caminhos não cobertos. Os 13 casos desta extensão
exercitam comparações `=`, `!=`, `<`, `<=`, `>` e `>=` e valores concretos
imediatamente abaixo, no e acima do limite. R3 lista os operadores; R13
permite valores concretos no CSV de `check`; R6 estabelece códigos 0 e 2;
R9 exemplifica fronteiras de `>` como o valor do limite e o seguinte.

Para cada operador, o solver independente gera três resultados e as duas
consultas SMT-LIB por valor. O CSV correto contém esses valores; o CSV
divergente inverte apenas o resultado esperado do ponto 3. Cada comparação
tem pelo menos um verdadeiro e um falso, que formam um par para sua única
condição. Assim, a suíte é completa; a versão divergente deve retornar 2.
O caso de fronteira exige que as variantes incluam 3 e 4, sem exigir que
sejam as únicas. O executor interpreta apenas resultados de teste e código,
não registra as métricas adicionais da saída de `check`. Não se assume
correção da tradução apenas porque o Z3 responde `sat`. Autoavaliação, sem
revisor independente.
