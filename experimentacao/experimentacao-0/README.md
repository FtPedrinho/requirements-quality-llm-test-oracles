# Experimentação 0 - análise formal e geração de oráculos

Esta experimentação estabelece uma linha de base para **The Impact of Requirements Quality on LLM-Generated Test Oracles**. Ela utiliza exclusivamente os requisitos originais do dataset, sem manipular clareza ou consistência.

## Objetivo

Investigar em que medida os requisitos originais permitem:

- formalização verificável por Z3;
- geração independente de oráculos por uma LLM;
- derivação de casos de teste estruturados;
- análise preliminar de MC/DC;
- identificação de limitações que exigem validação humana.

Esta etapa não responde à pergunta principal da pesquisa nem estabelece conclusões causais.

## Sequência obrigatória

1. inventário das fontes normativas;
2. formalização e análise com Z3;
3. geração independente de oráculos pelo Copilot;
4. verificação dos oráculos com Z3;
5. derivação da suíte e análise MC/DC;
6. preparação da validação humana.

## Artefatos

- [protocolo.md](protocolo.md)
- [metadata.md](metadata.md)
- [inventário Z3](z3-analysis/formalization.md)
- [resultados Z3](z3-analysis/verification-results.md)
- [contraexemplos](z3-analysis/counterexamples.md)
- [scripts Z3](z3-analysis/scripts/)
- [prompt da geração](llm-generation/prompt-copilot.md)
- [relatório da geração](llm-generation/generation-report.md)
- [catálogo de oráculos](oracles/oracle-catalog.md)
- [catálogo JSON](oracles/oracle-catalog.json)
- [casos de teste](test-suites/generated-test-cases.md)
- [análise MC/DC](test-suites/mcdc-analysis.md)
- [comparação com Z3](evaluation/z3-oracle-comparison.md)
- [validação humana](evaluation/human-validation.md)
- [avaliação preliminar](evaluation/preliminary-assessment.md)
- [questões e limitações](evaluation/issues-and-limitations.md)
- [relatório final](relatorio-final.md)
- [avaliação por Mutation Testing](mutation-testing/README.md)
- [relatório final da Mutation Testing](mutation-testing/final-report.md)

## Integridade

Os arquivos originais não são alterados. Todo conteúdo produzido por esta experimentação fica em `experimentacao/experimentacao-0/`.
