# Transcrição operacional disponível

- Pré-verificação: Java 21.0.3 e javac 21.0.3 disponíveis; Maven e executável
  `z3` ausentes do PATH. Biblioteca `z3-solver` instalada foi verificada
  separadamente e produziu `sat` com testemunha para a consulta de teste.
- Docker: cliente presente; conexão com o daemon indisponível. O usuário
  posteriormente dispensou explicitamente o isolamento operacional.
- Z3 independente: seis respostas `sat`, com testemunhas, e duas `unsat`;
  saída integral em [resultado-z3.json](resultado-z3.json).
- Compilação e relatório: o comando congelado de execução terminou com
  `[INFO] Loading execution data file ...\jacoco.exec`,
  `[INFO] Analyzing 69 classes.` e
  `Java terminou com código 1; veja os resultados por caso.` O código 1
  é registrado em [execucao.txt](execucao/execucao.txt).
- O arquivo [erros-java.log](execucao/erros-java.log) está vazio; as oito
  mensagens de asserção estão em [casos.jsonl](execucao/casos.jsonl).
- Verificação posterior dos três manifestos: `OK congelamento-oraculos.sha256`,
  `OK congelamento-suite.sha256`, `OK fontes-sut.sha256`. O SHA-256 da fonte
  C4 permaneceu igual ao valor do protocolo.

Esta transcrição registra a saída disponibilizada nesta sessão; uma gravação
integral independente dos fluxos de compilação não foi produzida.
