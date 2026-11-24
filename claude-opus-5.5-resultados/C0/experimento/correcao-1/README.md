# Correção 1: entradas JSON malformadas (C0-C07, C0-C08, C0-C09)

**O que houve.** Na rodada 1, `cafe-doc.json` e `temporal.json` foram gravados com `/\` dentro de uma string JSON. A barra dupla `/\` do exemplo literal do README se perdeu no heredoc do shell. O arquivo resultante é JSON inválido. O SUT respondeu `Erro: JSON inválido: Unrecognized character escape ' '` (código 1), e os três casos que usavam esses arquivos foram julgados FALHOU.

**Classificação.** São **casos inválidos** por defeito de entrada do executor, não falhas semânticas do SUT. O próprio `json.load` do Python recusa os arquivos originais, que estão preservados em `entradas-originais-malformadas/`.

**Perda de isolamento.** O defeito só foi notado ao ler a saída do SUT. A correção não altera nenhuma expectativa (o `oraculo.json` está intacto). As entradas passam a ser o exemplo literal do README, gerado com `json.dump` e com o mesmo conteúdo lógico.

**O que mudou.** Só `oraculo/entradas/cafe-doc.json` e `oraculo/entradas/temporal.json`. Os hashes novos estão em `../CONGELAMENTO-CORRECAO-1.sha256`. Também foi corrigido `suite/cobertura.sh` (caminho POSIX → Windows ao ler o `config.json`), que é uma ferramenta de medição e não mexe em nenhuma expectativa.

**Rodadas.** A rodada 1 fica preservada como baseline. A rodada 2 reexecuta a suíte inteira com as entradas corrigidas.
