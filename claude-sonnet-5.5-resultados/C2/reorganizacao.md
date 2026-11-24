# Registro de reorganização C2

Pastas realinhadas ao layout das demais LLMs (`avaliacao/`, `experimento/`, `resultados/`, `suite/`) após o envio do commit beb98bf.
Nenhum resultado, métrica, oráculo ou expectativa foi alterado; apenas movimentação e ajuste de caminhos/textos.

| Antes | Depois |
|---|---|
| `resultados/RESULTADOS-C2.md` | `avaliacao/relatorio.md` |
| `resultados/resultados-por-caso.csv` | `avaliacao/resultados-por-caso.csv` |
| `resultados/{bruto,junit-baseline.xml,jacoco-baseline*,resultados-por-caso-baseline.csv}` | `resultados/rodada-01-baseline/` |
| `resultados/{bruto-extensao1..3,junit-extensao1..3.xml,resultados-por-caso-extensao1..3.csv}` | `resultados/rodada-02-extensoes/` |
| `resultados/jacoco.{exec,csv,xml}`, `jacoco-html/` | `resultados/acumulado/` |
| `detalhes-C2/{oraculo*.json,gerar_oraculo*.py}` | `experimento/` |
| `detalhes-C2/analise-documental.md` | `experimento/analise-oraculo.md` |
| `detalhes-C2/{gerar_smt.py,smt/}` | `experimento/z3/` |
| `detalhes-C2/congelamento-{oraculo,suite}.sha256` | `experimento/congelamento/{01-oraculo,02-suite}.sha256` |
| `detalhes-C2/README.md` | `experimento/README.md` |

Os manifestos `congelamento/*.sha256` são históricos e **não** foram editados (seus caminhos refletem o layout antigo; `conftest.py`,
`test_c2.py` e `suite/README.md` constam neles com os hashes anteriores).

| Arquivo | SHA-256 antes | SHA-256 depois |
|---|---|---|
| `suite/conftest.py` | `29d9c098af36fe69613fa501c9555e53833ded94f9c7c4c7972abc80f85c10c5` | `dbc9cb9f466744a4fe17ee8ff43d9e6f0ccd315fc62fdd528b8bbbb698523cac` |
| `suite/test_c2.py` (só o caminho padrão do bruto) | `04e0a4760da039a62b315e9741260083ddf7d01cd097b544e28c5ab18e17b008` | `2fb07a007ccf2f41671265b2ebdc5ff7e29f96ac89ffc29a14702f93ad839d98` |
| `suite/README.md` | `c42e20d38db2f5cdb44eae00c3c9d416a3dc5080c9f91d8b650be1d684251a5e` | `88de68e203ef2e56028fea2eafa5a9e9844860e28b8830beb9b3a3c19be90b7e` |

`test_c2_ext1/2/3.py`, `oraculo.json`, `oraculo-extensao1.json` e `gerar_smt.py` não mudaram. As extensões usam as variáveis `C2_RAW`, `C2_CSV` e `C2_ORACULO`
para redirecionar saídas.
