# C1 — registro de tentativa bloqueada

## Estado

Experimento não realizado. A fonte normativa exclusiva solicitada,
`experimentacao\experimentacao-1\documentation\tool-readme-C2.md`, não existe
na árvore de trabalho nem no commit HEAD. Não foi possível verificar seu hash,
ler seus requisitos, derivar ou congelar oráculos ou proceder à inspeção e
execução do SUT. Nenhuma suíte foi gerada ou executada; Branch Coverage não foi
coletada. Taxas experimentais: não calculáveis (sem casos).

O protocolo informa o SHA-256 esperado da fonte C1:
`141C693DB506B2025D5EAD924C4C628660FEF7C163EC54BB7437C21FAA5C4856`.
Esse é o valor esperado, não uma verificação de arquivo disponível.
O arquivo `tool-readme-C1.md` encontrado na mesma pasta tem SHA-256
`91981FA0181E5CC1BC5A67DAAFC965BB82D6F8EB0A6D47EB58CE291A3EF5D33B`;
não foi lido nem usado como substituto. Também existe um arquivo homônimo em
`experimentacao\experimentacao-2\documentation`, de outra condição; não foi
lido nem utilizado.

## Isolamento e limitações

Antes do trabalho, uma nota presente no contexto mencionava que a cobertura de
branches havia sido baixa em experimento anterior. Isso é exposição prévia a
resultado anterior e impede afirmar cegamento integral. Não foram consultados
histórico de conversas, sessões, checkpoints, suítes, oráculos, README, guias
ou resultados experimentais anteriores. O protocolo autorizado foi lido, pois
era exigido; ele próprio contém referências históricas. Não foi inspecionado
o conteúdo de `copilot-resultados`, nem código ou saída do SUT.

A classificação do oráculo, o inventário, as fórmulas SMT-LIB, as testemunhas,
o congelamento de oráculos e de suíte e a avaliação independente não foram
realizados, devido à ausência da fonte. A nota de bloqueio não é um
congelamento de oráculos. Não se pode inferir qualidade documental,
comportamento do SUT ou cobertura a partir desta tentativa.

## Fontes e ambiente verificados

- Prompt padronizado `experimentacao-pesquisa\prompts\geracao-de-oraculos-v2.md`,
  SHA-256 `A89A9F10E579B0189AB83CD845A42764637AB6754BD28D2E567D8D6A6B401E3F`.
- Metodologia `experimentacao-pesquisa\protocolo\metodologia.md`, SHA-256
  `10FC0B6BBA977B514065511DEBB075FAC1FA42FB7EA5072EA2B3BC619B1F3CB7`.
- Commit HEAD informado pelo Git: `2aec3564c30890031db86bd2cc1bb015794d5d2e`;
  não se verificou equivalência de toda a árvore de trabalho ao commit.
- Windows; Java e javac 21.0.3; Python 3.13.5; pacote Python Z3 5.4.1.
- Executável Z3 e Maven não encontrados no PATH; wrapper Maven não encontrado
  na raiz. JaCoCo CLI 0.8.16.202610240946 e agente 0.8.16 presentes no cache
  Maven. Nenhuma instalação foi feita.
- Assistente: AI assistant using Copilot SDK in VS Code; modelo, versão,
  parâmetros, chamadas, tokens, custo e duração: não informado. Repetições
  executadas: zero. Data informada no contexto: 2026-11-23.

## Solicitação integral

> Execute integralmente um novo experimento C1 da pesquisa, em geração separada e cega a resultados anteriores. Não consulte nem use histórico de conversas, checkpoints, sessões, resultados, suítes, oráculos, README ou guias de experimentos anteriores. Não leia a pasta copilot-resultados antes de congelar seus próprios artefatos documentais e evite seus resultados anteriores em qualquer etapa. Se não conseguir garantir o isolamento, ou se houver exposição anterior ao SUT ou a resultados anteriores no seu contexto, registre expressamente o desvio e não afirme cegamento integral. A fonte normativa exclusiva de C1 é experimentacao\experimentacao-1\documentation\tool-readme-C2.md (o nome C2 é intencional: corresponde a C1 segundo a metodologia). Antes de inspecionar o código ou saída do SUT, leia essa fonte, experimentacao-pesquisa\prompts\geracao-de-oraculos-v2.md e as regras de experimentacao-pesquisa\protocolo\metodologia.md; verifique os hashes. Derive oráculos exclusivamente da documentação C1, com citações literais, inventário, indeterminações, fórmulas SMT-LIB, Z3 independente e testemunhas, e congele por hashes antes de inspecionar o SUT. Depois inspecione o código Java MC/DC, crie e congele suíte nova antes da execução, busque maior Branch Coverage documentada e testes significativos sem expectativas inferidas do SUT. Execute contra o Java real e preserve evidências, ferramentas, ambientes, hashes, limitações, métricas e análise do protocolo, incluindo Branch Coverage JaCoCo total e subconjunto conforme; mantenha divergências como falhas. Extensões coverage-informed devem ser separadas, com oráculos congelados antes de executar. Não colete Condition Coverage nem Mutation Score como métricas. Não altere fontes MC/DC, documentações normativas, metodologia ou quaisquer arquivos de experiências anteriores. Salve TODOS os artefatos novos e o relatório em copilot-resultados\C1 (use subdiretório novo e não sobrescreva artefatos preexistentes; se houver conflito de nome, crie subdiretório com data). Não altere o índice nem a documentação geral copilot-resultados, pois serão preparados separadamente. Confira ferramentas disponíveis antes de resolver bloqueios, inclusive Maven, cache JaCoCo, Python z3-solver e executável Z3. Preserve registro de prompt, resposta e metadados conhecidos; use 'não informado' para o que estiver ausente. Conclua o experimento end-to-end nesta sessão e informe o caminho do relatório e as limitações sem inventar execução. Esta solicitação não inclui resultados prévios.

## Resposta registrada

O experimento está bloqueado: a fonte normativa C1 exigida está ausente. Seu
hash esperado é o informado acima. Não houve execução do SUT nem coleta de
cobertura. Uma nota sobre cobertura anterior já estava presente no contexto;
portanto, não é possível declarar cegamento integral. Para prosseguir, é
necessário disponibilizar o arquivo exato no caminho solicitado e verificar
seu hash.
