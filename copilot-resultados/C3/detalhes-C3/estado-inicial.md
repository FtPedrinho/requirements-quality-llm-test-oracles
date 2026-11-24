# C3 — registro inicial

## Condições e proveniência

- Fonte normativa exclusiva: `experimentacao/experimentacao-3/documentation/tool-readme-C3.md`.
- SHA-256 observado e exigido pelo protocolo: `F18B0821D79C7315486C13D5260FA2F6D6E9418EF03B86CDE58E66B91B7B87A3`.
- Protocolo SHA-256: `EC3F96C59C6C2A3570E7833B2C561B6DB38BE415B41C10A7F383BF5DA2FA6B1F`.
- Prompt v2 SHA-256: `A89A9F10E579B0189AB83CD845A42764637AB6754BD28D2E567D8D6A6B401E3F`.
- Commit informado por Git: `2aec3564c30890031db86bd2cc1bb015794d5d2e`. O workspace contém alterações; esse identificador não prova identidade do conteúdo executado.
- Sistema: Windows NT 10.0.26200.0, x64; Java 21.0.3; Python 3.13.5; Git 2.41.0.windows.1.
- Solver independente: pacote Python `z3-solver` 5.4.1.0, identificador relatado `145c0c51570a357cc558ce898ce77573ba9d4fbf`; teste inicial `sat`. Executável `z3` não encontrado no PATH.
- Maven não encontrado no PATH; cache JaCoCo presente. Disponibilidade para o build e instrumentação ainda não verificada.
- Modelo, configuração, tokens e custos: não informado. Repetições: uma tentativa.

O contexto inicial já continha uma informação qualitativa de experimento anterior. O usuário autorizou prosseguir apesar dela; não é possível demonstrar ausência absoluta de influência. O protocolo foi lido como regra operacional, não como fonte normativa de comportamento. O comando de estado do Git produziu uma listagem extensa de caminhos alterados; apenas a prévia foi apresentada, não o conteúdo de outros experimentos. A fonte C3 foi lida integralmente e contém resultados históricos: estes não são metas nem gabaritos.

Este arquivo registra preparação; não representa conclusão do experimento nem congelamento de oráculos.

Tentativa inicial de geração Z3: erro técnico `Z3Exception`, declarações SMT duplicadas por fornecer símbolos em `decls` e também em `declare-const`. A geração parou sem produzir oráculos; a chamada de tradução foi corrigida antes de nova tentativa. Não é ambiguidade documental.
