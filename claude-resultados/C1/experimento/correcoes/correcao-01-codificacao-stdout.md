# Correção 01 — codificação do stdout da JVM (suíte, não oráculo)

- Rodada afetada: `resultados/rodada-01-baseline/`, caso AN-22 (FALHOU no baseline).
- Diagnóstico: a JVM (Windows) usava `stdout.encoding = Cp1252`; o arquivo de `-o` é gravado em UTF-8.
  O runner decodificava stdout como UTF-8 com substituição, então "Decisão" virou "Decis\ufffdo"
  (bytes `ef bf bd`) só na captura da tela. O arquivo (`AN-22.txt`) tem `c3 a3` (UTF-8 correto).
  A diferença está na captura do harness, não no conteúdo do relatório: é erro técnico de medição,
  não divergência semântica.
- Correção: lançar a JVM com `-Dstdout.encoding=UTF-8 -Dstderr.encoding=UTF-8` (propriedades de
  execução; o SUT, a documentação e o oráculo não mudam). Versão anterior preservada em
  `suite/versoes/run_suite.rodada-01.py`.
- Execução: suíte completa reexecutada em `resultados/rodada-02-correcao/` (todos os 79 casos, para
  medir cobertura com a suíte corrigida). O baseline fica preservado sem alteração.
- Expectativa de AN-22 inalterada (oráculo congelado em `congelamento/01-oraculo.sha256`).
