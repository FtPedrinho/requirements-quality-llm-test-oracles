# C2 — Claude (Opus 5.5)

Execução independente da condição **C2** do protocolo em
`experimentacao-pesquisa/protocolo/metodologia.md`, com o prompt
`experimentacao-pesquisa/prompts/geracao-de-oraculos-v3.md`.

- Fonte normativa exclusiva: `experimentacao-pesquisa/experimentacao-2/documentation/tool-readme-C2.md`
  (SHA-256 `61C4062B5FC6B4F364F40465B0E017C80E0FA0C5433412EB2E925C545F6EFBE1`, conferido).
- Commit de referência do SUT: `ed7d2e00170e3e2c28201bf63e1b51a24a1bfe81`.
- Oráculo congelado em 2026-11-24 11:07:01 -0300, antes de ler ou executar o SUT.

## Métricas

A cobertura oficial conta **só os casos determinados**; a execução diagnóstica dos casos
indeterminados não entra na Branch Coverage. Por isso a cobertura vem das rodadas r3/r4,
que reexecutam apenas os casos determinados (resultados por caso idênticos a r1/r2).

| Métrica | Baseline | Extensão | Acumulado |
|---|---|---|---|
| Branch Coverage (JaCoCo, 4 módulos, só determinados) | 1068/1296 (82,41%) | 901/1296 (69,52%) | **1091/1296 (84,18%)** |
| Testes aprovados | 75 | 12 | **87** |
| Testes falhos | 0 | 0 | **0** |
| Testes indeterminados | 15 | 0 | **15** |

Unidade: um caso = uma invocação da CLI com ID estável. Erros técnicos: 0.
As rodadas r1/r2 (com os indeterminados executados como diagnóstico) mediram 1076/1296
(83,02%) e 1099/1296 (84,80%); ficam preservadas, mas não são a métrica oficial.
Detalhes e limitações em [avaliacao/relatorio.md](avaliacao/relatorio.md).

## Ordem do que foi feito

1. Leitura do README da pesquisa, do protocolo, do modelo de relatório e do prompt.
   Conferência do SHA-256 da fonte C2 e leitura integral da fonte, sem código do SUT.
2. Leitura dos arquivos de `exemplos/` citados pela fonte, apenas como entrada.
3. Inventário dos requisitos (R1–R25) e decisões de leitura do texto degradado: lacuna
   reconstruída só quando outro trecho legível a fixa; senão INDETERMINADO.
4. Geração das entradas próprias e das consultas SMT-LIB; execução do Z3 independente.
   Uma consulta de fronteira com erro de ordem foi corrigida e tudo foi regerado.
5. Geração do oráculo (90 casos: 75 determinados, 15 indeterminados), da análise e do
   inventário; congelamento por SHA-256.
6. Só então: build do SUT fora do repositório e leitura da CLI, apenas para saber como
   invocá-la e onde está cada dado na saída JSON.
7. Criação do runner e do script de cobertura; congelamento da suíte; rodada `r1-baseline`.
8. A cobertura localizou áreas pouco exercitadas; 12 casos de extensão com suporte
   documental já registrado; congelamento; rodada `r2-extensao`; merge para o `acumulado`.
9. Como a cobertura dos casos indeterminados não deve contar, rodadas `r3-determinados-baseline`
   e `r4-determinados-extensao` reexecutaram só os casos determinados (mesmo runner, oráculo e
   entradas); merge em `acumulado-determinados`, que dá a cobertura oficial.
10. Relatório, resultados por caso e este README.

## Como reproduzir

```bash
bash experimento/build/build.sh <pasta-fora-do-repo>   # gera as classes; o classpath usado está em experimento/build/classpath.txt
python experimento/scripts/gerar_entradas.py           # entradas próprias
python experimento/scripts/gerar_z3.py                 # consultas e saídas Z3 (z3.exe 5.4.1)
python experimento/scripts/gerar_oraculo.py            # oraculo.json
python experimento/scripts/gerar_inventario.py
cd suite
python runner.py <nova-rodada>                         # baseline (recusa sobrescrever rodada existente)
python runner.py <nova-rodada-ext> --oraculo ../experimento/extensao-r2/oraculo-extensao.json \
  --manifesto ../experimento/congelamento/extensao-r2.sha256 --entradas ../experimento/extensao-r2/entradas
python cobertura.py ../resultados/<rodada>
python runner.py <rodada-det> --casos <IDs determinados>      # cobertura oficial: só casos determinados
python cobertura.py ../resultados/<acumulado> ../resultados/<r3>/jacoco.exec ../resultados/<r4>/jacoco.exec
```

## Índice

- [avaliacao/relatorio.md](avaliacao/relatorio.md): relatório no modelo do protocolo.
- [avaliacao/resultados-por-caso.md](avaliacao/resultados-por-caso.md): resultado de cada caso por rodada.
- `experimento/`
  - [analise-oraculo.md](experimento/analise-oraculo.md): leitura da fonte, inventário R1–R25, indeterminações, Z3.
  - [inventario-casos.md](experimento/inventario-casos.md) e `oraculo.json`: 90 casos do baseline.
  - `entradas/`: entradas próprias (geradas por `scripts/gerar_entradas.py`).
  - `z3/`: consultas SMT-LIB, saídas do Z3 5.4.1 e `resumo-z3.json`.
  - `scripts/`: geradores de entradas, consultas Z3, oráculo, inventário e tabela de resultados.
  - `build/`: build do SUT (`build.sh`, `build.md`, log, classes, `classes.sha256`, classpath).
  - `congelamento/`: manifestos `*.sha256` com data e hora (oráculo, suíte r1, extensão r2).
  - `extensao-r2/`: oráculo, entradas e Z3 da extensão.
  - [extensoes-e-correcoes.md](experimento/extensoes-e-correcoes.md): justificativa da extensão; sem correções pós-congelamento.
- `suite/`: `runner.py` (suíte), `cobertura.py` (JaCoCo); `versoes/` guarda o runner de cada rodada.
- `resultados/`
  - `r1-baseline/`, `r2-extensao/`: `resultados.json`, `console.txt`, `casos/<ID>/` (stdout/stderr), `arquivos-o/`, `jacoco.exec`, `jacoco.csv`, `jacoco.xml`, `jacoco-html/`, `cobertura.json`.
  - `r3-determinados-baseline/`, `r4-determinados-extensao/`: reexecução só dos casos determinados.
  - `acumulado-determinados/`: merge de r3+r4 — **cobertura oficial**.
  - `acumulado/`: merge de r1+r2 (inclui indeterminados; preservado, não oficial).
