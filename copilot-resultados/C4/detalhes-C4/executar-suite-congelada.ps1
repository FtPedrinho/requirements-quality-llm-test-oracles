param(
    [Parameter(Mandatory = $true)][string]$Z3
)

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..\..\..')).Path
$details = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..\detalhes')).Path
$out = Join-Path $details 'execucao'
if (Test-Path -LiteralPath $out) {
    throw "A pasta de execução já existe: $out. Não sobrescreva evidências."
}
if (-not (Test-Path -LiteralPath $Z3 -PathType Leaf)) {
    throw "Executável Z3 inexistente: $Z3"
}
$repo = Join-Path $env:USERPROFILE '.m2\repository'
$jackson = @(
    'com\fasterxml\jackson\core\jackson-databind\2.17.2\jackson-databind-2.17.2.jar',
    'com\fasterxml\jackson\core\jackson-core\2.17.2\jackson-core-2.17.2.jar',
    'com\fasterxml\jackson\core\jackson-annotations\2.17.2\jackson-annotations-2.17.2.jar'
) | ForEach-Object { Join-Path $repo $_ }
$agent = Join-Path $repo 'org\jacoco\org.jacoco.agent\0.8.16\org.jacoco.agent-0.8.16-runtime.jar'
$cli = Join-Path $repo 'org\jacoco\org.jacoco.cli\0.8.16\org.jacoco.cli-0.8.16-nodeps.jar'
foreach ($file in @($jackson) + @($agent, $cli)) {
    if (-not (Test-Path -LiteralPath $file -PathType Leaf)) { throw "Dependência ausente: $file" }
}
New-Item -ItemType Directory -Path $out | Out-Null
$sut = Join-Path $out 'classes-sut'
$harness = Join-Path $out 'classes-harness'
New-Item -ItemType Directory -Path $sut, $harness | Out-Null
$sources = foreach ($module in @('mcdc-core','mcdc-requirements','mcdc-z3','mcdc-cli')) {
    Get-ChildItem -LiteralPath (Join-Path $root "$module\src\main\java") -Filter '*.java' -File -Recurse |
        ForEach-Object { $_.FullName }
}
if (-not $sources) { throw 'Nenhuma classe de produção encontrada.' }
$jacksonPath = $jackson -join ';'
& javac -encoding UTF-8 -cp $jacksonPath -d $sut @sources
if ($LASTEXITCODE -ne 0) { throw "Compilação do SUT falhou: $LASTEXITCODE" }
$classpath = (@($sut) + $jackson) -join ';'
& javac -encoding UTF-8 -cp $classpath -d $harness (Join-Path $PSScriptRoot 'CasosC4.java')
if ($LASTEXITCODE -ne 0) { throw "Compilação da suíte falhou: $LASTEXITCODE" }
$classpath = (@($harness, $sut) + $jackson) -join ';'
$exec = Join-Path $out 'jacoco.exec'
$agentArgument = "-javaagent:${agent}=destfile=${exec},append=false"
$watch = [Diagnostics.Stopwatch]::StartNew()
& java $agentArgument -cp $classpath CasosC4 (Join-Path $details 'casos.json') $Z3 (Join-Path $out 'casos.jsonl') 2> (Join-Path $out 'erros-java.log')
$runExit = $LASTEXITCODE
$watch.Stop()
"exit=$runExit`nduration_ms=$($watch.ElapsedMilliseconds)" | Set-Content -LiteralPath (Join-Path $out 'execucao.txt') -Encoding UTF8
if (-not (Test-Path -LiteralPath $exec)) { throw 'Java não produziu dados de cobertura.' }
& java -jar $cli report $exec --classfiles $sut --xml (Join-Path $out 'jacoco.xml')
if ($LASTEXITCODE -ne 0) { throw "Relatório JaCoCo falhou: $LASTEXITCODE" }
& python (Join-Path $PSScriptRoot 'resumir.py') $out (Join-Path $details 'indeterminados.json')
if ($LASTEXITCODE -ne 0) { throw "Consolidação falhou: $LASTEXITCODE" }
Write-Output "Java terminou com código $runExit; veja os resultados por caso."
