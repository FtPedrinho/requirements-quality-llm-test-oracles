# Registro de reorganização C1

Pastas realinhadas ao layout das demais LLMs (`avaliacao/`, `experimento/`, `resultados/`, `suite/`). Nenhum resultado, métrica, oráculo
ou expectativa foi alterado; os arquivos foram movidos com `git mv`.

| Antes | Depois |
|---|---|
| `resultados/RESULTADOS-C1.md` | `avaliacao/relatorio.md` |
| `resultados/resultados-por-caso.csv` | `avaliacao/resultados-por-caso.csv` |
| `resultados/{bruto-baseline,junit-baseline.xml,jacoco-baseline*,resultados-por-caso-baseline.csv}` | `resultados/rodada-01-baseline/` |
| `resultados/{bruto-extensao,junit-extensao.xml,jacoco-extensao.exec,resultados-extensao.csv}` | `resultados/rodada-02-extensao/` |
| `resultados/jacoco-acumulado*` | `resultados/acumulado/` |
| `detalhes-C1/{oraculo.json,analise-documental.md}` | `experimento/{oraculo.json,analise-oraculo.md}` |
| `detalhes-C1/{gerar_smt.py,smt/}` | `experimento/z3/` |
| `detalhes-C1/congelamento-{oraculo,suite,extensao}.sha256` | `experimento/congelamento/{01-oraculo,02-suite,03-extensao}.sha256` |
| `detalhes-C1/README.md` | `experimento/README.md` |

Ajustes de caminho (manifestos `congelamento/*.sha256` históricos, **não** editados):

| Arquivo | SHA-256 antes | SHA-256 depois |
|---|---|---|
| `suite/conftest.py` | `606cd96471c729b26acaf21db5052befb507a2c1430b0764170bb924c1f3164c` | `07707ad5b7a5442a648a674d6376329ce83ae9a2c9018e2b1c338e522f1f12dc` |
| `suite/test_c1.py` | `93fa2d11771440cb8366e6edadcc520ad2712b966781700faa44f8d34a394bfc` | `a83d42c4278594e6545e4f4c92e148872a60683da6677aceac8eb439a180a6ce` |
| `suite/README.md` | `7d01378c561cfb68a419a343a446d1e9fa7b86ee916cbcf50813a1d027a72c71` | `812eea79db28050f4dc12af6ddd6de64cfd64ab06367a0490675a2fc6fa3d391` |

`test_c1_extensao.py` e `oraculo.json` não mudaram. A pasta `resultados/` de execução da extensão usa `C1_BRUTO`/`C1_CSV` para redirecionar saídas.
