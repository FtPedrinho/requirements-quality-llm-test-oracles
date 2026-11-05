package io.github.rvdomingos.mcdc.cli;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.github.rvdomingos.mcdc.core.Condition;
import io.github.rvdomingos.mcdc.core.DecisionAnalysis;
import io.github.rvdomingos.mcdc.core.IndependencePair;
import io.github.rvdomingos.mcdc.core.IndependencePairs;
import io.github.rvdomingos.mcdc.core.McdcOptions;
import io.github.rvdomingos.mcdc.core.McdcReport;
import io.github.rvdomingos.mcdc.core.TestVector;
import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Decision;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.ExprText;
import io.github.rvdomingos.mcdc.core.mutation.MutationReport;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import io.github.rvdomingos.mcdc.core.model.Predicate;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Relatório em JSON, o formato que volta para o Viewer da NAT2TEST.
 * Cada decisão leva {@code id} e {@code requirement} para o Viewer ligar o resultado ao requisito.
 */
final class JsonReport {

    private static final ObjectMapper MAPPER = new ObjectMapper();

    /** Tabelas maiores que isso ficam de fora do JSON; "truthTableRows" diz o tamanho. */
    static final int MAX_TABLE_ROWS = 4096;

    private JsonReport() {
    }

    static String format(String system, McdcOptions options, String constraint, List<DecisionAnalysis> analyses) {
        Map<String, Object> root = new LinkedHashMap<>();
        root.put("tool", "mcdc");
        root.put("system", system);
        root.put("variant", options.variant().name());
        root.put("constraint", constraint);
        root.put("complete", analyses.stream().allMatch(a -> a.report().isComplete()));
        root.put("decisions", analyses.stream().map(JsonReport::decision).toList());
        try {
            return MAPPER.writerWithDefaultPrettyPrinter().writeValueAsString(root) + "\n";
        } catch (JsonProcessingException e) {
            throw new IllegalStateException("Falha ao gerar o JSON", e);
        }
    }

    private static Map<String, Object> decision(DecisionAnalysis analysis) {
        Decision decision = analysis.decision();
        McdcReport report = analysis.report();

        Map<String, Object> node = new LinkedHashMap<>();
        node.put("id", decision.id());
        node.put("requirement", decision.requirement());
        node.put("guard", decision.text());
        node.put("actions", decision.actions());
        node.put("complete", report.isComplete());
        node.put("uncoveredConditions", report.uncoveredConditions());
        node.put("uncovered", report.uncovered().stream().map(u -> {
            Map<String, Object> item = new LinkedHashMap<>();
            item.put("condition", u.condition());
            item.put("reason", u.reason().name());
            item.put("blockedPairs", u.blockedPairs().stream()
                    .map(p -> List.of(p.whenTrue().name(), p.whenFalse().name())).toList());
            return item;
        }).toList());
        node.put("inputs", inputs(report));
        node.put("conditions", conditions(report));
        node.put("truthTableRows", report.table().rows().size());
        if (report.table().rows().size() <= MAX_TABLE_ROWS) {
            node.put("truthTable", report.table().rows().stream().map(row -> vector(row, true)).toList());
        }

        Map<String, Object> pairs = new LinkedHashMap<>();
        report.pairs().forEach((condition, list) -> pairs.put(condition,
                list.stream().map(p -> List.of(p.whenTrue().name(), p.whenFalse().name())).toList()));
        node.put("independencePairs", pairs);
        // condições com mais pares do que o teto: a lista acima traz só os primeiros
        node.put("pairsTruncated", report.pairs().entrySet().stream()
                .filter(e -> e.getValue().size() >= IndependencePairs.MAX_PAIRS_PER_CONDITION)
                .map(Map.Entry::getKey).toList());

        node.put("minimalSuite", report.minimalSuite().stream().map(row -> {
            Map<String, Object> test = vector(row, false);
            test.put("demonstrates", report.demonstratedBy(row));
            return test;
        }).toList());

        Map<String, Object> chosen = new LinkedHashMap<>();
        report.chosenPairs().forEach((condition, pair) -> {
            Map<String, Object> p = new LinkedHashMap<>();
            p.put("whenTrue", pair.whenTrue().name());
            p.put("whenFalse", pair.whenFalse().name());
            p.put("uniqueCause", pair.isUniqueCause());
            chosen.put(condition, p);
        });
        node.put("chosenPairs", chosen);
        if (analysis.mutation() != null) {
            MutationReport mutation = analysis.mutation();
            Map<String, Object> m = new LinkedHashMap<>();
            m.put("score", Math.round(mutation.score() * 10) / 10.0);
            Map<String, Object> faults = new LinkedHashMap<>();
            mutation.byFault().forEach((fault, s) -> {
                Map<String, Object> f = new LinkedHashMap<>();
                f.put("description", fault.description());
                f.put("total", s.total());
                f.put("equivalent", s.equivalent());
                f.put("killed", s.killed());
                faults.put(fault.name(), f);
            });
            m.put("faults", faults);
            m.put("survivors", mutation.survivors().stream()
                    .map(r -> r.mutant().fault() + ": " + ExprText.format(r.mutant().expression())).toList());
            node.put("mutation", m);
        }
        if (!analysis.boundaryTests().isEmpty()) {
            node.put("boundaryTests", analysis.boundaryTests().stream().map(b -> {
                Map<String, Object> item = new LinkedHashMap<>();
                item.put("base", b.baseVector());
                item.put("condition", b.condition());
                item.put("boundary", b.boundary());
                item.put("assignment", b.assignment());
                return item;
            }).toList());
        }
        return node;
    }

    /** Uma entrada por coluna da tabela, com o predicado quando a condição é uma comparação. */
    private static List<Map<String, Object>> inputs(McdcReport report) {
        Map<String, Predicate> predicates = new LinkedHashMap<>();
        collectPredicates(report.expression(), predicates);

        List<Map<String, Object>> inputs = new ArrayList<>();
        for (String name : report.table().inputs()) {
            Map<String, Object> input = new LinkedHashMap<>();
            input.put("name", name);
            Predicate predicate = predicates.get(name);
            if (predicate != null) {
                input.put("variable", predicate.variable());
                input.put("operator", predicate.operator());
                input.put("value", predicate.value());
            }
            inputs.add(input);
        }
        return inputs;
    }

    /** Cada ocorrência de uma entrada; "label" é a chave usada em independencePairs e uncoveredConditions. */
    private static List<Map<String, Object>> conditions(McdcReport report) {
        List<Map<String, Object>> conditions = new ArrayList<>();
        for (Condition condition : report.table().conditions()) {
            Map<String, Object> node = new LinkedHashMap<>();
            node.put("label", condition.label());
            node.put("input", condition.input());
            node.put("occurrence", condition.occurrence());
            conditions.add(node);
        }
        return conditions;
    }

    private static void collectPredicates(Expr expr, Map<String, Predicate> predicates) {
        switch (expr) {
            case Cond c -> {
                if (c.predicate() != null) {
                    predicates.put(c.id(), c.predicate());
                }
            }
            case And(var left, var right) -> {
                collectPredicates(left, predicates);
                collectPredicates(right, predicates);
            }
            case Or(var left, var right) -> {
                collectPredicates(left, predicates);
                collectPredicates(right, predicates);
            }
            case Not(var operand) -> collectPredicates(operand, predicates);
        }
    }

    private static Map<String, Object> vector(TestVector row, boolean withFeasibility) {
        Map<String, Object> node = new LinkedHashMap<>();
        node.put("vector", row.name());
        node.put("values", row.values());
        node.put("outcome", row.outcome());
        if (!row.assignment().isEmpty()) {
            node.put("assignment", row.assignment());
        }
        if (withFeasibility) {
            node.put("feasible", row.feasible());
        }
        return node;
    }
}
