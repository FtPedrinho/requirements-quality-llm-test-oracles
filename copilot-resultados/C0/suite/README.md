# Suíte C0 do Copilot

Esta pasta contém uma cópia da suíte C0 oficial, incluindo o baseline e as
duas extensões, sem alterações nos testes ou oráculos. As 98 unidades
executáveis são definidas em `oraculos.json`, `extension-oraculos.json` e
`extension2-oraculos.json`. Os casos indeterminados estão registrados
separadamente e não são julgamentos semânticos.

Os executores, entradas, evidências Z3, classes Java compiladas e executável
Z3 usado nas extensões estão nesta pasta.
O [manifesto da cópia](manifesto-copia.txt) contém os hashes dos arquivos
copiados. Os congelamentos, resultados brutos e demais evidências originais
permanecem no [experimento original](../../../resultados-llm/experimentos/C0/reinicio-2026-11-21/);
o [relatório C0](../C0-copilot.md) registra os resultados e limitações.
Em particular, não houve cegamento contextual integral.

## Execução

Os executores foram preservados sem alterações e gravam resultados no próprio
diretório; recusam sobrescrever resultados já existentes. Usam Python e Java
21, Jackson 2.17.2 e JaCoCo 0.8.16 no cache Maven do usuário, nos caminhos
indicados em `executar-baseline.py`. As extensões usam o Z3 local copiado.
O comando `--run` usa as classes copiadas. Após a realocação desta pasta,
o comando `--compile` do executor preservado não localiza corretamente as
fontes do SUT; para recompilar, use o executor no experimento original.
Para executar, a partir da raiz do repositório, em PowerShell:

```powershell
python copilot-resultados\C0\suite\executar-baseline.py --run
if ($LASTEXITCODE -eq 0) { python copilot-resultados\C0\suite\executar-extensao.py }
if ($LASTEXITCODE -eq 0) { python copilot-resultados\C0\suite\executar-extensao2.py }
```

Uma nova execução produz evidências próprias e não substitui os resultados
oficiais. As classes copiadas correspondem à compilação original; se o SUT
ou o ambiente forem diferentes, os resultados não são automaticamente
comparáveis. O relatório original contém versões, dependências e limites.
