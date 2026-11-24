# experimento — evidências do experimento C1 (Claude Sonnet 5.5)

| Arquivo | Conteúdo |
|---|---|
| `analise-oraculo.md` | Inventário, regras de decisão e tensões do texto C1 |
| `oraculo.json` | 72 casos (57 determinados, 15 indeterminados), trechos literais, expectativas, fixtures |
| `z3/gerar_smt.py` | Gerador/executor das consultas SMT-LIB (Z3 5.4.1, independente do SUT) |
| `z3/smt/` | Consultas `.smt2` e respostas `.out` do Z3 |
| `congelamento/01-oraculo.sha256` | Hashes de análise, oráculo, script e Z3 — antes de ler o SUT (autorrevisão) |
| `congelamento/02-suite.sha256` | Hashes da suíte baseline e do oráculo — antes da execução |
| `congelamento/03-extensao.sha256` | Hash da extensão E1 — antes da execução |

Ordem seguida: (1) hash da fonte; (2) leitura de C1 e oráculo; (3) SMT-LIB + Z3; (4) congelamento; (5) inspeção da CLI só para invocar; (6) suíte; (7) congelamento; (8) baseline único com JaCoCo; (9) extensão E1; (10) relatório.

Comandos (PowerShell, raiz do repositório; ajustar `<exec>`):

```powershell
python -I claude-sonnet-5.5-resultados/C1/experimento/z3/gerar_smt.py "C:\Users\User\AppData\Roaming\Python\bin\z3.exe"
$env:JAVA_TOOL_OPTIONS="-javaagent:$HOME\.m2\repository\org\jacoco\org.jacoco.agent\0.8.16\org.jacoco.agent-0.8.16-runtime.jar=destfile=<exec>,append=true"
python -m pytest claude-sonnet-5.5-resultados/C1/suite -p no:cacheprovider --junitxml=<junit.xml>
```

Relatório JaCoCo: `org.jacoco.cli-0.8.16-nodeps.jar report <exec> --classfiles` dos JARs `mcdc-core`, `mcdc-requirements`, `mcdc-z3` (`target/`) e `mcdc-cli/target/classes`.
