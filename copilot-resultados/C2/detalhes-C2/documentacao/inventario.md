# Inventário da fonte C2 completa

Fonte: `tool-readme-C2.md`, hash registrado em `metadados/preparacao.md`. A fonte contém texto técnico e histórico; números e resultados de execuções antigas não são usados como referência. A ortografia degradada e exemplos com campos incompletos limitam a clareza.

| ID | Linhas | Citação literal | Regra ou lacuna |
|---|---:|---|---|
| R01 | 3, 273–277 | "monta  tabela-verdade"; "para  entradas distintas  expressão, são consideradas  2ⁿ combinações  calculado  resultado da guada em cada" | Tabela por variáveis distintas, com resultado da guarda. |
| R02 | 129–137 | "`and`, `&&`, `/\`"; "`or`, `\|\|`, `\/`"; "`not`, `!`" | Formas de conectivos booleanos; precedência sem parênteses é descrita de modo degradado em outra seção e não será assumida quando ambígua. |
| R03 | 55 | "entrada é  variavel dstinta  expresão; condição é cada ocorencia   entrada  expressão"; "`(A and B) or (not A and C)`, há 3 entrads dstitas" | Ocorrências repetidas são condições distintas; exemplo nomeia quatro condições. |
| R04 | 49–55, 279 | "duas variants  MC/DC  supordas: **mascaramento** (pdrão) e **causa úica** (`--unique-cause`)"; "essa conição muda,  resultado  decisão  muda" | Existência de par exige mudança de condição e de decisão; não inferir detalhes de mascaramento ausentes. |
| R05 | 281 | "em caso  empate, prioriza caua únca"; "`--exact`,  Z   3 pocura  suíte de tamanho mnimo" | Seleção gulosa e exata; ordem total de empate não especificada. |
| R06 | 283 | "é classificada  redundante"; "classificada como bloqueada" | Sem par mesmo sem restrição: redundante; pares perdidos por combinações impossíveis: bloqueada. |
| R07 | 39, 105 | "Combinaçoes impossiveis descrtadas  valoes concretos"; "acim  12 entradas, passa soznho  modo dreto" | Viabilidade por solver e comutação automática; saídas textuais detalhadas não especificadas. |
| R08 | 41, 109 | "`speed > 100` → 100  101"; "`--boundary` ... acrsenta variants  frnteira" | Exemplo de fronteira; tipos e formato de representação não são globais. |
| R09 | 43–45, 107–109 | "`menro possivel, esclhida pelo Z3`"; "Paes pedds dreto  Z   3,  mnar a tabela ( 30 entradas)" | Suíte exata mínima e modo direto. |
| R10 | 103 | "`--constraint \"<expr>\"` ... Rtrição etre condições ... (  expressão dreta)" | Restrição sobre expressão direta. |
| R11 | 51, 113 | "Confltos (dois requistos valem jtos  escrvem valoes diferetes) e lacunas (nnum requisito vale)"; "`--context` ... smre algma guarda vale" | Verify, lacuna e conflito em contexto; caso sem ações não implica conflito. |
| R12 | 49, 187–193 | "Cobertura MC/DC  um cnjunto  testes"; "As colunas `decision`  `expected_outcome` são opcionis" | Check e entrada CSV; exemplo literal do cabeçalho contém `vlue`, grafia potencialmente ambígua, não substituí-la silenciosamente por outro schema. |
| R13 | 139 | "`0`: comndo concluido ... `1`: entraa invalida; `2`: resutado vido  processamto" | Código 2: analyze sem par, check sem demonstração ou expectativa divergente, verify conflito ou lacuna. |
| R14 | 143–151 | "um requisito  linha, `ID: expressão`. Lnhas com `#`  comentrios" | Formato `.mcdc`. |
| R15 | 153–185 | "cotm  variavis  seus tips, alem das decisões,     guarda   ações"; "sixo `_antes`" | JSON de entrada; exemplo apresenta campo `gard` e valor de ação possivelmente truncado. Não escolher schema ou correção por código. |
| R16 | 115–117, 195–207 | "`text` (pdrão), `json`, `csv` (suíte)  `truth-csv` (tabela-verdade intea)"; "Grava  relatorio  arqivo" | Formatos e saída em arquivo; detalhes de schema e ordenação parcialmente ausentes. |
| R17 | 585–587 | "20 entrdas   taela-verdade cmpleta"; "12  o Z3 linha a linha  30 no modo dreto"; "1000 pares guardads por condição" | Limites por modo; não assumir mensagem exata em excesso. |
| R18 | 591–593 | "a fnção de paridde  3 entrdas exige 8 testes"; "feraemta analsa  paso isoldo" | Paridade e limitação temporal; formato exato de expressão de paridade não é fornecido. |
| R19 | 57–73, 309–312 | "necessarios **JDK 21**"; "`z3` estja disponvel  `PATH`"; "chamda  prcesso tem lmite  60 segunds" | Dependências documentadas; aviso por ausência de Z3, sem texto fixado. |
| R20 | 295–312 | "`mcdc-core`"; "`mcdc-requirements`"; "`mcdc-z3`"; "`mcdc-cli`" | Escopo de produção de quatro módulos. |
| R21 | 211–272 | "`speed > 100`"; "`--unique-caue`"; "`--mutaion`" | Exemplos apresentam erros gráficos em comandos; não tratar erros como opções válidas. A funcionalidade de mutação não será testada por determinação do usuário. |
| R22 | 313–584 | "Qualidde e testes"; "Testes recomendads, ainda não autmatizados" | Seção examinada, mas testes e resultados históricos ali descritos não são gabarito. Os requisitos funcionais foram extraídos das definições técnicas e exemplos normativos, sem usar desempenhos registrados. |

Conflitos/ambiguidades a registrar: grafia degradada dos operadores e comandos; esquema JSON de exemplo e campo de CSV com possíveis erros; ordem e esquema detalhados das saídas; semântica exata de tipos ou mensagens em casos não explicitados. Nenhuma inconsistência global foi demonstrada; os níveis baixa clareza e alta consistência são pretendidos, não presumidos. Nenhuma regra histórica de desempenho é adotada como verdade.
