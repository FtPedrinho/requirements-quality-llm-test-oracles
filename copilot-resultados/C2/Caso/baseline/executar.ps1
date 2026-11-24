$ErrorActionPreference = 'Stop'
$root = (Resolve-Path 'copilot-resultados\C2\20261123T1109-7f9b1cb76e1b4ef7845a').Path
$repo = (Resolve-Path '.').Path
$base = Join-Path $root 'baseline'
$cache = Join-Path $env:USERPROFILE '.m2\repository'
$jackson = @('jackson-core', 'jackson-annotations', 'jackson-databind') | ForEach-Object {
    Join-Path $cache "com\fasterxml\jackson\core\$_\2.17.2\$_-2.17.2.jar"
}
$agent = Join-Path $cache 'org\jacoco\org.jacoco.agent\0.8.16\org.jacoco.agent-0.8.16-runtime.jar'
$cli = Join-Path $cache 'org\jacoco\org.jacoco.cli\0.8.16\org.jacoco.cli-0.8.16-nodeps.jar'
$z3dir = Join-Path $root 'dependencias\z3'
foreach ($file in @($agent, $cli, (Join-Path $z3dir 'z3.exe'), (Join-Path $z3dir 'libz3.dll')) + $jackson) {
    if (-not (Test-Path -LiteralPath $file)) { throw "Dependência ausente: $file" }
}
$env:PATH = "$z3dir;$env:PATH"
& (Join-Path $z3dir 'z3.exe') --version
if ($LASTEXITCODE -ne 0) { throw 'Z3 oficial indisponível' }
$classes = Join-Path $base 'production-classes'
$harness = Join-Path $base 'harness-classes'
New-Item -ItemType Directory -Path $classes -ErrorAction Stop | Out-Null
New-Item -ItemType Directory -Path $harness -ErrorAction Stop | Out-Null
$modules = @('mcdc-core', 'mcdc-requirements', 'mcdc-z3', 'mcdc-cli')
$sources = foreach ($module in $modules) {
    Get-ChildItem -LiteralPath (Join-Path $repo "$module\src\main\java") -Filter '*.java' -File -Recurse | ForEach-Object { $_.FullName }
}
$dependencies = $jackson -join ';'
& javac -encoding UTF-8 -cp $dependencies -d $classes $sources 2>&1 | Tee-Object -FilePath (Join-Path $base 'compilacao-sut.log')
if ($LASTEXITCODE -ne 0) { throw "Compilação do SUT falhou: $LASTEXITCODE" }
& javac -encoding UTF-8 -cp "$classes;$dependencies" -d $harness (Join-Path $base 'TestHarness.java') 2>&1 | Tee-Object -FilePath (Join-Path $base 'compilacao-harness.log')
if ($LASTEXITCODE -ne 0) { throw "Compilação do harness falhou: $LASTEXITCODE" }
foreach ($name in @('total', 'conformes')) {
    $exec = Join-Path $base "$name.exec"
    $watch = [Diagnostics.Stopwatch]::StartNew()
    & java '-Dfile.encoding=UTF-8' "-javaagent:${agent}=destfile=$exec,append=false" -cp "$harness;$classes;$dependencies" io.github.rvdomingos.mcdc.cli.TestHarness (Join-Path $root 'oraculos\casos.json') (Join-Path $root 'oraculos\entradas') (Join-Path $base "evidencias-$name") (Join-Path $base "$name-resultados.json") $name 2>&1 | Tee-Object -FilePath (Join-Path $base "$name-execucao.log")
    $code = $LASTEXITCODE
    $watch.Stop()
    "Duração da JVM em ms: $($watch.ElapsedMilliseconds); exit code do harness: $code" | Out-File -LiteralPath (Join-Path $base "$name-tempo.txt") -Encoding utf8 -NoClobber
    if ($code -gt 2) { throw "Harness terminou inesperadamente: $code" }
    & java -jar $cli report $exec --classfiles $classes --xml (Join-Path $base "$name-jacoco.xml") --csv (Join-Path $base "$name-jacoco.csv") 2>&1 | Tee-Object -FilePath (Join-Path $base "$name-jacoco.log")
    if ($LASTEXITCODE -ne 0) { throw "Relatório JaCoCo falhou: $LASTEXITCODE" }
}
