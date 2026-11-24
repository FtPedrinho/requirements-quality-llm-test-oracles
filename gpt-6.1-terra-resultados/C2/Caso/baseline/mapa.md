# Mapeamento e execução do baseline

Os 119 casos, suas entradas e expectativas estão em `../oraculos/casos.json`, congelado antes da criação deste harness. O mapeamento é por `tipo` e pelo campo `argumentos`, sem modificar expectativas.

- `truth`: `mcdc-requirements/ExpressionParser` e `mcdc-core/TruthTable`, cobrindo reconhecimento dos conectivos, construções com parênteses, folhas repetidas e resultados booleanos. Localiza-se a linha pelo mapa de entradas, não pela ordem.
- `cli` com `analyze`: `mcdc-cli/Main`, formatadores, `mcdc-core/Mcdc`, pares e seleção; `--exact` e `--direct` também exercitam os módulos Z3 e o executável oficial. Para o tamanho exato e fronteira, as chaves do JSON são somente adaptadores de leitura do resultado, nunca fonte da expectativa.
- `cli` com `verify`: `Main`, leitor `.mcdc` e verificador Z3 de lacunas. `--context` restringe o universo conforme o oráculo.
- `diagnostico`: executa as entradas registradas sem comparar sua saída com expectativa; contribui somente à cobertura total, não à conformidade ou aprovação.

Todos os casos têm entrada e instruções interpretáveis pelo harness. O script `executar.ps1`, chamado a partir da raiz do workspace, compila os quatro módulos em `production-classes` e o harness separadamente. Compila apenas fontes de produção. Ele configura o PATH para o executável Z3 isolado e executa duas JVMs: total e somente conformes. Para cada caso, o harness grava saída/erro e resultado com expectativa, observação, classificação, estado, mensagem e tempo. Um resultado divergente é mantido como `FALHOU`, com exit code não zero do harness; erros técnicos não viram divergência. O código de retorno da CLI é um dos resultados documentados.

Para não coletar métricas de condição ou de MC/DC fora do escopo de Branch Coverage, o fluxo de saída da CLI descarta as linhas agregadas iniciadas por `Resultados de condição demonstrados:` e `Cobertura MC/DC:` antes de gravar a evidência; o restante da saída é preservado. Essa filtragem significa que os logs da CLI não são saídas brutas integrais.

Reprodução em cópia fresca com os arquivos de oráculo e harness preservados e sem saídas anteriores: `powershell -NoProfile -File gpt-6.1-terra-resultados\C2\Caso\baseline\executar.ps1`. O script de coleta depende dos jars e do Z3 identificados em `metadados/`. Nenhuma opção ou algoritmo de mutação é invocado.
