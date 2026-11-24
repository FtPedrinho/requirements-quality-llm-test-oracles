# Relatório comparativo — experimentos C0–C4 executados pelo Claude

Este relatório reúne e compara as cinco execuções de `claude-opus-5.5-resultados/C0` a `C4`. Cada execução seguiu o
[protocolo comum](../experimentacao-pesquisa/protocolo/metodologia.md) e o
[prompt v3](../experimentacao-pesquisa/prompts/geracao-de-oraculos-v3.md), de forma independente das outras. A
comparação foi feita **depois** que as cinco terminaram. Os números abaixo foram conferidos contra os dados brutos
(`jacoco.csv` e `resultados.json` de cada rodada final), não só contra os READMEs. `gpt-6.1-terra-resultados/` não foi
usado.

## 1. Resumo das métricas finais

| Condição | Clareza / consistência pretendidas | Branch Coverage final | Aprovados | Falhos | Indeterminados | Casos | % indeterminados |
|---|---|---|---|---|---|---|---|
| C0 | original (sem nível atribuído) | 1097 / 1296 = **84,65%** | 92 | 1 | 14 | 107 | 13,1% |
| C1 | alta / alta | 1117 / 1296 = **86,19%** | 97 | 1 | 12 | 110 | 10,9% |
| C2 | baixa / alta | 1099 / 1296 = **84,80%** | 87 | 0 | 15 | 102 | 14,7% |
| C3 | alta / baixa | 859 / 1296 = **66,28%** | 40 | 0 | 39 | 79 | 49,4% |
| C4 | baixa / baixa | 500 / 1296 = **38,58%** | 44 | 1 | 37 | 82 | 45,1% |

Unidade de contagem em todas: caso do oráculo com ID estável. Denominador da cobertura em todas: as 69 classes
analisadas pelo JaCoCo 0.8.16 nos quatro módulos de produção (73 arquivos `.class`; o C1 registrou que as 4 restantes
não têm código executável ou são sintéticas), total de **1296 branches**. Os níveis de clareza/consistência são os
**pretendidos** pelo protocolo; não se presume que foram atingidos.

> **Atenção à comparabilidade da cobertura.** C0, C1 e C2 executaram os casos indeterminados como diagnóstico, e o
> `jacoco.exec` dessas rodadas inclui essas execuções. C3 (rodada final r4) e C4 seguiram a regra do pesquisador
> definida durante o C3: indeterminado não é teste, não é executado e não entra na cobertura. Logo a Branch
> Coverage de C0–C2 **não é diretamente comparável** à de C3–C4. O único dado sobre o tamanho desse efeito é o do
> C3: com os indeterminados executados (r3) a cobertura era 1056/1296 = 81,48%; sem eles (r4), 66,28%. Para C0–C2 a
> cobertura só dos determinados **não foi medida** (não informado). Aprovados, falhos e indeterminados são
> comparáveis entre as cinco.

### Baseline (antes de extensões) e fases

| Condição | Baseline | Extensões | Final |
|---|---|---|---|
| C0 | rodada 2 (com correção de entradas): 80,25%, 72 / 0 / 13 | extensão 1 (22 casos): 72,30% sozinha, 20 / 1 / 1 | acumulado |
| C1 | rodada 02 (com correção do harness): 80,40%, 70 / 0 / 9 | extensão 01 (31 casos): 70,22% sozinha, 27 / 1 / 3 | acumulado |
| C2 | r1: 83,02%, 75 / 0 / 15 | r2 (12 casos): 69,52% sozinha, 12 / 0 / 0 | acumulado |
| C3 | r1: 78,40% (3 inválidos); r3 refeita: 81,48% | r2 (correção + extensão; diagnósticos I40–I47 depois removidos) | r4: só determinados |
| C4 | r1-baseline: 38,58%, 44 / 1 / 37 | nenhuma | r1-baseline |

Formato: cobertura, aprovados / falhos / indeterminados.

### Cobertura final por módulo (branches cobertos / total)

| Módulo | C0 | C1 | C2 | C3 | C4 |
|---|---|---|---|---|---|
| `mcdc-core` (/411) | 348 | 371 | 346 | 327 | 277 |
| `mcdc-requirements` (/162) | 138 | 141 | 130 | 123 | 114 |
| `mcdc-z3` (/386) | 314 | 313 | 322 | 204 | **0** |
| `mcdc-cli` (/337) | 297 | 292 | 301 | 205 | 109 |
| **Total** (/1296) | 1097 | 1117 | 1099 | 859 | 500 |

## 2. Divergências encontradas (FALHOU)

| Condição | Caso | Expectativa documental | Observado |
|---|---|---|---|
| C0 | C0-X13 | Erro no CSV de testes informa o número da linha (`InputEdgeCasesTest`) | `Erro: T1: valor lógico inválido: X` (cita o teste, não a linha) |
| C1 | EX-27 | Opções que exigem Z3 avisam quando ele não está instalado; `verify` usa o Z3 | `verify` sem Z3 no PATH terminou com código 0, sem aviso (entrada com uma só decisão, nenhuma consulta necessária) |
| C2 | — | — | nenhuma |
| C3 | — | — | nenhuma |
| C4 | C4-D26 | Erro de sintaxe em requisito informa o número da linha (`InputEdgeCasesTest`) | `Erro: REQ-B: Faltou fechar parêntese` (cita o requisito, não a linha) |

C0 e C4 chegaram, de forma independente e a partir de textos diferentes, à mesma divergência: a frase sobre "número
da linha no erro" não se confirma no sistema (um para o CSV de testes, outro para o `.mcdc`). Nos dois casos o
relatório registra que a frase não diz a qual entrada se aplica, o que é uma ameaça à validade da expectativa.

## 3. Detalhes da experimentação realizada pelo Claude

### Configuração comum

- **Modelo:** Claude Opus 5.5 (`claude-opus-5-5`) no Claude Code (app desktop); cada condição em uma sessão
  separada, iniciada por outra sessão. Temperatura e demais parâmetros: não informado.
- **Ferramentas:** Java 21.0.3, Python 3.13.5, Z3 5.4.1 independente (`z3.exe`), JaCoCo 0.8.16, Jackson 2.17.2.
  Maven não funcionou offline; em todas as condições o SUT foi compilado com `javac --release 21` a partir de
  `git archive`, fora do repositório.
- **SUT:** C0 usou o commit `03589c4`, C1 `92d9df8` e C2–C4 `ed7d2e0`. `git diff 03589c4 ed7d2e0` nos quatro
  módulos é vazio: o código avaliado é o mesmo nas cinco condições.
- **Procedimento comum:** hash da fonte → leitura integral → inventário → consultas SMT-LIB no Z3 independente →
  oráculo congelado por SHA-256 antes de ler ou executar o SUT → build → leitura da CLI só para invocar e localizar
  dados → suíte congelada → rodadas com o agente JaCoCo → relatório. Revisão sempre própria (sem revisor
  independente).

### Por condição

| | C0 | C1 | C2 | C3 | C4 |
|---|---|---|---|---|---|
| Casos no baseline (det. / indet.) | 85 (72 / 13) | 79 (70 / 9) | 90 (75 / 15) | 75 + extensão → 79 (40 / 39) | 82 (45 / 37) |
| Consultas Z3 | 94 + 42 (extensão) | 63 arquivos + 48 (extensão) | 118 + 6 (extensão) | 106 + 6 (extensão) | 26 |
| Erro técnico do Z3 | 1 timeout, trocado por lemas | nenhum | nenhum | nenhum | nenhum |
| Correções pós-congelamento | entradas JSON com `/\` inválido (C07–C09) | codificação do stdout no harness (AN-22) | nenhuma | IDs de decisão nos CSVs (T20–T22 inválidos); remoção de I40–I47 | nenhuma |
| Indeterminados executados para a cobertura | sim (diagnóstico) | sim (diagnóstico) | sim (diagnóstico) | não (r4) | não |
| Observação principal | JSON e texto | JSON, CSV e texto | uma invocação por caso, JSON auxiliar | uma execução julgada por vários casos | uma execução julgada por vários casos; só JSON |
| Perdas de isolamento registradas | defeito de entrada notado pela mensagem do SUT | nenhuma | nome de arquivo de nota visto; títulos de C0/C1 vistos após concluir | nome da pasta C2 no `git status` | dois arquivos de entrada não citados exibidos |

### Políticas de interpretação que diferem

- **Lacunas do texto (C2 e C4):** o C2 reconstruiu uma palavra só quando outro trecho legível a fixava; o C4 não
  reconstruiu operandos apagados dos exemplos (o `A` sumiu) e usou expressões próprias para as regras em prosa.
- **Conflitos (C3 e C4):** os dois adotaram a mesma política: uma passagem que se declara prevalente ("substitui
  a anterior") é parte do conflito, não regra de precedência. Quando todas as leituras dão o mesmo resultado
  (verificado no Z3), o caso fica determinado; quando divergem, indeterminado. O C3 registra que outra política
  produziria mais expectativas e, possivelmente, falhas.
- **Regra de cobertura:** a exclusão dos indeterminados foi decidida pelo pesquisador durante o C3 e aplicada ao
  C4; C0–C2 terminaram antes dela.

## 4. Avaliação: como a documentação afetou oráculos e suítes

1. **Documentação clara e consistente (C0, C1).** Menos indeterminados (11–13%), cobertura acima de 84% e uma
   falha cada. Uma documentação forte gera asserções específicas (mensagens, avisos, números), e é aí que
   aparecem divergências: as duas falhas são em detalhes que o texto afirma com precisão.
2. **Clareza baixa com consistência alta (C2).** A degradação atingiu sobretudo a prosa; tabelas, opções e números
   ficaram legíveis. O percentual de indeterminados subiu pouco (14,7%) e não houve falhas, mas parte das
   expectativas dependeu de reconstruir lacunas, o que transfere o peso para a interpretação de quem lê.
3. **Consistência baixa (C3, C4).** É o fator que mais pesou: cerca de metade dos casos ficou indeterminada (49% e
   45%). As contradições atingiram o núcleo do MC/DC (critério de par, sat/unsat, gulosa × exata, redundante ×
   bloqueada, formatos csv/truth-csv, uso do Z3). O efeito não é mais falhas, e sim **perda de poder de detecção**:
   o oráculo só consegue afirmar propriedades comuns a todas as leituras, e o código ligado aos conflitos fica sem
   cobertura julgada (`mcdc-z3` com 204/386 no C3 e 0/386 no C4).
4. **As duas qualidades baixas (C4).** Somam-se os efeitos: a baixa clareza apagou os exemplos que dariam
   expectativas concretas ("4 testes", "5 em vez de 6"), e a baixa consistência tornou indeterminado tudo o que
   depende do Z3. No C4, o Z3 independente mostrou que a regra "sat = impossível" contradiz os números medidos da
   própria fonte (4/4/1 impossíveis na leitura original; 148/264/75 na regra invertida). A suíte alcançou só o
   caminho booleano sem Z3: 38,58% de branches.
5. **Ordem observada (só como descrição).** Pela proporção de indeterminados: C1 < C0 < C2 < C4 < C3; pela
   cobertura só com determinados (onde medida): C3 (66,28%) > C4 (38,58%). A consistência baixa separa
   claramente C3/C4 de C0–C2; a diferença entre clareza alta e baixa é menor que a de consistência nesta amostra.

## 5. Limitações da comparação

- **Uma execução por condição**, com o mesmo modelo: não há medida de variação entre execuções; diferenças
  pequenas (ex.: 84,65% × 84,80% × 86,19%) não devem ser interpretadas.
- **Cobertura não homogênea:** C0–C2 incluem diagnósticos de indeterminados; C3–C4 não (seção 1).
- **Procedimentos diferentes:** quantidade de extensões, correções, formato de observação, unidade de execução e
  políticas de interpretação variaram; parte da diferença pode vir do procedimento, não da documentação.
- **Autorrevisão** em todas as condições; a tradução texto → fórmula não tem revisor independente, e `sat`/`unsat`
  não provam fidelidade.
- **Sem inferência causal:** o protocolo pede não inferir causalidade sem controles; as relações acima descrevem a
  amostra.
- **Isolamento:** todas registram que não é possível demonstrar ausência de influência de conhecimento prévio do
  modelo; as perdas pontuais estão na seção 3.

## 6. Onde estão os dados

| Condição | README | Relatório | Resultados por caso | Rodada final |
|---|---|---|---|---|
| C0 | [C0/README.md](C0/README.md) | [relatorio.md](C0/avaliacao/relatorio.md) | [resultados-por-caso.md](C0/avaliacao/resultados-por-caso.md) | `C0/resultados/acumulado-rodada2-extensao1/` |
| C1 | [C1/README.md](C1/README.md) | [relatorio.md](C1/avaliacao/relatorio.md) | [resultados-por-caso.md](C1/avaliacao/resultados-por-caso.md) | `C1/resultados/acumulado/` |
| C2 | [C2/README.md](C2/README.md) | [relatorio.md](C2/avaliacao/relatorio.md) | [resultados-por-caso.md](C2/avaliacao/resultados-por-caso.md) | `C2/resultados/acumulado/` |
| C3 | [C3/README.md](C3/README.md) | [relatorio.md](C3/avaliacao/relatorio.md) | [resultados-por-caso.md](C3/avaliacao/resultados-por-caso.md) | `C3/resultados/r4/` |
| C4 | [C4/README.md](C4/README.md) | [relatorio.md](C4/avaliacao/relatorio.md) | [resultados-por-caso.md](C4/avaliacao/resultados-por-caso.md) | `C4/resultados/r1-baseline/` |
