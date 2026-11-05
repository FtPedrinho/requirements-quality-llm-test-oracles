package io.github.rvdomingos.mcdc.core;

import io.github.rvdomingos.mcdc.core.model.Expr;
import java.util.List;
import java.util.Map;

/**
 * Resultado completo de uma análise MC/DC.
 *
 * @param pairs        todos os pares de independência, por condição
 * @param minimalSuite vetores escolhidos
 * @param chosenPairs  par escolhido para cada condição: qual dupla de testes demonstra cada uma
 * @param uncovered    condições sem par, com o motivo
 */
public record McdcReport(
        Expr expression,
        McdcOptions options,
        TruthTable table,
        Map<String, List<IndependencePair>> pairs,
        List<TestVector> minimalSuite,
        Map<String, IndependencePair> chosenPairs,
        List<UncoveredCondition> uncovered) {

    /** Condições que um vetor da suíte ajuda a demonstrar. */
    public List<String> demonstratedBy(TestVector vector) {
        return new MinimalSuite.Selection(minimalSuite, chosenPairs).demonstratedBy(vector);
    }

    /** Condições sem nenhum par: não há como demonstrar o efeito delas. */
    public List<String> uncoveredConditions() {
        return uncovered.stream().map(UncoveredCondition::condition).toList();
    }

    public boolean isComplete() {
        return uncoveredConditions().isEmpty();
    }
}
