# Experimento C2 — baixa clareza e alta consistência

## Objetivo, condição e metodologia

Investigar como a redução da clareza afeta a geração de oráculos, mantendo as regras e relações documentais sem contradições deliberadas. A documentação C2 foi copiada e degradada linguisticamente; não foi corrigida durante a geração dos testes.

Foram preservados os 26 testes originais (S1), tentados os 10 casos ausentes (S2) e avaliadas as duas partes em conjunto (S3). Os oráculos foram comparados com o gabarito independente congelado de 19 comportamentos.

## Métricas utilizadas

Somente: cobertura de requisitos, Mutation Score, Precision, Recall e F1-score. Resultados de execução e contagens de testes contextualizam as cinco métricas, mas não são métricas adicionais da avaliação.

## Artefatos essenciais

- Resultados completos: [results.md](results.md).
- Documento C2 adaptado: [documentation/tool-readme-C2.md](documentation/tool-readme-C2.md).
- Suíte S1/S2 e suíte combinada: [test-suite/](test-suite/) e [test-suites/exp2/](test-suites/exp2/).
- Catálogo de testes: [test-suite/test-catalog.csv](test-suite/test-catalog.csv).
- Gabarito usado para avaliação: [oracle-reference/](oracle-reference/).

## Proveniência de IA

Os registros não indicam geração independente por outro modelo externo. Os complementos foram produzidos pelo agente Copilot desta sessão a partir da documentação literal; as suposições não foram tratadas como fatos documentados.
