# Caracterização do repositório como dataset

## 1. Origem

O dataset é o próprio repositório **Ferramenta MC/DC**, localizado neste fork. Ele não representa uma única aplicação de negócio; é uma ferramenta Java de geração e avaliação de testes, acompanhada de exemplos derivados de três sistemas e de relatórios históricos.

O repositório fornece como fontes potenciais:

- requisitos expressos como guardas lógicas;
- textos naturais associados a algumas decisões JSON;
- implementação da ferramenta;
- testes JUnit;
- suítes geradas em CSV;
- tabelas verdade e relatórios em JSON/CSV;
- relatórios de cobertura e mutação já existentes.

## 2. Estrutura

Diretórios principais:

- `mcdc-core/`: núcleo de expressões e MC/DC;
- `mcdc-requirements/`: leitores de entradas;
- `mcdc-z3/`: integração com Z3;
- `mcdc-cli/`: interface de linha de comando;
- `exemplos/`: `.mcdc`, JSON, CSV e saídas;
- `relatorios/`: JaCoCo e PIT;
- `docs/`: documentação desta pesquisa.

A organização física atual não foi alterada. O diretório próprio `dataset/` não foi criado porque sua criação e movimentação dos arquivos romperiam caminhos relativos utilizados por Maven, pelo script `mcdc`, por testes e por exemplos. A alternativa adotada é usar a raiz atual como dataset preservado e manter toda documentação em `docs/`.

## 3. Documentação de requisitos

Os formatos observados são:

- `.mcdc`: expressão por linha com identificador;
- JSON: decisões, guardas, ações, tipos e valores;
- CSV: casos de teste concretos;
- PDF técnico: fonte não confirmada textualmente nesta etapa;
- texto do README: instruções e descrição arquitetural.

Contagens observadas:

| Fonte | Unidades |
|---|---:|
| `exemplos/requisitos.mcdc` | 3 |
| `exemplos/decisoes.json` | 4 |
| `exemplos/vm-requisitos.mcdc` | 5 |
| `exemplos/vm-decisoes.json` | 5 |
| `exemplos/tis-decisoes.json` | 17 |
| `exemplos/npp-decisoes.json` | 11 |

Os arquivos JSON são mais adequados à análise semântica porque contêm texto, guardas e ações. Os `.mcdc` são mais adequados a testes controlados de expressões pequenas.

## 4. Características da implementação

O sistema implementado é deliberadamente genérico e não usa banco de dados, rede ou interface gráfica. É um programa de linha de comando com classes Java e dependências Maven. Z3 é externo e opcional para algumas funcionalidades.

Entrada e saída são determinadas por arquivos:

- expressões diretas;
- arquivos `.mcdc`;
- JSON NAT2TEST;
- CSV de testes;
- relatórios text, JSON, CSV e truth-Csv.

A implementação fornece metadados importantes para o estudo:

- identificador do requisito;
- expressão textual da guarda;
- entradas e tipos;
- ações esperadas;
- possíveis estados `_antes`;
- saída booleana da decisão;
- pares de independência;
- diagnóstico de cobertura;
- conflitos entre decisões.

## 5. Suíte de testes

O projeto contém testes JUnit distribuídos por cada módulo. Foram encontrados 34 arquivos Java de teste e aproximadamente 167 métodos anotados. O README informa 171 testes e relatórios históricos de qualidade. Esta caracterização não considera a contagem do README como reproduzida sem uma nova execução.

Os testes incluem o próprio motor de mutação usado pela ferramenta, mas não representam mutantes gerados para as aplicações VM, TIS e NPP.

Os artefatos de execução já disponíveis são:

- `relatorios/jacoco/`: cobertura de linhas e desvios;
- `relatorios/pit/`: mutantes já produzidos sobre o código da ferramenta;
- `exemplos/saidas/`: resultados gerados dos exemplos.

## 6. Metadados disponíveis

Os metadados úteis são mais ricos no JSON NAT2TEST:

- nome do sistema;
- variável e tipo;
- domínio enum ou escala de tipos;
- identificador da decisão;
- identificador do requisito;
- texto natural;
- guarda;
- ações;
- estado anterior por `_antes`.

Os resultados já gerados fornecem:

- tabelas verdade;
- suítes geradas;
- verificações de conflitos;
- cobertura histórica;
- notas de mutação histórica.

## 7. Candidatos a unidades experimentais

Candidatos prioritários:

- `vm#1` a `vm#5`: decisões independentes ou relacionadas por estados da máquina de café;
- `npp#1` a `npp#4`: transições de modo por limites de pressão;
- `npp#5` a `npp#11`: relações de override e safety injection;
- `tis#1` a `tis#17`: maior variedade de expressões, eventos e estados;
- `REQ-003` de `exemplos/requisitos.mcdc`: expressão com redundância lógica evidente.

A unidade pode ser uma decisão individual, um pequeno conjunto relacionado ou um módulo completo do exemplo. Isso deve ser decidido após validação humana e não foi realizado nesta etapa.

## 8. Limitações conhecidas

- não há rastreabilidade oficial entre requisitos e implementação de domínio;
- não há implementação dos sistemas VM, TIS e NPP;
- o número de casos existentes é limitado;
- o texto natural não é disponível para todas as decisões auxiliares;
- o PDF técnico não pôde ser extraído com as ferramentas disponíveis;
- há possíveis inconsistências entre contagens textuais e contagens efetivas;
- o `.gitignore` exclui `docs/`, exigindo atenção antes da integração Git;
- o Z3 é uma dependência externa opcional;
- alguns JSON possuem campos auxiliares como `temporal` cujo significado depende do leitor.

## 9. Recomendações de preservação

- manter o conteúdo atual sem mover ou renomear arquivos;
- preservar o PDF e os arquivos originais;
- registrar o commit e a versão usados;
- preservar saídas históricas como artefatos, mas separá-las de resultados novos;
- não reinterpretar `text`, `guard` e `actions` como uma única especificação independente sem validação;
- evitar comparar contagens históricas com contagens novas sem repetir a execução;
- antes de publicar a documentação, decidir uma exceção controlada para `docs/` no `.gitignore` ou uma forma rastreável de versionamento.
