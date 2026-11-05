# Tutorial: o motor MC/DC, do zero ao terminal

> **Nota:** este tutorial reproduz a primeira versão do motor. O código do repositório já evoluiu além dele: comparações no parser, leitura do JSON da NAT2TEST, relatórios em JSON e CSV e condições por ocorrência (`A#1`, `A#2`). O estado atual está em [implementacao-fase1.md](implementacao-fase1.md).

Ao fim deste tutorial você terá escrito o motor MC/DC da Fase 1 e um comando para usá-lo no terminal:

```
$ ./mcdc analyze "(A and B) or C"
Requisito: REQ
Decisão:   (A and B) or C
Variante:  mascaramento

Vetor A   B   C   | D
V1    T   T   T   | T
V2    T   T   F   | T
V3    T   F   T   | T
V4    T   F   F   | F
V5    F   T   T   | T
V6    F   T   F   | F
V7    F   F   T   | T
V8    F   F   F   | F

Pares de independência:
  A: (V2, V6)
  B: (V2, V4)
  C: (V3, V4), (V3, V6), (V3, V8), (V5, V4), (V5, V6), (V5, V8), ... (9 pares)

Suíte mínima (4 testes):
  V2  TTF  -> T
  V3  TFT  -> T
  V4  TFF  -> F
  V6  FTF  -> F

Cobertura MC/DC: completa
```

## Como usar

Cada passo explica uma ideia e traz **todos os arquivos completos** para digitar. Digite primeiro o teste, rode e veja falhar; depois o código, e veja passar.

Quando um passo altera um arquivo que já existe, ele mostra o arquivo inteiro de novo: é só substituir todo o conteúdo.

Todos os arquivos deste tutorial foram compilados e testados nesta ordem, com JDK 21. A coluna "Testes" diz quantos testes o `mvn verify` deve rodar, todos passando, ao fim de cada passo.

| Passo | O que você constrói | Testes |
|---|---|---|
| 0 | Ambiente | 3 |
| 1 | Lista de condições de uma expressão | 4 |
| 2 | Tabela verdade | 8 |
| 3 | Primeira execução no terminal | 8 |
| 4 | Pares de independência (causa única) | 11 |
| 5 | Suíte mínima | 13 |
| 6 | Parser: digitar a expressão no terminal | 17 |
| 7 | Mascaramento | 19 |
| 8 | Linhas impossíveis (restrições) | 22 |
| 9 | Fachada do motor | 25 |
| 10 | Comando `mcdc` | 29 |

Os passos 1 a 3 são curtos e já mostram a tabela verdade no terminal.

---

## Passo 0: ambiente

### Terminal

O projeto é compilado para Java 21. Use o JDK 21, o mesmo do seu outro projeto (coloque no `~/.zshrc` para não repetir):

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
```

Na pasta do projeto:

```bash
mvn clean verify
```

Deve terminar com `BUILD SUCCESS` e 3 testes. O `clean` apaga as classes compiladas antes; use-o sempre que trocar a versão do Java ou se aparecer um erro como `compiled by a more recent version of the Java Runtime`. No dia a dia, `mvn verify` basta. Se travar sem mensagem, o macOS provavelmente está pedindo permissão para o Java acessar a pasta `Documents`: libere em Ajustes do Sistema → Privacidade e Segurança → Arquivos e Pastas.

### Eclipse

Funciona com qualquer Eclipse 2023-12 ou mais novo, inclusive o pacote "Eclipse IDE for RCP and RAP Developers".

1. **JDK 21:** confira em Settings (ou Preferences) → Java → Installed JREs. Se não estiver na lista: Add → Standard VM, e em "JRE home" cole o resultado de `/usr/libexec/java_home -v 21`.
2. **Importar:** File → Import → Maven → Existing Maven Projects → selecione a pasta `Tool_MCDC_Java`. Aparecem `mcdc-parent`, `mcdc-core` e `mcdc-requirements`. O Eclipse não copia nada: os arquivos continuam na pasta do repositório.
3. **Rodar os testes:** botão direito no projeto → Run As → JUnit Test.

**Atalho para criar arquivos:** copie o conteúdo completo de uma classe, clique na pasta `src/main/java` (ou `src/test/java`) do projeto certo no Package Explorer e cole (Cmd+V). O Eclipse lê o `package` e o nome da classe e cria o arquivo no lugar certo. Para substituir um arquivo existente, abra-o, selecione tudo e cole por cima.

Se o Eclipse acusar erro de configuração depois de mudar um `pom.xml`: botão direito no projeto → Maven → Update Project.

---

## Passo 1: listar as condições da expressão

A tabela verdade precisa saber quais condições existem e em que ordem viram colunas. Em `(A and B) or (C and A)` as condições são `A`, `B`, `C`: ordem de primeira aparição, sem repetir.

Como `Expr` é uma interface `sealed` que só pode ser `Cond`, `And`, `Or` ou `Not`, um `switch` com padrões de record (Java 21) trata todos os casos e desmonta cada nó numa linha. Se um dia surgir um novo tipo de nó, o compilador aponta todo `switch` que ficou incompleto.

O `LinkedHashSet` guarda a ordem de inserção e ignora repetidos.

**Teste** (substitui o arquivo existente; o teste novo é o último):

**Arquivo:** `mcdc-core/src/test/java/io/github/rvdomingos/mcdc/core/model/ExprTest.java`

```java
package io.github.rvdomingos.mcdc.core.model;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

class ExprTest {

    // (A and B) or C
    private final Expr decision = new Or(new And(new Cond("A"), new Cond("B")), new Cond("C"));

    @Test
    void evaluatesAndOr() {
        assertTrue(decision.eval(Map.of("A", true, "B", true, "C", false)));
        assertFalse(decision.eval(Map.of("A", true, "B", false, "C", false)));
        assertTrue(decision.eval(Map.of("A", false, "B", false, "C", true)));
    }

    @Test
    void evaluatesNot() {
        Expr expr = new And(new Cond("A"), new Not(new Cond("B")));
        assertTrue(expr.eval(Map.of("A", true, "B", false)));
        assertFalse(expr.eval(Map.of("A", true, "B", true)));
    }

    @Test
    void rejectsMissingCondition() {
        assertThrows(IllegalArgumentException.class, () -> decision.eval(Map.of("A", true, "B", true)));
    }

    @Test
    void listsConditionsInOrderWithoutRepetition() {
        // (A and B) or (C and A)
        Expr expr = new Or(new And(new Cond("A"), new Cond("B")), new And(new Cond("C"), new Cond("A")));
        assertEquals(List.of("A", "B", "C"), expr.conditions());
    }
}
```

**Código** (substitui o arquivo existente):

**Arquivo:** `mcdc-core/src/main/java/io/github/rvdomingos/mcdc/core/model/Expr.java`

```java
package io.github.rvdomingos.mcdc.core.model;

import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/** Expressão booleana de uma decisão. As folhas são condições atômicas. */
public sealed interface Expr permits Cond, And, Or, Not {

    /** Avalia a expressão para os valores dados, indexados pelo id da condição. */
    boolean eval(Map<String, Boolean> values);

    /** Ids das condições na ordem em que aparecem pela primeira vez, sem repetição. */
    default List<String> conditions() {
        Set<String> ids = new LinkedHashSet<>();
        collect(this, ids);
        return List.copyOf(ids);
    }

    private static void collect(Expr expr, Set<String> ids) {
        switch (expr) {
            case Cond(var id) -> ids.add(id);
            case And(var left, var right) -> {
                collect(left, ids);
                collect(right, ids);
            }
            case Or(var left, var right) -> {
                collect(left, ids);
                collect(right, ids);
            }
            case Not(var operand) -> collect(operand, ids);
        }
    }
}
```

`mvn verify`: 4 testes.

---

## Passo 2: a tabela verdade

### A ideia: cada linha é um número binário

Com N condições há 2^N linhas. Numere as linhas de 0 a 2^N − 1 e escreva o número em binário com N dígitos: cada dígito é uma condição, **0 significa T e 1 significa F**. A linha 0 fica com tudo verdadeiro.

| Linha | Binário | A | B | C |
|---|---|---|---|---|
| 0 (V1) | 000 | T | T | T |
| 1 (V2) | 001 | T | T | F |
| 2 (V3) | 010 | T | F | T |
| ... | | | | |
| 7 (V8) | 111 | F | F | F |

A condição de posição `i` corresponde ao bit `1 << (n - 1 - i)`: a primeira condição é o bit mais à esquerda. Esse cálculo fica no método `bit(n, i)`, que o passo 4 reaproveita.

Com 20 condições a tabela já passa de um milhão de linhas. Acima disso, o código recusa com exceção.

O `values` de cada linha é um `LinkedHashMap`, para `bits()` sair na ordem das condições.

**Teste** (novo):

**Arquivo:** `mcdc-core/src/test/java/io/github/rvdomingos/mcdc/core/TruthTableTest.java`

```java
package io.github.rvdomingos.mcdc.core;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Or;
import java.util.stream.Collectors;
import org.junit.jupiter.api.Test;

class TruthTableTest {

    // (A and B) or C
    private final Expr decision = new Or(new And(new Cond("A"), new Cond("B")), new Cond("C"));

    @Test
    void hasOneRowPerCombination() {
        TruthTable table = TruthTable.of(decision);
        assertEquals(8, table.rows().size());
    }

    @Test
    void firstRowIsAllTrueAndLastIsAllFalse() {
        TruthTable table = TruthTable.of(decision);
        assertEquals("TTT", table.rows().get(0).bits());
        assertEquals("FFF", table.rows().get(7).bits());
    }

    @Test
    void computesOutcomeOfEachRow() {
        TruthTable table = TruthTable.of(decision);
        String outcomes = table.rows().stream()
                .map(row -> row.outcome() ? "T" : "F")
                .collect(Collectors.joining());
        assertEquals("TTTFTFTF", outcomes);
    }

    @Test
    void rejectsTooManyConditions() {
        Expr expr = new Cond("C0");
        for (int i = 1; i <= TruthTable.MAX_CONDITIONS; i++) {
            expr = new Or(expr, new Cond("C" + i));
        }
        Expr tooBig = expr;
        assertThrows(IllegalArgumentException.class, () -> TruthTable.of(tooBig));
    }
}
```

**Código** (novos):

**Arquivo:** `mcdc-core/src/main/java/io/github/rvdomingos/mcdc/core/TestVector.java`

```java
package io.github.rvdomingos.mcdc.core;

import java.util.Map;
import java.util.stream.Collectors;

/**
 * Uma linha da tabela verdade.
 *
 * @param index   posição na tabela, começando em 0
 * @param values  valor de cada condição, na ordem das condições da decisão
 * @param outcome resultado da decisão para esses valores
 */
public record TestVector(int index, Map<String, Boolean> values, boolean outcome) {

    /** Nome usado nos relatórios: V1, V2, ... */
    public String name() {
        return "V" + (index + 1);
    }

    /** Valores das condições como texto, ex.: "TTF". */
    public String bits() {
        return values.values().stream()
                .map(value -> value ? "T" : "F")
                .collect(Collectors.joining());
    }
}
```

**Arquivo:** `mcdc-core/src/main/java/io/github/rvdomingos/mcdc/core/TruthTable.java`

```java
package io.github.rvdomingos.mcdc.core;

import io.github.rvdomingos.mcdc.core.model.Expr;
import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Tabela verdade completa de uma expressão. A linha 0 tem todas as condições verdadeiras. */
public record TruthTable(List<String> conditions, List<TestVector> rows) {

    public static final int MAX_CONDITIONS = 20;

    public static TruthTable of(Expr expr) {
        List<String> conditions = expr.conditions();
        int n = conditions.size();
        if (n > MAX_CONDITIONS) {
            throw new IllegalArgumentException(
                    "Decisão com " + n + " condições; o limite é " + MAX_CONDITIONS);
        }

        List<TestVector> rows = new ArrayList<>();
        for (int row = 0; row < (1 << n); row++) {
            Map<String, Boolean> values = new LinkedHashMap<>();
            for (int i = 0; i < n; i++) {
                values.put(conditions.get(i), (row & bit(n, i)) == 0);
            }
            rows.add(new TestVector(row, Collections.unmodifiableMap(values), expr.eval(values)));
        }
        return new TruthTable(conditions, List.copyOf(rows));
    }

    /** Máscara do bit da condição i. A primeira condição é o bit mais significativo. */
    static int bit(int n, int i) {
        return 1 << (n - 1 - i);
    }

    public String format() {
        var sb = new StringBuilder();
        sb.append(String.format("%-6s", "Vetor"));
        for (String condition : conditions) {
            sb.append(column(condition, condition));
        }
        sb.append("| D\n");
        for (TestVector row : rows) {
            sb.append(String.format("%-6s", row.name()));
            for (String condition : conditions) {
                sb.append(column(row.values().get(condition) ? "T" : "F", condition));
            }
            sb.append("| ").append(row.outcome() ? "T" : "F").append('\n');
        }
        return sb.toString();
    }

    /** Alinha o texto na largura da coluna, que acompanha o tamanho do nome da condição. */
    private static String column(String text, String condition) {
        return String.format("%-" + (condition.length() + 3) + "s", text);
    }
}
```

`mvn verify`: 8 testes.

---

## Passo 3: primeira execução no terminal

A demo fica em `mcdc-requirements`, e não no core, porque no passo 6 ela vai usar o parser de expressões que mora nesse módulo.

**Código** (novo; crie o pacote `demo`):

**Arquivo:** `mcdc-requirements/src/main/java/io/github/rvdomingos/mcdc/requirements/demo/McdcDemo.java`

```java
package io.github.rvdomingos.mcdc.requirements.demo;

import io.github.rvdomingos.mcdc.core.TruthTable;
import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Or;

public class McdcDemo {

    public static void main(String[] args) {
        // (A and B) or C
        Expr expr = new Or(new And(new Cond("A"), new Cond("B")), new Cond("C"));

        TruthTable table = TruthTable.of(expr);
        System.out.println("Decisão: (A and B) or C");
        System.out.println();
        System.out.print(table.format());
    }
}
```

No terminal, na pasta do projeto:

```bash
mvn -q compile
CP=mcdc-core/target/classes:mcdc-requirements/target/classes
"$JAVA_HOME/bin/java" -cp $CP io.github.rvdomingos.mcdc.requirements.demo.McdcDemo
```

```
Decisão: (A and B) or C

Vetor A   B   C   | D
V1    T   T   T   | T
V2    T   T   F   | T
V3    T   F   T   | T
V4    T   F   F   | F
V5    F   T   T   | T
V6    F   T   F   | F
V7    F   F   T   | T
V8    F   F   F   | F
```

Use `"$JAVA_HOME/bin/java"`, e não só `java`: o `java` do PATH pode ser o 17, que não roda classes compiladas para 21.

No Eclipse: botão direito em `McdcDemo` → Run As → Java Application.

Troque a expressão no código, por exemplo para `new And(new Cond("A"), new Not(new Cond("B")))` (importe `Not`), e rode de novo.

---

## Passo 4: pares de independência (causa única)

Para cada condição, procuramos pares de vetores que provam que ela, sozinha, muda o resultado. Na variante **causa única**, entre os dois vetores muda só a condição analisada, e o resultado muda.

### A ideia: virar um bit

Pela numeração do passo 2, a linha com a condição `i` invertida é a mesma linha com o bit `i` trocado. Partindo das linhas em que a condição é verdadeira (bit 0), a linha "gêmea" é `row | mask`, onde `mask = bit(n, i)`.

Condição A em `(A and B) or C` (mask = `100`):

| Linha com A = T | Gêmea com A = F | Resultados | Par? |
|---|---|---|---|
| V1 `000` TTT | V5 `100` FTT | T / T | não |
| V2 `001` TTF | V6 `101` FTF | T / F | **sim** |
| V3 `010` TFT | V7 `110` FFT | T / T | não |
| V4 `011` TFF | V8 `111` FFF | F / F | não |

Uma condição pode não ter par nenhum. Em `A or (A and B)`, B nunca muda o resultado sozinha: é uma condição redundante no requisito, e a ferramenta deve apontar isso.

**Teste** (novo):

**Arquivo:** `mcdc-core/src/test/java/io/github/rvdomingos/mcdc/core/IndependencePairsTest.java`

```java
package io.github.rvdomingos.mcdc.core;

import static org.junit.jupiter.api.Assertions.assertEquals;

import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

class IndependencePairsTest {

    // (A and B) or C
    private final Expr andOr = new Or(new And(new Cond("A"), new Cond("B")), new Cond("C"));

    @Test
    void findsPairsForAndOr() {
        Map<String, List<IndependencePair>> pairs = IndependencePairs.uniqueCause(TruthTable.of(andOr));

        assertEquals("[(V2, V6)]", pairs.get("A").toString());
        assertEquals("[(V2, V4)]", pairs.get("B").toString());
        assertEquals("[(V3, V4), (V5, V6), (V7, V8)]", pairs.get("C").toString());
    }

    @Test
    void findsPairsWithNegation() {
        // A and not B
        Expr expr = new And(new Cond("A"), new Not(new Cond("B")));
        Map<String, List<IndependencePair>> pairs = IndependencePairs.uniqueCause(TruthTable.of(expr));

        assertEquals("[(V2, V4)]", pairs.get("A").toString());
        assertEquals("[(V1, V2)]", pairs.get("B").toString());
    }

    @Test
    void conditionWithoutEffectHasNoPair() {
        // A or (A and B): B nunca muda o resultado sozinha
        Expr expr = new Or(new Cond("A"), new And(new Cond("A"), new Cond("B")));
        Map<String, List<IndependencePair>> pairs = IndependencePairs.uniqueCause(TruthTable.of(expr));

        assertEquals(List.of(), pairs.get("B"));
    }
}
```

**Código** (novos):

**Arquivo:** `mcdc-core/src/main/java/io/github/rvdomingos/mcdc/core/IndependencePair.java`

```java
package io.github.rvdomingos.mcdc.core;

/**
 * Dois vetores que mostram o efeito independente de uma condição.
 *
 * @param condition  condição analisada
 * @param whenTrue   vetor em que a condição é verdadeira
 * @param whenFalse  vetor em que a condição é falsa
 */
public record IndependencePair(String condition, TestVector whenTrue, TestVector whenFalse) {

    @Override
    public String toString() {
        return "(" + whenTrue.name() + ", " + whenFalse.name() + ")";
    }
}
```

O `toString()` no formato `(V2, V6)` é usado pelos testes e pela saída no terminal.

**Arquivo:** `mcdc-core/src/main/java/io/github/rvdomingos/mcdc/core/IndependencePairs.java`

```java
package io.github.rvdomingos.mcdc.core;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class IndependencePairs {

    private IndependencePairs() {
    }

    /**
     * Pares de causa única: só a condição analisada muda entre os dois vetores, e o resultado muda.
     * O mapa segue a ordem das condições; condição sem par fica com lista vazia.
     */
    public static Map<String, List<IndependencePair>> uniqueCause(TruthTable table) {
        List<String> conditions = table.conditions();
        int n = conditions.size();
        Map<String, List<IndependencePair>> result = new LinkedHashMap<>();

        for (int i = 0; i < n; i++) {
            int mask = TruthTable.bit(n, i);
            List<IndependencePair> pairs = new ArrayList<>();
            for (TestVector row : table.rows()) {
                if ((row.index() & mask) != 0) {
                    continue; // só parte das linhas em que a condição é verdadeira
                }
                TestVector flipped = table.rows().get(row.index() | mask);
                if (row.outcome() != flipped.outcome()) {
                    pairs.add(new IndependencePair(conditions.get(i), row, flipped));
                }
            }
            result.put(conditions.get(i), List.copyOf(pairs));
        }
        return result;
    }
}
```

**Demo** (substitui a anterior):

**Arquivo:** `mcdc-requirements/src/main/java/io/github/rvdomingos/mcdc/requirements/demo/McdcDemo.java`

```java
package io.github.rvdomingos.mcdc.requirements.demo;

import io.github.rvdomingos.mcdc.core.IndependencePair;
import io.github.rvdomingos.mcdc.core.IndependencePairs;
import io.github.rvdomingos.mcdc.core.TruthTable;
import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Or;
import java.util.List;
import java.util.Map;

public class McdcDemo {

    public static void main(String[] args) {
        // (A and B) or C
        Expr expr = new Or(new And(new Cond("A"), new Cond("B")), new Cond("C"));

        TruthTable table = TruthTable.of(expr);
        System.out.println("Decisão: (A and B) or C");
        System.out.println();
        System.out.print(table.format());

        Map<String, List<IndependencePair>> pairs = IndependencePairs.uniqueCause(table);
        System.out.println();
        System.out.println("Pares de independência (causa única):");
        pairs.forEach((condition, list) ->
                System.out.println("  " + condition + ": " + (list.isEmpty() ? "nenhum par" : list)));
    }
}
```

`mvn verify`: 11 testes. Rode a demo como no passo 3; agora aparecem os pares:

```
Pares de independência (causa única):
  A: [(V2, V6)]
  B: [(V2, V4)]
  C: [(V3, V4), (V5, V6), (V7, V8)]
```

---

## Passo 5: suíte mínima

Agora escolhemos um par por condição de forma que o total de vetores seja o menor possível. Pares de condições diferentes podem compartilhar vetores; é isso que permite chegar a N + 1 testes em vez de 2N.

### A ideia: algoritmo guloso

1. Comece pelas condições com **menos** pares: elas não têm escolha, e o que for escolhido para elas ajuda as outras.
2. Para cada condição, pegue o par que acrescenta **menos vetores novos** ao que já foi escolhido.

| Condição | Pares disponíveis | Escolha | Vetores escolhidos |
|---|---|---|---|
| A | (V2, V6) | (V2, V6) | V2, V6 |
| B | (V2, V4) | (V2, V4), só V4 é novo | V2, V4, V6 |
| C | (V3, V4), (V5, V6), (V7, V8) | (V3, V4), só V3 é novo | V2, V3, V4, V6 |

O guloso é rápido mas nem sempre acha o mínimo absoluto. Dá para trocá-lo depois por uma busca exata sem mudar a assinatura.

Um `TreeMap` indexado pelo número do vetor evita duplicatas e já devolve tudo em ordem.

**Teste** (novo):

**Arquivo:** `mcdc-core/src/test/java/io/github/rvdomingos/mcdc/core/MinimalSuiteTest.java`

```java
package io.github.rvdomingos.mcdc.core;

import static org.junit.jupiter.api.Assertions.assertEquals;

import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import java.util.List;
import java.util.stream.Collectors;
import org.junit.jupiter.api.Test;

class MinimalSuiteTest {

    private static String suiteOf(Expr expr) {
        List<TestVector> suite = MinimalSuite.greedy(IndependencePairs.uniqueCause(TruthTable.of(expr)));
        return suite.stream().map(TestVector::name).collect(Collectors.joining(", "));
    }

    @Test
    void andOrNeedsFourTests() {
        // (A and B) or C
        assertEquals("V2, V3, V4, V6", suiteOf(new Or(new And(new Cond("A"), new Cond("B")), new Cond("C"))));
    }

    @Test
    void andNotNeedsThreeTests() {
        // A and not B
        assertEquals("V1, V2, V4", suiteOf(new And(new Cond("A"), new Not(new Cond("B")))));
    }
}
```

**Código** (novo):

**Arquivo:** `mcdc-core/src/main/java/io/github/rvdomingos/mcdc/core/MinimalSuite.java`

```java
package io.github.rvdomingos.mcdc.core;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

public final class MinimalSuite {

    private MinimalSuite() {
    }

    /**
     * Escolha gulosa: trata primeiro as condições com menos pares e, para cada uma,
     * pega o par que acrescenta menos vetores novos. Rápida, mas nem sempre ótima.
     */
    public static List<TestVector> greedy(Map<String, List<IndependencePair>> pairsByCondition) {
        Map<Integer, TestVector> selected = new TreeMap<>();

        List<List<IndependencePair>> byFewestPairs = new ArrayList<>(pairsByCondition.values());
        byFewestPairs.sort(Comparator.comparingInt(List::size));

        for (List<IndependencePair> pairs : byFewestPairs) {
            IndependencePair best = null;
            int bestCost = Integer.MAX_VALUE;
            for (IndependencePair pair : pairs) {
                int cost = (selected.containsKey(pair.whenTrue().index()) ? 0 : 1)
                        + (selected.containsKey(pair.whenFalse().index()) ? 0 : 1);
                if (cost < bestCost) {
                    best = pair;
                    bestCost = cost;
                }
            }
            if (best != null) {
                selected.put(best.whenTrue().index(), best.whenTrue());
                selected.put(best.whenFalse().index(), best.whenFalse());
            }
        }
        return List.copyOf(selected.values());
    }
}
```

**Demo** (substitui a anterior):

**Arquivo:** `mcdc-requirements/src/main/java/io/github/rvdomingos/mcdc/requirements/demo/McdcDemo.java`

```java
package io.github.rvdomingos.mcdc.requirements.demo;

import io.github.rvdomingos.mcdc.core.IndependencePair;
import io.github.rvdomingos.mcdc.core.IndependencePairs;
import io.github.rvdomingos.mcdc.core.MinimalSuite;
import io.github.rvdomingos.mcdc.core.TestVector;
import io.github.rvdomingos.mcdc.core.TruthTable;
import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Or;
import java.util.List;
import java.util.Map;

public class McdcDemo {

    public static void main(String[] args) {
        // (A and B) or C
        Expr expr = new Or(new And(new Cond("A"), new Cond("B")), new Cond("C"));

        TruthTable table = TruthTable.of(expr);
        System.out.println("Decisão: (A and B) or C");
        System.out.println();
        System.out.print(table.format());

        Map<String, List<IndependencePair>> pairs = IndependencePairs.uniqueCause(table);
        System.out.println();
        System.out.println("Pares de independência (causa única):");
        pairs.forEach((condition, list) ->
                System.out.println("  " + condition + ": " + (list.isEmpty() ? "nenhum par" : list)));

        List<TestVector> suite = MinimalSuite.greedy(pairs);
        System.out.println();
        System.out.println("Suíte mínima (" + suite.size() + " testes):");
        for (TestVector vector : suite) {
            System.out.println("  " + vector.name() + "  " + vector.bits() + "  -> " + (vector.outcome() ? "T" : "F"));
        }
    }
}
```

`mvn verify`: 13 testes. A demo agora termina com:

```
Suíte mínima (4 testes):
  V2  TTF  -> T
  V3  TFT  -> T
  V4  TFF  -> F
  V6  FTF  -> F
```

---

## Passo 6: digitar a expressão no terminal

Um parser transforma o texto `(A and B) or not C` na árvore `Expr`. Ele fica em `mcdc-requirements`, porque é um adaptador de entrada.

### A ideia: descida recursiva

A gramática tem uma regra por nível de precedência, e cada regra vira um método:

```
expr   := termo ( "or" termo )*                 -> expr()
termo  := fator ( "and" fator )*                -> term()
fator  := "not" fator | "(" expr ")" | IDENT    -> factor()
```

Como `expr()` chama `term()`, que chama `factor()`, o `and` fica mais "preso" que o `or`: `A or B and C` vira `A or (B and C)`. O parêntese funciona porque `factor()` chama `expr()` de volta.

Antes do parser, o tokenizador quebra o texto em pedaços (`(`, `A`, `and`, ...), traduz `&&`, `||` e `!` para `and`, `or` e `not`, e põe as palavras-chave em minúsculas.

Os testes comparam árvores com `assertEquals` direto: records já vêm com `equals` campo a campo.

**Teste** (novo):

**Arquivo:** `mcdc-requirements/src/test/java/io/github/rvdomingos/mcdc/requirements/ExpressionParserTest.java`

```java
package io.github.rvdomingos.mcdc.requirements;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import org.junit.jupiter.api.Test;

class ExpressionParserTest {

    private static final Cond A = new Cond("A");
    private static final Cond B = new Cond("B");
    private static final Cond C = new Cond("C");

    @Test
    void parsesParentheses() {
        assertEquals(new Or(new And(A, B), C), ExpressionParser.parse("(A and B) or C"));
    }

    @Test
    void andBindsTighterThanOr() {
        assertEquals(new Or(A, new And(B, C)), ExpressionParser.parse("A or B and C"));
    }

    @Test
    void acceptsSymbolsAndUppercaseKeywords() {
        assertEquals(new And(new Not(A), B), ExpressionParser.parse("!A && B"));
        assertEquals(new Or(A, new Not(B)), ExpressionParser.parse("A OR NOT B"));
    }

    @Test
    void rejectsInvalidExpressions() {
        assertThrows(IllegalArgumentException.class, () -> ExpressionParser.parse("A and"));
        assertThrows(IllegalArgumentException.class, () -> ExpressionParser.parse("(A or B"));
        assertThrows(IllegalArgumentException.class, () -> ExpressionParser.parse("A $ B"));
        assertThrows(IllegalArgumentException.class, () -> ExpressionParser.parse("A B"));
    }
}
```

**Código** (novo):

**Arquivo:** `mcdc-requirements/src/main/java/io/github/rvdomingos/mcdc/requirements/ExpressionParser.java`

```java
package io.github.rvdomingos.mcdc.requirements;

import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Set;

/**
 * Lê expressões como "(A and B) or not C". Também aceita &&, || e !.
 *
 * <pre>
 * expr   := termo ( "or" termo )*
 * termo  := fator ( "and" fator )*
 * fator  := "not" fator | "(" expr ")" | IDENT
 * </pre>
 */
public final class ExpressionParser {

    private static final Set<String> KEYWORDS = Set.of("and", "or", "not");

    private final List<String> tokens;
    private int pos;

    private ExpressionParser(String text) {
        this.tokens = tokenize(text);
    }

    public static Expr parse(String text) {
        var parser = new ExpressionParser(text);
        Expr expr = parser.expr();
        if (parser.pos < parser.tokens.size()) {
            throw new IllegalArgumentException("Sobrou texto na expressão: " + parser.tokens.get(parser.pos));
        }
        return expr;
    }

    private Expr expr() {
        Expr left = term();
        while (accept("or")) {
            left = new Or(left, term());
        }
        return left;
    }

    private Expr term() {
        Expr left = factor();
        while (accept("and")) {
            left = new And(left, factor());
        }
        return left;
    }

    private Expr factor() {
        if (accept("not")) {
            return new Not(factor());
        }
        if (accept("(")) {
            Expr inner = expr();
            if (!accept(")")) {
                throw new IllegalArgumentException("Faltou fechar parêntese");
            }
            return inner;
        }
        if (pos >= tokens.size()) {
            throw new IllegalArgumentException("Expressão incompleta");
        }
        String token = tokens.get(pos++);
        if (KEYWORDS.contains(token) || token.equals("(") || token.equals(")")) {
            throw new IllegalArgumentException("Esperava uma condição, encontrei: " + token);
        }
        return new Cond(token);
    }

    private boolean accept(String token) {
        if (pos < tokens.size() && tokens.get(pos).equals(token)) {
            pos++;
            return true;
        }
        return false;
    }

    private static List<String> tokenize(String text) {
        List<String> tokens = new ArrayList<>();
        int i = 0;
        while (i < text.length()) {
            char c = text.charAt(i);
            if (Character.isWhitespace(c)) {
                i++;
            } else if (c == '(' || c == ')') {
                tokens.add(String.valueOf(c));
                i++;
            } else if (c == '!') {
                tokens.add("not");
                i++;
            } else if (text.startsWith("&&", i)) {
                tokens.add("and");
                i += 2;
            } else if (text.startsWith("||", i)) {
                tokens.add("or");
                i += 2;
            } else if (Character.isLetterOrDigit(c) || c == '_') {
                int start = i;
                while (i < text.length() && (Character.isLetterOrDigit(text.charAt(i)) || text.charAt(i) == '_')) {
                    i++;
                }
                String word = text.substring(start, i);
                String lower = word.toLowerCase(Locale.ROOT);
                tokens.add(KEYWORDS.contains(lower) ? lower : word);
            } else {
                throw new IllegalArgumentException("Caractere inválido '" + c + "' na posição " + i);
            }
        }
        return tokens;
    }
}
```

**Demo** (substitui a anterior; agora lê a expressão do argumento):

**Arquivo:** `mcdc-requirements/src/main/java/io/github/rvdomingos/mcdc/requirements/demo/McdcDemo.java`

```java
package io.github.rvdomingos.mcdc.requirements.demo;

import io.github.rvdomingos.mcdc.core.IndependencePair;
import io.github.rvdomingos.mcdc.core.IndependencePairs;
import io.github.rvdomingos.mcdc.core.MinimalSuite;
import io.github.rvdomingos.mcdc.core.TestVector;
import io.github.rvdomingos.mcdc.core.TruthTable;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.requirements.ExpressionParser;
import java.util.List;
import java.util.Map;

public class McdcDemo {

    public static void main(String[] args) {
        String text = args.length > 0 ? String.join(" ", args) : "(A and B) or C";
        Expr expr;
        try {
            expr = ExpressionParser.parse(text);
        } catch (IllegalArgumentException e) {
            System.err.println("Expressão inválida: " + e.getMessage());
            System.exit(1);
            return;
        }

        TruthTable table = TruthTable.of(expr);
        System.out.println("Decisão: " + text);
        System.out.println();
        System.out.print(table.format());

        Map<String, List<IndependencePair>> pairs = IndependencePairs.uniqueCause(table);
        System.out.println();
        System.out.println("Pares de independência (causa única):");
        pairs.forEach((condition, list) ->
                System.out.println("  " + condition + ": " + (list.isEmpty() ? "nenhum par" : list)));

        List<TestVector> suite = MinimalSuite.greedy(pairs);
        System.out.println();
        System.out.println("Suíte mínima (" + suite.size() + " testes):");
        for (TestVector vector : suite) {
            System.out.println("  " + vector.name() + "  " + vector.bits() + "  -> " + (vector.outcome() ? "T" : "F"));
        }
    }
}
```

`mvn verify`: 17 testes. Agora dá para testar qualquer expressão:

```bash
mvn -q compile
CP=mcdc-core/target/classes:mcdc-requirements/target/classes
"$JAVA_HOME/bin/java" -cp $CP io.github.rvdomingos.mcdc.requirements.demo.McdcDemo "A and not B"
"$JAVA_HOME/bin/java" -cp $CP io.github.rvdomingos.mcdc.requirements.demo.McdcDemo "A or (A and B)"
"$JAVA_HOME/bin/java" -cp $CP io.github.rvdomingos.mcdc.requirements.demo.McdcDemo "(F1 && F2) || F3"
```

Sempre ponha a expressão entre aspas, senão o terminal interpreta `(`, `&` e `|`. No Eclipse, o argumento vai em Run → Run Configurations → McdcDemo → Arguments.

Repare que `A or (A and B)` mostra "B: nenhum par".

---

## Passo 7: mascaramento

A causa única é rígida: exige que só a condição analisada mude. O **mascaramento** (aceito na DO-178C) permite que outras condições mudem, desde que elas não influenciem o resultado naquele vetor, ou seja, estejam "mascaradas".

### A ideia: a condição decide o resultado?

Em um vetor, a condição **decide** o resultado se invertê-la sozinha inverte o resultado. No código, isso é comparar a linha com a linha gêmea `row ^ mask` (o `^` troca o bit, seja qual for o valor).

Um par de mascaramento para a condição X é:

- um vetor com X = T e outro com X = F;
- resultados diferentes;
- X decide o resultado **nos dois** vetores.

Exemplo em `(A and B) or C`: V7 (FFT) e V4 (TFF). Muda A e muda C. Mas `(A and B)` é falso nos dois, então A não influencia nada: está mascarada. O par vale para C em mascaramento, e não em causa única.

Todo par de causa única também é par de mascaramento; o contrário não. Um dos testes confere isso.

Para escolher a variante, o método `of(table, variant)` usa um `switch` sobre o enum `McdcVariant` que já existe no projeto.

**Teste** (substitui o arquivo inteiro; os dois últimos testes são novos):

**Arquivo:** `mcdc-core/src/test/java/io/github/rvdomingos/mcdc/core/IndependencePairsTest.java`

```java
package io.github.rvdomingos.mcdc.core;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

class IndependencePairsTest {

    // (A and B) or C
    private final Expr andOr = new Or(new And(new Cond("A"), new Cond("B")), new Cond("C"));

    @Test
    void findsPairsForAndOr() {
        Map<String, List<IndependencePair>> pairs = IndependencePairs.uniqueCause(TruthTable.of(andOr));

        assertEquals("[(V2, V6)]", pairs.get("A").toString());
        assertEquals("[(V2, V4)]", pairs.get("B").toString());
        assertEquals("[(V3, V4), (V5, V6), (V7, V8)]", pairs.get("C").toString());
    }

    @Test
    void findsPairsWithNegation() {
        // A and not B
        Expr expr = new And(new Cond("A"), new Not(new Cond("B")));
        Map<String, List<IndependencePair>> pairs = IndependencePairs.uniqueCause(TruthTable.of(expr));

        assertEquals("[(V2, V4)]", pairs.get("A").toString());
        assertEquals("[(V1, V2)]", pairs.get("B").toString());
    }

    @Test
    void conditionWithoutEffectHasNoPair() {
        // A or (A and B): B nunca muda o resultado sozinha
        Expr expr = new Or(new Cond("A"), new And(new Cond("A"), new Cond("B")));
        Map<String, List<IndependencePair>> pairs = IndependencePairs.uniqueCause(TruthTable.of(expr));

        assertEquals(List.of(), pairs.get("B"));
    }

    @Test
    void maskingAcceptsPairsWhereMaskedConditionsChange() {
        Map<String, List<IndependencePair>> pairs = IndependencePairs.masking(TruthTable.of(andOr));

        assertEquals("[(V2, V6)]", pairs.get("A").toString());
        assertEquals("[(V2, V4)]", pairs.get("B").toString());
        // V7 (FFT) e V4 (TFF): A também muda, mas (A and B) é falso nos dois, então A está mascarada
        assertEquals(9, pairs.get("C").size());
        assertTrue(pairs.get("C").toString().contains("(V7, V4)"));
    }

    @Test
    void everyUniqueCausePairIsAlsoAMaskingPair() {
        List<Expr> expressions = List.of(
                andOr,
                new And(new Cond("A"), new Not(new Cond("B"))),
                new Or(new And(new Cond("A"), new Cond("B")), new And(new Not(new Cond("A")), new Cond("C"))));

        for (Expr expr : expressions) {
            TruthTable table = TruthTable.of(expr);
            Map<String, List<IndependencePair>> unique = IndependencePairs.uniqueCause(table);
            Map<String, List<IndependencePair>> masking = IndependencePairs.masking(table);
            for (String condition : table.conditions()) {
                assertTrue(masking.get(condition).containsAll(unique.get(condition)), condition);
            }
        }
    }
}
```

**Código** (substitui o arquivo inteiro; entram `of`, `masking` e `decides`):

**Arquivo:** `mcdc-core/src/main/java/io/github/rvdomingos/mcdc/core/IndependencePairs.java`

```java
package io.github.rvdomingos.mcdc.core;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class IndependencePairs {

    private IndependencePairs() {
    }

    /** Pares da variante pedida. */
    public static Map<String, List<IndependencePair>> of(TruthTable table, McdcVariant variant) {
        return switch (variant) {
            case UNIQUE_CAUSE -> uniqueCause(table);
            case MASKING -> masking(table);
        };
    }

    /**
     * Pares de causa única: só a condição analisada muda entre os dois vetores, e o resultado muda.
     * O mapa segue a ordem das condições; condição sem par fica com lista vazia.
     */
    public static Map<String, List<IndependencePair>> uniqueCause(TruthTable table) {
        List<String> conditions = table.conditions();
        int n = conditions.size();
        Map<String, List<IndependencePair>> result = new LinkedHashMap<>();

        for (int i = 0; i < n; i++) {
            int mask = TruthTable.bit(n, i);
            List<IndependencePair> pairs = new ArrayList<>();
            for (TestVector row : table.rows()) {
                if ((row.index() & mask) != 0) {
                    continue; // só parte das linhas em que a condição é verdadeira
                }
                TestVector flipped = table.rows().get(row.index() | mask);
                if (row.outcome() != flipped.outcome()) {
                    pairs.add(new IndependencePair(conditions.get(i), row, flipped));
                }
            }
            result.put(conditions.get(i), List.copyOf(pairs));
        }
        return result;
    }

    /**
     * Pares de mascaramento: a condição muda, o resultado muda, e nos dois vetores a condição
     * decide o resultado sozinha. As outras condições podem mudar, desde que estejam mascaradas.
     */
    public static Map<String, List<IndependencePair>> masking(TruthTable table) {
        List<String> conditions = table.conditions();
        int n = conditions.size();
        Map<String, List<IndependencePair>> result = new LinkedHashMap<>();

        for (int i = 0; i < n; i++) {
            int mask = TruthTable.bit(n, i);
            List<TestVector> whenTrue = new ArrayList<>();
            List<TestVector> whenFalse = new ArrayList<>();
            for (TestVector row : table.rows()) {
                if (!decides(table, row, mask)) {
                    continue;
                }
                if ((row.index() & mask) == 0) {
                    whenTrue.add(row);
                } else {
                    whenFalse.add(row);
                }
            }

            List<IndependencePair> pairs = new ArrayList<>();
            for (TestVector t : whenTrue) {
                for (TestVector f : whenFalse) {
                    if (t.outcome() != f.outcome()) {
                        pairs.add(new IndependencePair(conditions.get(i), t, f));
                    }
                }
            }
            result.put(conditions.get(i), List.copyOf(pairs));
        }
        return result;
    }

    /** A condição decide o resultado nesta linha: invertê-la sozinha inverte o resultado. */
    private static boolean decides(TruthTable table, TestVector row, int mask) {
        return row.outcome() != table.rows().get(row.index() ^ mask).outcome();
    }
}
```

**Demo** (substitui a anterior; mostra as duas variantes):

**Arquivo:** `mcdc-requirements/src/main/java/io/github/rvdomingos/mcdc/requirements/demo/McdcDemo.java`

```java
package io.github.rvdomingos.mcdc.requirements.demo;

import io.github.rvdomingos.mcdc.core.IndependencePair;
import io.github.rvdomingos.mcdc.core.IndependencePairs;
import io.github.rvdomingos.mcdc.core.McdcVariant;
import io.github.rvdomingos.mcdc.core.MinimalSuite;
import io.github.rvdomingos.mcdc.core.TestVector;
import io.github.rvdomingos.mcdc.core.TruthTable;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.requirements.ExpressionParser;
import java.util.List;
import java.util.Map;

public class McdcDemo {

    public static void main(String[] args) {
        String text = args.length > 0 ? String.join(" ", args) : "(A and B) or C";
        Expr expr;
        try {
            expr = ExpressionParser.parse(text);
        } catch (IllegalArgumentException e) {
            System.err.println("Expressão inválida: " + e.getMessage());
            System.exit(1);
            return;
        }

        TruthTable table = TruthTable.of(expr);
        System.out.println("Decisão: " + text);
        System.out.println();
        System.out.print(table.format());

        Map<String, List<IndependencePair>> uniqueCause = IndependencePairs.of(table, McdcVariant.UNIQUE_CAUSE);
        Map<String, List<IndependencePair>> masking = IndependencePairs.of(table, McdcVariant.MASKING);
        printPairs("Pares de independência (causa única):", uniqueCause);
        printPairs("Pares de independência (mascaramento):", masking);

        List<TestVector> suite = MinimalSuite.greedy(masking);
        System.out.println();
        System.out.println("Suíte mínima, mascaramento (" + suite.size() + " testes):");
        for (TestVector vector : suite) {
            System.out.println("  " + vector.name() + "  " + vector.bits() + "  -> " + (vector.outcome() ? "T" : "F"));
        }
    }

    private static void printPairs(String title, Map<String, List<IndependencePair>> pairs) {
        System.out.println();
        System.out.println(title);
        pairs.forEach((condition, list) ->
                System.out.println("  " + condition + ": " + (list.isEmpty() ? "nenhum par" : list)));
    }
}
```

`mvn verify`: 19 testes. Na demo, compare as duas listas:

```
Pares de independência (causa única):
  A: [(V2, V6)]
  B: [(V2, V4)]
  C: [(V3, V4), (V5, V6), (V7, V8)]

Pares de independência (mascaramento):
  A: [(V2, V6)]
  B: [(V2, V4)]
  C: [(V3, V4), (V3, V6), (V3, V8), (V5, V4), (V5, V6), (V5, V8), (V7, V4), (V7, V6), (V7, V8)]
```

Mais pares significam mais liberdade para a suíte mínima. Isso faz diferença quando há linhas impossíveis, que é o próximo passo.

---

## Passo 8: linhas impossíveis

Condições de um requisito podem depender uma da outra. Se A = `speed > 100` e B = `speed > 50`, nenhuma linha pode ter A verdadeira e B falsa.

Por enquanto essa dependência é informada à mão, como uma **restrição**: uma expressão que toda linha possível satisfaz. Aqui, `not A or B` ("se A, então B"). Mais tarde o Z3 vai descobrir isso sozinho a partir dos predicados.

### A ideia: marcar, não apagar

As linhas impossíveis continuam na tabela, só marcadas com `feasible = false`. Assim o número de cada linha continua igual à posição dela na lista, e a busca da linha gêmea com `rows().get(...)` segue funcionando. O relatório também consegue mostrar quais linhas foram descartadas.

Mudanças:

- `TestVector` ganha o campo `feasible`.
- `TruthTable.of(expr, constraint)` avalia a restrição em cada linha. O `of(expr)` antigo continua existindo, sem restrição.
- `IndependencePairs` ignora linhas impossíveis nos pares.

Em mascaramento, "a condição decide o resultado" continua sendo calculado pela fórmula, mesmo quando a linha gêmea é impossível: é uma pergunta sobre a lógica da expressão, não sobre o mundo.

**Testes** (substituem os arquivos inteiros; os testes novos são os últimos de cada arquivo):

**Arquivo:** `mcdc-core/src/test/java/io/github/rvdomingos/mcdc/core/TruthTableTest.java`

```java
package io.github.rvdomingos.mcdc.core;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import java.util.stream.Collectors;
import org.junit.jupiter.api.Test;

class TruthTableTest {

    // (A and B) or C
    private final Expr decision = new Or(new And(new Cond("A"), new Cond("B")), new Cond("C"));

    @Test
    void hasOneRowPerCombination() {
        TruthTable table = TruthTable.of(decision);
        assertEquals(8, table.rows().size());
    }

    @Test
    void firstRowIsAllTrueAndLastIsAllFalse() {
        TruthTable table = TruthTable.of(decision);
        assertEquals("TTT", table.rows().get(0).bits());
        assertEquals("FFF", table.rows().get(7).bits());
    }

    @Test
    void computesOutcomeOfEachRow() {
        TruthTable table = TruthTable.of(decision);
        String outcomes = table.rows().stream()
                .map(row -> row.outcome() ? "T" : "F")
                .collect(Collectors.joining());
        assertEquals("TTTFTFTF", outcomes);
    }

    @Test
    void rejectsTooManyConditions() {
        Expr expr = new Cond("C0");
        for (int i = 1; i <= TruthTable.MAX_CONDITIONS; i++) {
            expr = new Or(expr, new Cond("C" + i));
        }
        Expr tooBig = expr;
        assertThrows(IllegalArgumentException.class, () -> TruthTable.of(tooBig));
    }

    @Test
    void marksRowsThatViolateTheConstraint() {
        // not A or B: A verdadeira exige B verdadeira, então TFT e TFF são impossíveis
        TruthTable table = TruthTable.of(decision, new Or(new Not(new Cond("A")), new Cond("B")));
        String feasible = table.rows().stream()
                .map(row -> row.feasible() ? "1" : "0")
                .collect(Collectors.joining());
        assertEquals("11001111", feasible);
    }

    @Test
    void rejectsConstraintWithUnknownCondition() {
        assertThrows(IllegalArgumentException.class, () -> TruthTable.of(decision, new Cond("Z")));
    }
}
```

**Arquivo:** `mcdc-core/src/test/java/io/github/rvdomingos/mcdc/core/IndependencePairsTest.java`

```java
package io.github.rvdomingos.mcdc.core;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

class IndependencePairsTest {

    // (A and B) or C
    private final Expr andOr = new Or(new And(new Cond("A"), new Cond("B")), new Cond("C"));

    @Test
    void findsPairsForAndOr() {
        Map<String, List<IndependencePair>> pairs = IndependencePairs.uniqueCause(TruthTable.of(andOr));

        assertEquals("[(V2, V6)]", pairs.get("A").toString());
        assertEquals("[(V2, V4)]", pairs.get("B").toString());
        assertEquals("[(V3, V4), (V5, V6), (V7, V8)]", pairs.get("C").toString());
    }

    @Test
    void findsPairsWithNegation() {
        // A and not B
        Expr expr = new And(new Cond("A"), new Not(new Cond("B")));
        Map<String, List<IndependencePair>> pairs = IndependencePairs.uniqueCause(TruthTable.of(expr));

        assertEquals("[(V2, V4)]", pairs.get("A").toString());
        assertEquals("[(V1, V2)]", pairs.get("B").toString());
    }

    @Test
    void conditionWithoutEffectHasNoPair() {
        // A or (A and B): B nunca muda o resultado sozinha
        Expr expr = new Or(new Cond("A"), new And(new Cond("A"), new Cond("B")));
        Map<String, List<IndependencePair>> pairs = IndependencePairs.uniqueCause(TruthTable.of(expr));

        assertEquals(List.of(), pairs.get("B"));
    }

    @Test
    void maskingAcceptsPairsWhereMaskedConditionsChange() {
        Map<String, List<IndependencePair>> pairs = IndependencePairs.masking(TruthTable.of(andOr));

        assertEquals("[(V2, V6)]", pairs.get("A").toString());
        assertEquals("[(V2, V4)]", pairs.get("B").toString());
        // V7 (FFT) e V4 (TFF): A também muda, mas (A and B) é falso nos dois, então A está mascarada
        assertEquals(9, pairs.get("C").size());
        assertTrue(pairs.get("C").toString().contains("(V7, V4)"));
    }

    @Test
    void everyUniqueCausePairIsAlsoAMaskingPair() {
        List<Expr> expressions = List.of(
                andOr,
                new And(new Cond("A"), new Not(new Cond("B"))),
                new Or(new And(new Cond("A"), new Cond("B")), new And(new Not(new Cond("A")), new Cond("C"))));

        for (Expr expr : expressions) {
            TruthTable table = TruthTable.of(expr);
            Map<String, List<IndependencePair>> unique = IndependencePairs.uniqueCause(table);
            Map<String, List<IndependencePair>> masking = IndependencePairs.masking(table);
            for (String condition : table.conditions()) {
                assertTrue(masking.get(condition).containsAll(unique.get(condition)), condition);
            }
        }
    }

    @Test
    void ignoresImpossibleRows() {
        // A or (B and C), com A = speed > 100 e B = speed > 50: A verdadeira exige B verdadeira
        Expr expr = new Or(new Cond("A"), new And(new Cond("B"), new Cond("C")));
        Expr constraint = new Or(new Not(new Cond("A")), new Cond("B"));
        TruthTable table = TruthTable.of(expr, constraint);

        Map<String, List<IndependencePair>> unique = IndependencePairs.uniqueCause(table);
        assertEquals("[(V2, V6)]", unique.get("A").toString());
        assertEquals("[(V5, V7)]", unique.get("B").toString());
        assertEquals("[(V5, V6)]", unique.get("C").toString());

        Map<String, List<IndependencePair>> masking = IndependencePairs.masking(table);
        assertEquals("[(V2, V6), (V2, V7), (V2, V8)]", masking.get("A").toString());
    }
}
```

**Código** (substituem os arquivos inteiros):

**Arquivo:** `mcdc-core/src/main/java/io/github/rvdomingos/mcdc/core/TestVector.java`

```java
package io.github.rvdomingos.mcdc.core;

import java.util.Map;
import java.util.stream.Collectors;

/**
 * Uma linha da tabela verdade.
 *
 * @param index    posição na tabela, começando em 0
 * @param values   valor de cada condição, na ordem das condições da decisão
 * @param outcome  resultado da decisão para esses valores
 * @param feasible se a combinação é possível; linhas impossíveis não entram em pares
 */
public record TestVector(int index, Map<String, Boolean> values, boolean outcome, boolean feasible) {

    /** Nome usado nos relatórios: V1, V2, ... */
    public String name() {
        return "V" + (index + 1);
    }

    /** Valores das condições como texto, ex.: "TTF". */
    public String bits() {
        return values.values().stream()
                .map(value -> value ? "T" : "F")
                .collect(Collectors.joining());
    }
}
```

**Arquivo:** `mcdc-core/src/main/java/io/github/rvdomingos/mcdc/core/TruthTable.java`

```java
package io.github.rvdomingos.mcdc.core;

import io.github.rvdomingos.mcdc.core.model.Expr;
import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Tabela verdade completa de uma expressão. A linha 0 tem todas as condições verdadeiras. */
public record TruthTable(List<String> conditions, List<TestVector> rows) {

    public static final int MAX_CONDITIONS = 20;

    public static TruthTable of(Expr expr) {
        return of(expr, null);
    }

    /**
     * @param constraint expressão que toda linha possível satisfaz, sobre as mesmas condições
     *                   da decisão; null quando não há restrição
     */
    public static TruthTable of(Expr expr, Expr constraint) {
        List<String> conditions = expr.conditions();
        int n = conditions.size();
        if (n > MAX_CONDITIONS) {
            throw new IllegalArgumentException(
                    "Decisão com " + n + " condições; o limite é " + MAX_CONDITIONS);
        }
        if (constraint != null) {
            for (String id : constraint.conditions()) {
                if (!conditions.contains(id)) {
                    throw new IllegalArgumentException("A restrição usa uma condição que não está na decisão: " + id);
                }
            }
        }

        List<TestVector> rows = new ArrayList<>();
        for (int row = 0; row < (1 << n); row++) {
            Map<String, Boolean> values = new LinkedHashMap<>();
            for (int i = 0; i < n; i++) {
                values.put(conditions.get(i), (row & bit(n, i)) == 0);
            }
            boolean feasible = constraint == null || constraint.eval(values);
            rows.add(new TestVector(row, Collections.unmodifiableMap(values), expr.eval(values), feasible));
        }
        return new TruthTable(conditions, List.copyOf(rows));
    }

    /** Máscara do bit da condição i. A primeira condição é o bit mais significativo. */
    static int bit(int n, int i) {
        return 1 << (n - 1 - i);
    }

    public String format() {
        var sb = new StringBuilder();
        sb.append(String.format("%-6s", "Vetor"));
        for (String condition : conditions) {
            sb.append(column(condition, condition));
        }
        sb.append("| D\n");
        for (TestVector row : rows) {
            sb.append(String.format("%-6s", row.name()));
            for (String condition : conditions) {
                sb.append(column(row.values().get(condition) ? "T" : "F", condition));
            }
            sb.append("| ").append(row.outcome() ? "T" : "F");
            if (!row.feasible()) {
                sb.append("  (impossível)");
            }
            sb.append('\n');
        }
        return sb.toString();
    }

    /** Alinha o texto na largura da coluna, que acompanha o tamanho do nome da condição. */
    private static String column(String text, String condition) {
        return String.format("%-" + (condition.length() + 3) + "s", text);
    }
}
```

**Arquivo:** `mcdc-core/src/main/java/io/github/rvdomingos/mcdc/core/IndependencePairs.java`

```java
package io.github.rvdomingos.mcdc.core;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class IndependencePairs {

    private IndependencePairs() {
    }

    /** Pares da variante pedida. */
    public static Map<String, List<IndependencePair>> of(TruthTable table, McdcVariant variant) {
        return switch (variant) {
            case UNIQUE_CAUSE -> uniqueCause(table);
            case MASKING -> masking(table);
        };
    }

    /**
     * Pares de causa única: só a condição analisada muda entre os dois vetores, e o resultado muda.
     * Linhas impossíveis ficam de fora. O mapa segue a ordem das condições; condição sem par fica
     * com lista vazia.
     */
    public static Map<String, List<IndependencePair>> uniqueCause(TruthTable table) {
        List<String> conditions = table.conditions();
        int n = conditions.size();
        Map<String, List<IndependencePair>> result = new LinkedHashMap<>();

        for (int i = 0; i < n; i++) {
            int mask = TruthTable.bit(n, i);
            List<IndependencePair> pairs = new ArrayList<>();
            for (TestVector row : table.rows()) {
                if (!row.feasible() || (row.index() & mask) != 0) {
                    continue; // só parte das linhas possíveis em que a condição é verdadeira
                }
                TestVector flipped = table.rows().get(row.index() | mask);
                if (flipped.feasible() && row.outcome() != flipped.outcome()) {
                    pairs.add(new IndependencePair(conditions.get(i), row, flipped));
                }
            }
            result.put(conditions.get(i), List.copyOf(pairs));
        }
        return result;
    }

    /**
     * Pares de mascaramento: a condição muda, o resultado muda, e nos dois vetores a condição
     * decide o resultado sozinha. As outras condições podem mudar, desde que estejam mascaradas.
     * Linhas impossíveis ficam de fora.
     */
    public static Map<String, List<IndependencePair>> masking(TruthTable table) {
        List<String> conditions = table.conditions();
        int n = conditions.size();
        Map<String, List<IndependencePair>> result = new LinkedHashMap<>();

        for (int i = 0; i < n; i++) {
            int mask = TruthTable.bit(n, i);
            List<TestVector> whenTrue = new ArrayList<>();
            List<TestVector> whenFalse = new ArrayList<>();
            for (TestVector row : table.rows()) {
                if (!row.feasible() || !decides(table, row, mask)) {
                    continue;
                }
                if ((row.index() & mask) == 0) {
                    whenTrue.add(row);
                } else {
                    whenFalse.add(row);
                }
            }

            List<IndependencePair> pairs = new ArrayList<>();
            for (TestVector t : whenTrue) {
                for (TestVector f : whenFalse) {
                    if (t.outcome() != f.outcome()) {
                        pairs.add(new IndependencePair(conditions.get(i), t, f));
                    }
                }
            }
            result.put(conditions.get(i), List.copyOf(pairs));
        }
        return result;
    }

    /**
     * A condição decide o resultado nesta linha: invertê-la sozinha inverte o resultado.
     * É uma propriedade da fórmula, então vale mesmo que a linha invertida seja impossível.
     */
    private static boolean decides(TruthTable table, TestVector row, int mask) {
        return row.outcome() != table.rows().get(row.index() ^ mask).outcome();
    }
}
```

`mvn verify`: 22 testes. A demo continua igual; as restrições aparecem no terminal no passo 10.

---

## Passo 9: fachada do motor

Até aqui a demo monta tabela, pares e suíte na mão. A fachada junta tudo numa chamada, que é a API que outras ferramentas (e o futuro plugin) vão usar:

```java
McdcReport report = Mcdc.analyze(expr, McdcOptions.defaults());
```

- `McdcOptions`: variante e restrição. O padrão é mascaramento, sem restrição. Os métodos `withVariant` e `withConstraint` devolvem uma cópia alterada, já que records são imutáveis.
- `McdcReport`: tudo o que a análise produziu, mais `uncoveredConditions()` e `isComplete()`.
- `Mcdc.analyze`: encadeia os passos 2, 4/7 e 5.

**Teste** (novo):

**Arquivo:** `mcdc-core/src/test/java/io/github/rvdomingos/mcdc/core/McdcTest.java`

```java
package io.github.rvdomingos.mcdc.core;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import java.util.List;
import java.util.stream.Collectors;
import org.junit.jupiter.api.Test;

class McdcTest {

    @Test
    void analyzesWithDefaults() {
        // (A and B) or C
        Expr expr = new Or(new And(new Cond("A"), new Cond("B")), new Cond("C"));
        McdcReport report = Mcdc.analyze(expr, McdcOptions.defaults());

        assertEquals(McdcVariant.MASKING, report.options().variant());
        assertEquals(4, report.minimalSuite().size());
        assertTrue(report.isComplete());
    }

    @Test
    void reportsRedundantCondition() {
        // A or (A and B)
        Expr expr = new Or(new Cond("A"), new And(new Cond("A"), new Cond("B")));
        McdcReport report = Mcdc.analyze(expr, McdcOptions.defaults());

        assertEquals(List.of("B"), report.uncoveredConditions());
        assertFalse(report.isComplete());
    }

    @Test
    void appliesConstraintAndVariant() {
        // A or (B and C), com restrição not A or B
        Expr expr = new Or(new Cond("A"), new And(new Cond("B"), new Cond("C")));
        McdcOptions options = McdcOptions.defaults()
                .withVariant(McdcVariant.UNIQUE_CAUSE)
                .withConstraint(new Or(new Not(new Cond("A")), new Cond("B")));

        McdcReport report = Mcdc.analyze(expr, options);
        String suite = report.minimalSuite().stream().map(TestVector::name).collect(Collectors.joining(", "));
        assertEquals("V2, V5, V6, V7", suite);
    }
}
```

**Código** (novos):

**Arquivo:** `mcdc-core/src/main/java/io/github/rvdomingos/mcdc/core/McdcOptions.java`

```java
package io.github.rvdomingos.mcdc.core;

import io.github.rvdomingos.mcdc.core.model.Expr;

/**
 * Opções da análise.
 *
 * @param variant    variante de MC/DC
 * @param constraint restrição entre as condições; null quando não há
 */
public record McdcOptions(McdcVariant variant, Expr constraint) {

    /** Mascaramento e sem restrição. */
    public static McdcOptions defaults() {
        return new McdcOptions(McdcVariant.MASKING, null);
    }

    public McdcOptions withVariant(McdcVariant variant) {
        return new McdcOptions(variant, constraint);
    }

    public McdcOptions withConstraint(Expr constraint) {
        return new McdcOptions(variant, constraint);
    }
}
```

**Arquivo:** `mcdc-core/src/main/java/io/github/rvdomingos/mcdc/core/McdcReport.java`

```java
package io.github.rvdomingos.mcdc.core;

import io.github.rvdomingos.mcdc.core.model.Expr;
import java.util.List;
import java.util.Map;

/** Resultado completo de uma análise MC/DC. */
public record McdcReport(
        Expr expression,
        McdcOptions options,
        TruthTable table,
        Map<String, List<IndependencePair>> pairs,
        List<TestVector> minimalSuite) {

    /** Condições sem nenhum par: não há como demonstrar o efeito delas. */
    public List<String> uncoveredConditions() {
        return pairs.entrySet().stream()
                .filter(entry -> entry.getValue().isEmpty())
                .map(Map.Entry::getKey)
                .toList();
    }

    public boolean isComplete() {
        return uncoveredConditions().isEmpty();
    }
}
```

**Arquivo:** `mcdc-core/src/main/java/io/github/rvdomingos/mcdc/core/Mcdc.java`

```java
package io.github.rvdomingos.mcdc.core;

import io.github.rvdomingos.mcdc.core.model.Expr;
import java.util.List;
import java.util.Map;

/** Ponto de entrada do motor. */
public final class Mcdc {

    private Mcdc() {
    }

    public static McdcReport analyze(Expr expression, McdcOptions options) {
        TruthTable table = TruthTable.of(expression, options.constraint());
        Map<String, List<IndependencePair>> pairs = IndependencePairs.of(table, options.variant());
        List<TestVector> suite = MinimalSuite.greedy(pairs);
        return new McdcReport(expression, options, table, pairs, suite);
    }
}
```

`mvn verify`: 25 testes.

---

## Passo 10: o comando `mcdc`

Um módulo novo, `mcdc-cli`, com o comando de terminal. Ele depende de `mcdc-requirements` (o parser), que por sua vez depende de `mcdc-core`.

```
mcdc analyze "<expressão>" [--unique-cause] [--constraint "<expressão>"]
mcdc analyze -f <arquivo> [--unique-cause]
```

Códigos de saída, para uso em scripts e CI:

| Código | Significado |
|---|---|
| 0 | Toda condição tem par de independência. |
| 1 | Erro de entrada. |
| 2 | Alguma condição ficou sem par. |

O `main` só chama `run(args)` e repassa o código para `System.exit`. Assim os testes chamam `run` direto, sem encerrar a JVM.

### Registrar o módulo

No `pom.xml` da raiz, acrescente a linha do `mcdc-cli` na lista de módulos:

```xml
  <modules>
    <module>mcdc-core</module>
    <module>mcdc-requirements</module>
    <module>mcdc-cli</module>
  </modules>
```

### Arquivos do módulo

Crie a pasta `mcdc-cli` na raiz do projeto, ao lado de `mcdc-core`.

**pom do módulo** (novo):

**Arquivo:** `mcdc-cli/pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <parent>
    <groupId>io.github.rvdomingos.mcdc</groupId>
    <artifactId>mcdc-parent</artifactId>
    <version>0.1.0-SNAPSHOT</version>
  </parent>

  <artifactId>mcdc-cli</artifactId>
  <name>MC/DC Command Line</name>

  <dependencies>
    <dependency>
      <groupId>io.github.rvdomingos.mcdc</groupId>
      <artifactId>mcdc-requirements</artifactId>
      <version>${project.version}</version>
    </dependency>
  </dependencies>
</project>
```

**Teste** (novo):

**Arquivo:** `mcdc-cli/src/test/java/io/github/rvdomingos/mcdc/cli/MainTest.java`

```java
package io.github.rvdomingos.mcdc.cli;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class MainTest {

    @Test
    void completeCoverageReturnsZero() {
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "(A and B) or C"}));
    }

    @Test
    void redundantConditionReturnsTwo() {
        assertEquals(Main.UNCOVERED, Main.run(new String[] {"analyze", "A or (A and B)"}));
    }

    @Test
    void invalidInputReturnsOne() {
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {}));
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "A and"}));
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "A", "--constraint"}));
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "A", "--constraint", "Z"}));
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "A", "--foo"}));
    }

    @Test
    void readsRequirementsFile(@TempDir Path dir) throws IOException {
        Path file = dir.resolve("requisitos.mcdc");
        Files.writeString(file, "# comentário\nREQ-1: A and B\n\nREQ-2: A or not B\n");
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "-f", file.toString()}));
    }
}
```

**Código** (novos):

**Arquivo:** `mcdc-cli/src/main/java/io/github/rvdomingos/mcdc/cli/Main.java`

```java
package io.github.rvdomingos.mcdc.cli;

import io.github.rvdomingos.mcdc.core.Mcdc;
import io.github.rvdomingos.mcdc.core.McdcOptions;
import io.github.rvdomingos.mcdc.core.McdcReport;
import io.github.rvdomingos.mcdc.core.McdcVariant;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.requirements.ExpressionParser;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/** Comando {@code mcdc}. */
public final class Main {

    static final int OK = 0;
    static final int INPUT_ERROR = 1;
    static final int UNCOVERED = 2;

    private static final String USAGE = """
            Uso:
              mcdc analyze "<expressão>" [--unique-cause] [--constraint "<expressão>"]
              mcdc analyze -f <arquivo> [--unique-cause]

            Exemplos:
              mcdc analyze "(A and B) or C"
              mcdc analyze "A or (B and C)" --constraint "not A or B"
              mcdc analyze -f exemplos/requisitos.mcdc
            """;

    private record Requirement(String id, String text) {
    }

    private Main() {
    }

    public static void main(String[] args) {
        System.exit(run(args));
    }

    static int run(String[] args) {
        if (args.length == 0 || !args[0].equals("analyze")) {
            System.err.print(USAGE);
            return INPUT_ERROR;
        }

        try {
            String expression = null;
            String file = null;
            String constraint = null;
            McdcVariant variant = McdcVariant.MASKING;

            for (int i = 1; i < args.length; i++) {
                switch (args[i]) {
                    case "--unique-cause" -> variant = McdcVariant.UNIQUE_CAUSE;
                    case "--constraint" -> {
                        constraint = valueAfter(args, i);
                        i++;
                    }
                    case "-f" -> {
                        file = valueAfter(args, i);
                        i++;
                    }
                    default -> {
                        if (args[i].startsWith("-")) {
                            throw new IllegalArgumentException("Opção desconhecida: " + args[i]);
                        }
                        expression = args[i];
                    }
                }
            }

            if ((expression == null) == (file == null)) {
                throw new IllegalArgumentException("Informe uma expressão ou um arquivo com -f.");
            }
            if (file != null && constraint != null) {
                throw new IllegalArgumentException("--constraint só vale com uma expressão direta.");
            }

            List<Requirement> requirements = file != null
                    ? readFile(Path.of(file))
                    : List.of(new Requirement("REQ", expression));
            McdcOptions options = McdcOptions.defaults()
                    .withVariant(variant)
                    .withConstraint(constraint == null ? null : ExpressionParser.parse(constraint));

            int exit = OK;
            for (Requirement requirement : requirements) {
                Expr expr;
                try {
                    expr = ExpressionParser.parse(requirement.text());
                } catch (IllegalArgumentException e) {
                    throw new IllegalArgumentException(requirement.id() + ": " + e.getMessage());
                }
                McdcReport report = Mcdc.analyze(expr, options);
                System.out.println(TextReport.format(requirement.id(), requirement.text(), constraint, report));
                if (!report.isComplete()) {
                    exit = UNCOVERED;
                }
            }
            return exit;
        } catch (IllegalArgumentException e) {
            System.err.println("Erro: " + e.getMessage());
            return INPUT_ERROR;
        } catch (IOException e) {
            System.err.println("Erro ao ler o arquivo: " + e.getMessage());
            return INPUT_ERROR;
        }
    }

    private static String valueAfter(String[] args, int i) {
        if (i + 1 >= args.length) {
            throw new IllegalArgumentException("Faltou o valor de " + args[i]);
        }
        return args[i + 1];
    }

    /** Um requisito por linha, no formato "ID: expressão". Linhas vazias e começando com # são ignoradas. */
    private static List<Requirement> readFile(Path path) throws IOException {
        List<Requirement> requirements = new ArrayList<>();
        List<String> lines = Files.readAllLines(path);
        for (int i = 0; i < lines.size(); i++) {
            String line = lines.get(i).strip();
            if (line.isEmpty() || line.startsWith("#")) {
                continue;
            }
            int colon = line.indexOf(':');
            if (colon <= 0) {
                throw new IllegalArgumentException(
                        "Linha " + (i + 1) + " sem identificador. Formato: REQ-001: expressão");
            }
            requirements.add(new Requirement(line.substring(0, colon).strip(), line.substring(colon + 1).strip()));
        }
        if (requirements.isEmpty()) {
            throw new IllegalArgumentException("Nenhum requisito em " + path);
        }
        return requirements;
    }
}
```

**Arquivo:** `mcdc-cli/src/main/java/io/github/rvdomingos/mcdc/cli/TextReport.java`

```java
package io.github.rvdomingos.mcdc.cli;

import io.github.rvdomingos.mcdc.core.IndependencePair;
import io.github.rvdomingos.mcdc.core.McdcReport;
import io.github.rvdomingos.mcdc.core.McdcVariant;
import io.github.rvdomingos.mcdc.core.TestVector;
import java.util.List;
import java.util.stream.Collectors;

/** Relatório em texto para o terminal. */
final class TextReport {

    private static final int MAX_PAIRS_SHOWN = 6;

    private TextReport() {
    }

    static String format(String id, String expression, String constraint, McdcReport report) {
        var sb = new StringBuilder();
        sb.append("Requisito: ").append(id).append('\n');
        sb.append("Decisão:   ").append(expression).append('\n');
        if (constraint != null) {
            sb.append("Restrição: ").append(constraint).append('\n');
        }
        sb.append("Variante:  ").append(variantName(report.options().variant())).append("\n\n");

        sb.append(report.table().format());

        sb.append("\nPares de independência:\n");
        report.pairs().forEach((condition, pairs) ->
                sb.append("  ").append(condition).append(": ").append(describe(pairs)).append('\n'));

        sb.append("\nSuíte mínima (").append(report.minimalSuite().size()).append(" testes):\n");
        for (TestVector vector : report.minimalSuite()) {
            sb.append("  ").append(vector.name())
                    .append("  ").append(vector.bits())
                    .append("  -> ").append(vector.outcome() ? "T" : "F")
                    .append('\n');
        }

        sb.append("\nCobertura MC/DC: ");
        if (report.isComplete()) {
            sb.append("completa\n");
        } else {
            sb.append("incompleta, sem par para ")
                    .append(String.join(", ", report.uncoveredConditions()))
                    .append('\n');
        }
        return sb.toString();
    }

    private static String describe(List<IndependencePair> pairs) {
        if (pairs.isEmpty()) {
            return "nenhum par";
        }
        String shown = pairs.stream()
                .limit(MAX_PAIRS_SHOWN)
                .map(IndependencePair::toString)
                .collect(Collectors.joining(", "));
        return pairs.size() <= MAX_PAIRS_SHOWN ? shown : shown + ", ... (" + pairs.size() + " pares)";
    }

    private static String variantName(McdcVariant variant) {
        return switch (variant) {
            case UNIQUE_CAUSE -> "causa única";
            case MASKING -> "mascaramento";
        };
    }
}
```

### Script e exemplo

**Script `mcdc`** na raiz do projeto (novo). Ele monta o classpath com as classes compiladas, para você não digitar o comando `java` inteiro:

**Arquivo:** `mcdc`

```bash
#!/usr/bin/env bash
# Roda a ferramenta a partir das classes compiladas. Compile antes com: mvn -q compile
DIR="$(cd "$(dirname "$0")" && pwd)"
JAVA="${JAVA_HOME:+$JAVA_HOME/bin/}java"
CP="$DIR/mcdc-core/target/classes:$DIR/mcdc-requirements/target/classes:$DIR/mcdc-cli/target/classes"
exec "$JAVA" -cp "$CP" io.github.rvdomingos.mcdc.cli.Main "$@"
```

Torne-o executável uma vez:

```bash
chmod +x mcdc
```

**Arquivo de requisitos de exemplo** (novo), um requisito por linha:

**Arquivo:** `exemplos/requisitos.mcdc`

```text
# Um requisito por linha, no formato  ID: expressão
REQ-001: (alarme_ativo and porta_aberta) or botao_emergencia
REQ-002: porta_fechada and not obstaculo
REQ-003: freio_acionado or (freio_acionado and pedal_pressionado)
```

### Rodar

No Eclipse, importe o módulo novo: File → Import → Maven → Existing Maven Projects → pasta do projeto → marque `mcdc-cli`. Ou botão direito em `mcdc-parent` → Maven → Update Project.

No terminal:

```bash
mvn verify            # 29 testes
mvn -q compile
./mcdc analyze "(A and B) or C"
```

A saída é a do início deste tutorial.

**Restrição entre condições**, com causa única:

```bash
./mcdc analyze "A or (B and C)" --constraint "not A or B" --unique-cause
```

```
Requisito: REQ
Decisão:   A or (B and C)
Restrição: not A or B
Variante:  causa única

Vetor A   B   C   | D
V1    T   T   T   | T
V2    T   T   F   | T
V3    T   F   T   | T  (impossível)
V4    T   F   F   | T  (impossível)
V5    F   T   T   | T
V6    F   T   F   | F
V7    F   F   T   | F
V8    F   F   F   | F

Pares de independência:
  A: (V2, V6)
  B: (V5, V7)
  C: (V5, V6)

Suíte mínima (4 testes):
  V2  TTF  -> T
  V5  FTT  -> T
  V6  FTF  -> F
  V7  FFT  -> F

Cobertura MC/DC: completa
```

**Arquivo de requisitos:**

```bash
./mcdc analyze -f exemplos/requisitos.mcdc
echo $?
```

O REQ-003 tem uma condição redundante, então o relatório dele termina assim e o código de saída é 2:

```
Pares de independência:
  freio_acionado: (V1, V3), (V1, V4), (V2, V3), (V2, V4)
  pedal_pressionado: nenhum par

Suíte mínima (2 testes):
  V1  TT  -> T
  V3  FT  -> F

Cobertura MC/DC: incompleta, sem par para pedal_pressionado
```

Sem argumentos, `./mcdc` mostra o uso. Uma expressão inválida, como `./mcdc analyze "A and ("`, mostra o erro e sai com código 1.

A `McdcDemo` já cumpriu o papel e pode ser apagada; o `mcdc` faz tudo o que ela fazia.

---

## Depois deste tutorial

O motor da Fase 1 está pronto para expressões booleanas em que cada nome aparece uma vez. A ordem completa dos próximos passos está na seção 11 do documento de arquitetura; os primeiros são:

1. **Condições por ocorrência:** em `(A and B) or (not A and C)`, cada `A` é uma condição distinta e precisa do seu próprio par (seções 5 e 6.1).
2. **Rastreabilidade:** o relatório diz qual par cobre cada condição, e a suíte prefere pares de causa única (seção 6.4).
3. **Condição sem par:** separar "redundante" de "impossível" (seção 6.5).
4. **Tabela compacta**, guardando cada linha como bits.
5. **Predicados e Z3:** `speed > 100` no parser, linhas impossíveis descobertas automaticamente e valores concretos de entrada (seções 6.2 e 7).
