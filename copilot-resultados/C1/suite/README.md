# Suíte C1

Esta é uma cópia operacional da suíte congelada em
[`../detalhes-C1/`](../detalhes-C1/). O executor baseline foi ajustado apenas
para localizar o Z3 nessa pasta. Os oráculos e as evidências originais
permanecem no diretório de detalhes.

Requer JDK 21, Python, Jackson 2.17.2 e JaCoCo 0.8.16 no cache Maven, além
dos arquivos Z3 preservados em `detalhes-C1/ferramentas`. Para uma nova
execução, copie esta pasta para outro subdiretório de `C1` e, a partir dele,
execute, nesta ordem:

```text
python suite-baseline.py
python extensao-suite-v2.py
python extensao2-suite.py
```

Uma execução escreve classes e resultados no próprio diretório da cópia;
não execute novamente sobre evidências que devam ser preservadas. A
reexecução não altera o resultado congelado do experimento original.
