package io.github.rvdomingos.mcdc.core;

import io.github.rvdomingos.mcdc.core.model.Decision;
import io.github.rvdomingos.mcdc.core.mutation.MutationReport;
import java.util.List;

/**
 * Uma decisão e o resultado da análise dela.
 *
 * @param boundaryTests variantes de fronteira dos testes da suíte; vazio quando não foram pedidas
 * @param mutation      validação por mutação da suíte; null quando não foi pedida
 */
public record DecisionAnalysis(Decision decision, McdcReport report, List<BoundaryTest> boundaryTests,
        MutationReport mutation) {

    public DecisionAnalysis {
        boundaryTests = boundaryTests == null ? List.of() : List.copyOf(boundaryTests);
    }

    public DecisionAnalysis(Decision decision, McdcReport report) {
        this(decision, report, List.of(), null);
    }

    public DecisionAnalysis withBoundaryTests(List<BoundaryTest> tests) {
        return new DecisionAnalysis(decision, report, tests, mutation);
    }

    public DecisionAnalysis withMutation(MutationReport mutation) {
        return new DecisionAnalysis(decision, report, boundaryTests, mutation);
    }
}
