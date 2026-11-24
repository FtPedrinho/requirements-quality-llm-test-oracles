$ErrorActionPreference = 'Stop'
$root = (Resolve-Path 'gpt-6.1-terra-resultados\C2\Caso').Path
$base = Join-Path $root 'baseline'
$ext = Join-Path $root 'extensao-1'
$cache = Join-Path $env:USERPROFILE '.m2\repository'
$jackson = @('jackson-core', 'jackson-annotations', 'jackson-databind') | ForEach-Object {
    Join-Path $cache "com\fasterxml\jackson\core\$_\2.17.2\$_-2.17.2.jar"
}
$agent = Join-Path $cache 'org\jacoco\org.jacoco.agent\0.8.16\org.jacoco.agent-0.8.16-runtime.jar'
$cli = Join-Path $cache 'org\jacoco\org.jacoco.cli\0.8.16\org.jacoco.cli-0.8.16-nodeps.jar'
$env:PATH = "$(Join-Path $root 'dependencias\z3');$env:PATH"
$classes = Join-Path $base 'production-classes'
$extHarness = Join-Path $ext 'harness-classes'
New-Item -ItemType Directory -Path $extHarness -ErrorAction Stop | Out-Null
$classpath = "$classes;$(Join-Path $base 'harness-classes');$extHarness;" + ($jackson -join ';')
& javac -encoding UTF-8 -cp $classpath -d $extHarness (Join-Path $ext 'ExtensionHarness.java') 2>&1 | Tee-Object -FilePath (Join-Path $ext 'compilacao.log')
if ($LASTEXITCODE -ne 0) { throw "Compilação do harness falhou: $LASTEXITCODE" }
foreach ($name in @('total', 'conformes')) {
    $exec = Join-Path $ext "$name.exec"
    $watch = [Diagnostics.Stopwatch]::StartNew()
    & java '-Dfile.encoding=UTF-8' "-javaagent:${agent}=destfile=$exec,append=true" -cp $classpath io.github.rvdomingos.mcdc.cli.TestHarness (Join-Path $root 'oraculos\casos.json') (Join-Path $root 'oraculos\entradas') (Join-Path $ext "evidencias-baseline-$name") (Join-Path $ext "$name-baseline.json") $name 2>&1 | Tee-Object -FilePath (Join-Path $ext "$name-baseline.log")
    $baselineCode = $LASTEXITCODE
    if ($baselineCode -gt 2) { throw "Baseline terminou inesperadamente: $baselineCode" }
    & java '-Dfile.encoding=UTF-8' "-javaagent:${agent}=destfile=$exec,append=true" -cp $classpath io.github.rvdomingos.mcdc.cli.ExtensionHarness (Join-Path $ext 'casos.json') (Join-Path $ext "evidencias-extensao-$name") (Join-Path $ext "$name-extensao.json") 2>&1 | Tee-Object -FilePath (Join-Path $ext "$name-extensao.log")
    $extensionCode = $LASTEXITCODE
    if ($extensionCode -gt 2) { throw "Extensão terminou inesperadamente: $extensionCode" }
    $watch.Stop()
    "Duração das duas JVMs em ms: $($watch.ElapsedMilliseconds); exit baseline: $baselineCode; exit extensão: $extensionCode" | Out-File -LiteralPath (Join-Path $ext "$name-tempo.txt") -Encoding utf8 -NoClobber
    & java -jar $cli report $exec --classfiles $classes --xml (Join-Path $ext "$name-jacoco.xml") --csv (Join-Path $ext "$name-jacoco.csv") 2>&1 | Tee-Object -FilePath (Join-Path $ext "$name-jacoco.log")
    if ($LASTEXITCODE -ne 0) { throw "Relatório JaCoCo falhou: $LASTEXITCODE" }
}
