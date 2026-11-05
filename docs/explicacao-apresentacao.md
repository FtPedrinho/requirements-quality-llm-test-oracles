# Explicação da apresentação: o que cada slide quer dizer, e como os algoritmos funcionam

Complemento do [roteiro](roteiro-apresentacao.md). O roteiro diz o que falar; este documento explica o porquê de cada coisa, para você ter segurança nas perguntas. A primeira parte explica os algoritmos com calma, executando cada um à mão. A segunda percorre os 25 slides.

---

# Parte 1 · Os algoritmos, passo a passo

Todos os exemplos usam a decisão do slide 3:

```
D = (A and B) or C
```

## 1.1 A tabela verdade como números binários

Com 3 condições há 2³ = 8 combinações. A ferramenta numera as linhas de 0 a 7 e escreve cada número em binário com 3 dígitos. Cada dígito é uma condição, na ordem A, B, C, e a convenção é **0 = verdadeira, 1 = falsa**:

| Linha | Binário | A | B | C | D = (A and B) or C |
|---|---|---|---|---|---|
| V1 | 000 | T | T | T | T |
| V2 | 001 | T | T | F | T |
| V3 | 010 | T | F | T | T |
| V4 | 011 | T | F | F | F |
| V5 | 100 | F | T | T | T |
| V6 | 101 | F | T | F | F |
| V7 | 110 | F | F | T | T |
| V8 | 111 | F | F | F | F |

O nome V1…V8 é só o número da linha mais 1.

**Por que binário?** Porque inverter uma condição vira uma operação de bits. A condição A é o bit da esquerda, que vale 100 em binário (4 em decimal). Para inverter só A numa linha, basta ligar ou desligar esse bit. Além disso, a ferramenta não precisa guardar "A=T, B=T, C=F" em cada linha: o próprio número da linha já diz isso. É o que permite 20 condições (1.048.576 linhas) caberem em memória.

## 1.2 Algoritmo 1: pares de causa única

**O que se procura.** Um par de independência de causa única para a condição A é um par de linhas em que:

1. só A muda, e B e C ficam iguais;
2. o resultado D muda.

Se isso acontece, fica provado que A, sozinha, muda a resposta.

**Como a ferramenta acha.** Para cada linha em que A é verdadeira (bit de A = 0), ela calcula a linha "gêmea", a mesma linha com o bit de A ligado, ou seja, `r | 100`. Depois compara os resultados.

| Linha com A = T | Gêmea (`r | 100`) | D na linha | D na gêmea | Par? |
|---|---|---|---|---|---|
| 000 (V1) | 100 (V5) | T | T | não: o resultado não mudou |
| 001 (V2) | 101 (V6) | T | F | **sim** |
| 010 (V3) | 110 (V7) | T | T | não |
| 011 (V4) | 111 (V8) | F | F | não |

Por que só V2/V6? Em V1 e V3, C é verdadeira, e um `or` com um lado verdadeiro dá T de qualquer jeito: A não consegue mudar nada. Em V4, B é falsa, então `A and B` é falso de qualquer jeito, e com C falsa D fica F. Só em V2 (B verdadeira, C falsa) A está "no comando".

Fazendo o mesmo para as outras:

- **B** (máscara 010): só o par (V2, V4).
- **C** (máscara 001): (V3, V4), (V5, V6) e (V7, V8). C decide sempre que `A and B` é falso, o que acontece em três situações.

**A fórmula do slide 5.** A caixa branca diz a mesma coisa em linguagem matemática:

- `v′ = v com só xᵢ invertida`: v′ é a gêmea de v.
- `(v, v′) é par de xᵢ ⇔ v(xᵢ) = T e D(v) ≠ D(v′)`: é par quando, partindo da linha em que a condição é verdadeira, o resultado muda.
- `∂D/∂xᵢ (v) = D(v|xᵢ=T) ⊕ D(v|xᵢ=F) = 1`: esta é a **derivada booleana**. "D com xᵢ verdadeira" ou-exclusivo "D com xᵢ falsa" dá 1 exatamente quando os dois resultados são diferentes, ou seja, quando xᵢ faz diferença naquela situação. A equação com ou-exclusivo é a de Kapoor e Bowen (seção 5, p. 12 do PDF), que escrevem `f|xᵢ=0 ⊕ f|xᵢ=1 = 1` a partir da expansão de Shannon e chamam o conjunto desses pares de ψᵢ (psi i). O símbolo ∂ e o nome "derivada booleana" (ou "diferença booleana") vêm da literatura clássica de circuitos (Akers, 1959; Sellers, Hsiao e Bearnson, 1968), não do artigo deles.

**Custo.** Para cada uma das N condições, a ferramenta olha metade das 2^N linhas. O total é proporcional a N · 2^N.

**E se a mesma variável aparecer duas vezes?** Em `(A and B) or (not A and C)` há dois A. Inverter "o A" inverte os dois ao mesmo tempo, porque é a mesma variável. Para provar cada aparição separadamente, a ferramenta exige mais uma coisa: que aquela aparição específica decida o resultado nos dois testes (o conceito de "decide" é o do algoritmo 2). Essa é a variante **UCMS** (causa única com mascaramento forte). Sem repetição, essa exigência extra é sempre verdadeira e não muda nada.

## 1.3 Algoritmo 2: mascaramento

**A ideia.** A causa única é exigente: só a condição pode mudar. Às vezes outras condições mudam junto, mas não importam, porque estão "mascaradas" naquela situação. O mascaramento aceita esses pares.

**O conceito central: "decidir".** Uma condição c *decide* o resultado numa linha v quando, invertendo **só aquela aparição** de c, o resultado se inverte:

```
decide(c, v) ⇔ D(v) ≠ D[c ↦ ¬c](v)
```

`D[c ↦ ¬c]` é a decisão com só aquela ocorrência negada. Note a diferença sutil para o algoritmo 1: aqui não se compara com outra linha da tabela, e sim se pergunta "nesta linha, essa condição está no comando?".

**O algoritmo**, como no slide 6:

1. `T(c)` = linhas possíveis em que c é verdadeira **e** decide;
2. `F(c)` = linhas possíveis em que c é falsa **e** decide;
3. `pares(c)` = combinações de uma linha de T(c) com uma de F(c) cujos resultados são diferentes.

**Executando para C em `(A and B) or C`.** C decide quando `A and B` é falso (com `A and B` verdadeiro, o `or` já dá T e C não importa). Isso vale nas linhas em que A ou B é falsa:

- T(C), com C verdadeira e decidindo: V3 (TFT), V5 (FTT), V7 (FFT), todas com D = T;
- F(C), com C falsa e decidindo: V4 (TFF), V6 (FTF), V8 (FFF), todas com D = F.

Toda combinação de um lado com o outro tem resultados opostos, então são 3 × 3 = **9 pares**. Na causa única eram só 3: os pares "vizinhos" (V3,V4), (V5,V6) e (V7,V8).

**O exemplo do slide: V7 (FFT) e V4 (TFF).** Entre esses dois, A e C mudam. Na causa única isso não vale. No mascaramento vale, porque nos dois testes B é falsa, então `A and B` é falso independentemente de A: A não tem como influenciar, está mascarada. Quem decide é C, e o resultado muda de T para F.

**Por que todo par de causa única é par de mascaramento?** Num par de causa única, só c muda e o resultado muda. Então, em cada uma das duas linhas, inverter c inverte o resultado: c decide nas duas. As três regras do mascaramento são cumpridas. O contrário não vale, como mostra o par V7/V4.

**Por que aceitar mais pares importa?** Quando algumas combinações são impossíveis (slide 16), a causa única pode ficar sem nenhum par válido, e o mascaramento ainda encontrar um.

**Relação com a literatura.** É a Definição 12 de Kapoor e Bowen ("condition sensitive"), e é o que o GCC 14 calcula, por outro caminho: a partir do diagrama de decisão binária do programa compilado.

## 1.4 Algoritmo 3: suíte mínima gulosa

**O problema.** Para cada condição, precisamos de um par dentro da suíte. Queremos o menor número total de testes. Como pares de condições diferentes podem compartilhar testes, escolher bem faz diferença.

Formalmente, como na caixa do slide 7:

```
mín |S|  sujeito a  ∀c ∃(t, f) ∈ pares(c) : t ∈ S e f ∈ S
```

"Encontre o menor conjunto de testes S tal que, para toda condição c, exista algum par dela inteiro dentro de S." É um problema conhecido como **cobertura de conjuntos**, que é difícil (NP-difícil) de resolver exatamente em geral. Por isso a ferramenta usa uma heurística gulosa.

**A heurística**, em quatro passos:

1. **Comece pelas condições com menos opções.** Quem tem um único par não tem escolha; resolvê-la primeiro cria testes que outras condições podem aproveitar.
2. **Para cada condição, escolha o par que menos aumenta a lista.** O custo de um par é quantos dos seus dois testes ainda não estão na suíte: 0, 1 ou 2. Na fórmula, é `|p \ S|`, o tamanho do par menos o que já está em S.
3. **No empate, prefira o par de causa única.** Ele dá mais garantia de detectar falhas (seção 1.6).
4. **Anote o par escolhido.** É a rastreabilidade: o relatório diz "V2 e V6 demonstram A".

**Executando em `(A and B) or C`, causa única:**

| Ordem | Condição | Pares disponíveis | Custo de cada | Escolha | Suíte |
|---|---|---|---|---|---|
| 1 | A (1 par) | (V2, V6) | 2 | (V2, V6) | V2, V6 |
| 2 | B (1 par) | (V2, V4) | 1 (só V4 é novo) | (V2, V4) | V2, V4, V6 |
| 3 | C (3 pares) | (V3, V4), (V5, V6), (V7, V8) | 1, 1, 2 | (V3, V4), o primeiro de custo 1 | V2, V3, V4, V6 |

Resultado: **4 testes para 3 condições**, ou seja, N + 1.

**Os limites inferiores.** Na causa única, uma suíte para N condições sem repetição precisa de pelo menos N + 1 testes (Kapoor e Bowen, Tabela I). No mascaramento, como os pares podem ser mais "distantes", o mínimo pode ser menor: pelo menos ⌈2√N⌉ (Chilenski, citado por Kvalsvik). Para N = 9, isso dá 6, contra 10 da causa única.

**Limitação.** O guloso nem sempre chega ao mínimo absoluto. A versão exata pode ser escrita como problema de otimização e entregue ao Z3, o próximo passo do roteiro.

## 1.5 Os algoritmos da ferramenta além do MC/DC básico

**Viabilidade com o Z3 (slide 16).** Cada condição com comparação vira uma fórmula. Para cada linha, a ferramenta pergunta ao Z3: "existe algum valor das variáveis que deixa exatamente estas condições verdadeiras e estas falsas?". Na linha V3 de `speed > 100 or (speed > 50 and rain)`:

```
(speed > 100) e não (speed > 50) e rain
```

O Z3 responde `unsat` (insatisfatível): não existe velocidade acima de 100 que não esteja acima de 50. A linha é marcada como impossível e sai dos pares. Para as linhas possíveis, ele devolve um exemplo, como `speed = 51, rain = true`, que vira o valor concreto do teste.

**Fronteira (`--boundary`).** Para cada teste e cada comparação numérica, a ferramenta pede ao Z3 o mesmo teste com a variável exatamente no limite. Se `speed > 100` é verdadeira no teste, o limite é `speed = 101`; se é falsa, `speed = 100`. A variante só entra se o resto do teste continuar valendo. Erros costumam aparecer justamente no limite (um `>` escrito como `>=`).

**Modo avaliação (slide 17).** Recebe testes já existentes e:

1. localiza cada teste na tabela verdade;
2. para cada condição, procura um par em que os dois testes estejam entre os existentes;
3. para cada condição sem par, escolhe o par que precisa de menos testes novos e sugere esses testes;
4. calcula a porcentagem do MCDC-Star.

Essa métrica funciona assim: cada condição tem dois "lados", o resultado T e o resultado F. Um lado conta como coberto se algum teste tem a condição naquele valor **e** ela decide o resultado naquele teste. A porcentagem é lados cobertos ÷ (2 × número de condições). Ela é mais justa que contar só pares completos, porque um teste que já prova metade do trabalho de uma condição recebe crédito.

**Validação por mutação (slide 18).** Para cada tipo de falha de Kapoor e Bowen, a ferramenta gera versões do requisito com um defeito: troca um `and` por `or`, nega uma parte, nega uma variável, desloca parênteses, apaga uma variável, troca uma variável por outra. Para cada versão:

- se ela dá a mesma resposta que a original em todas as linhas possíveis, é **equivalente** (nenhum teste pode diferenciar) e não conta;
- senão, procura um teste da suíte em que a resposta da versão errada difere da correta: se acha, a falha foi **detectada**.

## 1.6 O que o MC/DC garante detectar (Kapoor e Bowen)

| Falha | Exemplo | Detecção garantida com causa única? |
|---|---|---|
| Troca de operador (ORF) | `A and B` escrito `A or B` | Sim |
| Negação de subexpressão (ENF) | `A and (B or C)` escrito `A and not (B or C)` | Sim |
| Negação de variável (VNF) | `A and B` escrito `A and not B` | Sim |
| Variável ausente (MVF) | `A or B` escrito `A` | Sim |
| Troca de variável (VRF) | `A and B` escrito `A and C` | Sim (no mascaramento, não) |
| Parênteses deslocados (ASF) | `A and (B or C)` escrito `A and B or C` | Não, em nenhuma variante |

A intuição: um par de causa única "acende um holofote" sobre uma condição, porque nele ela é a única coisa que muda e a resposta acompanha. Qualquer defeito nessa condição ou num operador no caminho dela até o resultado muda o que o holofote mostra. Parênteses deslocados mudam a estrutura de um jeito que pode coincidir nos testes escolhidos, como no exemplo do slide 9.

---

# Parte 2 · Slide a slide

### Slide 1 · Testes melhores desde o requisito

A proposta em uma linha. "Desde o requisito" é o ponto-chave: normalmente o MC/DC é medido no fim, no código. A ideia é trazê-lo para o começo, quando corrigir é barato. A NAT2TEST aparece já na capa porque é ela que transforma o requisito em algo que a ferramenta consegue processar.

### Slide 2 · Cada condição precisa provar que faz diferença

Define condição, decisão e os quatro critérios.

- **Condição** é atômica: não tem `and`, `or` nem `not` dentro. "A porta está fechada" é uma condição; "a porta está fechada e não há obstáculo" é uma decisão.
- **Cada aparição conta separado.** Esta é a definição da DO-178, e não um capricho. Em `(A and B) or (A and C)`, o primeiro A pode estar certo e o segundo errado no código (alguém digitou A no lugar de D, por exemplo). Para pegar isso, cada aparição precisa da sua prova.
- **Os critérios 1 a 3** (entrada e saída, cada decisão nos dois resultados, cada condição nos dois valores) existem em coberturas mais fracas. **O 4º** é o que torna o MC/DC forte: não basta a condição ter assumido os dois valores, ela precisa ter mostrado que muda a resposta.

### Slide 3 · Com 4 testes, provamos o que 8 testariam

O exemplo concreto. A mensagem é a economia: testar todas as combinações cresce como 2^N; o MC/DC cresce como N + 1. Com 20 condições, 1.048.576 contra 21. O "segredo" de reaproveitar é a essência do algoritmo 3: V2 entra em dois pares ao mesmo tempo.

### Slide 4 · Para um “e” ou um “ou”, a receita cabe numa frase

A forma manual de Hayhurst e Veerhusen. No `and`, uma única entrada falsa já derruba tudo; por isso o teste "tudo verdadeiro" mais um teste para cada entrada sozinha falsa mostra que cada uma, sozinha, derruba a saída. No `or` é o espelho. Para expressões maiores, o método deles monta o circuito de portas e descarta à mão os testes em que uma porta esconde a saída da outra (o mascaramento). Os algoritmos 1 a 3 automatizam e generalizam essa ideia.

### Slide 5 · Algoritmo 1: troque um bit e veja se a resposta muda

Ver a seção 1.2. Pontos para ter claros: o binário é só uma forma eficiente de inverter uma condição; a gêmea é `r | mask`; o par exige que o resultado mude; a derivada booleana é a mesma ideia escrita como fórmula.

### Slide 6 · Algoritmo 2: e se outras condições mudarem junto?

Ver a seção 1.3. A pergunta muda de "só ela mudou?" para "ela decide nos dois testes?". O exemplo V7/V4 é o caso típico: A mudou, mas com B falsa ela estava sem voz.

### Slide 7 · Algoritmo 3: poucos testes que provem tudo

Ver a seção 1.4. Dois pontos que costumam gerar pergunta: por que começar pelas condições com menos pares (elas não têm escolha, e o que elas forçam ajuda as outras), e por que o guloso não é sempre ótimo (o problema é de cobertura de conjuntos; a solução exata exige otimização).

### Slide 8 · O quanto ser rigoroso na hora de aceitar um par?

As quatro variantes, da mais rígida para a mais flexível:

- **Causa única (UC):** só a condição muda. Mais garantias, mas às vezes impossível, quando há condições acopladas.
- **UC com mascaramento fraca (UCMW):** trata aparições repetidas como uma só. Basta provar uma delas. É a mais fraca: se uma aparição estiver errada no código, pode passar. Era o que a primeira versão da ferramenta fazia, até os artigos mostrarem o problema.
- **UC com mascaramento forte (UCMS):** só a variável muda (todas as suas aparições juntas, porque são a mesma variável), e cada aparição precisa decidir no par. Dá as mesmas garantias da UC.
- **Mascaramento:** outras condições podem mudar se estiverem mascaradas. Mais flexível; perde só a garantia sobre troca de variável.

A CAST-6 é um documento das autoridades certificadoras que aceita o mascaramento em projetos certificados. GCC e Clang implementam mascaramento. Por isso é o padrão da ferramenta, com a preferência por causa única no empate para recuperar parte da garantia.

### Slide 9 · O que esses testes pegam, e o que deixam passar

Ver a seção 1.6. O exemplo da direita é importante porque mostra um limite real do critério: a suíte (TTF, TFF, TFT, FTF) cumpre MC/DC para `A and (B or C)` e dá as mesmas respostas para `A and B or C`, que significa `(A and B) or C`. A diferença entre as duas só aparece em FFT ou FTT (A falsa, C verdadeira), e nenhum desses está na suíte.

### Slide 10 · Quanto maior o risco, mais a aviação exige dos testes

A DO-178C é a norma que as autoridades (FAA, EASA, ANAC) usam para aceitar software de aeronaves. Ela classifica o software por **nível de garantia (DAL)**, conforme o pior efeito de uma falha:

| Nível | Efeito | Cobertura estrutural |
|---|---|---|
| A | Catastrófico (perda da aeronave) | MC/DC, decisão e comandos |
| B | Perigoso | Decisão e comandos |
| C | Maior | Comandos |
| D | Menor | Não exigida |
| E | Sem efeito | Não se aplica |

No nível A, a verificação ainda precisa de **independência**: quem confere não pode ser quem fez. O número de 75% vem de uma pesquisa de 1999 citada por Hayhurst e Veerhusen: mostra que o custo do MC/DC é uma dor real da indústria.

### Slide 11 · Todo teste passa por duas perguntas

O ponto mais importante para entender o lugar da ferramenta. A DO-178C não aceita testes escritos olhando o código ("teste o que está aí"); os testes vêm dos requisitos. Depois, mede-se quanto do código esses testes exercitaram. Se faltar cobertura, a investigação aponta um de três problemas:

- **falta requisito:** o código faz algo que nenhum requisito pede;
- **sobra código:** código morto ou não intencional;
- **falta teste:** o requisito existe, mas os testes não o exploraram bem.

Pensar no MC/DC já ao escrever os testes de requisito reduz o terceiro caso, que é justamente o que gera retrabalho no fim.

### Slide 12 · Cinco trabalhos que guiaram cada decisão

- **Hayhurst e Veerhusen (NASA, 2001):** artigo prático, voltado a auditores. Dá as regras por operador, o método em 5 passos para avaliar se testes atingem MC/DC e a análise de quais erros o MC/DC pega.
- **Kapoor e Bowen:** formalização matemática das variantes e prova de quais falhas cada uma detecta. Daí vieram a correção das aparições repetidas e o teste do motor por mutação.
- **Sun et al. (Oxford e Rolls-Royce, 2017):** aplicam MC/DC sobre requisitos formais, com análise de fronteira e um verificador de modelos (CBMC) gerando os valores, num caso industrial. É a validação externa da ideia central da ferramenta.
- **Kvalsvik (2025):** como o GCC 14 mede mascaramento compilando as expressões em diagramas de decisão binária. Confirma o padrão e indica o caminho para a fase de código.
- **Hu, Wong et al. (MCDC-Star, 2018):** geram entradas para código C com execução simbólica e propõem a métrica por "lado" de cada condição, que o modo avaliação usa.

### Slide 13 · E se o MC/DC entrasse em cena antes do código?

A virada da apresentação: da teoria para a proposta. A NAT2TEST já faz a parte difícil, entender linguagem natural, e chega a uma representação formal das decisões. Com isso, a ferramenta consegue gerar os testes MC/DC e medir os testes que a NAT2TEST já produz.

### Slide 14 · Do texto do requisito ao relatório

O fluxo completo:

1. A NAT2TEST analisa o texto (sintaxe e semântica) e gera o **DFRS**, o modelo formal do sistema: variáveis, tipos, guardas e o que acontece quando cada guarda é verdadeira.
2. O **Extractor**, ainda a construir, lê o DFRS e grava um JSON com o que o MC/DC precisa: as guardas (as decisões), os tipos das variáveis, as ações e o identificador do requisito.
3. O **plugin** roda o motor.
4. O relatório volta para o **Viewer**, a tela da NAT2TEST.

O que está tracejado ainda não existe. O formato do JSON já foi definido e a ferramenta já o lê, por isso o caminho funciona hoje com um JSON escrito à mão.

### Slide 15 · O que acontece com cada requisito, passo a passo

Os cinco cartões resumem o motor:

1. **Cada repetição conta separado:** as condições por aparição, seção 1.2.
2. **Todas as combinações, compactas:** a tabela em bits, seção 1.1.
3. **As duplas que provam cada condição:** algoritmos 1 e 2.
4. **Poucos testes, e quem prova o quê:** algoritmo 3, com rastreabilidade.
5. **Um aviso quando uma condição não faz diferença:** o diagnóstico.

O diagnóstico separa dois casos que parecem iguais ("a condição não tem par") mas significam coisas diferentes:

- **Redundante:** nem na tabela completa há par. A condição nunca muda a resposta, então o requisito pode ser simplificado. Exemplo: em `freio or (freio and pedal)`, o pedal nunca importa.
- **Bloqueada:** havia pares, mas todos usam combinações impossíveis. O requisito pode estar certo; são as regras do sistema que impedem o teste.

### Slide 16 · Nem toda combinação existe, e o Z3 sabe quais

Ver a seção 1.5. A tabela verdade trata `speed > 100` e `speed > 50` como independentes, mas não são: a primeira implica a segunda. O Z3 é um **solver SMT**, um programa que responde se um conjunto de fórmulas sobre números, booleanos e outros tipos pode ser verdadeiro ao mesmo tempo, e, se puder, dá um exemplo. A ferramenta usa isso para descartar linhas impossíveis e para gerar valores reais. A NAT2TEST também usa o Z3, o que abre a possibilidade de reaproveitar a forma como eles traduzem o DFRS.

### Slide 17 · Já tem testes? A ferramenta diz o quanto eles cobrem

Ver a seção 1.5. No exemplo do slide, T3 e T4 formam um par para `mode = choice` (só ele muda e o resultado muda). Para as outras duas condições, a ferramenta indica os vetores V4 e V5, escolhidos para aproveitar os testes que já existem. O T4 tem o resultado esperado errado no arquivo de exemplo, de propósito: a ferramenta compara o que o teste diz esperar com o que a guarda realmente calcula.

### Slide 18 · Colocamos defeitos de propósito para ver se os testes pegam

Ver a seção 1.5. É mutação aplicada ao requisito. O resultado (94,1%) é: 16 de 17 versões detectáveis foram detectadas. A única que escapou é a de parênteses deslocados, exatamente o caso que a teoria diz não ser garantido. Além disso, um teste automatizado da ferramenta verifica o teorema de Kapoor e Bowen em 6 expressões. Se algum dia o motor passar a gerar pares errados, esse teste quebra: é uma forma independente de verificar a própria ferramenta.

### Slide 19 · Quem testa a ferramenta de teste?

A DO-330 é o suplemento da DO-178C (2011) para **qualificação de ferramentas**. A lógica: se a certificação deixa de fazer algo à mão porque uma ferramenta faz, a ferramenta precisa ser confiável na medida do risco. São três critérios:

- **Critério 1:** a saída da ferramenta vai para dentro do software do avião (um compilador, um gerador de código). Um erro dela vira erro no avião.
- **Critério 2:** a ferramenta automatiza uma verificação, e o resultado dela é usado para dispensar ou reduzir outras verificações.
- **Critério 3:** a ferramenta pode deixar de detectar um erro, sem que outras verificações sejam dispensadas por causa dela.

Cruzando o critério com o nível do software, sai o **TQL** (Tool Qualification Level), de 1 a 5: TQL-1 é quase tão rigoroso quanto desenvolver o próprio software do avião; TQL-5 pede basicamente requisitos operacionais da ferramenta e evidência de que ela os cumpre.

### Slide 20 · Onde a nossa ferramenta se encaixa

- No uso normal, a ferramenta gera testes que pessoas executam e revisam. Se ela errar, o pior caso é deixar de apontar algo: **critério 3, TQL-5**.
- Se um projeto usar o resultado do `check` para dispensar, por exemplo, a revisão manual de suficiência dos testes, ela passa ao **critério 2**: TQL-4 nos níveis A e B.
- **Critério 1 nunca**, porque nada que ela produz vai para o avião.

Os dois cuidados do slide são importantes para não exagerar o que a ferramenta faz. Primeiro, a DO-178C exige MC/DC **no código**; a ferramenta, nesta fase, atua no requisito. Segundo, a qualificação é sempre feita por quem usa a ferramenta num projeto real, junto com a autoridade. O papel do projeto é deixar as evidências prontas.

### Slide 21 · O que já temos e o que ainda falta

Uma visão geral do que uma qualificação TQL-5 costuma pedir, e quanto disso já existe:

- **Requisitos operacionais da ferramenta (TOR):** o que ela deve fazer. Os documentos de arquitetura e implementação já descrevem isso, mas não no formato da DO-330.
- **Verificação contra esses requisitos:** os 92 testes e a mutação. Falta ligar cada teste a um item do TOR.
- **Rastreabilidade da saída:** já existe (par por condição, id do requisito).
- **Gestão de configuração:** Git e Maven existem. Faltam versões publicadas e congeladas.
- **Plano e resumo de qualificação (TQP e TAS):** só fazem sentido dentro de um projeto real.

### Slide 22 · Onde estamos hoje

Os números da fase 1:
- 92 testes automatizados;
- 20 entradas (1.048.576 linhas) em 0,2 s em causa única, e 5 a 6 s em mascaramento, que testa cada condição em cada linha;
- dois modos: gerar (`analyze`) e medir (`check`);
- três fontes de entrada: expressão, arquivo `.mcdc` e JSON;
- quatro saídas: texto, JSON, CSV e Gherkin;
- cinco módulos Maven.

### Slide 23 · Para onde vamos

- **Mais Z3:** a suíte mínima exata, por otimização, e os pares pedidos direto ao Z3 em vez de montar a tabela, o que tira o limite de tamanho.
- **NAT2TEST:** Extractor, Viewer e a questão da alcançabilidade (slide 24).
- **Plugin Eclipse:** uma camada fina sobre o mesmo motor.
- **Fases 2 e 3, código Java:** aqui a ferramenta passa a medir o MC/DC que a DO-178C exige de fato. Exige tratar curto-circuito (em `A && B`, se A é falsa, B nem é avaliada) e instrumentar o código, seguindo a abordagem do GCC.

### Slide 24 · O que precisamos combinar com a NAT2TEST

As quatro perguntas abertas da integração. A quarta é a mais interessante do ponto de vista de pesquisa: o Z3 da ferramenta verifica cada combinação **num instante**, olhando só a guarda. Mas um sistema real tem estado: talvez a combinação "modo = preparando e moeda inserida" seja logicamente possível, mas nunca aconteça na prática por causa das transições anteriores. A NAT2TEST conhece esse comportamento ao longo do tempo. Juntas, a ferramenta diria quais testes o MC/DC exige, e a NAT2TEST, se e como é possível chegar a cada um.

### Slide 25 · Referências

As fontes de tudo o que foi dito: a DO-178C e a DO-330 (RTCA, 2011), a posição CAST-6 sobre mascaramento, o relatório do Chilenski para a FAA (origem das variantes), os cinco artigos e o artigo original do Z3.
