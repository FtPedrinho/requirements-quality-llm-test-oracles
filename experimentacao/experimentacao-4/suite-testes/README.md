# Suíte C4

A suíte usa JUnit 5 e invoca a CLI Java real sem alterar o código de produção. As expectativas estão congeladas em [oracle-catalog.csv](oracle-catalog.csv); entradas cuja sintaxe foi inventada ou inferida são identificadas no catálogo e no `test-audit.csv`.

## Pré-requisitos e execução

Requer Java 21, Maven 3.9.x, módulos instalados no repositório Maven local e Z3 no `PATH` para os cenários diretos/relacionais.

Na raiz do repositório, instale os módulos sem executar o gate preexistente de JaCoCo e execute a suíte:

```powershell
mvn -q -DskipTests -Djacoco.skip=true install
mvn -f experimentacao\experimentacao-4\suite-testes\pom.xml test
```

O catálogo e a auditoria em `../evidencias/execucoes/test-audit.csv` distinguem documentação explícita, inferências, suposições e casos indeterminados. Os testes que representam afirmações contraditórias permanecem como assertions separadas; não foram normalizados para coincidir com a implementação. A execução de referência teve 23 aprovações, 11 falhas e 6 casos desabilitados; veja o log de execução e o relatório final antes de interpretar qualquer aprovação.
