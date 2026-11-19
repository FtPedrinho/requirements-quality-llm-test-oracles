# Suíte de regressão da ferramenta — C2

## Objetivo

Esta é a suíte de regressão da ferramenta Java, separada da suíte S1/S2 usada no relatório C2.

## Pré-requisitos e execução

```powershell
mvn -q -DskipTests -Djacoco.skip=true install
mvn -f experimentacao\experimentacao-2\test-suites\exp2\pom.xml test
```

Requer JDK 21, Maven 3.9.x, Z3 no `PATH` e módulos instalados localmente.

## Resultado registrado

- testes: 25;
- aprovados: 25;
- reprovados: 0;
- ignorados: 0;
- não executáveis: 0.

Estes 25 testes não substituem S1, que preserva os 26 testes originais do experimento C2, nem S2, que contém os complementares.
