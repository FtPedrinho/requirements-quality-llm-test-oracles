# Suítes C2 — original e complementar

O diretório preserva S1 (os 26 testes originais, sem alterações) e S2 (os dez casos complementares). S3 é a execução combinada. Os detalhes e resultados finais estão em [../results.md](../results.md).

## Executar a suíte derivada

```powershell
mvn -f experimentacao\experimentacao-2\test-suite\pom.xml test
```

Os casos indeterminados permanecem registrados, mas não são executados com resultados inventados.
