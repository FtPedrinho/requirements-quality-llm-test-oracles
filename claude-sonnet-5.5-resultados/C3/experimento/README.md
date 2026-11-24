# Experimento C3 — oráculo e Z3

- `oraculo.json`: 72 casos (40 determinados, 32 indeterminados), com entrada, trecho literal, regra, expectativa e justificativa.
- `analise-oraculo.md`: inventário, contradições do texto, decisões e limitações (autorrevisão).
- `gerar_oraculo.py`: gera `oraculo.json` e `z3/*.smt2`. `rodar_z3.py`: executa o Z3 5.4.1 independente e grava `z3/*.out` e `z3/RESUMO.tsv`.
- `z3/`: 122 consultas SMT-LIB e respostas.
- `congelamento/`: SHA-256 do oráculo (`01`), da suíte (`02`) e dos resultados do baseline (`03`).

Fonte: `tool-readme-C3.md` (SHA-256 `F18B0821…B87A3`, conferido). O oráculo foi congelado antes de qualquer leitura do SUT.
