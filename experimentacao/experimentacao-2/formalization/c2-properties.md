# Formalizações extraídas da documentação C2

As formalizações abaixo usam apenas regras expressas literalmente no texto C2.

## Fontes de fórmula

| Propriedade | Trecho C2 |
|---|---|
| Fonte única | “expressao ... um arquivo .mcdc ou json nao manda tudo junto” |
| Operadores | AND/OR/NOT e operadores listados |
| Limite da tabela | “tabela 20 entrada” |
| Limite direto | “direto 30” |
| Limite Z3 linha a linha | “linha 4096” |
| Limite de pares | “condiçao 1000 par” |
| Timeout Z3 | “z3 60 segundo” |
| Códigos | “zero”, “um” e “dois” |

## Limitações

Não foram formalizadas:

- precedência completa;
- formato completo de CSV;
- formato completo de JSON;
- forma exata das saídas;
- semântica completa de UNKNOWN no Z3;
- algoritmo guloso;
- busca exata;
- condições temporais não descritas.
