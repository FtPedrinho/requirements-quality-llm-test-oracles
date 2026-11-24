# C3 — resultados e avaliação

## Acesso rápido

- [Suíte de testes](suite/README.md): executores, entradas e oráculos congelados.
- [Passo a passo](metodologia.md): verificação, preparação e reexecução sem sobrescrever o experimento.
- [Relatório completo e evidências](detalhes-C3/relatorio-final.md).
- [Métricas estruturadas](detalhes-C3/metricas.json) e [gráfico de Branch Coverage](detalhes-C3/branch-coverage.svg).

## Resultado

| Indicador | Resultado |
|---|---:|
| Branch Coverage total | **323 / 1296 (24,92%)** |
| Branch Coverage dos casos conformes, válidos e executáveis | **323 / 1296 (24,92%)** |
| Casos distintos | 30 |
| Casos aprovados após repetição técnica | 30 |
| Falhas semânticas observadas | 0 |
| Erro técnico inicial, preservado | 1 |
| Registros de conflito indeterminados | 15 |
| Oráculos classificados como incorretos ou inválidos | 0 |

O caso com erro técnico passou na repetição. Os 15 registros indeterminados agrupam conflitos documentais; não são casos executáveis completos. A taxa conservadora de indeterminação é 15/29 = 51,72%, contando 14 oráculos determinados e 15 registros de conflito. A classificação dos oráculos foi feita pela própria IA, sem revisão independente. Modelo: GPT 6.1 Terra (informado pelo pesquisador em 24/11/2026, após a coleta).

## Avaliação e limites

A cobertura é baixa: o módulo `mcdc-z3` teve 0/386 branches cobertos. Comparações, fronteiras, restrições, `check` e `verify` não foram cobertos por expectativas concretas congeladas nesta tentativa. As classes de produção dos quatro módulos, inclusive as de mutação não executadas, permaneceram no denominador.

Não é possível demonstrar cegamento nem ausência absoluta de influência: o contexto inicial tinha informação qualitativa anterior, e uma busca enumerou caminhos de suítes de outras condições, sem abrir seus conteúdos. O usuário autorizou continuar ignorando os resultados anteriores. O experimento não demonstra cobertura máxima nem conformidade geral do SUT.

A pasta [detalhes-C3](detalhes-C3/) conserva documentação normativa, formalizações, hashes, saídas Z3, resultados por caso, logs e dados brutos. Os caminhos originais dentro dos logs foram preservados como registro histórico; a [verificação de integridade](suite/verificar-integridade.py) reconhece a mudança de diretório sem alterar os manifestos congelados.
