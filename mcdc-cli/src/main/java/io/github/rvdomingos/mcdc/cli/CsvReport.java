package io.github.rvdomingos.mcdc.cli;

import io.github.rvdomingos.mcdc.core.BoundaryTest;
import io.github.rvdomingos.mcdc.core.DecisionAnalysis;
import io.github.rvdomingos.mcdc.core.TestVector;
import io.github.rvdomingos.mcdc.core.model.Decision;
import java.util.List;
import java.util.Map;

/**
 * Suíte mínima em CSV, uma linha por (decisão, teste, entrada). Com --z3, a última coluna traz os valores concretos do teste.
 * O formato "longo" funciona igual para decisões com entradas diferentes e abre direto numa planilha.
 */
final class CsvReport {

    static final String HEADER = "decision,requirement,test,input,value,expected_outcome,demonstrates,concrete_values";

    private CsvReport() {
    }

    static String format(List<DecisionAnalysis> analyses) {
        var sb = new StringBuilder(HEADER).append('\n');
        for (DecisionAnalysis analysis : analyses) {
            Decision decision = analysis.decision();
            for (TestVector test : analysis.report().minimalSuite()) {
                for (Map.Entry<String, Boolean> input : test.values().entrySet()) {
                    sb.append(cell(decision.id())).append(',')
                            .append(cell(decision.requirement())).append(',')
                            .append(test.name()).append(',')
                            .append(cell(input.getKey())).append(',')
                            .append(input.getValue() ? "T" : "F").append(',')
                            .append(test.outcome() ? "T" : "F").append(',')
                            .append(cell(String.join("; ", analysis.report().demonstratedBy(test)))).append(',')
                            .append(cell(TextReport.assignment(test).replace(", ", "; "))).append('\n');
                }
            }
            // variantes de fronteira: mesmas entradas do teste de origem, com outros valores concretos
            for (BoundaryTest boundary : analysis.boundaryTests()) {
                TestVector base = analysis.report().minimalSuite().stream()
                        .filter(t -> t.name().equals(boundary.baseVector())).findFirst().orElseThrow();
                for (Map.Entry<String, Boolean> input : base.values().entrySet()) {
                    sb.append(cell(decision.id())).append(',')
                            .append(cell(decision.requirement())).append(',')
                            .append(cell(base.name() + " (" + boundary.boundary() + ")")).append(',')
                            .append(cell(input.getKey())).append(',')
                            .append(input.getValue() ? "T" : "F").append(',')
                            .append(base.outcome() ? "T" : "F").append(',')
                            .append(',')
                            .append(cell(TextReport.assignment(boundary.assignment()).replace(", ", "; "))).append('\n');
                }
            }
        }
        return sb.toString();
    }

    /** Aspas só quando o texto tem vírgula, aspas ou quebra de linha. */
    static String cell(String text) {
        if (text == null) {
            return "";
        }
        if (text.contains(",") || text.contains("\"") || text.contains("\n")) {
            return "\"" + text.replace("\"", "\"\"") + "\"";
        }
        return text;
    }
}
