# C1 — análise documental anterior à inspeção do SUT

Fonte exclusiva: `experimentacao\experimentacao-1\documentation\tool-readme-C1.md`,
SHA-256 `91981FA0181E5CC1BC5A67DAAFC965BB82D6F8EB0A6D47EB58CE291A3EF5D33B`.
O pesquisador substituiu a fonte inicialmente indicada; o protocolo foi
alterado antes desta análise. A fonte inclui resultados e descrições de testes
históricos, aos quais houve exposição na leitura integral. Eles não são usados
como gabarito; o cegamento integral não é alegado.

## Inventário e rastreabilidade

| ID | Seção, citação literal | Regra e possibilidades documentadas |
|---|---|---|
| R01 | O que a ferramenta faz: “Tabela verdade, pares de independência, suíte de testes e o par que demonstra cada condição” | analyze deve produzir estes componentes. |
| R02 | Como funciona: “para as entradas distintas da expressão, são consideradas as 2ⁿ combinações e calculado o resultado da guarda em cada uma” | Para n entradas distintas, todos os 2^n vetores e resultados lógicos. |
| R03 | Como funciona: “dois testes possíveis nos quais essa condição muda, o resultado da decisão também muda” | Todo par relatado deve alternar a condição e a decisão; não supor que isto seja sozinho suficiente para mascaramento. |
| R04 | O que a ferramenta faz: “mascaramento (padrão) e causa única (`--unique-cause`)” | As duas variantes são opções. Não há nesta frase definição completa de mascaramento. |
| R05 | Uso: “`and`, `&&`, `/\`”; “`or`, `\|\|`, `\/`”; “`not`, `!`” | Cada grafia denota, respectivamente, conjunção, disjunção ou negação. |
| R06 | Uso: “`=`, `==`, `!=`, `<`, `<=`, `>`, `>=`” | Operadores relacionais aceitos; as expectativas numéricas aqui usam matemática inteira ordinária. |
| R07 | Uso: “`--constraint ...` Restrição entre condições escrita à mão (só com expressão direta)” e Como funciona: “combinações impossíveis ... não participam da análise” | Uma restrição explícita seleciona vetores elegíveis; o formato exato de apresentação não é especificado. |
| R08 | Como funciona: “se uma condição não possui par mesmo considerando todas as combinações, é classificada como redundante; se deixa de possuir pares por causa das combinações impossíveis, é classificada como bloqueada” | Distinguir redundância de bloqueio; ocorrências repetidas exigem cuidado. |
| R09 | O que a ferramenta faz: “`--z3` ... Combinações impossíveis descartadas e valores concretos para cada teste”; “`--z3 --boundary` ... (`speed > 100` → 100 e 101)” | Predicados numéricos devem ser simultaneamente viáveis; verificar testemunhos e fronteira explícita. |
| R10 | Uso: “`--exact` ... a menor possível”; “`--direct` ... sem montar a tabela (até 30 entradas)” | Exatidão é tamanho mínimo para a regra de pares aplicável; limites documentados. |
| R11 | Uso: “`text` (padrão), `json`, `csv` (suíte) ou `truth-csv` (tabela-verdade inteira); `check` e `verify` aceitam `text` e `json`” | Formatos aceitos; nomes de campos e mensagens exatos não especificados. |
| R12 | Uso: “`-o <arquivo>` ... Grava o relatório no arquivo em vez de mostrar na tela” | Arquivo solicitado deve receber relatório. |
| R13 | Formatos de entrada: “um requisito por linha, `ID: expressão`. Linhas com `#` são comentários.” | Arquivo pode ter múltiplas decisões identificadas e comentário. |
| R14 | Formatos de entrada: “contém as variáveis e seus tipos, além das decisões, cada uma com sua guarda e suas ações”; “sufixo `_antes`” | Entrada JSON conforme exemplo; sem inventar esquema adicional. |
| R15 | Formatos de entrada: “cada linha associa um teste a uma entrada e ao valor atribuído a essa entrada”; “`decision` e `expected_outcome` são opcionais” | CSV de check aceita entrada por linha; distinção e resultado esperado opcional. |
| R16 | Uso: “`0`: comando concluído ...; `1`: entrada inválida; `2`: ... condição sem par no `analyze`, ... condição não demonstrada ou um resultado esperado divergente no `check`, ou um conflito ou uma lacuna no `verify`” | Códigos, com contexto de cada comando. Falta de detalhes do formato da mensagem não cria expectativa textual. |
| R17 | O que a ferramenta faz: “Conflitos (dois requisitos valem juntos e escrevem valores diferentes) e lacunas (nenhum requisito vale)” e Uso: “`--context ...` ... nessa situação, sempre alguma guarda vale” | Conflito requer guardas simultâneas e ações divergentes na mesma variável; lacuna requer contexto e nenhuma guarda. |
| R18 | Instalação: “As opções que exigem o Z3 avisam quando o executável não está instalado.” | Aviso na ausência; mensagem e código específicos não são fixados por essa frase. |
| R19 | Como funciona: “até 20 entradas com a tabela-verdade completa, 12 entradas no processamento com Z3 linha a linha e 30 entradas no modo direto.” | Limites; não supor mensagem ou tempo ao exceder. |
| R20 | O que a ferramenta faz: “uma mesma variável pode corresponder a mais de uma condição” | Ocorrências repetidas distintas; não deduzir pares de mascaramento apenas de número de variáveis. |
| R21 | Como funciona: “estratégia gulosa considera primeiro as condições com menos pares ... menos testes ... empate, prioriza causa única.” | Critério de seleção; desempates adicionais não especificados. |
| R22 | Saídas: “`truth-csv` ... tabela-verdade inteira, com as combinações impossíveis marcadas”; “`csv` ... uma linha por teste e entrada” | Conteúdo dos dois formatos; grafia e ordenação dos campos não fixadas. |

O documento descreve também mutação, análises históricas, testes existentes,
instalação, desempenho, arquitetura, limites e relatórios. Estes constituem
inventário de funcionalidades, não são resultados desta rodada. Não executar
análise de mutação nem coletar sua métrica. Evidência observada para clareza:
comandos, exemplos, limites, operadores e códigos estão explicitados; faltam
esquemas completos dos relatórios, sintaxe completa e detalhes de certos erros.
Consistência: não foi comprovada globalmente; no subconjunto formalizado não
foi identificado conflito. Nenhum rótulo global é presumido.

## Semântica e conjunto de casos congelados

Todas as expectativas abaixo são `CONFORME À DOCUMENTAÇÃO`, interpretações
matemáticas de R01–R22. A evidência de Z3 é gerada independentemente por
`formalizacao.py`; o arquivo de resultados e as fórmulas são congelados antes da
inspeção do SUT. A ordem de linhas, nomes de campos, escolha de uma suíte
gulosa específica e mensagens textuais não são expectativas. Z3 valida apenas
as fórmulas, não a fidelidade da tradução documental.

| ID | Entrada e pré-condição | Resultado esperado / objetivo | Referências |
|---|---|---|---|
| B01 | `A` | tabela `{F→F,T→T}`, par F/T, suíte contém ambos, código 0 | R01–R03,R16 |
| B02 | `not A` | tabela `{F→T,T→F}`, par F/T, código 0 | R02,R03,R05,R16 |
| B03 | `A and B` | quatro vetores, saída `A∧B`, pares e demonstração de A e B, código 0 | R01–R03,R05,R16 |
| B04 | `A or B` | quatro vetores, saída `A∨B`, pares e demonstração de A e B, código 0 | R01–R03,R05,R16 |
| B05 | `(A and B) or C` | oito vetores com `(A∧B)∨C`, cada condição demonstrada, código 0 | R01–R03,R05,R16 |
| B06 | B05 com `--unique-cause` | mesmo resultado lógico; três condições demonstradas por pares de causa única | R02,R04,R05 |
| B07–B12 | `A && B`, `A /\ B`, `A || B`, `A \/ B`, `! A`, `not A` | tabela da operação correspondente, mesmo que B03/B04/B02 | R02,R05 |
| B13 | `A and` | entrada inválida; código 1 | R05,R16 |
| B14 | B03 com `--format json` | JSON válido com resultado de decisão; código 0 | R11,R16 |
| B15 | B03 com `--format csv` | CSV de suíte contém uma linha por teste e entrada; código 0 | R11,R22,R16 |
| B16 | B03 com `--format truth-csv` | CSV representa quatro combinações e suas saídas; código 0 | R02,R11,R22,R16 |
| B17 | B03 com `-o` e caminho novo | relatório gravado no arquivo solicitado, não na saída normal | R12 |
| B18 | arquivo `.mcdc` com comentário e duas linhas `R1: A`, `R2: B` | duas decisões identificadas e processadas, código 0 | R13,R16 |
| B19 | `A`, check com CSV dois testes F e T com expected F e T | condição demonstrada e expectativas corretas, código 0 | R03,R15,R16 |
| B20 | B19, inverter resultado esperado de um teste | resultado esperado divergente detectado, código 2 | R15,R16 |
| B21 | B19, apenas teste T | condição não demonstrada, código 2 | R03,R15,R16 |
| B22 | `A and B`, restrição `not A or B` | vetor A=T,B=F é inelegível; A=F,B=F é elegível | R07 |
| B23 | `speed > 100 or speed > 50`, `--z3 --boundary` | combinação primeiro verdadeiro e segundo falso impossível; valores 100 e 101 ocorrem como fronteiras de `speed > 100` | R06,R09 |
| B24 | B05 com `--exact` | suíte de quatro testes; existência e impossibilidade de três são verificadas em Z3 para pares de causa única; quatro também é limite inferior para três condições distintas | R03,R10 |
| B25 | B05 com `--direct` | condições demonstradas e saída lógica correta em testes fornecidos | R03,R10 |
| B26 | JSON com duas guardas A e ações `x := 0`, `x := 1`, verify | conflito: guardas simultaneamente verdadeiras e atribuições diferentes, código 2 | R14,R16,R17 |
| B27 | JSON com uma guarda A, verify com contexto `not A` | lacuna no contexto, código 2 | R14,R16,R17 |
| B28 | `(A and B) or (not A and C)` | três entradas distintas e quatro ocorrências de condição | R20 |
| B29 | `A or (A and B)` | B é redundante, pois trocar B jamais muda decisão para A fixo; código 2 | R08,R16 |
| B30 | `A and B`, restrição `A` | A bloqueada, pois todas as combinações viáveis têm A verdadeiro; código 2 | R07,R08,R16 |
| B31 | ausência de executável Z3 no PATH, analyze com `--z3` | aviso de indisponibilidade, sem exigir código ou texto exatos | R18 |

Os casos B23–B27 dependem do executável Z3 do SUT; solver Python independente
serve exclusivamente para gerar evidências, não para substituir o processo do
SUT. Entrada de JSON e CSV deve seguir os exemplos R14/R15; nomes de campos e
resultados não documentados não serão assumidos. Precondições de arquivos
temporários: caminhos novos no subdiretório desta rodada.

## Indeterminações e limites

- I01 — `INDETERMINADO — OMISSÃO`: esquema exato e ordem do JSON ou dos CSVs,
  texto das mensagens e nomes de arquivos padrão não são inteiramente definidos.
- I02 — `INDETERMINADO — OMISSÃO`: resultado exato de entrada malformada
  específica não claramente recusada pelo texto, especialmente argumentos
  conflitantes e opções repetidas.
- I03 — `INDETERMINADO — OMISSÃO`: desempate guloso além da preferência
  documentada, a suíte específica dentre várias mínimas e a ordem de pares.
- I04 — `INDETERMINADO — OMISSÃO`: tratamento de limites excedidos, ausência
  do Z3 e erros de processo além do aviso documentado.
- I05 — `INDETERMINADO — AMBIGUIDADE`: definição completa de mascaramento
  e pares para ocorrências repetidas não é fornecida pelas citações acima.

I01–I05 registram lacunas gerais, não são testes executáveis nem aumentam a
contagem de casos gerados. O arquivo `formalizacao.py` registra fórmulas,
objetivos e testemunhas; a enumeração booleana é exaustiva apenas no universo
de até três variáveis selecionado, e a otimização apenas para B24. Não se
afirma otimização global da suíte ou cobertura estrutural máxima.
