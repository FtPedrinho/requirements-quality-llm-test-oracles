$ErrorActionPreference = 'Stop'
$root = (Resolve-Path 'gpt-6.1-terra-resultados\C2\Caso').Path
$base = Join-Path $root 'baseline'
$one = Join-Path $root 'extensao-1'
$two = Join-Path $root 'extensao-2'
$cache = Join-Path $env:USERPROFILE '.m2\repository'
$jackson = @('jackson-core', 'jackson-annotations', 'jackson-databind') | ForEach-Object {
    Join-Path $cache "com\fasterxml\jackson\core\$_\2.17.2\$_-2.17.2.jar"
}
$agent = Join-Path $cache 'org\jacoco\org.jacoco.agent\0.8.16\org.jacoco.agent-0.8.16-runtime.jar'
$cli = Join-Path $cache 'org\jacoco\org.jacoco.cli\0.8.16\org.jacoco.cli-0.8.16-nodeps.jar'
$env:PATH = "$(Join-Path $root 'dependencias\z3');$env:PATH"
$classes = Join-Path $base 'production-classes'
$extHarness = Join-Path $two 'harness-classes'
New-Item -ItemType Directory -Path $extHarness -ErrorAction Stop | Out-Null
$classpath = "$classes;$(Join-Path $base 'harness-classes');$(Join-Path $one 'harness-classes');$extHarness;" + ($jackson -join ';')
& javac -encoding UTF-8 -cp $classpath -d $extHarness (Join-Path $two 'Extension2Harness.java') 2>&1 | Tee-Object -FilePath (Join-Path $two 'compilacao.log')
if ($LASTEXITCODE -ne 0) { throw "Compilação do harness falhou: $LASTEXITCODE" }
foreach ($name in @('total', 'conformes')) {
    $exec = Join-Path $two "$name.exec"
    $watch = [Diagnostics.Stopwatch]::StartNew()
    & java '-Dfile.encoding=UTF-8' "-javaagent:${agent}=destfile=$exec,append=true" -cp $classpath io.github.rvdomingos.mcdc.cli.TestHarness (Join-Path $root 'oraculos\casos.json') (Join-Path $root 'oraculos\entradas') (Join-Path $two "evidencias-baseline-$name") (Join-Path $two "$name-baseline.json") $name 2>&1 | Tee-Object -FilePath (Join-Path $two "$name-baseline.log")
    $baselineCode = $LASTEXITCODE
    if ($baselineCode -gt 2) { throw "Baseline terminou inesperadamente: $baselineCode" }
    & java '-Dfile.encoding=UTF-8' "-javaagent:${agent}=destfile=$exec,append=true" -cp $classpath io.github.rvdomingos.mcdc.cli.ExtensionHarness (Join-Path $one 'casos.json') (Join-Path $two "evidencias-extensao-1-$name") (Join-Path $two "$name-extensao-1.json") 2>&1 | Tee-Object -FilePath (Join-Path $two "$name-extensao-1.log")
    $oneCode = $LASTEXITCODE
    if ($oneCode -gt 2) { throw "Extensão 1 terminou inesperadamente: $oneCode" }
    & java '-Dfile.encoding=UTF-8' "-javaagent:${agent}=destfile=$exec,append=true" -cp $classpath io.github.rvdomingos.mcdc.cli.Extension2Harness (Join-Path $two 'casos.json') (Join-Path $two "$name-extensao-2.json") 2>&1 | Tee-Object -FilePath (Join-Path $two "$name-extensao-2.log")
    $twoCode = $LASTEXITCODE
    if ($twoCode -gt 2) { throw "Extensão 2 terminou inesperadamente: $twoCode" }
    $watch.Stop()
    "Duração das três JVMs em ms: $($watch.ElapsedMilliseconds); exit baseline: $baselineCode; exit extensão 1: $oneCode; exit extensão 2: $twoCode" | Out-File -LiteralPath (Join-Path $two "$name-tempo.txt") -Encoding utf8 -NoClobber
    & java -jar $cli report $exec --classfiles $classes --xml (Join-Path $two "$name-jacoco.xml") --csv (Join-Path $two "$name-jacoco.csv") 2>&1 | Tee-Object -FilePath (Join-Path $two "$name-jacoco.log")
    if ($LASTEXITCODE -ne 0) { throw "Relatório JaCoCo falhou: $LASTEXITCODE" }
}
