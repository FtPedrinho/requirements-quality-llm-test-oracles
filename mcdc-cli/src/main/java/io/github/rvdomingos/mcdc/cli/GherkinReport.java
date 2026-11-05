package io.github.rvdomingos.mcdc.cli;

import io.github.rvdomingos.mcdc.core.BoundaryTest;
import io.github.rvdomingos.mcdc.core.DecisionAnalysis;
import io.github.rvdomingos.mcdc.core.TestVector;
import io.github.rvdomingos.mcdc.core.model.Decision;
import java.util.List;
import java.util.Map;

/**
 * Suíte mínima em Gherkin, em português, um cenário por teste. Com --z3 os passos "Dado" trazem os
 * valores concretos das variáveis; sem ele, o valor lógico de cada condição.
 */
final class GherkinReport {

    private GherkinReport() {
    }

    static String format(String system, List<DecisionAnalysis> analyses) {
        var sb = new StringBuilder();
        sb.append("# language: pt\n");
        sb.append("# Gerado pela ferramenta MC/DC: um cenário por teste da suíte mínima.\n\n");
        sb.append("Funcionalidade: ").append(system != null ? system : "Requisitos").append(" - testes MC/DC\n");

        for (DecisionAnalysis analysis : analyses) {
            Decision decision = analysis.decision();
            String requirement = decision.requirement() != null ? decision.requirement() : decision.id();
            sb.append("\n  # ").append(decision.id()).append(": ").append(decision.text()).append('\n');

            for (TestVector test : analysis.report().minimalSuite()) {
                List<String> demonstrates = analysis.report().demonstratedBy(test);
                sb.append("\n  Cenário: ").append(requirement).append(' ').append(test.name())
                        .append(" demonstra ").append(String.join(", ", demonstrates)).append('\n');
                given(sb, test, test.assignment());
                outcome(sb, decision, test.outcome());
            }
            for (BoundaryTest boundary : analysis.boundaryTests()) {
                TestVector base = analysis.report().minimalSuite().stream()
                        .filter(t -> t.name().equals(boundary.baseVector())).findFirst().orElseThrow();
                sb.append("\n  Cenário: ").append(requirement).append(' ').append(base.name())
                        .append(" na fronteira ").append(boundary.boundary()).append('\n');
                given(sb, base, boundary.assignment());
                outcome(sb, decision, base.outcome());
            }
        }
        return sb.toString();
    }

    private static void given(StringBuilder sb, TestVector test, Map<String, String> assignment) {
        boolean first = true;
        if (assignment.isEmpty()) {
            for (Map.Entry<String, Boolean> input : test.values().entrySet()) {
                sb.append(first ? "    Dado que a condição \"" : "    E a condição \"").append(input.getKey())
                        .append("\" é ").append(input.getValue() ? "verdadeira" : "falsa").append('\n');
                first = false;
            }
        } else {
            for (Map.Entry<String, String> value : assignment.entrySet()) {
                sb.append(first ? "    Dado que " : "    E ").append(value.getKey()).append(" = ")
                        .append(value.getValue()).append('\n');
                first = false;
            }
        }
    }

    private static void outcome(StringBuilder sb, Decision decision, boolean outcome) {
        sb.append("    Quando a guarda \"").append(decision.text()).append("\" é avaliada\n");
        sb.append("    Então ela é ").append(outcome ? "verdadeira" : "falsa").append('\n');
        if (outcome) {
            for (String action : decision.actions()) {
                sb.append("    E o sistema executa \"").append(action).append("\"\n");
            }
        }
    }
}
