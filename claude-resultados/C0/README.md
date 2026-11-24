# C0: execução do Claude (documentação original)

Execução da condição C0 conforme o [protocolo](../../experimentacao-pesquisa/protocolo/metodologia.md) e o [prompt comum](../../experimentacao-pesquisa/prompts/geracao-de-oraculos-v3.md). O único gabarito é o README original (SHA-256 `72B827BD…95F8`).

## Resultado

| Métrica | Resultado final (rodada 2 + extensão 1) |
|---|---|
| Branch Coverage | **1097 / 1296 = 84,65%** |
| Testes aprovados | **92** |
| Testes falhos | **1** |
| Testes indeterminados | **14** |

Só o baseline (rodada 2): 72 aprovados, 0 falhos, 13 indeterminados, cobertura de 1040/1296 (80,25%). Os detalhes estão em [avaliacao/relatorio.md](avaliacao/relatorio.md).

## Estrutura

| Pasta | Conteúdo |
|---|---|
| [suite/](suite/) | A suíte: `executar_suite.py` (runner caixa-preta pela CLI com o agente JaCoCo e avaliadores próprios), `cobertura.sh` (relatório JaCoCo dos quatro módulos) e `config.json` |
| [resultados/](resultados/) | Uma pasta por fase (`rodada-1`, `rodada-2`, `extensao-1`, `acumulado-rodada2-extensao1`), com `resultados.json`, stdout e stderr por caso, `jacoco.exec`, CSV, XML e HTML |
| [avaliacao/](avaliacao/) | [relatorio.md](avaliacao/relatorio.md) (métricas, evidências, limitações) e [resultados-por-caso.md](avaliacao/resultados-por-caso.md) |
| [experimento/](experimento/) | Demais informações: o oráculo ([analise.md](experimento/oraculo/analise.md), [oraculo.json](experimento/oraculo/oraculo.json), entradas e consultas e resultados Z3), a [extensão 1](experimento/extensao-1/README.md), a [correção 1](experimento/correcao-1/README.md), o [build do SUT](experimento/build-sut/COMO-FOI-COMPILADO.md) e os manifestos de congelamento (`CONGELAMENTO-*.sha256` / `.data`) |

## Ordem do que foi feito

1. Conferi o hash da fonte e li o README C0 inteiro.
2. Montei o oráculo (85 casos: 72 determinados e 13 indeterminados) e fiz 94 consultas Z3 independentes. Congelei às 09:42.
3. Só então inspecionei o SUT, compilei uma cópia do commit, escrevi a suíte e congelei às 09:46.
4. Rodada 1: 69 aprovados, 13 indeterminados e 3 inválidos por entrada malformada. Corrigi as entradas sem mudar expectativas e congelei às 09:49.
5. Rodada 2: 72 aprovados, 0 falhos, 13 indeterminados.
6. Extensão 1: 22 casos novos para desvios ainda não cobertos, com 42 consultas Z3. Congelei às 09:55 e executei: 20 aprovados, 1 falho, 1 indeterminado.
7. Cobertura acumulada: 84,65%.
