# Experimento C0 — linha de base exploratória

## Objetivo, condição e metodologia

Registrar a linha de base com a documentação original, sem uma manipulação controlada de clareza ou consistência. C0 é exploratório e não corresponde, por si só, a uma célula do desenho fatorial C1–C4.

O processo histórico incluiu formalização de 36 expressões/requisitos com Z3, elaboração de oráculos e casos simbólicos para VM/TIS/NPP, além de uma suíte JUnit separada contra a ferramenta MC/DC. Essas duas trilhas têm sistemas sob teste e unidades de análise diferentes; não devem ser combinadas em um único score.

## Métricas do experimento

Para a trilha formal: casos, pares MC/DC, mutantes, equivalentes, sobreviventes e casos não avaliáveis. Para a suíte da ferramenta: execução JUnit e PIT. Não há uma cobertura de requisitos ou uma classificação Precision/Recall/F1 comparável à referência independente de 19 comportamentos usada em C2/C3.

## Artefatos essenciais

- Resultados: [results.md](results.md).
- Suíte JUnit da ferramenta: [test-suites/exp0/](test-suites/exp0/).
- Casos/oráculos formais: [oracles/](oracles/) e [test-suites/](test-suites/).
- Fonte documental: [requisitos originais em exemplos/](../../exemplos/) e [especificação técnica](<../../Especificação Técnica - Ferramenta Dupla MC_DC (Requisitos e Código Java).pdf>). C0 não possui uma versão documental adaptada.
- Instrução Copilot sem respostas geradas: [prompt-copilot.md](llm-generation/prompt-copilot.md).

## Proveniência e limites

Os registros de geração divergem quanto à proveniência: um relatório atribui os oráculos ao Copilot, enquanto outro registra que não houve LLM externo. Como versão e execução independente não foram preservadas de forma consistente, não se atribuem métricas de qualidade dos oráculos a um modelo externo.
