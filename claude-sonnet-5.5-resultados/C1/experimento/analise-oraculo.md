# Análise documental C1 (feita antes de ler qualquer código do SUT)

Fonte única: `experimentacao-pesquisa/experimentacao-1/documentation/tool-readme-C1.md`
(SHA-256 verificado = `91981FA0181E5CC1BC5A67DAAFC965BB82D6F8EB0A6D47EB58CE291A3EF5D33B`).
Lida integralmente. Revisão: **autorrevisão** (sem revisor independente).

## Inventário

- **Comandos**: `analyze`, `check`, `verify`; fontes: expressão direta, `-f .mcdc`, `--json`.
- **Opções**: `--unique-cause`, `--constraint`, `--z3`, `--exact`, `--direct`, `--boundary`,
  `--mutation`, `--context`, `--format {text,json,csv,truth-csv}`, `-o`.
- **Operadores**: e (`and`,`&&`,`/\`), ou (`or`,`||`,`\/`), não (`not`,`!`), comparações
  (`=`,`==`,`!=`,`<`,`<=`,`>`,`>=`); precedência e antes de ou.
- **Códigos de saída**: 0 / 1 (entrada inválida) / 2 (condição sem par, não demonstrada, esperado
  divergente, conflito ou lacuna).
- **Conceitos**: entrada = variável distinta; condição = ocorrência (`A#1`, `A#2`); tabela-verdade
  2ⁿ; pares; suíte gulosa (N+1 possível) ou exata (mínima); diagnóstico redundante × bloqueada.
- **Limites**: 20 / 12 / 30 entradas; 1000 pares por condição; guardas temporais de um passo.
- **Números documentados**: exemplos MinimalSuiteTest (4 e 3), exemplo `--exact` 5 × 6 guloso,
  paridade de 3 entradas = 8 testes, tabela de regressão VM/TIS/NPP, REQ-003 redundante.

## Regras de decisão do oráculo

1. Só entram como DETERMINADO casos cuja expectativa decorre de texto literal ou de fato
   lógico verificável pelo Z3 (existência de par de causa única, suíte mínima, relação entre predicados,
   fronteiras, enum, sobreposição de guardas, lacunas, avaliação de testes dados).
2. Definição adotada, declarada: *par de causa única* = linhas que diferem só na condição analisada
   e com resultado diferente (leitura do termo). A definição de **mascaramento** não é dada;
   nenhum caso depende dela (casos com `A#1/A#2` são INDETERMINADOS quanto a pares/suíte).
3. Não se esperam campos de JSON, nomes de colunas ou textos de mensagem, que o texto não especifica;
   só: códigos de saída, palavras documentadas (`redundante`, `bloqueada`, `A#1`, IDs, valores
   concretos), contagens (testes, linhas, 2ⁿ) e JSON sintaticamente válido.
4. Afirmações da seção *Qualidade e testes* sobre comportamento do produto (descrições dos testes e
   tabela de regressão) foram tratadas como parte da fonte normativa, porque C1 é a verdade absoluta.

## Registro de tensões (não resolvidas pelo texto)

- **Paridade de 3 entradas = 8 testes** × Z3 por entrada = 4: o texto conta por *ocorrência*;
  o caso C1-S07 mantém 8 (afirmação literal). Divergência de granularidade registrada.
- "`speed > 100` é uma entrada ou ocorrência da variável `speed`?" — C1-I12 INDETERMINADO.
- "lacunas só com contexto" admite duas leituras — C1-I05 INDETERMINADO.
- Opções de execução das métricas de regressão (VM/TIS/NPP) não são citadas; usadas `--z3` (e
  `--mutation` para mutantes) como leitura mais natural; é suposição registrada.
- Arquivos `exemplos/*.json|.mcdc` são citados pela documentação mas não fazem parte dela; sua
  existência no repositório só é verificada na execução.

## Casos

57 DETERMINADOS e 15 INDETERMINADOS (ver `oraculo.json`). Indeterminados não são executados
(decisão do pesquisador).
