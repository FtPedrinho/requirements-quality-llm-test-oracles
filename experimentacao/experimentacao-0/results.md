# Resultados — Experimento C0

## Síntese

C0 é uma linha de base exploratória com duas trilhas distintas: (1) análise formal e mutação de expressões de VM/TIS/NPP; e (2) testes JUnit/PIT da ferramenta MC/DC. Os resultados não medem a mesma população e não devem ser somados.

## Trilha formal VM/TIS/NPP

- 36 expressões/requisitos analisados; 33 decisões NAT2TEST e 3 expressões gerais.
- 36 oráculos e 152 casos simbólicos registrados, incluindo 119 pares MC/DC.
- 185 casos na versão executável do modelo: 173 concretizáveis e 12 não concretizados.
- 981 mutantes de especificação: 894 mortos, 42 sobreviventes, 21 equivalentes e 24 não avaliáveis.
- O relatório histórico apresenta Mutation Score de 93,125% quando os não avaliáveis permanecem no denominador e 95,513% quando são excluídos junto com equivalentes. As duas convenções são mantidas explícitas; nenhuma representa PIT sobre o código Java.
- Os relatórios também divergem em Recall/F1 entre execuções/agregações (95,5%/97,7% e 90,92%/95,24%). Sem unidade harmonizada, não se escolhe um número único como resultado comparável.

## Trilha da ferramenta Java

O resumo consolidado registra 25 testes JUnit aprovados e 320 mutantes PIT mortos de 333 (96,096%). Estes valores pertencem à suíte de regressão da ferramenta e não validam a semântica dos oráculos VM/TIS/NPP.

## Métricas da pesquisa

Não há valores C0 comparáveis para cobertura de requisitos, Precision, Recall ou F1 sobre o gabarito independente de 19 comportamentos usado em C2/C3. C0 precede essa referência e não é uma condição experimental controlada.

## Limitações

Os mutantes da trilha formal são mutações da especificação/modelo, não defeitos de implementações VM/TIS/NPP. A execução JUnit/PIT da ferramenta avalia outro alvo. A proveniência dos oráculos não está completamente reconciliada entre os registros históricos; por isso, os números não sustentam uma conclusão causal sobre qualidade documental.
