package io.github.rvdomingos.mcdc.cli;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.github.rvdomingos.mcdc.core.Condition;
import io.github.rvdomingos.mcdc.core.IndependencePair;
import io.github.rvdomingos.mcdc.core.McdcOptions;
import io.github.rvdomingos.mcdc.core.TestSetEvaluation;
import io.github.rvdomingos.mcdc.core.TestVector;
import io.github.rvdomingos.mcdc.core.UncoveredCondition;
import io.github.rvdomingos.mcdc.core.model.Decision;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.stream.Collectors;

/** Relatório do modo avaliação (mcdc check), em texto e JSON. */
final class CheckReport {

    record Entry(Decision decision, TestSetEvaluation evaluation) {
    }

    private CheckReport() {
    }

    static String text(List<Entry> entries) {
        return entries.stream().map(CheckReport::text).collect(Collectors.joining("\n"));
    }

    private static String text(Entry entry) {
        Decision decision = entry.decision();
        TestSetEvaluation e = entry.evaluation();
        var sb = new StringBuilder();
        sb.append("Decisão:   ").append(decision.id()).append('\n');
        if (decision.requirement() != null && !decision.requirement().equals(decision.id())) {
            sb.append("Requisito: ").append(decision.requirement()).append('\n');
        }
        sb.append("Guarda:    ").append(decision.text()).append('\n');

        if (e.tests().isEmpty()) {
            sb.append("Testes:    nenhum para esta decisão\n");
        } else {
            sb.append("Testes:    ").append(e.tests().size()).append("\n");
            e.vectorOfTest().forEach((name, row) -> sb.append("  ").append(name).append(" = ").append(row.name())
                    .append("  ").append(row.bits()).append("  -> ").append(row.outcome() ? "T" : "F").append('\n'));
        }

        sb.append("\nCondições:\n");
        for (Condition condition : e.table().conditions()) {
            String label = condition.label();
            sb.append("  ").append(label).append(": ");
            IndependencePair pair = e.demonstrated().get(label);
            List<TestVector> missing = e.suggestions().get(label);
            UncoveredCondition impossible = e.uncoverable().stream()
                    .filter(u -> u.condition().equals(label)).findFirst().orElse(null);
            if (pair != null) {
                sb.append("demonstrada por ").append(String.join("/", e.testsAt(pair.whenTrue())))
                        .append(" (T) e ").append(String.join("/", e.testsAt(pair.whenFalse()))).append(" (F)");
            } else if (missing != null) {
                sb.append("falta; acrescente ").append(missing.stream()
                        .map(v -> v.name() + " (" + v.bits() + " -> " + (v.outcome() ? "T" : "F") + ")")
                        .collect(Collectors.joining(" e ")));
            } else if (impossible != null) {
                sb.append("não pode ser demonstrada: ").append(TextReport.explain(impossible));
            }
            sb.append('\n');
        }

        if (!e.problems().isEmpty()) {
            sb.append("\nProblemas:\n");
            e.problems().forEach(p -> sb.append("  ").append(p).append('\n'));
        }

        sb.append("\nResultados de condição demonstrados: ").append(e.outcomesCovered()).append(" de ")
                .append(e.outcomesTotal()).append(" (").append(percent(e.outcomePercentage())).append(")\n");
        sb.append("Cobertura MC/DC: ").append(e.isComplete() ? "completa" : "incompleta")
                .append(", ").append(e.demonstrated().size()).append(" de ").append(e.table().conditions().size())
                .append(" condições demonstradas\n");
        return sb.toString();
    }

    static String json(String system, McdcOptions options, List<Entry> entries) {
        Map<String, Object> root = new LinkedHashMap<>();
        root.put("tool", "mcdc");
        root.put("mode", "check");
        root.put("system", system);
        root.put("variant", options.variant().name());
        root.put("complete", entries.stream().allMatch(en -> en.evaluation().isComplete()));
        List<Map<String, Object>> decisions = new ArrayList<>();
        for (Entry entry : entries) {
            TestSetEvaluation e = entry.evaluation();
            Map<String, Object> node = new LinkedHashMap<>();
            node.put("id", entry.decision().id());
            node.put("requirement", entry.decision().requirement());
            node.put("guard", entry.decision().text());
            node.put("complete", e.isComplete());
            node.put("conditionsDemonstrated", e.demonstrated().size());
            node.put("conditionsTotal", e.table().conditions().size());
            node.put("outcomesCovered", e.outcomesCovered());
            node.put("outcomesTotal", e.outcomesTotal());
            node.put("outcomePercentage", Math.round(e.outcomePercentage() * 10) / 10.0);

            List<Map<String, Object>> tests = new ArrayList<>();
            e.vectorOfTest().forEach((name, row) -> {
                Map<String, Object> t = new LinkedHashMap<>();
                t.put("test", name);
                t.put("vector", row.name());
                t.put("outcome", row.outcome());
                tests.add(t);
            });
            node.put("tests", tests);

            List<Map<String, Object>> conditions = new ArrayList<>();
            for (Condition condition : e.table().conditions()) {
                Map<String, Object> c = new LinkedHashMap<>();
                c.put("condition", condition.label());
                IndependencePair pair = e.demonstrated().get(condition.label());
                c.put("demonstrated", pair != null);
                if (pair != null) {
                    c.put("whenTrue", e.testsAt(pair.whenTrue()));
                    c.put("whenFalse", e.testsAt(pair.whenFalse()));
                }
                List<TestVector> missing = e.suggestions().get(condition.label());
                if (missing != null) {
                    c.put("addVectors", missing.stream().map(v -> {
                        Map<String, Object> m = new LinkedHashMap<>();
                        m.put("vector", v.name());
                        m.put("values", v.values());
                        m.put("outcome", v.outcome());
                        if (!v.assignment().isEmpty()) {
                            m.put("assignment", v.assignment());
                        }
                        return m;
                    }).toList());
                }
                e.uncoverable().stream().filter(u -> u.condition().equals(condition.label())).findFirst()
                        .ifPresent(u -> c.put("uncoverable", u.reason().name()));
                conditions.add(c);
            }
            node.put("conditions", conditions);
            node.put("problems", e.problems());
            decisions.add(node);
        }
        root.put("decisions", decisions);
        try {
            return new ObjectMapper().writerWithDefaultPrettyPrinter().writeValueAsString(root) + "\n";
        } catch (JsonProcessingException ex) {
            throw new IllegalStateException("Falha ao gerar o JSON", ex);
        }
    }

    private static String percent(double value) {
        return String.format(Locale.ROOT, "%.1f%%", value).replace('.', ',');
    }
}
