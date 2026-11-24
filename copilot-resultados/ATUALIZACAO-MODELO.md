# Atualização: modelo usado na coleta do Copilot

Em 24/11/2026, depois da coleta, o pesquisador informou que o modelo usado pelo GitHub Copilot (Copilot SDK no VS Code) em C0–C4 foi o **GPT 6.1 Terra**. Os relatórios originais registravam o modelo como "não informado".

## O que foi alterado

Somente os documentos de acesso, onde o "não informado" do modelo virou o nome do modelo com esta ressalva. Versão exata, parâmetros, tokens e custo continuam "não informado".

| Arquivo | SHA-256 antes | SHA-256 depois |
|---|---|---|
| `README.md` | `2f863b77e14cd224b315998d383497b13ddae4e3ca8c21fe8f5e66c35842da0d` | `9fd3bc46818de374ae1e8d8ab7b492df9f62c4ae23887db863b9d2a3bf2bb840` |
| `C0/C0-copilot.md` | `bd54ee3012b30a6cb29521a45f71b29b8ffa0d4d5d55c07ad8b6f25ce4536b61` | `579896daea982a81e023c06c42e77aa79e1eba0f08926981d03530269f1ae1a2` |
| `C1/C1-copilot.md` | `b4b0a1c0db739a192813ddecbb92a2fd57ac803e6c6bbcf67bd412395feb9d62` | `04d83a8bec453e1211a00fb2b0243cfe03a9b8f2fefdb507ce7758bdde1cb2cc` |
| `C2/detalhes-C2/relatorio.md` | `89d96db6fad67aa57adcdb22046f56a0183f0ae0e29e8076fda492f9179374a3` | `d20b15b4759feff907e91c636423b9f6f6600a3058f192d51b64b2ca9ee01dfa` |
| `C3/detalhes-C3/relatorio-final.md` | `afd79a93db48c4b6ce7db7e87a3d1becec9155512cd6d2b67f8d020efd83d59c` | `81d08c43cf3914ca467f982efa84dac7ee20f1bd771b5f2ed6f68cf14e4d504b` |
| `C4/C4-copilot.md` | `7d27bcc7c22dd26e74b12534acbf548015982e6af8bb9bc34dae237028e2fd6d` | `384ed37d14921c57665b8ad8440c465b9effa3e80011f6b6e832f97f57eea894` |
| `C2/C2-copilot.md` | `2c300083b6be4b49d561ec295c2854508e10ec7ce92f267c35f2d9a65eac1620` | `4cf21150185a7f02f8e88ba9fb9b4a8903af1beffcac640a2c0d7cd510394e1b` |
| `C3/C3-copilot.md` | `5420c62cdd39ceade7a0b89b55b5183bfbc87603d1a52de0112de46f3842e862` | `69eb168a14a011a04f90b5d20a9db839971595c85ccb8d69cf2addcfecba4cdf` |

`C4/C4-copilot.md` está listado em `C4/detalhes-C4/organizacao.sha256`: o hash registrado ali é o da versão anterior, que está na tabela acima.

## O que não foi alterado

As evidências congeladas, que estão em manifestos de hash, continuam com o texto original ("não informado"). Entre elas: `C0/detalhes-C0/C0-copilot-original.md`, `C1/detalhes-C1/relatorio-final.md`, `C1/detalhes-C1/relatorio.md`, `C1/detalhes-C1/registro.md`, `C2/detalhes-C2/metadados/preparacao.md`, `C4/detalhes-C4/relatorio-original.md`, `C4/detalhes-C4/ambiente.md` e os prompts preservados.
