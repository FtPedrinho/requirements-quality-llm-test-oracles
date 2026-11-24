# C3 — execução da condição (Claude)

Fonte: `experimentacao-pesquisa/experimentacao-3/documentation/tool-readme-C3.md`
(SHA-256 `F18B0821…87A3`, conferido). SUT: commit `ed7d2e0`.

## Métricas (resultado final: r4, cobertura só dos casos determinados)

| | Branch Coverage | Aprovados | Falhos | Indeterminados |
|---|---|---|---|---|
| **r4 (final)** | **859/1296 = 66,28%** | **40** | **0** | **39** |
| r3 (indeterminados executados como diagnóstico; histórico) | 1056/1296 = 81,48% | 40 | 0 | 39 |

Regra adotada: um registro INDETERMINADO não cumpre o papel de teste (não tem expectativa). Por isso, na r4, os
39 indeterminados são registrados e contados, mas não executados, e não afetam a cobertura.

Histórico preservado: r1 = 78,40%, 34/2/39 brutos (T20, T21 e T22 eram inválidos por erro de entrada do
harness); r2 = correção + extensão; acumulado r1+r2 = 82,41%, 40/0/47. O acumulado foi **substituído pela r3**,
porque incluía I40–I47, diagnósticos criados só para alcançar código, sem base documental. Na r3 eles foram
removidos, e o código que só eles alcançavam ficou sem cobertura. Detalhes em `avaliacao/relatorio.md`.

## Ordem do que foi feito

1. Leitura do protocolo, do modelo e do prompt; conferência do hash e leitura da fonte C3.
2. Análise e catálogo de conflitos K1–K15 (`experimento/analise.md`); entradas e 106 consultas Z3
   (`experimento/gerar_oraculo.py`); oráculo com 75 casos (`experimento/casos.py` → `oraculo.json`,
   `inventario-oraculo.md`).
3. Congelamento: `experimento/congelamento-oraculo.sha256`.
4. Build do SUT fora do repositório (`experimento/build/build.sh`, `classes.sha256`).
5. Leitura da CLI (só invocação e formato de saída); `suite/runner.py` e `suite/cobertura.sh`; congelamento em
   `experimento/congelamento-suite-r1.sha256`.
6. Rodada r1 → `resultados/r1/`.
7. Correção e extensão (`experimento/extensao-r2/`, congelada em `experimento/congelamento-r2.sha256`) →
   rodada r2 → `resultados/r2/`.
8. Acumulado r1+r2 (`resultados/acumulado/`), depois substituído.
9. Revisão: remoção de I40–I47 (sem base documental) e suíte refeita do zero (`experimento/r3/selecao.py`,
   congelada em `experimento/congelamento-r3.sha256`; runner `suite/versoes/runner-r3.py`, uma execução por
   comando distinto) → rodada r3 → `resultados/r3/`.
10. Cobertura sem os indeterminados: rodada r4 só com os 40 determinados (`experimento/r4/ids-determinados.txt`,
    `congelamento-r4.sha256`) → `resultados/r4/` (resultado final).

## Como reproduzir (Git Bash)

```bash
export MSYS_NO_PATHCONV=1
cd claude-opus-5.5-resultados/C3
python -I experimento/gerar_oraculo.py C:/Users/User/AppData/Roaming/Python/bin/z3.exe && python -I experimento/casos.py
bash experimento/build/build.sh C:/Users/User/requirements-quality-llm-test-oracles <SUT_DIR>
cd suite && python -I runner.py <rodada> <SUT_DIR> && cd ..
bash suite/cobertura.sh resultados/<rodada> <SUT_DIR>
python -I experimento/extensao-r2/gerar_r2.py <z3.exe>
python -I experimento/r3/selecao.py
cd suite && C3_ORACULO=../experimento/r3/oraculo-r3.json python -I runner.py <rodada> <SUT_DIR> && cd ..
bash suite/cobertura.sh resultados/<rodada> <SUT_DIR>
# r4: os mesmos comandos, passando ao runner.py os IDs de experimento/r4/ids-determinados.txt
```

`runner.py` recusa uma rodada já existente. As versões usadas estão em `suite/versoes/` (r1: `runner-r1.py`,
r2: `runner-r2.py`, r3: `runner-r3.py`, r4: `runner-r4.py` = `runner.py` atual). Para conferir os manifestos: `sha256sum -c experimento/congelamento-*.sha256`. Esses
manifestos usam caminhos relativos: `congelamento-oraculo` a partir de `experimento/`, `congelamento-suite-r1` a partir de `suite/` (o `runner.py` atual é a versão r4, idêntica à r3; a r1 está em `suite/versoes/runner-r1.py`), e `congelamento-r2`, `congelamento-r3` e `congelamento-r4` a partir de `C3/`.

## Índice

- `avaliacao/relatorio.md`: relatório (modelo da pesquisa), metodologia e discussão.
- `avaliacao/resultados-por-caso.md`: resultado de cada caso por rodada e acumulado.
- `experimento/`: análise, oráculo, inventário, entradas, Z3, build, manifestos e extensão r2.
- `suite/`: runner, script de cobertura, tabulação e versões.
- `resultados/r4` (final); `resultados/r3`, `resultados/r1`, `resultados/r2`, `resultados/acumulado` (histórico): saídas por caso, `jacoco.exec`, CSV, XML e HTML.
