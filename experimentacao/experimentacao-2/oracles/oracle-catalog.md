# Catálogo de oráculos C2

Esta geração usa exclusivamente a documentação C2 literal.
Não foi utilizado LLM externo independente nem informação de C1.

| Oracle ID | Behavior ID | Classificação | Interpretação |
|---|---|---|---|
| C2-ORACLE-B001 | B001 | Indeterminado | Nenhum trecho C2 fornece uma definição suficiente. |
| C2-ORACLE-B002 | B002 | Indeterminado | Nenhum trecho C2 fornece uma definição suficiente. |
| C2-ORACLE-B003 | B003 | Indeterminado | Nenhum trecho C2 fornece uma definição suficiente. |
| C2-ORACLE-B004 | B004 | Ambiguo | Sem comando, a CLI pode apresentar instruções, mas o texto não garante o resultado. |
| C2-ORACLE-B005 | B005 | Ambiguo | O texto indica uma única fonte, mas não especifica exatamente a validação de fontes combinadas. |
| C2-ORACLE-B006 | B006 | Determinado | Opção não reconhecida resulta em erro. |
| C2-ORACLE-B007 | B007 | Ambiguo | Os operadores são listados, mas a precedência não é descrita. |
| C2-ORACLE-B008 | B008 | Ambiguo | Os operadores são listados, mas a precedência não é descrita. |
| C2-ORACLE-B009 | B009 | Ambiguo | NOT é listado sem explicar precedência ou expressões complexas. |
| C2-ORACLE-B010 | B010 | Determinado | Comparações incluem igualdade, diferença, menor e maior. |
| C2-ORACLE-B011 | B011 | Ambiguo | Expressões inválidas são mencionadas, mas a resposta exata não é definida. |
| C2-ORACLE-B012 | B012 | Determinado | Um arquivo .mcdc contém linha com identificação e expressão. |
| C2-ORACLE-B013 | B013 | Indeterminado | O comportamento de arquivo vazio não é definido. |
| C2-ORACLE-B014 | B014 | Ambiguo | JSON contém sistema, entradas e decisões, mas o esquema completo não é definido. |
| C2-ORACLE-B015 | B015 | Indeterminado | O texto não diz o que ocorre com JSON sem decisões. |
| C2-ORACLE-B016 | B016 | Indeterminado | O conteúdo do CSV de testes não é descrito. |
| C2-ORACLE-B017 | B017 | Indeterminado | O tratamento de cabeçalho inválido não é especificado. |
| C2-ORACLE-B018 | B018 | Determinado | A tabela é limitada a 20 entradas. |
| C2-ORACLE-B019 | B019 | Indeterminado | O texto não menciona entradas repetidas. |
| C2-ORACLE-B020 | B020 | Determinado | Mascaramento é o modo inicial por padrão. |
| C2-ORACLE-B021 | B021 | Determinado | Causa única existe e pode ser escolhida. |
| C2-ORACLE-B022 | B022 | Ambiguo | Z3 pode indicar combinação impossível, mas a marcação no resultado não é detalhada. |
| C2-ORACLE-B023 | B023 | Ambiguo | Uma seleção pode ser feita, mas o algoritmo guloso não é descrito. |
| C2-ORACLE-B024 | B024 | Ambiguo | A busca exata é mencionada, mas não o critério operacional completo. |
| C2-ORACLE-B025 | B025 | Ambiguo | O modo direto é limitado a 30 entradas, mas o formato da saída não é claro. |
| C2-ORACLE-B026 | B026 | Ambiguo | Fronteiras podem ser consideradas, mas os casos exatos não são descritos. |
| C2-ORACLE-B027 | B027 | Ambiguo | Mutação interna é mencionada apenas implicitamente. |
| C2-ORACLE-B028 | B028 | Determinado | Valores diferentes na mesma variável podem representar conflito. |
| C2-ORACLE-B029 | B029 | Determinado | Nenhuma decisão aplicável pode representar lacuna. |
| C2-ORACLE-B030 | B030 | Ambiguo | JSON é uma saída possível, mas os campos não são definidos. |
| C2-ORACLE-B031 | B031 | Ambiguo | CSV é uma saída possível, mas as colunas não são definidas. |
| C2-ORACLE-B032 | B032 | Ambiguo | truth-csv é possível, mas a representação não é definida. |
| C2-ORACLE-B033 | B033 | Determinado | Código 2 representa condição não coberta, divergência ou problema de verify. |
| C2-ORACLE-B034 | B034 | Determinado | Z3 necessário ausente significa que o cálculo não terminou. |
