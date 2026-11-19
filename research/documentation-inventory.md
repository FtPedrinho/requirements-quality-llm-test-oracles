# Inventário documental

## Documentos principais

| Documento | Caminho | Tipo | Conteúdo | Relação com implementação | Adequação ao corpus |
|---|---|---|---|---|---|
| README da ferramenta | `docs/README.md` | Manual/documentação do usuário | Funcionalidades, instalação, comandos, formatos, saídas e exemplos | Corresponde em grande parte à CLI implementada | Alta para uso e comportamento externo |
| README de pesquisa anterior | `README.md` | Documento de pesquisa | Objetivo, metodologia, fork e experimentos | Não descreve o SUT como fonte normativa | Baixa |
| Análise técnica histórica | `docs/repository-analysis.md` | Diagnóstico secundário | Arquitetura, requisitos, implementação e limitações | Derivada do repositório | Média como contexto, não como fonte primária |
| Caracterização do dataset | `docs/dataset-characterization.md` | Diagnóstico secundário | Estrutura do repositório e exemplos | Mistura SUT e dados de entrada | Média |
| Viabilidade histórica | `docs/research-feasibility.md` | Diagnóstico secundário | Viabilidade de pesquisa anterior | Pode conter conclusões metodológicas anteriores | Baixa como especificação |
| Matriz histórica | `docs/traceability-matrix.md` | Rastreabilidade secundária | Relações prévias | Não cobre toda a implementação | Média |
| Especificação técnica PDF | `Especificação Técnica - Ferramenta Dupla MC_DC (Requisitos e Código Java).pdf` | Proposta arquitetural/especificação | Visão, modos requisito/código, Eclipse, análise Java, RCP | Contradiz o snapshot atual em várias funcionalidades | Não normativa até ser reconciliada |
| Uso da CLI no código | `mcdc-cli/src/main/java/.../Main.java` | Implementação + ajuda embutida | Comandos, opções, fontes e validações | Evidência direta do comportamento executável | Alta |
| Javadocs dos módulos | classes `src/main/java/**/*.java` | Comentários técnicos | Contratos, limites e resultados | Evidência direta quando confirmada pelo código/testes | Média/alta |
| Testes JUnit | `mcdc-*/src/test/java/**/*.java` | Especificação executável | Casos esperados e regressão | Evidência independente; reservada para validação | Alta para validar oráculos |
| POM Maven | `pom.xml` | Configuração | Java 21, módulos, JaCoCo, PIT, limites | Evidência de build e qualidade | Média |
| Script `mcdc` | `mcdc` | Interface operacional | Execução das classes compiladas | Evidência do modo de uso | Média |
| Setup | `setup.sh` | Histórico de criação | Esqueleto histórico | Não representa especificação atual | Baixa |
| Página HTML | `index.html` | Interface estática | Link para relatórios | Artefato auxiliar | Baixa |
| Relatórios HTML/CSV/XML | `relatorios/` | Artefato histórico de execução | Cobertura e mutação da ferramenta | Evidência histórica, não especificação | Baixa para geração, alta apenas como histórico |
| Exemplos `.mcdc` | `exemplos/*.mcdc` | Dados de entrada | Expressões de exemplo | Processados pela ferramenta, não documentação funcional do SUT | Auxiliar |
| JSON NAT2TEST | `exemplos/*-decisoes.json` | Dados de entrada | Decisões, guardas e ações de VM/TIS/NPP | Não descrevem o SUT | Auxiliar, reservado |
| CSV de testes | `exemplos/testes.csv` | Dados de entrada | Conjunto de teste externo | Pode testar o modo `check`, não oráculos do SUT | Auxiliar |
| Saídas geradas | `exemplos/saidas/` | Artefatos gerados | Exemplos de relatórios | Evidência do comportamento observado, não norma primária | Média como validação |

## Fontes externas

Nenhuma fonte externa foi necessária para o inventário atual. Links no README apontam Z3, JaCoCo e PIT, mas não foram usados como especificação da implementação local.
