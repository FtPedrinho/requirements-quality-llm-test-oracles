package io.github.rvdomingos.mcdc.core;

import java.util.List;
import java.util.Map;

/**
 * Resultado do modo avaliação: quanto de MC/DC um conjunto de testes existente atinge.
 *
 * @param demonstrated    par formado por testes existentes, por condição demonstrada
 * @param suggestions     linhas a acrescentar para cada condição que falta
 * @param uncoverable     condições que nenhum teste consegue demonstrar, com o motivo
 * @param outcomesCovered resultados de condição (T ou F) com efeito independente demonstrado (MCDC-Star)
 * @param problems        resultados esperados divergentes ou testes em combinações impossíveis
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
