# Análise documental — C2

Fonte normativa exclusiva: `experimentacao-pesquisa/experimentacao-2/documentation/tool-readme-C2.md`
(SHA-256 verificado antes da leitura: `61C4062B5FC6B4F364F40465B0E017C80E0FA0C5433412EB2E925C545F6EFBE1`, coincide).
Revisão: **autorrevisão** (sem revisor independente). Nenhum código, saída ou resultado do SUT foi consultado
nesta fase; nenhum resultado de outras condições/LLMs foi usado.

## 1. Estado do texto-fonte

O documento está fortemente degradado: letras e palavras ausentes em quase todas as frases (p.ex.
"Gera tetes  **MC/DC** ... a partir  requisitos"), espaços duplos e blocos de código com caracteres faltando
(`mcdc anlyze`, `"( and B) or C"`). A degradação é parte da fonte e é tratada como verdade absoluta
**literal**: não se completa o texto por suposição. Princípio aplicado:

- **DETERMINADO** só quando o trecho (ou combinação de trechos íntegros) fixa uma expectativa única, mesmo
  que a prosa ao redor esteja corrompida: expressões íntegras (`(A and B) or C` na linha de `--unique-cause`,
  `(A and B) or (not A and C)` no parágrafo conceitual, `speed > 100 or (speed > 50 and rain)`), opções do
  quadro de opções (`--unique-cause`, `--constraint`, `--z3`, `--exact`, `--direct`, `--boundary`,
  `--mutation`, `--context`, `--format`, `-o`), códigos de saída, tabela de números de regressão
  (dígitos íntegros), limites (20/12/30 entradas), formatos de arquivo (`.mcdc`, JSON NAT2TEST, CSV de testes).
- **INDETERMINADO** quando a expressão/regra ficou corrompida a ponto de ter mais de uma leitura (p.ex.
  `((E or D) and (not  or D)) or B`, "Precedênca ( ates de )"), quando o texto só nomeia o tema de um teste
  sem dizer o resultado, ou quando falta definição operacional (mascaramento para ocorrências repetidas,
  comportamento acima dos limites, `_antes`, códigos de saída de casos não cobertos).

## 2. Inventário (resumo)

| Tema | Trechos-chave | Casos |
|---|---|---|
| Função da ferramenta, tabela-verdade 2^n, pares, suíte, demonstração por condição | seção "O que a ferramenta faz", "Como funciona" | C2-001..004 |
| Variantes MC/DC (mascaramento padrão, `--unique-cause`) | parágrafo "duas variantes"; opção `--unique-cause` | C2-001, 002, 017, 018 |
| Entrada vs. condição (ocorrência, `A#1`, `A#2`) | parágrafo conceitual | C2-004, 005 |
| Operadores e comparações | tabela de operadores | C2-006..009 |
| Restrição, redundante × bloqueada | `--constraint`; "Como funciona" passos 2 e 5 | C2-010..012 |
| Z3: impossíveis, valores concretos, fronteira, ausência do Z3 | `--z3`, `--boundary`, seção Instalação | C2-013..015 |
| Suíte exata, modo direto, limites | `--exact`, `--direct`, "Limites conhecidos" | C2-016..025 |
| Sistemas de exemplo VM/TIS/NPP (números travados) | tabela de regressão | C2-026..034, 036 |
| Formatos de entrada/saída, `-o` | "Formatos de entrada", "Saídas" | C2-037..042 |
| `check` | uso, formato CSV, códigos de saída | C2-043..048 |
| `verify` (conflito, lacuna, `--context`) | tabela de funções, descrição de opções | C2-049..053, 035 |
| Entradas inválidas (código 1) | "Código de saída" | C2-054..057 |
| Indeterminações | ver abaixo | C2-005, 018, 019, 024, 025, 035, 048, 058..068 |

Seções do texto que **não** geram casos executáveis: notas de cobertura/mutação do próprio projeto (JaCoCo/PIT,
18/11/2026), notas mínimas de build (Maven), relatórios publicados, descrição da suíte JUnit do projeto,
referências. São metadados do projeto, não comportamento observável da CLI; apenas os números que a tabela de
regressão atribui a sistemas de exemplo e os exemplos de suíte mínima conhecida viraram expectativas.

## 3. Decisões de interpretação (registro de fidelidade)

1. **Mascaramento** não é definido no texto. Foi formalizado pela definição usual (condição alvo muda, decisão
   muda, e a condição é *sensível* — inverter só ela inverte a decisão — nas duas linhas). Ela é usada **apenas**
   como evidência Z3 de existência de pares e de mínimo em casos em que coincide com causa única
   (`(A and B) or C`, `A and not B`, conjunções de ≤3). Onde diferem (`(A or B) and (C or D)`: mascaramento
   mínimo 4, causa única mínimo 5) só a causa única é determinada (C2-017); a de mascaramento é
   INDETERMINADA (C2-018).
2. **Tamanho de suíte "N+1"**: o texto diz "pode ter N+1" para guardas simples e fixa 4 e 3 testes para
   `(A and B) or C` e `A and not B` ("Exemplos conhecidos ... 4 testes ... 3"; o rótulo da expressão tem a letra
   `A` ausente, mas a expressão aparece íntegra na linha de `--unique-cause`). Esses dois valores são determinados;
   outros tamanhos só quando a estrutura é a mesma ou o Z3 fixa o mínimo.
3. **Tabela de regressão**: "Completos" é lido como requisitos cujas condições têm todas par; consequência
   usada: código de saída 0 se completos = requisitos (VM, NPP) e 2 caso contrário (TIS), por "2: ... condição
   sem par para analyze". Consistência numérica: testes = condições + requisitos em VM (21+5=26) e NPP (29+11=40);
   mutantes TIS 450 − 21 equivalentes = 429 ≥ 428 detectados.
4. **Códigos de saída**: 0 sem problemas; 1 entrada inválida; 2 resultado válido com condição sem par (`analyze`),
   condição não demonstrada ou esperado divergente (`check`), conflito ou lacuna (`verify`). `verify` sem
   `--context` não checa lacunas (a opção é que "confere se, nessa situação, sempre alguma guarda vale").
5. **Exemplo corrompido de `--exact`** (`((E or D) and (not ? or D)) or B`, "5 testes em vez de 6 da escolha
   gulosa"): a letra negada está ausente; qualquer completação seria suposição → C2-019 INDETERMINADO; o
   tamanho da suíte gulosa padrão também é INDETERMINADO.
6. **Arquivos de entrada** criados para o experimento (CSV de testes, JSON de decisões, `.mcdc`) seguem os formatos
   do texto. No JSON do exemplo a ação aparece como `"the_system_mode := choce"`; foi escrita `choice` (valor
   listado em `values`), o que não afeta a guarda nem as expectativas.
7. Cada **caso do oráculo = um teste** (unidade de contagem). Casos INDETERMINADOS (18) são registrados e **não
   executados** (decisão do pesquisador); não entram na cobertura.

## 4. Z3 independente

- Versão: Z3 5.4.1 (64 bit, build 145c0c51570a357cc558ce898ce77573ba9d4fbf), executável independente do `mcdc-z3`
  e da CLI avaliada; limite -T:60 por consulta; nenhuma resposta `unknown`/timeout.
- Consultas geradas por `gerar_smt.py` (arquivos `smt/*.smt2`, respostas `smt/*.out`, resumo `smt/RESUMO.md`):
  - z01–z06b: suíte mínima por k testes simbólicos (mascaramento e causa única); resultados: `(A and B) or C` → 4
    (ambas as variantes); `A and not B` → 3; `(A or B) and (C or D)` → 4 (masc.) / 5 (causa única);
    `A and B and C` → 4; condição única → 2; `(A and B) or not C` → 4.
  - z06_redundante_B: `A or (A and B)`: B nunca altera a decisão (`unsat`).
  - z07/z07b: `A and B` com restrição `not (A and B)` não tem linha alterando a saída (`unsat`), sem restrição tem (`sat`).
  - z08: restrição `not A or B`: linhas A=T,B=F `unsat` (2 de 8).
  - z09: `speed > 100 or (speed > 50 and rain)`: combinações (c1=T,c2=F,·) `unsat` (2 de 8); as demais `sat`.
  - z10: fronteira 100/101 e 50/51 (`unsat`/`sat`/`unsat`/`sat`).
  - z11: aritmética da tabela de regressão e 2^20.
  - z12: `check`: conjunto T1..T4 demonstra A,B,C; {T1,T2} só A; {T1,T3} só B; esperados T1..T4 = T,F,F,T.
  - z13/z14: `verify`: sobreposição de guardas e lacuna de contexto.
  - z15: informativo (não define expectativa).
  - z16: complementaridade dos operadores de comparação.
- Limitações: `sat`/`unsat` dizem respeito às fórmulas, **não provam fidelidade** da tradução texto→fórmula;
  a definição de mascaramento é uma escolha desta análise (item 3.1).
