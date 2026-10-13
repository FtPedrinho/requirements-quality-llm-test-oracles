# Arquitetura da Fase 1: Motor MC/DC e Módulo de Requisitos

Complemento à "Especificação Técnica e Arquitetural: Ferramenta MC/DC Híbrida" (v1.0). Aquele documento continua valendo como visão do produto; este define o que ele deixa em aberto para começar a Fase 1.

Status: proposta. O formato do XML de entrada é **hipotético** até termos um arquivo real da ferramenta de origem (seção 6).

## 1. Escopo

A Fase 1 entrega uma biblioteca Java que recebe um requisito e devolve:

- a tabela verdade da decisão;
- os pares de independência de cada condição;
- a suíte mínima de testes que atinge MC/DC.

Entradas aceitas na Fase 1:

| Entrada | Situação |
|---|---|
| XML com árvore e requirement frames | Principal. Formato a confirmar. |
| Expressão textual, ex.: `(A and B) or C` | Para testes e uso sem a ferramenta de origem. |
| Frase livre em linguagem natural | Fora da Fase 1. Entra depois como mais um adaptador. |

Ficam fora: análise de código Java, instrumentação, plugin Eclipse (Fases 2 a 4 do documento de visão).

## 2. Repositórios e módulos

**Um repositório só, com módulos Maven.** Motor e API mudam juntos nesta fase, e dois repositórios obrigariam a versionar e publicar o motor a cada ajuste no contrato.

```
Tool_MCDC_Java/
├── pom.xml                  (pai)
├── mcdc-core/               motor + modelo de decisão; sem dependências externas
├── mcdc-requirements/       adaptadores de entrada: XML e expressão textual
└── docs/
```

Módulos previstos para depois, no mesmo repositório:

| Módulo | Quando | Para quê |
|---|---|---|
| `mcdc-cli` | fim da Fase 1 | Rodar por linha de comando: arquivo de entrada, relatório de saída. |
| `mcdc-rest` | quando houver integração com ferramenta que não seja Java | Serviço HTTP fino sobre o `mcdc-core`. |
| `mcdc-java` | Fases 2 e 3 | Parser de código Java e instrumentação. |

"API" aqui tem dois sentidos, e só o primeiro existe na Fase 1:

1. **API Java:** a fachada pública do `mcdc-core` (seção 4). Outra ferramenta Java integra adicionando a dependência Maven.
2. **API REST:** o módulo `mcdc-rest`, que só expõe a API Java por HTTP.

O plugin Eclipse (Fase 4) é o único candidato real a um segundo repositório, porque o build de plugin (Tycho/OSGi) é diferente do Maven comum. Ele consumiria o `mcdc-core` como dependência.

Regra de dependência: `mcdc-core` não conhece XML, ANTLR nem Eclipse. Todo o resto depende dele, nunca o contrário.

## 3. Fluxo

```
XML (árvore + frames) ──> XmlRequirementReader ──┐
                                                  ├──> Decision ──> motor MC/DC ──> McdcReport ──> JSON / CSV / Gherkin
"(A and B) or C" ──────> ExpressionParser ───────┘
```

Os adaptadores vivem em `mcdc-requirements`. O motor só enxerga `Decision`.

## 4. Modelo de decisão e API do motor

### Modelo

```java
public sealed interface Expr permits Cond, And, Or, Not { }

public record Cond(String id) implements Expr { }
public record And(Expr left, Expr right) implements Expr { }
public record Or(Expr left, Expr right) implements Expr { }
public record Not(Expr operand) implements Expr { }

public record Decision(
    String id,                       // ex.: "REQ-001"
    Expr expression,                 // antecedente do requisito
    Map<String, String> labels,      // id da condição -> texto legível, ex.: "F1" -> "velocidade > 100 km/h"
    String expectedAction            // consequente, ex.: "sistema ativa o alerta"
) { }
```

Uma condição é atômica para o motor: ele não interpreta `velocidade > 100`, só sabe que `F1` é verdadeira ou falsa. O texto vai em `labels` e serve para o relatório.

Se a mesma condição aparece duas vezes na expressão, ela usa o mesmo `id` nas duas ocorrências.

### Fachada

```java
McdcReport report = Mcdc.analyze(decision, McdcOptions.defaults());
```

```java
public record McdcOptions(
    McdcVariant variant,             // UNIQUE_CAUSE ou MASKING
    List<Expr> constraints           // restrições entre condições (seção 5.2)
) { }

public record McdcReport(
    Decision decision,
    List<TestVector> truthTable,                     // todas as combinações viáveis, com o resultado
    Map<String, List<IndependencePair>> pairs,       // por condição
    List<TestVector> minimalSuite,
    List<String> uncoveredConditions                 // condições sem nenhum par viável
) { }
```

### Exemplo de saída

Para `REQ-001`, decisão `(F1 and F2) or F3`, variante causa única:

| Vetor | F1 | F2 | F3 | Resultado |
|---|---|---|---|---|
| V1 | T | T | T | T |
| V2 | T | T | F | T |
| V3 | T | F | T | T |
| V4 | T | F | F | F |
| V5 | F | T | T | T |
| V6 | F | T | F | F |
| V7 | F | F | T | T |
| V8 | F | F | F | F |

| Condição | Pares de independência |
|---|---|
| F1 | (V2, V6) |
| F2 | (V2, V4) |
| F3 | (V4, V3), (V6, V5), (V8, V7) |

Suíte mínima: V2, V4, V6 e V3 (ou V5 no lugar de V3). São 4 testes para 3 condições.

## 5. Decisões sobre o algoritmo

### 5.1 Variante de MC/DC

O motor implementa as duas e a escolha é uma opção da chamada:

| Variante | Regra do par | Observação |
|---|---|---|
| Causa única (`UNIQUE_CAUSE`) | Só a condição analisada muda entre os dois vetores, e o resultado muda. | Mais restritiva. Pode não ter solução quando há condições acopladas. |
| Mascaramento (`MASKING`) | A condição analisada muda e o resultado muda; outras condições podem mudar desde que, em cada vetor, inverter só a condição analisada inverta o resultado. | Aceita em DO-178C (CAST-6). Padrão recomendado. |

O exemplo da seção 4 do documento de visão usa o par TFF/FFT para a condição C. Ele só é válido em mascaramento, porque A também muda. Em causa única o par seria TFF/TFT.

Curto-circuito não se aplica ao modo requisitos: é uma propriedade de como o código avalia a expressão. Ele volta a ser relevante no `mcdc-java`.

### 5.2 Condições acopladas

Condições de um requisito podem depender uma da outra. Em `REQ-003`, `F1 = velocidade > 100` implica `F2 = velocidade > 50`, então qualquer vetor com F1 verdadeira e F2 falsa é impossível.

Na Fase 1 a restrição é informada explicitamente em `McdcOptions.constraints`, como uma expressão que todo vetor viável precisa satisfazer (aqui, `not F1 or F2`). O motor descarta os vetores inviáveis antes de procurar pares.

Efeito em `REQ-003`, decisão `F1 or (F2 and F3)`:

| Condição | Sem restrição | Com `not F1 or F2` |
|---|---|---|
| F1 | 3 pares | 1 par: (TTF, FTF) |
| F2 | 1 par: (FTT, FFT) | igual |
| F3 | 1 par: (FTT, FTF) | igual |

Suíte mínima com a restrição: TTF, FTF, FTT, FFT.

Derivar as restrições automaticamente a partir dos frames (mesmo sujeito, operadores comparáveis) fica para depois, com Z3 ou uma análise de intervalos simples.

### 5.3 Tamanho da decisão

A tabela verdade tem 2^N linhas. O motor enumera tudo até N = 20 condições e recusa acima disso com erro claro. Requisitos reais raramente passam de 8.

### 5.4 Suíte mínima

Encontrar a suíte mínima é um problema de cobertura de conjuntos. Para N pequeno, busca exata; acima de um limite a definir, heurística gulosa. O relatório indica qual foi usada.

## 6. Adaptador XML

### Formato assumido (hipotético)

Três exemplos em [exemplos-xml/](exemplos-xml/):

| Arquivo | Decisão | O que exercita |
|---|---|---|
| [req-001-and-or.xml](exemplos-xml/req-001-and-or.xml) | `(F1 and F2) or F3` | Caso básico. |
| [req-002-negacao.xml](exemplos-xml/req-002-negacao.xml) | `F1 and not F2` | Negação. |
| [req-003-condicoes-acopladas.xml](exemplos-xml/req-003-condicoes-acopladas.xml) | `F1 or (F2 and F3)` | Condições acopladas. |

Estrutura:

```xml
<requirement id="REQ-002">
  <text>Se a porta estiver fechada e o sensor não detectar obstáculo, o sistema deve liberar a partida.</text>
  <frames>
    <frame id="F1" type="condition"> ... </frame>
    <frame id="F2" type="condition"> ... </frame>
    <frame id="F3" type="action"> ... </frame>
  </frames>
  <tree>
    <implies>
      <antecedent>
        <and>
          <ref frame="F1"/>
          <not><ref frame="F2"/></not>
        </and>
      </antecedent>
      <consequent><ref frame="F3"/></consequent>
    </implies>
  </tree>
</requirement>
```

Mapeamento:

| XML | Modelo |
|---|---|
| `requirement/@id` | `Decision.id` |
| `frame[@type="condition"]` | `Cond(id)` + entrada em `labels` montada a partir dos campos do frame |
| `and`, `or`, `not` dentro de `antecedent` | `And`, `Or`, `Not` |
| `consequent` | `Decision.expectedAction` |

### O que conferir quando o XML real chegar

1. **A árvore é lógica ou sintática?** Este é o maior risco. Se os nós forem operadores (`and`, `or`, `not`), o adaptador é um mapeamento direto. Se for uma árvore de análise linguística (sujeito, verbo, oração subordinada), será preciso um passo extra para extrair a estrutura lógica.
2. **Como a negação aparece:** nó próprio, atributo do frame ou só no texto.
3. **Como condição e ação são distinguidas:** por tipo de frame, por posição na árvore ou por outro marcador.
4. **Um arquivo traz um requisito ou vários.**
5. **A mesma condição repetida tem o mesmo identificador.**
6. **Há requisitos sem condição** ("o sistema deve registrar todo acesso"). Eles não geram decisão e o adaptador deve ignorá-los com aviso.

Só o `XmlRequirementReader` muda com o formato real. Motor, modelo e relatórios não são afetados.

## 7. Expressão textual

Gramática mínima para a Fase 1:

```
expr    := termo ( "or" termo )*
termo   := fator ( "and" fator )*
fator   := "not" fator | "(" expr ")" | IDENT
```

`not` tem precedência sobre `and`, que tem sobre `or`. Também são aceitos `&&`, `||` e `!`.

Com uma gramática deste tamanho, um parser escrito à mão resolve. ANTLR 4, previsto no documento de visão, passa a compensar quando a DSL ganhar comparações (`velocidade > 100`) ou blocos de requisito.

## 8. Saídas

| Formato | Fase 1 | Conteúdo |
|---|---|---|
| JSON | sim | `McdcReport` completo. É o formato de integração. |
| CSV | sim | Tabela verdade e suíte mínima. |
| Gherkin (`.feature`) | sim | Um cenário por vetor da suíte mínima, usando os `labels`. |
| Stubs JUnit | depois | |
| HTML / PDF | Fase 4 | |

## 9. Ordem de implementação

1. Modelo (`Expr`, `Decision`) e avaliação de expressão.
2. Tabela verdade com filtro de restrições.
3. Pares de independência, causa única e mascaramento.
4. Suíte mínima.
5. Parser de expressão textual.
6. Adaptador XML, sobre o formato hipotético e ajustado ao real quando disponível.
7. Exportadores JSON, CSV e Gherkin.
8. `mcdc-cli`.

Os passos 1 a 5 não dependem do XML real.

## 10. Em aberto

- Formato real do XML (seção 6).
- A ferramenta de origem é Java? Define se `mcdc-rest` é necessário.
- `groupId` e nome de pacote definitivos. O esqueleto usa `io.github.rvdomingos.mcdc`.
- Java 17 ou 21. O esqueleto usa 17, que é o instalado.
