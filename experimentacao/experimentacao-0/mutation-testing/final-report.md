# Avaliação final da Experimentação 0

## Resultado quantitativo

Os artefatos resultaram em:

- 981 mutantes;
- 21 equivalentes;
- 894 mortos;
- 42 sobreviventes;
- 24 não determinados por problemas de formalização;
- 24 não avaliáveis no registro final;
- Mutation Score de 93,125%;
- Precision de 1,000;
- Recall de 0,955;
- F1-score de 0,977.

Os 152 casos originais foram preservados. Doze pares MC/DC não produziram modelos concretos e ficaram não avaliáveis.

## Respostas às questões

1. **Os oráculos detectam comportamentos incorretos?**
   Na maior parte dos mutantes não equivalentes, sim: 894 dos 960 mutantes não equivalentes foram mortos.

2. **A suíte mata mutantes relevantes?**
   O resultado agregado é alto dentro do conjunto artificial de mutantes, mas não demonstra capacidade contra defeitos reais.

3. **Existem falsos positivos?**
   Não foram encontrados falsos positivos contra o comportamento original ou entre mutantes equivalentes mortos.

4. **Precision, recall e F1 indicam qualidade satisfatória?**
   Precision 1,000 e F1 0,977 são elevados no escopo avaliado. Recall 0,955 indica 42 defeitos sintéticos sobreviventes.

5. **Há diferenças entre oráculos?**
   Sim. Alguns oráculos atingiram 100%, enquanto VM REQ002-REQ004 e TIS REQ002-REQ004 apresentaram mutantes sobreviventes ou equivalentes.

6. **Principais limitações?**
   Ausência de implementação independente, 12 pares não concretizados, domínios parcialmente representados e dependência da tradução Z3.

7. **Linha de base confiável?**
   É útil como baseline formal exploratória, mas não como evidência definitiva de qualidade semântica ou eficácia contra defeitos reais.

## Operadores

Mutantes de operador relacional, constantes e remoção de condição são os principais responsáveis pelos sobreviventes. Alterações AND/OR, negações e muitas remoções foram efetivamente detectadas pela suíte.

## Conclusão

**ADEQUADA COM RESSALVAS**

Os resultados fornecem evidência suficiente de que os oráculos possuem boa capacidade de distinguir muitos comportamentos mutados dentro das formalizações. Porém, os 42 sobreviventes, os 24 casos não determinados, os 12 pares não concretizados e a ausência de implementação independente impedem uma conclusão forte sobre correção semântica ou Mutation Score de sistemas reais.
