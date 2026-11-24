# Registro de reorganização C0

Pastas realinhadas ao layout das demais LLMs (`avaliacao/`, `experimento/`, `resultados/`, `suite/`). Nenhum resultado, métrica, oráculo
ou expectativa foi alterado; os arquivos foram movidos com `git mv`.

| Antes | Depois |
|---|---|
| `resultados/RESULTADOS-C0.md` | `avaliacao/relatorio.md` |
| `resultados/resultados-por-caso.csv` | `avaliacao/resultados-por-caso.csv` |
| `resultados/{bruto,cobertura,junit-baseline.xml}` | `resultados/rodada-01-baseline/` |
| `detalhes-C0/oraculo/{oraculo.json,gerar_*.py}` | `experimento/` |
| `detalhes-C0/oraculo/analise-documental.md` | `experimento/analise-oraculo.md` |
| `detalhes-C0/oraculo/smt/` | `experimento/z3/` |
| `detalhes-C0/congelamento-{oraculo,suite}.sha256` | `experimento/congelamento/{01-oraculo,02-suite}.sha256` |
| `detalhes-C0/README.md` | `experimento/README.md` |

Ajustes de caminho (os manifestos `congelamento/*.sha256` são históricos e **não** foram editados; seus caminhos refletem o layout antigo):

| Arquivo | SHA-256 antes | SHA-256 depois |
|---|---|---|
| `suite/conftest.py` (caminhos do oráculo e do bruto) | `d708e603e02f8875a6ac3fc841f5ba6a7fd1d23f52096b215e2df71102d8954c` | `fa19312b2103857108c7f75aeef4ade49a8b2f56c42272f99b18735c3928913b` |
| `suite/README.md` | `ecceee26eb608afd018797d5f57b5a5990f3a46878736d50288c20950cbf6b1a` | `3abddb267e2d6f400a34788681a290f3408bb13aac6cef0c0138f10849a81072` |
| `experimento/gerar_oraculo.py` (diretório de saída `smt` → `z3`) | `9dab78fdd9a94b87bc32ba72a66988a4a47a145001265d65632f1291e2524174` | `86a6d151b244364f7d6c84b763196be39d2a689cc72966907511b379df48dec4` |

O `test_mcdc_c0.py` e o `oraculo.json` não mudaram (hashes dos manifestos continuam válidos).
