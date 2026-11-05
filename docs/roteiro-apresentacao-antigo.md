# Roteiro da apresentação: Testes melhores desde o requisito

Roteiro de fala para os 25 slides da apresentação ([link](https://claude.ai/artifact/RPdM1NZzNqgJhFLDGkD2Pr)). Cada slide tem: o título como está no slide, o tempo sugerido, a ideia que precisa ficar, o que falar e a passagem para o próximo. No fim há uma demonstração opcional ao vivo e respostas para as perguntas mais prováveis.

As frases entre aspas são sugestões para dizer em voz alta; adapte ao seu jeito de falar.

**Duração total:** cerca de 30 minutos sem a demonstração; 35 a 40 com ela.

| Bloco | Slides | Tempo |
|---|---|---|
| 1. MC/DC: definição e algoritmos | 1 a 7 | 10 min |
| 2. Variantes e o que o MC/DC detecta | 8 e 9 | 3 min |
| 3. Por que MC/DC: a DO-178C | 10 e 11 | 3 min |
| 4. Estado da arte | 12 | 2 min |
| 5. A ferramenta | 13 a 18 | 7 min |
| 6. Certificação: DO-330 | 19 a 21 | 3 min |
| 7. Estado atual e próximos passos | 22 a 25 | 2 min |

## Antes de apresentar

- [ ] Preencher na capa: `[Nome] · [Orientador ou grupo] · [Data]`.
- [ ] Compartilhar o link da apresentação (menu Share da página); sem isso, ninguém além de você abre.
- [ ] Confirmar com o pessoal da NAT2TEST os nomes das etapas no slide 14 ("análise sintática", "análise semântica e DFRS").
- [ ] Se importar no Google Drive: conferir os slides 5 a 7, que usam símbolos matemáticos (xᵢ, ⊕, ∂, ⌈ ⌉). Se algum aparecer como quadradinho, trocar a fonte daquela caixa.
- [ ] Se for fazer a demonstração: no terminal, na pasta do projeto, rodar uma vez antes:
  ```bash
  export JAVA_HOME=$(/usr/libexec/java_home -v 21)
  mvn -q clean compile
  ./mcdc analyze "(A and B) or C"
  ```
  e deixar o terminal com fonte grande.

---

## Bloco 1 · MC/DC: definição e algoritmos

### Slide 1 · Testes melhores desde o requisito (30 s)

**Ideia:** aplicar o critério de cobertura da aviação já na fase de requisitos.

**Falar:**
- "Hoje quero mostrar como dá para testar melhor desde o requisito, usando o MC/DC, o critério de cobertura mais exigente da aviação."
- "Vou primeiro explicar o que é o MC/DC e como ele se calcula; depois por que a aviação exige; e por fim o que a ferramenta já faz e como ela conversa com a NAT2TEST."

**Passagem:** "Começando pelo que o MC/DC pede."

### Slide 2 · Cada condição precisa provar que faz diferença (1 min 30 s)

**Ideia:** cada condição, sozinha, tem que conseguir mudar a resposta.

**Falar:**
- "Uma condição é a menor peça de uma decisão, algo que é verdadeiro ou falso, como 'a porta está fechada'. A decisão é a pergunta inteira: 'a porta está fechada e não há obstáculo?'."
- "Um detalhe importante: se a mesma variável aparece duas vezes, cada aparição conta separado. Em `(A and B) or (A and C)` são 3 variáveis, mas 4 condições."
- "Os três primeiros critérios são comuns a outras coberturas. O quarto é o que define o MC/DC: cada condição, sozinha, consegue mudar a resposta."
- "Esse detalhe das repetições parece pequeno, mas a primeira versão da ferramenta errava nisso. Os artigos ajudaram a corrigir."

**Passagem:** "Vamos ver isso num exemplo."

### Slide 3 · Com 4 testes, provamos o que 8 testariam (1 min 30 s)

**Ideia:** N + 1 testes no lugar de 2^N.

**Falar:**
- "Com três condições, a tabela completa tem 8 linhas."
- "Um par de independência são dois testes quase iguais: só uma condição muda, e a resposta muda junto. A tem o par V2 e V6; B, V2 e V4; C tem três opções."
- "O segredo é reaproveitar: o V2 ajuda a provar A e B ao mesmo tempo. Com isso, 4 testes bastam: V2, V3, V4 e V6."
- "E a diferença cresce rápido: com 20 condições, a tabela passaria de 1 milhão de linhas, e continuaríamos com 21 testes."

**Passagem:** "Antes do algoritmo geral, a receita que se usa à mão."

### Slide 4 · Para um “e” ou um “ou”, a receita cabe numa frase (1 min 30 s)

**Ideia:** para `and` e `or` de n entradas, bastam n + 1 testes.

**Falar:**
- "No 'e', começamos com tudo verdadeiro e derrubamos uma entrada por vez. No 'ou', o contrário: tudo falso, e acendemos uma por vez."
- "Cada teste com uma única entrada diferente forma par com o primeiro. O 'não' só precisa dos dois valores."
- "Essa é a receita de Hayhurst e Veerhusen, da NASA. Para expressões maiores, eles percorrem o circuito de portas à mão. Os algoritmos a seguir fazem isso de forma automática, para qualquer expressão."

**Passagem:** "Primeiro algoritmo."

### Slide 5 · Algoritmo 1: troque um bit e veja se a resposta muda (2 min)

**Ideia:** inverter uma condição é trocar um bit.

**Falar:**
- "Cada linha da tabela é um número binário: um bit por condição, e zero quer dizer verdadeira."
- "Para inverter só uma condição, basta trocar o bit dela. A linha 'gêmea' é a mesma linha com aquele bit ligado: `r | mask`."
- Ler a caixa branca, de cima para baixo:
  - "v linha é o vizinho de v que só difere em xᵢ."
  - "O par existe quando, com xᵢ verdadeira em v, a resposta muda entre os dois."
  - "A terceira linha diz o mesmo como derivada booleana: D com xᵢ verdadeira, ou-exclusivo, D com xᵢ falsa, igual a 1. Kapoor e Bowen usam essa equação, com ou-exclusivo, para achar todos os pares de uma condição."
- Apontar a tabela: "das quatro linhas com A verdadeira, só a 001 forma par, com a 101. São V2 e V6."
- "O custo é N vezes 2 elevado a N. Como a ferramenta guarda a tabela em bits, ela chega a 20 entradas."
- Se perguntarem sobre variáveis repetidas: "aí a ferramenta exige também que aquela aparição decida nos dois testes; é a variante forte, do slide 8."

**Passagem:** "E se outras condições mudarem junto?"

### Slide 6 · Algoritmo 2: e se outras condições mudarem junto? (2 min)

**Ideia:** no mascaramento, a pergunta passa a ser "a condição decide a resposta?".

**Falar:**
- Ler a caixa escura:
  - "Uma condição decide num teste quando, negando só ela, a resposta se inverte."
  - "T de c são os testes possíveis em que c é verdadeira e decide; F de c, os em que c é falsa e decide."
  - "Os pares são as combinações de um teste de cada lado com respostas opostas."
- "Todo par de causa única também cumpre essas regras; o contrário não."
- Exemplo à direita: "Entre V7 e V4, o A também mudou, mas tanto faz: com B falso, A não tem como influenciar. Dizemos que A está mascarada, e quem decide é C."
- "Aceitar esses pares dá mais opções: C passa de 3 para 9 pares. Isso ajuda muito quando algumas combinações não podem acontecer."
- "É a mesma ideia da Definição 12 de Kapoor e Bowen, e o que o GCC 14 calcula."

**Passagem:** "Com os pares em mãos, falta escolher os testes."

### Slide 7 · Algoritmo 3: poucos testes que provem tudo (1 min 30 s)

**Ideia:** escolher poucos pares que se aproveitam, e anotar quem prova o quê.

**Falar:**
- Os quatro passos: "começamos pelas condições com menos opções; escolhemos o par que menos aumenta a lista; no empate, ficamos com o mais rigoroso; e anotamos quem prova o quê."
- Seguir a tabela: "A e B só têm um par cada. Para C, o par V3 e V4 só acrescenta o V3. Resultado: V2, V3, V4 e V6."
- "Anotar quem prova o quê é a rastreabilidade: é o que um auditor de certificação quer ver."
- Ler a caixa de fórmulas:
  - "Formalmente, queremos o menor conjunto de testes S que contenha um par inteiro de cada condição; é um problema de cobertura de conjuntos."
  - "O guloso escolhe, para cada condição, o par que menos acrescenta a S."
  - "E há limites: pelo menos N + 1 testes na causa única, e pelo menos teto de 2 raiz de N no mascaramento."
- "É rápido e chega perto do mínimo. Para garantir o mínimo exato, o próximo passo é pedir ajuda ao Z3."

**Passagem:** "Falei de causa única e mascaramento. A literatura tem quatro variantes."

---

## Bloco 2 · Variantes e o que o MC/DC detecta

### Slide 8 · O quanto ser rigoroso na hora de aceitar um par? (1 min 30 s)

**Ideia:** as variantes não são equivalentes, e a fraca é arriscada.

**Falar:**
- Percorrer a tabela, da mais rigorosa para a mais flexível.
- "A fraca aceita provar só uma das repetições de uma variável. Quando há repetição, ela não garante nada. Era o que a primeira versão da ferramenta fazia sem querer."
- "Usamos a forma mais adotada na indústria, o mascaramento, aceito pela CAST-6 e usado no GCC e no Clang. E, quando dá, preferimos a mais rigorosa."
- "Mínimo de testes: N + 1 na causa única; no mascaramento, pode cair até teto de 2 raiz de N."

**Passagem:** "E o que esses testes realmente pegam?"

### Slide 9 · O que esses testes pegam, e o que deixam passar (1 min 30 s)

**Ideia:** cinco tipos de falha são garantidos; parênteses no lugar errado, não.

**Falar:**
- "Kapoor e Bowen provaram que um par de causa única por condição pega sempre cinco tipos de falha: trocar o operador, negar uma parte da expressão, negar uma variável, esquecer uma variável ou trocar uma variável por outra."
- "O que nenhuma variante garante é pegar parênteses no lugar errado."
- Apontar a tabela da direita: "Esta suíte atinge MC/DC em `A and (B or C)`, mas dá exatamente as mesmas respostas na versão errada, sem os parênteses. O erro passa."
- "Guardem esse exemplo: mais adiante a ferramenta reproduz exatamente isso."

**Passagem:** "Mas por que a aviação se importa tanto com tudo isso?"

---

## Bloco 3 · Por que MC/DC: a DO-178C

### Slide 10 · Quanto maior o risco, mais a aviação exige dos testes (1 min 30 s)

**Ideia:** quanto mais grave a falha, mais cobertura; no nível A, MC/DC.

**Falar:**
- "A DO-178C classifica o software pelo estrago que uma falha dele causaria: de A, catastrófica, até E, sem efeito."
- "No nível A, os testes precisam atingir MC/DC no código, e quem verifica não pode ser quem desenvolveu. No B, cobertura de decisão; no C, de comandos."
- Apontar o número: "Numa pesquisa de 1999, 75% dos profissionais achavam o MC/DC difícil, e quase o mesmo tanto achava o custo pesado demais."
- "É esse custo que a ferramenta quer diminuir."

**Passagem:** "E onde exatamente o MC/DC entra no processo?"

### Slide 11 · Todo teste passa por duas perguntas (1 min 30 s)

**Ideia:** o MC/DC é medido no código, mas os testes vêm dos requisitos.

**Falar:**
- "Primeira pergunta: testamos tudo o que foi pedido? Os testes saem dos requisitos, sem olhar o código."
- "Segunda: com esses mesmos testes, passamos por todo o código? No nível A, com MC/DC."
- "Quando a segunda resposta é 'não', falta requisito, sobra código ou falta teste."
- "Se os testes já nascem pensados para MC/DC, essa surpresa no fim não acontece. É aí que a ferramenta entra."

**Passagem:** "Antes de mostrar a ferramenta, em quem nos apoiamos."

---

## Bloco 4 · Estado da arte

### Slide 12 · Cinco trabalhos que guiaram cada decisão (2 min)

**Ideia:** cada artigo resolveu uma questão concreta do projeto.

**Falar (uma frase por linha da tabela):**
- **Hayhurst e Veerhusen:** "a base de tudo: as regras práticas e o jeito de medir se um conjunto de testes atinge MC/DC."
- **Kapoor e Bowen:** "a parte formal. Eles nos mostraram o erro das repetições, e o teorema deles virou teste da ferramenta."
- **Sun et al.:** "a prova de que a ideia funciona na indústria: MC/DC sobre requisitos com um verificador gerando os valores. Nós usamos o Z3 no lugar do verificador deles."
- **Kvalsvik:** "como o GCC faz; confirma que o mascaramento é o padrão dos compiladores."
- **MCDC-Star:** "a régua que usamos para medir testes que já existem."

**Passagem:** "Com isso, chegamos à pergunta que motivou a ferramenta."

---

## Bloco 5 · A ferramenta

### Slide 13 · E se o MC/DC entrasse em cena antes do código? (30 s)

**Ideia:** gerar e medir MC/DC já no requisito, a partir do que a NAT2TEST entende.

**Falar:** fazer a pergunta do slide em voz alta e deixar um segundo de silêncio. Depois: "A NAT2TEST já entende os requisitos. A ferramenta aproveita isso para dizer quais testes provam cada condição e para conferir os que já existem."

### Slide 14 · Do texto do requisito ao relatório (1 min 30 s)

**Ideia:** a NAT2TEST faz a parte difícil; a ferramenta recebe as decisões e devolve o relatório.

**Falar:**
- "Na NAT2TEST, o requisito em linguagem natural passa pela análise sintática e pela semântica e vira o DFRS."
- "Um Extractor, que ainda vamos construir, traduz o DFRS para uma linguagem que a ferramenta entende: as guardas, os tipos, as ações e o requisito de origem. O formato já está definido, e a ferramenta já sabe ler."
- "O plugin calcula tudo e o resultado volta para quem escreveu o requisito, no Viewer da NAT2TEST."
- "O que está tracejado ainda não existe. Mas todo o caminho, da entrada ao relatório, já funciona hoje pela linha de comando."

**Passagem:** "O que acontece lá dentro."

### Slide 15 · O que acontece com cada requisito, passo a passo (1 min)

**Ideia:** os algoritmos do bloco 1, mais rastreabilidade e diagnóstico.

**Falar:**
- Percorrer os cinco cartões: "cada repetição conta separado; todas as combinações guardadas de forma compacta; as duplas que provam cada condição; poucos testes, sabendo quem prova o quê; e um aviso quando uma condição não faz diferença."
- "Esse aviso separa dois problemas diferentes: uma condição redundante, que indica que o requisito pode ser simplificado, e uma condição que as regras do sistema impedem de testar."
- Mostrar as duas linhas da caixa escura como exemplo de saída.

**Passagem:** "E de onde vêm essas regras do sistema?"

### Slide 16 · Nem toda combinação existe, e o Z3 sabe quais (1 min 30 s)

**Ideia:** o Z3 descarta combinações impossíveis e dá valores reais aos testes.

**Falar:**
- Ler a caixa: "velocidade acima de 100 e, ao mesmo tempo, não acima de 50? Não existe."
- Apontar V3 e V4 na tabela: "a tabela, sozinha, não sabe disso. O Z3 sabe, e descarta essas linhas."
- "Cada linha vira uma pergunta ao Z3. Se a resposta é 'impossível', a linha sai; se é 'possível', ele ainda dá um exemplo de valores."
- "Os testes saem com valores reais, como velocidade 101. E com a opção de fronteira, cada comparação é levada ao limite, como no trabalho de Sun et al."
- "E a NAT2TEST já usa o Z3, o que facilita a integração."

**Passagem:** "Gerar testes é metade. A outra metade é medir os que já existem."

### Slide 17 · Já tem testes? A ferramenta diz o quanto eles cobrem (1 min 30 s)

**Ideia:** a ferramenta mede os testes que a NAT2TEST já gera e diz o que falta.

**Falar:**
- Percorrer a lista: "quais condições já estão provadas, que teste acrescentar para fechar o que falta, onde o resultado esperado não bate e quanto do MC/DC foi atingido."
- Apontar a caixa: "T3 e T4 provam a primeira condição. Para as outras duas, ela diz exatamente quais testes acrescentar. E o T4 tem o resultado esperado errado; deixamos de propósito, e a ferramenta encontrou."
- "A porcentagem segue o MCDC-Star: cada condição tem dois lados, verdadeiro e falso, e conta cada lado que algum teste mostra fazendo diferença."
- "Para a NAT2TEST, talvez este seja o ponto de maior valor."

**Passagem:** "E como sabemos que a própria ferramenta está certa?"

### Slide 18 · Colocamos defeitos de propósito para ver se os testes pegam (1 min 30 s)

**Ideia:** a ferramenta se comporta como a teoria prevê.

**Falar:**
- "A ferramenta cria versões do requisito com um defeito cada, nos seis tipos do Kapoor e Bowen, e confere se os testes gerados pegam."
- "Em `A and (B or C)`, ela pegou tudo, menos os parênteses no lugar errado. Só um escapou, e é exatamente o caso que a literatura já apontava, o do slide 9. Inclusive, os testes gerados são exatamente os do artigo."
- "Um teste automatizado cobra o teorema do Kapoor e Bowen em 6 expressões. Se o motor errasse os pares, esse teste quebraria."
- "Isso também serve como evidência de confiança na ferramenta, que é o próximo assunto."

---

## Bloco 6 · Certificação: DO-330

### Slide 19 · Quem testa a ferramenta de teste? (1 min)

**Ideia:** se a certificação confia na ferramenta, a ferramenta precisa merecer essa confiança.

**Falar:**
- Fazer a pergunta do título e responder: "a DO-330, o suplemento da DO-178C para ferramentas, de 2011."
- "A regra é: quanto maior o estrago que um erro da ferramenta causaria, mais rigorosa a qualificação."
- "São três casos: a ferramenta gera algo que vai para o avião; ela automatiza uma verificação e por isso dispensa outra; ou ela pode deixar de pegar um erro."
- "Cruzando o caso com o nível do software, temos de TQL-1, o mais rigoroso, a TQL-5, o mais leve."

### Slide 20 · Onde a nossa ferramenta se encaixa (1 min)

**Ideia:** é uma ferramenta de verificação: TQL-5, ou TQL-4 nos níveis A e B se o resultado dispensar outra verificação.

**Falar:**
- "No uso normal, ela gera testes que alguém executa e revisa: é o caso 3, TQL-5, o mais leve."
- "Se um projeto usar o resultado do check para dispensar outra verificação, vira o caso 2: TQL-4 nos níveis A e B."
- "O caso 1 nunca se aplica: ela não produz nada que vá para o avião."
- Os dois cartões: "requisito não é código: a DO-178C cobra o MC/DC no código, e aqui ajudamos a chegar lá com bons testes desde o começo. E quem qualifica é quem usa: cada projeto qualifica no seu contexto; nosso papel é entregar as evidências."

### Slide 21 · O que já temos e o que ainda falta (1 min)

**Ideia:** boa parte da base já existe; falta formalizar.

**Falar:**
- "Já temos: requisitos da ferramenta documentados, 92 testes automatizados, a mutação como verificação independente, rastreabilidade e controle de versões."
- "Falta: escrever os requisitos da ferramenta no formato da DO-330, ligar cada teste a eles e publicar versões congeladas. O plano e o resumo de qualificação só fazem sentido junto de um projeto real."
- "Ferramentas de cobertura costumam ficar no TQL-5, e a mutação é um diferencial: mostra, com teste, que a ferramenta respeita a teoria."

---

## Bloco 7 · Estado atual e próximos passos

### Slide 22 · Onde estamos hoje (30 s)

**Falar:** "Em números: 92 testes passando; 20 entradas, mais de 1 milhão de combinações, em 0,2 segundo [em causa única; 5 a 6 segundos em mascaramento]; dois modos, gerar e medir; três tipos de entrada; quatro formatos de saída; e cinco módulos."

### Slide 23 · Para onde vamos (45 s)

**Falar:**
- "A fase 1 está feita."
- "O próximo passo é usar mais o Z3: achar a suíte mínima exata e pedir os pares direto a ele, sem montar a tabela inteira."
- "Depois, a integração com a NAT2TEST e o plugin Eclipse."
- "E nas fases 2 e 3, o código Java: aí medimos o MC/DC que a DO-178C cobra de fato, no código, seguindo o caminho do GCC."

### Slide 24 · O que precisamos combinar com a NAT2TEST (45 s)

**Falar:** ler as quatro perguntas e destacar a última: "o Z3 da ferramenta olha cada combinação num instante; a NAT2TEST conhece o sistema ao longo do tempo. Juntas, a ferramenta diz quais testes o MC/DC pede, e a NAT2TEST diz como chegar a cada um."

### Slide 25 · Referências (encerramento)

**Falar:** "Obrigado! O código e toda a documentação estão no repositório. Vamos conversar?" Abrir para perguntas.

---

## Demonstração ao vivo (opcional, 5 a 8 min)

Melhor momento: depois do slide 18, antes da certificação. Os comandos rodam na pasta do projeto.

| Comando | O que mostrar |
|---|---|
| `./mcdc analyze "(A and B) or C"` | A tabela, os pares, a suíte com "demonstra" e a demonstração por condição. É o slide 3 saindo da ferramenta. |
| `./mcdc analyze "(A and B) or (not A and C)" --unique-cause` | `A#1` e `A#2` com pares próprios: cada repetição conta separado. |
| `./mcdc analyze -f exemplos/requisitos.mcdc` | O REQ-003 com duas condições redundantes; código de saída 2 (`echo $?`). |
| `./mcdc analyze "speed > 100 or (speed > 50 and rain)" --z3 --boundary --unique-cause` | Linhas impossíveis, valores reais e fronteiras. |
| `./mcdc check --json exemplos/decisoes.json --tests exemplos/testes.csv` | O que falta e a divergência do T4. |
| `./mcdc analyze "A and (B or C)" --mutation` | Os 94,1% e o `A and B or C` que escapou. |
| `./mcdc analyze --json exemplos/decisoes.json --z3 --format gherkin` | Os cenários em português, com as ações do DFRS. |

Use aspas simples se for digitar `/\` ou `\/`. Se algo falhar ao vivo, os slides 3, 16, 17 e 18 já mostram as mesmas saídas.

---

## Perguntas prováveis

**"A DO-178C não pede MC/DC sobre o código? Por que fazer no requisito?"**
"Pede sobre o código, sim. Mas os testes que atingem esse MC/DC precisam sair dos requisitos (slide 11). A ferramenta ajuda a desenhar esses testes já pensando no MC/DC. Medir no código é a fase 2 e 3. Sun et al. seguem a mesma lógica."

**"Por que mascaramento como padrão, se a causa única detecta mais?"**
"Porque é o aceito pela CAST-6 e o que GCC e Clang usam, e porque dá mais opções de pares, o que ajuda quando há combinações impossíveis. Para compensar, no empate a ferramenta prefere o par de causa única. E a causa única está a um `--unique-cause` de distância."

**"O algoritmo guloso dá o mínimo?"**
"Nem sempre; é um problema de cobertura de conjuntos. A versão exata é o próximo passo, com otimização no Z3. Nos exemplos da apresentação, sem repetições, ele chega a N + 1; com repetição, como em `(A and B) or (not A and C)`, a suíte tem 6 testes para 4 condições."

**"E com muitas condições?"**
"A tabela é guardada em bits: 20 entradas levam 0,2 segundo em causa única e 5 a 6 em mascaramento. O Z3 linha a linha vai até 12 entradas; acima disso, o plano é pedir os pares direto a ele."

**"Por que o Z3, se o DFRS já tem as funções?"**
"O DFRS descreve o sistema; o Z3 tira conclusões a partir dele. Saber que o modo não pode ser 'idle' e 'choice' ao mesmo tempo, ou que velocidade acima de 100 implica acima de 50, exige raciocinar sobre as comparações. E os valores reais dos testes também vêm do Z3."

**"A ferramenta já pode ser usada num projeto certificado?"**
"Ainda não como ferramenta qualificada. Ela se encaixa como ferramenta de verificação, TQL-5, ou TQL-4 nos níveis A e B se o resultado dispensar outra verificação. Boa parte das evidências já existe; falta formalizar (slide 21)."

**"Por que não RC/DC?"**
"Kapoor e Bowen mostram que os testes extras do RC/DC não aumentam a detecção das falhas estudadas em relação ao MC/DC."

**"Qual a diferença para o MCDC-Star ou para o GCC?"**
"Os dois trabalham sobre o código: o MCDC-Star gera entradas analisando o programa, e o GCC mede enquanto os testes rodam. A ferramenta trabalha antes, no requisito. A régua do MCDC-Star e o caminho do GCC entram nas próximas fases."
