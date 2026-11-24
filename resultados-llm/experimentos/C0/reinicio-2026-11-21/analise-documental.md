# C0: análise anterior à inspeção do SUT

## Integridade contextual

A fonte normativa C0 exigida inclui, na seção "Qualidade e testes", tabelas
de resultados, nomes e descrições de suítes anteriores. Esses dados foram
expostos ao modelo ao ler a fonte integralmente, antes da geração. Também
houve exposição prévia, no contexto disponibilizado pela plataforma, a uma
nota genérica de metodologia de cobertura e a uma instrução anterior de
pesquisa. Não é possível garantir cegamento contextual integral. Os números,
nomes e descrições históricos não são usados para definir expectativas,
selecionar casos ou interpretar resultados desta rodada. Nenhuma suíte,
oráculo ou relatório anterior foi aberto ou executado. O índice de resultados
foi lido exclusivamente para permitir sua atualização solicitada, não como
fonte normativa.

Fonte exclusiva: `documentacao-original/tool-readme-original.md`, SHA-256
`72B827BDEE6CE859527765CFF574A473519C00A1AF9AA9F3AACCE4236A4995F8`.
Prompt operacional: `prompts/geracao-de-oraculos-v2.md`, SHA-256
`A89A9F10E579B0189AB83CD845A42764637AB6754BD28D2E567D8D6A6B401E3F`.
Metodologia: `protocolo/metodologia.md`, SHA-256
`10FC0B6BBA977B514065511DEBB075FAC1FA42FB7EA5072EA2B3BC619B1F3CB7`.
Somente a primeira é fonte normativa de comportamento.

## Inventário documental

| ID | Seção | Trecho literal | Comportamento e limites |
|---|---|---|---|
| R1 | O que a ferramenta faz | "Tabela verdade, pares de independência, suíte de testes e o par que demonstra cada condição" | `analyze` produz tabela e pares; não determina ordem nem representação das linhas. |
| R2 | Como funciona | "tabela verdade: as 2ⁿ combinações das entradas e a saída de cada uma" | Uma linha por valoração booleana, resultado da expressão. |
| R3 | Uso / Operadores | "e ... `and`, `&&`, `/\`"; "ou ... `or`, `\|\|`, `\/`"; "não ... `not`, `!`" | Conjunção, disjunção e negação nas grafias documentadas. |
| R4 | O que a ferramenta faz | "mascaramento (padrão) e causa única (`--unique-cause`)" | Variantes preservam o valor da expressão. |
| R5 | O que a ferramenta faz | "Cada aparição de uma entrada na expressão conta como uma condição" | Repetições representam a mesma entrada, mas condições distintas. |
| R6 | Uso / Código de saída | "`0` tudo certo; `1` entrada inválida; `2` alguma condição sem par" | Erro sintático inequívoco resulta em 1; condição sem par resulta em 2. |
| R7 | Saídas | "`truth-csv` ... A tabela verdade inteira, com as combinações impossíveis marcadas" | Formato contém tabela inteira; nomes e ordem de colunas não são especificados. |
| R8 | Uso | "`--constraint` ... Restrição entre condições escrita à mão (só com expressão direta)" | Restrição pode excluir combinações; formato exato de marcação não é definido. |
| R9 | Uso | "`--z3` ... combinações impossíveis e ... valores concretos"; "`--boundary` ... variantes de fronteira" | Viabilidade e fronteiras; detalhes de seleção/ordem são parcialmente omitidos. |
| R10 | Uso | "`--exact` ... a menor possível"; "`--direct` ... até 30 entradas" | Otimização exata e busca direta; conteúdo e desempate não especificados. |
| R11 | Formatos de entrada | "um requisito por linha, `ID: expressão`. Linhas com `#` são comentários" | Arquivo de requisitos; identificadores e comentários. |
| R12 | Formatos de entrada | "variáveis com tipo e as decisões com a guarda e as ações" | Fonte JSON NAT2TEST; `_antes` para passo anterior. |
| R13 | Formatos de entrada | "uma linha por teste e entrada ... `decision` e `expected_outcome` são opcionais" | `check` lê CSV; cobertura e divergências são reportadas. |
| R14 | Uso | "`verify` ... Conflitos ... e lacunas"; "`--context` ... sempre alguma guarda vale" | Verificação de conflitos e lacunas. |
| R15 | Uso | "`--format` ... `text` ... `json`, `csv` ... `truth-csv`"; "`-o` ... arquivo" | Formatos e destino; a estrutura exata não é integralmente especificada. |
| R16 | Limites conhecidos | "20 entradas com a tabela inteira ... 12 com o Z3 linha a linha e 30 no modo direto; até 1000 pares guardados por condição" | Limites declarados, sem mensagem de erro ou tratamento de todas as fronteiras. |

O documento descreve os comandos e muitas regras, exemplos e limites, mas não
especifica exaustivamente esquemas de saída, diagnóstico de entradas malformadas,
desempates ou todas as interações de opções. Essas omissões limitam os
oráculos; não se atribui a C0 um nível automático de clareza ou consistência.
Não foi identificado conflito aplicável aos casos deste baseline. A
correspondência texto-fórmula foi autoavaliada, sem revisor independente.

## Formalização e busca

Para cada expressão booleana `e`, a tabela tem exatamente uma linha para cada
valoração dos nomes de entrada e saída `e(v)` (R2). `and` é conjunção, `or`
disjunção, `not` negação (R3); formas alternativas preservam essa semântica.
Identificadores repetidos usam o mesmo valor (R5). Alterar a variante MC/DC não
altera a função booleana (R4). Um erro sintático inequivocamente inválido tem
código 1 (R6). `A or not A` é tautologia, portanto nenhuma condição pode
alterar a saída, logo não há par e o código é 2 (R6; definição de pares em
Como funciona).

`gerar-oraculos.py` usa exclusivamente Python e z3-solver independente: para
cada valoração, fixa cada variável booleana, consulta a fórmula e sua negação,
registra SMT-LIB, ambos os resultados e a testemunha. Apenas `sat`/`unsat`
complementares produzem expectativa. O objetivo é enumeração exaustiva das
valorações de cada expressão selecionada, não minimização de suíte nem busca
global; parada após todas as valorações. Z3 valida a fórmula, não a tradução.
Nenhuma otimização global ou cobertura máxima é alegada.

Os casos congelados cobrem saídas verdadeiras e falsas, operadores, grafias,
aninhamento, entradas repetidas e variante causa única, além de dois códigos
de saída. Casos específicos de Z3 integrado, fronteiras, exatidão, restrições,
arquivos, JSON, `check`, `verify` e mensagens permanecem não cobertos no
baseline; não se inventa sua saída. Formatos precisos, ordem de tabela e
mensagens textuais são indeterminados: o harness deve apenas adaptar a leitura
da saída, sem introduzir expectativas sobre essas representações.

Pré-condições: Java 21, classes compiladas e execução do comando `analyze`.
O escopo de cobertura proposto inclui os quatro módulos Java documentados,
inclusive classes não carregadas; classes de testes não entram no denominador.
Os caminhos e branches concretos serão mapeados depois do congelamento.
