# Experimento C4 (Claude)

Condição C4 da pesquisa de oráculos e suítes MC/DC gerados por LLM. Fonte normativa exclusiva:
`experimentacao-pesquisa/experimentacao-4/tool-readme-C4.md` (SHA-256
`D6BC0A588CD9A7DF7F1F566573944FA5CB1707BBA676B4E9854CAD2CC5440FC2`). Modelo: Claude Opus 5.5. Commit: `ed7d2e0`.

## Métricas (rodada final `r1-baseline`)

| Métrica | Resultado |
|---|---|
| Branch Coverage (JaCoCo 0.8.16, produção dos 4 módulos) | **500 / 1296 = 38,58%** |
| Aprovados | **44** |
| Falhos | **1** (C4-D26: erro de sintaxe em `.mcdc` sem número da linha) |
| Indeterminados | **37** (não executados; não entram na cobertura) |

Unidade: caso do oráculo. Erros técnicos: 0. Houve uma única rodada, sem correções nem extensões.

## Ordem do que foi feito

1. Conferência do SHA-256 e leitura da fonte, do protocolo, do modelo de relatório e do prompt v3.
2. Análise e inventário (`experimento/analise.md`, `experimento/inventario-oraculo.md`).
3. Consultas SMT-LIB e execução do Z3 5.4.1 independente (`experimento/z3/`).
4. Oráculo (`experimento/oraculo.json`, 45 determinados e 37 indeterminados) e congelamento por SHA-256
   (`experimento/congelamento-oraculo.sha256`) antes de qualquer leitura do SUT.
5. Compilação do SUT fora do repositório (`experimento/build/`) e leitura da CLI só para invocação.
6. Suíte (`suite/runner.py`, `suite/cobertura.sh`), congelada (`suite/congelamento-suite-r1.sha256`, cópia em
   `suite/versoes/r1-baseline/`).
7. Rodada `r1-baseline` com JaCoCo (`resultados/r1-baseline/`).
8. Avaliação (`avaliacao/relatorio.md`, `avaliacao/resultados-por-caso.md`).

## Como reproduzir (Git Bash)

```bash
export MSYS_NO_PATHCONV=1
REPO=C:/Users/User/requirements-quality-llm-test-oracles
W=<diretório de trabalho fora do repositório>
C4=$REPO/claude-opus-5.5-resultados/C4
# 1. Z3 independente (regera consultas/saídas em experimento/z3)
python -I $C4/experimento/z3/gerar_e_executar.py $REPO C:/Users/User/AppData/Roaming/Python/bin/z3.exe
# 2. Oráculo (regera oraculo.json e inventario-oraculo.md; confira com congelamento-oraculo.sha256)
python -I $C4/experimento/construir_oraculo.py
# 3. Build do SUT
bash $C4/experimento/build/build-sut.sh $REPO $W
# 4. Rodada (em diretório novo) e cobertura
python -I $C4/suite/runner.py $REPO $W/classpath.txt \
  C:/Users/User/.m2/repository/org/jacoco/org.jacoco.agent/0.8.16/org.jacoco.agent-0.8.16-runtime.jar $C4/resultados/<nova-rodada>
bash $C4/suite/cobertura.sh $W $C4/resultados/<nova-rodada>
python -I $C4/avaliacao/gerar_resultados_por_caso.py <nova-rodada>
```

Requisitos: Java 21, Python 3, Jackson 2.17.2 e JaCoCo 0.8.16 no `~/.m2`. Nenhuma execução usa `--z3`.

## Índice

| Caminho | Conteúdo |
|---|---|
| `experimento/analise.md` | Estado da fonte, inventário de regras, conflitos, decisões de análise, resumo Z3 |
| `experimento/inventario-oraculo.md` | Trecho literal, regra, expectativa e justificativa por caso |
| `experimento/oraculo.json` | Oráculo congelado (casos e execuções planejadas) |
| `experimento/construir_oraculo.py` | Gerador do oráculo e do inventário |
| `experimento/entradas/` | Entrada própria (`erro-sintaxe.mcdc`) |
| `experimento/entradas-exemplos.sha256` | Hashes das entradas de `exemplos/` usadas |
| `experimento/z3/` | Gerador, consultas `.smt2`, saídas `.out`, `resumo.json` |
| `experimento/fonte.sha256` | Hashes da fonte, do prompt e do protocolo |
| `experimento/congelamento-oraculo.sha256` | Manifesto de congelamento do oráculo e das evidências |
| `experimento/build/` | Script de build, commit e hashes das classes |
| `suite/` | Runner, script de cobertura, manifesto de congelamento e `versoes/` |
| `resultados/r1-baseline/` | stdout/stderr por execução, `resultados.json`, JaCoCo (exec, CSV, XML, HTML) |
| `resultados/r1-baseline.sha256` | Hashes dos dados da rodada (exceto HTML) |
| `avaliacao/relatorio.md` | Relatório no modelo: métricas, metodologia, mudanças, discussão, limitações |
| `avaliacao/resultados-por-caso.md` | Resultado de cada caso |
