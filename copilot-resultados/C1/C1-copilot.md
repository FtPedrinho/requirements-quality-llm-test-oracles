# Experimento C1 — relatório final

Esta é uma cópia de acesso reorganizada do
[relatório congelado](detalhes-C1/relatorio-final.md). Após o congelamento,
`metodologia-utilizada.md` foi alterada por fora desta reorganização e foi
preservada. A [metodologia](metodologia.md) nesta raiz foi copiada do
protocolo cujo hash corresponde ao registrado no experimento. Detalhes e
novos hashes constam no [registro de reorganização](detalhes-C1/reorganizacao.md).

## Conclusão e desvios

Uma geração documental, um baseline e duas extensões foram executados nesta
sessão contra o Java real. Melhor Branch Coverage acumulada: **872/1296
(67,28%)**, tanto no total como no subconjunto conforme/executável usado
abaixo. Não se afirma cobertura máxima global.

**Não houve cegamento integral.** Antes da geração, o contexto já continha uma
nota sobre cobertura baixa anterior. Além disso, a fonte C1 autorizada contém
resultados e descrições de testes históricos, aos quais houve exposição na
leitura. Esses resultados não foram usados para formular expectativas. Não
foram consultados resultados, suites ou oráculos externos à fonte, histórico
de conversas, checkpoints ou outras sessões.

A fonte originalmente indicada, `tool-readme-C2.md` em experimentação 1,
estava ausente. Por decisão expressa posterior do pesquisador, foi substituída
por `tool-readme-C1.md`, e o protocolo foi atualizado com seu caminho e hash.
Isto muda a referência congelada do desenho anterior e restringe comparações
com experimentos que utilizaram outra fonte. O documento C1 não foi alterado
pelo executor; seu estado anterior à tarefa já aparecia como modificado no
Git. O protocolo já era não rastreado no início. O registro inicial de
bloqueio está em [relatorio.md](detalhes-C1/relatorio.md).

## Fontes, congelamento e solver

| Entrada | SHA-256 |
|---|---|
| [Fonte C1 utilizada](detalhes-C1/fonte-normativa-C1.md) | `91981FA0181E5CC1BC5A67DAAFC965BB82D6F8EB0A6D47EB58CE291A3EF5D33B` |
| [Protocolo atualizado](metodologia.md) | `EC3F96C59C6C2A3570E7833B2C561B6DB38BE415B41C10A7F383BF5DA2FA6B1F` |
| Protocolo antes da mudança autorizada | `10FC0B6BBA977B514065511DEBB075FAC1FA42FB7EA5072EA2B3BC619B1F3CB7` |
| [Prompt padronizado](detalhes-C1/prompt-padronizado.md) | `A89A9F10E579B0189AB83CD845A42764637AB6754BD28D2E567D8D6A6B401E3F` |

A referência anterior ausente tinha hash **esperado**, não verificado,
`141C693DB506B2025D5EAD924C4C628660FEF7C163EC54BB7437C21FAA5C4856`.
Análise, citações, inventário, indeterminações e casos: [oraculos.md](detalhes-C1/oraculos.md).
O Z3 Python independente 5.4.1 produziu 51 consultas: 26 `sat`, 25 `unsat`,
zero `unknown`; [fórmulas](detalhes-C1/formulas.smt2) e [resultados](detalhes-C1/z3-resultados.json).
A primeira extensão acrescentou 14 consultas `sat` com testemunhas:
[fórmulas](detalhes-C1/extensao-formulas.smt2), [resultados](detalhes-C1/extensao-z3.json).
Z3 não prova fidelidade da tradução ao texto. A revisão foi autoavaliação da
IA; não houve revisor independente.

Os hashes de análise e evidências foram fixados às 07:26:39-03:00 em
[congelamento-documental.sha256](detalhes-C1/congelamento-documental.sha256), antes da
inspeção do código. A versão final da suíte baseline foi congelada às
07:31:44-03:00 em [congelamento-suite-v2.sha256](detalhes-C1/congelamento-suite-v2.sha256),
antes da execução. Uma primeira versão do manifesto também foi preservada;
ela antecede um reparo feito antes de qualquer execução e não identifica a
suíte efetivamente executada.

Após o baseline, a extensão E1 foi congelada em
[congelamento-extensao.sha256](detalhes-C1/congelamento-extensao.sha256). A primeira
tentativa terminou por erro de ambiente antes de iniciar qualquer caso; seu
executor foi preservado, corrigido e novamente congelado em
[congelamento-extensao-v2.sha256](detalhes-C1/congelamento-extensao-v2.sha256), às
08:05:40-03:00. A extensão E2 foi congelada em
[congelamento-extensao2.sha256](detalhes-C1/congelamento-extensao2.sha256), às
08:10:10-03:00, antes de sua execução. Todos esses hashes foram verificados.

## Ambiente e escopo

- HEAD: `2aec3564c30890031db86bd2cc1bb015794d5d2e`; nenhuma alteração nas
  fontes Java de produção foi listada no status Git. Os hashes individuais das
  51 fontes utilizadas estão em [fontes-java.sha256](detalhes-C1/fontes-java.sha256).
- Windows x64, Java/Javac 21.0.3, Python 3.13.5. Maven e executável Z3 não
  estavam no PATH; não se usou Maven. Compilação real com javac para
  [classes](detalhes-C1/classes/) e Jackson 2.17.2 em cache; comando e resultado em
  [compilacao.json](detalhes-C1/compilacao.json).
- JaCoCo 0.8.16.202610240946, agente e CLI do cache; hashes em
  [dependencias.sha256](detalhes-C1/dependencias.sha256). Escopo fixado: todas as 69
  classes de produção compiladas dos quatro módulos, inclusive classes
  internas e código de mutação; dependências externas, JDK e harness excluídos.
  Nenhum módulo de produção foi excluído. As classes de mutação permanecem no
  denominador, mas não foi executada análise de mutação.
- Z3 CLI 4.13.4 obtido da distribuição oficial depois da confirmação de
  ausência; arquivo local SHA-256
  `0A36DD5654FE423D23A727C4570C9DB9A315926A4301189B868B6EB9BFD5979D`.
  Apenas os processos que o requerem receberam seu diretório no PATH; B31/E01
  exercitam ausência deliberada. O solver Python para os oráculos é distinto.
- Modelo/versão/configuração, número de chamadas, tokens, custo e duração da
  geração: **não informado**. Plataforma: Copilot SDK no VS Code. Uma
  repetição; não é possível tirar conclusão causal entre condições. Datas e
  instruções do pesquisador em [registro](detalhes-C1/registro.md).

## Cobertura de branches

| Rodada | Total | Subconjunto conforme, estruturalmente válido e com avaliação técnica concluída |
|---|---:|---:|
| Baseline | 771/1296 = 59,49% | 771/1296 = 59,49% |
| E1 isolada | 571/1296 = 44,06% | 525/1296 = 40,51% |
| Baseline + E1 | 872/1296 = 67,28% | 839/1296 = 64,74% |
| E2 isolada | 197/1296 = 15,20% | 197/1296 = 15,20% |
| Acumulado final | **872/1296 = 67,28%** | **872/1296 = 67,28%** |

E1 aumentou o acumulado total em 101 branches (7,79 pontos percentuais).
E2 não aumentou o total, mas elevou o subconjunto conforme em 33 branches
(2,54 pontos), ao substituir em cobertura as asserções sem suporte de E02.
O subconjunto conservador exclui B31, cuja avaliação teve erro de decodificação,
e E02, cuja asserção não tinha suporte; inclui testes conformes que falharam.
Cada processo produziu seu próprio arquivo `.exec`; os relatórios brutos
incluem [baseline total](detalhes-C1/baseline/jacoco-total.xml),
[baseline conforme](detalhes-C1/baseline-conforme.xml),
[E1 total](detalhes-C1/extensao-total.xml), [E1 conforme](detalhes-C1/extensao-conforme.xml),
[acumulado E1 total](detalhes-C1/acumulado-total.xml),
[acumulado E1 conforme](detalhes-C1/acumulado-conforme.xml),
[E2](detalhes-C1/extensao2-total.xml), [final total](detalhes-C1/final-total.xml) e
[final conforme](detalhes-C1/final-conforme.xml), acompanhados dos `.exec`.

No resultado final: core, incluindo modelo e mutação, 271/411; requirements
115/162; Z3 255/386; CLI 231/337 branches. O escopo não permite atribuição
causal nem comparação automática com outros ambientes.

## Casos, erros e taxas

Há 51 casos com chamadas reais, mais cinco registros indeterminados I01–I05.
Embora a análise inicialmente os tenha chamado de lacunas gerais, eles
receberam IDs e classificações; por prudência são contabilizados como cinco
oráculos indeterminados, sem entrada concreta e não executáveis, em vez de
serem omitidos do denominador. Foram gerados **56** registros; **51**
estruturalmente válidos e executáveis; **51** executados; **48** aprovações,
**2** falhas de asserção, **1** erro técnico na avaliação e **5**
indeterminados sem julgamento. Oráculos: 50 conformes, 1 incorreto/sem
suporte, 0 inválidos e 5 indeterminados. Os registros brutos continuam
inalterados; as correções de classificação abaixo são explicitadas em vez
de modificar os resultados gerados pelo harness.

| Taxa | Cálculo | Resultado |
|---|---:|---:|
| Executabilidade | 51/56 | 91,07% |
| Aprovação bruta, sobre asserções avaliadas | 48/50 | 96,00% |
| Aprovação com oráculo conforme | 48/49 | 97,96% |
| Aprovação com oráculo sem suporte | 0/1 | 0,00% |
| Indeterminação | 5/56 | 8,93% |
| Conformidade documental, excluindo indeterminados | 50/51 | 98,04% |
| Oráculos incorretos/sem suporte | 1/56 | 1,79% |
| Inválidos | 0/56 | 0,00% |
| Divergência documentação–SUT, entre conformes conclusivos | 1/49 | 2,04% |

Baseline: 36 registros incluindo I01–I05; 31 executados, 29 aprovações,
uma divergência e um erro de avaliação. E1: 19 executados, 18 aprovados e
uma falha sob asserção sem suporte; houve ainda uma tentativa inicial de
executor que falhou antes dos casos por erro técnico de infraestrutura.
E2: um caso executado e aprovado. A soma de durações registradas é 81,502 s
no baseline, 74,771 s em E1 e 2,468 s em E2; E01 não registrou duração,
portanto esses valores não são duração total exata. B12 repete B02 e B14
repete a chamada de B03: são contabilizados, mas são redundâncias, não
evidência de testes adicionais significativos. E01 e E20 são repetições
separadas para tratar problemas dos executores.

### Revisão das falhas preservadas

- **B23 — divergência documentação/SUT.** A documentação exemplifica
  `speed > 100` com fronteiras 100 e 101. Para a expressão com dois limiares,
  foram relatadas fronteiras 100, 50 e 51, mas não 101 como variante de
  fronteira; 101 aparece como atribuição de linha da tabela, não como variante
  de fronteira. A asserção continua falha. A leitura de que ambas as variantes
  são exigidas mesmo quando a suíte não contém uma linha-base verdadeira para
  o primeiro predicado é uma interpretação literal a revisar; não prova qual
  fonte representa a intenção original. [Evidência](detalhes-C1/baseline/B23.json).
- **B31 — erro técnico de avaliação, não divergência.** O processo emitiu um
  aviso de Z3 ausente, mas o executor decodificou incorretamente o stderr
  Windows e comparou texto com substituição Unicode. O resultado bruto
  erroneamente marcado como falha permanece em [B31](detalhes-C1/baseline/B31.json).
  E01 repetiu o teste com bytes e codificação preservados e passou:
  [evidência](detalhes-C1/extensao-v2/E01.json).
- **E02 — oráculo incorreto/sem suporte.** O executor exigiu a palavra
  literal “tabela”, não exigida pelo texto, embora a saída contenha as quatro
  linhas. A falha bruta permanece em [E02](detalhes-C1/extensao-v2/E02.json); não é
  divergência. E20 testa conteúdo, pares e suíte sem essa suposição:
  [evidência](detalhes-C1/extensao2/E20.json).

As classificações corrigidas acima são uma auditoria posterior transparente;
as classificações iniciais e asserções congeladas não foram apagadas nem
reescritas. Não há erro `unknown` ou `timeout` no Z3 independente. Os
resultados por caso estão em [baseline](detalhes-C1/baseline/resultados.json),
[E1](detalhes-C1/extensao-v2/resultados.json) e [E2](detalhes-C1/extensao2/resultados.json).

## Limitações e reprodução

Os casos cobrem parte do inventário, não todos os comportamentos, configurações,
limites ou branches. A análise coverage-informed foi limitada a duas
extensões; mensagens específicas, formatos incompletamente especificados e
branches sem apoio documental não ganharam expectativas inferidas do código.
Foram mantidos os branches das classes de mutação no denominador, embora a
análise de mutação não tenha sido executada. Nenhuma métrica de cobertura de
condições ou de mutação foi coletada. Saídas de `check` tiveram campos de
resultados de condições removidos antes de serem salvos, conforme
[mapeamento](detalhes-C1/mapeamento-baseline.md).

O harness e as entradas estão no diretório desta rodada; os comandos são
`python suite-baseline.py`, `python extensao-suite-v2.py` e
`python extensao2-suite.py`, nesta ordem, com pré-requisitos descritos no
mapeamento. Uma cópia da suíte está em [suite](suite/). Para não sobrescrever evidências, reproduzir somente em um novo
subdiretório equivalente e verificar os hashes e caminhos antes de iniciar.
Os logs, arquivos de dados e classes da rodada atual não substituem uma
avaliação independente nem asseguram comparabilidade entre máquinas.
