# C3 — passo a passo

Os resultados observados estão em [C3-copilot.md](C3-copilot.md). Os oráculos foram derivados da documentação técnica C3 e congelados antes da leitura do código. Não utilize resultados anteriores como expectativas. A reexecução abaixo verifica a suíte já criada; não constitui nova geração cega de oráculos.

## 1. Verificar os arquivos preservados

No PowerShell, na raiz do repositório:

```powershell
python .\gpt-6.1-terra-resultados\C3\suite\verificar-integridade.py
```

O verificador confere os manifestos originais, inclusive as classes e ferramentas registradas, e compara as cópias da suíte com os originais. Ele adapta apenas os caminhos históricos do diretório C3; não reescreve os manifestos. Uma dependência removida ou uma fonte alterada é reportada como erro.

## 2. Preparar uma reexecução separada

É necessário Java/Javac 21, Python e os três jars Jackson 2.17.2 e JaCoCo 0.8.16 do cache Maven local. O executável de Z3 e Maven não são necessários para os casos congelados desta suíte. Não execute mutação.

Na raiz do repositório, copie a suíte para um diretório novo. O comando interrompe se o destino já existir:

```powershell
$origem = Join-Path (Get-Location) 'gpt-6.1-terra-resultados\C3\suite'
$pasta = Join-Path (Get-Location) 'gpt-6.1-terra-resultados\C3\detalhes-C3\reexecucoes'
if (-not (Test-Path -LiteralPath $pasta)) { New-Item -ItemType Directory -Path $pasta | Out-Null }
$run = Join-Path $pasta (Get-Date -Format 'yyyyMMdd-HHmmss')
if (Test-Path -LiteralPath $run) { throw 'Destino já existe' }
New-Item -ItemType Directory -Path $run -ErrorAction Stop | Out-Null
Get-ChildItem -LiteralPath $origem -Force | Copy-Item -Destination $run -Recurse -ErrorAction Stop
foreach ($dir in @('build\classes', 'evidencias', 'cobertura')) {
    New-Item -ItemType Directory -Path (Join-Path $run $dir) -ErrorAction Stop | Out-Null
}
```

Compile somente fontes de produção para o novo diretório, sem alterar o SUT:

```powershell
$jackson = Join-Path $HOME '.m2\repository\com\fasterxml\jackson\core'
$jars = @(
    (Join-Path $jackson 'jackson-annotations\2.17.2\jackson-annotations-2.17.2.jar'),
    (Join-Path $jackson 'jackson-core\2.17.2\jackson-core-2.17.2.jar'),
    (Join-Path $jackson 'jackson-databind\2.17.2\jackson-databind-2.17.2.jar')
)
foreach ($jar in $jars) { if (-not (Test-Path -LiteralPath $jar)) { throw "Dependência ausente: $jar" } }
$fontes = foreach ($modulo in @('mcdc-core','mcdc-requirements','mcdc-z3','mcdc-cli')) {
    Get-ChildItem -LiteralPath (Join-Path $modulo 'src\main\java') -Recurse -File -Filter '*.java' |
        ForEach-Object { $_.FullName }
}
& javac -encoding UTF-8 -g -cp ($jars -join ';') -d (Join-Path $run 'build\classes') $fontes
if ($LASTEXITCODE -ne 0) { throw 'Falha ao compilar as fontes de produção' }
```

## 3. Executar e avaliar

```powershell
python (Join-Path $run 'executar-suite.py')
```

Confira `resultados.json` e `evidencias` no novo diretório, inclusive se o processo retornar código diferente de zero. Não remova nem altere falhas. No ambiente original, F03 teve erro de decodificação de stdout; caso o mesmo erro ocorra, a repetição técnica usa o mesmo oráculo:

```powershell
python (Join-Path $run 'repetir-f03.py')
```

Para executar a extensão documentada, mantendo os resultados do baseline:

```powershell
python (Join-Path $run 'executar-extensao.py')
```

As evidências por caso incluem comando, stdout/stderr, resultado e duração. Os relatórios iniciais desta pesquisa continuam separados em [detalhes-C3](detalhes-C3/).

## 4. Gerar Branch Coverage

Após as execuções desejadas, ainda na mesma sessão PowerShell:

```powershell
$cli = Join-Path $HOME '.m2\repository\org\jacoco\org.jacoco.cli\0.8.16\org.jacoco.cli-0.8.16-nodeps.jar'
if (-not (Test-Path -LiteralPath $cli)) { throw "JaCoCo ausente: $cli" }
$dados = @(Get-ChildItem -LiteralPath (Join-Path $run 'cobertura') -Filter '*.exec' -File |
    ForEach-Object { $_.FullName })
if ($dados.Count -eq 0) { throw 'Nenhum dado de cobertura encontrado' }
$merged = Join-Path $run 'cobertura\reexecucao-total.exec'
if (Test-Path -LiteralPath $merged) { throw 'Relatório de reexecução já existe' }
& java -jar $cli merge $dados --destfile $merged
if ($LASTEXITCODE -ne 0) { throw 'Falha ao agregar dados JaCoCo' }
& java -jar $cli report $merged --classfiles (Join-Path $run 'build\classes') `
    --xml (Join-Path $run 'cobertura\reexecucao-total.xml')
if ($LASTEXITCODE -ne 0) { throw 'Falha ao gerar relatório JaCoCo' }
```

O denominador deve incluir todas as classes de produção dos quatro módulos, inclusive as classes de mutação, e excluir o harness e as bibliotecas. Para o subconjunto conforme, agregue separadamente os arquivos `.exec` dos casos aplicáveis; não exclua silenciosamente casos indeterminados ou erros técnicos das contagens.
