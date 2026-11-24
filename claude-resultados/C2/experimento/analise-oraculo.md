# Análise documental e oráculo — condição C2

Escrita **antes** de qualquer leitura do código do SUT (`mcdc-*/src`) ou execução
do SUT. Autorrevisão (não houve revisor independente).

## Fonte

- Arquivo: `experimentacao-pesquisa/experimentacao-2/documentation/tool-readme-C2.md`
  (602 linhas).
- SHA-256 verificado antes da leitura:
  `61C4062B5FC6B4F364F40465B0E017C80E0FA0C5433412EB2E925C545F6EFBE1` (confere com o protocolo).
- Nível pretendido pelo protocolo: clareza baixa / consistência alta. Não se presume que foi atingido.

## Característica da fonte

O texto C2 é o README da ferramenta com **letras, artigos, preposições e palavras
apagadas** em quase toda frase (ex.: L139 `**Cigo  saída:** ... `2`: resutado vido
 processamto,  com  condição  par  `analyze`...`), mais espaços inseridos dentro de
palavras (`Z   3`, `cond   ição`). Tabelas, números e trechos de código estão quase
sempre legíveis; os exemplos de linha de comando às vezes perdem letras de variáveis
(`" or (B and C)"`, `"(not  or D)"`) ou de opções (`- tabela.csv`).

Regra de leitura adotada (mesma para todos os casos):

1. Uma lacuna só foi reconstruída quando **outro trecho legível da própria fonte**
   fixa a palavra ausente (ex.: L139 "condição  par" → "sem par", porque L39 e L461
   usam "condição sem par" como o problema; L227 `(not  and C)` → `not A` porque L55
   dá a expressão completa).
2. Quando a lacuna muda o sentido e nada no texto a fixa (operador da precedência em
   L515, "considera primeiro as condições   pars" em L285, preposição de `--boundary`
   em L115, letra da expressão do exemplo `--exact`), o caso é **INDETERMINADO**.
3. Temas listados apenas como nome de teste interno ("linha sem identificador",
   "ids repetidos", "sinal de menos só em números") só dão expectativa quando o
   próprio tema já diz o comportamento; caso contrário, INDETERMINADO.
4. Não se usou conhecimento do código, de saídas do sistema, de outras condições nem
   de outras cópias da documentação.

## Inventário de requisitos extraídos da fonte

| # | Requisito (leitura) | Linhas | Uso |
|---|---|---|---|
| R1 | Comandos `analyze`, `check`, `verify`; fontes: expressão direta, `-f` `.mcdc`, `--json` NAT2TEST | L33-L53, L77-L97 | todos |
| R2 | Variantes: mascaramento (padrão) e causa única (`--unique-cause`) | L55, L105 | A01, A02, A22-A26, A31-A33, J*3 |
| R3 | Entrada = variável distinta; condição = cada ocorrência; `(A and B) or (not A and C)`: 3 entradas, 4 condições `A#1, B, A#2, C` | L55, L225 | A10 |
| R4 | Operadores: `and && /\`, `or \|\| \/`, `not !`, `= == != < <= > >=` | L125-L137 | A04-A09, A14 |
| R5 | Código de saída 0 / 1 (entrada inválida) / 2 (condição sem par; não demonstrada ou divergente; conflito ou lacuna) | L139 | quase todos |
| R6 | `.mcdc`: um requisito por linha `ID: expressão`; `#` comentário | L143 | M01-M05 |
| R7 | JSON NAT2TEST com variáveis, tipos, decisões, guarda e ações; sufixo `_antes` | L153 | J*, V* |
| R8 | CSV de testes: teste, entrada, valor (`T`/`F` ou concreto); `decision` e `expected_outcome` opcionais | L183 | K01-K07 |
| R9 | Formatos `text` (padrão), `json`, `csv`, `truth-csv`; `check`/`verify` aceitam `text` e `json`; `-o` grava em arquivo | L121-L123, L197-L207 | F01-F07, J06, J07 |
| R10 | Tabela-verdade de 2ⁿ combinações sobre entradas distintas; linha 0 é tudo verdadeiro | L279, L485 | A10, F03 |
| R11 | Com Z3: combinações `unsat` são impossíveis e saem da análise; valores concretos realizam a combinação | L41, L281, L463 | A27-A30, J*4, J03 |
| R12 | Fronteira de cada comparação (`speed > 100` → 100 e 101) | L43, L115 | A28 |
| R13 | Diagnóstico: sem par mesmo com todas as combinações → redundante; perde par por combinações impossíveis → bloqueada | L39, L287 | A22-A26, M01 |
| R14 | `--exact`: a menor suíte possível escolhida pelo Z3 | L45, L111, L285 | A31-A34, J*2 |
| R15 | `--direct`: pares pedidos ao Z3 sem tabela (até 30 entradas); `--z3` com > 12 entradas passa ao modo direto; mesmo diagnóstico da tabela | L47, L109, L113, L419 | A19-A21, A23, J02 |
| R16 | Limites: 20 entradas na tabela completa, 12 no Z3 linha a linha, 30 no modo direto | L293, L587 | A17, A18, A21 |
| R17 | `--constraint`: restrição entre condições escrita à mão (ex.: A ⇒ B) | L107, L229-L231 | A25, A26 |
| R18 | Mutação: seis tipos (ORF, ENF, VNF, MVF, VRF, ASF), equivalentes fora da contagem | L49, L117, L289 | A35, A36, J*1 |
| R19 | Exemplos conhecidos: `(A∧B)∨C` → 4 testes; `A∧¬B` → 3 | L493 | A01, A03-A06, M02 |
| R20 | Paridade de 3 entradas exige 8 testes | L591 | A16 |
| R21 | REQ-003 de `exemplos/requisitos.mcdc` tem condição redundante | L241 | M01 |
| R22 | Números de regressão VM/TIS/NPP; busca exata e causa única dão o mesmo número de testes | L461, L465-L477 | J*1-J*3 |
| R23 | `verify`: conflito = dois requisitos valem juntos e escrevem valores diferentes; lacuna = nenhum requisito vale; `--context` restringe a situação; contradição só com valores diferentes da mesma variável | L53, L119, L503 | V01-V09 |
| R24 | Sem Z3, recursos que não dependem dele continuam; opções que exigem Z3 avisam | L73 | Z01-Z03 |
| R25 | `check`: cobertura MC/DC, o que falta e resultado esperado errado | L51 | K01-K07 |

## Decisões de leitura relevantes

- **Código 2 em `analyze`** ("condição  par"): lido como *condição sem par* (regra 1).
- **Causa única**: o texto não define a variante além do nome. Usou-se o sentido do
  nome (só a condição avaliada muda), que é o que o nome diz, e L491 ("par de causa
  única vale no mascaramento"). Consequência: *existência* de par de causa única
  implica condição com par nas duas variantes; *ausência* de par só foi usada como
  expectativa na variante causa única. Para o mascaramento, a ausência de par nunca
  foi derivada (exceto o REQ-003, dito explicitamente pela fonte).
- **`--constraint`**: L231 descreve a restrição como implicação física (A = `speed >
  100` implica B = `speed > 50`); combinações que a violam foram tratadas como
  inexistentes para a análise (A25, A26).
- **Tipos em expressão direta**: a fonte não declara tipos; o exemplo `speed > 100 →
  100 e 101` mostra inteiros. As fórmulas Z3 usam `Int` para comparações numéricas,
  e domínio textual aberto para `mode = idle`.
- **Números de regressão**: a tabela L467-L477 não diz as opções usadas; a coluna
  "Impossíveis" exige Z3 e "Mutantes" exige `--mutation`, por isso J*1 usa
  `--z3 --mutation` na variante padrão. "Completos" não tem definição → J01 INDETERMINADO.

## Indeterminações (15)

A11 precedência; A15 menos em identificador; A18 21 entradas sem Z3; A21 31 entradas
no modo direto; A34 exemplo `--exact` com letra apagada; A36 contagem de mutantes;
A37 ordem gulosa; F07 `check` com formato não aceito; M05 linha sem id; J01 coluna
"Completos"; J05 ids repetidos; Z04 `--boundary` sem `--z3`; V09 lacunas sem
contexto; E01 arquivo ausente; E02 comando inexistente. Motivos por caso em
`oraculo.json` e `inventario-casos.md`.

## Formalização Z3

- Z3 5.4.1 (`C:/Users/User/AppData/Roaming/Python/bin/z3.exe`), independente do SUT,
  chamado com arquivos SMT-LIB gerados por `scripts/gerar_z3.py` (parser próprio que
  **recusa** misturar and/or sem parênteses, pois a precedência é indeterminada).
- Consultas em `z3/*.smt2`, saídas em `z3/*.out`, resumo em `z3/resumo-z3.json`.
  Nenhuma resposta `unknown`. As duas mensagens `model is not available` em
  `Q22-V06-lacuna.out` e `Q22-V07-lacuna.out` vêm de `(get-model)` depois de `unsat`
  (resultado esperado da consulta); não afetam a resposta.
- O que foi formalizado: viabilidade de cada combinação (tabelas de A10, A16, A22,
  A27, J03 e de todas as decisões de VM/TIS/NPP); existência de par de causa única
  por condição, com e sem domínio/restrição; tamanho mínimo de suíte de causa única
  (A31-A33, `(<= soma k)` sat/unsat); menor/maior inteiro da fronteira e sua
  unicidade; valor das guardas nos testes de `check`; conflitos (sobreposição de
  guardas com ações de valores diferentes) e lacunas no contexto.
- Conferência de consistência da fonte (não altera o oráculo): o Z3 reproduz
  VM 5/21/152/4 e 0 conflitos, TIS 17/69/268/4 e 3 conflitos, NPP 11/29/76/1 e 1
  conflito, exatamente como L471-L475.
- Limite: `sat`/`unsat` dizem respeito às fórmulas; não provam que a tradução do
  texto para as fórmulas é fiel.

## Autorrevisão texto–fórmula

Cada expectativa determinada em `oraculo.json` cita o trecho literal e as consultas
Z3 que a sustentam. Revisão feita pelo mesmo modelo que gerou o oráculo; não há
revisor independente.
