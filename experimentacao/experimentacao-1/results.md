# Resultados — Experimento C1

## Qualidade documental

| Medida | Original | C1 |
|---|---:|---:|
| Clareza média (escala 1–5) | 4,06 | 4,97 |
| Consistência média (escala 1–5) | 4,67 | 4,67 |

C1 melhorou a organização e a clareza, mas não eliminou os quatro pares de ações potencialmente incompatíveis nem a variável NPP não declarada. Portanto, “alta consistência” é condição pretendida, não conclusão confirmada.

## Suíte Java/PIT

O resumo de execução registra 25/25 testes aprovados. A avaliação PIT da suíte da ferramenta reporta 320 mutantes mortos de 333 (96,096%). Esses resultados descrevem a suíte de regressão da ferramenta, não a correção semântica de oráculos gerados por LLM.

## Trilha formal herdada de C0

A formalização de 36 expressões, 152 casos simbólicos e mutação de 981 expressões manteve os mesmos resultados de C0: 894 mortos, 42 sobreviventes, 21 equivalentes e 24 não avaliáveis. As guardas e ações não foram alteradas; portanto, essa igualdade não evidencia efeito da revisão documental C1.

## Métricas de oráculos

Não há Precision, Recall e F1 avaliados por uma geração independente e anotação independente para a suíte Java. A referência histórica de 95,513% de Mutation Score pertence à trilha sintética de especificação, e não deve ser apresentada como score de defeitos da implementação.

## Limitações de proveniência

Os documentos de status indicam que não houve LLM externo independente; outros registros históricos descrevem oráculos gerados pelo Copilot. Não há modelo/versão independente registrado para reconciliar esses registros. Assim, não se atribuem os números da suíte Java ao desempenho de um modelo externo.
