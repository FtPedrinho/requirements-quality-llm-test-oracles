package io.github.rvdomingos.mcdc.z3;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import io.github.rvdomingos.mcdc.core.IndependencePair;
import io.github.rvdomingos.mcdc.core.IndependencePairs;
import io.github.rvdomingos.mcdc.core.Mcdc;
import io.github.rvdomingos.mcdc.core.McdcOptions;
import io.github.rvdomingos.mcdc.core.McdcReport;
import io.github.rvdomingos.mcdc.core.McdcVariant;
import io.github.rvdomingos.mcdc.core.SuiteMethod;
import io.github.rvdomingos.mcdc.core.TestVector;
import io.github.rvdomingos.mcdc.core.TruthTable;
import io.github.rvdomingos.mcdc.core.UncoveredCondition;
import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import io.github.rvdomingos.mcdc.core.model.Predicate;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

class Z3DirectAnalyzerTest {

    @BeforeAll
    static void requiresZ3() {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "z3 não instalado; testes pulados");
    }

    private final Z3DirectAnalyzer direct = new Z3DirectAnalyzer(List.of());

    private static Cond c(String id) {
        return new Cond(id);
    }

    private static Cond p(String variable, String operator, String value) {
        return new Cond(new Predicate(variable, operator, value));
    }

    /** Uma e de n comparações a_i > i, sobre variáveis diferentes. */
    private static Expr chain(int n) {
        Expr expr = p("a0", ">", "0");
        for (int i = 1; i < n; i++) {
            expr = new And(expr, p("a" + i, ">", String.valueOf(i)));
        }
        return expr;
    }

    @Test
    void agreesWithTheTableOnSmallDecisions() {
        List<Expr> expressions = List.of(
                new Or(new And(c("A"), c("B")), c("C")),
                new Or(c("A"), new And(c("A"), c("B"))),
                new Or(new And(c("A"), c("B")), new And(new Not(c("A")), c("C"))),
                new Or(p("speed", ">", "100"), new And(p("speed", ">", "50"), c("rain"))));
        for (McdcVariant variant : McdcVariant.values()) {
            McdcOptions options = McdcOptions.defaults().withVariant(variant);
            for (Expr expr : expressions) {
                McdcReport table = Mcdc.analyze(expr, options.withFeasibility(new Z3FeasibilityChecker(List.of())));
                McdcReport report = direct.analyze(expr, options);

                assertEquals(SuiteMethod.DIRECT, report.suiteMethod());
                assertEquals(reasons(table), reasons(report), expr + " " + variant);
                // todo par escolhido é um par de verdade na tabela inteira
                Map<String, List<IndependencePair>> all = IndependencePairs.of(table.table(), variant);
                report.chosenPairs().forEach((condition, pair) -> assertTrue(all.get(condition).stream().anyMatch(q ->
                        q.whenTrue().index() == pair.whenTrue().index()
                                && q.whenFalse().index() == pair.whenFalse().index()), condition + " " + pair));
            }
        }
    }

    private static Map<String, UncoveredCondition.Reason> reasons(McdcReport report) {
        Map<String, UncoveredCondition.Reason> reasons = new java.util.LinkedHashMap<>();
        report.uncovered().forEach(u -> reasons.put(u.condition(), u.reason()));
        return reasons;
    }

    @Test
    void handlesDecisionsBeyondTheRowByRowLimit() {
        McdcReport report = direct.analyze(chain(16), McdcOptions.defaults());

        assertTrue(report.isComplete());
        assertEquals(17, report.minimalSuite().size()); // n + 1
        assertFalse(report.table().isFull());
        assertEquals(1L << 16, report.table().combinations());
        TestVector allTrue = report.minimalSuite().get(0);
        assertEquals("V1", allTrue.name());
        for (int i = 0; i < 16; i++) {
            assertTrue(Integer.parseInt(allTrue.assignment().get("a" + i)) > i, allTrue.assignment().toString());
        }
    }

    @Test
    void goesBeyondTheTableLimitOfTwentyInputs() {
        McdcReport report = direct.analyze(chain(24), McdcOptions.defaults());

        assertTrue(report.table().combinations() > 1L << TruthTable.MAX_INPUTS);
        assertTrue(report.isComplete());
        assertEquals(25, report.minimalSuite().size());
    }

    @Test
    void findsConditionsBlockedByCoupledPredicates() {
        // ... and (speed > 100 and speed > 50): speed > 50 não decide sem que speed > 100 também mude
        Expr expr = new And(chain(14), new And(p("speed", ">", "100"), p("speed", ">", "50")));
        McdcReport report = direct.analyze(expr, McdcOptions.defaults());

        assertEquals(List.of("speed > 50"), report.uncoveredConditions());
        assertEquals(UncoveredCondition.Reason.INFEASIBLE, report.uncovered().get(0).reason());
        assertEquals(1, report.uncovered().get(0).blockedPairs().size());
    }

    @Test
    void uniqueCausePairsDifferInOneInputOnly() {
        Expr expr = new Or(new And(c("A"), c("B")), new And(c("C"), new Or(c("D"), c("E"))));
        McdcReport report = direct.analyze(expr, McdcOptions.defaults().withVariant(McdcVariant.UNIQUE_CAUSE));

        assertTrue(report.isComplete());
        assertTrue(report.chosenPairs().values().stream().allMatch(IndependencePair::isUniqueCause));
    }
}
