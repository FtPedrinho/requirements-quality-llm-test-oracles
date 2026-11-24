# Análise do oráculo — condição C1

Fonte normativa exclusiva: `experimentacao-pesquisa/experimentacao-1/documentation/tool-readme-C1.md`,
SHA-256 `91981FA0181E5CC1BC5A67DAAFC965BB82D6F8EB0A6D47EB58CE291A3EF5D33B` (conferido em
2026-11-24T10:22:08-03:00, antes da leitura). Referências `Lnnn` são linhas desse arquivo.

Esta análise foi escrita **antes** de qualquer leitura de `mcdc-*/src` e de qualquer execução do SUT.
Os arquivos de `exemplos/` citados pela fonte (`requisitos.mcdc`, `vm-/tis-/npp-decisoes.json`,
`decisoes.json`, `testes.csv`) foram lidos apenas como entrada. `exemplos/saidas/` não foi aberto.

## 1. Inventário de comportamentos da fonte

| Área | Comportamentos documentados usados | Linhas |
|---|---|---|
| Comandos | `analyze`, `check`, `verify`; fonte única (expressão, `-f`, `--json`) | L79–97 |
| Opções | `--unique-cause`, `--constraint` (só expressão direta), `--z3`, `--exact`, `--direct` (≤30), `--boundary` (com `--z3`), `--mutation`, `--context`, `--format`, `-o` | L101–123 |
| Operadores | e/ou/não em 3 grafias; 7 comparadores; precedência e antes de ou | L127–137, L515 |
| Código de saída | 0 / 1 (entrada inválida) / 2 (sem par, não demonstrada, esperado divergente, conflito, lacuna) | L139 |
| Entradas | `.mcdc` com `ID: expr` e `#`; JSON NAT2TEST; CSV de testes com `decision`/`expected_outcome` opcionais | L143–193 |
| Saídas | text, json (ligado ao requisito), csv (linha por teste e entrada), truth-csv (tabela inteira, impossíveis marcadas) | L199–207 |
| Algoritmo | tabela 2ⁿ por entradas distintas; impossíveis = `unsat`; pares; gulosa; exata; redundante × bloqueada; mutação 6 tipos | L275–291 |
| Limites | 20 (tabela), 12 (Z3 linha a linha), 30 (direto); 1000 pares por condição | L293, L587 |
| Garantias da suíte interna (usadas como afirmações sobre o comportamento) | (A∧B)∨C → 4 testes, A∧¬B → 3; linha 0 tudo verdadeiro; condição sem efeito sem par; par de causa única vale em mascaramento; ids repetidos e colunas faltando recusados; sinal de menos só em números; direto = tabela; exata/causa única = mesmo nº de testes nos exemplos; números de regressão | L461–537 |
| Exemplos com resultado | REQ-003 redundante; `--exact` 5 vs gulosa 6; paridade 3 → 8 testes; `speed > 100` → 100/101 | L241, L255, L591, L43 |

## 2. Decisões de interpretação (registradas, não inventadas)

1. **Mascaramento não é definido pelo texto.** Só uso dele: (a) L491 — todo par de causa única vale em
   mascaramento; (b) L491 — condição sem efeito fica sem par; (c) números literais (4, 3, 5, 6, 8 testes;
   regressão). Expectativas que dependeriam da definição exata de mascaramento não foram criadas.
2. **Causa única** é lida literalmente: só a condição alvo muda entre as duas linhas. Para entradas
   repetidas (A#1/A#2) o texto não resolve → AN-38 INDETERMINADO.
3. **Código 1 por elementos fora do documentado** (arquivo inexistente AN-41, formato não listado AN-21,
   `csv` no `check` CK-07, `-x` AN-20): o código 1 é o único documentado para entrada que não pode ser
   processada; 0 e 2 exigem processamento concluído. Registrado como inferência por eliminação.
4. **Números de regressão** (L467–477) são lidos como resultado do `analyze`/`verify` com Z3 sobre os
   três JSON de exemplo; "Requisitos" = decisões (nas entradas, decisões = requisitos distintos: 5/17/11).
   "Completos" não é definido → SY-TIS-07 INDETERMINADO; para VM e NPP (todos completos) vale N+1 por decisão.
5. **Lacunas** só são procuradas com `--context` (L537); sem contexto, `verify` sem conflitos → 0.
6. **Aviso sem Z3** (AN-32): a forma do aviso não é definida; aceita-se qualquer menção a "z3" em stdout/stderr.
7. Detalhes de formato (nomes de campos JSON, colunas do CSV, marca de impossível) não são definidos;
   a extração das medidas é feita pela suíte após inspeção, sem alterar a expectativa. Se a medida não
   puder ser extraída de forma única, o caso é registrado como não avaliado (erro técnico/medição),
   não como falha.

## 3. Formalização Z3

Z3 5.4.1 (`z3.exe`, build 145c0c51…), independente do SUT, limite `-T:60`. Gerador:
`z3/gerar_e_executar.py`; consultas em `z3/consultas/`, saídas em `z3/saidas/`, resumo em
`z3/saidas/_resumo.tsv`. Nenhum `unknown` ou timeout. As mensagens `model is not available` em
8 saídas são o `(get-model)` após `unsat`, esperado.

| Grupo | O que formaliza | Resultado |
|---|---|---|
| Q01 | Existência de par de causa única por condição (com/sem restrição) | AN-01/03/04/05/13 todos `sat`; AN-14 A `unsat` com restrição e `sat` sem (bloqueada); REQ-003 pedal `unsat` (redundante) |
| Q02 | Tamanho mínimo de suíte de causa única | (A∧B)∨C: 3 `unsat`, 4 `sat`; A∧¬B: 2 `unsat`, 3 `sat`; AN-27 por entrada: 4 `unsat`, 5 `sat` (auxiliar); paridade ≡ XOR (`unsat` da negação) |
| Q03 | Viabilidade das 8 linhas de `speed>100 ∨ (speed>50 ∧ rain)`; fronteiras; bloqueio | 2 linhas `unsat` (A=T,B=F); fronteiras 101/100 e 51/50 válidas; AN-42 B `unsat` com A⇒B, `sat` sem |
| Q04 | VM: viabilidade das 152 linhas | 148 `sat`, 4 `unsat` (vm4 e vm5: TFF e FFF) — coincide com "Impossíveis 4" |
| Q05 | VM: conflitos (10 pares com escritas diferentes) e lacuna no contexto | 10 `unsat` (0 conflitos, coincide com a tabela); lacuna `sat` (testemunha no `.out`) |
| Q06 | JSON montados do verify | VF01 `sat` (conflito), VF03 `unsat`, VF04 `sat` (lacuna), VF05 `unsat` |
| Q07 | Consistência aritmética da tabela de regressão e N+1 | `unsat` da negação (consistente); TIS 69+17≠80 |
| Q08 | Avaliação de guardas dos testes do `check` | CK-01 sem divergência; decisoes.json T4 guarda F (esperado T diverge), T3 guarda T |
| Q09 | Precedência discrimina | `sat` |

Limites: `sat`/`unsat` dizem respeito às fórmulas; não provam que a tradução do texto seja fiel.
Q02 usa causa única por entrada, não mascaramento por ocorrência; é evidência auxiliar, não fonte
das expectativas de 4/3/5/6/8 testes, que vêm de números literais.

## 4. Casos

79 casos (70 DETERMINADO, 9 INDETERMINADO). Ver `oraculo.json` (fonte de verdade) e
`inventario-oraculo.md` (tabela gerada a partir dele).

INDETERMINADOS: AN-25 (>20 entradas), AN-35 (>30 no direto), AN-36 (`--boundary` sem `--z3`),
AN-37 (`--constraint` com arquivo), AN-38 (causa única com entrada repetida), AN-39 (comando
desconhecido), AN-40 (sem argumentos), AN-44 (linha `.mcdc` sem identificador), SY-TIS-07 ("completos").

## 5. Revisão

Não houve revisor independente. **Autorrevisão**: conferi cada caso contra a linha citada, a
coerência entre os totais da tabela de regressão (Q07) e a correspondência entre as fórmulas e as
guardas das entradas (Q04–Q06, Q08). Perdas de isolamento conhecidas: o modelo tem conhecimento
geral prévio de MC/DC (literatura), e a sessão recebeu do orquestrador apenas as notas de ambiente
(caminhos de ferramentas e procedimento de build), sem resultados de outras condições.
