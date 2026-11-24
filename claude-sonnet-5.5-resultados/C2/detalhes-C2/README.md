# detalhes-C2

Evidências do experimento C2 (Claude Sonnet 5.5), derivadas **somente** do texto de
`tool-readme-C2.md` (SHA-256 `61C4062B…EFBE1`, verificado antes da leitura).

| Arquivo | Conteúdo |
|---|---|
| `analise-documental.md` | Inventário, decisões de interpretação, resumo das consultas Z3 |
| `oraculo.json` | 68 casos (50 determinados, 18 indeterminados), com entrada, pré-condição, trecho literal, regra, expectativa, justificativa e evidência Z3 |
| `gerar_oraculo.py` | Gerador do `oraculo.json` (texto-fonte → casos) |
| `gerar_smt.py` | Gerador/executor das consultas SMT-LIB com o Z3 independente |
| `smt/*.smt2`, `smt/*.out`, `smt/RESUMO.md` | Consultas SMT-LIB e respostas do Z3 5.4.1 |
| `congelamento-oraculo.sha256` | SHA-256 do oráculo, análise, geradores e consultas/respostas Z3, gravado **antes** de ler o SUT |
| `congelamento-suite.sha256` | SHA-256 da suíte e entradas, gravado antes da execução do baseline |

Revisão: autorrevisão. O Z3 não prova a fidelidade da tradução texto→fórmula.
Os arquivos de resultados estão em `../resultados/` e a suíte em `../suite/`.
