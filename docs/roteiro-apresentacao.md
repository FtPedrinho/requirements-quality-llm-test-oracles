# Roteiro da apresentação: MC/DC, o que é e como automatizar

Roteiro para o deck de 31 slides (fundo branco, com pseudocódigo). A fala de cada slide é uma sugestão para ler em voz alta; adapte ao seu jeito. As frases entre aspas também estão nas notas do apresentador de cada slide.

**Tempo previsto:** cerca de 37 minutos, mais as perguntas.

| Bloco | Slides | Tempo |
|---|---|---|
| Abertura | 1–3 | 2 min 15 s |
| 1 · O que é MC/DC | 4–8 | 7 min 15 s |
| 2 · É exaustivo? | 9–11 | 4 min |
| 3 · Causa única e mascaramento | 12–16 | 7 min |
| 4 · Artigos e fórmulas | 17–18 | 1 min 45 s |
| 5 · A ferramenta | 19–28 | 13 min 15 s |
| Encerramento | 29–31 | 1 min + perguntas |

**Se o tempo for menor:**

- **Versão de 30 min:** pule os slides 18, 20, 21, 22 e 24 (tabela de fórmulas e pseudocódigos). Deixe-os no fim, como apoio para perguntas.
- **Versão de 20 min:** além dos acima, pule 8, 11, 15, 17 e 23. Nos slides 13 e 14, fale só a ideia de cada variante, sem a fórmula.

---

## Antes de apresentar

- [ ] Trocar `[Seu nome]` e `[Grupo ou instituição]` na capa.
- [ ] Compilar o projeto e testar o comando da demonstração:
  ```bash
  export JAVA_HOME=$(/usr/libexec/java_home -v 21)
  mvn clean verify
  ./mcdc analyze "(A and B) or C"
  ```
  Se o `./mcdc` reclamar de `classpath.txt`, é porque o `mvn clean verify` não rodou até o fim.
- [ ] Para o slide 27 ao vivo: conferir que o Z3 está instalado (`z3 --version`; se não, `brew install z3`).
- [ ] Deixar um terminal aberto na raiz do projeto, com fonte grande.
- [ ] Ter este roteiro aberto no celular ou impresso; as notas do apresentador do deck têm a mesma fala.

---

## Abertura

### Slide 1 · Capa (30 s)

**Na tela:** título, seu nome e a expressão `(A and B) or C`.

**Fala:** “Hoje eu quero mostrar três coisas: o que é o MC/DC, quanto ele custa de verdade e uma ferramenta que gera esses testes direto do requisito.”

**Transição:** “Primeiro, o caminho que vamos seguir.”

### Slide 2 · O caminho de hoje (45 s)

**Na tela:** as 5 partes, cada uma com uma linha de explicação.

**Fala:** “São cinco partes. Começo pelo conceito, mostro quanto ele custa, explico as duas variantes, mostro de onde vem cada fórmula e termino com a ferramenta rodando. A parte de código-fonte fica para depois; hoje é só requisito.”

**Transição:** “Mas por que alguém inventou o MC/DC?”

### Slide 3 · Por que o MC/DC existe (1 min)

**Na tela:** nível A da DO-178 e a citação de Hayhurst e Veerhusen.

**Fala:** “Pensem num software de controle de voo. Se ele errar, pode derrubar o avião. Para esse tipo de software, o nível A, a norma DO-178 exige MC/DC. O ideal seria testar todas as combinações, mas isso é inviável. O MC/DC foi criado para dar quase a mesma confiança com muito menos testes.”

**Transição:** “Para entender o critério, preciso de duas palavras.”

---

## Bloco 1 · O que é MC/DC

### Slide 4 · Primeiro, duas palavras (1 min 15 s)

**Na tela:** condição, decisão e o exemplo `(A and B) or (A and C)`.

**Fala:** “Condição é a menor pergunta de sim ou não, como ‘a velocidade passou de 100?’. Decisão é a combinação dessas perguntas com and, or e not. Um detalhe que vai importar mais tarde: se a mesma variável aparece duas vezes, a norma conta como duas condições. Aqui são 3 entradas, mas 4 condições.”

**Transição:** “Agora, por que não basta testar a decisão dando verdadeiro e falso?”

### Slide 5 · Testar só o T e o F da decisão não basta (1 min 30 s)

**Na tela:** o requisito `A and B` contra o código com bug `A or B`, com 2 testes e com 3.

**Fala:** “O requisito é A and B, mas o programador escreveu A or B. Se eu testar só tudo verdadeiro e tudo falso, as duas versões dão a mesma resposta, e o bug passa. Repare que esses dois testes já fazem a decisão e cada condição valerem T e F. O MC/DC me obriga a testar A sozinho e B sozinho, e aí as respostas ficam diferentes. É isso que ele ganha em relação aos critérios mais simples.”

**Transição:** “Então, o que exatamente o MC/DC pede?”

### Slide 6 · O que o MC/DC pede (1 min)

**Na tela:** as quatro exigências, com a quarta em destaque.

**Fala:** “Esta é a definição oficial, em quatro partes. As três primeiras já existiam em critérios mais simples, como os do slide anterior. A quarta é a que faz a diferença: cada condição precisa provar, sozinha, que muda o resultado. O resto da apresentação é sobre como fazer isso.”

**Transição:** “Como se prova que uma condição muda o resultado?”

### Slide 7 · Como provar que uma condição importa (1 min 30 s)

**Na tela:** os testes V1 e V5 de `A and B and C` e a fórmula `f(v) ≠ f(vⁱ)`.

**Fala:** “Pego um teste, troco só o A e vejo se a saída muda. Com tudo verdadeiro, a saída é verdadeira; troco o A para falso e a saída vira falsa. Então A importa. Um teste sozinho não prova nada: é o par que prova. Em fórmula: f de v é diferente de f de v-i, onde v-i é o mesmo teste com só a condição i trocada. O MC/DC pede um par desses para cada condição.”

**Transição:** “Vamos fazer isso numa tabela inteira.”

### Slide 8 · Achando os pares numa tabela inteira (2 min)

**Na tela:** as 8 linhas de `(A and B) or C`, com V2 e V6 em amarelo.

**Fala:** “São 3 condições, então 8 linhas. Para achar os pares, pego uma linha, troco só uma condição e procuro a linha gêmea. Se a saída mudou, achei um par. Em amarelo: V2 e V6 só diferem no A, e a saída vai de verdadeiro para falso. É o par de A. Fazendo isso para todas as linhas, B tem um par só e C tem três. Guardem isso: vai pesar na hora de escolher os testes.”

**Transição:** “E aqui vem a pergunta que muita gente faz: isso não é testar tudo?”

---

## Bloco 2 · É exaustivo?

### Slide 9 · Testar tudo: a conta dobra a cada entrada (1 min)

**Na tela:** `2ⁿ` e a tabela de crescimento.

**Fala:** “Primeiro, o que seria exaustivo: testar todas as combinações. Com 3 entradas são 8; cada entrada nova dobra a conta. Com 30 entradas, passa de um bilhão de testes.”

**Transição:** “E o MC/DC?”

### Slide 10 · O MC/DC pede bem menos: de n + 1 a 2n (1 min 30 s)

**Na tela:** os 4 testes da porta and e a comparação com o exaustivo.

**Fala:** “Numa porta and com 3 entradas, basta um teste com tudo verdadeiro e um teste para cada entrada sozinha em falso: 4 testes, não 8. Em geral, cada condição precisa de um par, ou seja, 2 testes. Se nenhum teste for compartilhado, são 2n. Se um teste servir a vários pares, como o teste 1 aqui, cai para n + 1. Com 30 entradas, no máximo 60 testes, contra um bilhão. Então não: o MC/DC não é exaustivo.”

**Transição:** “Mas então de onde vem a sensação de que ele é exponencial?”

### Slide 11 · Então onde está o exponencial? (1 min 30 s)

**Na tela:** os dois cartões e a frase final em destaque.

**Fala:** “Essa sensação tem fundamento, mas está no lugar errado. Primeiro: para escolher poucos testes, a ferramenta olha todas as combinações antes. Esse trabalho é exponencial, mas é da máquina, e é rápido: um milhão de linhas em 0,2 segundo na causa única. Segundo: existem fórmulas que, escritas com and, or e not, ficam gigantes. Aí sim os testes chegam a 2ⁿ. Para quem executa os testes num requisito normal, o MC/DC é linear.”

**Transição:** “Até aqui, cada condição podia mudar sozinha. Nem sempre é assim.”

---

## Bloco 3 · Causa única e mascaramento

### Slide 12 · E quando a condição não muda sozinha? (1 min 30 s)

**Na tela:** `(A#1 and B) or (not A#2 and C)` e os cartões de acoplamento forte e fraco.

**Fala:** “Olhem esta expressão: o A aparece duas vezes. Se eu troco o primeiro A, o segundo troca junto, porque é a mesma variável. Isso se chama acoplamento. Pode ser forte, como aqui, ou fraco, como ‘velocidade maior que 50’ e ‘maior que 100’: às vezes muda só uma, às vezes as duas. A norma pede para mudar uma condição e deixar as outras fixas, mas não diz o que fazer quando isso é impossível.”

**Transição:** “Existem duas respostas para esse problema. A primeira é a causa única.”

### Slide 13 · Causa única: muda uma coisa de cada vez (1 min 30 s)

**Na tela:** os pares de `(A and B) or C`, com a letra que mudou sublinhada, e a fórmula.

**Fala:** “A causa única é a leitura ao pé da letra da norma: entre os dois testes do par, só a condição que estou testando muda. A letra sublinhada é a que mudou. Em fórmula: para toda condição i, existem dois testes na suíte que formam um par de i. Quando a variável se repete, vale a forma forte: um par para cada aparição. É a forma mais fácil de explicar para um auditor, mas também a mais rígida.”

**Transição:** “A segunda resposta é mais flexível.”

### Slide 14 · Mascaramento: muda o que não faz diferença (2 min)

**Na tela:** as regras do and e do or, o par de B com C em cinza e a fórmula.

**Fala:** “No mascaramento, outras condições podem mudar junto, desde que naquele teste elas estejam ‘desligadas’. Quando uma condição fica desligada? Num and, se o outro lado é falso, tanto faz o que ela vale. Num or, se o outro lado é verdadeiro, também. Neste par de B, o C também mudou, em cinza. Mas como A é verdadeiro, a parte ‘not A and C’ é falsa de qualquer jeito. Então só o B pode ter mudado a saída. A fórmula pede dois testes em que a condição está ligada, com valores diferentes e saídas diferentes, e não exige que só ela mude.”

**Transição:** “Vamos ver o que isso dá na prática.”

### Slide 15 · O mesmo requisito, nas duas variantes (1 min)

**Na tela:** 6 testes na causa única contra 4 no mascaramento.

**Fala:** “Mesmo requisito, rodado nas duas variantes: 6 testes na causa única, 4 no mascaramento. De onde vem a economia? Quando A é verdadeiro, a metade da direita está desligada; quando A é falso, a da esquerda. O mascaramento aproveita isso: um mesmo teste ajuda a provar duas condições.”

**Transição:** “E qual das duas usar?”

### Slide 16 · Qual das duas usar (1 min)

**Na tela:** a tabela de comparação e a escolha da ferramenta.

**Fala:** “Pela pesquisa de Chilenski, as duas encontram, em geral, os mesmos bugs. O mascaramento pede menos testes e aceita variável repetida sem complicação. Por isso ele é o padrão da ferramenta, como é no GCC. A causa única continua disponível para quem precisa dela, com a opção --unique-cause.”

**Transição:** “Tudo isso não fui eu que inventei. Vou mostrar de onde vem.”

---

## Bloco 4 · Os artigos e as fórmulas

### Slide 17 · Em quem nos apoiamos (1 min)

**Na tela:** os três artigos, cada um com o que trouxe.

**Fala:** “Três artigos sustentam o trabalho. O primeiro, da NASA, explica o que a norma pede, em linguagem de engenheiro. O segundo, de Kapoor e Bowen, transforma isso em fórmulas que um programa consegue calcular. O terceiro mostra um compilador de verdade, o GCC, medindo MC/DC. Quase tudo que a ferramenta faz sai desses três.”

**Transição:** “E cada passo da ferramenta tem uma definição por trás.”

### Slide 18 · De onde vem cada fórmula (45 s)

**Na tela:** a tabela passo, fórmula e fonte.

**Fala:** “Este é o slide para quando alguém perguntar ‘de onde vem essa fórmula?’. Cada passo tem uma definição de Kapoor e Bowen por trás, menos o último: a escolha da menor suíte é uma regra da ferramenta, que eu mostro daqui a pouco.”

**Dica:** não leia a tabela; aponte para ela e siga. Ela é para consulta.

**Transição:** “Agora, a ferramenta.”

---

## Bloco 5 · A ferramenta, a partir de requisitos

### Slide 19 · Do requisito aos testes, passo a passo (1 min 30 s)

**Na tela:** o pipeline de 7 caixas e o Z3 opcional.

**Fala:** “Ela recebe o requisito, que pode ser uma expressão, um arquivo com vários requisitos ou o JSON que sai do DFRS da NAT2TEST. Lê a expressão, separa as condições, cada aparição contando como uma, monta a tabela verdade, acha os pares que vimos na seção 3 e escolhe poucos testes. No fim, entrega a lista de testes dizendo por que cada um está ali. Quando as condições falam da mesma variável, o Z3 entra para descartar o que é impossível.”

**Transição:** “Vou abrir a caixa e mostrar como a ferramenta calcula a fórmula do par.”

### Slide 20 · A fórmula base, em pseudocódigo (1 min 30 s)

**Na tela:** `f(v) ≠ f(vⁱ)` ligada ao pseudocódigo de `decide` e `avalie`.

**Fala:** “Esta é a peça que as duas variantes usam. A fórmula diz: troque só uma condição e veja se a saída muda. A função decide faz isso ao pé da letra: guarda a saída original, avalia a expressão de novo trocando só aquela folha, e compara. As folhas são contadas da esquerda para a direita, e só a folha alvo é invertida, na linha em laranja. Por isso ela troca a aparição, e não a variável: A#1 muda sem mexer em A#2.”

**Transição:** “Com essa peça, a causa única fica curta.”

### Slide 21 · Causa única, em pseudocódigo (1 min 30 s)

**Na tela:** a fórmula decomposta e o laço que acha a gêmea.

**Fala:** “Para cada condição, a ferramenta percorre as linhas em que ela é verdadeira e acha a gêmea. Como cada linha da tabela é um número binário, achar a gêmea é só ligar um bit: é a linha em laranja. Depois vêm as checagens da fórmula: as duas linhas são possíveis, as saídas são diferentes, e a condição decide nas duas. Essa última checagem é o que faz o caso com variável repetida funcionar.”

**Transição:** “No mascaramento, muda um detalhe importante.”

### Slide 22 · Mascaramento, em pseudocódigo (1 min 30 s)

**Na tela:** a fórmula decomposta e os grupos T e F.

**Fala:** “Aqui a ferramenta não procura a gêmea. Primeiro ela filtra: só ficam as linhas em que a condição decide, ou seja, não está mascarada. É a linha em laranja, o ‘sensíveis a c’ da fórmula. Depois separa essas linhas em dois grupos, com a condição verdadeira e com ela falsa, e combina cada linha de um grupo com cada linha do outro, guardando as combinações em que a saída muda. Como as outras condições podem ser diferentes, aparecem muito mais pares. Foi por isso que o mascaramento demorou 5 segundos com 20 entradas, contra 0,2 da causa única.”

**Transição:** “Achados os pares, falta escolher poucos testes.”

### Slide 23 · Como a ferramenta escolhe os testes (1 min 30 s)

**Na tela:** a regra e a tabela passo a passo para `(A and B) or C`.

**Fala:** “A regra é simples. Começa pelas condições com menos opções, porque elas não têm escolha: A só tem um par, então entram V2 e V6. B também só tem um, V2 e V4; como V2 já está na lista, só V4 é novo. C tem três opções; a ferramenta pega a que acrescenta menos, V3 e V4, e só V3 é novo. Resultado: 4 testes, que é o mínimo para 3 condições. É rápido, mas não garante o menor possível em todo caso.”

**Transição:** “A mesma regra, escrita como algoritmo.”

### Slide 24 · Escolha dos testes, em pseudocódigo (1 min)

**Na tela:** o pseudocódigo de `MinimalSuite`, com a ordenação em laranja.

**Fala:** “Primeiro, ordena as condições pela quantidade de pares. Depois, para cada condição, calcula o custo de cada par: quantos testes novos ele acrescentaria. Fica com o mais barato; no empate, prefere o de causa única. Por fim, anota qual par demonstra cada condição. É essa anotação que aparece no relatório como ‘demonstra A, B’. Esta parte é escolha nossa, não vem dos artigos.”

**Transição:** “Agora, a ferramenta rodando.”

### Slide 25 · Exemplo 1: um requisito comum (1 min)

**Na tela:** a saída do terminal para `(A and B) or C`.

**Fala:** “Dei o requisito ‘A and B, or C’. Ela devolveu 4 testes, exatamente os que escolhemos à mão no slide 23, e diz para que serve cada um: V2 prova A e B, V3 prova C, e assim por diante. Isso é ouro numa auditoria, porque cada teste tem um motivo escrito.”

**Transição:** “Às vezes, o problema não está no teste, e sim no requisito.”

### Slide 26 · Exemplo 2: o problema está no requisito (1 min 30 s)

**Na tela:** a saída para o requisito do freio e os três cartões.

**Fala:** “O requisito diz: freio acionado, ou freio acionado e pedal pressionado. Repare que, se o freio está acionado, o resultado já é verdadeiro, e o pedal nunca muda nada. A ferramenta percebe isso: o pedal não tem par, e ela avisa que o requisito pode ser simplificado. Ou seja, ela acha um problema no requisito, antes de alguém escrever código.”

**Transição:** “Lembram do acoplamento fraco? Ele aparece aqui.”

### Slide 27 · Exemplo 3: duas condições, a mesma velocidade (1 min 30 s)

**Na tela:** sem Z3, o teste impossível V6; com Z3, os valores concretos.

**Fala:** “Para a tabela, ‘velocidade maior que 50’ e ‘maior que 100’ são duas letras independentes. Sem ajuda, ela escolhe o teste V6, que pede velocidade até 50 e acima de 100 ao mesmo tempo. Ninguém consegue executar isso. Com o Z3 ligado, a ferramenta descobre sozinha que V5 e V6 são impossíveis, troca V6 por V7 e ainda diz o valor de cada teste: velocidade 101, 51, 0.”

**Transição:** “Isso é o que existe hoje. E o que vem depois?”

### Slide 28 · O que já existe e o que vem depois (45 s)

**Na tela:** pronto (requisitos) e próximo (código).

**Fala:** “A parte de requisitos está pronta. O próximo passo é o código: medir o MC/DC de um programa já testado, como o gcov faz para outras coberturas, e integrar com a NAT2TEST. O motor é o mesmo; muda só de onde vem a expressão.”

**Transição:** “Para fechar, três ideias.”

---

## Encerramento

### Slide 29 · Para levar (45 s)

**Na tela:** os três cartões.

**Fala:** “Se for para lembrar de três coisas: primeiro, no MC/DC cada condição precisa provar que importa, com um par de testes. Segundo, ele não é exaustivo: pede de n + 1 a 2n testes; o exponencial fica com a ferramenta. Terceiro, a ferramenta faz essa conta sozinha, a partir do requisito, e ainda avisa quando o requisito tem algo estranho.”

### Slide 30 · Referências (15 s)

**Fala:** “As referências estão aqui; todas as fórmulas que mostrei têm a página citada no rodapé do slide.”

### Slide 31 · Obrigado. Perguntas?

**Fala:** “Obrigado. Fico à disposição para perguntas.” Deixe o comando da tela visível para quem quiser testar.

---

## Demonstração ao vivo (opcional, 3 a 5 min)

Pode substituir os slides 25 a 27 ou vir logo depois deles. Rode da raiz do projeto:

```bash
# Exemplo 1: requisito comum, causa única (slide 25)
./mcdc analyze "(A and B) or C" --unique-cause

# As duas variantes no mesmo requisito (slide 15)
./mcdc analyze "(A and B) or (not A and C)" --unique-cause
./mcdc analyze "(A and B) or (not A and C)"

# Exemplo 2: condição sem efeito (slide 26)
./mcdc analyze "freio_acionado or (freio_acionado and pedal_pressionado)"

# Exemplo 3: sem e com Z3 (slide 27)
./mcdc analyze "speed > 50 and (speed > 100 or rain)" --unique-cause
./mcdc analyze "speed > 50 and (speed > 100 or rain)" --unique-cause --z3
```

Se algo falhar ao vivo, volte para os slides 25 a 27: eles mostram exatamente essas saídas.

---

## Perguntas prováveis

**“Então o MC/DC é exaustivo?”**
Não. Slide 10: são de n + 1 a 2n testes. O exponencial é o trabalho da ferramenta para achar os pares, e fórmulas gigantes (slide 11).

**“Por que não basta cobertura de decisão?”**
Slide 5: com `A and B` trocado por `A or B`, testar só tudo T e tudo F deixa o bug passar.

**“Por que mascaramento e não causa única?”**
Slide 16: em geral encontram os mesmos bugs (Chilenski, citado por Kvalsvik), e o mascaramento pede menos testes. A causa única está disponível com `--unique-cause`.

**“De onde vem essa fórmula?”**
Slide 18, que tem a definição e a página de cada uma.

**“Como o código calcula isso?”**
Slides 20 a 22 (pares) e 24 (escolha dos testes).

**“A ferramenta acha sempre a menor suíte?”**
Não garante. Slides 23 e 24: a regra gulosa é rápida e, nos exemplos, chega ao mínimo, mas em casos raros pode usar um teste a mais.

**“E se uma combinação for impossível?”**
Slide 27: com `--z3`, a ferramenta descarta as linhas impossíveis e dá valores concretos. Sem o Z3, dá para escrever a restrição à mão com `--constraint`.

**“A NAT2TEST já usa o Z3. Precisa de outro?”**
O solver pode ser o mesmo, mas as perguntas são do MC/DC: “esta combinação é possível?” e “que valores tornam este par real?”. A NAT2TEST faz as perguntas dela, para gerar os testes dela. Na integração, o plugin pode reaproveitar a instalação do Z3 e a tradução do DFRS que a NAT2TEST já tem.

**“Em que nível da DO-178C o MC/DC é exigido?”**
Só no nível A, o de falha catastrófica. O nível B pede cobertura de decisão e o C pede cobertura de comandos. Os níveis D e E não pedem cobertura estrutural.

**“A ferramenta precisaria ser qualificada (DO-330)?”**
Ela é uma ferramenta de verificação: não insere erro no software, mas poderia deixar de detectar um. Isso a coloca no critério 3, nível de qualificação TQL-5. Se o resultado dela for usado para dispensar outras verificações nos níveis A ou B, passa ao critério 2, TQL-4.

**“Como sabemos que os testes gerados pegam defeitos?”**
A ferramenta tem validação por mutação (`--mutation`): cria versões do requisito com um defeito cada, nos tipos de falha de Kapoor e Bowen, e confere se a suíte detecta. Em `A and (B or C)`, a suíte pega 94,1% dos mutantes. O único que passa é `A and B or C`, o mesmo exemplo de Hayhurst e Veerhusen. Há um teste automatizado que confere, em 6 expressões, o teorema de Kapoor e Bowen: um par de causa única por condição detecta sempre cinco tipos de falha.
```bash
./mcdc analyze "A and (B or C)" --mutation
```

**“E se eu já tiver testes? A ferramenta mede?”**
Sim, com o comando `check`. Ele diz quais condições já estão demonstradas, dá a porcentagem de cobertura no estilo do MCDC-Star e sugere os testes que faltam.
```bash
./mcdc check --json exemplos/decisoes.json --tests exemplos/testes.csv
```
