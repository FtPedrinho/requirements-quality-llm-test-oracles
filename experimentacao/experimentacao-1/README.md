# Experimento 1 - revisão C1 dos requisitos

Esta etapa prepara exclusivamente uma versão **alta clareza e alta consistência (C1)** dos documentos usados na Experimentação 0.

## Estrutura

```text
experimentacao/experimentacao-1/
├── README.md
├── requirements/
│   ├── original/
│   ├── experimental/
│   ├── source-hashes.csv
│   ├── change-log.csv
│   ├── traceability-matrix.csv
│   └── review-decisions.md
└── document-quality-audit.md
```

Os arquivos originais não foram modificados. Toda revisão foi aplicada às cópias em `requirements/experimental/`.

## Estado atual

- 6 documentos duplicados;
- 36 unidades principais da Experimentação 0 analisadas;
- 33 textos estruturados JSON padronizados;
- 42 registros rastreáveis, incluindo três expressões gerais e seis versões auxiliares `.mcdc`;
- 0 regras funcionais alteradas;
- 0 contradições resolvidas por suposição;
- 5 pendências críticas ou documentais restantes.

A classificação C1 não está confirmada porque permanecem incompatibilidades formais e lacunas que exigem evidência ou validação humana.

## Execução concluida

- Formalização Z3 dos 36 requisitos centrais;
- geração independente de 36 oráculos C1;
- geração de 152 casos simbólicos;
- análise preliminar de 119 pares MC/DC;
- Mutation Testing com 981 mutantes;
- auditoria independente das métricas;
- análise de sensibilidade às ressalvas TIS/NPP.

## Artefatos principais

- [Protocolo experimental](experiment-protocol.md)
- [Relatório técnico](experiment-report.md)
- [Catálogo de oráculos](oracles/oracle-catalog.md)
- [Catálogo JSON](oracles/oracle-catalog.json)
- [Casos de teste](test-suites/generated-test-cases.md)
- [Auditoria de Mutation Testing](mutation-testing/audit/audit-summary.md)
- [Relatório de métricas](metrics-report.md)
- [Limitações e validade](limitations-and-validity.md)
- [Resumo estruturado](results-summary.csv)
- [Suíte executável C1](test-suites/executable-suite/README.md)
- [sessão das suítes de teste](test-suite-session.md)
- [comparação estrutural da documentação](document-structure-comparison.md)
- [métricas dos oráculos](oracle-metrics.csv)
- [classificação dos oráculos](oracle-classification.csv)
- [gabarito dos oráculos](oracle-reference-catalog.csv)
- [análise das métricas dos oráculos](oracle-metrics-analysis.md)

## Entregáveis concretos adicionados pelo adendo

- [documentação EXP1](documentation/)
- [avaliação da documentação EXP0](documentation-assessment/exp0-documentation-assessment.md)
- [avaliação da documentação EXP1](documentation-assessment/exp1-documentation-assessment.md)
- [comparação documental](documentation-assessment/documentation-comparison.csv)
- [gabarito independente](oracle-reference/oracle-reference-catalog.csv)
- [status da geração por LLM](oracle-generation/exp1/status.md)
- [suíte JUnit EXP1](test-suites/exp1/README.md)
- [catálogo da suíte EXP1](test-suites/exp1/test-catalog.csv)
- [rastreabilidade da suíte EXP1](test-suites/exp1/traceability.csv)
- [resultados da execução EXP1](execution-results/exp1/execution-summary.md)
- [classificação dos oráculos](oracle-evaluation/oracle-classification.csv)
- [métricas dos oráculos](oracle-evaluation/oracle-metrics.csv)
- [comparação de Mutation Testing](mutation-testing/mutation-comparison.md)
- [análise comparativa final](comparison/exp0-exp1-final-analysis.md)
- [status do experimento](experiment-status.md)
