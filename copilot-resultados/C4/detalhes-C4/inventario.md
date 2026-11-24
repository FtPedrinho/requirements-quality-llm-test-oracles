# C4: inventário e análise anterior ao SUT

Fonte exclusiva: `experimentacao/experimentacao-4/tool-readme-C4.md`,
SHA-256 `D6BC0A588CD9A7DF7F1F566573944FA5CB1707BBA676B4E9854CAD2CC5440FC2`.
O arquivo começa no meio de uma frase. As referências a seguir são linhas
desse arquivo, com transcrição literal, inclusive erros.

| ID | Linhas e trecho literal | Tratamento |
|---|---|---|
| I01 | 3, 5: "`csv`|  suíte:  linha teste entrada" / "`truth-csv`|  tablea-verdade inteia" | Conflito com I02; formato de tabela indeterminado. |
| I02 | 7: "`truth-csv`contém soemnte [trecho omitido] inependência, nunca tabela-verdade.  tabela-verdade comoopleta é exporada exclusivamente  `csv`, coném testets gerados." | Conflito com I01; conteúdo exato também omitido. |
| I03 | 15, 19: "mascaramo (padrão)  cusa única" / "`--unique-cause`" | Duas variantes; exemplo tem expressão incompleta. |
| I04 | 23: "`speed > 100 /\ mode = idle`" | Exemplo de comparações; saída concreta não especificada. |
| I05 | 25: "entrada repetida: cada aparição é  condiç  par próprio (#1, #2)" | Uma condição por aparição; exemplo seguinte está incompleto. |
| I06 | 29–31: "implica B = speed > 50" / "`--constraint`" | Exemplo de restrição incompleto; sem reconstrução da expressão omitida. |
| I07 | 33–35: "Z3 descobre  combinações impossíveis" / "`speed > 100 or (speed > 50 and rain)`" / "`--z3 --boundary`" | Expressão concreta adotada para estudar I12. Valores de fronteira não são especificados. |
| I08 | 41–43: "vários requisitos   arttquivo" / "`-f elos/requisitos.mcdc`" | Formato, conteúdo e resultado omitidos; não abrir arquivo de exemplo. |
| I09 | 45–51: "NAT2TEST" / "`--json`" / "`--format json`" | Formato completo da entrada e resultados não especificados. |
| I10 | 53–59: "`--exact`" / "`--direct`" | Exemplo de exact incompleto; garantias conflitantes em I14. |
| I11 | 61–69: "`verify`" / "conflitos  requisitos  lcunas" / "`chsseck`" | Contexto, formato e saída insuficientes; não corrigir comandos por suposição. |
| I12 | 79–83: "são consideradas  2ⁿ combinações" / "reltados `unsat` representam combinações psíveis  devem ser mantidos. Resultad `sat` representam combinações impossíveis  de ser descartados.  interpretação substitui  distiçnão anterior  vale  tdoas  operações." | A segunda regra expressamente substitui a distinção anterior. Casos F01–F08 formalizam essa regra, não a definição matemática de satisfatibilidade. Sem assumir formato de saída. |
| I13 | 85–87: "resuldo  decisão também muda" / "restado  decisão pode permanecer igual" | Conflito sobre par de independência; sem expectativa única. |
| I14 | 89–91: "`--exact`,  Z3 procura  suíte  tamanho mínimo" / "`--exact` executa  mesma heurística aproximada  pode retornar  suíe maior" | Conflito sobre minimalidade; não escolher resultado. |
| I15 | 93–95: "classificada  redundante" / "classificada  bloequeada" / "duas classificações são intercambiáveis" | Critérios contraditórios; não escolher classificação. |
| I16 | 97: "mutação (opcional)" | Fora do escopo de execução deste experimento. |
| I17 | 101: "limites documentados são: 20 entraas tabela-vrdade completa, 12 entads  processamento  Z3 linhuua linha 30 entradas modo dirto." | A reação exata ao limite e sua inclusão não são estabelecidas; fronteiras sem julgamento. |
| I18 | 105 em diante: "quatro módulos" e descrições dos módulos | Define escopo arquitetural; não determina comportamento concreto das APIs. |
| I19 | 119, 123: "Z3 é executado prosso extero" / "Z3 é carregado biioteca na dentro JVM não é iniciado proesso eterno" | Conflito de arquitetura, instalação e timeout; não assumir qual versão prevalece. |
| I20 | seção Limites: "**Guards temporais:** ferramenta analisa  passo iolado." | Alcançabilidade real e exemplos concretos omitidos; sem expectativa adicional. |

O documento contém tabelas e descrições de testes e resultados históricos.
Eles não fundamentam casos, metas, expectativas ou comparação. A documentação
também não fornece uma gramática completa, esquema de JSON, mensagens de erro,
contratos de API nem critérios únicos para os conflitos identificados. A
clareza é prejudicada por omissões, fragmentos e erros; a consistência é
prejudicada pelos conflitos citados. Não se atribui pontuação numérica.

## Decisões e autorrevisão

Os oito casos concretos F01–F08 verificam a regra substitutiva I12 para cada
combinação booleana dos três predicados do exemplo I07. As relações aritméticas
`speed > 100` e `speed > 50` são formalizadas literalmente; `rain` é um
booleano livre. Uma combinação `sat` deve ser descartada, uma `unsat` mantida.
A fórmula SMT verifica apenas a viabilidade matemática: a regra documental
para tratamento da resposta é separada e intencionalmente inversa. O texto não
descreve uma representação de saída sem conflito; o ponto de observação deve ser
identificado depois do congelamento, sem alterar o julgamento.
Em todos os casos a entrada é o exemplo literal de I07, com Z3 habilitado; as
três variáveis `p`, `q` e `rain` identificam a combinação examinada. A
pré-condição adicional desta busca é `speed` inteiro. Isso restringe a busca;
não afirma que a documentação exclui outros tipos numéricos. O caso F01 usa
`p=false`, `q=false`, `rain=false`, e assim sucessivamente conforme
`casos.json`. A regra é `sat => descartada`, `unsat => mantida`.

A autorrevisão verificou que a frase de substituição é explícita e que não se
aplicou a mesma precedência aos demais conflitos. O resultado Z3 não prova
fidelidade dessa interpretação. Não houve revisor independente. Interpretar
`rain` como booleano e os operadores de comparação como aritméticos é uma
interpretação necessária do exemplo, não uma gramática especificada; possível
erro de tradução é uma limitação. Os casos indeterminados I01/I02, I06, I08,
I09, I10/I14, I11, I13, I15, I17, I19 e I20 não têm asserção semântica.

Os casos não verificam saída exata, resultado da decisão, pares, minimização,
diagnóstico, fronteiras ou erros onde o texto não fornece expectativa única.
A seleção cobre as oito combinações do exemplo, sem pretender busca exaustiva
do universo de documentos ou cobertura global máxima.
