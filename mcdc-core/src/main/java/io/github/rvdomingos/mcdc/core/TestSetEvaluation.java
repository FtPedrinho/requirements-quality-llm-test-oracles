package io.github.rvdomingos.mcdc.core;

import java.util.List;
import java.util.Map;

/**
 * Resultado do modo avaliação: quanto de MC/DC um conjunto de testes existente atinge.
 *
 * @param table             tabela verdade da decisão
 * @param tests             testes avaliados
 * @param vectorOfTest      linha da tabela de cada teste, pelo nome do teste
 * @param demonstrated      par formado por testes existentes, por condição demonstrada
 * @param suggestions       para cada condição que falta, as linhas a acrescentar (vazio se não houver par possível)
 * @param uncoverable       condições que nenhum conjunto de testes consegue demonstrar, com o motivo
 * @param outcomesCovered   resultados de condição (T ou F) com efeito independente demonstrado (métrica do MCDC-Star)
 * @param outcomesTotal     2 × o número de condições
 * @param problems          resultados esperados que divergem da guarda, ou testes em combinações impossíveis
 */
public record TestSetEvaluation(
        TruthTable table,
        List<TestCase> tests,
        Map<String, TestVector> vectorOfTest,
        Map<String, IndependencePair> demonstrated,
        Map<String, List<TestVector>> suggestions,
        List<UncoveredCondition> uncoverable,
        int outcomesCovered,
        int outcomesTotal,
        List<String> problems) {

    public double outcomePercentage() {
        return outcomesTotal == 0 ? 100.0 : 100.0 * outcomesCovered / outcomesTotal;
    }

    /** Toda condição demonstrada e nenhum problema. */
    public boolean isComplete() {
        return demonstrated.size() == table.conditions().size() && problems.isEmpty();
    }

    /** Nomes dos testes que caem numa linha da tabela. */
    public List<String> testsAt(TestVector vector) {
        return vectorOfTest.entrySet().stream()
                .filter(e -> e.getValue().index() == vector.index())
                .map(Map.Entry::getKey)
                .toList();
    }
}
