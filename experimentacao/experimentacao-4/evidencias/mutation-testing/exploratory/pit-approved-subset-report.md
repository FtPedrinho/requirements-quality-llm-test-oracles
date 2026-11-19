# C4 — PIT exploratório em subconjunto aprovado

## Escopo

O score abaixo não é da suíte C4 integral. A execução original teve 11 falhas de linha de base e seis casos já desabilitados; seu Mutation Score integral continua não avaliável. Para responder ao pedido posterior de executar PIT, foi preparada uma cópia isolada da classe de teste e somente os 11 métodos que falhavam sem mutação receberam `@Disabled` nessa cópia. Os testes originais, resultados esperados e código de produção não foram alterados.

A linha de base filtrada passou: 40 casos descobertos, 23 aprovados e 17 desabilitados (11 falhas de linha de base e os seis casos já desabilitados).

## Ambiente e execução

- Implementação: commit `20288f1f2e40dcd4ca3e9412f772b72a5489b188`.
- Java 21.0.3; Maven 3.9.11; Z3 4.15.4.
- PIT 1.30.2 com o conjunto padrão de mutadores, suporte JUnit 5 1.2.3; alvo `mcdc-core`, classes `io.github.rvdomingos.mcdc.*`.
- O módulo core e o POM raiz foram copiados para uma área isolada. A cópia do POM do core recebeu somente uma dependência de teste `mcdc-cli`, necessária para a classe C4 chamar `Main.run`. O JAR local usado teve SHA-256 `2E6019EA9ECEC1FDD92AA9D44BD4F44843C82BD35AD24F8871E173A2C3C855F6`.
- SHA-256 da classe de teste: original `497BBA9E0F0EF1FDA8D78CBB79F72A1EF0757D69F560F7B595917BA73FE9ACAD`; cópia filtrada `C977A0AE87CB2F2781B45D70ED176C026A92E025347DD1D67ABF06F1B9297C75`.
- Comando PIT: `mvn -f <copia-isolada>\mcdc-core\pom.xml -DtargetTests=io.github.rvdomingos.mcdc.cli.C4DocumentationSuiteTest -Dqualidade.mutacao.minima=0 -Djacoco.skip=true org.pitest:pitest-maven:1.30.2:mutationCoverage`.
- Os testes filtrados estão em [passing-subset-tests](passing-subset-tests/); os métodos excluídos estão em [baseline-exclusions.csv](baseline-exclusions.csv).

## Resultado

| Classificação | Quantidade |
|---|---:|
| Mutantes gerados (M) | 333 |
| Killed (K) | 131 |
| Survived | 82 |
| No coverage | 120 |
| Equivalent identificado (E) | 0 |
| Timed out | 0 |
| Non-viable / Error | 0 |
| Mutation Score exploratório | `131 / (333 - 0) × 100 = 39,34%` |

Os mutantes sem cobertura permanecem no denominador `M-E`, de acordo com a fórmula definida para a avaliação. O PIT não identificou equivalentes; isso não significa que houve adjudicação semântica manual.

O arquivo [mutation-results-passing-subset.csv](mutation-results-passing-subset.csv) registra cada mutante e, para os mortos, o killer reportado pelo PIT. O XML bruto está em [pit-raw-passing-subset.xml](pit-raw-passing-subset.xml). O XML registra o teste detector reportado pelo PIT, não uma lista exaustiva de todos os testes que poderiam matar cada mutante. A execução da linha de base filtrada e o PIT estão registrados em [pit-approved-subset-baseline.log](../execution-logs/pit-approved-subset-baseline.log) e [pit-approved-subset.log](../execution-logs/pit-approved-subset.log).

## Comparação e limitações

O conjunto de 333 mutantes é idêntico ao usado no C3 exploratório e difere dos 456 mutantes das execuções históricas de C2/C3. Em relação ao subconjunto C3, o C4 matou 13 mutantes a mais e obteve score 3,90 pontos percentuais maior (39,34% contra 35,44%). O tamanho e a composição das suítes diferem; essa diferença não demonstra efeito causal da clareza ou consistência. O resultado mede somente a detecção operacional dos 23 testes aprovados, não valida a semântica dos oráculos e não elimina as 11 falhas da suíte original.
