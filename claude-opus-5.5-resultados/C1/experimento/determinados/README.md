# Rodadas só com casos determinados (C1)

**Por quê:** pela regra definida pelo pesquisador durante o C3, um caso INDETERMINADO não é teste. Ele não é executado e não entra na Branch Coverage. O C1 terminou antes dessa regra: suas rodadas 02 e 03 executaram os indeterminados como diagnóstico. Estas rodadas medem o C1 sob a regra nova, sem apagar as anteriores.

**Como:** o runner congelado (`suite/run_suite.py`, conferido pelo manifesto `04-extensao-01.sha256`) recebeu, pela opção `--casos` que ele já tinha, as listas de IDs determinados (`ids-baseline.txt`: 70; `ids-extensao-01.txt`: 28). Os oráculos, as entradas e o runner são os mesmos já congelados, e nenhuma expectativa mudou. Os 12 indeterminados continuam registrados e contados, mas não são executados.

**Build:** `experimento/build-sut/build.sh` foi executado de novo (HEAD `ed7d2e0`). As 73 classes conferem com `experimento/build-sut/classes.sha256`.

**Execução:** feita a pedido do pesquisador pela sessão que consolidou os relatórios, não pela sessão original do C1. Rodadas: `resultados/rodada-04-determinados` (baseline), `resultados/rodada-05-extensao-01-determinados` e `resultados/acumulado-determinados`.
