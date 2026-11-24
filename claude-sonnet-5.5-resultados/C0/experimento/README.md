# Detalhes do experimento C0 (Claude Sonnet 5.5)

| Item | Onde |
|---|---|
| Análise documental, regras de observação, casos e justificativas | `analise-oraculo.md` |
| Oráculo estruturado (94 casos: 72 determinados, 22 indeterminados) | `oraculo.json` |
| Gerador do oráculo (força bruta + Z3) e da análise | `gerar_oraculo.py`, `gerar_analise.py` |
| Consultas SMT-LIB (107) e respostas do Z3 | `z3/*.smt2`, `z3/resultados-z3.json` |
| Congelamento do oráculo (SHA-256, antes de ler o SUT) | `congelamento/01-oraculo.sha256` |
| Congelamento da suíte (SHA-256, antes da execução) | `congelamento/02-suite.sha256` |
| Resultados, cobertura e avaliação | `../resultados/`, `../avaliacao/` |

## Identificação

- Fonte C0: `experimentacao-pesquisa/documentacao-original/tool-readme-original.md`, SHA-256 `72b827bdee6ce859527765cff574a473519c00a1af9aa9f3aacce4236a4995f8` (conferido).
- Commit de referência: `5d40d5a31ad473719b4e0553344e64524610884e` (árvore limpa no início).
- Z3: `Z3 version 5.4.1 - 64 bit` (pacote `z3-solver`; executável independente do `mcdc-z3`). Sem `unknown` nem timeout.
- Revisão do oráculo: autorrevisão.

## Ordem cronológica

1. Verificação do hash e leitura integral da fonte C0.
2. Oráculo, Z3 e conferência por força bruta; congelamento por SHA-256 (2026-11-24 20:06Z). Só depois o SUT foi inspecionado (`mcdc`, classpath e uma execução de teste do launcher).
3. Suíte escrita e congelada (20:07Z); execução única do baseline com JaCoCo; relatório de cobertura.

## SHA-256 dos binários do SUT usados

- `mcdc-core-0.1.0-SNAPSHOT.jar` `a33cbcb1ca2b3eb9e86cb55f7838332231d46e6c718b5df037c00a1442cb5896`
- `mcdc-requirements-0.1.0-SNAPSHOT.jar` `049e67312f202bdb293dbf7811b030149603f31b64cd07f4edd026750629845e`
- `mcdc-z3-0.1.0-SNAPSHOT.jar` `1645ea39462ccee92f229997e178639cfbb4a0180e1a2f92d7726305c22ce92e`
- `mcdc-cli/target/classes` (hash agregado das classes) `f24162bca9a72193b3f452f5cd20ad01ba5750774637215d7d77a625ce499d71`
- JaCoCo agent `37ae2f374ad77e85c59c6e5b46565226c3ac3cb460ac19de0bcb844ac2f43e33`
- JaCoCo CLI `1f2a806225623fbd9f53d1ee0e42a6975323de0adebe01c12fc464ed147d756a`
- `resultados/rodada-01-baseline/cobertura/jacoco.exec` `32b7065ab86891ae736cef3cfc15acbbce436c2214b8353c1f0dda48d8896a36`
