# Inventário de documentação e artefatos

## Documentação do SUT e requisitos C0-C4

| Conteúdo | Localização ativa | Tratamento |
|---|---|---|
| Documentação de usuário do SUT | `docs/README.md` | Documentação do produto; preservada sem alteração |
| Documentação original de referência | `experimentacao-pesquisa/documentacao-original/` | Cópia e manifesto com origem/hash; não alterar |
| C1 | `experimentacao-pesquisa/experimentacao-1/documentation/tool-readme-C1.md` | Fonte normativa preservada |
| C2 | `experimentacao-pesquisa/experimentacao-2/documentation/tool-readme-C2.md` | Fonte normativa preservada |
| C3 | `experimentacao-pesquisa/experimentacao-3/documentation/tool-readme-C3.md` | Fonte normativa preservada |
| C4 | `experimentacao-pesquisa/experimentacao-4/tool-readme-C4.md` | Fonte normativa preservada |
| PDF técnico | `experimentacao-pesquisa/documentacao-original/technical-specification.pdf` | Referência de proposta/arquitetura; não autoriza assumir funcionalidades não especificadas no documento de usuário |

As fontes normativas e hashes estão no protocolo. Outras cópias documentais são preservadas, mas não substituem a fonte selecionada.

## Código e ambiente do SUT

- `mcdc-core/`: motor de expressões e MC/DC.
- `mcdc-requirements/`: leitores de requisitos e testes.
- `mcdc-z3/`: integração com o processo externo Z3.
- `mcdc-cli/`: interface da ferramenta.
- `pom.xml`, script `mcdc`, testes próprios e configuração são recursos do sistema sob teste; não são documentação experimental nem resultados de LLM.

## Dados de exemplo

Arquivos `.mcdc`, JSON NAT2TEST e CSV em `exemplos/` são entradas demonstrativas da ferramenta. VM, TIS e NPP não são sistemas de domínio implementados no repositório e não são o SUT desta pesquisa.

## Materiais auxiliares da pesquisa

- Objetivo, corpus, riscos e análises: documentos em `research/` e `docs/` (exceto `docs/README.md`, que pertence ao SUT).
- Protocolo e modelo vazio de coleta: `experimentacao-pesquisa/`.
- Cópias técnicas históricas: `research/archive/legacy-experimental-results/`; não substituem as fontes normativas.
- Resultados adotados e evidências complementares: `gpt-6.1-terra-resultados/`.
- Relatórios de qualidade do próprio produto em `relatorios/` e no README do SUT: não representam cobertura das suítes geradas pela nova pesquisa.

Os documentos de requisitos experimentais C0-C4 são preservados. Os experimentos e metodologias anteriores descartados foram removidos.
