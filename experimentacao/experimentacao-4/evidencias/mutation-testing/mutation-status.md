# Mutation Testing — C4

## Suíte integral: não avaliável

A execução original da suíte teve 11 falhas. PIT não foi executado sobre a suíte integral; por isso, o Mutation Score integral de C4 permanece **não avaliável**, e os resultados abaixo não o substituem.

## Execução exploratória em subconjunto aprovado

Para atender ao pedido posterior de executar mutation testing, foi feita uma execução exploratória em cópia isolada. Os 11 métodos que falhavam sem mutação foram desabilitados somente nessa cópia; os seis casos já desabilitados foram preservados. Os 23 métodos restantes passaram na linha de base filtrada. A suíte original, o código de produção e as expectativas não foram alterados.

| Resultado PIT | Quantidade |
|---|---:|
| Mutantes gerados (M) | 333 |
| Killed (K) | 131 |
| Survived | 82 |
| No coverage | 120 |
| Equivalent identificado (E) | 0 |
| Timed out | 0 |
| Non-viable / Error | 0 |
| Mutation Score exploratório | `131 / (333 - 0) = 39,34%` |

Os mutantes sem cobertura permanecem no denominador, conforme a fórmula `K / (M - E)`. O PIT não identificou equivalentes; isso não equivale a uma avaliação semântica de equivalência.

O mesmo build limpo do core e as mesmas 333 assinaturas de mutantes foram usados no C3 exploratório. As métricas por mutante e os testes detectores estão em [mutation-results-passing-subset.csv](exploratory/mutation-results-passing-subset.csv); o resultado PIT bruto está em [pit-raw-passing-subset.xml](exploratory/pit-raw-passing-subset.xml). As exclusões e cópias filtradas estão na mesma pasta. Os logs estão em [execution-logs](execution-logs/), incluindo a linha de base filtrada.

O resultado não valida a semântica dos oráculos e não elimina as 11 falhas originais. É uma medida exploratória da capacidade de detecção operacional dos 23 testes que passaram na linha de base. O conjunto de 333 mutantes difere dos 456 mutantes dos registros históricos de C2/C3; os scores não devem ser comparados diretamente entre esses conjuntos.
