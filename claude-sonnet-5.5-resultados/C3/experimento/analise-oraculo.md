# Análise documental C3 (antes de ler qualquer código do SUT)

- Fonte única: `experimentacao-pesquisa/experimentacao-3/documentation/tool-readme-C3.md`.
- SHA-256 verificado antes da leitura: `F18B0821D79C7315486C13D5260FA2F6D6E9418EF03B86CDE58E66B91B7B87A3` (confere).
- Modelo: Claude Sonnet 5.5. Prompt: `geracao-de-oraculos-v3.md`. Revisão: **autorrevisão** (não houve revisor independente).
- Nenhum código, saída do SUT, `exemplos/*`, `contradictions.csv`, README de `experimentacao-3` ou resultado de outra condição/LLM foi lido antes do congelamento.

## 1. Inventário e contradições internas do texto

O texto contém afirmações que se contradizem entre si. Nesses pontos o próprio texto não resolve qual vale
(não se usou o código nem suposição para desempatar). Cada ponto é um caso INDETERMINADO (`C3-I01`…`I24`), registrado e **não executado**:

| ID | Conflito (linhas do arquivo) |
|---|---|
| I01 | condições: 4 por ocorrência (L55, L238) × 3 por variável distinta (L57) |
| I02 | Z3 obrigatório para qualquer execução (L77) × opcional / só recursos avançados (L75, L77) |
| I03 | códigos de saída 0/1/2 (L145) × mapeamento invertido (L147) |
| I04 | `--z3` acima de 12 entradas passa ao modo direto (L113) × continua na tabela completa (L115) |
| I05 | modo direto até 30 entradas sem tabela (L119, L617) × só até 12 e exige tabela (L115) |
| I06 | CSV de `check`: colunas opcionais (L191) × obrigatórias e aceitas-se-ausentes (L193) |
| I07 | `csv` = suíte / `truth-csv` = tabela (L215–217) × invertido (L219) |
| I08 | `unsat` = impossível (L293) × `unsat` = possível (L295) |
| I09 | par exige mudança do resultado (L297) × resultado pode permanecer (L299) |
| I10 | exata 5 × gulosa 6 (L265, L449) × gulosa sempre mínima, exata sem garantia (L303) |
| I11 | rótulos redundante/bloqueada (L305) × invertidos (L307) |
| I12 | Z3 processo externo, 60 s (L331) × implementação interna Java (L333) × biblioteca nativa sem limite (L335) |
| I13–I15 | métricas/regras de build (cobertura, PIT, agregação JaCoCo; L357–L383): fora do comportamento da CLI |
| I16 | parênteses deslocados: único sem garantia (L619) × garantia total (L621) |

Também são INDETERMINADOS por **omissão** (texto não dá expectativa única): I17 (`--constraint` com `-f`/`--json`),
I18 (linha sem identificador, ids repetidos), I19 (resultado do `verify` com contexto na VM), I20 (paridade de 3 entradas: expressão não dada),
I21 (resultado do `check` nos arquivos de exemplo), I22 (`-` antes de variável), I23 (tamanho da suíte de causa única), I24 (suíte/desempenho do build).

## 2. Casos determinados (48)

`C3-D01`…`D48`, cada um com expectativa única sustentada por trecho literal (ver `oraculo.json`). Decisões de modelagem:

- A afirmação **“Z3 obrigatório × opcional”** (I02) torna indeterminada qualquer expectativa para execução *sem* Z3.
  Por isso os casos determinados assumem Z3 no PATH (única condição em que as duas leituras concordam). Os casos “sem Z3” não são executados.
- Os valores numéricos “travados pela regressão” (tabela L497–L507) são usados como expectativa direta (requisitos, completos, combinações, impossíveis,
  testes, mutantes, equivalentes, detectados, conflitos). **O número de condições (21/69/29) não é afirmado**, pois depende de I01.
- O código de saída **nunca** é afirmado (I03); os casos observam saída, mensagens e arquivos.
- Não se afirma o rótulo redundante/bloqueada (I11), a distinção de pares quando o resultado não muda (I09) nem o formato `csv`/`truth-csv` (I07).
- `C3-D05`, `D01` usam os números 4 e 3 do “MinimalSuiteTest” (exemplos conhecidos). Para a variante de causa única não se afirma tamanho (I23).
- Casos de `check`/`verify` usam arquivos próprios criados pela suíte (tipos `enum`/`bool` documentados; ações `x := v`).

## 3. Z3

Z3 independente do SUT (`z3.exe` 5.4.1, Python), sem usar o módulo `mcdc-z3`. 122 consultas em `z3/*.smt2` com respostas em `z3/*.out`
(resumo em `z3/RESUMO.tsv`). Todas as respostas coincidem com a esperada (sem `unknown` nem timeout). Usos:

- tamanho mínimo da suíte de causa única (k−1 `unsat`, k `sat`) e testemunhas de pares por condição (D01, D02, D05, D06, D08, D34);
- linhas impossíveis de uma restrição (D09: 2 `unsat` em 8) e fronteiras (D10, D11) e realizabilidade de valores concretos (D12);
- mutantes por tipo mortos por uma suíte de causa única concreta (D14);
- consistência aritmética das tabelas do texto (D16–D27);
- conflito/lacuna do `verify` (D37–D41) e cadeia de 20 entradas (D43);
- cada INDETERMINADO por conflito: afirmação 1 `sat`, afirmação 2 `sat`, conjunção `unsat` (prova formal de que o texto afirma coisas incompatíveis).

`sat`/`unsat` dizem respeito às fórmulas; o Z3 não prova a fidelidade da tradução texto→fórmula.
Casos sem restrição lógica (comparação de saídas, formatos, arquivos) não têm consulta própria.

## 4. Limitações

- Autorrevisão; tradução texto→SMT não verificada por terceiro.
- Algumas expectativas aplicam o texto por analogia (D11: fronteira 50/51 para `speed > 50`).
- A escolha de tratar parágrafos autocontraditórios como INDETERMINADO é julgamento do modelo.
