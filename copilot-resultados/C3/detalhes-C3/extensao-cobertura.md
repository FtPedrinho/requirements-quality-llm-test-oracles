# Extensão orientada por cobertura

O relatório acumulado apontou branches ainda não cobertos em `Main`, `TextReport`, `IndependencePairs` e `RequirementsFile`. Esta rodada recombina apenas os oráculos concretos já congelados: T01–T11 com `--unique-cause` e relatório textual; T09–T11 com relatório textual padrão; F01 com `--unique-cause`; e F02 com destino em arquivo, reutilizando a propriedade de saída de F03. O mesmo resultado de tabela de cada T é comparado com a respectiva tabela congelada. Não se julgam pares, cobertura MC/DC, condições repetidas ou códigos de saída.

Os formatos e variantes são opções documentadas no inventário D17 e D19; a tabela da guarda é D02. A observação de branches apenas selecionou as invocações, não produziu expectativa. A leitura textual usa os nomes das colunas e T/F para recuperar a tabela que o teste compara ao oráculo existente.

Branches associados à mutação permanecem no denominador e não serão executados. Os caminhos `mcdc-z3`, `check`, `verify`, formatos CSV e comparações têm comportamentos documentados ou conflitos no inventário, mas não dispõem de expectativas concretas congeladas aplicáveis nesta tentativa. Não serão criados oráculos retrospectivos nem expectativas inferidas do código. As ambiguidades I01–I15 continuam registradas no inventário, sem convertê-las artificialmente em casos executáveis.
