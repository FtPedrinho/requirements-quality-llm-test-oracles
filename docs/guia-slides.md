# Guia para montar os slides do zero

Este guia substitui a ordem do deck anterior. São 23 slides em 5 seções. Cada slide traz o que vai na tela, a fórmula (quando houver) com a página do artigo de onde ela vem, e o que falar.

As fórmulas são as dos próprios artigos, sem a notação de derivada booleana:

- **[HV]** Hayhurst e Veerhusen, *A Practical Approach to Modified Condition/Decision Coverage* (`docs/20040086014.pdf`). Traz as definições do DO-178B e a regra n+1.
- **[KB]** Kapoor e Bowen, *A Formal Analysis of MCDC and RCDC Test Criteria* (`docs/A_formal_analysis_of_MCDC_and_RCDC_test_criteria.pdf`). Traz as definições formais de par, causa única e mascaramento.
- **[KV]** Kvalsvik, *Modified Condition/Decision Coverage in the GNU Compiler Collection* (`docs/2501.02133v1.pdf`). Traz a comparação de tamanho entre causa única e mascaramento.

As páginas citadas são as do PDF; nesses arquivos elas coincidem com o número impresso.

---

## Antes de começar

**Estrutura**

| Seção | Slides | Pergunta que responde |
|---|---|---|
| Abertura | 1–3 | Do que vamos falar e por quê |
| 1. O que é MC/DC | 4–6 | O que o critério exige |
| 2. É exaustivo? | 7–9 | Quantos testes ele pede e onde está o exponencial |
| 3. Causa única e mascaramento | 10–14 | As duas formas de mostrar o efeito de uma condição |
| 4. Artigos e fórmulas | 15–16 | De onde vem cada regra que a ferramenta usa |
| 5. A ferramenta (requisitos) | 17–21 | Como ela funciona, com exemplos reais |
| Encerramento | 22–23 | Referências e perguntas |

**Visual**

- Use um único modelo, fundo claro e uma fonte sem serifa (por exemplo Inter ou Roboto) para o texto.
- Use uma fonte monoespaçada (Roboto Mono ou JetBrains Mono) para tabelas verdade, expressões e saídas da ferramenta. Isso deixa as colunas T/F alinhadas.
- Use sempre as mesmas cores: **verde para T**, **vermelho para F** e **amarelo para destacar a condição que mudou** dentro de um par.
- Coloque o nome da seção num canto do slide, em letra pequena (por exemplo "2 · É exaustivo?"). Assim você não precisa de slides só para separar seções.
- Coloque uma ideia por slide, no máximo umas 25 palavras de texto corrido. O resto vai nas notas do apresentador.

**Fórmulas no Google Slides**

O Google Slides não tem editor de equações. Há dois caminhos:

1. Digitar a versão Unicode que está em cada slide abaixo. Ela usa caracteres como `≠`, `∀`, `∃`, `∈`, `ⁱ` e funciona em fontes como Cambria Math, Noto Sans Math ou STIX Two Math. Se algum símbolo virar um quadradinho, troque a fonte daquela caixa.
2. Gerar uma imagem a partir da versão LaTeX, também incluída em cada slide, e colar a imagem.

**Como rodar os exemplos**

Os exemplos foram rodados com `./mcdc analyze ...` na raiz do projeto. Se quiser trocar os prints, rode os mesmos comandos e cole a saída em fonte monoespaçada.

---

## Abertura

### Slide 1 · Capa

**Na tela**
- Título: **MC/DC: o que é, quanto custa e como automatizar a partir de requisitos**
- Subtítulo: *Cobertura de condição/decisão modificada aplicada a requisitos*
- Seu nome, grupo ou instituição, e a data
- Opcional: um desenho pequeno de uma porta lógica `and` com 3 entradas, que volta no slide 8

**Fala**
"Vou mostrar o que é o MC/DC, quanto ele custa de verdade, as duas formas de calcular e uma ferramenta que gera os testes direto do requisito."

### Slide 2 · Roteiro

**Na tela**: as 5 seções numeradas, uma por linha.
1. O que é MC/DC
2. Ele é exaustivo?
3. Causa única e mascaramento
4. Os artigos e as fórmulas
5. A ferramenta no contexto de requisitos

**Fala**
"A parte de código-fonte fica para depois; hoje é só requisito."

### Slide 3 · Por que MC/DC

**Na tela**
- "DO-178B/C, nível A: software cuja falha pode ser catastrófica"
- "Para esse nível, os testes precisam atingir MC/DC"
- Citação curta: *"the size and complexity of today's avionics products prohibit exhaustive testing"* [HV, p. 1]

**Fala**
"No nível A, testar tudo não é viável. O MC/DC foi criado para dar quase a mesma confiança que testar tudo, com muito menos testes."
- Base: [HV, p. 1], *"developed to provide many of the benefits of exhaustive testing of Boolean expressions without requiring exhaustive testing"*.

---

## Seção 1 · O que é MC/DC

### Slide 4 · Condição e decisão

**Na tela**
- **Condição**: expressão booleana sem operador booleano. Exemplos: `A`, `speed > 100`.
- **Decisão**: condições ligadas por `and`, `or`, `not`. Exemplo: `(A and B) or C`.
- **Regra importante**: se uma condição aparece duas vezes, cada aparição é uma condição diferente.
  - Exemplo: `(A and B) or (A and C)` tem 3 entradas (A, B, C) e 4 condições (A, B, A, C).

**Fonte**: definições do glossário do DO-178B, citadas em [HV, p. 2].

**Fala**
"Vou chamar de 'entrada' a variável e de 'condição' cada lugar onde ela aparece. Essa diferença vai importar na seção 3."

### Slide 5 · A definição do MC/DC

**Na tela**: as quatro exigências, numa lista com a última destacada.
1. Todo ponto de entrada e saída executado ao menos uma vez
2. Toda condição assume T e F ao menos uma vez
3. Toda decisão assume T e F ao menos uma vez
4. **Cada condição mostra que afeta o resultado da decisão sozinha**

E, embaixo, a frase do padrão: *"varying just that condition while holding fixed all other possible conditions"*.

**Fonte**: [HV, p. 2] e [KB, p. 7]. Kapoor e Bowen dizem que é a quarta exigência que torna o MC/DC um critério único.

**Fala**
"Os três primeiros itens outros critérios já pediam. O que é próprio do MC/DC é o quarto: provar que cada condição, sozinha, muda o resultado."

### Slide 6 · O par de independência

**Na tela**

Exemplo: `A and B and C`

| Teste | A | B | C | Resultado |
|---|---|---|---|---|
| V1 | T | T | T | **T** |
| V5 | **F** | T | T | **F** |

Só A mudou, e o resultado mudou. Então esse par mostra o efeito de A.

**Fórmula** [KB, Definição 1, p. 11]

- Unicode: `f(v) ≠ f(vⁱ)`
- LaTeX: `f(v) \neq f(v^{i})`
- Leitura: "vⁱ é o mesmo teste v com só a condição i invertida. Se o resultado muda, o teste v é **sensível** a i."
- O par `(v, vⁱ)` é chamado de **par vizinho sensível**. O conjunto de todos esses pares de uma entrada é ψᵢ ("psi i") [KB, Def. 2 e 3, p. 11].

**Fala**
"Um teste sozinho não prova nada. É o par que prova: duas execuções que diferem só em A, com resultados diferentes. O MC/DC pede um par desses para cada condição."

---

## Seção 2 · É exaustivo?

> **Mensagem da seção**: o MC/DC **não** é exaustivo. O número de testes cresce em linha reta com o número de condições. O que cresce de forma exponencial é o trabalho de **encontrar** esses testes quando se olha a tabela verdade inteira, e isso é custo da ferramenta, não de quem executa os testes.

### Slide 7 · Teste exaustivo: 2ⁿ

**Na tela**
- "Com n entradas booleanas, testar todas as combinações exige 2ⁿ testes"
- Tabela de crescimento:

| n | 2ⁿ |
|---|---|
| 3 | 8 |
| 10 | 1.024 |
| 20 | 1.048.576 |
| 30 | 1.073.741.824 |

**Fórmula** [KB, p. 10]

- Unicode: `testes exaustivos = 2ⁿ`
- LaTeX: `|T_{exaustivo}| = 2^{n}`
- Texto do artigo: *"In order to completely verify a Boolean formula with n inputs, 2ⁿ test cases are required"*.
- O artigo completa: os critérios existentes buscam uma solução prática que exige um número **linear** de testes.

**Fala**
"Isso é o exaustivo: a tabela verdade inteira. Com 30 entradas, passa de um bilhão de testes."

### Slide 8 · Quanto o MC/DC pede: n+1

**Na tela**

Porta `and` com 3 entradas [HV, p. 3, Tabela 2]:

| Teste | A | B | C | Resultado |
|---|---|---|---|---|
| 1 | T | T | T | T |
| 2 | **F** | T | T | F |
| 3 | T | **F** | T | F |
| 4 | T | T | **F** | F |

- Regra do `and`: um teste com tudo T, e um teste para cada entrada sozinha em F, ou seja, **n + 1 testes**.
- Regra do `or`: um teste com tudo F, e um teste para cada entrada sozinha em T, também n + 1 [HV, p. 4].
- Comparação:

| n | exaustivo 2ⁿ | MC/DC (causa única) |
|---|---|---|
| 3 | 8 | 4 a 6 |
| 10 | 1.024 | 11 a 20 |
| 20 | 1.048.576 | 21 a 40 |
| 30 | 1.073.741.824 | 31 a 60 |

**Fórmula** [KB, Tabela I, p. 19]

- Unicode: `n + 1 ≤ |T| ≤ 2n`
- LaTeX: `n + 1 \le |T| \le 2n`
- Leitura: "cada condição precisa de um par, ou seja, 2 testes. No pior caso nenhum teste é compartilhado (2n). No melhor, um teste serve a vários pares (n+1)."

**Fala**
"Aqui está a resposta: o MC/DC é linear. Com 30 entradas, no máximo 60 testes, contra um bilhão."

### Slide 9 · Então onde está o exponencial?

**Na tela**: duas caixas lado a lado.

**Caixa 1: achar os testes**
- Para descobrir os pares, a ferramenta monta a tabela verdade inteira: **2ⁿ linhas**.
- Medido na ferramenta: com 20 entradas são cerca de 1 milhão de linhas, analisadas em 0,2 s na causa única e em cerca de 5 s no mascaramento.
- Esse custo é da ferramenta. O testador continua executando só n+1 a 2n testes.

**Caixa 2: fórmulas muito grandes**
- O número de testes cresce com o número de **condições**, não de entradas.
- Para algumas funções, escrevê-las com `and`/`or`/`not` exige um número exponencial de condições. O exemplo do artigo é a função paridade.
- Nesses casos, e só por isso, o teto chega a 2ⁿ [KB, p. 19–20, Tabela I, linhas UCMS e Masking].

**Fala**
"A intuição de que o MC/DC é exponencial tem fundamento, mas está no lugar errado. O exponencial aparece para a ferramenta, que precisa olhar todas as combinações para escolher poucas, e em fórmulas gigantes. Para quem roda os testes, o MC/DC é linear."

---

## Seção 3 · Causa única e mascaramento

### Slide 10 · Quando uma condição não pode mudar sozinha

**Na tela**
- Expressão: `(A and B) or (not A and C)`, com as duas aparições de A marcadas como **A#1** e **A#2**.
- "Inverter A#1 inverte A#2 junto: é a mesma variável."
- Outro caso: `speed > 50` e `speed > 100`. Ir de 49 para 101 muda as duas condições ao mesmo tempo.
- Nome disso: **acoplamento** de condições.
  - **Forte**: mudar uma sempre muda a outra, como A#1 e A#2.
  - **Fraco**: às vezes muda, como `i > 50` e `i < 100`.
  - Fonte: [KB, p. 7].

**Fala**
"A definição pede para mudar uma condição mantendo as outras fixas. Quando as condições estão acopladas, isso é impossível, e o padrão não diz o que fazer [KB, p. 7]. As duas variantes a seguir são as duas respostas a esse problema."

### Slide 11 · Causa única

**Na tela**
- Ideia: **só uma condição muda** entre os dois testes do par. O par é sempre de vizinhos.
- Exemplo `(A and B) or C`:

| Condição | Par | Testes |
|---|---|---|
| A | V2, V6 | **T**TF → T, **F**TF → F |
| B | V2, V4 | T**T**F → T, T**F**F → F |
| C | V3, V4 | TF**T** → T, TF**F** → F |

Suíte: 4 testes (V2, V3, V4, V6), igual a n + 1.

**Fórmula** [KB, Def. 9a e 10, p. 15–16]

- Unicode: `∀i ∃ t₁, t₂ ∈ T : (t₁, t₂) ∈ ψᵢ`
- LaTeX: `\forall i\ \exists\, t_1, t_2 \in T : (t_1, t_2) \in \psi_i`
- Leitura: "para toda condição i, a suíte T tem dois testes que formam um par vizinho sensível de i."
- Kapoor e Bowen definem a causa única pura só para condições **não acopladas** (Def. 10). Com repetição, usam a forma forte UCMS: o par continua de vizinhos, mas precisa mostrar o efeito de **cada aparição** (Def. 8 e 11, p. 15–16).

**Fala**
"Causa única é a leitura literal do padrão: mudo só uma coisa, e o resultado muda. É o mais fácil de explicar a um auditor, mas é o mais rígido."

### Slide 12 · Mascaramento

**Na tela**
- Ideia: outras condições **podem mudar**, desde que não consigam afetar o resultado naquele momento. Diz-se que elas estão mascaradas.
- Como uma condição fica mascarada:
  - em `X and Y`, se Y = F, o valor de X não importa;
  - em `X or Y`, se Y = T, o valor de X não importa.
- Exemplo em `(A and B) or (not A and C)`, par de B:

| Teste | A | B | C | Resultado |
|---|---|---|---|---|
| V2 | T | **T** | F | T |
| V3 | T | **F** | T | F |

C também mudou, mas com A = T a parte `not A and C` é F de qualquer jeito. C está mascarada, e só B pode ter causado a mudança.

**Fórmula** [KB, Def. 12, p. 17]. As regras "and com F" e "or com T" do quadro estão em [KV, p. 2].

- Unicode: `∀ xᵢʲ ∈ F ∃ v₁, v₂ ∈ T : v₁, v₂ sensíveis a xᵢʲ, v₁[i] ≠ v₂[i], f(v₁) ≠ f(v₂)`
- LaTeX: `\forall x_i^j \in F\ \exists\, v_1, v_2 \in T : v_1, v_2 \text{ sensíveis a } x_i^j,\ v_1[i] \neq v_2[i],\ f(v_1) \neq f(v_2)`
- Leitura: "para cada condição, a suíte tem dois testes em que a condição está ativa (não mascarada), tem valores diferentes, e o resultado é diferente."
- Note que a fórmula **não** exige `v₂ = v₁ⁱ`, ou seja, os testes não precisam ser vizinhos. O artigo diz isso de forma explícita na p. 17.

**Fala**
"No mascaramento eu posso mudar outras coisas, desde que eu prove que elas não tinham como influenciar. Isso dá mais liberdade para escolher os testes."

### Slide 13 · As duas no mesmo requisito

**Na tela**: o requisito `(A and B) or (not A and C)` rodado nas duas variantes, em duas colunas.

| | Causa única | Mascaramento |
|---|---|---|
| Testes | **6** (V1, V2, V3, V5, V6, V7) | **4** (V2, V3, V6, V7) |
| Par de B | V1, V3 (só B muda) | V2, V3 (C mascarada) |
| Par de C | V5, V6 (só C muda) | V7, V6 (B mascarada) |

Comandos:
```
./mcdc analyze "(A and B) or (not A and C)" --unique-cause
./mcdc analyze "(A and B) or (not A and C)"
```

**Fala**
"Mesmo requisito, 6 contra 4 testes. A diferença vem da condição repetida: o mascaramento aproveita os testes em que uma parte da expressão está desligada."

### Slide 14 · Qual escolher

**Na tela**

| | Causa única | Mascaramento |
|---|---|---|
| Testes, mínimo [KV, p. 2] | n + 1 | ⌈2√n⌉ |
| Testes, máximo [KB, Tab. I] | 2n | 2 × nº de condições, conta nossa a partir do Teorema 1 (2ⁿ só em fórmulas gigantes, slide 9) |
| Aceita condição repetida | só na forma forte (UCMS) | sim |
| Detecção de defeitos | em geral, a mesma [KV, p. 2, citando Chilenski] | em geral, a mesma |

- Recomendação: o **mascaramento** é o padrão da ferramenta e o que o GCC 14 usa [KV, p. 2]. A **causa única** fica como opção (`--unique-cause`).

**Fala**
"Pela pesquisa de Chilenski, as duas pegam praticamente os mesmos defeitos. O mascaramento pede menos testes e aceita mais casos, por isso é o padrão."

---

## Seção 4 · Os artigos e as fórmulas

### Slide 15 · Os artigos base

**Na tela**: três linhas, uma por artigo, cada uma com o que ele traz para o trabalho.

| Artigo | O que usamos |
|---|---|
| Hayhurst e Veerhusen (NASA) | Definições do DO-178B; regra n+1 para `and` e `or`; uma condição repetida conta como duas |
| Kapoor e Bowen | Definições formais de par sensível, causa única (UC, UCMS) e mascaramento; limites de tamanho (Tabela I); condição sem par = redundante |
| Kvalsvik (GCC 14) | Mascaramento como padrão; comparação de tamanho entre as variantes |

**Fala**
"O primeiro artigo diz o que o padrão pede. O segundo transforma isso em fórmulas que um programa pode calcular. O terceiro mostra um compilador real fazendo isso."

### Slide 16 · As fórmulas que a ferramenta usa

**Na tela**: uma tabela-resumo. Este é o slide para voltar em caso de pergunta.

| Passo | Fórmula | Fonte |
|---|---|---|
| Combinações possíveis | `2ⁿ` linhas na tabela verdade | [KB, p. 10] |
| Teste sensível a i | `f(v) ≠ f(vⁱ)` | [KB, Def. 1] |
| Par de causa única | `(v, vⁱ)` sensível, para cada aparição | [KB, Def. 8 e 11] |
| Par de mascaramento | `v₁[i] ≠ v₂[i]`, `f(v₁) ≠ f(v₂)`, ambos sensíveis a i | [KB, Def. 12] |
| Suíte completa | `∀ condição ∃ t₁, t₂ ∈ T` formando um par | [KB, Def. 9] |
| Tamanho da suíte | `n + 1 ≤ \|T\| ≤ 2n` | [KB, Tab. I] |
| Condição sem nenhum par | a entrada é redundante, ou a fórmula tem aparições a mais | [KB, Prop. 1 e 3; p. 15] |
| Escolha da suíte mínima | guloso: pega o teste que cobre mais pares ainda sem cobertura | escolha da ferramenta |

**Fala**
"Tudo nesta tabela vem dos artigos, menos a última linha. Escolher a menor suíte é um problema difícil, e a ferramenta usa uma heurística gulosa: rápida, e quase sempre chega no n+1."

---

## Seção 5 · A ferramenta no contexto de requisitos

### Slide 17 · O pipeline

**Na tela**: um diagrama de caixas da esquerda para a direita.

```
Requisito  →  Parser  →  Condições  →  Tabela   →  Pares  →  Suíte    →  Relatório
(expressão)   (árvore)   (A#1, A#2)    verdade     (UC ou    mínima      texto, JSON,
                                       (2ⁿ)        mask.)                CSV, Gherkin
                                         ↑
                                Z3 (opcional): marca linhas impossíveis
                                e dá valores concretos
```

O que cada caixa faz, em uma linha:

- **Requisito**: uma expressão (`"(A and B) or C"`), um arquivo `.mcdc` com vários requisitos, ou o JSON de decisões do DFRS.
- **Parser**: aceita `and`/`&&`/`/\`, `or`/`||`/`\/`, `not`/`!` e comparações (`speed > 100`).
- **Condições**: cada aparição vira uma condição (DO-178B, [HV, p. 2]).
- **Tabela verdade**: todas as 2ⁿ combinações, com o resultado de cada uma.
- **Pares**: aplica a Def. 11 (causa única) ou a Def. 12 (mascaramento).
- **Suíte mínima**: o guloso do slide 16, mostrando qual teste demonstra qual condição.
- **Relatório**: o mesmo resultado em texto, JSON, CSV ou cenário Gherkin.

**Fala**
"Entra o requisito, sai a lista de testes com o motivo de cada um. Hoje a entrada é o requisito; o código-fonte é o próximo passo."

### Slide 18 · Exemplo 1: um requisito comum

**Na tela**: o comando e a saída reduzida.

```
$ ./mcdc analyze "(A and B) or C" --unique-cause

Suíte mínima (4 testes):
  V2  TTF  -> T   demonstra A, B
  V3  TFT  -> T   demonstra C
  V4  TFF  -> F   demonstra B, C
  V6  FTF  -> F   demonstra A

Cobertura MC/DC: completa
```

**Fala**
"Três condições, quatro testes: exatamente n + 1. E cada teste diz para que serve. Isso é a rastreabilidade que o auditor pede."

### Slide 19 · Exemplo 2: requisito com condição sem efeito

**Na tela**

```
$ ./mcdc analyze "freio_acionado or (freio_acionado and pedal_pressionado)"

Cobertura MC/DC: incompleta, sem par para freio_acionado#2, pedal_pressionado
  pedal_pressionado: redundante: não muda o resultado em nenhuma combinação;
                     o requisito pode ser simplificado
```

**Base**: [KB, Prop. 1 e 3, p. 12 e 15]. Se uma entrada não influencia o resultado, ela não tem par, e nenhuma suíte consegue MC/DC.

**Fala**
"Aqui a ferramenta acha um problema no requisito, não no teste. `pedal_pressionado` nunca muda nada, porque o requisito se reduz a `freio_acionado`. Isso aparece antes de escrever uma linha de código."

### Slide 20 · Exemplo 3: requisito com números

**Na tela**: duas colunas, sem Z3 e com Z3, para `speed > 50 and (speed > 100 or rain)`.

Sem Z3, a suíte inclui:
```
V6  FTF  -> F   demonstra speed > 50
```
Isso pede `speed > 50` falso e `speed > 100` verdadeiro ao mesmo tempo, o que é **impossível**.

Com Z3 (`--z3`):
```
V5, V6 marcadas (impossível)
V2  TTF  [speed = 101, rain = false]
V3  TFT  [speed = 51,  rain = true]
V4  TFF  [speed = 51,  rain = false]
V7  FFT  [speed = 0,   rain = true]
```

**Fala**
"Este é o acoplamento do slide 10, na prática. Sozinha, a tabela não sabe que as duas condições falam da mesma velocidade. O Z3 descarta as combinações impossíveis e ainda dá o valor de entrada de cada teste."

### Slide 21 · Próximos passos

**Na tela**
- **Feito**: o contexto de requisitos (expressão, arquivo `.mcdc` e JSON do DFRS); causa única e mascaramento; Z3; avaliação de testes existentes.
- **Próximo**: o contexto de código.
  - Medir o MC/DC de um programa já testado, no estilo do gcov.
  - Integração com a NAT2TEST: os requisitos em linguagem natural chegam ao DFRS, depois ao JSON, à ferramenta e ao visualizador.
  - Plugin Eclipse.

**Fala**
"Hoje mostrei a ferramenta olhando requisitos. O mesmo motor vai servir para o código: muda só de onde vem a expressão."

---

## Encerramento

### Slide 22 · Referências

**Na tela**
1. K. J. Hayhurst, D. S. Veerhusen. *A Practical Approach to Modified Condition/Decision Coverage*. 20th Digital Avionics Systems Conference (DASC), 2001. DOI 10.1109/DASC.2001.963305.
2. K. Kapoor, J. P. Bowen. *A Formal Analysis of MCDC and RCDC Test Criteria*. Software Testing, Verification and Reliability 15(1):21–40, 2005. DOI 10.1002/stvr.306.
3. J. Kvalsvik. *Modified Condition/Decision Coverage in the GNU Compiler Collection*. arXiv:2501.02133, 2025.
4. J. J. Chilenski, S. P. Miller. *Applicability of Modified Condition/Decision Coverage to Software Testing*. Software Engineering Journal, 1994. Citado em [HV].
5. RTCA DO-178C / DO-330.

> Títulos e autores conferidos nos PDFs; local, ano e DOI conferidos nos registros da IEEE e da Wiley. O PDF de Kapoor e Bowen em `docs/` é a versão preliminar de 2004; as páginas citadas são as desse PDF.

### Slide 23 · Perguntas

**Na tela**: "Obrigado. Perguntas?" e, opcionalmente, o comando do slide 18 para quem quiser testar.

**Perguntas prováveis, para as notas**

- *"Então MC/DC é exaustivo?"* Não. Volte ao slide 8: são de n+1 a 2n testes. O exponencial é a análise (slide 9).
- *"Por que mascaramento e não causa única?"* Slide 14: detecção equivalente e menos testes.
- *"De onde vem tal fórmula?"* Slide 16.
- *"E se a condição for impossível?"* Slide 20.
