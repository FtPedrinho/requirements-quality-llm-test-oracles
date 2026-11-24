# Avaliação qualitativa do oráculo

A documentação da condição é a única referência normativa da expectativa.
Avaliar cada oráculo contra o trecho literal e a formalização, sem usar o
resultado do SUT ou a resposta Z3 como prova de fidelidade ao texto.

- **Conforme:** expectativa explicitamente declarada ou unicamente implicada
  pela documentação, sem conflito aplicável não resolvido.
- **Sem suporte:** expectativa depende de suposição ou regra não documentada.
- **Inválido:** caso ou formalização malformado impede avaliação válida.
- **Indeterminado:** omissão, ambiguidade ou conflito não resolvido impede
  expectativa única.

Registrar a classificação do oráculo separadamente da execução: `PASSOU`,
`FALHOU` ou `INDETERMINADO`. Erro técnico e caso inválido são registrados à
parte, não como falha semântica ou indeterminação. Um teste falho com
expectativa documental conforme indica divergência em relação à referência,
sem decidir qual fonte é objetivamente correta.

Para cada caso preservar ID, citação, regra, entrada, expectativa ou motivo
da indeterminação, fórmula, evidência Z3, resultado e eventual erro. Congelar
o oráculo antes da inspeção do SUT. Se não houver revisor independente,
registrar a autorrevisão como limitação. As métricas são somente Branch
Coverage e quantidades de testes aprovados, falhos e indeterminados.
