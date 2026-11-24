# Rodadas só com casos determinados (C0)

**Por quê:** pela regra definida pelo pesquisador durante o C3, um caso INDETERMINADO não é teste. Ele não é executado e não entra na Branch Coverage. O C0 terminou antes dessa regra: suas rodadas 2 e extensão 1 executaram os indeterminados como diagnóstico. Estas rodadas medem a cobertura do C0 sob a regra nova, sem apagar as anteriores.

**Como:** `filtrar.py` copia dos oráculos congelados (`../oraculo/oraculo.json` e `../extensao-1/oraculo-extensao-1.json`) apenas os casos `DETERMINADO`, sem alterar nenhum. Resultado: 72 casos no baseline e 21 na extensão. As entradas, o runner (`suite/executar_suite.py`, versão da extensão 1), o build do SUT e as ferramentas são os mesmos já congelados. Os 14 indeterminados continuam registrados e contados, mas não são executados.

**Rodadas:** `resultados/rodada-3-determinados` (baseline), `resultados/extensao-1-determinados` e `resultados/acumulado-determinados` (merge dos dois `jacoco.exec`).

**Restauração de bytes:** o checkout do `main` com `core.autocrlf=true` tinha convertido os arquivos de texto do C0 para CRLF. Antes destas rodadas, cada arquivo listado nos manifestos foi convertido de volta para LF **somente quando** o resultado reproduzia exatamente o SHA-256 congelado (31 arquivos). As divergências que sobraram são as esperadas pelo histórico: arquivos alterados na correção 1 e na extensão 1, que conferem nos manifestos posteriores.
