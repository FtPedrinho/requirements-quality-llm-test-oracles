package io.github.rvdomingos.mcdc.core;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Or;
import io.github.rvdomingos.mcdc.core.model.Predicate;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

class TestSetEvaluationTest {

    // (A and B) or C
    private final Expr expr = new Or(new And(new Cond("A"), new Cond("B")), new Cond("C"));

    private static TestCase test(String name, boolean a, boolean b, boolean c) {
        return new TestCase(name, Map.of("A", a, "B", b, "C", c), null);
    }

    @Test
    void theMinimalSuiteIsComplete() {
        List<TestCase> suite = List.of(test("T1", true, true, false), test("T2", true, false, true),
                test("T3", true, false, false), test("T4", false, true, false));
        TestSetEvaluation e = Mcdc.evaluate(expr, McdcOptions.defaults(), suite);

        assertTrue(e.isComplete());
        assertEquals(6, e.outcomesCovered());
        assertEquals(List.of("T1"), e.testsAt(e.demonstrated().get("A").whenTrue()));
    }

    @Test
    void suggestsWhatIsMissing() {
        // só V2 (TTF) e V4 (TFF): demonstra B; para A falta V6, para C falta V3
        TestSetEvaluation e = Mcdc.evaluate(expr, McdcOptions.defaults(),
                List.of(test("T1", true, true, false), test("T2", true, false, false)));

        assertFalse(e.isComplete());
        assertEquals(List.of("B"), List.copyOf(e.demonstrated().keySet()));
        assertEquals("V6", e.suggestions().get("A").get(0).name());
        assertEquals("V3", e.suggestions().get("C").get(0).name());
    }

    @Test
    void countsConditionOutcomesWithIndependentEffect() {
        // V1 (TTT): inverter qualquer uma das três sozinha mantém o resultado T, então nenhuma decide
        TestSetEvaluation e = Mcdc.evaluate(expr, McdcOptions.defaults(), List.of(test("T1", true, true, true)));
        assertEquals(0, e.outcomesCovered());
        assertEquals(6, e.outcomesTotal());

        // V2 (TTF): inverter A ou B derruba o resultado, então A=T e B=T decidem; inverter C mantém T
        TestSetEvaluation e2 = Mcdc.evaluate(expr, McdcOptions.defaults(), List.of(test("T1", true, true, false)));
        assertEquals(2, e2.outcomesCovered()); // A=T e B=T
    }

    @Test
    void reportsWrongExpectedOutcomes() {
        TestCase wrong = new TestCase("T1", Map.of("A", true, "B", true, "C", false), false);
        TestSetEvaluation e = Mcdc.evaluate(expr, McdcOptions.defaults(), List.of(wrong));

        assertEquals(1, e.problems().size());
        assertTrue(e.problems().get(0).startsWith("T1: resultado esperado F"));
    }

    @Test
    void resolvesConcreteValuesThroughPredicates() {
        Expr speed = new Or(new Cond(new Predicate("speed", ">", "100")),
                new And(new Cond(new Predicate("speed", ">", "50")), new Cond("rain")));
        TestCase t = TestCase.resolve(speed, "T1", Map.of("speed", "75", "rain", "true"), null);

        assertEquals(Map.of("speed > 100", false, "speed > 50", true, "rain", true), t.values());
        assertThrows(IllegalArgumentException.class, () -> TestCase.resolve(speed, "T2", Map.of("speed", "75"), null));
    }

    @Test
    void predicatesCompareNumbersAndNames() {
        assertTrue(new Predicate("x", ">=", "2.5").holds(Map.of("x", "2.50")));
        assertTrue(new Predicate("mode", "=", "idle").holds(Map.of("mode", "IDLE")));
        assertTrue(new Predicate("x", "<", "limit").holds(Map.of("x", "3", "limit", "10")));
        assertThrows(IllegalArgumentException.class, () -> new Predicate("mode", "<", "idle").holds(Map.of("mode", "on")));
    }
}
