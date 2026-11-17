package io.github.rvdomingos.mcdc.core;

import io.github.rvdomingos.mcdc.core.model.Decision;
import io.github.rvdomingos.mcdc.core.model.Expr;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

/** Ponto de entrada do motor. */
public final class Mcdc {

    private Mcdc() {
    }

    public static McdcReport analyze(Expr expression, McdcOptions options) {
        TruthTable table = TruthTable.of(expression, options.constraint(), options.feasibility());
        Map<String, List<IndependencePair>> pairs = IndependencePairs.of(table, options.variant());
        MinimalSuite.Selection suite = options.optimizer() == null
                ? MinimalSuite.select(pairs)
                : MinimalSuite.fromRows(pairs, options.optimizer().minimumRows(pairs));
        return new McdcReport(expression, options, table, pairs, suite.tests(), suite.chosen(),
                diagnose(table, pairs, options.variant()),
                options.optimizer() == null ? SuiteMethod.GREEDY : SuiteMethod.EXACT);
    }

    /**
     * Mede o MC/DC de testes existentes. A porcentagem segue o MCDC-Star: conta cada resultado (T e F)
     * de condição mostrado com efeito independente.
     */
    public static TestSetEvaluation evaluate(Expr expression, McdcOptions options, List<TestCase> tests) {
        TruthTable table = TruthTable.of(expression, options.constraint(), options.feasibility());
        Map<String, List<IndependencePair>> pairs = IndependencePairs.of(table, options.variant());
        int n = table.inputs().size();

        Map<String, TestVector> vectorOfTest = new LinkedHashMap<>();
        Set<Integer> present = new HashSet<>();
        List<String> problems = new ArrayList<>();
        for (TestCase test : tests) {
            int index = 0;
            for (int i = 0; i < n; i++) {
                Boolean value = test.values().get(table.inputs().get(i));
                if (value == null) {
                    throw new IllegalArgumentException(test.name() + ": sem valor para " + table.inputs().get(i));
                }
                if (!value) {
                    index |= TruthTable.bit(n, i);
                }
            }
            TestVector row = table.rows().get(index);
            vectorOfTest.put(test.name(), row);
            present.add(index);
            if (test.expected() != null && test.expected() != row.outcome()) {
                problems.add(test.name() + ": resultado esperado " + (test.expected() ? "T" : "F")
                        + ", mas a guarda dá " + (row.outcome() ? "T" : "F") + " para esses valores");
            }
            if (!row.feasible()) {
                problems.add(test.name() + ": a combinação " + row.bits() + " foi marcada como impossível");
            }
        }

        Map<String, IndependencePair> demonstrated = new LinkedHashMap<>();
        Map<String, List<TestVector>> suggestions = new LinkedHashMap<>();
        Map<String, Condition> byLabel = new LinkedHashMap<>();
        table.conditions().forEach(c -> byLabel.put(c.label(), c));
        for (Map.Entry<String, List<IndependencePair>> entry : pairs.entrySet()) {
            // o par é procurado entre os testes informados, e não na lista de pares, que tem teto por condição
            IndependencePair found = pairAmong(table, byLabel.get(entry.getKey()), present, options.variant());
            IndependencePair cheapest = null;
            int cheapestCost = Integer.MAX_VALUE;
            for (IndependencePair pair : entry.getValue()) {
                int cost = (present.contains(pair.whenTrue().index()) ? 0 : 1)
                        + (present.contains(pair.whenFalse().index()) ? 0 : 1);
                if (cost < cheapestCost || (cost == cheapestCost && pair.isUniqueCause() && !cheapest.isUniqueCause())) {
                    cheapest = pair;
                    cheapestCost = cost;
                }
            }
            if (found != null) {
                demonstrated.put(entry.getKey(), found);
            } else if (cheapest != null) {
                List<TestVector> missing = new ArrayList<>();
                if (!present.contains(cheapest.whenTrue().index())) {
                    missing.add(cheapest.whenTrue());
                }
                if (!present.contains(cheapest.whenFalse().index())) {
                    missing.add(cheapest.whenFalse());
                }
                suggestions.put(entry.getKey(), missing);
            }
        }

        int covered = 0;
        for (Condition condition : table.conditions()) {
            for (boolean value : new boolean[] {true, false}) {
                boolean shown = false;
                for (int index : present) {
                    TestVector row = table.rows().get(index);
                    if (row.value(condition.input()) == value && condition.decides(expression, row)) {
                        shown = true;
                        break;
                    }
                }
                covered += shown ? 1 : 0;
            }
        }

        return new TestSetEvaluation(table, List.copyOf(tests), vectorOfTest, demonstrated, suggestions,
                diagnose(table, pairs, options.variant()), covered, 2 * table.conditions().size(), problems);
    }

    /** Um par da condição entre os testes informados, preferindo causa única; null se não houver. */
    private static IndependencePair pairAmong(TruthTable table, Condition condition, Set<Integer> present,
            McdcVariant variant) {
        int mask = TruthTable.bit(table.inputs().size(), table.inputs().indexOf(condition.input()));
        List<TestVector> whenTrue = new ArrayList<>();
        List<TestVector> whenFalse = new ArrayList<>();
        for (int index : new java.util.TreeSet<>(present)) {
            TestVector row = table.rows().get(index);
            if (row.feasible() && condition.decides(table.expression(), row)) {
                ((index & mask) == 0 ? whenTrue : whenFalse).add(row);
            }
        }
        IndependencePair found = null;
        for (TestVector t : whenTrue) {
            for (TestVector f : whenFalse) {
                if (t.outcome() == f.outcome()) {
                    continue;
                }
                boolean unique = (t.index() ^ f.index()) == mask;
                if (unique) {
                    return new IndependencePair(condition.label(), t, f);
                }
                if (variant == McdcVariant.MASKING && found == null) {
                    found = new IndependencePair(condition.label(), t, f);
                }
            }
        }
        return found;
    }

    /** Para cada condição sem par: redundante, ou bloqueada pelas linhas impossíveis. */
    static List<UncoveredCondition> diagnose(TruthTable table, Map<String, List<IndependencePair>> pairs, McdcVariant variant) {
        List<UncoveredCondition> uncovered = new ArrayList<>();
        Map<String, List<IndependencePair>> relaxed = null;
        for (Map.Entry<String, List<IndependencePair>> entry : pairs.entrySet()) {
            if (!entry.getValue().isEmpty()) {
                continue;
            }
            if (relaxed == null) {
                relaxed = IndependencePairs.of(table.withoutConstraints(), variant);
            }
            List<IndependencePair> blocked = relaxed.get(entry.getKey());
            uncovered.add(new UncoveredCondition(entry.getKey(),
                    blocked.isEmpty() ? UncoveredCondition.Reason.REDUNDANT : UncoveredCondition.Reason.INFEASIBLE,
                    blocked));
        }
        return List.copyOf(uncovered);
    }

    public static DecisionAnalysis analyze(Decision decision, McdcOptions options) {
        return new DecisionAnalysis(decision, analyze(decision.expression(), options));
    }
}
