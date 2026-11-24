# Extensão coverage-informed E1 — congelada antes da execução

O JaCoCo do baseline mostrou branches não cobertos em `Predicate`,
`SmtEncoding`, `TextReport`, `CheckReport` e `VerifyReport`. A localização
orienta as entradas abaixo, mas não define seus resultados. Os oráculos
continuam derivados somente da fonte C1 congelada. Não são alterados os
artefatos nem os resultados do baseline.

Fonte, seção Uso: “`=`, `==`, `!=`, `<`, `<=`, `>`, `>=`”; seção Formatos de
entrada: “O valor pode ser lógico (`T`/`F`) ou concreto, conforme o tipo da
variável”; seção Uso: “`0`: comando concluído ... `2`: ... uma condição não
demonstrada ou um resultado esperado divergente no `check`”. Para `x` inteiro,
cada par abaixo tem uma atribuição verdadeira e uma falsa, que demonstram a
única condição, com saídas esperadas explicitadas.

| Casos | Operador | Verdadeiro | Falso | Classes visadas |
|---|---|---:|---:|---|
| E03, E10 | `=` | 0 | 1 | parser, Predicate, SmtEncoding |
| E04, E11 | `==` | 0 | 1 | parser, Predicate, SmtEncoding |
| E05, E12 | `!=` | 1 | 0 | parser, Predicate, SmtEncoding |
| E06, E13 | `<` | -1 | 0 | parser, Predicate, SmtEncoding |
| E07, E14 | `<=` | 0 | 1 | parser, Predicate, SmtEncoding |
| E08, E15 | `>` | 1 | 0 | parser, Predicate, SmtEncoding |
| E09, E16 | `>=` | 0 | -1 | parser, Predicate, SmtEncoding |

E03–E09: `check "x OP 0"` com CSV contendo as duas atribuições e seus
resultados; espera código 0. E10–E16: `analyze "x OP 0" --z3 --format json`;
espera as duas linhas viáveis, atribuições concretas que satisfaçam seus
resultados e código 0. As fórmulas e testemunhas explícitas são geradas pelo
Z3 independente em `extensao-formulas.smt2` e `extensao-z3.json` antes da
execução. Cada caso é `CONFORME À DOCUMENTAÇÃO`; nomes de campos usados para
acesso são detalhes de adaptação do harness, não exigências de nomenclatura.

- E01: repetir B31 usando decodificação apropriada ao canal de erro Windows.
  A fonte diz “As opções que exigem o Z3 avisam quando o executável não está
  instalado.” Pré-condição PATH sem Z3; deve haver aviso da ausência. O
  baseline permanece inalterado; a leitura incorreta de seus bytes é erro
  técnico do harness, não uma divergência do SUT.
- E02: `analyze "A and B"` no formato padrão texto. Fonte: “`text` (padrão)”
  e “Tabela verdade, pares de independência, suíte de testes”. O relatório
  deve conter os componentes identificáveis, com saída 0. Alvo `TextReport`.
- E17: `check "A"` com CSV `test,input,value`, linhas `T1,A,F` e `T2,A,T`,
  sem colunas opcionais. A fonte diz “As colunas `decision` e
  `expected_outcome` são opcionais.” Ambas as atribuições demonstram a
  condição; código 0. Alvo `TestCasesFile` e `CheckReport` textual.
- E18: `verify` em duas decisões guardadas por `A`, ambas atribuindo `x := 0`.
  Fonte: “Conflitos (dois requisitos valem juntos e escrevem valores
  diferentes)”; os valores são iguais, logo não há conflito. Sem contexto,
  nenhuma lacuna foi solicitada; código 0. Alvo `VerifyReport` texto.
- E19: `verify` com guarda `A or not A`, contexto `A or not A`, sem outra
  decisão. A guarda é sempre verdadeira, portanto não há lacuna e código 0.
  Fonte: “lacunas (nenhum requisito vale)” e “nessa situação, sempre alguma
  guarda vale”. Alvo ramo sem lacuna do verificador.

Lacunas sem suporte: aspectos de mensagens específicas, exceções internas,
tratamento de estruturas JSON sem esquema documentado e seleção gulosa além
dos critérios declarados. Não são asserções. Os branches das classes de
mutação permanecem no denominador, mas não são exercitados por análise de
mutação nesta pesquisa. Esta busca é limitada, não exaustiva.
