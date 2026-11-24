# Análise documental C3 — segunda tentativa (critério estrito)

Esta é a **segunda** execução de C3 (a primeira está preservada em `../tentativa-1/`). Foi refeita por determinação do pesquisador:
a documentação C3 é verdade absoluta; o sistema só serve de entrada para criar a suíte; não criar expectativa por suposição; não ter receio de registrar INDETERMINADO.

- Fonte única: `experimentacao-pesquisa/experimentacao-3/documentation/tool-readme-C3.md`, SHA-256 `F18B0821D79C7315486C13D5260FA2F6D6E9418EF03B86CDE58E66B91B7B87A3` (conferido).
- Modelo: Claude Sonnet 5.5; prompt `geracao-de-oraculos-v3.md`; revisão: **autorrevisão**.
- **Perda de isolamento (declarada):** esta tentativa ocorre na mesma sessão da primeira. O autor já viu a saída do SUT e o resultado da tentativa 1 (inclusive a falha de um caso). Não é possível “esquecer” isso; o oráculo foi derivado do texto e revisado com critério mais estrito, mas a influência não pode ser descartada. Os casos rebaixados abaixo foram justificados por razões documentais, e um deles (antigo D15) coincide com um caso que falhara na tentativa 1.

## O que mudou em relação à tentativa 1

Casos que dependiam de interpretação, analogia ou assunção foram rebaixados a INDETERMINADO (agora `C3-I25…I32`):

| Novo ID | Motivo |
|---|---|
| I25 | fronteira de `speed > 50`: o texto só exemplifica `speed > 100`; seria extrapolação |
| I26 | “REQ-003 tem uma condição redundante”: depende de I09/I11 e de “uma” = exatamente uma |
| I27 | modo direto concorda com a tabela: o funcionamento do modo é contraditório (I04/I05) |
| I28 | “expressões inválidas recusadas”: gramática e forma da recusa não definidas |
| I29 | “erro de sintaxe com o requisito”: não define o erro nem a mensagem |
| I30 | verify sem `--context`: só há descrição de teste de unidade |
| I31 | 21 entradas: o texto dá o limite, não o comportamento ao excedê-lo |
| I32 | “arquivos inválidos” não definido |

Também foram **enxugadas** as expectativas determinadas: não se afirma tamanho de suíte em `A and not B`, não se afirma equivalência de pares, não se afirma tempo (a partida da JVM não é separável) e a contagem de mutantes de `C3-D12` é só a estrutura (total > 0, tipos entre os seis).

## Contradições internas do texto (casos I01–I24)

Mantidas as da tentativa 1: condições por ocorrência × por variável (I01); Z3 obrigatório × opcional (I02); códigos de saída (I03); 12 × 30 entradas e modo direto (I04, I05); colunas do CSV (I06); `csv`/`truth-csv` (I07); `unsat` = impossível × possível (I08); par exige mudança de resultado × não (I09); minimalidade gulosa/exata (I10); redundante × bloqueada (I11); arquitetura do Z3 (I12); regras de build (I13–I15); garantia para parênteses (I16); e omissões I17–I24.

## Casos determinados (40)

`C3-D01…D40` (ver `oraculo.json`). Sustentados por trecho literal e sem conflito interno: formas de operadores e precedência; tabela-verdade e 4 testes de `(A and B) or C` (exemplo do texto); restrição manual; fronteira 100/101; valores concretos; mutação (estrutura e causa única); valores “travados pela regressão” (requisitos, completos, combinações, impossíveis, testes, mutantes, conflitos) para VM/TIS/NPP; `check`, `verify`, `-o`, `.mcdc`, JSON, 20 entradas, `_antes`, número negativo.

Decisão sobre o Z3: como I02 torna a expectativa sem Z3 indeterminada, os casos determinados rodam com Z3 no PATH (única condição em que as duas leituras concordam). Código de saída nunca é afirmado (I03).

## Z3

Z3 5.4.1 independente do SUT; 122 consultas em `z3/*.smt2`, respostas em `z3/*.out`, resumo em `z3/RESUMO.tsv`. Todas coincidem com a resposta esperada da fórmula (sem `unknown`/timeout). Cada conflito textual está formalizado (afirmações isoladas `sat`, conjunção `unsat`). `sat`/`unsat` não provam a fidelidade da tradução. Casos sem lógica formalizável (formatos, arquivos) não têm consulta própria.

## Limitações

Autorrevisão; perda de isolamento descrita acima; a fronteira entre “determinado” e “indeterminado” é julgamento do modelo.
