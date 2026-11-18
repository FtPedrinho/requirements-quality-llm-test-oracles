# Metodologia

## Estrutura testada

Os testes são executados sobre as 33 decisões NAT2TEST presentes em:

- `exemplos/vm-decisoes.json`;
- `exemplos/tis-decisoes.json`;
- `exemplos/npp-decisoes.json`.

As três expressões gerais não foram usadas como mutantes porque não possuem ações ou modelos de domínio associados.

## Operadores

São usados operadores aplicáveis às estruturas reais:

- AND -> OR;
- OR -> AND;
- negação de subexpressão;
- remoção de condição em AND/OR;
- negação de folha;
- troca de operador relacional;
- inversão de operador relacional;
- alteração de constante numérica em ±1;
- substituição de constante por seu limite oposto;
- substituição de guarda pela sua negação.

Mutantes duplicados são removidos por expressão textual normalizada.

## Equivalência

Para original `P` e mutante `P'`, Z3 verifica:

```text
P XOR P'
```

sob os domínios enum e os demais constrangimentos registrados.

- SAT: existe atribuição que diferencia a expressão.
- UNSAT: equivalente dentro das restrições consideradas.
- UNKNOWN: não determinado.

Mutantes equivalentes são excluídos do denominador tradicional, mas registrados separadamente.

## Casos concretos

Os 152 casos originais são preservados como unidade da suíte. Cada caso recebe valores concretos quando Z3 consegue realizá-lo:

- `PASS`: modelo que satisfaz a guarda;
- `MC/DC`: dois modelos obtidos pelo mesmo par abstrato, mantendo outras folhas fixas e invertendo apenas a folha analisada.

Casos sem modelo concreto são classificados como não avaliáveis.

## Execução

Para o modelo original:

- PASS passa se o modelo satisfaz a guarda.
- Pareamento MC/DC passa se os dois modelos produzem resultados opostos.

Para mutantes:

- PASS mata o mutante se o mutante não satisfaz onde o original satisfaz.
- Par MC/DC mata o mutante se o mutante não preserva a diferença esperada entre os dois modelos.

Erros de infraestrutura ou parsing não são mortos nem sobreviventes.
