# Experimento C3 — alta clareza e baixa consistência

## Objetivo, condição e metodologia

Avaliar a geração de oráculos a partir de documentação legível, mas internamente contraditória. A análise documental foi congelada antes dos testes: registrou 10 contradições/tensões e 4 pares aparentemente compatíveis, sem consultar implementação ou gabarito para escolher qual lado deveria prevalecer.

S1 contém expectativas derivadas das afirmações documentais; S2 contém candidatos complementares; S3 é a combinação. Contradições foram mantidas, e casos sem oráculo defensável ficaram desabilitados em vez de receberem um resultado inventado. As suítes executam contra a implementação Java real, sem modificá-la.

## Métricas utilizadas

Somente: cobertura de requisitos, Mutation Score, Precision, Recall e F1-score, avaliados contra a cópia congelada do gabarito independente C2 de 19 comportamentos. A clareza foi caracterizada qualitativamente; não foi registrada uma nota numérica diretamente comparável à escala de C1/C2.

## Artefatos essenciais

- Resultados: [results.md](results.md).
- Documento C3 adaptado: [documentation/EXP3.md](documentation/EXP3.md).
- Suíte Copilot S1/S2/S3: [tests/](tests/).
- Gabarito congelado: [oracle-reference/](oracle-reference/).

## Proveniência

Os testes complementares foram gerados pelo agente Copilot desta sessão. Não há registro de outro modelo externo. O registro do processo está em [tests/test-generation.md](tests/test-generation.md), separado da documentação adaptada e dos resultados.
