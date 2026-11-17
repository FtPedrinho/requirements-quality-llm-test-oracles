package io.github.rvdomingos.mcdc.cli;

import io.github.rvdomingos.mcdc.core.BoundaryTest;
import io.github.rvdomingos.mcdc.core.DecisionAnalysis;
import io.github.rvdomingos.mcdc.core.IndependencePair;
import io.github.rvdomingos.mcdc.core.IndependencePairs;
import io.github.rvdomingos.mcdc.core.McdcReport;
import io.github.rvdomingos.mcdc.core.McdcVariant;
import io.github.rvdomingos.mcdc.core.TestVector;
import io.github.rvdomingos.mcdc.core.UncoveredCondition;
import io.github.rvdomingos.mcdc.core.model.Decision;
import io.github.rvdomingos.mcdc.core.model.ExprText;
import io.github.rvdomingos.mcdc.core.mutation.MutationReport;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.stream.Collectors;

/** Relatório em texto para o terminal. */
final class TextReport {

    private static final int MAX_PAIRS_SHOWN = 6;

    /** Acima disso a tabela não é impressa no texto; o JSON traz até JsonReport.MAX_TABLE_ROWS linhas. */
    static final int MAX_TABLE_ROWS_SHOWN = 64;

    private TextReport() {
    }

    /** Relatórios de todas as decisões, separados por uma linha em branco. */
    static String format(List<DecisionAnalysis> analyses, String constraint) {
        return analyses.stream()
                .map(analysis -> format(analysis, constraint))
                .collect(Collectors.joining("\n"));
    }

    static String format(DecisionAnalysis analysis, String constraint) {
        Decision decision = analysis.decision();
        McdcReport report = analysis.report();
        var sb = new StringBuilder();
        sb.append("Decisão:   ").append(decision.id()).append('\n');
        if (decision.requirement() != null && !decision.requirement().equals(decision.id())) {
            sb.append("Requisito: ").append(decision.requirement()).append('\n');
        }
        sb.append("Guarda:    ").append(decision.text()).append('\n');
        if (!decision.actions().isEmpty()) {
            sb.append("Ações:     ").append(String.join("; ", decision.actions())).append('\n');
        }
        if (constraint != null) {
            sb.append("Restrição: ").append(constraint).append('\n');
        }
        sb.append("Variante:  ").append(variantName(report.options().variant())).append("\n\n");

        if (report.table().conditions().size() > report.table().inputs().size()) {
            // alguma entrada aparece mais de uma vez: cada ocorrência é uma condição com par próprio
            sb.append("Condições: ")
                    .append(String.join(", ", report.table().conditions().stream().map(c -> c.label()).toList()))
                    .append("\n\n");
        }
        int rows = report.table().rows().size();
        if (!report.table().isFull()) {
            sb.append("Tabela verdade: não montada (modo direto: os pares foram pedidos ao Z3; ")
                    .append(report.table().combinations()).append(" combinações)\n");
        } else if (rows <= MAX_TABLE_ROWS_SHOWN) {
            sb.append(report.table().format());
        } else {
            long feasible = report.table().rows().stream().filter(TestVector::feasible).count();
            sb.append("Tabela verdade: ").append(rows).append(" linhas, ").append(feasible)
                    .append(" possíveis (grande demais para o texto; use --format json até ")
                    .append(JsonReport.MAX_TABLE_ROWS).append(" linhas)\n");
        }

        sb.append("\nPares de independência:\n");
        report.pairs().forEach((condition, pairs) ->
                sb.append("  ").append(condition).append(": ").append(describe(pairs)).append('\n'));

        sb.append("\n").append(switch (report.suiteMethod()) {
            case GREEDY -> "Suíte mínima";
            case EXACT -> "Suíte mínima, exata (Z3)";
            case DIRECT -> "Suíte do modo direto";
        }).append(" (").append(report.minimalSuite().size()).append(" testes):\n");
        for (TestVector vector : report.minimalSuite()) {
            sb.append("  ").append(vector.name())
                    .append("  ").append(vector.bits())
                    .append("  -> ").append(vector.outcome() ? "T" : "F")
                    .append("   demonstra ").append(String.join(", ", report.demonstratedBy(vector)));
            if (!vector.assignment().isEmpty()) {
                sb.append("   [").append(assignment(vector)).append(']');
            }
            sb.append('\n');
        }

        if (!analysis.boundaryTests().isEmpty()) {
            sb.append("\nTestes de fronteira (").append(analysis.boundaryTests().size()).append("):\n");
            for (BoundaryTest b : analysis.boundaryTests()) {
                sb.append("  ").append(b.baseVector()).append(" com ").append(b.boundary())
                        .append("   [").append(assignment(b.assignment())).append("]\n");
            }
        }

        if (analysis.mutation() != null) {
            MutationReport mutation = analysis.mutation();
            sb.append("\nValidação por mutação: ").append(String.format(Locale.ROOT, "%.1f", mutation.score()).replace('.', ','))
                    .append("% das falhas detectáveis foram detectadas\n");
            mutation.byFault().forEach((fault, s) -> sb.append("  ").append(fault.description()).append(" (")
                    .append(fault).append("): ").append(s.killed()).append(" de ").append(s.detectable())
                    .append(s.equivalent() > 0 ? " (+" + s.equivalent() + " equivalentes)" : "").append('\n'));
            for (MutationReport.Result r : mutation.survivors()) {
                sb.append("  não detectada: ").append(r.mutant().fault()).append(' ')
                        .append(ExprText.format(r.mutant().expression())).append('\n');
            }
        }

        if (!report.chosenPairs().isEmpty()) {
            sb.append("\nDemonstração por condição:\n");
            report.chosenPairs().forEach((condition, pair) -> sb.append("  ").append(condition).append(": ")
                    .append(pair.whenTrue().name()).append(" (T) e ").append(pair.whenFalse().name()).append(" (F)")
                    .append(pair.isUniqueCause() ? ", só ela muda" : ", outras mascaradas")
                    .append('\n'));
        }

        sb.append("\nCobertura MC/DC: ");
        if (report.isComplete()) {
            sb.append("completa\n");
        } else {
            sb.append("incompleta, sem par para ")
                    .append(String.join(", ", report.uncoveredConditions()))
                    .append('\n');
            for (UncoveredCondition u : report.uncovered()) {
                sb.append("  ").append(u.condition()).append(": ").append(explain(u)).append('\n');
            }
        }
        return sb.toString();
    }

    /** Valores concretos vindos do Z3, ex.: "speed = 101, rain = true". */
    static String assignment(TestVector vector) {
        return assignment(vector.assignment());
    }

    static String assignment(Map<String, String> values) {
        return values.entrySet().stream()
                .map(e -> e.getKey() + " = " + e.getValue())
                .collect(Collectors.joining(", "));
    }

    static String explain(UncoveredCondition u) {
        return switch (u.reason()) {
            case REDUNDANT -> "redundante: não muda o resultado em nenhuma combinação; o requisito pode ser simplificado";
            case INFEASIBLE -> "bloqueada pelas restrições: os pares " + describe(u.blockedPairs()) + " usam linhas impossíveis";
        };
    }

    private static String describe(List<IndependencePair> pairs) {
        if (pairs.isEmpty()) {
            return "nenhum par";
        }
        String shown = pairs.stream()
                .limit(MAX_PAIRS_SHOWN)
                .map(IndependencePair::toString)
                .collect(Collectors.joining(", "));
        String total = pairs.size() >= IndependencePairs.MAX_PAIRS_PER_CONDITION
                ? IndependencePairs.MAX_PAIRS_PER_CONDITION + "+ pares"
                : pairs.size() + " pares";
        return pairs.size() <= MAX_PAIRS_SHOWN ? shown : shown + ", ... (" + total + ")";
    }

    private static String variantName(McdcVariant variant) {
        return switch (variant) {
            case UNIQUE_CAUSE -> "causa única";
            case MASKING -> "mascaramento";
        };
    }
}
