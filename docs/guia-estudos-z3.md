# Guia de estudos: Z3 para a ferramenta MC/DC

Roteiro para entender o Z3 do zero até o ponto de ler e evoluir o módulo `mcdc-z3`, e de conversar com o pessoal da NAT2TEST sobre como eles usam o mesmo solver.

Todos os exemplos deste guia foram rodados no Z3 instalado na máquina (`z3 5.3.2`), e as respostas mostradas são as reais.

## Como usar

São 8 módulos. Cada um tem: o que entender, o que ler, exercícios e a ligação com a ferramenta. Os módulos 1 a 4 bastam para ler o `mcdc-z3` inteiro; os módulos 5 a 8 preparam os próximos passos do roteiro e a conversa com a NAT2TEST.

| Módulo | Assunto | Tempo sugerido |
|---|---|---|
| 0 | Ambiente | 30 min |
| 1 | Lógica proposicional e SAT | 2 a 3 dias |
| 2 | SMT: teorias e tipos | 2 a 3 dias |
| 3 | A linguagem SMT-LIB | 3 a 4 dias |
| 4 | Tipos de dados e enumerações | 1 a 2 dias |
| 5 | Por que uma combinação é impossível (unsat core) | 1 dia |
| 6 | Otimização | 1 a 2 dias |
| 7 | APIs: Python e Java | 2 a 3 dias |
| 8 | Z3 aplicado a MC/DC | 3 a 5 dias |

Escreva todos os exercícios num arquivo `.smt2` e rode no terminal. Digitar é o que fixa a sintaxe.

## Referências principais

| Referência | Para quê |
|---|---|
| **Z3 Guide**, microsoft.github.io/z3guide | Tutorial oficial, com exemplos que rodam no navegador. Ponto de partida de quase todos os módulos. |
| **Programming Z3**, de Bjørner, de Moura, Nachmanson e Wintersteiger, theory.stanford.edu/~nikolaj/programmingz3.html | Texto mais completo: teorias, APIs e como o Z3 funciona por dentro. Os exemplos são em Python. |
| **Padrão SMT-LIB**, smt-lib.org | Referência da linguagem, para consulta. |
| de Moura e Bjørner, *Satisfiability Modulo Theories: Introduction and Applications*, Communications of the ACM, 2011 | Visão geral curta de SMT e onde ele é usado. Boa leitura antes do módulo 2. |
| de Moura e Bjørner, *Z3: An Efficient SMT Solver*, TACAS 2008 | O artigo original do Z3, para citar. |
| Kroening e Strichman, *Decision Procedures: An Algorithmic Point of View*, 2ª ed., Springer | Livro-texto da teoria: SAT, aritmética, igualdade. Para quem quiser entender os algoritmos. |
| Sun et al., *Functional Requirements-Based Automated Testing for Avionics* (na pasta `docs`) | A mesma ideia da ferramenta, com outro verificador (CBMC). |

---

## Módulo 0: ambiente

O Z3 já está instalado (`brew install z3`). Três formas de usar:

```bash
z3 arquivo.smt2                      # roda um arquivo
z3 -in                               # interativo: digite os comandos, Ctrl+D para sair
echo '(check-sat)' | z3 -in          # uma linha só
```

Opcional, para o módulo 7: `pip install z3-solver` instala a API Python, a mais usada nos tutoriais.

---

## Módulo 1: lógica proposicional e SAT

**O que entender**

- **Fórmula satisfatível:** existe pelo menos uma atribuição de verdadeiro/falso às variáveis que a torna verdadeira. Essa atribuição se chama **modelo**.
- **Fórmula insatisfatível (unsat):** nenhuma atribuição funciona.
- **Validade por refutação:** F é sempre verdadeira se e só se `not F` é insatisfatível. É assim que um solver *prova* coisas: ele procura um contraexemplo e mostra que não existe.
- **SAT** é o problema de decidir se uma fórmula proposicional é satisfatível. É difícil no pior caso (NP-completo), mas os solvers modernos resolvem instâncias enormes na prática.

**O que ler**

- Z3 Guide: *Getting Started* e *Basic Commands*.
- Programming Z3: seção de lógica proposicional.

**Exercícios**

1. A tabela verdade da ferramenta é, para cada linha, um modelo candidato. Pegue `(A and B) or C` e escreva no Z3 a pergunta "existe linha com resultado verdadeiro e A falsa?". Resposta esperada: `sat`, por exemplo com `C` verdadeira.

2. **Provar que duas expressões são diferentes.** Este é o exercício mais útil do módulo:

   ```smt
   (declare-const A Bool) (declare-const B Bool) (declare-const C Bool)
   (assert (not (= (and A (or B C)) (or (and A B) C))))
   (check-sat)
   (get-model)
   ```
   ```
   sat
   (define-fun C () Bool true)
   (define-fun A () Bool false)
   (define-fun B () Bool true)
   ```

   `sat` quer dizer que as duas expressões **não** são equivalentes, e o modelo (A=F, B=T, C=T) é a entrada que as diferencia. Se a resposta fosse `unsat`, estaria provado que são equivalentes.

3. Use o mesmo truque para provar que `not (A and B)` é equivalente a `(not A) or (not B)` (De Morgan). Resposta esperada: `unsat`.

**Ligação com a ferramenta.** O exercício 2 é exatamente um "parênteses deslocado", um dos tipos de falha de Kapoor e Bowen. Ele é a base da validação por mutação (seção 6.7 da arquitetura): para cada versão alterada do requisito, o Z3 diz se ela é mesmo diferente e dá a entrada que mostra a diferença.

---

## Módulo 2: SMT, teorias e tipos

**O que entender**

- **SMT** (Satisfiability Modulo Theories) é SAT com **teorias**: em vez de só verdadeiro/falso, as fórmulas falam de inteiros, reais, igualdades e outras estruturas. `speed > 100` é um átomo da teoria da aritmética.
- **Sort** é o tipo de uma variável: `Bool`, `Int`, `Real`, e outros que você pode definir.
- Teorias mais comuns e suas siglas, que aparecem nos tutoriais: aritmética linear inteira (LIA), aritmética linear real (LRA), igualdade com funções não interpretadas (UF).
- **Linear vs. não linear:** `x + 2*y > 3` é linear e o Z3 decide sempre; `x*y > 3` é não linear e pode dar `unknown`.

**O que ler**

- Artigo da CACM (2011): visão geral.
- Z3 Guide: *Theories* → *Arithmetic*.
- Programming Z3: seção de aritmética.

**Exercícios**

1. **Inteiro e real mudam a resposta:**

   ```smt
   (declare-const x Int)
   (assert (and (> x 1) (< x 2)))
   (check-sat)                      ; unsat: não existe inteiro entre 1 e 2
   ```
   ```smt
   (declare-const x Real)
   (assert (and (> x 1.0) (< x 2.0)))
   (check-sat)                      ; sat
   (get-value (x))                  ; ((x (/ 3.0 2.0)))
   ```

   Repare no formato `(/ 3.0 2.0)`: é assim que o Z3 escreve 1,5. O `SmtEncoding.number` converte isso para `1.5`.

2. Escreva as 8 linhas de `speed > 100 or (speed > 50 and rain)` e descubra quais são impossíveis. Resposta: as duas com `speed > 100` verdadeira e `speed > 50` falsa.

3. Troque `speed` de `Int` para `Real` no exercício 2. As linhas impossíveis mudam? (Não mudam, mas os valores do modelo sim.)

**Ligação com a ferramenta.** É aqui que o `SmtEncoding` decide o tipo de cada variável: o tipo declarado no `inputs` do JSON, ou inferido dos valores (`100` vira `Int`, `2.5` vira `Real`). Um tipo errado muda a resposta, como mostra o exercício 1.

---

## Módulo 3: a linguagem SMT-LIB

**O que entender** — os comandos que a ferramenta usa, e mais dois úteis:

| Comando | Para quê |
|---|---|
| `(declare-const x Int)` | Declara uma variável. |
| `(define-fun f ((a Bool) (b Bool)) Bool (and a b))` | Define uma função (uma macro). |
| `(assert F)` | Acrescenta uma fórmula que tem de ser verdadeira. |
| `(check-sat)` | Pergunta se as fórmulas são satisfatíveis: `sat`, `unsat` ou `unknown`. |
| `(get-model)` / `(get-value (x y))` | Depois de `sat`: o modelo inteiro, ou só algumas variáveis. |
| `(push 1)` / `(pop 1)` | Abre e fecha um contexto: o que for declarado dentro some no `pop`. |
| `(set-option :produce-models true)` | Liga a geração de modelos, necessária em alguns modos. |
| `(check-sat-assuming (p (not q)))` | Pergunta com hipóteses temporárias, sem `push`/`pop`. |

Toda a sintaxe é de **S-expressions**: operador primeiro, entre parênteses. `speed > 100` vira `(> speed 100)`, e `-5` vira `(- 5)`.

Nomes com espaço ou símbolo vão entre barras: `|the system mode|`. A ferramenta sempre usa barras, por segurança.

**O que ler**

- Z3 Guide: *Basic Commands* e *Logic*.
- Padrão SMT-LIB: capítulo de comandos, como referência.

**Exercícios**

1. Reproduza na mão o que o `Z3FeasibilityChecker` faz na primeira chamada: um `push`/`assert`/`check-sat`/`pop` por linha, num único arquivo, para as 8 linhas do exemplo do `speed`. Compare a ordem das respostas com a coluna "impossível" do `./mcdc analyze "speed > 100 or (speed > 50 and rain)" --z3`.

2. Faça a segunda chamada: só para as linhas `sat`, acrescente `(get-value (speed rain))`. Tente também pedir valores de uma linha `unsat` e veja o erro: é por isso que a ferramenta faz duas chamadas.

3. Reescreva o exercício 1 com `check-sat-assuming`. Uma forma:

   ```smt
   (declare-const speed Int)
   (declare-const p1 Bool) (declare-const p2 Bool)
   (assert (= p1 (> speed 100)))
   (assert (= p2 (> speed 50)))
   (check-sat-assuming (p1 (not p2)))     ; unsat
   (check-sat-assuming ((not p1) p2))     ; sat
   ```

   Cada condição vira uma variável booleana "rótulo" (`p1`, `p2`), e cada linha é só uma lista de hipóteses. É uma alternativa ao `push`/`pop` que poderia simplificar o código.

**Ligação com a ferramenta.** Depois deste módulo, leia `mcdc-z3/.../Z3FeasibilityChecker.java` e `SmtEncoding.java`: eles só montam, como texto, o que você escreveu nos exercícios 1 e 2.

---

## Módulo 4: tipos de dados e enumerações

**O que entender**

- O SMT-LIB permite declarar tipos próprios com `declare-datatype`. Uma enumeração é o caso mais simples.
- A ferramenta **não** usa isso hoje: ela codifica a enumeração como inteiro de 0 a k−1 com uma restrição de domínio. Os dois jeitos funcionam; o inteiro deixa a leitura da resposta mais simples.

**O que ler**

- Z3 Guide: *Theories* → *Datatypes*.

**Exercícios**

1. Enumeração com tipo próprio:

   ```smt
   (declare-datatype Mode ((idle) (choice) (preparing_strong) (preparing_weak)))
   (declare-const mode Mode)
   (assert (not (= mode idle)))
   (assert (not (= mode choice)))
   (assert (not (= mode preparing_strong)))
   (check-sat)
   (get-value (mode))               ; ((mode preparing_weak))
   ```

2. Faça o mesmo do jeito da ferramenta: `(declare-const mode Int)`, `(assert (and (>= mode 0) (< mode 4)))`, e cada valor vira um número. Confirme que a resposta é a mesma.

3. Escreva a decisão 4 do `exemplos/decisoes.json` à mão e confirme que as linhas V1 e V2 dão `unsat`.

4. Tire da enumeração o valor `preparing_weak` e pergunte de novo o exercício 1. A resposta vira `unsat`. É por isso que a ferramenta acrescenta `_outro` às enumerações que não foram declaradas: sem ele, "nenhum dos valores citados" seria considerado impossível.

**Ligação com a ferramenta.** Uma melhoria possível é trocar a codificação por inteiro por `declare-datatype`: o modelo já viria com o nome do valor, e a restrição de domínio deixaria de ser necessária.

---

## Módulo 5: por que uma combinação é impossível

**O que entender**

- Quando a resposta é `unsat`, o Z3 pode dizer **quais** fórmulas causaram o conflito: o *unsat core*. Para isso, cada fórmula recebe um nome com `(! F :named nome)`.

**O que ler**

- Z3 Guide: *Basic Commands* → unsat cores.

**Exercício**

```smt
(set-option :produce-unsat-cores true)
(declare-const speed Int)
(declare-const rain Bool)
(assert (! (> speed 100) :named c1_verdadeira))
(assert (! (not (> speed 50)) :named c2_falsa))
(assert (! rain :named c3_verdadeira))
(check-sat)                      ; unsat
(get-unsat-core)                 ; (c1_verdadeira c2_falsa)
```

O Z3 aponta que o conflito está entre a condição 1 verdadeira e a condição 2 falsa; `rain` não tem nada a ver.

**Ligação com a ferramenta.** É exatamente o que falta para o diagnóstico de condição sem par (passo 14 do roteiro): em vez de só "linha impossível", o relatório pode dizer "impossível porque `speed > 100` verdadeira contradiz `speed > 50` falsa".

---

## Módulo 6: otimização

**O que entender**

- Além de "existe?", o Z3 responde "qual é o menor/maior?" com `minimize` e `maximize`.
- Também aceita restrições **suaves** (`assert-soft`): tenta satisfazer o máximo possível delas. Isso resolve problemas de "escolher o mínimo de itens que cobrem tudo", como a suíte mínima.

**O que ler**

- Z3 Guide: *Optimization*.
- Programming Z3: seção de otimização (MaxSAT).

**Exercícios**

1. Valor de fronteira:

   ```smt
   (declare-const speed Int)
   (assert (> speed 100))
   (minimize speed)
   (check-sat)
   (get-value (speed))              ; ((speed 101))
   ```

   O resultado é o valor de fronteira de `speed > 100`.

2. Faça o mesmo com `speed >= 100` e com `speed` do tipo `Real` em `speed > 100`. (Em reais não existe "o menor maior que 100": veja o que o Z3 responde.)

3. Desafio: modele a suíte mínima de `(A and B) or C` como otimização. Uma variável booleana por linha da tabela ("a linha está na suíte"); para cada condição, uma restrição dizendo que pelo menos um dos seus pares tem as duas linhas escolhidas; e `minimize` na soma das linhas escolhidas (use `(ite usada 1 0)`). A resposta deve ser 4.

**Ligação com a ferramenta.** O exercício 1 é o passo 16 do roteiro (valores de fronteira), e o 3 é o passo 20 (suíte exata em vez do algoritmo guloso).

---

## Módulo 7: APIs (Python e Java)

**O que entender**

- Em vez de escrever texto SMT-LIB, dá para construir as fórmulas por código. O Z3 tem APIs oficiais em C, C++, Python, Java, .NET e JavaScript.
- A ferramenta usa o **executável** com texto SMT-LIB, de propósito: não exige biblioteca nativa no build e o script pode ser lido e rodado na mão. A API Java fica como otimização, se o número de consultas pesar (seção 6.2 da arquitetura).

**O que ler**

- Programming Z3: todos os exemplos são em Python. Refaça os módulos 1 a 6 em Python, que é o jeito mais rápido de ganhar fluência.
- Repositório do Z3 (github.com/Z3Prover/z3): `examples/java/JavaExample.java`, um exemplo completo da API Java.

**Exercícios**

1. Em Python, refaça o exemplo do `speed`:

   ```python
   from z3 import *
   speed, rain = Int('speed'), Bool('rain')
   s = Solver()
   s.add(speed > 100, Not(speed > 50), rain)
   print(s.check())    # unsat
   ```

2. Ainda em Python, gere as 8 linhas com um laço e imprima `sat`/`unsat` de cada uma. É o `Z3FeasibilityChecker` em 15 linhas.

3. Leia o `JavaExample.java` e identifique os equivalentes Java de `Int`, `Solver`, `add` e `check`. Isso prepara uma possível troca do executável pela API dentro do `mcdc-z3`, ou o reaproveitamento do Z3 que a NAT2TEST já usa.

---

## Módulo 8: Z3 aplicado a MC/DC

**O que entender**

Até aqui, a ferramenta enumera a tabela verdade e usa o Z3 linha a linha. Dá para ir além e pedir ao Z3 **o par de independência diretamente**, sem montar a tabela: são duas cópias das variáveis, uma por vetor, e as regras do par viram restrições.

**Exercícios**

1. **Par de causa única para A em `(A and B) or C`:**

   ```smt
   (declare-const A1 Bool) (declare-const B1 Bool) (declare-const C1 Bool)
   (declare-const A2 Bool) (declare-const B2 Bool) (declare-const C2 Bool)
   (define-fun f ((a Bool) (b Bool) (c Bool)) Bool (or (and a b) c))
   (assert A1)
   (assert (not A2))
   (assert (= B1 B2))
   (assert (= C1 C2))
   (assert (not (= (f A1 B1 C1) (f A2 B2 C2))))
   (check-sat)
   (get-value (A1 B1 C1 A2 B2 C2))
   ```
   ```
   sat
   ((A1 true) (B1 true) (C1 false) (A2 false) (B2 true) (C2 false))
   ```

   O par é (TTF, FTF), ou seja, (V2, V6): o mesmo que a ferramenta calcula enumerando a tabela.

2. **Par de mascaramento para C.** Agora A e B podem mudar, mas C precisa decidir o resultado nos dois vetores. "C decide em um vetor" vira: o resultado muda quando só C é invertida.

   ```smt
   (assert C1)
   (assert (not C2))
   (assert (not (= (f A1 B1 C1) (f A2 B2 C2))))
   (assert (not (= (f A1 B1 C1) (f A1 B1 (not C1)))))   ; C decide no vetor 1
   (assert (not (= (f A2 B2 C2) (f A2 B2 (not C2)))))   ; C decide no vetor 2
   (assert (or (not (= A1 A2)) (not (= B1 B2))))        ; algo além de C muda
   ```

   Monte o resto do arquivo (declarações, `f`, `check-sat`, `get-value`). Resposta esperada: um par como (FTT, TFF), ou seja, (V5, V4), que está na lista de mascaramento da ferramenta e que a causa única não aceita.

3. Some os dois mundos: acrescente ao exercício 1 os predicados de verdade (`A` vira `speed > 100`, com `speed1` e `speed2` inteiros). Agora o Z3 encontra, numa só pergunta, um par possível **e** os valores concretos.

**Ligação com a ferramenta.** Essa formulação resolve o problema de escala (passo 15 do roteiro): com 20 entradas a tabela tem 1 milhão de linhas, mas a pergunta "existe um par para esta condição?" continua sendo uma consulta só. É a mesma ideia das *trap properties* do artigo do Sun et al. e dos trabalhos de Rayadurgam e Heimdahl citados por Kapoor e Bowen: cada objetivo de teste vira uma fórmula, e o verificador gera o vetor ou prova que ele não existe.

---

## Para a conversa com a NAT2TEST

Como a NAT2TEST já usa o Z3, vale levar estas perguntas depois do módulo 7:

1. **Codificação:** como eles traduzem o DFRS para o Z3? Tipos, enumerações, tempo. Se a codificação deles já existe, o plugin pode reaproveitá-la em vez de manter a do `SmtEncoding`.
2. **Forma de uso:** API Java ou executável? Se for a API, o plugin pode usar a mesma dependência dentro do produto Eclipse.
3. **Alcançabilidade:** o Z3 da ferramenta verifica se uma combinação é possível olhando só a guarda. A NAT2TEST gera testes seguindo o sistema ao longo do tempo. Ela consegue dizer se um vetor da suíte mínima é alcançável e com qual sequência de passos? Isso fecharia o ciclo: a ferramenta escolhe **quais** testes o MC/DC exige, e a NAT2TEST diz **como** chegar neles.
