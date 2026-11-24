# C0 — reinício de 21/11/2026

**Resultado C0 único e oficial do Copilot**, adotado por decisão do
pesquisador em 21/11/2026. A adoção não altera os resultados nem as
limitações da execução.

Após a realocação do relatório, os links abaixo foram atualizados. Os
manifestos originais preservam os hashes e caminhos registrados à época;
o [registro da atualização](detalhes-C0/atualizacao-links.txt) identifica esta versão.

## Limitação crítica de isolamento

**Não houve cegamento contextual integral.** A própria fonte normativa
obrigatória contém tabelas de resultados e descrições de suítes anteriores,
expostas durante sua leitura integral. O contexto inicial também continha
uma nota genérica de metodologia de cobertura e uma instrução anterior de
pesquisa. Esses dados não foram usados para selecionar casos nem definir
expectativas. Não foram abertos nem executados arquivos de suítes, oráculos
ou resultados antigos. O índice de resultados, necessário à atualização
pedida, foi lido apenas para essa edição; embora se chame `README.md`, não
foi usado como guia nem como fonte normativa. Esta exposição compromete a
validade de qualquer alegação de geração cega ou plenamente isolada.

## Método e rastreabilidade

Uma repetição C0 no commit `2aec3564c30890031db86bd2cc1bb015794d5d2e`;
fontes Java de produção sem diferenças rastreadas no momento da compilação.
Fonte normativa exclusiva:
[documentação original](../../experimentacao-pesquisa/documentacao-original/tool-readme-original.md),
SHA-256 `72B827BDEE6CE859527765CFF574A473519C00A1AF9AA9F3AACCE4236A4995F8`.
Prompt operacional
[v2](../../resultados-llm/prompts/geracao-de-oraculos-v2.md), SHA-256
`A89A9F10E579B0189AB83CD845A42764637AB6754BD28D2E567D8D6A6B401E3F`;
[metodologia da pesquisa](../../experimentacao-pesquisa/protocolo/metodologia.md), SHA-256 na execução
`10FC0B6BBA977B514065511DEBB075FAC1FA42FB7EA5072EA2B3BC619B1F3CB7`.
Foi registrado o [pedido integral](../../resultados-llm/experimentos/C0/reinicio-2026-11-21/pedido-integral.md)
e uma cópia integral do prompt operacional. A
[resposta final](../../resultados-llm/experimentos/C0/reinicio-2026-11-21/resposta-integral.md)
também foi preservada.

Análise, citações, regras, omissões e oráculos do baseline foram congelados
antes da inspeção das fontes Java. O Python z3-solver independente 5.4.1
enumerou valorações e produziu consultas SMT-LIB, resultados e testemunhas.
`sat` não valida a tradução documental. Após a inspeção, os casos e o
harness foram congelados antes da execução. As duas extensões orientadas pela
cobertura têm oráculos, entradas e provas independentes congelados antes de
suas respectivas execuções. As expectativas não foram adaptadas aos
resultados. Não houve revisor independente: a classificação é autoavaliação
da IA.

Documentação C0 descreve comandos, operadores, exemplos e limites, mas omite
detalhes de representação, mensagens e diversas interações de opções. Não
se atribui artificialmente nível alto/baixo de clareza ou consistência. Não
foi identificado conflito documental aplicável aos casos avaliados.

## Branch Coverage JaCoCo

Instrumentação JaCoCo **0.8.16**, fontes Java de produção dos quatro módulos,
69 classes analisadas, inclusive classes não carregadas; classes de testes,
dependências externas e harness excluídos. O denominador é o mesmo em todas
as linhas. O pacote de mutação integra o denominador de produção, mas não foi
executado para coletar notas de mutação. O relatório XML bruto contém outros
contadores padrão do JaCoCo; somente branches são analisados como cobertura.

| Rodada | Cobertos / total | Branch Coverage total | Subconjunto conforme |
|---|---:|---:|---:|
| Baseline | 290 / 1.296 | 22,38% | 290 / 1.296 — 22,38% |
| Extensão 1 isolada | 778 / 1.296 | 60,03% | 778 / 1.296 — 60,03% |
| Baseline + extensão 1 | 817 / 1.296 | 63,04% | 817 / 1.296 — 63,04% |
| Extensão 2 isolada | 430 / 1.296 | 33,18% | 430 / 1.296 — 33,18% |
| Todas combinadas | **847 / 1.296** | **65,35%** | **847 / 1.296 — 65,35%** |

Ganhos cumulativos: +527 branches na extensão 1 e +30 na extensão 2.
O subconjunto é igual ao total porque apenas os casos conformes foram
executados; indeterminados não foram executados. Esta é a melhor cobertura
observada nesta busca, não uma máxima global. Permaneceram 449 branches não
cobertos, incluindo caminhos sem expectativa textual única; exemplos
registrados em
[indeterminados pós-cobertura](../../resultados-llm/experimentos/C0/reinicio-2026-11-21/indeterminados-pos-cobertura.json).
Não foi feita busca exaustiva de todos os comportamentos documentados.

## Contagens e taxas

Uma unidade é um caso/oráculo. Os três casos indeterminados descobertos na
inspeção entram no baseline; cinco descobertos após a cobertura entram no
registro posterior. Não foram executados nem julgados semanticamente.

| Rodada | Gerados | Executados | Passaram | Falharam | Indeterminados | Inválidos | Erros técnicos |
|---|---:|---:|---:|---:|---:|---:|---:|
| Baseline | 67 | 64 | 64 | 0 | 3 | 0 | 0 |
| Extensão 1 | 21 | 21 | 21 | 0 | 0 | 0 | 0 |
| Extensão 2 | 13 | 13 | 13 | 0 | 0 | 0 | 0 |
| Registro pós-cobertura | 5 | 0 | 0 | 0 | 5 | 0 | 0 |
| **Total** | **106** | **98** | **98** | **0** | **8** | **0** | **0** |

- Estruturalmente válidos e executáveis pelo harness implementado: 98/106;
  oito indeterminados foram registrados como observações, mas não foram
  implementados para execução diagnóstica. Executabilidade: **92,45%**.
- Aprovação bruta e dos conformes: **98/98 = 100%**; sem oráculos
  incorretos/sem suporte avaliados, cuja taxa de aprovação é não calculável.
- Indeterminação: **8/106 = 7,55%**. Incorretos/sem suporte: **0/106**;
  inválidos: **0/106**.
- Conformidade documental autoavaliada: **98/(98+0) = 100%**; divergência
  documentação–SUT: **0/98 = 0%**. São conclusões relativas ao texto,
  não prova de correção objetiva do sistema ou do documento.
- Duração de execução medida: baseline 38,936 s; extensão 1 43,712 s;
  extensão 2 29,561 s, incluindo geração de relatórios de cada executor.
  Duração exata de geração: não informado. Chamadas, tokens, preço,
  custo, modelo/versão e parâmetros da plataforma: não informado.

## Ambiente e evidências

Windows 10.0.26200, AMD64; Java/Javac 21.0.3; Python 3.13.5;
z3-solver Python 5.4.1; Jackson 2.17.2; JaCoCo 0.8.16. Maven não
estava disponível no PATH; compilação feita diretamente com `javac`,
sem usar `target` ou testes preexistentes. Z3 executável não estava no
PATH nem nos locais procurados; após a verificação de indisponibilidade
foi obtida a distribuição oficial Windows 4.13.3 em
`https://github.com/Z3Prover/z3/releases/download/z3-4.13.3/z3-4.13.3-x64-win.zip`
e usada localmente apenas nos subprocessos da extensão. A distribuição,
executável e DLL estão preservados e têm hashes no manifesto. O binário
baixado não teve assinatura ou hash oficial independente verificado.
O hash das fontes e dependências usadas na compilação está em
[`compilacao.json`](../../resultados-llm/experimentos/C0/reinicio-2026-11-21/compilacao.json).

Artefatos da rodada em
[reinicio-2026-11-21](../../resultados-llm/experimentos/C0/reinicio-2026-11-21/):
[análise](../../resultados-llm/experimentos/C0/reinicio-2026-11-21/analise-documental.md),
[oráculos](../../resultados-llm/experimentos/C0/reinicio-2026-11-21/oraculos.json),
[evidências Z3](../../resultados-llm/experimentos/C0/reinicio-2026-11-21/z3-evidencias.json),
[congelamento documental](../../resultados-llm/experimentos/C0/reinicio-2026-11-21/congelamento-documental.txt),
[congelamento baseline](../../resultados-llm/experimentos/C0/reinicio-2026-11-21/congelamento-baseline.txt),
[congelamento extensão 1](../../resultados-llm/experimentos/C0/reinicio-2026-11-21/congelamento-extensao.txt)
e [extensão 2](../../resultados-llm/experimentos/C0/reinicio-2026-11-21/congelamento-extensao2.txt).
O [manifesto final](../../resultados-llm/experimentos/C0/reinicio-2026-11-21/manifesto-final.txt)
registra hashes das evidências e das versões do relatório e índice anteriores
à adoção oficial. Os hashes posteriores à adoção estão no
[registro de adoção](../../resultados-llm/experimentos/C0/reinicio-2026-11-21/adocao-oficial.txt).
Resultados individuais e saídas estão em
[baseline](../../resultados-llm/experimentos/C0/reinicio-2026-11-21/baseline-resultados.json),
[extensão 1](../../resultados-llm/experimentos/C0/reinicio-2026-11-21/extension-resultados.json)
e [extensão 2](../../resultados-llm/experimentos/C0/reinicio-2026-11-21/extension2-resultados.json);
execuções `check` preservam hash de stdout e resultados pertinentes, não
as métricas adicionais da ferramenta. Dados instrumentados e relatórios
XML de cada rodada e agregados estão no mesmo diretório. A reprodução
requer os mesmos JARs em cache ou ajuste explícito dos caminhos do executor;
os executores recusam sobrescrever resultados existentes.
