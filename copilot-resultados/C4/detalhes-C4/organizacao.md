# Organização posterior à execução

A pasta foi organizada para seguir o padrão imediato `suite`, `detalhes-C4` e
`C4-copilot.md`. Os oráculos, entradas, resultados, dados de cobertura e
manifestos originais não foram alterados.

Os manifestos originais preservam os caminhos da execução: para verificá-los,
substitua o prefixo `copilot-resultados\C4\detalhes\` por
`copilot-resultados\C4\detalhes-C4\`. Duas exceções preservam as versões
anteriores à reorganização:

- `copilot-resultados\C4\suite\executar.ps1` no manifesto de congelamento
  corresponde a [executar-suite-congelada.ps1](executar-suite-congelada.ps1).
  O executor atual em `suite` foi ajustado somente para localizar
  `detalhes-C4`; não é o arquivo congelado antes da execução.
- `copilot-resultados\C4\relatorio-C4-20261123.md` no manifesto de evidências
  corresponde a [relatorio-original.md](relatorio-original.md). O relatório
  principal foi renomeado e seus links foram atualizados.

Os caminhos registrados em [ambiente.md](ambiente.md) e
[transcricao.md](transcricao.md) descrevem a execução histórica e não foram
reescritos. A reorganização não executou novamente a suíte.

Após a mudança, foram verificados 76 hashes dos manifestos originais com o
mapeamento acima. Os 16 links locais do relatório principal e a sintaxe do
executor atualizado também foram verificados.
