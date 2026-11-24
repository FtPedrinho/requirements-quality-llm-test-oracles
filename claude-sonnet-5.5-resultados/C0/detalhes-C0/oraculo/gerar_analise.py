import json,os
A=os.path.dirname(os.path.abspath(__file__))
o=json.load(open(os.path.join(A,"oraculo.json"),encoding="utf-8"))
L=["# Análise documental C0 e oráculo (congelada antes de ler o SUT)\n",
"Fonte normativa exclusiva: `experimentacao-pesquisa/documentacao-original/tool-readme-original.md` "
"(SHA-256 `72b827bdee6ce859527765cff574a473519c00a1af9aa9f3aacce4236a4995f8`, conferido antes da leitura).\n",
"Revisão: **autorrevisão** (sem revisor independente). O Z3 prova apenas as fórmulas; a fidelidade texto→fórmula não é provada.\n",
"## 1. Inventário do comportamento documentado\n",
"- **Comandos:** `analyze`, `check`, `verify`; fonte única: expressão, `-f` (.mcdc) ou `--json` (NAT2TEST).",
"- **Operadores:** e (`and`,`&&`,`/\`), ou (`or`,`||`,`\/`), não (`not`,`!`), comparações (`= == != < <= > >=`); precedência *e* antes de *ou*; sinal de menos só em números.",
"- **MC/DC:** mascaramento (padrão) e causa única; cada aparição é uma condição (`A#1`, `A#2`); par = dois testes possíveis em que a condição muda, a saída muda e ela decide nos dois.",
"- **Diagnóstico:** condição sem par é *redundante* ou *bloqueada* por combinações impossíveis.",
"- **Tamanho da suíte:** N+1 em guardas simples; exemplos explícitos: (A∧B)∨C = 4, A∧¬B = 3, paridade de 3 entradas = 8, `--exact` do exemplo = 5.",
"- **Opções:** `--constraint`, `--z3`, `--exact`, `--direct`, `--boundary`, `--mutation`, `--format`, `-o`, `--context`.",
"- **Formatos:** `text`, `json`, `csv` (uma linha por teste e entrada), `truth-csv` (tabela inteira, impossíveis marcadas, cabeçalho por decisão); `check`/`verify` aceitam `text` e `json`.",
"- **Códigos de saída:** 0 tudo certo; 1 entrada inválida; 2 condição sem par / (check) não demonstrada ou esperado divergente / (verify) conflito ou lacuna.",
"- **Limites:** 20 entradas (tabela), 12 (Z3 linha a linha; acima passa ao modo direto), 30 (direto).",
"- **Verificação:** conflito = dois requisitos valem juntos e escrevem valores diferentes; lacuna = nenhum requisito vale (só com `--context`).",
"- **Sistemas de exemplo:** VM (0 conflitos), TIS (3), NPP (1); `exemplos/requisitos.mcdc` tem REQ-003 com condição redundante.\n",
"## 2. Regras de observação adotadas\n",
"- `exit`: código de saída do processo `./mcdc`.",
"- `csv_rows`: linhas não vazias do CSV da suíte; aceita `n` ou `n+1` (a fonte não diz se há cabeçalho no CSV da suíte).",
"- `lines`: linhas não vazias do `truth-csv`, exatas (2^n combinações + 1 cabeçalho por decisão).",
"- `contains`/`not_contains`: busca sem distinção de maiúsculas na saída padrão+erro.",
"- Casos **INDETERMINADOS** não recebem expectativa e **não entram na execução usada para cobertura** (decisão do pesquisador).\n",
"## 3. Casos determinados\n",
"| ID | Grupo | Caso | Argumentos | Expectativa | Trecho literal | Justificativa |","|---|---|---|---|---|---|---|"]
def esc(s): return str(s).replace("|","\|").replace("\n"," ")
for c in o["casos"]:
    if c["status"]=="DETERMINADO":
        L.append("| %s | %s | %s | `%s` | `%s` | %s | %s |"%(c["id"],c["grupo"],esc(c["titulo"]),esc(" ".join(c["args"])),esc(json.dumps(c["observa"],ensure_ascii=False)),esc(c["citacao"]),esc(c["justificativa"])))
L+=["\n## 4. Casos INDETERMINADOS\n","| ID | Caso | Trecho | Motivo |","|---|---|---|---|"]
for c in o["casos"]:
    if c["status"]=="INDETERMINADO":
        L.append("| %s | %s | %s | %s |"%(c["id"],esc(c["titulo"]),esc(c["citacao"]),esc(c["motivo"])))
L+=["\n## 5. Evidência Z3\n","Executável: `Z3 version 5.4.1` (pacote `z3-solver`), independente do módulo `mcdc-z3`. Consultas SMT-LIB em `smt/*.smt2`; respostas e resumo em `smt/resultados-z3.json`. Formalizado: existência de par MC/DC por condição (com e sem restrição), menor suíte (confirma 3, 4, 5 e 8 testes dos exemplos da fonte), pares numéricos com `speed` inteiro, demonstração de testes dados, conflito e lacuna do `verify`. Todas as expectativas de saída foram conferidas também por força bruta em Python. Nenhum `unknown`/timeout."]
open(os.path.join(A,"analise-documental.md"),"w",encoding="utf-8",newline="\n").write("\n".join(L)+"\n")
