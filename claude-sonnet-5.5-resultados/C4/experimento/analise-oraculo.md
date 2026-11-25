# Análise documental C4 (antes de ler o SUT)

Fonte normativa exclusiva: `documentacao/tool-readme-C4.md`, SHA-256
`D6BC0A588CD9A7DF7F1F566573944FA5CB1707BBA676B4E9854CAD2CC5440FC2` (conferido
antes da leitura). Critério estrito do pesquisador: documentação como verdade,
nenhum preenchimento por suposição, INDETERMINADO sempre que omissão,
corrupção, ambiguidade ou conflito impedir expectativa única.

## 1. Estado do texto

O texto começa no meio de uma tabela (a linha 1 é um fragmento) e está
degradado: letras e palavras (inclusive identificadores de expressões, nomes de
opções e comandos) foram suprimidas, há marcas `[trecho omitido]`, e há pares de
afirmações explicitamente contraditórias. Nada foi reconstruído. Casos só são
DETERMINADOS quando o trecho usado está legível o bastante para afirmar um
resultado único e observável.

## 2. Inventário e decisão

| Região do texto | Conteúdo | Tratamento |
|---|---|---|
| Linhas 1–9 (formatos `csv`, `truth-csv`) | conteúdo dos formatos; regra de saída | conflito sobre `truth-csv` (I01); `csv` ambíguo (I02) |
| Linhas 11–71 (exemplos) | comandos com comentários, sem saída esperada | os com expressão/arquivo íntegros viram casos de propriedade (D22–D24, D30, D34); os corrompidos são I13–I20, I28 |
| Linhas 73–101 (como funciona) | 6 passos | passos 2, 3, 4, 5 têm regras contraditórias (I03–I06); tabela-verdade 2ⁿ usada (D22–D26) |
| Linha 101 e 405 (limites 20/12/30; 1000 pares) | limites | aceitação dentro do limite (D26–D28); comportamento acima: omissão (I10) |
| Linhas 103–123 (arquitetura) | módulos, dependências | estrutura (D35–D38); Z3 externo × biblioteca: conflito (I08) |
| Linhas 125–181 (qualidade) | JaCoCo/PIT, notas mínimas | notas mínimas no `pom.xml` (D39–D40); métricas e regras de build: conflitos/ não comportamento (I30, I33) |
| Linhas 183–221 (relatórios) | caminhos | existência (D41) |
| Linhas 223–373 (suíte) | descrições de testes, tempos, tabela de regressão | tabela de regressão numérica: D01–D21; propriedades legíveis: D29–D32, D33; descrições sem resultado observável, tempos: I11, I26, I31, I34–I36 |
| Linhas 375–401 | como rodar, recomendações | Maven indisponível / sem resultado observável (I33) |
| Linhas 403–413 (limites) | parênteses, paridade, guardas | paridade (D29); parênteses em conflito (I21–I22); guardas temporais ambíguo (I32) |
| Linhas 415–423 | referências | sem expectativa |

## 3. Casos DETERMINADOS (42)

Fonte de cada expectativa: trecho literal registrado em `oraculo.json`.

* **Tabela de “números travados de regressão” (linhas 285–295), D01–D21.** Para
  VM, TIS e NPP: requisitos, condições, combinações, combinações impossíveis,
  testes, mutantes totais e equivalentes, conflitos (comando `verify`). A coluna
  “Completos” e a coluna “Pegos” (esta por causa do conflito de parênteses)
  **não** são usadas. A aritmética interna da tabela foi verificada no Z3
  (z01 A01–A04) — consistência, não fidelidade.
* **D22–D26:** regra 2ⁿ sobre entradas distintas (linha 79), “cada aparição é
  uma condição própria (#1, #2)” (linha 25), limite de 20 entradas.
* **D27–D28:** limites de 12 (Z3 linha a linha) e 30 (modo direto).
* **D29:** paridade de 3 entradas exige 8 testes (linha 411).
* **D30–D34:** propriedades legíveis de relatórios e do modo direto.
* **D35–D42:** estrutura documentada do repositório (módulos, dependências,
  propriedades `qualidade.*` do `pom.xml`, relatórios e arquivos de exemplo).
  São verificações documento–repositório, não de comportamento da CLI.

Observáveis que o texto não define (nome de campo JSON, rótulo de erro) serão
mapeados na suíte após a inspeção do SUT somente para saber **como medir**;
nenhuma expectativa será alterada por isso. Se a medição não for possível, o
caso é registrado como erro técnico/não avaliado, nunca como aprovação ou falha.

## 4. Casos INDETERMINADOS (36)

Listados em `oraculo.json` (I01–I36) com tipo de indeterminação. Resumo:

* **Conflitos textuais (Z3: cada afirmação sat isolada, unsat na conjunção):**
  `truth-csv` (z02), `unsat`/`sat` (z03), critério de par (z04), guloso × exato
  (z05), redundante × bloqueada (z06), parênteses (z07), arquitetura do Z3 e
  tempo (z08), cobertura de linhas × desvios (z09), significado da nota de
  mutação (z10), regra global de aprovação (z11).
* **Corrupção:** expressões com identificador suprimido (I13–I17), comando
  `check` e opções (I19, I20), opção de saída em arquivo (I28).
* **Omissão:** acima dos limites (I10), código de saída (I12), aviso sem Z3
  (I09), esquemas de entrada (I26), saídas de exemplos (I27), tempos (I11).
* **Ambiguidade:** csv (I02), “Completos” (I23), “mesmo número” (I24), N + 1
  “pode ter” (I25), “contagem” de mutantes (I29).

### Decisão sobre a regra de satisfatibilidade (I03)

A linha 83 afirma que sua interpretação “substitui a distinção anterior e vale
para todas as operações”. Isso estabelece precedência, mas **não** define qual
fórmula é enviada ao Z3; sem isso não há expectativa observável única sobre
quais combinações são descartadas. Por isso nenhum caso verifica *quais*
combinações são impossíveis; só as contagens numéricas da tabela de regressão
são usadas.

### Desvio sobre obrigatoriedade do Z3

Linhas 119–123 se contradizem sobre processo externo × biblioteca e sobre se o
Z3 é obrigatório. Seguindo a instrução do pesquisador, o Z3 permanece no `PATH`
em todos os casos, o que só é compatível com a leitura “processo externo”.
Isso é um desvio de isolamento/execução registrado no relatório.

## 5. Z3 (independente do `mcdc-z3`)

Z3 5.4.1 (`z3.exe` standalone), consultas em `z3/*.smt2`, respostas em
`z3/*.out`, resumo em `z3/resumo-z3.csv`. Resultado: 56 verificações, todas
conforme o esperado pelo autor, sem `unknown` nem timeout (limite `-T:60`).
`sat`/`unsat` dizem respeito às fórmulas, não à fidelidade da tradução.

## 6. Revisão

Autorrevisão (um único revisor, o próprio modelo). Nenhum revisor independente.
