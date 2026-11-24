# Análise documental da fonte C4 (antes do SUT)

## Identificação

- Condição: C4 (clareza e consistência pretendidas baixas; o nível não é presumido).
- Fonte normativa exclusiva: `experimentacao-pesquisa/experimentacao-4/tool-readme-C4.md`.
- SHA-256 conferido antes da leitura: `D6BC0A588CD9A7DF7F1F566573944FA5CB1707BBA676B4E9854CAD2CC5440FC2` (coincide; ver `fonte.sha256`).
- Prompt: `experimentacao-pesquisa/prompts/geracao-de-oraculos-v3.md`. Protocolo: `experimentacao-pesquisa/protocolo/metodologia.md`.
- Modelo: Claude Opus 5.5 (`claude-opus-5-5`), Claude Code (app desktop); outras configurações: não informado.
- Commit de referência do repositório: `ed7d2e0`.

## Contexto e isolamento

- Lidos: README da pesquisa, metodologia, modelo de relatório, prompt v3, fonte C4 e os arquivos de entrada de
  `exemplos/` citados pela fonte (`requisitos.mcdc`, `decisoes.json`, `testes.csv`, `vm/tis/npp-decisoes.json`).
- Perda de isolamento menor: um comando de leitura exibiu também `exemplos/vm-requisitos.mcdc` e
  `exemplos/maquina-cafe.mcdc` (arquivos de entrada não citados pela fonte). Contêm só guardas e comentários; não
  foram usados no oráculo.
- Não foram abertos: `claude-resultados/C0..C3`, `copilot-resultados/`, `research/`, `relatorios/`, `exemplos/saidas/`,
  as outras `experimentacao-*`, `experimentacao-pesquisa/experimentos/`, histórico git desses caminhos e notas de
  outras sessões. Não se pode demonstrar ausência de influência de conhecimento prévio do modelo sobre ferramentas MC/DC
  em geral.
- O SUT (`mcdc-*/src`) não foi lido nem executado antes do congelamento.

## Estado da fonte

A fonte tem 423 linhas e começa no meio de uma tabela (L1). Faltam a introdução, a descrição da instalação, a lista
de opções da CLI e a descrição dos formatos de texto/JSON. Há palavras curtas apagadas em todo o texto (artigos,
preposições e também identificadores de uma letra, como o `A` dos exemplos), erros de grafia, marcas
`[trecho omitido]`, links e caminhos corrompidos (`elos/requisitos.mcdc`, `--te`, `--cotnext`, `ana`, `chsseck`,
`analoyze`) e parágrafos injetados que contradizem o restante.

## Inventário de regras e situação

| Tema | Linhas | Situação |
|---|---|---|
| Tabela-verdade: 2^n combinações sobre entradas distintas, resultado por combinação | L79 | Determinada |
| Linha 0 = tudo verdadeiro | L303 | Determinada (ordem das demais: omissão, I35) |
| Aparição repetida = condição própria com par próprio (#1, #2) | L25, L305 | Determinada |
| Mascaramento padrão; `--unique-cause` | L15-19 | Determinada |
| Todo par de causa única vale no mascaramento; linhas impossíveis nunca entram nos pares | L309 | Determinada |
| Comparações e operador DFRS `/\` | L21-23, L333 | Determinada (aceitação e contagem) |
| Restrição escrita à mão (`--constraint`) | L29-31, L319 | Determinada para expressão própria; exemplo literal incompleto (I03) |
| Expressões inválidas recusadas; erro de sintaxe em `.mcdc` com número da linha | L333, L335, L341 | Determinada (código de saída não, I23) |
| Arquivo `.mcdc` com vários requisitos e comentários | L41-43, L335 | Determinada |
| Números de regressão: requisitos, condições, combinações | L285-295 | Determinada; demais colunas indeterminadas |
| JSON: relatório válido com rastreabilidade por decisão | L49, L369 | Determinada |
| `check`: resultado esperado errado; falta de pares | L67-69, L317 | Determinada |
| Mutação: seis tipos | L97 | Determinada (tipos); quantidades/equivalentes indeterminados |
| Limite de 20 entradas; 1000 pares por condição | L101, L405 | Determinada dentro do limite; acima, omissão |
| Impossíveis via Z3 (unsat x sat) | L81, L83 | **Conflito** (I09) |
| Critério do par (decisão muda x pode ficar igual) | L85, L87, L309 | **Conflito** (I18) |
| Minimalidade da gulosa x `--exact` | L89-91, L53-55, L351 | **Conflito** (I05, I16, I17) |
| Diagnóstico redundante x bloqueada | L93, L95 | **Conflito** (I19, I20) |
| Arquitetura do Z3 (processo externo, interno Java, biblioteca nativa; limite de 60 s) | L119-123 | **Conflito** (I21, I22) |
| Formatos `csv` e `truth-csv` | L3-7 | **Conflito** (I07, I08) |
| Garantia de parênteses / mutação | L407-409, L323 | **Conflito** (I30) |
| Cobertura de linhas x desvios, nota de mutação, regra global de aprovação | L145-171 | Conflitos, mas sobre o build/qualidade do projeto; não são comportamento observável da CLI e ficam fora do oráculo |

## Decisões de análise (registradas antes do SUT)

1. **Operandos apagados não são reconstruídos.** Os exemplos literais com identificador ausente (`( and B) or C` etc.)
   ficam INDETERMINADOS. Para exercitar as regras gerais usam-se expressões próprias (E1–E7, DFRS), cujas expectativas
   decorrem só das regras em prosa.
2. **Conflito que não altera o resultado não impede a expectativa.** Quando as duas leituras de um conflito levam ao
   mesmo resultado, o caso é determinado e a equivalência é mostrada no Z3 (Q03/Q07: par que muda a decisão e mudança
   isolada são ambos `sat`). Quando divergem (Q03-REQ-003: `unsat` x `sat`), o caso é INDETERMINADO.
3. **Regra de satisfatibilidade (L83).** Embora se declare prevalente, ela contradiz números medidos do mesmo texto
   (tabela de regressão). Q05 mostra que a leitura original (unsat = impossível) dá 4/4/1 impossíveis, exatamente a
   tabela, e a leitura substituta daria 148/264/75. O texto não diz qual das duas afirmações prevalece sobre os números;
   tudo o que depende da classificação de combinações pelo Z3 (`--z3`, `--boundary`, `--direct`, `verify`, tamanhos de
   suíte e mutantes da tabela) fica INDETERMINADO. Por isso nenhuma execução planejada usa `--z3`.
4. **Caminho `elos/requisitos.mcdc`.** Tratado como `exemplos/requisitos.mcdc` (único arquivo existente com REQ-003); a
   correção é só de localização da entrada, não de expectativa.
5. **Grafia degradada de opções** (`--te`, `ana`, `chsseck`) é detalhe de invocação e será resolvida após o
   congelamento, pelo código, sem alterar expectativas.
6. **Códigos de saída** não são exigidos em nenhum caso (significado não documentado, I23). Recusa é observada como
   ausência de análise e presença de mensagem de erro.
7. **Unidade de contagem:** caso do oráculo (ID estável). Um comando (Xnn) roda uma vez e pode ser julgado por vários
   casos. Casos INDETERMINADOS não são executados e não entram na cobertura (decisão do pesquisador).

## Z3

- Z3 independente: `z3.exe` 5.4.1 (64 bit, hashcode 145c0c51570a357cc558ce898ce77573ba9d4fbf), fora do SUT.
- Gerador próprio: `z3/gerar_e_executar.py` (parser próprio de expressões; não usa código `mcdc-*`).
- Consultas em `z3/consultas/*.smt2`, saídas em `z3/saidas/*.out`, síntese em `z3/resumo.json`.
- Nenhuma resposta `unknown`/timeout.

| Consulta | Objeto | Resultado |
|---|---|---|
| Q01-E1..E4 | Resultado da decisão em cada combinação de E1–E4 | E1: 8 linhas, 1 V; E2: 4 linhas, 1 F; E3: 8 linhas; E4: 8 linhas |
| Q02 | Linhas de E4 que violam `not p or q` | 2 (p=V,q=F) |
| Q03-REQ-001/002/003 | Existência de par por entrada: leitura A (decisão muda) e B (mudança isolada) | REQ-001/002: A=sat, B=sat em todas; REQ-003 pedal_pressionado: A=unsat, B=sat |
| Q04-T1..T4 | Valor da guarda nos valores concretos de testes.csv | T1 V, T2 F, T3 V, T4 F (esperado T: divergente) |
| Q05-vm/tis/npp | Viabilidade de cada combinação (152/268/76) e aritmética da tabela | unsat 4/4/1; sat 148/264/75; contagens 5/21/152, 17/69/268, 11/29/76 conferem |
| Q06 | 2^20 e pares de x01 em E5 | 1048576; 524287 > 1000 |
| Q07 | Par de causa única em (p and q) or r | sat para p, q, r |

Limites: `sat`/`unsat` dizem respeito às fórmulas; não provam que a tradução do texto degradado esteja correta. As
enumerações de enum foram codificadas como inteiros com domínio restrito; reais como `Real`.

## Revisão

Não houve revisor independente. A relação texto–fórmula foi revista pelo próprio executor (autorrevisão) antes do
congelamento.
