package io.github.rvdomingos.mcdc.cli;

import io.github.rvdomingos.mcdc.core.DecisionAnalysis;
import io.github.rvdomingos.mcdc.core.McdcReport;
import io.github.rvdomingos.mcdc.core.TestVector;
import io.github.rvdomingos.mcdc.core.model.Decision;
import java.util.List;

/**
 * Tabela verdade inteira em CSV: uma linha por combinação, uma coluna por condição. Cada decisão tem
 * o próprio cabeçalho, separado do anterior por uma linha em branco.
 */
final class TruthTableCsvReport {

    /** Colunas antes das condições. */
    static final String PREFIX = "decision,requirement,row";

    /** Colunas depois das condições. */
    static final String SUFFIX = "outcome,feasible,in_suite,demonstrates,concrete_values";

    /** Acima disso a planilha fica ilegível; o JSON usa o mesmo teto. */
    static final int MAX_ROWS = JsonReport.MAX_TABLE_ROWS;

    private TruthTableCsvReport() {
    }

    static String format(List<DecisionAnalysis> analyses) {
        var sb = new StringBuilder();
        for (DecisionAnalysis analysis : analyses) {
            if (!sb.isEmpty()) {
                sb.append('\n');
            }
            Decision decision = analysis.decision();
            McdcReport report = analysis.report();
            List<String> inputs = report.table().inputs();
            int size = report.table().rows().size();
            if (!report.table().isFull()) {
                throw new IllegalArgumentException(decision.id() + ": a tabela não foi montada (modo direto). Use --format json ou csv.");
            }
            if (size > MAX_ROWS) {
                throw new IllegalArgumentException(decision.id() + ": a tabela tem " + size
                        + " linhas; o truth-csv vai até " + MAX_ROWS + ". Use --format json ou csv.");
            }

            sb.append(PREFIX);
            for (String input : inputs) {
                sb.append(',').append(CsvReport.cell(input));
            }
            sb.append(',').append(SUFFIX).append('\n');

            for (TestVector row : report.table().rows()) {
                boolean inSuite = report.minimalSuite().stream().anyMatch(t -> t.index() == row.index());
                sb.append(CsvReport.cell(decision.id())).append(',')
                        .append(CsvReport.cell(decision.requirement())).append(',')
                        .append(row.name());
                for (String input : inputs) {
                    sb.append(',').append(row.value(input) ? "T" : "F");
                }
                sb.append(',').append(row.outcome() ? "T" : "F")
                        .append(',').append(row.feasible() ? "T" : "F")
                        .append(',').append(inSuite ? "T" : "F")
                        .append(',').append(CsvReport.cell(inSuite ? String.join("; ", report.demonstratedBy(row)) : ""))
                        .append(',').append(CsvReport.cell(TextReport.assignment(row).replace(", ", "; ")))
                        .append('\n');
            }
        }
        return sb.toString();
    }
}
