# Suíte C4 (baseline)

Suíte pytest com **um teste por caso DETERMINADO** (D01–D42) do oráculo
congelado em `../experimento/oraculo.json`. IDs: `test_C4_Dnn_...`. Os 36 casos
INDETERMINADOS (I01–I36) não têm teste e não são executados.

* `test_c4_oraculo.py`: os 42 testes.
* `c4_util.py`: invocação da CLI (`java -cp ... io.github.rvdomingos.mcdc.cli.Main`), Z3 no `PATH`, gravação dos brutos.
* `dados/entradas.json`: expressões e arquivos de entrada usados.

Execução (a partir da raiz do repositório; ver `../experimento/README.md`):

```
python -m pytest claude-sonnet-5.5-resultados/C4/suite -p no:cacheprovider
```

Asserções sobre código de saída: nenhuma (o texto C4 não define seus significados).
Expectativas não foram ajustadas ao comportamento do SUT.
