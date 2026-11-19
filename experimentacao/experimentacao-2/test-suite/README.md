# Suíte derivada da documentação C2

Esta suíte foi criada a partir dos oráculos determinados ou suficientemente especificados pela documentação C2.

Comportamentos ambíguos ou indeterminados não originaram testes.

A execução contém 36 testes registrados: 26 aprovados e 10 erros documentais por não haver informação C2 suficiente.

## Executar

```powershell
$env:PATH="C:\Users\User\.copilot\session-state\8457bad6-f839-4d1b-96a8-6cea1a9c9dea\files\tools\z3-4.15.4-x64-win\bin;$env:PATH"
& "C:\Users\User\.copilot\session-state\8457bad6-f839-4d1b-96a8-6cea1a9c9dea\files\tools\apache-maven-3.9.11\bin\mvn.cmd" "-f" "experimentacao\experimentacao-2\test-suite\pom.xml" "clean" "test"
```

## Resultado da execução

- 36 testes executados;
- 26 aprovados;
- 0 reprovados;
- 10 erros documentais;
- 0 ignorados.
