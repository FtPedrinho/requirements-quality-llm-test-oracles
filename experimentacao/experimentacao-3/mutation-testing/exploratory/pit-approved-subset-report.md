# C3 — PIT exploratório em subconjunto aprovado

## Escopo

O score abaixo não é da suíte C3 integral. A execução integral continua com sete falhas de linha de base e, portanto, sem Mutation Score avaliável. Para responder ao pedido posterior de executar PIT, foi preparada uma cópia isolada das duas classes de teste C3; somente os sete métodos que falhavam sem mutação receberam `@Disabled` nessa cópia. Os testes originais, resultados esperados e código de produção não foram alterados.

A linha de base filtrada passou: 54 casos descobertos, 38 aprovados e 16 desabilitados (sete falhas de linha de base e nove já desabilitados). Isso corresponde ao subconjunto aprovado combinado, não a uma execução exploratória individual de S1 ou S2.

## Ambiente e execução

- Implementação: commit `20288f1f2e40dcd4ca3e9412f772b72a5489b188`.
- Java 21.0.3; Maven 3.9.11; Z3 4.15.4.
- PIT 1.30.2 com o conjunto padrão de mutadores, suporte JUnit 5 1.2.3; alvo `mcdc-core`, classes `io.github.rvdomingos.mcdc.*`.
- O módulo core e o POM raiz foram copiados para uma área isolada. A cópia do POM do core recebeu somente uma dependência de teste `mcdc-cli`, necessária para as classes C3 chamarem `Main.run`. O JAR local usado teve SHA-256 `2E6019EA9ECEC1FDD92AA9D44BD4F44843C82BD35AD24F8871E173A2C3C855F6`.
- SHA-256 das classes de teste: original C3 documental `D6F3268632D6E1653CED6B0A99E877148826BFBC801E0B22B23096D39D1A4969`; cópia filtrada `5717017725E46E71B1B5FE2714101DC718A6FC68D76F9A7CD2067F938F68F6B9`. A classe complementar não foi alterada: original e cópia `12264880A5D0B53360DCEE1CAF633D4CB43192A64E26890C3CC083996E77432A`.
- Comando PIT: `mvn -f <copia-isolada>\mcdc-core\pom.xml -DtargetTests=io.github.rvdomingos.mcdc.cli.C3DocumentationSuiteTest,io.github.rvdomingos.mcdc.cli.C3ComplementarySuiteTest -Dqualidade.mutacao.minima=0 -Djacoco.skip=true org.pitest:pitest-maven:1.30.2:mutationCoverage`.
- Os testes filtrados estão em [passing-subset-tests](passing-subset-tests/); os métodos excluídos estão em [baseline-exclusions.csv](baseline-exclusions.csv).

## Resultado

| Classificação | Quantidade |
|---|---:|
| Mutantes gerados (M) | 333 |
| Killed (K) | 118 |
| Survived | 110 |
| No coverage | 105 |
| Equivalent identificado (E) | 0 |
| Timed out | 0 |
| Non-viable / Error | 0 |
| Mutation Score exploratório | `118 / (333 - 0) × 100 = 35,44%` |

Os mutantes sem cobertura permanecem no denominador `M-E`, de acordo com a fórmula definida para a avaliação. O PIT não identificou equivalentes; isso não significa que houve adjudicação semântica manual.

O arquivo [mutation-results-passing-subset.csv](mutation-results-passing-subset.csv) registra cada mutante e, para os mortos, o killer reportado pelo PIT. O XML bruto está em [pit-raw-passing-subset.xml](pit-raw-passing-subset.xml). O XML registra o teste detector reportado pelo PIT, não uma lista exaustiva de todos os testes que poderiam matar cada mutante. A execução da linha de base filtrada e o PIT estão registrados em [pit-approved-subset-baseline.log](../execution-logs/pit-approved-subset-baseline.log) e [pit-approved-subset.log](../execution-logs/pit-approved-subset.log).

## Limitações e interpretação

O conjunto limpo contém 333 mutantes e é idêntico ao conjunto gerado para o C4 exploratório. Ele difere dos 456 mutantes das execuções históricas de C2/C3; os scores não são diretamente comparáveis entre conjuntos. O resultado mede somente a detecção operacional dos 38 testes aprovados. Não corrige as sete falhas nem valida a semântica dos oráculos; essa validação continua separada e depende do gabarito independente.
