package io.github.rvdomingos.mcdc.core;

import io.github.rvdomingos.mcdc.core.model.Expr;
import java.util.List;
import java.util.Map;

/**
 * Resultado de uma análise MC/DC.
 *
 * @param table       tabela verdade; no modo direto, só as linhas da suíte
 * @param chosenPairs par escolhido para cada condição
 * @param uncovered   condições sem par, com o motivo
 */
public record McdcReport(
        Expr expression,
        McdcOptions options,
        TruthTable table,
        Map<String, List<IndependencePair>> pairs,
        List<TestVector> minimalSuite,
        Map<String, IndependencePair> chosenPairs,
        List<UncoveredCondition> uncovered,
        SuiteMethod suiteMethod) {

    /** Condições que um vetor da suíte ajuda a demonstrar. */
    public List<String> demonstratedBy(TestVector vector) {
        return new MinimalSuite.Selection(minimalSuite, chosenPairs).demonstratedBy(vector);
    }

    /** Condições sem nenhum par. */
    public List<String> uncoveredConditions() {
        return uncovered.stream().map(UncoveredCondition::condition).toList();
    }

    public boolean isComplete() {
        return uncoveredConditions().isEmpty();
    }
}
