# Análise documental do C3 (antes do SUT)

Fonte normativa exclusiva: `experimentacao-pesquisa/experimentacao-3/documentation/tool-readme-C3.md`,
SHA-256 `F18B0821D79C7315486C13D5260FA2F6D6E9418EF03B86CDE58E66B91B7B87A3` (conferido com `certutil` antes da leitura).
Referências `[Lnn]` são linhas dessa fonte.

## 1. Inventário de comportamentos

| Área | O que o texto descreve | Linhas |
|---|---|---|
| Comandos | `analyze`, `check`, `verify`; fontes: expressão direta, `-f .mcdc`, `--json` (uma só) | 33-53, 81-101 |
| Opções | `--unique-cause`, `--constraint`, `--z3`, `--exact`, `--direct`, `--boundary`, `--mutation`, `--context`, `--format`, `-o` | 103-129 |
| Operadores | e/ou/não nas formas textuais, C e DFRS; comparações | 131-143 |
| Códigos de saída | duas definições incompatíveis | 145, 147 |
| Entradas | `.mcdc`, JSON NAT2TEST (sufixo `_antes`), CSV do `check` | 149-203 |
| Saídas | `text`, `json`, `csv`, `truth-csv` + regra conflitante | 205-219 |
| Algoritmo | tabela-verdade (2ⁿ), impossíveis via Z3, pares, escolha gulosa/exata, diagnóstico, mutação | 285-311 |
| Limites | 20 / 12 / 30 entradas; 1000 pares por condição | 113-119, 313, 617 |
| Arquitetura | Z3 como processo externo com limite de 60 s × biblioteca interna sem limite | 331-335 |
| Testes do projeto | descrições de garantias (usadas como texto normativo quando dizem um resultado) e números de regressão | 337-613 |

Itens não verificáveis pela CLI (fora do oráculo): notas de cobertura/PIT do próprio projeto, regras de build Maven,
tempos de desempenho, publicação de relatórios (L339-433, L455-483).

## 2. Conflitos internos (consistência baixa)

Política adotada: quando duas passagens normativas dão resultados incompatíveis para o mesmo observável e o texto não
tem uma regra de precedência **externa às partes em conflito**, o observável é INDETERMINADO. Expressões como
"Interpretação definitiva", "substitui a distinção anterior" ou "Regra complementar" fazem parte do próprio conflito
(são uma das partes), não uma meta-regra da documentação; por isso não desempatam. Quando todas as leituras
dão o mesmo resultado para o observável, ele permanece DETERMINADO (Z3: leituras juntas sat e a negação da
expectativa unsat, ou checagem direta de que ambas implicam a mesma propriedade).

| ID | Conflito | Trechos | Observáveis afetados | Evidência Z3 |
|---|---|---|---|---|
| K1 | condição por ocorrência × por variável distinta | L55, L237, L507 (TIS 69) × L57 | contagem de condições e pares quando há entrada repetida | `K01_contagem_condicoes_*`; `K01_sem_repeticao_*` (sem repetição as leituras concordam) |
| K2 | Z3 opcional × indispensável para qualquer execução | L61, L75 × L77 (L77 contradiz-se a si mesmo) | qualquer execução sem z3 no PATH | `K02_z3_ausente_*` |
| K3 | códigos 0/1/2 (L145) × 0 = inválida, 1 = ok, 2 = só falha do Z3 (L147) | L145, L579 × L147 | todo código de saída | `K03_codigo_*` |
| K4 | colunas `decision`/`expected_outcome` opcionais × obrigatórias × aceitas e inferidas | L191, L551 × L193 | CSV sem essas colunas | `K04_csv_colunas_*` |
| K5 | `csv` = suíte e `truth-csv` = tabela inteira × o inverso | L127, L215-217 × L219 | conteúdo de `csv` e `truth-csv` | `K05_*` |
| K6 | `unsat` = impossível × `unsat` = possível ("vale para todas as operações") | L293 × L295 | impossíveis com `--z3`, conflitos/lacunas do `verify`, modo direto, `--exact` | `Z07_viabilidade_speed`, `K06_viabilidade_*` |
| K7 | par exige mudança do resultado e critério da variante × basta a condição mudar | L297 × L299 | pares que não mudam o resultado, condições sem par, tamanho de suíte | `Z03`, `Z04_*`, `K07_*` |
| K8 | `--exact` mínima e gulosa pode não ser (exemplo 5 × 6) × gulosa sempre mínima, exata heurística | L117, L265, L449 × L303 | tamanhos de suíte | `K08_exata_*` |
| K9 | redundante/bloqueada (L305) × classificação inversa e "intercambiável" (L307) | L305 × L307 | rótulo do diagnóstico | `K09_classificacao_*` |
| K10 | `--z3` > 12 entradas passa ao direto; direto até 30 sem tabela × permanece na tabela; direto só até 12 e exige tabela | L113, L119, L617 × L115 | `--z3` com 13+ entradas; `--direct` | `K10_*` |
| K11 | Z3 processo externo, 60 s, exige PATH × implementação interna/biblioteca nativa, sem PATH, sem limite | L61, L331 × L333, L335 | execução sem z3 no PATH (com K2) | `K02_*` |
| K12 | cobertura de linhas e desvios distintas e total ponderado × mesma métrica e média simples | L357 × L359 | não observável pela CLI | — |
| K13 | PIT altera o código × altera os requisitos; detectado quando todos passam | L361 × L363 | não observável pela CLI | — |
| K14 | parênteses deslocados podem escapar (1 de 727) × nenhum pode escapar | L619 × L621 | detecção de mutantes ASF | `K14_parenteses_*` |
| K15 | regra global de aprovação × verificação por módulo | L381 × L383 | build Maven, não observável pela CLI | — (o nome `K15_regressao_testes` nos arquivos Z3 refere-se ao total de testes da VM, efeito de K7/K8) |

## 3. Decisões de interpretação (autorrevisão)

- **A1 — comparações são entradas.** L55 define entrada como "variável distinta". As passagens L41/L43
  (`speed > 100`), L243 (`A = speed > 100 implica B = speed > 50`), L247 (o Z3 descobre combinações impossíveis entre
  `speed > 100` e `speed > 50`) e a tabela de regressão (VM: 21 condições, 152 = Σ2ⁿ combinações com cada comparação
  como entrada) só fazem sentido se cada comparação (átomo) for uma entrada lógica. O texto resolve assim a
  ambiguidade; com isso VM e NPP não têm entradas repetidas (K1 não as afeta), e TIS tem (tis#2-#4).
- **A2 — expectativas parciais.** Um caso é DETERMINADO quando a parte julgada não é atingida por conflitos/omissões;
  componentes atingidos (sobretudo o código de saída, K3) são registrados como "não julgados" no próprio caso, e
  observáveis relevantes atingidos têm casos INDETERMINADO próprios (C3-I01…I05 etc.).
- **A3 — descrições da suíte do projeto** (L439-585) são usadas quando enunciam um resultado (ex.: "expressões
  inválidas recusadas", "lacunas só com contexto", "a linha 0 é tudo verdadeiro"); quando apenas nomeiam um tópico
  ("ids repetidos", "arquivos inválidos", "linha sem identificador") não fornecem expectativa → INDETERMINADO.
- **A4 — fronteiras.** L43 dá o exemplo `speed > 100 → 100 e 101` e a regra "variações no limite de cada comparação".
  Formalizei limite como o único par de inteiros adjacentes (v, v+1) em que a comparação muda de valor (Z3 com
  verificação de unicidade). Aplicado a `>`, `>=`, `<`, `<=` sobre inteiros; reais e enumerações não foram usados.
  É uma generalização do exemplo — registrada como tal (C3-T28, C3-T29).
- **A5 — "recusada"** significa: sem relatório de análise e com mensagem de erro; o código de saída não é julgado (K3).
- **A6 — precondição Z3 no PATH.** Com z3 no PATH todas as leituras de K2/K11 permitem a execução; por isso os casos
  determinados rodam com z3 no PATH, e o comportamento sem z3 é registrado como indeterminado (C3-I17, I18).

## 4. Formalização Z3

`gerar_oraculo.py` grava 106 consultas em `z3/*.smt2` e as saídas em `z3/*.out` (Z3 5.4.1, executável
independente, `-T:60`). Tipos de consulta:

- `Z01_tt_*`: uma consulta `check-sat` por combinação; `sat` ⇔ guarda verdadeira. O avaliador próprio `exprlib.py`
  é conferido contra o Z3 linha a linha.
- `Z02_eq_*`: equivalência de formas de operadores (negação da igualdade `unsat`).
- `Z03`/`Z04`/`Z09`: existência de par por condição em três critérios (mascaramento estrito, causa única,
  simplificado), com restrição quando há.
- `Z07`: viabilidade das combinações de `speed > 100`, `speed > 50`, `rain` (2 `unsat`).
- `Z08`: fronteiras (par adjacente e unicidade).
- `Z10`: pares de causa única em `A1 and … and A20`.
- `Z11`/`Z12`: resultado das guardas nos testes dos CSVs de `check`.
- `Z13`: somas de combinações dos sistemas = 152/268/76 (total 496).
- `Kxx_*`: cada leitura isolada `sat`, as duas juntas `unsat` (conflito relevante para o observável).

Limites: `sat`/`unsat` dizem respeito às fórmulas; não provam que a tradução do texto seja fiel. Nenhum `unknown`
ou timeout ocorreu.

## 5. Isolamento e revisão

- Antes do congelamento li apenas: README/protocolo/modelo/prompt da pesquisa, a fonte C3 e os arquivos de entrada de
  `exemplos/` citados pela fonte (`requisitos.mcdc`, `decisoes.json`, `testes.csv`, `vm/tis/npp-decisoes.json`).
  Também vi o script de lançamento `./mcdc` (raiz do repositório, não é `mcdc-*/src`), que revela o nome da classe
  principal; nenhuma expectativa vem dele.
- Os comentários dentro de `exemplos/testes.csv` (ex.: "T4 tem o resultado esperado errado") não foram usados como
  expectativa; T4 foi avaliado pelo Z3 a partir das guardas.
- Não há revisor independente: a revisão texto–fórmula é **autorrevisão**.
