# Extensão 2 — regras documentais já congeladas

Após a extensão 1 permanecem branches sem teste no verificador Z3, codificação e modelo de ações. O inventário original congelou R07 (combinações impossíveis), R11 (conflito e lacuna) e R19 (Z3). Esta rodada instancia essas regras gerais: conflitos exigem guardas simultâneas e atribuições diferentes à mesma variável; lacunas são verificadas em contexto explicitamente fornecido; comparações numéricas têm combinações satisfatíveis ou impossíveis.

`preparar.py` formaliza cada instância e executa Z3 independente antes de congelar e executar a extensão. As expectativas são derivadas das regras documentais e fórmulas, não de resultados do SUT. O adapter usa `Decision`, `DecisionSet`, `Z3RequirementsVerifier`, `TruthTable` e `Z3FeasibilityChecker` para chegar aos mesmos comportamentos; entradas e asserções são congeladas antes de usar esses pontos de entrada.

Ramos de ações malformadas, formatos de relatório não especificados, respostas inesperadas do solver e classes de mutação continuam sem asserção semântica. Alguns podem ser documentados, mas não foram mapeados integralmente. Nenhum algoritmo de mutação é invocado.
