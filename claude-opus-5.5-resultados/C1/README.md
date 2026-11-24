# Experimento C1: execução independente (Claude)

Esta pasta guarda a condição C1 da pesquisa de oráculos e testes gerados por LLM para a ferramenta MC/DC. A única
fonte das expectativas é `experimentacao-pesquisa/experimentacao-1/documentation/tool-readme-C1.md` (SHA-256
`91981FA0…D33B`, conferido). O SUT foi avaliado no commit `92d9df8`, sem alterações. O protocolo seguido está em
`experimentacao-pesquisa/protocolo/metodologia.md`, e o prompt usado foi `geracao-de-oraculos-v3.md`.

## Resumo das métricas (acumulado: baseline corrigido + extensão 01)

| Métrica | Resultado |
|---|---|
| Branch Coverage (JaCoCo 0.8.16, 4 módulos) | **1117 / 1296 = 86,19%** (baseline: 1042 / 1296 = 80,40%) |
| Testes aprovados | **97** |
| Testes falhos | **1** (EX-27: `verify` sem Z3 não avisou) |
| Testes indeterminados | **12** |

**Cobertura só com os casos determinados** (regra do pesquisador definida depois, durante o C3; indeterminados não
executados): **1107 / 1296 = 85,42%** (`resultados/acumulado-determinados`). Os vereditos são idênticos: 97 aprovados
e 1 falho. Detalhes em `experimento/determinados/README.md`.

Unidade de contagem: um caso = um ID do oráculo (110 casos: 79 no baseline e 31 na extensão). Erro técnico: AN-22 na
rodada-01 (codificação do stdout no harness), corrigido na rodada-02 sem mudar a expectativa.

## Índice

- `avaliacao/relatorio.md`: relatório completo no modelo do protocolo.
- `avaliacao/resultados-por-caso.md`: veredito, códigos de saída e asserções de cada caso
  (gerado por `avaliacao/gerar_resultados_por_caso.py`).
- `suite/`
  - `run_suite.py`: runner que lê o oráculo congelado, executa a CLI real com o agente JaCoCo e avalia cada caso.
  - `coverage.sh`: relatório JaCoCo (CSV, XML e HTML) com as classes de produção dos 4 módulos.
  - `versoes/`: versões do runner usadas nas rodadas 01 e 02.
- `resultados/`
  - `rodada-01-baseline/`: 79 casos, preservado.
  - `rodada-02-correcao/`: os 79 casos com a correção 01.
  - `rodada-03-extensao-01/`: os 31 casos da extensão.
  - `acumulado/`: merge do `jacoco.exec` das rodadas 02 e 03.
  - `rodada-04-determinados/`, `rodada-05-extensao-01-determinados/` e `acumulado-determinados/`: as mesmas
    suítes sem os indeterminados (regra posterior do pesquisador).
  - Em cada rodada: `casos/<ID>/` (stdout, stderr, `resultado.json`), `resultados.json`, `execucao.log`,
    `jacoco.exec`, `jacoco.csv`, `jacoco.xml`, `jacoco-html/` e `cobertura.txt`.
- `experimento/`
  - `analise-oraculo.md`, `inventario-oraculo.md`, `oraculo.json` e `gerar_oraculo.py`: o oráculo do baseline.
  - `entradas/`: entradas montadas para o experimento (`.mcdc`, CSV e JSON, gravados com `json.dump`).
  - `z3/`: gerador, consultas SMT-LIB, saídas do Z3 5.4.1 e `_resumo.tsv`.
  - `build-sut/`: `build.sh`, `build.log`, `classes.sha256` e `runtime.classpath`.
  - `correcoes/correcao-01-codificacao-stdout.md`: a correção da suíte e a justificativa.
  - `extensao-01/`: justificativa, oráculo, inventário, entradas e consultas Z3 da extensão.
  - `congelamento/01…05-*.sha256`: manifestos com data e hora (oráculo antes de ler o SUT; suíte antes de executar;
    correção; extensão; resultados).

## Como reproduzir

```bash
bash experimento/build-sut/build.sh <dir-build>
python -I suite/run_suite.py --oraculo experimento/oraculo.json --classpath-file <dir-build>/runtime.classpath --rodada <nova-rodada>
python -I suite/run_suite.py --oraculo experimento/extensao-01/oraculo-extensao-01.json --entradas experimento/extensao-01/entradas --classpath-file <dir-build>/runtime.classpath --rodada <nova-rodada-ext>
bash suite/coverage.sh <dir-build> <nova-rodada>
```

O runner espera o Z3 em `C:/Users/User/AppData/Roaming/Python/bin` e o JaCoCo em `~/.m2`. Os casos marcados com o
ambiente `sem_z3` tiram o Z3 do PATH.
