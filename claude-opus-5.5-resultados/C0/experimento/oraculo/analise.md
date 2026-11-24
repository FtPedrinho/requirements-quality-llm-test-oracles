# C0 — Análise documental e oráculo

Fonte normativa exclusiva: `experimentacao-pesquisa/documentacao-original/tool-readme-original.md`
(SHA-256 `72B827BDEE6CE859527765CFF574A473519C00A1AF9AA9F3AACCE4236A4995F8`, conferido antes da leitura).
A especificação em PDF (`technical-specification.pdf`) **não** foi usada, porque o manifesto a declara como não normativa.
Os casos estão em [oraculo.json](oraculo.json). As consultas SMT-LIB e os resultados do Z3 estão em [z3/](z3/).

## Inventário do texto

| Área | O que o README define | Casos |
|---|---|---|
| Códigos de saída | 0 tudo certo; 1 entrada inválida; 2 condição sem par / não demonstrada / esperado divergente / conflito ou lacuna | quase todos |
| Variantes | mascaramento (padrão), causa única (`--unique-cause`) | A02, A03, F10, G09, G10, E09 |
| Condições por aparição | `A#1`, `A#2` em `(A and B) or (not A and C)` | A05, A06, G09 |
| Diagnóstico | redundante × bloqueada | A06–A09, C06 |
| Restrição manual | `--constraint`, só com expressão direta | A08–A10, B08, C12 |
| Tamanho da suíte | (A∧B)∨C = 4; A∧¬B = 3; exemplo exato 5 × guloso 6; paridade 3 = 8; guardas simples N+1 | A02, A04, A11–A14, A16 |
| Limites | 20 entradas na tabela, 12 com Z3 linha a linha (acima disso, modo direto), 30 no direto | A14–A18 |
| Operadores | and/&&/`/\`, or/\|\|/`\/`, not/!, comparações; precedência "e antes de ou" | B01–B13 |
| Formatos | text, json, csv (uma linha por teste e entrada), truth-csv (tabela inteira, impossíveis marcadas); check/verify só text e json; `-o` | B07, B08, B14, C01, C02, E10, F06, F09 |
| Fontes | expressão, `.mcdc` (ID: expr, `#` comentário), JSON NAT2TEST (`_antes`) | C03–C11 |
| Z3 | impossíveis, valores concretos, fronteira (`speed > 100` → 100 e 101), aviso sem Z3 | C08, D01–D06 |
| Mutação | seis tipos (ORF, ENF, VNF, MVF, VRF, ASF); equivalentes fora da conta | D07, D08, G10, E01–E03 |
| Regressão dos sistemas | tabela "Números travados pela regressão" (VM/TIS/NPP) | E01–E06, E08, E09 |
| `check` | cobertura, o que falta, esperado errado, valores lógicos ou concretos, colunas faltando | F01–F10 |
| `verify` | conflito = duas guardas valem juntas e escrevem valores diferentes; lacuna só com contexto | G01–G08 |

## Decisões de interpretação (autorrevisão)

1. **Definição de par.** Uso a frase de "Como funciona": *dois testes possíveis em que ela muda, a saída muda e ela decide nos dois*. Para causa única, acrescento "demais entradas iguais", que é a definição usual das referências citadas (Chilenski). Isso é uma interpretação e fica registrada.
2. **"Guardas simples" → N+1.** Aplico só à conjunção de entradas distintas (A14, A16), a leitura mais restrita.
3. **Código 1 para formato não aceito** (B14, F06). O texto lista os formatos aceitos e diz que o código 1 significa "entrada inválida". Tratei o valor fora da lista como entrada inválida. É uma leitura do texto.
4. **Ids repetidos e "linha sem identificador".** "ids repetidos" aparece ao lado de "arquivos inválidos" e foi tratado como erro (C11). "linha sem identificador" não diz se é erro ou se recebe ID automático, então não virou caso determinado.
5. **"Completos"** (tabela de regressão) não tem definição operacional, então não é afirmado. Os códigos de saída de `analyze` nos sistemas também não são afirmados, exceto em E10, que aceita 0 ou 2.
6. **Sistemas de exemplo (E01–E09).** As entradas são os arquivos `exemplos/*.json` citados pelo README. Não foram abertos antes do congelamento. As expectativas são só os números da tabela de regressão.
7. **Saída em texto.** O formato não é documentado. Só verifico menções mínimas citadas no texto ("redundante", "bloqueada", fronteiras 100/101, IDs).
8. **Leitura das saídas JSON e CSV.** Os nomes dos campos não estão documentados. Os **valores esperados** ficam congelados aqui. Os **adaptadores** que extraem esses valores só serão escritos depois do congelamento, a partir do código, e isso conta como ameaça à validade.

## Indeterminados (13)

A15 (21 entradas sem Z3), A17 (31 entradas no direto), B15 (comando desconhecido), B16 (sem argumentos), B17 (gramática do sinal de menos), C12 (`--constraint` com arquivo), D03 (`--boundary` sem `--z3`), E07 (resultado do exemplo `--context`), F07 (check sem `--tests`), F08 (resultado do exemplo `check`), G06 (verify em `.mcdc` sem ações), G07 (verify com expressão direta), G09 (causa única com aparições acopladas).

Contagem: 85 casos no total, 72 determinados e 13 indeterminados.

## Z3

Z3 5.4.1 (`z3.exe` do pacote `z3-solver`), chamado como processo e independente do módulo `mcdc-z3`. Foram 94 consultas, todas com a resposta esperada. Uma consulta de minimalidade (conjunção de 13 entradas com 13 slots) deu *timeout* na rodada 1. Isso é erro técnico, registrado em `z3/rodada-1-timeout.txt`, e a consulta foi substituída por lemas por condição para N=13 e N=20. O `sat`/`unsat` vale para as fórmulas: não prova que a tradução do texto é fiel.

Revisão: **autorrevisão**, sem revisor independente.
